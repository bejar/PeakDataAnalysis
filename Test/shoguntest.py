"""
.. module:: shoguntest

shoguntest
*************

:Description: shoguntest

    

:Authors: bejar
    

:Version: 

:Created on: 05/02/2015 11:55 

"""

__author__ = 'bejar'

from kemlglearn.datasets import cluster_generator
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import modshogun as sg


nc = 3
_, X = cluster_generator(n_clusters=nc, sepval=0.01, numNonNoisy=2, numNoisy=0, rangeN=[50, 100])

fig = plt.figure()

ax = fig.add_subplot(111)
plt.scatter(X[:, 0], X[:, 1])

feats_train = sg.RealFeatures(X)
distance = sg.EuclideanDistance(feats_train, feats_train)

kmeans = sg.KMeans(nc, distance)
kmeans.set_use_kmeanspp(True)
kmeans.train()

out_centers = kmeans.get_cluster_centers()

print kmeans.get_labels()
print out_centers.shape
fig = plt.figure()

ax = fig.add_subplot(111)
plt.scatter(out_centers[:, 0], out_centers[:, 1])

plt.show()

km = KMeans(n_clusters=nc)
km.fit(X)

fig = plt.figure()

ax = fig.add_subplot(111)
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1])

plt.show()
