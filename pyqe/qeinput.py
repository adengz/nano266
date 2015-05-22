__author__ = 'Zhi Deng'

import os
import glob
import shutil
from monty.os import cd
from pymatgen.core.composition import Composition

def _write_input_from_temp(template, jobname, params):
    '''
    Private method as the writer of QE input file.
    '''
    with open('%s.pw.in' % jobname, 'w') as f:
        f.write(template.format(**params))

def get_template(template):
    with open('%s.pw.in.template' % template) as f:
        t = f.read()
    struc_info = template.split('.')
    return t, struc_info

def write_input(temp, params, xkeys, func='pbe', parr=True):
    '''
    Method to write QE input file in scratch dir from template.
    :param temp (list): Returned from get_template() method.
    :param params (dict): Dict of parameters to pass into template. Keys
        are the strings within the placeholders in the template.
    :param xkeys ([str]): Parameters to distinguish between different
        inpur files.temwr
    :param func (str): Functional used. Default to GGA. Refer to the
        format of filename of template files.
    :param parr (bool): Whether use parallel mode (send the calculation
        to computational nodes). Default to True. Note in non-parallel
        (serial, run the calculation on login nodes), you need to cp the
        psp files into scratch dir.
    :return: None
    '''
    t, info = temp
    pl = [str(params[k]) for k in xkeys]
    jobname = "_".join(info+pl)
    if parr:
        c = Composition(info[0])
        elements = [e.symbol for e in c.elements]
        psp = {}
        for e in elements:
            psp[e] = os.path.abspath(glob.glob('../%s.%s*.UPF' % (e, func))[0])
        os.makedirs(jobname)
        with cd(jobname):
            _write_input_from_temp(t, jobname, params)
            for e in psp.keys():
                shutil.copyfile(psp[e],os.path.split(psp[e])[1])
    else:
        _write_input_from_temp(t, jobname, params)


if __name__ == '__main__':
    pass
