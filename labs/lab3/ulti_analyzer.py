__author__ = 'zhideng'

import pandas as pd
import numpy as np
from pymatgen.util.plotting_utils import get_publication_quality_plot

class UltiAnalyzer(object):

    def __init__(self, csv_file, e_scale):
        df = pd.read_csv(csv_file)
        d = {}
        for col_value in df.columns.values:
            d[col_value] = df[col_value].values
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':13605.7*e_scale,
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            d[k] *= v
        self._d = d
        self._df = df

    def __getitem__(self, key):
        return self._d[key]

    @property
    def dataframe(self):
        return self._df

    def get_converged_kgrid(self, tol=1):
        nkpts = self['nkpts']
        assert nkpts.max() != nkpts.min()
        e = self['energy']
        filename = self['filename']
        k = [int(f.split('.')[0].split('_')[2]) for f in filename]
        self._d['kgrid'] = np.array(k)
        ed = np.absolute(e[1:]-e[:-1])
        if ed[-1] > tol:
            raise ValueError('Not converged yet. Try larger k-point grid.')
        else:
            i = np.where(ed < tol)[0][0] + 1
            return k[i]

    def get_kgrid_plot(self, tol=1):
        ck = self.get_converged_kgrid(tol)
        print 'Convergence reached at %d' % ck
        plt = get_publication_quality_plot(8,6)
        k = self['kgrid']
        e = self['energy']
        plt.plot(k,e,'bo-',fillstyle='none')
        ax = plt.gca()
        xmin,xmax = ax.get_xlim()
        for b in [e[-1]-tol,e[-1]+tol]:
            plt.plot([xmin,xmax],[b,b],'k--',linewidth=2)
        plt.ylabel('Energy (meV/atom)')
        plt.xticks(k[::2])
        return plt

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




