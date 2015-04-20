__author__ = 'zhideng'

from pymatgen.io.nwchemio import NwInput, NwOutput

class NWChemAnalyzer(object):

    def __init__(self,nh3_input,output_dict):
        self._input = nh3_input
        self._output_dict = output_dict
        self._task_inds = {"optimize":0,"energy":2}

    @classmethod
    def from_files(cls,nh3_input_file="H3N1.nw",
                   h2_output_file="H2.nwout",
                   n2_output_file="N2.nwout",
                   nh3_output_file="H3N1.nwout"):
        nh3_input = NwInput.from_file(nh3_input_file)
        output_dict = {"H2":NwOutput(h2_output_file),
                       "N2":NwOutput(n2_output_file),
                       "NH3":NwOutput(nh3_output_file)}
        return cls(nh3_input,output_dict)

    def _get_functional(self, operation):
        operation_task = self._input.tasks[self._task_inds[operation]]
        theory = operation_task.theory
        if theory == "scf":
            return "HF"
        elif theory == "dft":
            xc = operation_task.theory_directives["xc"]
            if xc == "xpbe96 cpbe96":
                return "PBE"
            elif xc == "b3lyp":
                return "B3LYP"

    def _get_basis_set(self, operation):
        operation_task = self._input.tasks[self._task_inds[operation]]
        basis_set = operation_task.basis_set["N"]
        return basis_set

    @property
    def input_parameters(self):
        input_parameters = {}
        for operation,name in zip(["optimize","energy"],
                       ["Geometry & Frequency","Energy"]):
            functional = self._get_functional(operation)
            basis_set = self._get_basis_set(operation)
            input_parameters.update({name:{"Functional":functional,
                                           "Basis Set":basis_set}})
        return input_parameters

    def _get_final_geometry(self, mol_name):
        output = self._output_dict[mol_name]
        mol = output.data[0]["molecules"][-1]
        return mol

    @property
    def final_geometry_parameters(self):
        final_mol = {}
        for mol_name in self._output_dict.keys():
            final_mol.update({mol_name:
                                  self._get_final_geometry(mol_name)})
        h2 = final_mol["H2"]
        h_h = h2.get_distance(0,1)
        n2 = final_mol["N2"]
        n_n = n2.get_distance(0,1)
        nh3 = final_mol["NH3"]
        n_h = 0
        for i in range(1,4):
            n_h += nh3.get_distance(0,i)
        n_h = n_h/3
        bond_lengths = {"H-H":h_h,"N-N":n_n,"N-H":n_h}
        h_n_h = 0
        for i,j in ((1,2),(2,3),(3,1)):
            h_n_h +=nh3.get_angle(i,0,j)
        h_n_h = h_n_h/3
        geometry_parameters = {"Bond Length":bond_lengths,
                               "Bond Angle":{"H-N-H":h_n_h}}
        return geometry_parameters

    def _get_final_energy(self, mol_name):
        output = self._output_dict[mol_name]
        energy = output.data[2]["energies"][-1]
        return energy

    @property
    def final_energies(self):
        final_energies = {}
        for mol_name in self._output_dict.keys():
            final_energies.update(
                {mol_name:self._get_final_energy(mol_name)})
        return final_energies

    def _get_thermal_correction(self, mol_name):
        output = self._output_dict[mol_name]
        corre = output.data[1]["corrections"]["Thermal correction to Enthalpy"]
        corre = corre*96.4869*0.0433634
        return corre

    @property
    def enthalpy_corrections(self):
        enthalpy_corrections = {}
        for mol_name in self._output_dict.keys():
            enthalpy_corrections.update(
                {mol_name:self._get_thermal_correction(mol_name)})
        return enthalpy_corrections

    @property
    def formation_enthalpy(self):
        energy = self.final_energies
        corre = self.enthalpy_corrections
        enthalpy = {}
        for mol_name in self._output_dict.keys():
            enthalpy.update(
                {mol_name:energy[mol_name].real+corre[mol_name].real})
        formation_enthalpy = 2*enthalpy["NH3"]-(3*enthalpy["H2"]+enthalpy["N2"])
        return formation_enthalpy

