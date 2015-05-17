__author__ = 'zhideng'

import pandas as pd
import numpy as np
from pymatgen.util.plotting_utils import get_publication_quality_plot

class BasicAnalyzer(object):

    def __init__(self, csv_file, sorted_column, e_scale=1):
        df = pd.read_csv(csv_file)
        ndf = df.sort(columns=sorted_column)
        factor = {'ecut':13.6057, 'alat':0.5292,
                  'energy':13605.7*e_scale,
                  'total_force':13.6057/0.5292}
        for k,v in factor.items():
            ndf[k] *= v
        self._df = ndf

    def __getitem__(self, key):
        return self._df[key].values

    @property
    def df(self):
        return self._df

def analyze_kgrid(analyzer):
    a = analyzer
    df = a.df
    nkpts = a['nkpts']
    assert nkpts.max() != nkpts.min()
    k = [int(f.split('.')[0].split('_')[2]) for f in a['filename']]
    df['kgrid'] = k
    return df

def get_converged_kgrid(df,tol=1):
    energy = df['energy'].values
    ed = np.absolute(energy[1:]-energy[:-1])
    if ed[-1] > tol:
        raise ValueError('Not converged yet. Try larger k-point grid.')
    else:
        i = np.where(ed < tol)[0][0] + 1
        return df['kgrid'].values[i]




