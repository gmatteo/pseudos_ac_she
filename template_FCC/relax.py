#!/usr/bin/env python

r"""
Relaxation Flow
===============

This example shows how to build a very simple Flow for the structural relaxation of SiC.
One could use a similar logic to perform multiple relaxations with different input parameters...
"""

import sys
import os
import json
import numpy as np

import abipy.abilab as abilab
#from abipy.core.structure import Structure
#import abipy.data as data
import abipy.flowtk as flowtk


AE_FCC_A0 = {
"85_At"	: 7.191602243,
"87_Fr"	: 10.385617352,
"88_Ra"	: 8.843815553,
"89_Ac"	: 7.593414710,
"90_Th"	: 6.758367409,
"91_Pa"	: 6.220412926,
"92_U"	: 5.903319246,
"93_Np"	: None,
"94_Pu"	:6.460780896,
"95_Am"	:6.923665533,
"96_Cm"	:6.661556739,
"97_Bk"	: None,
"98_Cf"	:6.203849952,
"99_Es"	: None,
"100_Fm":6.673581066,
"101_Md": None,
"102_No" :7.218033842,
"103_Lr" :6.607962216,
"104_Rf" :6.177085761,
"105_Db" :5.878951057,
"106_Sg" :5.655914411,
"107_Bh" :5.507431070,
"108_Hs" :5.424292569,
"109_Mt" :5.441005307,
"110_Ds" :5.574234778,
"111_Rg" :5.856726158,
"112_Cn" :7.440280753,
"113_Nh" :7.052079983,
"114_Fl" :7.089273573,
"115_Mc": None,
"116_Lv" :7.134838649,
"117_Ts": 7.455648006,
"118_Og": 9.610763498,
"119_Uue": 9.926738935,
"120_Ubn": 9.078847165,
}




def make_relax_input(pseudo_path):

    pseudo = abilab.Pseudo.from_file(pseudo_path)
    print(pseudo)

    djrepo_path, _ = os.path.splitext(pseudo_path)
    djrepo_path = djrepo_path + ".djrepo"
    with open(djrepo_path) as fh:
        ppgen_hints = json.load(fh)["ppgen_hints"]
        ecut = ppgen_hints["high"]["ecut"] + 10
        #ecut = ppgen_hints["high"]["ecut"] + 40

    print(f"running with ecut: {ecut}")
    symbol, z = pseudo.symbol, pseudo.Z
    key = f"{z}_{symbol}"
    a_bohr = AE_FCC_A0[key]
    import pymatgen.core.units as pmg_units
    a_ang = pmg_units.Length(a_bohr, "bohr").to("ang")

    lattice = float(a_ang) * np.array([
        0,  1,  1,
        1,  0,  1,
        1,  1,  0]) / np.sqrt(2.0)

    coords = [[0, 0, 0]]

    structure = abilab.Structure(lattice, species=[symbol], coords=coords)
    #structure = abilab.Structure.fcc(a_bohr, species=[symbol], units="bohr")

    # Initialize the input
    inp = abilab.AbinitInput(structure, pseudos=pseudo)

    nband = inp.num_valence_electrons // 2
    nband = max(np.ceil(nband * 1.2), nband + 10)

    spinat = [0, 0, 6]

    inp.set_vars(
        paral_kgb=0,
        rmm_diis=1,
        nband=nband,
        # Occupation
        occopt=3, #Fermi-Dirac
        tsmear=0.001,
        #smdelta 2,
        ecutsm=0.5,
        nsppol=2,
        nspden=2,
        # optimization parameters
        optcell=2,
        ionmov=2,
        tolmxf=1.0e-6,
        dilatmx=1.1,
        #chkprim=0,
        chkdilatmx=0,
        # SCF procedure
        #ixc 11
        iscf=17,
        nstep=1000,
        ecut=ecut,
        spinat=spinat,
        #ecut=60,
        tolvrs=1.0e-12,
        # k-point grid
        #kptopt=1,
        ngkpt=[15, 15, 15],
        nshiftk=1,
        shiftk=[0.0, 0.0, 0.0],
        )

    return inp


def build_flow(options):
    extra = options.extra
    if extra is None:
        raise RuntimeError("This script requires `-e PSEUDO_PATH`")
    pseudo_path = os.path.abspath(extra)
    relax_inp = make_relax_input(pseudo_path)

    root = os.path.dirname(pseudo_path)
    workdir = os.path.join(root, "FCC_RELAX_" + os.path.basename(pseudo_path))

    # Initialize the flow
    flow = flowtk.Flow(workdir=workdir)
    work = flowtk.Work()
    work.register_relax_task(relax_inp)
    flow.register_work(work)

    return flow


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())

