__author__ = 'Zhi Deng'

import pandas as pd
import numpy as np
from pymatgen.util.plotting_utils import get_publication_quality_plot

class BasicAnalyzer(object):
    '''
    Class for further processing the output data from a csv file.
    The basic function is converting the total energy from Ry to
    meV, and the lattice constant from a.u. to angstrom.
    '''

    def __init__(self, csv_file, sorted_column=None, e_scale=1):
        '''
        Initializing the analyzer.
        :param csv_file (str): CSV file name.
        :param sorted_column (str): Ascending ort by this column name.
        :param e_scale (float): The factor of total energy in case
            various scales (meV/f.u. or meV/atom) are needed.
        :return:
        '''
        df = pd.read_csv(csv_file)
        ndf = df.sort(columns=sorted_column)
        factor = {'alat':0.5292,
                  'energy':13605.7*e_scale,
                  'total_force':13605.7/0.5292}
        for k,v in factor.items():
            ndf[k] *= v
        self._df = ndf

    def __getitem__(self, key):
        '''
        Returns a numpy array of certain column.
        :param key (str): Column name.
        :return: np.array
        '''
        return self._df[key].values

    @property
    def df(self):
        '''
        Return the processed pandas dataframe.
        :return:pd.df
        '''
        return self._df

    @property
    def emin_config(self):
        '''
        Show the minimum energy configuration.
        :return:pd.df
        '''
        i = self.df['energy'].idxmin()
        return self.df[i]


def analyze_kgrid(analyzer):
    '''
    Update the k-mesh to the padans dataframe.
    :param analyzer: BasicAnalyzer obj.
    :return:pd.df with new 'kgrid' column
    '''
    df = analyzer.df
    nkpts = df['nkpts']
    assert nkpts.max() != nkpts.min()
    k = [int(f.split('_')[-1]) for f in df['filename']]
    df['kgrid'] = k
    return df

def get_converged_param(df, x, y, tol=1):
    '''
    Method to perform the convergence test.
    :param df (pd.df): Pandas dataframe. For energy cutoff, use the df from
        analyzer. For others, you need to update the input parameter using
        appropriate analyze_*() method.
    :param x (str): Tested input parameter. Choose among ['nkpts','ecut',
        'nvac','nslab'].
    :param e (str): Energy option. Default to total energy.
    :param tol (float): Convergence criteria.
    :return:he input parameter at convergence
    '''
    assert df[x].max() != df[x].min()
    y = df[y].values
    #absolute and relative convergence
    abse = np.absolute(y[:-1]-y[-1])
    rele = np.absolute(y[1:]-y[:-1])
    if abse[-1] > tol:
        raise ValueError('Not converged yet. Try larger input parameter.')
    else:
        i = np.intersect1d(np.where(abse < tol)[0],
                           np.where(rele < tol)[0])[0] + 1
        return df[x].values[i]

def get_convergence_plot(df, x, y, tol=1):
    i = get_converged_param(df, x, y, tol)
    print i
    plt = get_publication_quality_plot(8,6)
    x = df[x].values
    y = df[y].values
    plt.plot(x, y, 'bo-', fillstyle='none')
    for e in [y[-1]-tol, y[-1]+tol]:
        plt.plot([x[0],x[-1]],[e,e],'k--',lw=2)
    plt.axvline(x=i,color='k',linestyle='dashed',lw=2)
    return plt

