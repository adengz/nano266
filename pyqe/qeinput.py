__author__ = 'Zhi Deng'

import os
import glob
import shutil
from monty.os import cd
from pymatgen.core.composition import Composition

def write_input(template,params,xkeys,func='pbe'):
    jobinfo = template.split('.')
    c = Composition(jobinfo[0])
    elements = [e.symbol for e in c.elements]
    with open('../%s.pw.in.template' % template) as f:
        t = f.read()
    for k in xkeys:
        jobinfo.append(str(params[k]))
    jobname = "_".join(jobinfo)
    os.makedirs(jobname)
    with cd(jobname):
        with open("%s.pw.in" % jobname, "w") as f:
            f.write(t.format(**params))
        for e in elements:
            psp = glob.glob('../../%s.%s*.UPF' % (e,func))[0]
            shutil.copyfile(psp,os.path.split(psp)[1])

if __name__ == '__main__':
    pass
