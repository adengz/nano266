__author__ = 'zhideng'

from pymatgen.io.nwchemio import NwInput, NwTask
import os
from monty.os import cd

H2 = NwInput.from_file('H2.nw').molecule
N2 = NwInput.from_file('N2.nw').molecule
NH3 = NwInput.from_file('NH3.nw').molecule

init_mols = [H2,N2,NH3]
basis_sets = ["6-31+G*","6-311+G*"]
functionals = ["HF","PBE","B3LYP"]

def write_task(molecule,functional,basis_set,operation):
    if functional == "HF":
        task = NwTask.from_molecule(molecule,
                                    theory="scf",
                                    basis_set=basis_set,
                                    operation=operation)
    elif functional == "PBE":
        task = NwTask.dft_task(molecule,
                               xc="xpbe96 cpbe96",
                               basis_set=basis_set,
                               operation=operation)
    elif functional == "B3LYP":
        task = NwTask.dft_task(molecule,
                               xc="b3lyp",
                               basis_set=basis_set,
                               operation=operation)
    return task

def write_input(geofreq_functional,geofreq_basisset,
                energy_functional,energy_basisset):
    for molecule in init_mols:
        tasks = []
        for operation in ["optimize","freq"]:
            tasks.append(write_task(molecule,
                                    geofreq_functional,
                                    geofreq_basisset,
                                    operation))
        tasks.append(write_task(molecule,
                                energy_functional,
                                energy_basisset,
                                "energy"))
        input_obj = NwInput(molecule,tasks,
                            memory_options="total 1000 mb")
        input_obj.write_file("%s.nw" %
                             molecule.formula.replace(' ', ''))

if __name__ == "__main__":
    i = 1
    with cd("Q5"):
        for energy_func in functionals:
            for energy_bs in basis_sets:
                for geofreq_func in functionals:
                    for geofreq_bs in basis_sets:
                        os.mkdir("%02d" % i)
                        with cd("%02d" % i):
                            write_input(geofreq_func,geofreq_bs,
                                        energy_func,energy_bs)
                        i += 1
