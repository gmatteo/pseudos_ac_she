#!/usr/bin/env python

r"""
===============

"""
import sys
import os
import argparse
import copy
import numpy as np
import logging
import abipy.abilab as abilab
import abipy.flowtk as flowtk

from monty.termcolor import cprint
from monty.functools import prof_main
from monty.os.path import find_exts
from tabulate import tabulate
from abipy.tools.plotting import get_ax_fig_plt, get_axarray_fig_plt
try:
    from abipy.tools.plotting import MplExpose as MplExposer, PanelExpose as PanelExposer
except ImportError:
    from abipy.tools.plotting import MplExposer, PanelExposer


from pseudo_dojo.core.pseudos import dojopseudo_from_file, DojoTable
from tools import DfEcutFlow, MyDojoReport

logger = logging.getLogger(__name__)


def dojo_rundf(options):

    for pseudo in options.pseudos:
        flow = DfEcutFlow.from_pseudo(pseudo)
        #print("# a, volume [Ang]")
        #for task in flow[0]:
        #    structure = task.input.structure
        #    print(structure.lattice.abc[0], structure.volume)
        #sys.exit(1)

        sched = flow.make_scheduler()
        print(sched)
        sched.start()

    return 0


def _plot_ae_eos_from_djrepo(djrepo, ax=None, show=False):
    df = djrepo.get_pdframe("deltafactor")
    df = df[["ecut", "dfact_meV", "dfactprime_meV", "v0", "b0_GPa", "b1"]]
    last_deltaf = df["dfact_meV"].values[-1]
    last_delta_prime = df["dfactprime_meV"].values[-1]
    #djrepo.basename
    text = f"Delta = {last_deltaf: .2f}, Delta' = {last_delta_prime: .2f} " + djrepo["basename"]
    fig = djrepo.plot_ae_eos(text=text, ax=ax, show=show)
    return fig


