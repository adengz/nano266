__author__ = 'zhideng'

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from pymatgen.util.plotting_utils import get_publication_quality_plot

class UltiAnalyzer(object):

    def __init__(self, csv_file):
        df = pd.read_csv(csv_file)
        d = {}
        for col_value in df.columns.values:
            d[col_value] = df[col_value].values
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':13605.7,
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            d[k] *= v
        #BCC
        if d['calat'][0] == 0:
            d['volume'] = d['alat']**3
        #HCP
        else:
            d['energy'] *= 0.5
            d['volume'] = 0.8660*d['calat']*d['alat']**3
        self._d = d
        self._df = df

    @property
    def dataframe(self):
        return self._df

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
    def best_lat(self):
        i = self._get_best_alat_ind()
        return self._d['alat'][i], self._d['calat'][i]




