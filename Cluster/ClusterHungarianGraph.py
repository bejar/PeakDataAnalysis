"""
.. module:: ClusterHungarianGraph

ClusterHungarianGraph
*************

:Description: ClusterHungarianGraph

    

:Authors: bejar
    

:Version: 

:Created on: 27/01/2015 15:19 

"""

__author__ = 'bejar'

import scipy.io
from munkres import Munkres
from sklearn.metrics.pairwise import euclidean_distances
import networkx as nx
from pylab import *

from config.paths import clusterpath


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

signalGraph = nx.Graph()

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
                if not inv:
                    if c1 < centers1.shape[0] and c2 < centers2.shape[0]:
                        v = euclidean_distances(centers1[c1], centers2[c2])
                        signalGraph.add_weighted_edges_from([(line1 + str(c1), line2 + str(c2), v)])
                        print [(line1 + str(c1), line2 + str(c2), v)]
                else:
                    if c2 < centers1.shape[0] and c1 < centers2.shape[0]:
                        v = euclidean_distances(centers1[c2], centers2[c1])
                        signalGraph.add_weighted_edges_from([(line1 + str(c2), line2 + str(c1), v)])
                        print [(line1 + str(c2), line2 + str(c1), v)]

nx.draw_graphviz(signalGraph)
plt.show()