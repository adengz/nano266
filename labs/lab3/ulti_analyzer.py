__author__ = 'zhideng'

import pandas as pd
import numpy as np
from pymatgen.util.plotting_utils import get_publication_quality_plot

class BasicAnalyzer(object):

    def __init__(self, csv_file, sorted_column, n_atoms=1):
        df = pd.read_csv(csv_file)
        ndf = df.sort(columns=sorted_column)
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':13605.7*n_atoms,
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            ndf[k] *= v
        self._df = ndf

    def __getitem__(self, key):
        return self._df[key].values

    @property
    def dataframe(self):
        return self._df

def get_converged_kgrid(kgrid,energy,tol=1):
    ed = np.absolute(energy[1:]-energy[:-1])
    if ed[-1] > tol:
        raise ValueError('Not converged yet. Try larger k-point grid.')
    else:
        i = np.where(ed < tol)[0][0] + 1
        return kgrid[i]


