"""
.. module:: PeaksOutliers

PeaksOutliers
*************

:Description: PeaksOutliers

Detects peaks that are outliers and saves them as TimeClean variable at each sensor

:Authors: bejar
    

:Version: 

:Created on: 14/07/2015 9:00 

"""

__author__ = 'bejar'


import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *
from sklearn.neighbors import NearestNeighbors
from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter
from collections import Counter
from joblib import Parallel, delayed


def do_the_job(dpath, dname, dfile, sensor, nn):
    """
    Identifies the outliers in the peaks

    :param dfile:
    :param sensor:
    :return:
    """
    print 'Processing ', sensor, dfile
    f = h5py.File(dpath + dname + '.hdf5', 'r')

    d = f[dfile + '/' + sensor + '/' + 'PeaksResample']
    data = d[()]
    neigh = NearestNeighbors(n_neighbors=nn)
    neigh.fit(data)

    vdist = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        vdist[i] = np.sum(neigh.kneighbors(data[i], return_distance=True)[0][0][1:])/(nn-1)
    dmean = np.mean(vdist)
    dstd = np.std(vdist)
    nout = 0
    lout = []
    for i in range(data.shape[0]):
        if vdist[i] > dmean + (6*dstd):
            nout += 1
            lout.append(i)
    return dfile, lout



lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220', 'e120516', 'e140515']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

lexperiments = ['e150514b']
for expname in lexperiments:
    datainfo = experiments[expname]

    for s in datainfo.sensors:
        print s

        lout = Parallel(n_jobs=-1)(delayed(do_the_job)(datainfo.dpath, datainfo.name, dfiles, s, 16)for dfiles in datainfo.datafiles)

        f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
        for dfile, out in lout:
            d = f[dfile + '/' + s + '/Time']
            times = d[()]
            ntimes = np.zeros(times.shape[0]-len(out))
            npeaks = 0
            for i in range(times.shape[0]):
                if i not in out:
                    ntimes[npeaks] = times[i]
                    npeaks += 1

            d = f.require_dataset(dfile + '/' + s + '/' + 'TimeClean', ntimes.shape, dtype='d',
                                  data=ntimes, compression='gzip')
            d[()] = ntimes
            print times.shape, ntimes.shape, len(out)
        f.close()
