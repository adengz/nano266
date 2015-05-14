#!/usr/bin/env python


import os
import shutil
from monty.os import cd
import numpy as np

def write_hcp_input(alat,calat,k1=13,k3=8):
    with open('../Fe.hcp.pw.in.template') as f:
        template = f.read()
    s = template.format(alat=alat, calat=calat, k1=k1, k3=k3)
    jobname = "Fe_hcp_%s_%s" % (calat,alat)
    os.makedirs(jobname)
    with open("%s/%s.pw.in" % (jobname,jobname), "w") as f:
        f.write(s)
    shutil.copyfile('../Fe.pbe-spn-kjpaw_psl.0.2.1.UPF',
                    '%s/Fe.pbe-spn-kjpaw_psl.0.2.1.UPF' % jobname)

if __name__ == "__main__":
    with cd('scratch'):
        write_hcp_input(4.8,1.71)

