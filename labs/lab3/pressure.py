__author__ = 'zhideng'

from math import sqrt
import numpy as np
from scipy.optimize import fsolve
from pymatgen.util.plotting_utils import get_publication_quality_plot
from ulti_analyzer import BasicAnalyzer


def get_dfs():
    #make sure you have all the data needed in results.csv
    b = BasicAnalyzer('results.csv')
    df = b.df
    #filter bcc and hcp structures, calculate the energy and volume
    #within a pandas.dataframe
    bcc = df[df.calat==0]
    bcc = bcc.sort(columns='alat')
    bcc['volume'] = bcc['alat']**3
    bcc['energy'] *=2
    c = 1.73
    hcp = df[df.calat==c]
    hcp = hcp.sort(columns='alat')
    hcp['volume'] = sqrt(3)/2*c*hcp['alat']**3
    return bcc,hcp

def get_poly_params(df):
    #fit the curve to a 4 degree polynomial
    z = np.polyfit(df['volume'],df['energy'],4)
    p = np.poly1d(z) #function of the curve
    pk = p.deriv() #derivetive, also the slope of the tangent line
    pb = pk * np.poly1d([-1,0]) + p #intercept of the tangent line
    return p,pk,pb

def get_ev_plot():
    bcc,hcp = get_dfs()
    plt = get_publication_quality_plot(12,8)
    plt.plot(bcc['volume'],bcc['energy'],'bo',
             fillstyle='none',label='bcc raw data')
    plt.plot(hcp['volume'],hcp['energy'],'ro',
             fillstyle='none',label='hcp raw data')
    X = np.arange(10,25,0.1)
    p1,pk1,pb1 = get_poly_params(bcc)
    plt.plot(X,p1(X),'b-',label='bcc curve')
    p2,pk2,pb2 = get_poly_params(hcp)
    plt.plot(X,p2(X),'r-',label='hcp curve')

    def func(x):
        #equations k1=k2, b1=b2
        x0 = float(x[0])
        x1 = float(x[1])
        return [pk1(x0)-pk2(x1),pb1(x0)-pb2(x1)]

    #numerically solve the equations, starting from
    #the intersection on the plot
    xs = fsolve(func, [18,18])
    dx = xs[0] - xs[1]
    dy = p1(xs[0]) - p2(xs[1])
    #Calculate the pressure in GPa
    pressure = -dy/dx*0.1602
    #plot out the common tangent and also extend it
    plt.plot([xs[0]+3*dx,xs[1]-5*dx],[p1(xs[0])+3*dy,p2(xs[1])-5*dy],
             'k--',label='common tangent')
    ax = plt.gca()
    plt.text(0.3, 0.3,'Phase transition pressure \n%.2f GPa' % pressure,fontsize=30,
             transform=ax.transAxes)
    plt.xlabel('Volume ($\AA^3$)')
    plt.ylabel('Energy (meV/cell)')
    plt.legend(loc=0,fontsize=25)
    plt.tight_layout()
    return plt

if __name__ == "__main__":
    plt = get_ev_plot()
    plt.show()