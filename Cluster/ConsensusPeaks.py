"""
.. module:: ConsensusPeaks

ConsensusPeaks
*************

:Description: ConsensusPeaks

    

:Authors: bejar
    

:Version: 

:Created on: 10/02/2015 13:54 

"""

__author__ = 'bejar'

from kemlglearn.cluster.consensus import MeanPartitionClustering
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
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
        ndata[i] += (data[i]-mean)/std

    return ndata




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


matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + 'L4ci' + '.mat')
data = matpeaks['Trazos']
data = normalize(data)
nc = 3
for nc in range(2, 19):
    gkm = MeanPartitionClustering(n_clusters=nc, n_components=30, cdistance='ANMI', trans='spectral', n_neighbors=1)
    res = gkm.fit(data)


    fig = plt.figure()

    # ax = fig.gca(projection='3d')
    # pl.scatter(X[:, 1], X[:, 2], zs=X[:, 0], c=gkm.labels_, s=25)

    ax = fig.add_subplot(111)
    plt.scatter(res[:, 0], res[:, 1])

    print 'NC= ', nc
    plt.show()



