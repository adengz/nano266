__author__ = 'Zhi Deng'

import os
import glob
import shutil
import numpy as np
from math import sqrt
from monty.os import cd
from pymatgen.core.composition import Composition

def _write_input_from_temp(template, jobname, params):
    '''
    Private method as the writer of QE input file.
    '''
    with open('%s.pw.in' % jobname, 'w') as f:
        f.write(template.format(**params))

def get_template(template):
    '''
    Method to initialize the template from file. 
    :param template (str): Template name (e.g., 'Cu.fcc')
    :return: template (str), structural info (list)
    '''
    with open('%s.pw.in.template' % template) as f:
        t = f.read()
    struc_info = template.split('.')
    return t, struc_info

def write_input(temp, params, xkeys, parr=True, func='pbe'):
    '''
    Method to write QE input file in scratch dir from template.
    :param temp (list): Returned from get_template() method.
    :param params (dict): Dict of parameters to pass into template. Keys
        are the strings within the placeholders in the template.
    :param xkeys ([str]): Parameters to distinguish between different
        input files.
    :param parr (bool): Whether use parallel mode (send the calculation
        to computational nodes). Default to True. Note in non-parallel
        (serial, run the calculation on login nodes), you need to cp the
        psp files into scratch dir.
    :param func (str): Functional used. Default to GGA. Refer to the
        format of filename of template files.
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

def get_slab_params(a0, miller_indices, nslab, nvac):
    '''
    Method to generate input parameters for Al slab calculations.
    :param a0 (float): Lattice constant of fcc Al at equilibrium.
    :param miller_indices (str): Miller indices. Only '100' and '111' are
        supported.
    :param nslab (int): Number of slab layers.
    :param nvac (int): Number of vacuum layers.
    :return: p (dict): Parameters dict to fill in the template. 
    '''
    nlayers = float(nslab + nvac)
    if miller_indices == '100':
        coords = np.array([[0.0, 0.0, 0.0],
                           [0.5, 0.5, 0.0],
                           [0.5, 0.0, 0.5],
                           [0.0, 0.5, 0.5]])
        alat = a0
        calat = nlayers
    elif miller_indices == '111':
        coords = np.array([[0.0, 0.0, 0.0],
                           [0.666667, 0.333333, 0.333333],
                           [0.333333, 0.666667, 0.666667]])
        alat = a0 / sqrt(2)
        calat = nlayers * sqrt(6)
    else:
        raise ValueError('Only 100 and 111 planes are supported.')
    coords[:, 2] = coords[:, 2] / nlayers
    ncoords = []
    for i in range(nslab):
        ncoords.extend(coords + [0, 0, i / nlayers])
    nat = len(ncoords)
    atompos = []
    for i, c in enumerate(ncoords):
        atompos.append("  Al %s %s %s" % tuple(c))
    atompos = "\n".join(atompos)
    conv_thr = 1e-6 * nat
    p = {'alat': alat, 'calat': calat, 'nslab': nslab, 'nvac': nvac,
         'k': 16, 'atompos': atompos, 'nat': nat, 'conv_thr': conv_thr}
    return p

if __name__ == '__main__':
    pass
