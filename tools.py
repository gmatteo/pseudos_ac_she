import os
import json
import numpy as np
import abipy.core.abinit_units as abu
import abipy.flowtk as flowtk

from monty.string import list_strings, is_string
from monty.collections import AttrDict, dict2namedtuple
from pymatgen.core.periodic_table import Element
from abipy.core.structure import Structure
from abipy.flowtk.works import Work
from abipy.flowtk.flows import Flow
from abipy.flowtk.pseudos import Pseudo
from abipy.abio.inputs import AbinitInput
from abipy.tools.plotting import add_fig_kwargs, get_ax_fig_plt
#from deltafactor.eosfit import BM
from pseudo_dojo.util.dojo_eos import EOS
from pseudo_dojo.core.dojoreport import DojoReport
from pseudo_dojo.refdata.deltafactor import df_compute



#AE_FCC_A0_BOHR = {
#"85_At"	: 7.191602243,
#"87_Fr"	: 10.385617352,
#"88_Ra"	: 8.843815553,
#"89_Ac"	: 7.593414710,
#"90_Th"	: 6.758367409,
#"91_Pa"	: 6.220412926,
#"92_U"	: 5.903319246,
#"93_Np"	: None,
#"94_Pu"	:6.460780896,
#"95_Am"	:6.923665533,
#"96_Cm"	:6.661556739,
#"97_Bk"	: None,
#"98_Cf"	:6.203849952,
#"99_Es"	: None,
#"100_Fm":6.673581066,
#"101_Md": None,
#"102_No" :7.218033842,
#"103_Lr" :6.607962216,
#"104_Rf" :6.177085761,
#"105_Db" :5.878951057,
#"106_Sg" :5.655914411,
#"107_Bh" :5.507431070,
#"108_Hs" :5.424292569,
#"109_Mt" :5.441005307,
#"110_Ds" :5.574234778,
#"111_Rg" :5.856726158,
#"112_Cn" :7.440280753,
#"113_Nh" :7.052079983,
#"114_Fl" :7.089273573,
#"115_Mc": None,
#"116_Lv" :7.134838649,
#"117_Ts": 7.455648006,
#"118_Og": 9.610763498,
#"119_Uue": 9.926738935,
#"120_Ubn": 9.078847165,
#}


_AEDF_Z = None


def get_aedf_z():
    global _AEDF_Z
    if _AEDF_Z is not None:
        return _AEDF_Z

    _AEDF_Z = AeDfZ()
    return _AEDF_Z


class AeDfZ(dict):

    def __init__(self):
        super().__init__()

        def parse_ae(path):
            try:
                data = np.loadtxt(path)
                data[:,2] *= abu.Ha_to_eV
                #volumes_ang = data[:,1]
                #v0 = volumes_ang[3]
                #for i in range(len(volumes_ang) - 1):
                #    delta = 100 * (volumes_ang[i+1] - volumes_ang[i]) / v0
                #    print(delta)

                d = dict(alist_ang=data[:,0], volumes_ang=data[:,1], etotals_ev=data[:,2])
                num_sites = 1
                eos_fit = EOS.DeltaFactor().fit(d["volumes_ang"] / num_sites, d["etotals_ev"] / num_sites)
                for k in ("e0", "v0", "b0", "b0_GPa", "b1"):
                    d[k] = getattr(eos_fit, k)
                return AttrDict(**d)

            except Exception as exc:
                print("Error in path", path)
                raise exc

        root = os.path.join(os.path.dirname(__file__), "AE_calcs")

        mag_file = os.path.join(root, "..", "Magnetization.txt")
        lines = open(mag_file, "rt").readlines()
        i = lines.index("<END JSON>\n")
        json_string = " ".join([l for l in lines[:i] if not l.startswith("#")])
        #print(json_string)
        mag = json.loads(json_string)
        mag_z = {}
        for k in mag:
            z = int(k.split("_")[0])
            mag_z[z] = mag[k]
        #print(mag_z)

        # For these elements, we use the non-magnetic configuration with suffix `_ae_NM.txt`.
        black_list = {
             #"94_ae.txt",
             #"96_ae.txt",
             "94_ae_NM.txt",
             "96_ae_NM.txt",
             "99_ae.txt",
             "100_ae.txt",
             "101_ae.txt",
             # New
             "91_ae.txt",
             "92_ae.txt",
             "93_ae.txt",
             #"98_ae.txt",
             "98_ae_NM.txt",  # Use magnetic config for 98_Cf
             "113_ae.txt",
             "117_ae.txt",
             "118_ae.txt",
        }

        for basename in os.listdir(root):
            path = os.path.join(root, basename)
            if not path.endswith(".txt"): continue
            if basename in black_list: continue

            # Use z instead of element because pymatgen element does not support z >= 120.
            z = int(basename.split("_")[0])
            #Element.from_Z(z)

            if (path.endswith("_ae.txt") or path.endswith("_ae_NM.txt")) and not path.endswith("_ox_ae.txt"):
                if z in self:
                    raise ValueError(f"Found multiple files for z: {z}")

                self[z] = parse_ae(path)
                self[z]["mag"] = mag_z.get(z, 0.0)
                #if z == 94:
                #    print("Parsing path", path)
                #    print(self[z])


