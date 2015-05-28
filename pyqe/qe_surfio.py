__author__ = 'Zhi Deng'

from math import sqrt
import numpy as np

SURF = {'100':{'coords':np.array([[0.0, 0.0, 0.0],
                                  [0.5, 0.5, 0.0],
                                  [0.5, 0.0, 0.5],
                                  [0.0, 0.5, 0.5]]),
               'a':1.0, 'c':1.0},
        '111':{'coords':np.array([[0.0, 0.0, 0.0],
                                  [0.666667, 0.333333, 0.333333],
                                  [0.333333, 0.666667, 0.666667]]),
               'a':1/sqrt(2), 'c':sqrt(6)}}


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
    if miller_indices not in ['100', '111']:
        raise ValueError('Only 100 and 111 planes are supported.')
    nlayers = float(nslab + nvac)
    info = SURF[miller_indices]
    coords = info['coords'].copy()
    alat = a0 * info['a']
    calat = nlayers * info['c']
    coords[:, 2] = coords[:, 2] / nlayers
    pos = []
    for i in range(nslab):
        pos.extend(coords + [0, 0, i / nlayers])
    nat = len(pos)
    atompos = []
    for i, c in enumerate(pos):
        atompos.append("  Al %s %s %s" % tuple(c))
    atompos = "\n".join(atompos)
    conv_thr = 1e-6 * nat
    p = {'alat': alat, 'calat': calat, 'nslab': nslab, 'nvac': nvac,
         'k': 16, 'atompos': atompos, 'nat': nat, 'conv_thr': conv_thr}
    return p