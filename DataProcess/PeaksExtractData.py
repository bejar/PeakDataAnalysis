"""
.. module:: PeaksExtractData

PeaksExtractData
*************

:Description: PeaksExtractData

 Saves a data collection from the HDF5 file to a matlab file

:Authors: bejar
    

:Version: 

:Created on: 07/04/2015 13:38 

"""

__author__ = 'bejar'

import scipy.io
import h5py

from config.experiments import experiments, lexperiments


def extract_data(expname, dataset):
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')
    print datainfo.dpath + datainfo.name + '.hdf5'

    for df in datainfo.datafiles:
        print f[df + '/' + dataset].shape
        d = f[df + '/' + dataset]

        data = d[()]
        matdata = {}
        matdata['data'] = data
        scipy.io.savemat(datainfo.dpath + '/' + df + '-' + dataset, matdata, do_compression=True)

    f.close()

# lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e130716']

for exp in lexperiments:
    extract_data(exp, 'RawResampled')
