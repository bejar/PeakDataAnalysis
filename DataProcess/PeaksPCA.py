"""
.. module:: PeaksPCA

PeaksPCA
*************

:Description: PeaksPCA

    Performs a PCA of the peaks and reconstructs them with only a number of them
    Eventually saves the peaks in *Signal*/PeaksPCA

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 7:52 

"""

__author__ = 'bejar'

import h5py
from sklearn.decomposition import PCA
import numpy as np

from config.experiments import experiments
from util.plots import show_signal

# Components for reconstructing the peaks
components = 10

# Points to compute the baseline
lind = range(40)
lind.extend(range(130, 170))

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225','e140220']

for expname in lexperiments:
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

    for dfile in datainfo.datafiles:
        for s in datainfo.sensors:
            d = f[dfile + '/' + s + '/' + 'PeaksResample']
            pca = PCA(n_components=d.shape[1])
            res = pca.fit_transform(d[()])
            res[:, components:] = 0
            trans = pca.inverse_transform(res)

            # Substract the basal
            for row in range(trans.shape[0]):
                vals = trans[row, lind]
                basal = np.mean(vals)
                trans[row] -= basal

            # show_signal(trans[0, :])
            print dfile + '/' + s + '/' +'PeaksResamplePCA'
            d = f.require_dataset(dfile + '/' + s + '/' +'PeaksResamplePCA', trans.shape, dtype='f',
                              data=trans, compression='gzip')
            d[()] = trans

