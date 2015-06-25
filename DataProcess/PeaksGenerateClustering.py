"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    Generates and saves a clustering of the peaks for only the first file of the experiment

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 8:10 

"""

__author__ = 'bejar'

import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

lexperiments = ['e140515']

ext = ''

#expname = lexperiments[3]
for expname in lexperiments:
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')

    for sensor, nclusters in zip(datainfo.sensors, datainfo.clusters):
        print sensor
        ldata = []
        for dfile in datainfo.datafiles:
        #dfile = datainfo.datafiles[0]
            print dfile
            d = f[dfile + '/' + sensor + '/' + 'PeaksResamplePCA']
            data = d[()]

            km = KMeans(n_clusters=nclusters, n_jobs=-1)
            km.fit_transform(data)
            lsignals = []
            cnt = Counter(list(km.labels_))

            lmax = []
            for i in range(km.n_clusters):
                lmax.append((i,np.max(km.cluster_centers_[i])))
            lmax = sorted(lmax, key=itemgetter(1))

            centers = np.zeros(km.cluster_centers_.shape)
            for nc in range(nclusters):
                centers[nc] = km.cluster_centers_[lmax[nc][0]]

            d = f.require_dataset(dfile + '/' + sensor + '/Clustering/' + 'Centers' + ext, centers.shape, dtype='f',
                                  data=centers, compression='gzip')
            d[()] = centers
            lmax = []


