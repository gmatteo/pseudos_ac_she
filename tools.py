import sys
import os
import json
import numpy as np
import abipy.core.abinit_units as abu
import abipy.flowtk as flowtk

from abipy.core.structure import Structure

from abipy.flowtk.works import Work
from abipy.flowtk.flows import Flow
from abipy.flowtk.pseudos import Pseudo
from abipy.abio.inputs import AbinitInput


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


_AEDATA = None

def get_aedata():
    global _AEDATA
    if _AEDATA is not None:
        return _AEDATA

    _AEDATA = AeData()
    return _AEDATA


class AeData:

    def __init__(self):

        def parse_ae(path):
            a_ang, vols_ang, energies_ha = [], [], []
            with open(path, "rt") as fh:
                for line in fh:
                    if line.startswith("a"): continue
                    a, v, e = map(float, line.split())
                    a_ang.append(a)
                    vols_ang.append(v)
                    energies_ha.append(e)

            return dict(a_ang=a_ang, vols_ang=vols_ang, energies_ha=energies_ha)

        def parse_ox_ae(path):
            a_ang, c_ang, vols_ang, energies_ha = [], [], [], []
            #print(path)
            with open(path, "rt") as fh:
                for i, line in enumerate(fh):
                    print(line)
                    if line.startswith("a"): continue
                    tokens = line.split()
                    if len(tokens) == 4:
                        a, c, v, e = map(float, tokens)
                    elif len(tokens) == 3:
                        a, v, e = map(float, tokens)
                        c = a
                    else:
                        raise ValueError(f"Wrong line: {line} in path: {path}")
                    a_ang.append(a)
                    c_ang.append(c)
                    vols_ang.append(v)
                    energies_ha.append(e)

            return dict(a_ang=a_ang, c_ang=c_ang, vols_ang=vols_ang, energies_ha=energies_ha)


        self.unary_z = {}
        self.oxides_z = {}
        root = os.path.join(os.path.dirname(__file__), "AE_calcs")

        for basename in os.listdir(root):
            path = os.path.join(root, basename)
            if not path.endswith(".txt"): continue

            z = int(basename.split("_")[0])

            if path.endswith("_ox_ae.txt"):
                try:
                    data = parse_ox_ae(path)
                except Exception as exc:
                    print("Error in path", path)
                    raise exc
                self.unary_z[z] = data

            elif path.endswith("_ae.txt"):
                try:
                    data = parse_ae(path)
                except Exception as exc:
                    print("Error in path", path)
                    raise exc
                self.oxides_z[z] = data
            else:
                raise ValueError(f"Don't know how to handle file: {path}")


class MyFlow(Flow):

    @classmethod
    def from_pseudo_path(cls, pseudo_path: str):

        pseudo_path = os.path.abspath(pseudo_path)
        pseudo = Pseudo.from_file(pseudo_path)
        print(pseudo)

        root = os.path.dirname(pseudo_path)
        workdir = os.path.join(root, os.path.basename(pseudo_path) + "_flow")
        flow = cls(workdir=workdir)

        # Get initial hints from djrepo file.
        djrepo_path, _ = os.path.splitext(pseudo_path)
        flow.djrepo_path = djrepo_path + ".djrepo"
        with open(flow.djrepo_path) as fh:
            #d = json.load(fh)
            #flow.ecut_list = d["ecuts"]
            ppgen_hints = json.load(fh)["ppgen_hints"]
            ecut = ppgen_hints["high"]["ecut"] + 20
            #ecut = ppgen_hints["low"]["ecut"]


        flow.ecut_list = [ecut]

        print(f"running with ecut: {ecut}")
        symbol, z = pseudo.symbol, pseudo.Z
        key = f"{z}_{symbol}"
        a_bohr = AE_FCC_A0[key]
        a_ang = a_bohr * abu.Bohr_Ang

        relax_inp = make_input(pseudo, a_ang, relax=True)
        work = flowtk.Work()
        for ecut in flow.ecut_list:
            work.register_relax_task(relax_inp.new_with_vars(ecut=ecut))
        flow.register_work(work)

        scf_inp = make_input(pseudo, a_ang, relax=False)
        for ecut in flow.ecut_list:
            work = flowtk.Work()
            #work.register_relax_task(relax_inp.new_with_vars(ecut=ecut))

        return flow

    def on_all_ok(self):

        with open(self.djrepo_path, "r") as fh:
            in_data = json.load(fh)

        # Get relaxed lattice parameters as a function of ecut
        energies_ev, pressures_gpa = [], []
        for task in self.works[0]:
            with task.open_gsr() as gsr:
                energies_ev.append(float(gsr.energy))
                pressures_gpa.append(float(gsr.pressure))

        in_data["relax"] = dict(
            #ecut_list=self.ecut_list,
            energies_ev=energies_ev,
            pressure_gpa=pressures_gpa,
        )

        # Compute deltafactor as a function of ecut
        #for work in self.works[1:]:
        #    get_delta(work)

        # Update djrepo file.
        with open(self.djrepo_path, "w") as fh:
            json.dump(in_data, fh) #, indent=4)

        return True



def get_delta(work):
    num_sites = self._input_structure.num_sites
    etotals = self.read_etotals(unit="eV")

    d, eos_fit = dojo_dfact_results(self.dojo_pseudo, num_sites, self.volumes, etotals)

    print("[%s]" % self.dojo_pseudo.symbol, "eos_fit:", eos_fit)
    print("Ecut %.1f, dfact = %.3f meV, dfactprime %.3f meV" % (self.ecut, d["dfact_meV"], d["dfactprime_meV"]))

    self.add_entry_to_dojoreport(d)





def make_input(pseudo, a_ang, relax):

    lattice = float(a_ang) * np.array([
        0,  1,  1,
        1,  0,  1,
        1,  1,  0]) / np.sqrt(2.0)

    coords = [[0, 0, 0]]

    structure = Structure(lattice, species=[pseudo.symbol], coords=coords)

    # Initialize the input
    inp = AbinitInput(structure, pseudos=pseudo)

    nband = inp.num_valence_electrons // 2
    nband = max(np.ceil(nband * 1.2), nband + 10)

    spinat = [0, 0, 6]

    inp.set_vars(
        paral_kgb=0,
        #rmm_diis=1,
        nband=nband,
        # Occupation
        occopt=3, #Fermi-Dirac
        tsmear=0.001,
        #smdelta 2,
        ecutsm=0.5,
        nsppol=2,
        nspden=2,
        # SCF procedure
        iscf=17,
        nstep=1000,
        #ecut=ecut,
        spinat=spinat,
        tolvrs=1.0e-12,
        # k-point grid
        #ngkpt=[15, 15, 15],
        ngkpt=[1, 1, 1],
        nshiftk=1,
        shiftk=[0.0, 0.0, 0.0],
    )

    if relax:
        inp.set_vars(
            # optimization parameters
            optcell=2,
            ionmov=2,
            tolmxf=1.0e-6,
            dilatmx=1.1,
            #chkprim=0,
            #chkdilatmx=0,
        )

    return inp


if __name__ == "__main__":
    aedata = get_aedata()
