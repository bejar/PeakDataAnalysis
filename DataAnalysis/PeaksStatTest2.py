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

from scipy.stats import bartlett, levene, ttest_ind, ks_2samp, shapiro, fligner, f_oneway, anderson, kstest
from scipy.signal import butter, filtfilt, freqs, lfilter

from util.plots import show_signal, plotSignals, show_two_signals


lexperiments = ['e150514']
iband = 10
fband = 70
for expname in lexperiments:
    datainfo = experiments[expname]
    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    step = 100000
    length = 200000
    d = f[datainfo.datafiles[15] + '/' + 'Raw']
    samp = f[datainfo.datafiles[15] + '/Raw'].attrs['Sampling']
    data = d[()]
    freq = samp * 0.5
    print freq
    b, a = butter(3, [iband/freq, fband/freq], btype='band')

    datainit = filtfilt(b, a, d[0:length, 8])
#    print datainfo.datafiles[0], np.mean(datainit), np.std(datainit)
    for pos in range(step, d.shape[0], step):
        d = f[datainfo.datafiles[15] + '/' + 'Raw']
        datanext = filtfilt(b, a, d[pos:pos+length, 8])
        bval, pval = levene(datainit, datanext)
        print  np.std(datainit)- np.std(datanext), pval
        datainit = datanext
        if pval > 0.05:
            print '*'
