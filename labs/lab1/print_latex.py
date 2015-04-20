__author__ = 'zhideng'

from analysis import NWChemAnalyzer
from pylatextable import LaTeXTable
from monty.os import cd
import glob

def get_row(option):
    na = NWChemAnalyzer.from_files()
    input_params = na.input_parameters
    row = []
    for operation in ["Geometry & Frequency","Energy"]:
        for item in ["Functional","Basis Set"]:
            row.append(input_params[operation][item])
    if option == "geometry":
        final_geo = na.final_geometry_parameters
        for bond in ["H-H","N-N","N-H"]:
            row.append("%.2f" % final_geo["Bond Length"][bond])
        row.append("%.2f" % final_geo["Bond Angle"]["H-N-H"])
    elif option == "energy":
        final_energy = na.final_energies
        for mol_name in ["H2","N2","NH3"]:
            row.append("%.2f" % final_energy[mol_name])
    elif option == "performance":
        enthalpy = na.formation_enthalpy
        row.append("%.2f" % enthalpy)
        cpu_time = na.cpu_time
        row.append(str(cpu_time))
    return row

if __name__ == "__main__":
    tb = LaTeXTable(["1"]*8)
    with cd("Q5"):
        for dir_name in sorted(glob.glob("*")):
            with cd(dir_name):
                row = get_row("geometry")
                tb.add_row(row)
    print tb
