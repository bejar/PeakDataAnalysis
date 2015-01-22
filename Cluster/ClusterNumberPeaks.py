"""
.. module:: ClusterNumberPeaks

ClusterNumberPeaks
*************

:Description: ClusterNumberPeaks

    

:Authors: bejar
    

:Version: 

:Created on: 21/01/2015 13:45 

"""

__author__ = 'bejar'

from kemlglearn.metrics import scatter_matrices_scores
import scipy.io
import numpy as np
from config.paths import clusterpath, datapath
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN, SpectralClustering
from collections import Counter
from util.plots import plotSignals


aline = [
        ('L4cd', 'k9.n5', 9),
        ('L4ci', 'k9.n1', 9),
        ('L5cd', 'k10.n6', 10),
        ('L5rd', 'k20.n1', 10),
        ('L5ci', 'k15.n1', 15),
        ('L5ri', 'k15.n9', 15),
        ('L6cd', 'k17.n1', 17),
        ('L6rd', 'k13.n9', 13),
        ('L6ci', 'k15.n1', 10),
        ('L6ri', 'k18.n4', 18),
        ('L7ri', 'k18.n4', 18)
        ]

for line, _, _ in aline:
    print 'LINE=', line
#    print cpath + '/WHOLE/trazos.' + line + '.mat'
    matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + line + '.mat')
#    print matpeaks['Trazos'].shape
    data = matpeaks['Trazos']

    minc = np.inf
    chosen = -1
    for nc in range(2, 20):
        #cluster = KMeans(n_clusters=nc, n_jobs=-1)
        cluster = SpectralClustering(n_clusters=nc, assign_labels='discretize',
                                     affinity='nearest_neighbors', n_neighbors=30)


        cluster.fit(data)
        score = scatter_matrices_scores(data, cluster.labels_, ['ZCF', 'CH'])
        print score
        #print nc, scatter_matrices_scores(data, cluster.labels_, ['ZCF', 'CH'])
        if minc > score['ZCF']:
            minc = score['ZCF']
            chosen = nc

    print chosen