def _plot_from_djrepos(djrepo_list, pseudos, what):

    num_plots, ncols, nrows = len(djrepo_list), 1, 1
    if num_plots > 1:
        ncols = 1
        nrows = (num_plots // ncols) + (num_plots % ncols)

    ax_list, fig, plt = get_axarray_fig_plt(None, nrows=nrows, ncols=ncols,
                                            sharex=False, sharey=False, squeeze=False)

    ax_list = ax_list.ravel()
    if num_plots % ncols != 0: ax_list[-1].axis('off')

    for (ax, djrepo, pseudo) in zip(ax_list, djrepo_list, pseudos):
        if what == "eos":
            _plot_ae_eos_from_djrepo(djrepo, ax=ax, show=False)
        elif what == "conv":
            djrepo.plot_deltafactor_convergence(xc=pseudo.xc, what=("-dfact_meV", "-dfactprime_meV"), ax=ax, show=False)
        else:
            raise ValueError(f"Invalid what: {what})")

    fig.tight_layout()

    return fig


def dojo_plot(options):

    djrepo_list = []
    for pseudo in options.pseudos:
        path = pseudo.filepath.replace(".psp8", ".djrepo")
        djrepo = MyDojoReport.from_file(path)
        djrepo_list.append(djrepo)

        #df = djrepo.get_pdframe("deltafactor")
        #df = df[["ecut", "dfact_meV", "dfactprime_meV", "v0", "b0_GPa", "b1"]]
        #last_deltaf = df["dfact_meV"].values[-1]
        #last_delta_prime = df["dfactprime_meV"].values[-1]

    #with MplExposer() as e:
    with PanelExposer(title=path) as e:
        for djrepo in djrepo_list:
            e(_plot_ae_eos_from_djrepo(djrepo))
        for djrepo in djrepo_list:
            e(djrepo.plot_etotal_vs_ecut(show=False))
        for djrepo in djrepo_list:
            e(djrepo.plot_deltafactor_convergence(xc=pseudo.xc, what=("-dfact_meV", "-dfactprime_meV"), show=False))
        #e(djrepo.plot_ae_eos(text=f"Delta = {last_deltaf: .2f}, Delta' = {last_delta_prime: .2f}", show=False))
        #djrepo.plot_deltafactor_eos()

    return 0


def dojo_compare(options):
    """Compare DOJO results for multiple pseudos."""
    pseudos = options.pseudos

    dojo_table(options)

    djrepo_list = []
    for pseudo in pseudos:
        path = pseudo.filepath.replace(".psp8", ".djrepo")
        djrepo_list.append(MyDojoReport.from_file(path))

    #with MplExposer() as e:
    with PanelExposer(title="Compare Pseudos") as e:
        e(pseudos.dojo_compare(what=options.what_plot, show=False)[0])
        e(_plot_from_djrepos(djrepo_list, options.pseudos, "eos"))
        e(_plot_from_djrepos(djrepo_list, options.pseudos, "conv"))

    return 0


def dojo_table(options):
    """Build and show a pandas table."""
    pseudos = options.pseudos
    data, errors = pseudos.get_dojo_dataframe()
    if errors:
        cprint("get_dojo_dataframe returned %s errors" % len(errors), "red")
        if options.verbose:
            for i, e in enumerate(errors): print("[%s]" % i, e)

    if options.best:
        print("Selecting best pseudos according to deltafactor")
        best_frame = data.select_best()
        if options.json: best_frame.to_json('table.json')

        print(tabulate(best_frame, headers="keys"))
        print(tabulate(best_frame.describe(), headers="keys"))
        #best_frame["high_dfact_meV"].hist(bins=100)
        #import matplotlib.pyplot as plt
        #plt.show()
        return 0

    accuracies = ["normal", "high"]
    keys = ["dfact_meV", "dfactprime_meV", "v0", "b0_GPa", "b1", "ecut_deltafactor", "ecut_hint"]
    if options.json:
        accuracies = ["low", "normal", "high"]
        keys.append("phonon")

    columns = ["symbol"] + [acc + "_" + k for k in keys for acc in accuracies]

    #data = data[data["high_dfact_meV"] <= data["high_dfact_meV"].mean()]
    #data = data[data["high_dfact_meV"] <= 9]

    try:
        data["low_dfact_abserr"] = data["low_dfact_meV"] - data["high_dfact_meV"]
        data["normal_dfact_abserr"] = data["normal_dfact_meV"] - data["high_dfact_meV"]
        data["low_dfact_rerr"] = 100 * (data["low_dfact_meV"] - data["high_dfact_meV"]) / data["high_dfact_meV"]
        data["normal_dfact_rerr"] = 100 * (data["normal_dfact_meV"] - data["high_dfact_meV"]) / data["high_dfact_meV"]

        for k in ["v0", "b0_GPa", "b1"]:
            data["low_" + k + "_abserr"] = data["low_" + k] - data["high_" + k]
            data["normal_" + k + "_abserr"] = data["normal_" + k] - data["high_" + k]
            data["low_" + k + "_rerr"] = 100 * (data["low_" + k] - data["high_" + k]) / data["high_" + k]
            data["normal_" + k + "_rerr"] = 100 * (data["normal_" + k] - data["high_" + k]) / data["high_" + k]
    except Exception as exc:
        cprint("Python exception: %s" % type(exc), "red")
        if options.verbose: print(exc)

    try:
        wrong = data[data["high_b1"] < 0]
        if not wrong.empty:
            cprint("WRONG".center(80, "*"), "red")
            print(wrong)
    except Exception as exc:
        print(exc)

    if options.json: data.to_json('table.json')

    try:
        data = data[
                 [acc + "_dfact_meV" for acc in accuracies]
               + [acc + "_dfactprime_meV" for acc in accuracies]
               + [acc + "_ecut_deltafactor" for acc in accuracies]
               #+ [acc + "_gbrv_fcc_a0_rel_err" for acc in accuracies]
               #+ [acc + "_gbrv_bcc_a0_rel_err" for acc in accuracies]
               #+ [acc + "_abs_fcc" for acc in accuracies]
               #+ [acc + "_abs_bcc" for acc in accuracies]
               + [acc + "_ecut_hint" for acc in accuracies]
                   ]
    except KeyError:
        data = data[
                 [acc + "_dfact_meV" for acc in accuracies]
               + [acc + "_ecut_deltafactor" for acc in accuracies]
               + [acc + "_dfactprime_meV" for acc in accuracies]
               + [acc + "_ecut_hint" for acc in accuracies]
                   ]

    print("\nONCVPSP TABLE:\n")
    tablefmt = "grid"
    floatfmt = ".2f"

    columns = [acc + "_dfact_meV" for acc in accuracies]
    columns += [acc + "_ecut_deltafactor" for acc in accuracies]

    print(tabulate(data[columns], headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))
    if len(data) > 5:
        print(tabulate(data[columns].describe(), headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))

    """
    columns = [acc + "_dfactprime_meV" for acc in accuracies]
    columns += [acc + "_ecut_deltafactor" for acc in accuracies]
    print(tabulate(data[columns], headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))
    if len(data) > 5:
        print(tabulate(data[columns].describe(), headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))

    try:
        columns = [acc + "_gbrv_fcc_a0_rel_err" for acc in accuracies]
        columns += [acc + "_gbrv_bcc_a0_rel_err" for acc in accuracies]
        columns += [acc + "_abs_fcc" for acc in accuracies]
        columns += [acc + "_abs_bcc" for acc in accuracies]
        print(tabulate(data[columns], headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))
        if len(data) > 5:
            print(tabulate(data[columns].describe(), headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))
    except KeyError as exc:
        cprint('No GBRV data', "red")
        if options.verbose: print("Python exception:\n", str(exc))
    """

    columns = [acc + "_ecut_hint" for acc in accuracies]
    print(tabulate(data[columns], headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))
    if len(data) > 5:
        print(tabulate(data[columns].describe(), headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))

    #print(data.to_string(columns=columns))

    if len(data) > 5:
        bad = data[data["high_dfact_meV"] > data["high_dfact_meV"].mean() + data["high_dfact_meV"].std()]
        good = data[data["high_dfact_meV"] < data["high_dfact_meV"].mean()]
        print("\nPSEUDOS with high_dfact > mean plus one std (%.3f + %.3f):\n" % (
              data["high_dfact_meV"].mean(), data["high_dfact_meV"].std())) # ".center(80, "*"))
        print(tabulate(bad[["high_dfact_meV", "high_ecut_deltafactor"]], headers="keys",
             tablefmt=tablefmt, floatfmt=floatfmt))

    #gbrv_fcc_bad = data[data["high_gbrv_fcc_a0_rerr"] > (data["high_gbrv_fcc_a0_rerr"].abs()).mean()]
    #print("\nPSEUDOS with high_dfact > mean:\n") # ".center(80, "*"))
    #print(tabulate(bad, headers="keys", tablefmt=tablefmt, floatfmt=floatfmt))

    return 0


def main():
    def str_examples():
        return """\
Usage example:

    relax.py plot H.psp8                ==> Plot dojo data for pseudo H.psp8
    relax.py rundf H.psp8                ==> Plot dojo data for pseudo H.psp8
"""

    #relax.py compare H.psp8 H-low.psp8  ==> Plot and compare dojo data for pseudos H.psp8 and H-low.psp8
    #dojodata.py nbcompare H.psp8 H-low.psp8 ==> Plot and compare dojo data in ipython notebooks.
    #dojodata.py trials H.psp8 -r 1
    #dojodata.py table .                    ==> Build table (find all psp8 files within current directory)
    #dojodata.py figures .                  ==> Plot periodic table figures
    #dojodata.py notebook H.psp8            ==> Generate ipython notebook and open it in the browser
    #dojodata.py check table/*/*.psp8 -v --check-trials=gbrv_fcc,gbrv_bcc


    def show_examples_and_exit(err_msg=None, error_code=1):
        """Display the usage of the script."""
        sys.stderr.write(str_examples())
        if err_msg: sys.stderr.write("Fatal Error\n" + err_msg + "\n")
        sys.exit(error_code)

    def parse_rows(s):
        if not s: return []
        tokens = s.split(",")
        return list(map(int, tokens)) if tokens else []

    def parse_symbols(s):
        if not s: return []
        return s.split(",")

    # Parent parser for commands that need to know on which subset of pseudos we have to operate.
    copts_parser = argparse.ArgumentParser(add_help=False)
    copts_parser.add_argument('pseudos', nargs="+", help="Pseudopotential file or directory containing pseudos")
    copts_parser.add_argument('-s', "--symbols", type=parse_symbols,
        help=("List of chemical symbols to include or exclude."
              "Example --symbols=He,Li to include He and Li, --symbols=-He to exclude He"))
    copts_parser.add_argument('-v', '--verbose', default=0, action='count', # -vv --> verbose=2
                         help='Verbose, can be supplied multiple times to increase verbosity')

    copts_parser.add_argument('--loglevel', default="ERROR", type=str,
                        help="set the loglevel. Possible values: CRITICAL, ERROR (default), WARNING, INFO, DEBUG")
    copts_parser.add_argument('--no-colors', default=False, help='Disable ASCII colors')
    copts_parser.add_argument('--seaborn', action="store_true", help="Use seaborn settings")

    # Options for pseudo selection.
    group = copts_parser.add_mutually_exclusive_group()
    group.add_argument("-r", '--rows', default="", type=parse_rows, help="Select these rows of the periodic table.")
    group.add_argument("-f", '--family', type=str, default="", help="Select this family of the periodic table.")

    # Build the main parser.
    parser = argparse.ArgumentParser(epilog=str_examples(), formatter_class=argparse.RawDescriptionHelpFormatter)

    # Create the parsers for the sub-commands
    subparsers = parser.add_subparsers(dest='command', help='sub-command help', description="Valid subcommands")

    plot_options_parser = argparse.ArgumentParser(add_help=False)
    plot_options_parser.add_argument("-w", "--what-plot", type=str, default="all",
                                      help="Quantity to plot e.g df for deltafactor, gbrv for GBRV tests")
    plot_options_parser.add_argument("-e", "--eos", action="store_true", help="Plot EOS curve")

    p_rundf = subparsers.add_parser('rundf', parents=[copts_parser, plot_options_parser],
                                    help=dojo_plot.__doc__)

    # Subparser for plot command.
    p_plot = subparsers.add_parser('plot', parents=[copts_parser, plot_options_parser],
                                   help=dojo_plot.__doc__)

    # Subparser for notebook command.
    #p_notebook = subparsers.add_parser('notebook', parents=[copts_parser],
    #                                   help=dojo_notebook.__doc__)
    #parser.add_argument('--foreground', action='store_true', default=False,
    #                     help="Run jupyter notebook in the foreground.")
    #p_notebook.add_argument('--no-validation', action='store_true', default=False,
    #                         help="Don't add the validation cell.")
    #p_notebook.add_argument('--hide-code', action='store_true', default=False,
    #                        help="Add a cell that hides the raw code.")
    #p_notebook.add_argument('--no-tmp', action='store_true', default=False,
    #                        help="Don't use temporary file for notebook.")

    # Subparser for compare.
    p_compare = subparsers.add_parser('compare', parents=[copts_parser, plot_options_parser],
                                      help=dojo_compare.__doc__)

    p_compare.add_argument("-j", '--json', default=False, action="store_true",
                         help="Dump table in json format to file table.json")
    p_compare.add_argument("-b", '--best', default=False, action="store_true",
                         help="Select best pseudos according to deltafactor")


    # Subparser for nbcompare.
    #p_nbcompare = subparsers.add_parser('nbcompare', parents=[copts_parser, plot_options_parser],
    #                                    help=dojo_nbcompare.__doc__)

    # Subparser for figures
    #p_figures = subparsers.add_parser('figures', parents=[copts_parser], help=dojo_figures.__doc__)

    # Subparser for table command.
    p_table = subparsers.add_parser('table', parents=[copts_parser], help=dojo_table.__doc__)
    p_table.add_argument("-j", '--json', default=False, action="store_true",
                         help="Dump table in json format to file table.json")
    p_table.add_argument("-b", '--best', default=False, action="store_true",
                         help="Select best pseudos according to deltafactor")

    #p_nbtable = subparsers.add_parser('nbtable', parents=[copts_parser], help=dojo_nbtable.__doc__)

    # Subparser for check command.
    #def parse_trials(s):
    #    if s is None: return s
    #    return s.split(",")

    #p_check = subparsers.add_parser('check', parents=[copts_parser], help=dojo_check.__doc__)
    #p_check.add_argument("--check-trials", type=parse_trials, default=None, help="List of trials to check")

    # Subparser for validate command.
    #p_validate = subparsers.add_parser('validate', parents=[copts_parser], help=dojo_validate.__doc__)

    # Parse command line.
    try:
        options = parser.parse_args()
    except Exception as exc:
        show_examples_and_exit(error_code=1)

    # loglevel is bound to the string value obtained from the command line argument.
    # Convert to upper case to allow the user to specify --loglevel=DEBUG or --loglevel=debug
    #import logging
    #numeric_level = getattr(logging, options.loglevel.upper(), None)
    #if not isinstance(numeric_level, int):
    #    raise ValueError('Invalid log level: %s' % options.loglevel)
    #logging.basicConfig(level=numeric_level)

    #if options.no_colors:
    #    # Disable colors
    #    termcolor.enable(False)

    def get_pseudos(options):
        """
        Find pseudos in paths, return :class:`DojoTable` object sorted by atomic number Z.
        Accepts filepaths or directory.
        """
        exts = ("psp8", "xml")

        paths = options.pseudos

        if len(paths) == 1:
            # Handle directory argument
            if os.path.isdir(paths[0]):
                top = os.path.abspath(paths[0])
                paths = find_exts(top, exts, exclude_dirs="_*")
            # Handle glob syntax e.g. "./*.psp8"
            elif "*" in paths[0]:
                paths = glob.glob(paths[0])

        if options.verbose > 1: print("Will read pseudo from: %s" % paths)

        pseudos = []
        for p in paths:
            try:
                pseudo = dojopseudo_from_file(p)
                if pseudo is None:
                    cprint("[%s] Pseudo.from_file returned None. Something wrong in file!" % p, "red")
                    continue
                pseudos.append(pseudo)

            except Exception as exc:
                print(exc)
                cprint("[%s] Python exception. This pseudo will be ignored" % p, "red")
                if options.verbose: print(exc)

        table = DojoTable(pseudos)

        # Here we select a subset of pseudos according to family or rows
        if options.rows:
            table = table.select_rows(options.rows)
        elif options.family:
            table = table.select_families(options.family)

        # here we select chemical symbols.
        if options.symbols:
            table = table.select_symbols(options.symbols)

        return table.sort_by_z()

    # Build DojoTable from the paths specified by the user.
    options.pseudos = get_pseudos(options)
    if not options.pseudos:
        cprint("Empty pseudopotential list. Returning", "magenta")
        return 1
    if options.verbose: print(options.pseudos)

    if options.seaborn:
        import seaborn as sns
        sns.set(style="dark", palette="Set2")
        #sns.set(style='ticks', palette='Set2')
        #And to remove "chartjunk", do:
        #sns.despine()
        #plt.tight_layout()
        #sns.despine(offset=10, trim=True)

    # Dispatch
    return globals()["dojo_" + options.command](options)


if __name__ == "__main__":
    sys.exit(main())
