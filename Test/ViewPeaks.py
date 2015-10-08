"""
.. module:: ViewPeaks

ViewPeaks
*************

:Description: ViewPeaks

    

:Authors: bejar
    

:Version: 

:Created on: 27/05/2015 14:50 

"""

__author__ = 'bejar'

import h5py
from util.plots import show_signal, plotSignals, show_two_signals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from scipy.signal import resample, decimate, detrend

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import util.TotalVariation as tv

lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']
lexperiments = ['e140515']
expname = lexperiments[0]

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')
print expname

for s in datainfo.sensors:
    print s
    ldatap = []
    ldatappca = []
    ldataraw = []
    for dfiles in [datainfo.datafiles[0]]:
        print dfiles
        d = f[dfiles + '/' + s + '/' + 'Peaks']
        dataf = d[()]
        ldataraw.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksFilter']
        dataf = d[()]
        ldatap.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
        dataf = d[()]
        ldatappca.append(dataf)

    data = ldatap[0] #np.concatenate(ldata)
    datapca = ldatappca[0] #np.concatenate(ldata)
    dataraw = ldataraw[0] #np.concatenate(ldata)

    print data.shape, datapca.shape, dataraw.shape
    print len(data)
    for i in range(dataraw.shape[0]):
        print i
        # print dataraw[i]
        # print data[i]
        show_signal(dataraw[i])
        # show_two_signals(dataraw[i], detrend(dataraw[i]))
        show_signal(data[i])
        show_signal(datapca[i])
