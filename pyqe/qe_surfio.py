__author__ = 'Zhi Deng'

from math import sqrt
import numpy as np

SURF = {'100':{'coords':np.array([[0.0, 0.0, 0.0],
                                  [0.5, 0.5, 0.0],
                                  [0.5, 0.0, 0.5],
                                  [0.0, 0.5, 0.5]]),
               'a':1.0, 'c':1.0, 'area':1.0},
        '111':{'coords':np.array([[0.0, 0.0, 0.0],
                                  [0.666667, 0.333333, 0.333333],
                                  [0.333333, 0.666667, 0.666667]]),
               'a':1/sqrt(2), 'c':sqrt(6), 'area':sqrt(3)/2}}


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
    alat = round(a0 * info['a'], 3)
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

def analyze_surf(analyzer, miller_indices, e_bulk):
    '''
    Update nslab, nvac, natom and surf_energy to the pd.DataFrame.
    :param analyzer: BasicAnalyzer object.
    :param miller_indices (str): Miller indices. Only '100' and '111' are
        supported.
    :param e_bulk (float): Bulk energy in meV/atom.
    :return: pd.df with surface related information
    '''
    df = analyzer.df
    filename = analyzer['filename']
    m = filename[0].split('_')[1]
    assert miller_indices == m
    info = SURF[miller_indices]
    natom = len(info['coords'])
    nslab = [int(f.split('_')[-2]) for f in filename]
    nvac = [int(f.split('_')[-1]) for f in filename]
    df['nslab'] = nslab
    df['nvac'] = nvac
    df['natom'] = natom * df['nslab']
    area = analyzer['alat'][0] ** 2 * info['area']
    df['surf_energy'] = 0.01602 / (2 * area) * \
                        (df['energy'] - df['natom'] * e_bulk)
    return df