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
from scipy.signal import resample
from sklearn.cluster import KMeans
from collections import Counter


def plotSignalsMax(signals, pp, n, m, title, maxaxis, minaxis, rsens):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    fig.suptitle(str(title), fontsize=48)
    i=1
    # vmax = []
    # vmin = []
    # for s, _ in signals:
    #     vmax.append(np.max(s))
    #     vmin.append(np.min(s))
    for s,snm in signals:
        plotSignalValuesMax(fig,s,n,m,i,snm,maxaxis, minaxis, rsens)
        i+=1
    fig.savefig(pp, orientation='landscape',format='pdf')
    plt.close()

# Plot a set of signals
def plotSignalValuesMax(fig,signal1,n,m,p,name, maxaxis, minaxis, rsens):
    num = signal1.shape[1]
    sp1 = fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    if name == rsens:
        sp1.patch.set_facecolor('red')
        sp1.patch.set_alpha(0.2)


    t = arange(0.0, num, 1)
    vmax = np.max(signal1, axis=0)
    vmin = np.min(signal1, axis=0)
    vmean = np.mean(signal1, axis=0)
    vstd = np.std(signal1, axis=0)

    sp1.plot(t,vmean,'r', linewidth=3)
    sp1.plot(t,vmean+(2*vstd), 'b', linewidth=2)
    sp1.plot(t,vmean-(2*vstd), 'b', linewidth=2)
    sp1.plot(t,vmax, 'g', linewidth=1)
    sp1.plot(t,vmin, 'g', linewidth=1)

#    plt.show()

def plotSignalsAll(signals, pp, n, m, title):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    fig.suptitle(str(title), fontsize=48)
    i=1
    vmax = []
    vmin = []
    for s, _ in signals:
        vmax.append(np.max(s))
        vmin.append(np.min(s))
    for s,snm in signals:
        plotSignalValuesAll(fig,s,n,m,i,snm,np.max(vmax), np.min(vmin))
        i+=1
    fig.savefig(pp, orientation='landscape',format='pdf')
    plt.close()

# Plot a set of signals
def plotSignalValuesAll(fig,signal1,n,m,p,name, maxaxis, minaxis):
    num = signal1.shape[1]
    sp1 = fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    for i in range(signal1.shape[0]):
        sp1.plot(t,signal1[i])
#    plt.show()


def plotSignals(signals, pp, n, m, title, maxaxis, minaxis, rsens):
    fig = plt.figure()
    fig.set_figwidth(16)
    fig.set_figheight(30)
    fig.suptitle(str(title), fontsize=48)
    i=1
    # vmax = []
    # vmin = []
    # for s, _ in signals:
    #     vmax.append(np.max(s))
    #     vmin.append(np.min(s))
    for s,snm in signals:
        if min(s) != max(s):
            plotSignalValues(fig,s,n,m,i,snm,maxaxis, minaxis, rsens)
        else:
            plotDummy(fig,len(s),n,m,i,snm)
        i+=1
    fig.savefig(pp, orientation='landscape',format='pdf')
    plt.close()

#    plt.show()



# Plot a set of signals
def plotSignalValues(fig,signal1,n,m,p,name, maxaxis, minaxis, rsens):
    num = len(signal1)
    sp1 = fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])

    if name == rsens:
        sp1.patch.set_facecolor('red')
        sp1.patch.set_alpha(0.2)
    t = arange(0.0, num, 1)
    sp1.plot(t,signal1)
#    plt.show()

def plotDummy(fig,num,n,m,p,name):
    minaxis = -1
    maxaxis  =1
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


def extract_sincro(raw, lsync, sens, nsens, resamp, twin):
    """
    Generates a list of data matrices with syncronizations (one for each sensor)
    """
    def busca_syn(syn, s):
        for sig, time, cl in syn:
            if s == sig:
                return time
        return s, 0

    sigmatrix = []
    for i in range(len(sens)):
        sigmatrix.append(np.zeros((len(lsync), twin)))

    for i, syn in enumerate(lsync):
        center = busca_syn(syn, nsens)
        if center - (twin/2) > 0 and center + (twin/2) < raw.shape[0]:
            for j in range(len(sens)):
                sigmatrix[j][i] = raw[center - (twin/2):center + (twin/2), j]


    # for i in range(len(sigmatrix)):
    #     sigmatrix[i] = resample(sigmatrix[i], resamp, axis=1, window=resamp*2)

    return sigmatrix


def select_sensor(synchs, sensor, slength):
    """
    Maintains only the syncs corresponding to the given sensor

    :param synchs:
    :param sensor:
    :return:
    """
    lres = []
    for syn in synchs:
        for s, _, _ in syn:
            if s == sensor and len(syn) >= slength:
                lres.append(syn)
    return lres


