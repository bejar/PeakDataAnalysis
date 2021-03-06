"""
.. module:: PeaksOutliers

PeaksOutliers
*************

:Description: PeaksOutliers

 Eliminates from the signal all the outliers and the too wavy signals

:Authors: bejar

:Version: 

:Created on: 14/07/2015 9:00 

"""

__author__ = 'bejar'


import h5py
from pylab import *
from sklearn.neighbors import NearestNeighbors
from config.experiments import experiments
from joblib import Parallel, delayed
from util.plots import show_signal

def is_wavy_signal(signal, thresh):
    """
    Detects if a signal has many cuts over the positive middle part of the signal

    :param signal:
    :return:
    """

    middle = np.max(signal)/2.0
    tmp = signal.copy()

    tmp[signal < middle] = 0

    count = 0
    for i in range(1, signal.shape[0]):
        if tmp[i-1] == 0 and tmp[i] != 0:
            count += 1
    return count > thresh


def do_the_job(dpath, dname, dfile, sensor, nn, nstd=6, wavy=5):
    """
    Identifies the outliers in the peaks

    :param dfile:
    :param sensor:
    :return:
    """

    # Detect outliers based on the distribution of the distances of the signals to the knn
    # Any signal that is farther from its neighbors that a number of standar deviations of the mean knn-distance is out
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
        if vdist[i] > dmean + (nstd*dstd):
            nout += 1
            lout.append(i)
            show_signal(data[i])
        elif is_wavy_signal(data[i], wavy):
            nout += 1
            lout.append(i)
            show_signal(data[i])




    return dfile, lout


if __name__ == '__main__':

    lexperiments = ['e150707']
    for expname in lexperiments:
        datainfo = experiments[expname]

        for s in datainfo.sensors:
            print s

            lout = Parallel(n_jobs=-1)(delayed(do_the_job)(datainfo.dpath, datainfo.name, dfiles, s, 16, nstd=6, wavy=6)for dfiles in datainfo.datafiles)

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
