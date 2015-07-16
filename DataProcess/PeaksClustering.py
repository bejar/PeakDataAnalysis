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
from util.plots import show_signal, plotSignals
import numpy as np
from sklearn.cluster import KMeans

from config.experiments import experiments
from collections import Counter


expname = 'e130827'


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225','e140220']

lexperiments = ['e140515']

nclusters = 8
datainfo = experiments['e140515']

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

for dfile in datainfo.datafiles:
    print dfile
    for s, nclusters in zip(datainfo.sensors, datainfo.clusters):
        d = f[dfile + '/' + s + '/' + 'PeaksResamplePCA']
        km = KMeans(n_clusters=nclusters)
        data = d[()]
        km.fit_transform(data)
        lsignals = []
        cnt = Counter(list(km.labels_))

        print s, cnt

        # for nc in range(nclusters):
        #     lsignals.append((km.cluster_centers_[nc], str(nc)+' ( '+str(cnt[nc])+' )'))
        #
        # print s, np.max(km.cluster_centers_), np.min(km.cluster_centers_)
        # if nclusters % 2 == 0:
        #     part = nclusters /2
        # else:
        #     part = (nclusters /2) + 1
        # plotSignals(lsignals,part,2,np.max(km.cluster_centers_),np.min(km.cluster_centers_), datainfo.name + '-' + dfile + '-' + s, s, datainfo.dpath+'/Results/')
        # # for cc in range(nclusters):
        # #     show_signal(km.cluster_centers_[cc])