def draw_sincro(lclusters, n_clusters, nex, cres, name, sens, rsens):
    """
    Generates files with syncronizations
    """
    pp = PdfPages(cres+'/synch-cluster-raw' + name + '.pdf')

    vmax = []
    vmin = []
    for cl in lclusters:
        vmax.append(np.max(cl))
        vmin.append(np.min(cl))

    for i in range(n_clusters):
        lsig = []
        for cl, s in zip(lclusters, sens):
            lsig.append((cl[i], s))

        plotSignals(lsig, pp, 6, 2, rsens + ' Clase' + str(int(i)) + ' (' + str(nex[i]) + ')', np.max(vmax), np.min(vmin), rsens)

    pp.close()

def draw_sincro_all(lclusters, n_clusters, nex, cres, name, sens, rsens):
    """
    Generates files with syncronizations
    """
    pp = PdfPages(cres+'/synch-cluster-raw' + name + '.pdf')

    for i in range(n_clusters):
        lsig = []
        for cl, s in zip(lclusters, sens):
            lsig.append((cl[i], s))

        plotSignalsAll(lsig, pp, 6, 2, rsens + ' Clase' + str(int(i)) + '(' + str(nex[i]) + ')')

    pp.close()

def draw_sincro_max(lclusters, n_clusters, nex, cres, name, sens, rsens):
    """
    Generates files with syncronizations
    """
    pp = PdfPages(cres+'/synch-cluster-raw' + name + '.pdf')
    vmax = []
    vmin = []
    for cl in lclusters:
        for c in cl:
            vmax.append(np.max(c))
            vmin.append(np.min(c))


    for i in range(n_clusters):
        lsig = []
        for cl, s in zip(lclusters, sens):
            lsig.append((cl[i], s))

        plotSignalsMax(lsig, pp, 6, 2, rsens + ' Clase' + str(int(i)) + '(' + str(nex[i]) + ')', np.max(vmax), np.min(vmin), rsens)

    pp.close()

if __name__ == '__main__':
    window = 400  # concidence window for the synchronization
    resampw = 6.0
    print 'W=', int(round(window))
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e140515']

    TVD = False
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]
        peakw = 2000 # Window to extract for each peak from the signal
        slength = 2 # Number of signals synchronized
        n_clusters = 12 # Number of clusters for the synchronizations
        resampw = 170 # Resampling window

        for rsensor in ['L5ri', 'L5ci', 'L6ri', 'L6ci']:
            print rsensor
            nsensor = datainfo.sensors.index(rsensor)
            # dfile = datainfo.datafiles[0]
            for dfile in datainfo.datafiles:
                print dfile

                lsens_labels = []
                #compute the labels of the data
                for sensor in datainfo.sensors:
                    lsens_labels.append(compute_data_labels(datainfo.dpath + datainfo.name, datainfo.datafiles[0], dfile, datainfo.sensors[0], sensor))

                # Times of the peaks
                ltimes = []
                expcounts = []
                f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')
                for sensor in datainfo.sensors:
                    d = f[dfile + '/' + sensor + '/' + 'TimeClean']
                    data = d[()]
                    #expcounts.append(data.shape[0])
                    ltimes.append(data)
                lsynchs = compute_synchs(ltimes, lsens_labels, window=window)
                lsynchs = select_sensor(lsynchs, nsensor, slength)
                d = f[dfile + '/Raw']
                raw = d[()]
                f.close()

                lmatrix = extract_sincro(raw, lsynchs, datainfo.sensors, nsensor, resampw, peakw)

                cmatrix = lmatrix[nsensor]

                km = KMeans(n_clusters=n_clusters)

                km.fit(cmatrix)
                nex = Counter(km.labels_)
                print nex
                lcentroids = []
                for cm in lmatrix:
                    cent = np.zeros((n_clusters, peakw))
                    for cl in range(n_clusters):
                        cent[cl] = np.sum(cm[cl == km.labels_], axis=0)/nex[cl]
                    lcentroids.append(cent)

                draw_sincro(lcentroids, n_clusters, nex, datainfo.dpath + '/Results', dfile + '-' + rsensor + '-Len' + str(slength) + '-nC'+str(n_clusters), datainfo.sensors, rsensor)

                lcentroids = []
                for cm in lmatrix:
                    cent = []
                    for cl in range(n_clusters):
                        cent.append(cm[cl == km.labels_])
                    #print cent
                    lcentroids.append(cent)
                draw_sincro_max(lcentroids, n_clusters, nex, datainfo.dpath + '/Results', dfile + '-' + rsensor + '-Len' + str(slength) + '-nC'+str(n_clusters) + '-X', datainfo.sensors, rsensor)
