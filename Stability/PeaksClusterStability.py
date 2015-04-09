# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 08:18:00 2013

Clusters signals a bunch of times and test the distance among the clusters

@author: bejar
"""

import time

import scipy.io
from sklearn.cluster import KMeans
from numpy import mean
from sklearn import metrics


# Loads all the matlab files and generates a dictionary with
# the clusters, the data of the peaks and the list of the peaks
def loadClusterData(signals, name):
    cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/WHOLE/capsa06-01-2011/ctrl/'

    rsignals = {}
    for s in signals:
        # mats=scipy.io.loadmat( cpath+'/lido4.'+ s+'.mat')
        #        rsignals[s]=(mats['Dc2'])
        mats = scipy.io.loadmat(cpath + name + '.' + s + '.mat')
        rsignals[s] = (mats['Trazos'])

    return rsignals


lsignals = ['L4cd', 'L4ci', 'L5cd', 'L5ci', 'L5rd', 'L5ri', 'L6cd', 'L6ci', 'L6rd', 'L6ri', 'L7ri']
# lsignals=['L5ci']

niter = 40

name = 'trazos'
ldata = loadClusterData(lsignals, name)
rname = '/home/bejar/Documentos/Investigacion/cinvestav/Cluster/' + name + '-20110106-whole-ctrl.txt'
f = open(rname, 'w')

for s in lsignals:
    print s
    f.write('-----> ' + s + '\n')
    data = ldata[s]
    for nc in range(4, 21):
        print time.ctime()
        print nc, '=',
        lclasif = []
        for i in range(niter):
            k_means = KMeans(init='k-means++', n_clusters=nc, n_init=10, n_jobs=-1)
            k_means.fit(data)
            lclasif.append(k_means.labels_.copy())
            print i,

        vnmi = []
        vrand = []
        for i in range(niter):
            for j in range(i + 1, niter):
                nmi = metrics.adjusted_mutual_info_score(lclasif[i], lclasif[j])
                vnmi.append(nmi)

        f.write(str(nc) + ' ' + str(mean(vnmi)) + '\n')
        f.flush()
        print
f.close()

    
    
    

