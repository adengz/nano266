__author__ = 'zhideng'

import pandas as pd
import numpy as np
from pymatgen.util.plotting_utils import get_publication_quality_plot

class BasicAnalyzer(object):

    def __init__(self, csv_file, sorted_column, n_atoms=1):
        df = pd.read_csv(csv_file)
        ndf = df.sort(columns=sorted_column)
        d = {}
        for col_value in ndf.columns.values:
            d[col_value] = ndf[col_value].values
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':13605.7*n_atoms,
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            d[k] *= v
        nkpts = d['nkpts']
        #Detect k-point convergence or not
        if nkpts.max() != nkpts.min():
            k = [int(f.split('.')[0].split('_')[2]) for f in d['filename']]
        d['kgrid'] = np.array(k)
        self._d = d
        self._df = ndf

    def __getitem__(self, key):
        return self._d[key]

    @property
    def dataframe(self):
        return self._df

    def _get_best_alat_ind(self):
        e = self['energy']
        a = self['alat']
        assert a.max() != a.min()
        ind = int(np.where(e==e.min())[0])
        return ind

    @property
    def best_lat(self):
        i = self._get_best_alat_ind()
        return self['alat'][i], self['calat'][i]


def get_converged_kgrid(kgrid,energy,tol=1):
    ed = np.absolute(energy[1:]-energy[:-1])
    if ed[-1] > tol:
        raise ValueError('Not converged yet. Try larger k-point grid.')
    else:
        i = np.where(ed < tol)[0][0] + 1
        return kgrid[i]


