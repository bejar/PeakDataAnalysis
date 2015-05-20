"""
.. module:: PeaksPCA

PeaksPCA
*************

:Description: PeaksPCA

    Experiments using PCA features for clustering

:Authors: bejar

:Version: 

:Created on: 26/03/2015 7:52 

"""

__author__ = 'bejar'

import h5py
from sklearn.decomposition import PCA, KernelPCA
import numpy as np
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

from config.experiments import experiments
from util.plots import show_signal
from sklearn.cluster import KMeans
from collections import Counter
from util.plots import show_signal, plotSignals

import matplotlib.pyplot as plt
import pylab as pl

# Components for reconstructing the peaks
components = 10
nclusters = 2
# Points to compute the baseline (40 initial, 40 final)
lind = range(40)
#lind.extend(range(130, 170))

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']
lexperiments = ['e130827']

for expname in lexperiments:
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

    for dfile in datainfo.datafiles:
        for s in datainfo.sensors:
            d = f[dfile + '/' + s + '/' + 'PeaksResample']
            data = d[()]
            # Substract the basal
            for row in range(data.shape[0]):
                vals = data[row, lind]
                basal = np.mean(vals)
                data[row] -= basal

            pca = PCA(n_components=data.shape[1])
            res = pca.fit_transform(data)

            # Kmeans of some components of the PCA of the data

            cdata = res[:, 0:3*components].copy()
            kpca = KernelPCA(n_components=components, kernel='rbf', degree=3, gamma=1)
            cdata = kpca.fit_transform(cdata)
            k_means = KMeans(init='k-means++', n_clusters=nclusters, n_init=10, n_jobs=-1)

            k_means.fit_transform(cdata)

            fig = plt.figure()
            ax = fig.gca(projection='3d')

            #ax=pl.subplot(1, 1, 1, projection='3d')

            pl.scatter(cdata[:,1],cdata[:,2],zs=cdata[:,0],s=25, c=k_means.labels_)


            pl.show()


            # Data Reconstruction with only a number of components
            # res[:, components:] = 0
            # trans = pca.inverse_transform(res)

            # cnt = Counter(list(k_means.labels_))
            #
            #
            # labels = k_means.labels_
            # llabels = np.unique(labels)
            # nclust = len(llabels)

            # # compute the centroids
            # centroids = np.zeros((nclust, trans.shape[1]))
            # for idx in llabels:
            #     center = np.zeros((1, trans.shape[1]))
            #     center_mask = labels == idx
            #     center += np.sum(trans[center_mask], axis=0)
            #     center /= center_mask.sum()
            #     centroids[idx] = center
            #
            #
            # lsignals = []
            # for nc in range(centroids.shape[0]):
            #     lsignals.append((centroids[nc], str(nc)+' ( '+str(cnt[nc])+' )'))
            #
            # #print s, np.max(km.cluster_centers_), np.min(km.cluster_centers_)
            # if nclusters % 2 == 0:
            #     part = nclusters /2
            # else:
            #     part = (nclusters /2) + 1
            # plotSignals(lsignals,part,2,np.max(centroids),np.min(centroids), datainfo.name + dfile + '-PCA' + '-' + s, s,
            #             datainfo.dpath+'/Results/')
