"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    Clusters the Peaks from an experiment

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 8:10 

"""

__author__ = 'bejar'

import h5py
import numpy as np
from sklearn.cluster import KMeans

from config.experiments import experiments
from util.plots import show_signal, plotSignals
from collections import Counter

expname = 'e130827'


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225','e140220']


nclusters = 8
datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

for dfile in datainfo.datafiles:
    for s in datainfo.sensors:
        d = f[dfile + '/' + s + '/' + 'PeaksResamplePCA']
        km = KMeans(n_clusters=nclusters)
        data = d[()]
        km.fit_transform(data)
        lsignals = []
        cnt = Counter(list(km.labels_))

        #print cnt

        for nc in range(nclusters):
            lsignals.append((km.cluster_centers_[nc], str(nc)+' ( '+str(cnt[nc])+' )'))

        print s, np.max(km.cluster_centers_), np.min(km.cluster_centers_)
        plotSignals(lsignals,4,2,np.max(km.cluster_centers_),np.min(km.cluster_centers_), dfile + '-' + s, s, datainfo.dpath+'/Results/')
        # for cc in range(nclusters):
        #     show_signal(km.cluster_centers_[cc])

