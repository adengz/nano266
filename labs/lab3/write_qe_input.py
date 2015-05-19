__author__ = 'zhideng'

import os
import shutil
from monty.os import cd
from pymatgen.core.composition import Composition

PSP = {'Fe':'Fe.pbe-nd-rrkjus.UPF',
       'Pb':'Pb.pbe-dn-rrkjus_psl.0.2.2.UPF',
       'Ti':'Ti.pbe-sp-van_ak.UPF',
       'O':'O.pbe-n-rrkjus_psl.0.1.UPF',
       'Au':'Au.pbe-dn-rrkjus_psl.0.1.UPF',
       'Cu':'Cu.pbe-dn-rrkjus_psl.0.2.UPF'}

def write_tscc_script(jobname):
    t = '''#!/bin/bash
#PBS -q glean
#PBS -N {name}
#PBS -l nodes=1:ppn=4
#PBS -l walltime=1:00:00
#PBS -o job.out
#PBS -e job.err
#PBS -V
#PBS -M z4deng@ucsd.edu
#PBS -m abe
#PBS -A ong-group
#PBS -d /home/z4deng/nano266/labs/lab3/scratch/{name}

CURR_DIR=`pwd`

SCRATCH=/oasis/tscc/scratch/z4deng/{name}
mkdir $SCRATCH
cp * $SCRATCH
ln -s $SCRATCH scratch
cd $SCRATCH
mkdir tmp

mpirun -machinefile $PBS_NODEFILE -np 4 pw.x -inp {name}.pw.in > {name}.out

rm -r tmp
mv * $CURR_DIR
cd $CURR_DIR
rm scratch
rm -r $SCRATCH
'''
    with open('tscc_script','w') as f:
        f.write(t.format(name=jobname))

def write_input(template,params,xkeys):
    comp,latt = template.split('.')
    c = Composition(comp)
    elements = [e.symbol for e in c.elements]
    with open('../%s.pw.in.template' % template) as f:
        t = f.read()
    jobinfo = [comp,latt]
    for k in xkeys:
        jobinfo.append(str(params[k]))
    jobname = "_".join(jobinfo)
    os.makedirs(jobname)
    with cd(jobname):
        with open("%s.pw.in" % jobname, "w") as f:
            f.write(t.format(**params))
        for e in elements:
            shutil.copyfile('../../%s' % PSP[e],
                            './%s' % PSP[e])
        write_tscc_script(jobname)

if __name__ == '__main__':
    pass
