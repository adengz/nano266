__author__ = 'zhideng'

from monty.os import cd
import glob
import json

def get_cpu_time(h2_output_file="H2.nwout",
                 n2_output_file="N2.nwout",
                 nh3_output_file="H3N1.nwout"):
    output_files = [h2_output_file,n2_output_file,
                    nh3_output_file]
    cpu_time = 0
    for output in output_files:
        f = open(output,'r')
        lastline = f.readlines()[-1].split()
        cpu_time += float(lastline[3][:-1])
    return cpu_time

if __name__ == "__main__":
    with cd("Q5"):
        for dir_name in sorted(glob.glob("*")):
            with cd(dir_name):
                cpu_time = get_cpu_time()
                with open("cpu_time.json",'w') as jf:
                    json.dump(cpu_time,jf)
