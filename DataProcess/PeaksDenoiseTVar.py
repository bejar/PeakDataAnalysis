"""
.. module:: PeaksDenoiseTVar

PeaksDenoiseTVar
*************

:Description: PeaksDenoiseTVar

    Denoise data using Total Variance Denoising

:Authors: bejar
    

:Version: 

:Created on: 28/05/2015 9:32 

"""


__author__ = 'bejar'

import h5py
from sklearn.decomposition import PCA
import numpy as np

from config.experiments import experiments
from util.plots import show_signal
import util.TotalVariation as tv


def total_variation_denoising(expname, lratio=np.array([2e-2])):
    """
    Performs Total Variation Denoising of the raw peaks

    :param expname:
    :param lratio:  Ratio for the regularization  - The higher the flatter is the signal
    :return:
    """
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

    for dfile in datainfo.datafiles:
        for s in datainfo.sensors:
            print dfile + '/' + s + '/' +'PeaksTVD'

            d = f[dfile + '/' + s + '/' + 'Peaks']
            data = d[()]

            datares = np.zeros(data.shape)

            for i in range(data.shape[0]):
                x = data[i].reshape((data[i].shape[0]), 1)
                lmax = tv.tvdiplmax(x)
                y, _, _, _ = tv.tvdip(x, lmax*lratio, False, 1e-3)
                datares[i] = y[:, 0]

            d = f.require_dataset(dfile + '/' + s + '/' + 'PeaksTVD', datares.shape, dtype='f',
                                  data=datares, compression='gzip')
            d[()] = datares

# -----------------------------------------------------------------------------------------------------

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']
# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']
lexperiments = ['e130827']

for expname in lexperiments:
    total_variation_denoising(expname)
