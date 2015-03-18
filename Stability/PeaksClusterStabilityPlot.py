"""
.. module:: PeaksClusterStabilityPlot

PeaksClusterStabilityPlot
*************

:Description: PeaksClusterStabilityPlot

    

:Authors: bejar
    

:Version: 

:Created on: 02/03/2015 7:09 

"""

__author__ = 'bejar'

import matplotlib.pyplot as plt
from pylab import *

path = '/home/bejar/Documentos/Investigacion/cinvestav/Cluster/'
name = 'trazos-20120516-wholeEspaciado'
file = open(path+name+'.txt','r')

all=file.readlines()
file.close()

line=0
cline=all[line].split(' ')
nsig=1
fig = plt.figure()
while line<len(all):
    signal=cline[1]
    print signal
    numc=[]
    valc=[]
    line+=1
    cline=all[line].split(' ')
    while cline[0]!='----->' and line < len(all):
        numc.append(int(cline[0]))
        valc.append(float(cline[1]))
        line+=1
        if line<len(all):
            cline=all[line].split(' ')
    ax = fig.add_subplot(6,2,nsig)
    xis=ax.axis([4,max(numc),0.5,1])
    plt.xticks(np.arange(4,max(numc)+1,2))
    ax.text(6,0.9,signal)
    ax.plot(numc,valc)
    plt.title(name)
    nsig+=1
fig.set_figwidth(15)
fig.set_figheight(30)
fig.savefig(path+'/'+name+'.pdf', orientation='landscape',format='pdf')