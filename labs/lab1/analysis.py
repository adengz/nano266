__author__ = 'zhideng'

from pymatgen.io.nwchemio import NwInput, NwOutput

class NWChemAnalyzer(object):

    def __init__(self,nh3_input,output_dict):
        self._input = nh3_input
        self._output_dict = output_dict
        self._task_inds = {"optimize":0,"energy":2}
        #self._molecule_inds = {"H2":0,"N2":1,"NH3":2}

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

    def _get_final_geometry(self, molecule):
        output = self._output_dict[molecule]
        mol = output.data[0]["molecules"][-1]
        return mol


    def _get_final_energy(self, molecule):
        output = self._output_dict[molecule]
        energy = output.data[2]["energies"][-1]
        return energy
