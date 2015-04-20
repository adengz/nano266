__author__ = 'zhideng'

from pymatgen.io.nwchemio import NwInput, NwOutput

class NWChemAnalyzer(object):

    def __init__(self,nh3_input,output_dict):
        self._input = nh3_input
        self._output_dict = output_dict
        self._task_inds = {"optimize":0,"energy":2}
        self._molecule_inds = {"H2":0,"N2":1,"NH3":2}

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
    def geofreq_functional(self):
        functional = self._get_functional("optimize")
        return functional

    @property
    def geofreq_basisset(self):
        basis_set = self._get_basis_set("optimize")
        return basis_set

    @property
    def energy_functional(self):
        functional = self._get_functional("energy")
        return functional

    @property
    def energy_basisset(self):
        basis_set = self._get_basis_set("energy")
        return basis_set