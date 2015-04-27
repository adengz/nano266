__author__ = 'zhideng'

import pandas as pd
from pymatgen.util.plotting_utils import get_publication_quality_plot

class UltiAnalyzer(object):

    def __init__(self, csv_file):
        df = pd.read_csv(csv_file)
        self._summ_dict = {}
        for col_value in df.columns.values:
            self._summ_dict[col_value] = df[col_value].values
        factor = {"ecut":13.6057, "alat":0.5292,
                  "energy":13.6057*1000/2, "total_force":13.6057/0.5292}
        for k,v in factor.items():
            self._summ_dict[k] *= v

    @property
    def summ_dict(self):
        return self._summ_dict

    def get_plot(self, xkey, ykey):
        plt = get_publication_quality_plot(8,6)
        plt.plot(self.summ_dict[xkey], self.summ_dict[ykey],
                 'bo',fillstyle='none')
        return plt



