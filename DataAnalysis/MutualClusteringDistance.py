"""
.. module:: MutualClusteringDistance

MutualClusteringDistance
*************

:Description: MutualClusteringDistance

    Mutual distances from clustering comparison

:Authors: bejar
    

:Version: 

:Created on: 26/06/2015 8:34 

"""

__author__ = 'bejar'


import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.manifold import MDS, TSNE, SpectralEmbedding

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

lexperiments = ['e140515']

colors = 'rrryyyyyyyyybbbbbbbbbbbbb'
ext = ''

def compute_data_labels(dfilec, dfile, sensor):
    """
    Computes the labels of the data using the centroids of the cluster in the file
    :param dfile:
    :param sensor:
    :return:
    """
    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

    d = f[dfilec + '/' + sensor + '/Clustering/' + 'Centers']
    centers = d[()]
    d = f[dfile + '/' + sensor + '/' + 'PeaksResamplePCA']
    data = d[()]
    labels, _ = pairwise_distances_argmin_min(data, centers)
    f.close()
    return labels


# ------------------------------------------------------------------------
reference = 0

size = [0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2]
size = (np.array(size)+1) * 25
colors = 'yyyrrrrrrrrrbbbbbbbbbbb'
for expname in lexperiments:
    datainfo = experiments[expname]

    #f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')
    for s in datainfo.sensors:
        print s
        mdist = np.zeros((len(datainfo.datafiles), len(datainfo.datafiles)))
        print mdist.shape
        for i, rfile in enumerate(datainfo.datafiles):
            rfile = rfile
            rlabels = compute_data_labels(rfile, rfile, s)
            rcnt = Counter(list(rlabels))
            rhisto = [rcnt[i] for i in range(len(rcnt))]
            for j, dfile in enumerate(datainfo.datafiles):
                dlabels = compute_data_labels(rfile, dfile, s)
                cnt = Counter(list(dlabels))
                histo = [cnt[i] for i in range(len(cnt))]
                mdist[i,j] = hellinger_distance(rhisto, histo)
                #print rfile, dfile, hellinger_distance(rhisto, histo)
        for i in range(mdist.shape[0]):
            for j in range(mdist.shape[1]):
                tmp = (mdist[i,j] + mdist[j,i])/2
                mdist[i,j] = mdist[j,i] = tmp


        transf = MDS(n_components=2, dissimilarity='precomputed', n_jobs=-1)
        #transf = TSNE(n_components=2, metric='precomputed')
        mres = transf.fit_transform(mdist)

        fig = plt.figure()
#        ax = fig.gca(projection='3d')
        plt.scatter(mres[:, 0], mres[:, 1], c=colors)

        for label, x, y in zip([l[-2:] for l in datainfo.datafiles], mres[:, 0], mres[:, 1]):
            plt.annotate(label, xy=(x, y))

        plt.show()


