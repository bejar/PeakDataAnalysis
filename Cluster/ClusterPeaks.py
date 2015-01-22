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
from config.paths import datapath, clusterpath
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN, SpectralClustering
from collections import Counter
from util.plots import plotSignals


aline = [
 #   ('L4cd', 'k9.n5', 9),
 #        ('L4ci', 'k9.n1', 9),
 #        ('L5cd', 'k10.n6', 10),
         ('L5cd', 'k20.n1', 10),
 #        ('L5ci', 'k15.n1', 15),
 #        ('L5ri', 'k15.n9', 15),
 #        ('L6cd', 'k17.n1', 17),
 #        ('L6rd', 'k13.n9', 13),
 #        ('L6ci', 'k15.n1', 10),
 #        ('L6ri', 'k18.n4', 18),
 #        ('L7ri', 'k18.n4', 18)
        ]

nc = 4
alg = 'spectral'

#aline = [('L6cd', 'k17.n1', 17)]
#line = aline[0][0]
for line, _, _ in aline:
    print 'LINE=', line
    print datapath + '/WHOLE/trazos.' + line + '.mat'
    matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + line + '.mat')
    print matpeaks['Trazos'].shape
    data = matpeaks['Trazos']


    if alg == 'spectral':
        spectral = SpectralClustering(n_clusters=nc, assign_labels='discretize',
                                      affinity='nearest_neighbors', n_neighbors=30)
    elif alg == 'kmeans':
        spectral = KMeans(n_clusters=nc, n_jobs=-1)

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
    numex = np.zeros(nc)
    for i in c:
        centers[i] /= c[i]
        print i, c[i]
        numex[i] = c[i]
        lcenters.append((centers[i], 'center %d' % i))

    mx = 0.26  # np.max(centers)
    mn = -0.06  # np.min(centers)

    plotSignals(lcenters, nc, 1, mx, mn, 'cluster-'+alg+'-%s-NC%d' % (line, nc), 'cluster-'+alg+'-%sNC%d' % (line, nc), clusterpath)


    if alg == 'spectral':
        params = {'clalg': 'spectral',
                           'nc': nc,
                           'labels': 'discretize',
                           'affinity': 'nearest_neighbors',
                           'n_neigbors': 30
                           }
    elif alg == 'kmeans':
        params = {'clalg': 'kmeans', 'nc': nc}
    peakdata = {'labels': lab,
                'centers': centers,
                'numex': numex,
                'params': params
                }

    scipy.io.savemat(clusterpath + 'cluster-'+alg+'-peaks-' + line + '-nc' + str(nc) + '.mat', peakdata)



