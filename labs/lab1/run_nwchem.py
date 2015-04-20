__author__ = 'zhideng'

import subprocess
import json
from monty.os import cd

def run_nwchem(dir_name):
    with cd(dir_name):
        cpu_time = 0
        for name in ["H2","N2","H3N1"]:
            subprocess.call(["nwchem", "%s.nw" % name, ">", "%s.nwout"])
            yield
            f = open("%s.nwout" % name)
            lastline = f.readlines()[-1]
            output = " ".join(lastline.split())
            cpu_time += float(output.split()[3][:-1])
        with open("job_info.json","w") as jf:
            json.dump(cpu_time,jf)
