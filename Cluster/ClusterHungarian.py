"""
.. module:: ClusterHungarian

ClusterHungarian
*************

:Description: ClusterHungarian

    

:Authors: bejar
    

:Version: 

:Created on: 27/01/2015 8:59 

"""

__author__ = 'bejar'

import scipy.io
import numpy as np
from munkres import Munkres
from sklearn.metrics.pairwise import euclidean_distances

from config.paths import clusterpath
from util.plots import plotHungarianSignals


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

for line1, nc1, p1 in aline:
    print 'LINE=', line1, '***************************************'
    matclust1 = scipy.io.loadmat(clusterpath + 'cluster-' + alg + '-peaks-' + norm + line1 + '-nc' + str(nc1) + '.mat')
    centers1 = matclust1['centers']
    print centers1.shape
    inv = None
    for line2, nc2, p2 in aline:
        if p1 < p2:
            print 'LINE=', line2

            matclust2 = scipy.io.loadmat(
                clusterpath + 'cluster-' + alg + '-peaks-' + norm + line2 + '-nc' + str(nc2) + '.mat')

            centers2 = matclust2['centers']
            print centers2.shape
            if nc1 <= nc2:
                inv = False
                dist = euclidean_distances(centers1, centers2)
            else:
                inv = True
                dist = euclidean_distances(centers2, centers1)
            print dist.shape
            m = Munkres()
            a = m.pad_matrix(dist, pad_value=1000)
            nm = np.array(a)
            print len(a), len(a[0])
            indexes = m.compute(dist)
            sumdist = 0

            for c1, c2 in indexes:
                if c1 < centers1.shape[0] and c2 < centers2.shape[0]:
                    sumdist += euclidean_distances(centers1[c1], centers2[c2])
            print sumdist

            print indexes
            mx = max(np.max(centers1), np.max(centers2))
            mn = min(np.min(centers1), np.min(centers2))
            if inv:
                plotHungarianSignals(indexes, centers2, centers1, mx, mn, 'HNG-' + line2 + line1,
                                     'HNG-' + line2 + '(' + str(nc2) + ')-' + line1 + '(' + str(nc1) + ')',
                                     clusterpath)
            else:
                plotHungarianSignals(indexes, centers1, centers2, mx, mn, 'HNG-' + line1 + line2,
                                     'HNG-' + line1 + '(' + str(nc1) + ')-' + line2 + '(' + str(nc2) + ')',
                                     clusterpath)


