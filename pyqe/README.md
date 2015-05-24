# PyQE

Designed for NANO266, PyQE is a supplementary Python package to perform PWSCF (Quantum Espresso) calculations and result analyses. Basic features include: 

  - Write input file from provided templates in serial or parallel mode. 
  - In parallel mode, send batch of jobs to glean queue on TSCC. 
  - Analyze preliminary results from output files and store them in results.csv.
  - Further data processing, including converting the annoying energy/length units in PWSCF to favored ones. 
  - Convergence analysis and finding equilibrium lattice constant. 


### Version
0.1


### Installation

First, clone this forked nano266 repo. 
```sh
$ git clone git@github.com:adengz/nano266.git
```
Then, under the root directory of nano266, setup PyQE
```sh
$ cd nano266
$ sudo python setup.py develop
```
If you are on a supercomputer, like TSCC, after cd to nano266, then do
```sh
$ python setup.py develop --user
```
This will install all the scripts as well as PyQE library. 


### Examples

Find the lattice constant at equilibrium for hcp Fe in lab3. To finish this particular question, parallel mode (send to computational nodes) is way more efficient than serial mode (run on login nodes or your own laptop). 

After changing directory to the root of lab3, create a scratch directory. 
```sh
$ mkdir scratch
```

Use your favorite text editor to write a python script. 

    from pyqe.qe_input import write_input, get_template
    from monty.os import cd
    import numpy as np
    
    k1 = 16
    k3 = 10
    temp = get_template('Fe.hcp')
    with cd('scratch'):
        for c in np.linspace(1.71,1.74,4):
            for a in np.linspace(4.75,4.85,11):
                p = {'alat':a,'calat':c,'k1':k1,'k3':k3}
                write_input(temp,p,['alat','calat'])

By excuting this script, you should be able to see 44 new folders in the scratch directory. A PWSCF input file and a Fe PSP file is in each folder. In the scratch directory, do
```sh
$ qsend_qe *
```
Each set of PWSCF input is sent to glean queue as one job. When all the jobs are done, in the scratch directory, do
```sh
$ analyze */*_*.out
```
A results.csv file will be written in the scratch directory. Note all the job.out are not parsed. 

More examples on further analysis  are available in the ipython notebooks in the report directory of lab2 and lab3. 
    

### Todo's

 - Surface energy module for lab4
 - Unittests???

**Free Software, Hell Yeah!**
