"""
.. module:: PeaksDistanceSeparation

PeaksDistanceSeparation
*************

:Description: PeaksDistanceSeparation

    

:Authors: bejar
    

:Version: 

:Created on: 04/06/2015 8:36 

"""

__author__ = 'bejar'


import h5py
from sklearn.decomposition import PCA
import numpy as np

from config.experiments import experiments
from util.plots import show_signal
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from pylab import *



def do_the_job(sensor, dfile, ext=''):
    """
    Computes the distribution of the time separation between peaks
    :param sensor:
    :return:
    """
    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

    sampling = f[dfile + '/Raw'].attrs['Sampling']
    d = f[dfile + '/' + sensor + '/' + 'Time' + alt]
    data = d[()]

    lsep = []
    for i in range(data.shape[0] - 1):
        lsep.append((data[i+1] - data[i]) * (1000.0/sampling))

    print dfile + '/' + sensor, np.mean(lsep), np.std(lsep), len(lsep)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(lsep, 25, normed=1, facecolor='green', alpha=0.75)

    ax.set_xlabel('Smarts')

    ax.set_xlim(0, max(lsep))
    ax.set_ylim(0, 0.01)
    ax.grid(True)
    plt.show()

    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    minaxis = min(lsep)
    maxaxis = max(lsep)
    num = len(lsep)
    sp1 = fig.add_subplot(111)
    sp1.axis([0, num, minaxis, maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t, lsep, 'r')
    plt.show()

# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    #lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e140515b']

    ext = ''
    TVD = False
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''
        datainfo = experiments[expname]


        for dfile in datainfo.datafiles:
            print dfile
            # Distance Separation
            for s in datainfo.sensors:
                do_the_job(s, dfile, ext=ext)