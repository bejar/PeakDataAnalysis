"""
.. module:: TestBokeh

TestBokeh
*************

:Description: TestBokeh

    

:Authors: bejar
    

:Version: 

:Created on: 04/06/2015 17:10 

"""

__author__ = 'bejar'

import time

import h5py
from util.plots import show_signal, plotSignals, show_two_signals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from scipy.signal import resample, decimate

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import util.TotalVariation as tv

from bokeh.plotting import cursession, figure, show, output_server, hplot, gridplot



lexperiments = ['e140515b']
expname = lexperiments[0]

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

for s in datainfo.sensors:
    print s
    ldatap = []
    ldatappca = []
    ldataraw = []
    for dfiles in datainfo.datafiles:
        d = f[dfiles + '/' + s + '/' + 'Peaks']
        dataf = d[()]
        ldataraw.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksResample']
        dataf = d[()]
        ldatap.append(dataf)
        d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
        dataf = d[()]
        ldatappca.append(dataf)

    data = ldatap[0] #np.concatenate(ldata)
    datapca = ldatappca[0] #np.concatenate(ldata)
    dataraw= ldataraw[0] #np.concatenate(ldata)
    output_server("line_animate")

    p1 = figure()
    y = data[0]
    p1.line(range(data.shape[1]), y, color="#3333ee", name="samp1")
    p2 = figure()
    z = datapca[0]
    p2.line(range(datapca.shape[1]), z, color="#ee33ee", name="samp2")
    p3 = figure(width=1000)
    w = dataraw[0]
    p3.line(range(dataraw.shape[1]), w, color="#ee33ee", name="samp3")
    p=gridplot([[p1,p2],[p3]])
    show(p)




    renderer = p1.select(dict(name="samp1"))
    ds = renderer[0].data_source
    renderer = p2.select(dict(name="samp2"))
    ds2 = renderer[0].data_source
    renderer = p3.select(dict(name="samp3"))
    ds3 = renderer[0].data_source

    for i in range(data.shape[0]):
        ds.data["y"] = data[i]
        ds2.data["y"] = datapca[i]
        ds3.data["y"] = dataraw[i]
        cursession().store_objects(ds)
        cursession().store_objects(ds2)
        cursession().store_objects(ds3)
        time.sleep(0.5)