#if path.endswith("_ox_ae.txt"):
#    try:
#        data = parse_ox_ae(path)
#    except Exception as exc:
#        print("Error in path", path)
#        raise exc
#    self.unary_z[z] = data
#
#    # volumes in A^3/atom and energies in eV/atom,
#
#    natom = 1
#    array = np.stack((data["volumes_ang"], data["etotals_ev"] ), axis=-1) / natom
#    volume, bulk_modulus, bulk_deriv, residuals = BM(array)
#
#
#

#def parse_ox_ae(path):
#    a_ang, c_ang, vols_ang, etotals_ev = [], [], [], []
#    with open(path, "rt") as fh:
#        for i, line in enumerate(fh):
#            print(line)
#            if line.startswith("a"): continue
#            tokens = line.split()
#            if len(tokens) == 4:
#                a, c, v, e = map(float, tokens)
#            elif len(tokens) == 3:
#                a, v, e = map(float, tokens)
#                c = a
#            else:
#                raise ValueError(f"Wrong line: {line} in path: {path}")
#            a_ang.append(a)
#            c_ang.append(c)
#            vols_ang.append(v)
#            etotals_ev.append(e)
#
#    d = dict(a_ang=a_ang, c_ang=c_ang, vols_ang=vols_ang, etotals_ev=etotals_ev)
#    for k in d:
#        d[k] = np.array(d[k])
#    return d


def _dojo_dfact_results(pseudo, num_sites, volumes, etotals):
    """
    This function computes the deltafactor and returns the dictionary to be inserted
    in the dojoreport file.

    Args:
        pseudo: Pseudopotential object.
        num_sites: Number of sites in unit cell
        volumes: List with unit cell volumes in Ang**3
        etotals: List of total energies in eV.

    Return:
        (dojo_entry, eos_fit)
        where dojo_entry is the Dictionary with results to be inserted in the djrepo file.
        eos_fit is the object storing the results of the EOS fit.
    """
    nan = float('NaN')

    dojo_entry = dict(
        etotals=list(etotals),
        volumes=list(volumes),
        num_sites=num_sites,
        dfact_meV=nan,
        dfactprime_meV=nan,
        v0=nan,
        b0=nan,
        b0_GPa=nan,
        b1=nan,
    )

    volumes, etotals = np.asarray(volumes), np.asarray(etotals)
    eos_fit = None
    try:
        # Use same fit as the one employed for the deltafactor.
        eos_fit = EOS.DeltaFactor().fit(volumes/num_sites, etotals/num_sites)

        # Get AE reference results (Wien2K).
        #wien2k = df_database(pseudo.xc).get_entry(pseudo.symbol)
        ae = get_aedf_z()[pseudo.Z]

        # Compute deltafactor estimator.
        dfact = df_compute(ae.v0, ae.b0_GPa, ae.b1,
                           eos_fit.v0, eos_fit.b0_GPa, eos_fit.b1, b0_GPa=True)

        dfactprime_meV = dfact * (30 * 100) / (eos_fit.v0 * eos_fit.b0_GPa)

        dfres = {
            "dfact_meV": dfact,
            "dfactprime_meV": dfactprime_meV,
            "v0": eos_fit.v0,
            "b0": eos_fit.b0,
            "b0_GPa": eos_fit.b0_GPa,
            "b1": eos_fit.b1,
        }

        for k, v in dfres.items():
            v = v if not isinstance(v, complex) else nan
            dfres[k] = v

        dojo_entry.update(dfres)

    except EOS.Error as exc:
        dojo_entry["_exceptions"] = str(exc)

    return dojo_entry, eos_fit


