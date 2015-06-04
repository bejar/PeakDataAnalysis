"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    Clusters the Peaks from an experiment all the files together

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

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

lexperiments = ['e140515b']

colors = 'rgbymc'
ext = ''

#expname = lexperiments[3]
for expname in lexperiments:
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')

    for s, nclusters in zip(datainfo.sensors, datainfo.clusters):
        print s
        ldata = []
        for dfiles in datainfo.datafiles:
            print dfiles
            d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
            dataf = d[()]
            km = KMeans(n_clusters=nclusters)
            km.fit_transform(dataf)

            lsignals = []
            cnt = Counter(list(km.labels_))


            print '*******************'
            for nc in range(nclusters):
                lsignals.append((km.cluster_centers_[nc], str(nc)+' ( '+str(cnt[nc])+' )'))

            #print s, np.max(km.cluster_centers_), np.min(km.cluster_centers_)
            if nclusters % 2 == 0:
                part = nclusters /2
            else:
                part = (nclusters /2) + 1
            plotSignals(lsignals,part,2,np.max(km.cluster_centers_),np.min(km.cluster_centers_), datainfo.name + '-'  + dfiles + '-' + s + ext,
                        datainfo.name + '-'  + dfiles + '-' + s + ext, datainfo.dpath+'/Results/')

