#!/usr/bin/env python


import os
from monty.os import cd
import numpy as np

def write_hcp_input(alat,calat,k1=13,k3=8):
    with open('Fe.hcp.pw.in.template') as f:
        template = f.read()
    s = template.format(alat=alat, calat=calat, k1=k1, k3=k3)
    jobname = "Fe_hcp_%s_%s" % (calat,alat)
    os.makedirs(jobname)
    with open("%s/%s.pw.in" % (jobname,jobname), "w") as f:
        f.write(s)

if __name__ == "__main__":
    with cd('scratch'):
        for alat in np.linspace(4.7,4.9,21):
            write_hcp_input(alat,1.71)

