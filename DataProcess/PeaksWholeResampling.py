"""
.. module:: PeaksWholeResampling

PeaksWholeResampling
*************

:Description: PeaksWholeResampling

    Resamples the original data and saves on the HDF5 file as /RawResample

:Authors: bejar
    

:Version: 

:Created on: 07/04/2015 11:03 

"""

__author__ = 'bejar'

from scipy.signal import decimate
import h5py

from config.experiments import experiments, lexperiments


resampling = 6


def resample_data(expname):
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
    print datainfo.dpath + datainfo.name + '.hdf5'

    for df in datainfo.datafiles:
        print f[df + '/Raw'].shape
        d = f[df + '/Raw']
        samp = f[df + '/Raw'].attrs['Sampling']

        data = d[()]
        datasampled = decimate(data, resampling, axis=0)
        print datasampled.shape
        d = f[df]
        d.create_dataset('RawResampled', datasampled.shape, dtype='f', data=datasampled, compression='gzip')
        f[df + '/RawResampled'].attrs['Sampling'] = float(samp / resampling)

    f.close()


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

for exp in lexperiments:
    resample_data(exp)

