# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 08:18:00 2013

Clusters signals a bunch of times and test the distance among the clusters

@author: bejar
"""



import scipy.io
from sklearn.cluster import KMeans
from ClValIndicescp import VINMI,Arand
from numpy import mean, std
import numpy as np
#import time


# Loads all the matlab files and generates a dictionary with
# the clusters, the data of the peaks and the list of the peaks
def loadClusterData(signals,ndata):
#    cpath='/home/bejar/Dropbox/Gennaro/Gatos/Lab Rudomin/FILTRO GE/ClassCorr/'
    cpath='/home/bejar/Dropbox/Filtro Rudomin/Estability/CTRL2/'
    
    rsignals={}
    for s in signals:
        for name in ndata:
            mats=scipy.io.loadmat( cpath+'/'+name+'.'+ s+'.mat')
            if not s in rsignals:
                rsignals[s]=(mats['Dc2'])
            else:
                rsignals[s]=(np.append(rsignals[s],mats['Dc2'],axis=0))
    
    return rsignals
    
    

lsignals=['L4cd','L4ci','L5cd','L5ci','L5rd','L5ri','L6cd', 'L6ci','L6rd','L6ri', 'L7ri']
ndata=['capsa1','capsa2','capsa3']#,'ctrl1','ctrl2','lido1','lido2','lido3','lido4']    
nclust=11
niter=40

ldata=loadClusterData(lsignals,ndata)
cpath='/home/bejar/Documentos/Investigacion/cinvestav/Cluster/'
rname='capsa123.txt'
f = open(cpath+rname,'w')

for s in lsignals:
    f.write( '-----> '+s+'\n')
    data=ldata[s]
    print '-----> '+s
    for nc in range(4,21): 
    
        lclasif=[]
        for i in range(niter):
            k_means = KMeans(init='k-means++', n_clusters=nc, n_init=10,n_jobs=-1)
            k_means.fit(data)
            lclasif.append(k_means.labels_.copy())
            print '.',
            
        vnmi=[]
        vrand=[]
        for i in range(niter):
            for j in range(i+1,niter):
                _,nmi=VINMI(lclasif[i],lclasif[j])
                #rand=Arand(lclasif[i],lclasif[j])
                vnmi.append(nmi)
        print '\n'
                
        f.write( str(nc)+' '+str(mean(vnmi))+'\n')
        f.flush()
f.close()
    

        

    
    
    

