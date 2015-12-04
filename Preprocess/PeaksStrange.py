"""
.. module:: PeaksStrange

PeaksStrange
*************

:Description: PeaksStrange

    

:Authors: bejar
    

:Version: 

:Created on: 03/12/2015 15:33 

"""

import h5py
from util.plots import show_signal, plotSignals
from pylab import *
from config.experiments import experiments


__author__ = 'bejar'

def detect_wavy_sinus(signal, thresh):
    """
    Detect if a signal is a high frequecy sinus

    :param signal:
    :return:
    """

    middle = np.max(signal)/2.0
    tmp = signal.copy()

    tmp[signal < middle] = 0

    count = 0
    for i in range(1, signal.shape[0]):
        if tmp[i-1] == 0 and tmp[i] != 0:
            count += 1
    return count >= thresh




if __name__ == '__main__':

    lexperiments = ['e150707']
    for expname in lexperiments:
        datainfo = experiments[expname]
        f = h5py.File(datainfo.dpath + datainfo.name + '/' + datainfo.name + '.hdf5', 'r+')

        for dfile in [datainfo.datafiles[0]]:
            for s in datainfo.sensors:
                print(s)
                d = f[dfile + '/' + s + '/' + 'PeaksResample']

                data = d[()]
                lstrange = []
                for i in range(data.shape[0]):
                    if detect_wavy_sinus(data[i], 6):
                        lstrange.append(i)
                        #show_signal(data[i])
                print(len(lstrange))


        f.close()