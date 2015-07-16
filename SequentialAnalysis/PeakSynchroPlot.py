"""
.. module:: PeakSyncroPloy

PeakSyncroPloy
*************

:Description: PeakSyncroPloy

    

:Authors: bejar
    

:Version: 

:Created on: 09/07/2015 15:53 

"""

__author__ = 'bejar'

from  matplotlib.backends.backend_pdf import PdfPages
from SequentialAnalysis.PeaksSynchro import compute_data_labels, compute_synchs
from config.experiments import experiments
import h5py
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


def plotSignals(signals,pp,n,m, title):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    fig.suptitle(str(title), fontsize=48)
    i=1
    vmax = []
    vmin = []
    for s, _, _ in signals:
        vmax.append(np.max(s))
        vmin.append(np.min(s))

    for s,snm,v in signals:
        if min(s)!=max(s):
            plotSignalValues(fig,s,n,m,i,snm,v, np.max(vmax), np.min(vmin))
        else:
            plotDummy(fig,len(s),n,m,i,snm)
        i+=1
    fig.savefig(pp, orientation='landscape',format='pdf')
    plt.close()

#    plt.show()



# Plot a set of signals
def plotSignalValues(fig,signal1,n,m,p,name,v, maxaxis, minaxis):
    # minaxis=min(signal1)
    # maxaxis=max(signal1)
    num=len(signal1)
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    if v !=0:
        sp1.plot(t,signal1, 'r')
    else:
        sp1.plot(t,signal1, 'b')

#    plt.show()

def plotDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t,t)
#    plt.show()




# def plotSignalFile(name):
#     mats=scipy.io.loadmat( cpath+name+'-'+banda+'.mat')
#     data= mats['data']
#     chann=mats['names']
#     freq=40
#     off=60000
#     length=60000
#     for i in range(0,data.shape[0]+1,20):
#         lsignals=[]
#         for j in range(i,i+20):
#             if j<data.shape[0]:
#                 # copy the current segment
#                 orig=data[j][off:off+length]
#                 lsignals.append((orig,chann[j]))
#         plotSignals(lsignals,cres,10,2)


def draw_sincro(raw, lsync, num, nums, cres, name, sens):
    """
    Generates files with syncronizations
    """
    def busca_syn(syn, s):
        for sig, time, cl in syn:
            if s == sig:
                return sig, time
        return s, 0

    pp = PdfPages(cres+'/synch-raw' + name + '-' +str(num) + '-' + str(nums) + '.pdf')

    for i in range(num, nums):
        syn = lsync[i]
        ldraw = []
        for j in range(len(sens)):
            ldraw.append(busca_syn(syn, j))

        center = np.sum([v for s, v in ldraw if v > 0])/np.sum([1 for s, v in ldraw if v > 0])
        print i
        lsig = []
        for s, v in ldraw:
            lsig.append((raw[center-1000:center+1000, s], sens[s], v))

        plotSignals(lsig, pp, 6, 2, int(center))

    pp.close()


def select_sensor(synchs, sensor, slength):
    """
    Maintains only the syncs corresponding to the given sensor

    :param synchs:
    :param sensor:
    :return:
    """
    lres = []
    for syn in synchs:
        for s, _,_ in syn:
            if s == sensor and len(syn) >= slength:
                lres.append(syn)
    return lres



if __name__ == '__main__':
    window = 400
    print 'W=', int(round(window))
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e140515']

    TVD = True
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]
        rsensor = 'L5ci'
        nsensor = datainfo.sensors.index(rsensor)
        slength = 2
        filter = False

        # dfile = datainfo.datafiles[0]
        for dfile in [datainfo.datafiles[0]]:
            print dfile

            lsens_labels = []
            #compute the labels of the data
            for sensor in datainfo.sensors:
                lsens_labels.append(compute_data_labels(datainfo.dpath + datainfo.name, datainfo.datafiles[0], dfile, datainfo.sensors[0], sensor))

            # Times of the peaks
            ltimes = []
            expcounts = []
            f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')
            if filter:
                ext = '-F'
                d = f[dfile + '/RawFiltered']
            else:
                ext = ''
                d = f[dfile + '/Raw']

            raw = d[()]
            for sensor in datainfo.sensors:
                d = f[dfile + '/' + sensor + '/' + 'TimeClean']
                data = d[()]
                #expcounts.append(data.shape[0])
                ltimes.append(data)
            f.close()
            lsynchs = compute_synchs(ltimes, lsens_labels, window=window)
            print len(lsynchs)
            lsynchs = select_sensor(lsynchs, nsensor, slength)
            print len(lsynchs)

            for i in range(0, 100, 100):
                draw_sincro(raw, lsynchs, i, i + 100, datainfo.dpath + '/Results', dfile + '-' + rsensor + '-Len' + str(slength) + ext, datainfo.sensors)
