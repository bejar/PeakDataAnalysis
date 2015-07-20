"""
.. module:: PeaksStatTest

PeaksStatTest
*************

:Description: PeaksStatTest

    

:Authors: bejar
    

:Version: 

:Created on: 20/07/2015 11:54 

"""

__author__ = 'bejar'

import h5py
import numpy as np
from config.experiments import experiments, lexperiments

from scipy.stats import bartlett, levene, ttest_ind

from util.plots import show_signal, plotSignals, show_two_signals


lexperiments = ['e140515']

for expname in lexperiments:
    datainfo = experiments[expname]
    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    rslt = 2400000
    step = 2400000
    d = f[datainfo.datafiles[0] + '/' + 'RawFiltered']

    datainit = d[0:step, 5]
#    print datainfo.datafiles[0], np.mean(datainit), np.std(datainit)
    for dfile in range(1,len(datainfo.datafiles)):
        d = f[datainfo.datafiles[dfile] + '/' + 'RawFiltered']
        datanext = d[0:step, 5]
        bval, pval = bartlett(datainit, datanext)
        print datainfo.datafiles[dfile], np.mean(datanext), np.std(datanext)
        print datainfo.datafiles[dfile], bval, pval, '*'
        datainit = datanext

        # for s in range(len(datainfo.sensors)):
        #     print dfile, datainfo.sensors[s]
        #     for pos in range(1, length):
        #         pvar = np.mean(d[pos*step:(pos*step)+rslt, s])
        #         pmean = np.std(d[pos*step:(pos*step)+rslt, s])
        #         #print pmean, pvar
                    # show_signal(d[(pos-1)*step:((pos-1)*step)+rslt, s])
                    # show_signal(d[pos*step:(pos*step)+rslt, s])
