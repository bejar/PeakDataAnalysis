"""
.. module:: ComputeSeqProbMatrix

ComputeSeqProbMatrix
*************

:Description: ComputeSeqProbMatrix

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2015 12:41 

"""

__author__ = 'bejar'


import operator
import h5py
import numpy as np

from config.experiments import experiments
import scipy.io
from pylab import *

from rstr_max import *
from util.misc import compute_frequency_remap
from sklearn.metrics import pairwise_distances_argmin_min
import random
import string
import os
import seaborn as sns
from util.plots import plotMatrices

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


def compute_sequence_probability_matrix(timepeaks, clpeaks, sensor, nsym, gap, laplace):
    """
    Computes the transition probability matrix of a sequence of peaks

    :param dfile:
    :param timepeaks:
    :param clpeaks:
    :param sensor:
    :param ncl:
    :param gap:
    :return:
    """
    pm = np.zeros((nsym, nsym)) + laplace
    for i in range(0, timepeaks.shape[0]-1):
        if timepeaks[i + 1] - timepeaks[i] < gap:
            pm[clpeaks[i], clpeaks[i + 1]]+= 1.0
    return pm / pm.sum()
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e150514']
    TVD = False
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]
        f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

        for dfile in datainfo.datafiles:
            print(dfile)
            lmatrices = []
            for ncl, sensor in zip(datainfo.clusters, datainfo.sensors):
                print(sensor)
                clpeaks = compute_data_labels(datainfo.datafiles[0], dfile, sensor)
                d = f[dfile + '/' + sensor + '/' + 'Time']
                timepeaks = data = d[()]
                pmatrix = compute_sequence_probability_matrix(timepeaks, clpeaks, sensor, ncl, gap=1000, laplace=1)
                lmatrices.append((pmatrix, sensor))
            plotMatrices(lmatrices, 6, 2, dfile, dfile,  datainfo.dpath + '/Results/')
