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
from scipy.signal import resample, decimate

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import util.TotalVariation as tv

lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']
lexperiments = ['e140515b']
expname = lexperiments[0]

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

for s in datainfo.sensors:
    print s
    ldatap = []
    ldatappca = []
    ldataraw = []
    for dfiles in datainfo.datafiles:
        d = f[dfiles + '/' + s + '/' + 'Peaks']
        dataf = d[()]
        ldataraw.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksResample']
        dataf = d[()]
        ldatap.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
        dataf = d[()]
        ldatappca.append(dataf)

    data = ldatap[0] #np.concatenate(ldata)
    datapca = ldatappca[0] #np.concatenate(ldata)
    dataraw= ldataraw[0] #np.concatenate(ldata)

    for i in range(data.shape[0]):
        show_two_signals( datapca[i], data[i])
        show_signal(dataraw[i])
