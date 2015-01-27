"""
.. module:: tmp

tmp
*************

:Description: tmp

    

:Authors: bejar
    

:Version: 

:Created on: 27/01/2015 12:21 

"""

__author__ = 'bejar'


import scipy.io
import numpy as np
from config.paths import datapath, clusterpath
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN, SpectralClustering
from collections import Counter
from util.plots import plotSignals, plotHungarianSignals
from munkres import Munkres
from sklearn.metrics.pairwise import euclidean_distances,rbf_kernel
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, normalized_mutual_info_score

def normalize(data):
    """
    Normalizes all peaks to N(0,1)

    :param data:
    :return:
    """
    ndata = np.zeros(data.shape)

    for i in range(data.shape[0]):
        mean = np.mean(data[i])
        std = np.std(data[i])
        ndata[i] += (data[i]-mean)/std

    return ndata



aline = [
        ('L4cd', 11, 0),
        ('L4ci', 11, 1),
        ('L5cd', 10, 2),
        ('L5rd', 9, 3),
        ('L5ci', 13, 4),
        ('L5ri', 11, 5),
        ('L6cd', 13, 6),
        ('L6rd', 11, 7),
        ('L6ci', 13, 8),
        ('L6ri', 12, 9),
        ('L7ri', 14, 10)
        ]

alg = 'kmeans'

norm = 'N'

for line, nc1, p1 in aline:
    print 'LINE=', line, '***************************************'
    matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + line + '.mat')
    data = matpeaks['Trazos']
    data = normalize(data)
    print data.shape

    matclust = scipy.io.loadmat(clusterpath + 'cluster-'+alg+'-peaks-' + norm + line + '-nc' + str(nc1) + '.mat')
    centers = matclust['centers']
    print centers.shape
    lab = matclust['labels'][0]
    print lab
    nc = centers.shape[0]
    cstd = np.zeros((nc, data.shape[1]))
    print nc

    for i in range(nc):
        center_mask = lab == i
        cstd[i] = np.std(data[center_mask], axis=0)
    lcenters = []
    for i in range(nc):
        lcenters.append((centers[i], 'center %d' % i))


    mx = np.max(centers) # 0.26
    mn = np.min(centers) #-0.06

    plotSignals(lcenters, 8, 2, mx, mn, 'cluster-'+alg+'-N-%s-NC%d' % (line, nc), 'cluster-'+alg+'-%sNC%d' % (line, nc), clusterpath, cstd=cstd)