class DeltaUnaryWork(Work):

    @classmethod
    def from_pseudo_ecut(cls, pseudo, ecut):
        work = cls()
        work.dojo_pseudo = pseudo
        work.ecut = float(ecut)
        symbol, z = pseudo.symbol, pseudo.Z
        #key = f"{z}_{symbol}"
        #a_ang = AE_FCC_A0_BOHR[key] * abu.Bohr_Ang

        ae = get_aedf_z()[pseudo.Z]

        #connect = True
        connect = False

        for a_ang in ae.alist_ang:
            #print("a_ang", a_ang)
            scf_inp = make_input_unary(pseudo, a_ang, ae["mag"], do_relax=False, ecut=ecut)
            if connect: scf_inp["prtwf"] = 1
            work.register_scf_task(scf_inp)

        if connect:
            middle = len(work) // 2
            filetype = "WFK"
            for i, task in enumerate(work[:middle]):
                #task.add_deps({work[i + 1]: filetype})
                task.add_deps({work[middle]: filetype})

            for i, task in enumerate(work[middle+1:]):
                #task.add_deps({work[middle + i]: filetype})
                task.add_deps({work[middle]: filetype})

        return work

    def get_deltafactor_entry(self):
        #etotals = self.read_etotals(unit="eV")
        etotals, mag_list = [], []

        for task in self:
            with task.open_gsr() as gsr:
                etot = gsr.reader.read_value("etotal") * abu.Ha_eV
                etotals.append(etot)
                mag_list.append(gsr.ebands.get_collinear_mag())

        num_sites = 1
        volumes = [task.input.structure.volume for task in self]

        d, eos_fit = _dojo_dfact_results(self.dojo_pseudo, num_sites, volumes, etotals)
        print("[%s]" % self.dojo_pseudo.symbol, "eos_fit:", eos_fit)
        print("Ecut %.1f, dfact = %.3f meV, dfactprime %.3f meV" % (self.ecut, d["dfact_meV"], d["dfactprime_meV"]))
        #print("mag_list:", mag_list)
        d["mag_list"] = mag_list

        dojo_ecut = "%.1f" % self.ecut
        return {dojo_ecut: d}


