"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    Clusters the Peaks from an experiment all the files together

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 8:10 

"""

__author__ = 'bejar'

import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220', 'e120516', 'e140515']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220', 'e140304']

lexperiments = ['e150514'] #['e150514b']

#colors = 'rrryyyyyyyyybbbbbbbbbbbbb'
ext = ''

#expname = lexperiments[3]
for expname in lexperiments:
    datainfo = experiments[expname]
    colors = datainfo.colors

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

    for s, nclusters in zip(datainfo.sensors, datainfo.clusters):
        print s
        ldata = []
        for dfiles in datainfo.datafiles:
            d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
            dataf = d[()]
            ldata.append(dataf)

        data = ldata[0] #np.concatenate(ldata)

        km = KMeans(n_clusters=nclusters)
        km.fit_transform(data)
        lsignals = []
        cnt = Counter(list(km.labels_))

        lmax = []
        for i in range(km.n_clusters):
            lmax.append((i,np.max(km.cluster_centers_[i])))
        lmax = sorted(lmax, key=itemgetter(1))

        print lmax
        print data.shape

        lhisto = []
        for dataf, ndata in zip(ldata, datainfo.datafiles):
            histo = np.zeros(nclusters)
            for i in range(dataf.shape[0]):
                histo[km.predict(dataf[i])] += 1.0
            histo /= dataf.shape[0]
            print datainfo.name, ndata
            print histo
            histosorted = np.zeros(nclusters)
            for i in range(histosorted.shape[0]):
                histosorted[i] = histo[lmax[i][0]]
            lhisto.append(histosorted)

        # for h in lhisto[1:]:
        #     rms = np.dot(lhisto[0] - h,  lhisto[0] - h)
        #     rms /= h.shape[0]
        #     print np.sqrt(rms), hellinger_distance(h, lhisto[0])

        matplotlib.rcParams.update({'font.size': 26})
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1)
        fig.set_figwidth(60)
        fig.set_figheight(40)

        ind = np.arange(nclusters)  # the x locations for the groups
        width = 1.0/(len(lhisto)+1)   # the width of the bars
        ax.set_xticks(ind+width)
        ax.set_xticklabels(ind)
        for i, h in enumerate(lhisto):
            rects = ax.bar(ind+(i*width), h, width, color=colors[i])
        fig.suptitle(datainfo.name + '-' + s + ext, fontsize=48)

        minaxis = np.min(km.cluster_centers_)
        maxaxis = np.max(km.cluster_centers_)

        for nc in range(nclusters):
            ax2 = fig.add_subplot(2, nclusters, nc+nclusters+1)
            signal = km.cluster_centers_[lmax[nc][0]]
            plt.title(' ( '+str(cnt[lmax[nc][0]])+' )')
            t = arange(0.0, len(signal), 1)
            ax2.axis([0, len(signal), minaxis, maxaxis])
            ax2.plot(t,signal)
            plt.axhline(linewidth=1, color='r', y=0)
        fig.savefig(datainfo.dpath+'/Results/' + datainfo.name + '-' + s + ext + '-histo-sort.pdf', orientation='landscape', format='pdf')
    #    plt.show()

        print '*******************'
        for nc in range(nclusters):
            lsignals.append((km.cluster_centers_[lmax[nc][0]], str(nc)+' ( '+str(cnt[lmax[nc][0]])+' )'))

        #print s, np.max(km.cluster_centers_), np.min(km.cluster_centers_)
        if nclusters % 2 == 0:
            part = nclusters /2
        else:
            part = (nclusters /2) + 1
        plotSignals(lsignals,part,2,np.max(km.cluster_centers_),np.min(km.cluster_centers_), datainfo.name + '-' + s + ext,
                    datainfo.name + '-' + s + ext, datainfo.dpath+'/Results/')
        # for cc in range(nclusters):
        #     show_signal(km.cluster_centers_[cc])
    f.close()