"""
.. module:: ClusterSaveData

ClusterSaveData
*************

:Description: ClusterSaveData

    

:Authors: bejar
    

:Version: 

:Created on: 27/01/2015 15:53 

"""

__author__ = 'bejar'

from collections import Counter

import scipy.io
import numpy as np
from sklearn.cluster import KMeans

from config.paths import clusterpath, datapath


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
        ndata[i] += (data[i] - mean) / std

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

for line, nc, _ in aline:
    print 'LINE=', line
    print datapath + '/WHOLE/trazos.' + line + '.mat'
    matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + line + '.mat')
    print matpeaks['Trazos'].shape
    data = matpeaks['Trazos']
    data = normalize(data)

    km = KMeans(n_clusters=nc, n_jobs=-1, n_init=25)

    km.fit(data)

    lab = km.labels_

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
        numex[i] = c[i]

    peakdata = {'Trazos': data,
                'labels': lab,
                'centers': centers,
                'numex': numex,
                'nc': nc
                }

    scipy.io.savemat(clusterpath + 'trazos-' + alg + '-' + line + '.mat', peakdata)

