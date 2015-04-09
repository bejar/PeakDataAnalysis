"""
.. module:: PeaksPCA

PeaksPCA
*************

:Description: PeaksPCA

    

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 7:52 

"""

__author__ = 'bejar'

import h5py
from sklearn.decomposition import PCA

from config.experiments import experiments
from util.plots import show_signal


expname = 'e130716f00'

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

for s in datainfo.sensors:
    d = f[datainfo.datafiles[0] + '/' + s + '/' + 'PeaksResample']
    pca = PCA(n_components=d.shape[1])
    res = pca.fit_transform(d[()])
    res[:, 10:-1] = 0
    trans = pca.inverse_transform(res)
    show_signal(trans[0, :])
    # f.create_dataset(datainfo.datafiles[0] + '/' + s + '/' +'PeaksPCA', trans.shape, dtype='f',
    # data=trans, compression='gzip')

