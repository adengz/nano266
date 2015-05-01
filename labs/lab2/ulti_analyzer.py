__author__ = 'zhideng'

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from pymatgen.util.plotting_utils import get_publication_quality_plot

class UltiAnalyzer(object):

    def __init__(self, csv_file, energy_scale='per_atom'):
        df = pd.read_csv(csv_file)
        self._d = {}
        for col_value in df.columns.values:
            self._d[col_value] = df[col_value].values
        ef = {'per_atom':13.6057/2,'per_cell':13.6057}
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':ef[energy_scale],
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            self._d[k] *= v
        self._d['volume'] = self._d['alat']**3/4.0

    @property
    def summ_dict(self):
        return self._d

    def get_plot(self, xkey, ykey):
        plt = get_publication_quality_plot(8,6)
        plt.plot(self._d[xkey], self._d[ykey],
                 'bo',fillstyle='none')
        return plt

    def _get_best_alat_ind(self):
        e = self._d['energy']
        a = self._d['alat']
        assert a.max() != a.min()
        ind = int(np.where(e==e.min())[0])
        return ind

    @property
    def best_alat(self):
        i = self._get_best_alat_ind()
        return self._d['alat'][i]

    def get_bulk_modulus(self, dv=0.01):
        e = self._d['energy']
        v = self._d['volume']
        i = self._get_best_alat_ind()
        f = interp1d(v,e,'quadratic')
        k = v[i]*(f(v[i]+2*dv)+f(v[i]-2*dv)-2*e[i])/(4*dv**2)
        return k*160.2




