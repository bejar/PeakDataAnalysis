"""
.. module:: plots

plots
*************

:Description: plots

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2014 13:40 

"""

__author__ = 'bejar'

from pylab import *


def plotHungarianSignals(coinc, centers1, centers2, vmax, vmin, name, title, path):
    """
    Plots two sets of signals according to the Hungarian Algorithm assignment
    :param coinc:
    :param centers1:
    :param centers2:
    :param name:
    :param title:
    :param path:
    :return:
    """

    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    i=1
    n= len(coinc)
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    for i1, i2 in coinc:
        if i1 < centers1.shape[0]:
            s1 = centers1[i1]
            plotSignalValues(fig, s1, n, 2, i, 'cluster' + str(i1), vmax, vmin)
        else:
            plotDummy(fig, centers1.shape[0], n, 2, i, '')

        if i2 < centers2.shape[0]:
            s2 = centers2[i2]

            plotSignalValues(fig, s2, n, 2, i+1, 'cluster' + str(i2), vmax, vmin)
        else:
            plotDummy(fig, centers2.shape[0], n, 2, i+1, '')
        i += 2

    fig.suptitle(title, fontsize=48)
    fig.savefig(path+'/'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()



def plotSignals(signals, n, m, vmax, vmin, name, title, path, cstd=None):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    i=1
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    for s, snm in signals:
        if min(s) != max(s):
            if cstd is not None:
                pstd = cstd[i-1]
            plotSignalValues(fig, s, n, m, i, snm, vmax, vmin, cstd=pstd)
        else:
            plotDummy(fig, len(s), n, m, i, snm)
        i += 1

    fig.suptitle(title, fontsize=48)
    fig.savefig(path+'/'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()
#    plt.show()

def show_signal(signal):
    """
    Plots a signal
    :param signal:
    :return:
    """
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    minaxis = min(signal)
    maxaxis = max(signal)
    num = len(signal)
    sp1 = fig.add_subplot(111)
    sp1.axis([0, num, minaxis, maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t, signal)

    plt.show()

def show_two_signals(signal1, signal2):
    """
    Shows two signals in the same picture
    :param signal1:
    :param signal2:
    :return:
    """
    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    minaxis = min(signal1)
    maxaxis = max(signal1)
    num = len(signal1)
    sp1 = fig.add_subplot(111)
    sp1.axis([0, num, minaxis, maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t, signal1)
    sp1.plot(t, signal2)
    plt.show()




# Plot a set of signals
def plotSignalValues(fig, signal1, n, m, p, name, vmax, vmin, cstd=None):
    minaxis=vmin#min(signal1)
    maxaxis= vmax#max(signal1)
    num=len(signal1)
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    plt.axhline(linewidth=4, color='r', y=np.mean(signal1))
    pstd = np.std(signal1)
    plt.axhline(linewidth=4, color='b', y=np.mean(signal1)+pstd)
    plt.axhline(linewidth=4, color='b', y=np.mean(signal1)-pstd)
    sp1.plot(t,signal1)
    if cstd is not None:
        sp1.plot(t, signal1 + cstd)
        sp1.plot(t, signal1 - cstd)

#    plt.show()

def plotDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t, t)
#    plt.show()


def plotMatrices(matrices, n, m, name, title, path):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(50)
    fig.set_figheight(60)
    i=1
    plt.subplots_adjust(hspace = 0.1, wspace = 0.1)
    for s, snm in matrices:
        if s is not None:
            plotMatrixValues(fig,s,n,m,i, snm)
        else:
            plotMatrixDummy(fig,len(s),n,m,i, snm)
        i += 1

    fig.suptitle(title, fontsize=60)
    fig.savefig(path+'/'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()
#    plt.show()


# Plot a set of signals
def plotMatrixValues(fig, matrix, n, m, p, name):
    sp1=fig.add_subplot(n,m,p)
    plt.title(name, fontsize=48)
    sp1.imshow(matrix,  cmap=plt.cm.gray, interpolation='none')
#    plt.show()

def plotMatrixDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t,t)
#    plt.show()


def plotMatrix(matrix,name, title, ticks, lticks, path):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(50)
    fig.set_figheight(60)
    sp1=fig.add_subplot(1,1,1)
    plt.title(title, fontsize=48)
    img = sp1.imshow(matrix,  cmap=plt.cm.seismic, interpolation='none')
    plt.xticks(ticks, lticks, fontsize=28)
    plt.yticks(ticks, lticks, fontsize=28)
    plt.subplots_adjust(bottom=0.15)
    fig.colorbar(img, orientation='horizontal')
    fig.savefig(path+'/corr-'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()