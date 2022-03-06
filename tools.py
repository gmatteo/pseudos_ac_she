import sys
import os
import json
import numpy as np
import abipy.core.abinit_units as abu
import abipy.flowtk as flowtk

from monty.collections import AttrDict, dict2namedtuple
from abipy.core.structure import Structure
from abipy.flowtk.works import Work
from abipy.flowtk.flows import Flow
from abipy.flowtk.pseudos import Pseudo
from abipy.abio.inputs import AbinitInput
from deltafactor.eosfit import BM
from pymatgen.core.periodic_table import Element

from pseudo_dojo.util.dojo_eos import EOS
from pseudo_dojo.refdata.deltafactor import df_compute



AE_FCC_A0_BOHR = {
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
        for basename in os.listdir(root):
            path = os.path.join(root, basename)
            if not path.endswith(".txt"): continue

            # Use z instead of element becayse pymatgen element does not support z >= 120.
            z = int(basename.split("_")[0])
            #Element.from_Z(z)

            if path.endswith("_ae.txt") and not path.endswith("_ox_ae.txt"):
                self[z] = parse_ae(path)


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
        for a_ang in ae.alist_ang:
            print("a_ang", a_ang)
            scf_inp = make_input_unary(pseudo, a_ang, do_relax=False, ecut=ecut)
            work.register_scf_task(scf_inp)

        return work

    def get_deltafactor_entry(self):
        etotals = self.read_etotals(unit="eV")
        num_sites = 1
        volumes = [task.input.structure.volume for task in self]

        d, eos_fit = _dojo_dfact_results(self.dojo_pseudo, num_sites, volumes, etotals)
        print("[%s]" % self.dojo_pseudo.symbol, "eos_fit:", eos_fit)
        print("Ecut %.1f, dfact = %.3f meV, dfactprime %.3f meV" % (self.ecut, d["dfact_meV"], d["dfactprime_meV"]))

        dojo_ecut = "%.1f" % self.ecut
        return {dojo_ecut: d}


class DfEcutFlow(Flow):

    @classmethod
    def from_pseudo(cls, pseudo):

        print(pseudo)
        root = os.path.dirname(pseudo.filepath)
        workdir = os.path.join(root, os.path.basename(pseudo.filepath) + "_flow")
        flow = cls(workdir=workdir)

        # Get initial hints from djrepo file.
        djrepo_path, _ = os.path.splitext(pseudo.filepath)
        flow.djrepo_path = djrepo_path + ".djrepo"
        with open(flow.djrepo_path) as fh:
            d = json.load(fh)
            ppgen_hints = d["ppgen_hints"]
            #ecut = ppgen_hints["high"]["ecut"] + 20
            #ecut = ppgen_hints["low"]["ecut"]
            #flow.ecut_list = [ecut]
            flow.ecut_list = d["ecuts"]

        #print(f"running with ecut: {ecut}")
        #symbol, z = pseudo.symbol, pseudo.Z
        #key = f"{z}_{symbol}"
        #a_ang = AE_FCC_A0_BOHR[key] * abu.Bohr_Ang
        #relax_inp = make_input_unary(pseudo, a_ang, do_relax=True)
        #work = flowtk.Work()
        #for ecut in flow.ecut_list:
        #    work.register_relax_task(relax_inp.new_with_vars(ecut=ecut))
        #flow.register_work(work)

        #scf_inp = make_input_unary(pseudo, a_ang, do_relax=False)
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
        in_data["deltafactor"] = []
        for work in self.works:
            entry = work.get_deltafactor_entry()
            in_data["deltafactor"].append(entry)

        # Update djrepo file.
        print("in_data:\n", in_data)
        with open(self.djrepo_path, "w") as fh:
            #json.dump(in_data, fh) #, indent=4)
            from monty.json import MontyEncoder
            json.dump(in_data, fh, indent=-1, sort_keys=True, cls=MontyEncoder)

        return True


def make_input_unary(pseudo, a_ang, do_relax, ecut=None):

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
        nsppol=2,  # FIXME
        #nsppol=1,
        # SCF procedure
        iscf=17,
        nstep=1000,
        spinat=spinat,
        #tolvrs=1.0e-12,
        toldfe=1.0e-10,
        # k-point grid
        #ngkpt=[1, 1, 1],
        ngkpt=[15, 15, 15],  # FIXME
        nshiftk=1,
        shiftk=[0.0, 0.0, 0.0],
    )

    if do_relax:
        inp.set_vars(
            # optimization parameters
            optcell=2,
            ionmov=2,
            tolmxf=1.0e-6,
            dilatmx=1.1,
            #chkprim=0,
            #chkdilatmx=0,
        )

    if ecut is not None:
        inp["ecut"] = ecut

    return inp


def add_entry_to_dojoreport(self, entry, overwrite_data=False, pop_trial=False):
    """
    Write/update the DOJO_REPORT section of the pseudopotential.
    Important parameters such as the name of the dojo_trial and the energy cutoff
    are provided by the sub-class.
    Client code is responsible for preparing the dictionary with the data.

    Args:
        entry: Dictionary with results.
        overwrite_data: If False, the routine raises an exception if this entry is
            already filled.
        pop_trial: True if the trial should be removed before adding the new entry.
    """
    djrepo = self.djrepo_path
    self.history.info("Writing dojreport data to %s" % djrepo)

    # Update file content with Filelock.
    with FileLock(djrepo):
        # Read report from file.
        file_report = DojoReport.from_file(djrepo)

        # Create new entry if not already there
        dojo_trial = self.dojo_trial

        if pop_trial:
            file_report.pop(dojo_trial, None)

        if dojo_trial not in file_report:
            file_report[dojo_trial] = {}

        # Convert float to string with 1 decimal digit.
        dojo_ecut = "%.1f" % self.ecut

        # Check that we are not going to overwrite data.
        if dojo_ecut in file_report[dojo_trial]:
            if not overwrite_data:
                raise RuntimeError("dojo_ecut %s already exists in %s. Cannot overwrite data" %
                        (dojo_ecut, dojo_trial))
            else:
                file_report[dojo_trial].pop(dojo_ecut)

        # Update file_report by adding the new entry and write new file
        file_report[dojo_trial][dojo_ecut] = entry

        # Write new dojo report and update the pseudo attribute
        file_report.json_write()
        self._pseudo.dojo_report = file_report


if __name__ == "__main__":
    aedf_z = get_aedf_z()