class DfEcutFlow(Flow):

    @classmethod
    def from_pseudo(cls, pseudo):

        #print(pseudo)
        root = os.path.dirname(pseudo.filepath)
        workdir = os.path.join(root, os.path.basename(pseudo.filepath) + "_flow")
        flow = cls(workdir=workdir)

        # Get initial hints from djrepo file.
        djrepo_path, _ = os.path.splitext(pseudo.filepath)
        flow.djrepo_path = djrepo_path + ".djrepo"
        with open(flow.djrepo_path) as fh:
            d = json.load(fh)
            ppgen_hints = d["ppgen_hints"]
            flow.ecut_list = d["ecuts"]

        #print(f"running with ecut: {ecut}")
        #symbol, z = pseudo.symbol, pseudo.Z
        #key = f"{z}_{symbol}"
        #a_ang = AE_FCC_A0_BOHR[key] * abu.Bohr_Ang
        #relax_inp = make_input_unary(pseudo, a_ang, mag, do_relax=True)
        #work = flowtk.Work()
        #for ecut in flow.ecut_list:
        #    work.register_relax_task(relax_inp.new_with_vars(ecut=ecut))
        #flow.register_work(work)

        for ecut in flow.ecut_list:
            flow.register_work(DeltaUnaryWork.from_pseudo_ecut(pseudo, ecut))

        return flow

    def on_all_ok(self):

        with open(self.djrepo_path, "r") as fh:
            in_data = json.load(fh)

        # Get relaxed lattice parameters as a function of ecut
        #etotals_ev, pressures_gpa = [], []
        #for task in self.works[0]:
        #    with task.open_gsr() as gsr:
        #        etotals_ev.append(float(gsr.energy))
        #        pressures_gpa.append(float(gsr.pressure))

        #in_data["relax"] = dict(
        #    #ecut_list=self.ecut_list,
        #    etotals_ev=etotals_ev,
        #    pressure_gpa=pressures_gpa,
        #)

        # Compute deltafactor as a function of ecut
        in_data["deltafactor"] = out = {}
        for work in self.works:
            entry = work.get_deltafactor_entry()
            out.update(entry)

        # Update djrepo file.
        with open(self.djrepo_path, "w") as fh:
            from monty.json import MontyEncoder
            json.dump(in_data, fh, indent=-1, sort_keys=True, cls=MontyEncoder)

        return True


def make_input_unary(pseudo, a_ang, mag, do_relax=False, ecut=None):

    lattice = float(a_ang) * np.array([
        0,  1,  1,
        1,  0,  1,
        1,  1,  0]) / np.sqrt(2.0)

    coords = [[0, 0, 0]]

    structure = Structure(lattice, species=[pseudo.symbol], coords=coords)
    #print(structure.volue, float(a_ang) **3 * 2**(-1/2))

    # Initialize the input
    inp = AbinitInput(structure, pseudos=pseudo)

    #if pseudo.symbol in ("Ra", "Fm", "Cn", "Ts", "Og"):
    #    print(f"Setting mag to None for {pseudo.symbol=}")
    #    mag = None

    if mag == 0.0:
        nsppol, spinat = 1, None
        #nsppol, spinat = 2, [0, 0, 8]
    else:
        nsppol = 2
        if mag is None:
            #spinat = [0, 0, 6]
            spinat = [0, 0, 8]
        else:
            spinat = [0, 0, mag]
            #spinat = [0, 0, 8]

    print(f"Using nsppol: {nsppol} with spinat {spinat}")

    nband = inp.num_valence_electrons // 2
    nband = max(np.ceil(nband * 1.2), nband + 10)

    ngkpt = [15, 15, 15]
    #if pseudo.symbol in ("Bk", "Fm", "Md", "Nh"):
    #    # Calculations done by BANDS developers with densified sampling.
    #    ngkpt = [17, 17, 17]
    #    print("Using densified ngkpt", ngkpt, "for symbol:", pseudo.symbol)

    inp.set_vars(
        paral_kgb=0,
        #rmm_diis=1,
        nband=nband,
        # Occupation
        occopt=3, # Fermi-Dirac
        tsmear=0.001,
        #smdelta 2,
        ecutsm=0.5,
        # SCF procedure
        iscf=17,
        nstep=1000,
        nsppol=nsppol,
        spinat=spinat,
        # k-point grid
        ngkpt=ngkpt,
        nshiftk=1,
        shiftk=[0.0, 0.0, 0.0],
        prtwf=0,
    )

    if do_relax:
        inp.set_vars(
            # optimization parameters
            optcell=2,
            ionmov=2,
            tolmxf=1.0e-6,
            tolvrs=1.0e-12,
            dilatmx=1.1,
        )
    else:
        inp.set_vars(
            toldfe=1.0e-10,
        )

    if ecut is not None:
        inp["ecut"] = ecut

    return inp


