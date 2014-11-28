"""
.. module:: ClusterPeaks

ClusterPeaks
*************

:Description: ClusterPeaks

    

:Authors: bejar
    

:Version: 

:Created on: 27/11/2014 14:18 

"""

__author__ = 'bejar'


import scipy.io
import numpy as np
from util.paths import cpath, rpath
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN, SpectralClustering
from collections import  Counter
from util.plots import plotSignals


# aline = [('L4cd', 'k9.n5', 9),
#          ('L4ci', 'k9.n1', 9),
#         ('L5cd', 'k10.n6' , 10),
#         #('L5rd', 'k20.n1' ),
#         ('L5ci', 'k15.n1', 15),
#         ('L5ri', 'k15.n9', 15),
#         ('L6cd', 'k17.n1', 17),
#         ('L6rd', 'k13.n9', 13),
#         #('L6ci', 'k15.n1'),
#         ('L6ri', 'k18.n4', 18),
#         ('L7ri', 'k18.n4', 18)
#         ]

nc = 12

aline = [('L4cd', 'k9.n1', 9)]

for line, _, _ in aline:
    matpeaks = scipy.io.loadmat(cpath + '/WHOLE/trazos.' + line + '.mat')
    print matpeaks['Trazos'].shape
    data = matpeaks['Trazos']

spectral = SpectralClustering(n_clusters=nc, assign_labels='discretize',
                              affinity='nearest_neighbors', n_neighbors=30)

spectral.fit(data)

lab = spectral.labels_

centers = np.zeros((nc, data.shape[1]))

for i in range(data.shape[0]):
    centers[lab[i]] += data[i]


print len(lab)

l = [lab[i] for i in range(len(lab))]

c = Counter(l)

print c

lcenters = []
for i in c:
    centers[i] /= c[i]
    print i, c[i]
    lcenters.append((centers[i], 'center %d'%i))

mx = np.max(centers)
mn = np.min(centers)

plotSignals(lcenters, 6, 2, mx, mn, 'cluster-L4cd', 'cluster-L4cd')



