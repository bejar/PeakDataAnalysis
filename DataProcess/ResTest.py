"""
.. module:: ResTest

ResTest
*************

:Description: ResTest

    Traverses the HDF5 files of the data and prints information

:Authors: bejar
    

:Version: 

:Created on: 25/03/2015 14:40 

"""

__author__ = 'bejar'

import h5py

from config.experiments import experiments


def printing(name, object):
    if type(object) == h5py._hl.dataset.Dataset and 'Time' in name:
        print name, object.shape


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

lexperiments = ['e140515']
for expname in lexperiments:
    print '########################'
    print 'Experiment:', expname
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    files = datainfo.datafiles
    for file in files:
        print '++++++++++++++++++++++++++++'
        print 'FILE:', file
        for s in datainfo.sensors:
            if s[0] == 'L':
                d = f[file + '/' + s + '/' + 'Peaks']
                print s, d.shape[0]

                # f.visititems(printing)