class MyDojoReport(DojoReport):

    @add_fig_kwargs
    def plot_deltafactor_convergence(self, xc, code="WIEN2k", with_soc=False, what=None, ax_list=None, **kwargs):
        """
        Plot the convergence of the deltafactor parameters wrt ecut.

        Args:
            xc: String or XcFunc object specifying the XC functional. E.g "PBE" or XcFunc.from_name("PBE")
            code: Reference code.
            with_soc: If True, the results obtained with SOC are plotted (if available).
            what:
            ax_list: List of matplotlib Axes, if ax_list is None a new figure is created

        Returns:
            `matplotlib` figure or None if the deltafactor test is not present
        """
        trial = "deltafactor" if not with_soc else "deltafactor_soc"
        if trial not in self:
            cprint("dojo report does not contain trial: %s" % str(trial), "red")
            return None

        all_keys = ["dfact_meV", "dfactprime_meV", "v0", "b0_GPa", "b1"]
        if what is None:
            keys = all_keys
        else:
            what = list_strings(what)
            if what[0].startswith("-"):
                # Exclude keys
                what = [w[1:] for w in what]
                keys = [k for k in all_keys if k not in what]
            else:
                keys = what

        # Get reference entry
        #reference = df_database(xc=xc).get_entry(symbol=self.symbol, code=code)
        element = Element[self.symbol]
        reference = get_aedf_z()[element.Z]
        #print("Reference data:", reference)

        # Get DataFrame.
        frame = self.get_pdframe(trial, *keys)
        ecuts = np.array(frame["ecut"])

        import matplotlib.pyplot as plt
        if ax_list is None:
            fig, ax_list = plt.subplots(nrows=len(keys), ncols=1, sharex=True, squeeze=False)
            ax_list = ax_list.ravel()
        else:
            fig = plt.gcf()

        if len(keys) != len(ax_list):
            raise ValueError("len(keys)=%s != len(ax_list)=%s" % (len(keys), len(ax_list)))

        for i, (ax, key) in enumerate(zip(ax_list, keys)):
            values = np.array(frame[key])
            refval = getattr(reference, key)
            # Plot difference pseudo - ref.
            #print("ecuts", ecuts, "values", values)
            psmae_diff = values - refval
            ax.plot(ecuts, psmae_diff, "o-")

            # Add vertical lines at hints.
            if self.has_hints:
                vmin, vmax = psmae_diff.min(), psmae_diff.max()
                for acc in self.ALL_ACCURACIES:
                    ax.vlines(self["hints"][acc]["ecut"], vmin, vmax,
                              colors=self.ACC2COLOR[acc], linestyles="dashed")

            ax.grid(True)
            ax.set_ylabel(r"$\Delta$" + key)
            if i == len(keys) - 1: ax.set_xlabel("Ecut [Ha]")

            xmin, xmax = min(ecuts), max(ecuts)
            if key == "dfactprime_meV":
                # Add horizontal lines (used to find hints for ecut).
                last = values[-1]
                for pad, acc in zip(self.ATOLS, self.ALL_ACCURACIES):
                    color = self.ACC2COLOR[acc]
                    ax.hlines(y=last + pad, xmin=xmin, xmax=xmax, colors=color, linewidth=1.5, linestyles='dashed')
                    ax.hlines(y=last - pad, xmin=xmin, xmax=xmax, colors=color, linewidth=1.5, linestyles='dashed')
                # Set proper limits so that we focus on the relevant region.
                #ax.set_ylim(last - 1.1*self.ATOLS[0], last + 1.1*self.ATOLS[0])
            else:
                ax.hlines(y=0., xmin=xmin, xmax=xmax, colors="black", linewidth=2, linestyles='dashed')

        plt.tight_layout()

        return fig

    @add_fig_kwargs
    def plot_ae_eos(self, ax=None, text=None, cmap="jet", **kwargs):

        ax, fig, plt = get_ax_fig_plt(ax)
        cmap = plt.get_cmap(cmap)

        ppgen_ecuts = set([self["ppgen_hints"][acc]["ecut"] for acc in ("low", "normal", "high")])

        # Get DataFrame.
        trial = "deltafactor" #if not with_soc else "deltafactor_soc"
        frame = self.get_pdframe(trial, "num_sites", "volumes", "etotals")
        ecuts = frame["ecut"]
        num_sites = np.array(frame["num_sites"])
        assert np.all(num_sites == num_sites[0])
        num_sites = num_sites[0]

        # Get reference entry
        #reference = df_database(xc=xc).get_entry(symbol=self.symbol, code=code)
        element = Element[self.symbol]
        reference = get_aedf_z()[element.Z]
        #print("Reference data:", reference)

        ys = reference.etotals_ev - np.min(reference.etotals_ev)
        #ax.plot(reference.volumes_ang, ys, label="AE1")

        # Use same fit as the one employed for the deltafactor.
        eos_fit = EOS.DeltaFactor().fit(reference.volumes_ang/num_sites, ys/num_sites)
        eos_fit.plot(ax=ax, text=False, label="AE", color="k", marker="^", alpha=1, show=False)

        for i, ecut in enumerate(ecuts):
            #if ecut not in ppgen_ecuts: continue
            #if i not in (0, len(ecuts) -1): continue
            if i not in (2, len(ecuts) -1): continue

            # Subframe with this value of ecut.
            ecut_frame = frame.loc[frame["ecut"] == ecut]
            assert ecut_frame.shape[0] == 1
            # Extract volumes and energies for this ecut.
            volumes = (np.array(list(ecut_frame["volumes"].values), dtype=float)).flatten()
            etotals = (np.array(list(ecut_frame["etotals"].values), dtype=float)).flatten()

            ys = etotals - etotals.min()
            #ax.plot(volumes, ys)

            # Use same fit as the one employed for the deltafactor.
            eos_fit = EOS.DeltaFactor().fit(volumes/num_sites, ys/num_sites)
            eos_fit.plot(ax=ax, text=False, label="ecut %.1f" % ecut, color=cmap(i/len(ecuts), alpha=0.8), show=False)

        ax.grid(True)
        if text is not None:
            ax.set_title(text)
        ax.legend(loc='best', shadow=True, frameon=True) #fancybox=True)

        return fig


