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
lexperiments = ['e130827']
expname = lexperiments[0]

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '-TVD.hdf5', 'r')

for s, nclusters in zip(datainfo.sensors, datainfo.clusters):

    for dfiles in datainfo.datafiles:
        d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
        dataf = d[()]

        print dataf.shape
        for i in range(dataf.shape[0]):
            show_signal(dataf[i])

