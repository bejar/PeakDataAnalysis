"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 8:10 

"""

__author__ = 'bejar'

import h5py
from sklearn.cluster import KMeans

from config.experiments import experiments


expname = 'e130716f00'

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

for s in datainfo.sensors:
    d = f[datainfo.datafiles[0] + '/' + s + '/' + 'PeaksPCA']
    km = KMeans(n_clusters=10)
    data = d[()]

