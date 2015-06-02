"""
.. module:: TestTVDwhole

TestTVDwhole
*************

:Description: TestTVDwhole

    

:Authors: bejar
    

:Version: 

:Created on: 02/06/2015 14:42 

"""

__author__ = 'bejar'

import scipy.io
from numpy.fft import rfft, irfft
from scipy.signal import resample, decimate
import h5py
import util.TotalVariation as tv
import numpy as np
import scipy.io

from config.experiments import experiments, lexperiments
from util.plots import show_two_signals

def tvd_data(expname):
    """
    :param expname:
    :param TVD:
    :return:
    """

    lratio=np.array([1e-3])
    datainfo = experiments[expname]
    for dfiles in datainfo.datafiles:
        mattime = scipy.io.loadmat(datainfo.dpath + dfiles + '.mat')

        raw = mattime['data']
        newtvd = np.zeros(raw.shape)
        for i, s in enumerate(datainfo.sensors):
            for chunk in range(0,raw.shape[0],500000):
                sdata = raw[chunk:chunk+500000, i]
                x = sdata.reshape((sdata.shape[0]), 1)
                lmax = tv.tvdiplmax(x)
                y, _, _, _ = tv.tvdip(x, lmax*lratio, False, 1e-5)
                print s, sdata.shape, x.shape, y.shape
                newtvd[chunk:chunk+500000, i] = y.reshape((y.shape[0]))
        peakdata = {'data': newtvd}

        scipy.io.savemat(datainfo.dpath + dfiles + '-TVD.mat', peakdata, do_compression=True)


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e130827']

for exp in lexperiments:
    tvd_data(exp)