def check_data(z, data, verbose=0):
    from pymatgen.core.lattice import Lattice
    tol = 1e-4
    if verbose: print(f"Testing volume for z: {z} with tol: {tol}")
    for a_ang, vol in zip(data["alist_ang"], data["volumes_ang"]):
        lattice = float(a_ang) * np.array([
            0,  1,  1,
            1,  0,  1,
            1,  1,  0]) / np.sqrt(2.0)
        lattice = Lattice(lattice)

        # V = l**3 2 * (-1/2)
        #print(lattice.volume, float(a_ang) **3 * 2**(-1/2))
        #print(lattice.volume * np.sqrt(2),  float(a_ang) ** 3)
        #print(lattice.volume ** (1/3) * (2 ** (1/6)), float(a_ang))
        #print(float(a_ang) / lattice.volume ** 1/3)

        adiff = abs(vol - lattice.volume)
        print("adiff:", adiff)
        if adiff > tol:
            print(f"Inexact a/vol for z: {z}: volume from file:", vol, ", volume from a", lattice.volume, "adiff", adiff)

if __name__ == "__main__":
    from pprint import pprint, pformat
    aedf_z = get_aedf_z()
    for z, data in aedf_z.items():
        print("Checking z:", z) #, pformat(data))
        check_data(z, data, verbose=0)
