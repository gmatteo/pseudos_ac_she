#!/usr/bin/env python

import sys
import os
import numpy as np

from pseudo_dojo.util.dojo_eos import EOS
from pseudo_dojo.refdata.deltafactor import df_compute


def main():
    path = sys.argv[1]

    # V [ang3]       AE (ev)             Abinit (eV)
    data = np.loadtxt(path)
    volumes, ae_enes, ps_enes = data[:, 0], data[:, 1], data[:, 2]
    ae_enes = ae_enes - ae_enes.min()
    ps_enes = ps_enes - ps_enes.min()
    num_sites = 1

    ae_fit = EOS.DeltaFactor().fit(volumes/num_sites, ae_enes/num_sites)
    print("ae_fit:\n", ae_fit)
    ps_fit = EOS.DeltaFactor().fit(volumes/num_sites, ps_enes/num_sites)
    print("ps_fit:\n", ps_fit)

    # Compute deltafactor estimator.
    dfact = df_compute(ae_fit.v0, ae_fit.b0_GPa, ae_fit.b1,
                       ps_fit.v0, ps_fit.b0_GPa, ps_fit.b1, b0_GPa=True)

    dfactprime_meV = dfact * (30 * 100) / (ps_fit.v0 * ps_fit.b0_GPa)

    s = f"deltafactor: {dfact: .2f}"
    print(s)

    from abipy.tools.plotting import add_fig_kwargs, get_ax_fig_plt
    ax, fig, plt = get_ax_fig_plt(ax=None)
    ax.set_title(s)
    ae_fit.plot(ax=ax, label="AE", color="r", text=False, show=False)
    ps_fit.plot(ax=ax, label="PS", color="b")


    #dfres = {
    #    "dfact_meV": dfact,
    #    "dfactprime_meV": dfactprime_meV,
    #    "v0": ps_fit.v0,
    #    "b0": ps_fit.b0,
    #    "b0_GPa": ps_fit.b0_GPa,
    #    "b1": ps_fit.b1,
    #}


if __name__ == "__main__":
    sys.exit(main())

