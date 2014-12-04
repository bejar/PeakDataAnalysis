"""
.. module:: ComputeSubsequences

ComputeSubsequences
*************

:Description: ComputeSubsequences

    

:Authors: bejar
    

:Version: 

:Created on: 03/10/2014 9:55 

"""

__author__ = 'bejar'


from rstr_max import *
import operator
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import networkx as nx
from operator import itemgetter, attrgetter, methodcaller
from util.misc import compute_frequency_remap

def drawgraph(nodes, edges, nfile, legend):
    rfile = open(rpath + 'maxseq-' + nfile + '.dot', 'w')

    rfile.write('digraph G {\nsize="20,20"\nlayout="neato"\n'+
                'imagepath="'+ipath+'"\n'+
                'imagescale=true'+'\n'+
                'labeljust=r'+'\n'+
                'labelloc=b'+'\n'+
                'nodesep=0.4'+'\n'+
                'fontsize="30"\nlabel="'+legend+'"\n')

    radius = 5.0

    nnodes = len(nodes)
    for i in range(nnodes):
        posx = -np.cos(((np.pi*2)/nnodes)*i + (np.pi/2))*radius
        posy = np.sin(((np.pi*2)/nnodes)*i+ (np.pi/2))*radius
        rfile.write(str(nodes[i])+'[label="'+ str(i+1) +'",labeljust=l, labelloc=b, fontsize="24",height="0.2"' +
                    ', image="'+line+'.cl'+str(nodes[i])+'.png'+'"' +
                    ', pos="'+str(posx)+','+str(posy)+'!", shape = "square"];\n')

    for e, nb, pe in edges:
        if len(e) == 2:
            rfile.write(str(e[0])+'->'+str(e[1]))
            # if pe/nb > 1.3:
            #        rfile.write('[color="red"]')
            # if pe/nb < 0.7:
            #        rfile.write('[color="green"]')
            rfile.write('\n')

    rfile.write('}\n')

    rfile.close()


def drawgraph_with_edges(nodes, edges, nfile):
    rfile = open(rpath + 'maxseq-' + nfile + '.dot', 'w')

#    rfile.write('digraph G {\nsize="6,6"\nlayout="neato"\nfontsize="30"\nlabel="'+nfile+'"\n')
    rfile.write('digraph G {\nsize="20,20"\nlayout="neato"\n'+
                'imagepath="' + ipath + '"\n' +
                'imagescale=true' + '\n' +
                'labeljust=r' +  '\n' +
                'labelloc=b' + '\n' +
                'nodesep=0.4' + '\n' +
                'fontsize="30"\nlabel="'+nfile+'"\n')

    radius = 5.0

    nnodes = len(nodes)
    for i in range(nnodes):
        posx = -np.cos(((np.pi*2)/nnodes)*i + (np.pi/2))*radius
        posy = np.sin(((np.pi*2)/nnodes)*i + (np.pi/2))*radius
        rfile.write(str(nodes[i])+'[label="'+str(i+1)+'",labeljust=l, labelloc=b, fontsize="24",height="0.7"' +
                    ', image="'+line+'.cl'+str(nodes[i])+'.png'+'"' +
                    ', pos="'+str(posx)+','+str(posy)+'!", shape = "square"];\n')


        # rfile.write(str(i+1)+'[label="'+str(i+1) +
        #             '", fontsize="24",height="0.7"' +
        #             'image="'+rpath+'cl1.png'+'"' +
        #             ', pos="'+str(posx)+','+str(posy) +
        #             '!", shape = "circle"];\n')
    rfile.write('\n')
    for e in edges:
        if len(e) == 2:
            rfile.write(str(e[0])+'->'+str(e[1])+'\n')

    rfile.write('}\n')

    rfile.close()


def max_seq_long(nexp, clpeaks, timepeaks, sup, nfile, remap, gap=0):
    """
    Secuencias con soporte mas que un limite grabadas en fichero de texto

    :param nexp:
    :param clpeaks:
    :param timepeaks:
    :param sup:
    :param nfile:
    :param remap:
    :param gap:
    :return:
    """
    # Select the index of the experiment
    peakini = 0
    i = 0
    while i < nexp:
        exp = timepeaks[i]
        peakini += exp.shape[0]
        i += 1

    exp = timepeaks[nexp]
    peakend = peakini + exp.shape[0]

    # Build the sequence string
    peakstr = ''


    for i in range(peakini, peakend):
        peakstr += voc[clpeaks[i][0]]
        if i < peakend-1 and gap != 0:
            if (timepeaks[nexp][i-peakini+1] - timepeaks[nexp][i-peakini]) > gap:
                peakstr += '#'

    # Compute the sufix array
    rstr = Rstr_max()
    rstr.add_str(peakstr)

    r = rstr.go()

    # Compute the sequences that have minimum support
    lstrings = []

    for (offset_end, nb), (l, start_plage) in r.iteritems():
        ss = rstr.global_suffix[offset_end-l:offset_end]
        id_chaine = rstr.idxString[offset_end-1]
        s = rstr.array_str[id_chaine]
        #print '[%s] %d'%(ss.encode('utf-8'), nb)
        if nb > sup and len(ss.encode('utf-8')) > 1:
            lstrings.append((ss.encode('utf-8'), nb))

    lstrings = sorted(lstrings, key=operator.itemgetter(0), reverse=True)
    lstringsg = []
    rfile = open(rpath + 'maxseqlong-' + nfile + '.txt', 'w')
    cntlong = np.zeros(10)
    for seq, s in lstrings:
        wstr = ''
        if not '#' in seq:
            sigsym = []
            for c in range(len(seq)):
                #wstr += str(remap[voc.find(seq[c])-1])
                wstr += '{0:0>2d}'.format(voc.find(seq[c]))
                #rmp = remap[voc.find(seq[c])-1]
                rmp = voc.find(seq[c])
                sigsym.append(rmp)
                if c < (len(seq)-1):
                    wstr += ' - '
            lstringsg.append(sigsym)
            wstr += ' = ' + str(s)

            rfile.write('[' + str(len(seq)) + '] ' + wstr+'\n')
            cntlong[len(seq)] += 1
    rfile.close()
    for i in range(2,10):
        print i, ':', cntlong[i]
    print '----------'


def max_seq_exp(nexp, clpeaks, timepeaks, nfile, remap, gap=0):
    """
    Grafos de las secuencias
    :param nexp:
    :param clpeaks:
    :param timepeaks:
    :param sup:
    :param nfile:
    :param remap:
    :param gap:
    :return:
    """
    # Select the index of the experiment
    peakini = 0
    i = 0
    while i < nexp:
        exp = timepeaks[i]
        peakini += exp.shape[0]
        i += 1

    exp = timepeaks[nexp]
    peakend = peakini + exp.shape[0]

    # Build the sequence string
    peakstr = ''

    peakfreq = {'#': 0}

    for i in range(peakini, peakend):
        peakstr += voc[clpeaks[i][0]]
        if i < peakend-1 and gap != 0:
            if (timepeaks[nexp][i-peakini+1] - timepeaks[nexp][i-peakini]) > gap:
                peakstr += '#'
                peakfreq['#'] += 1

        if voc[clpeaks[i][0]] in peakfreq:
            peakfreq[voc[clpeaks[i][0]]] += 1
        else:
            peakfreq[voc[clpeaks[i][0]]] = 1

    #print peakend - peakini, len(peakstr), len(peakstr)*(1.0 / (len(peakfreq)*len(peakfreq)))
    sup= int(round(len(peakstr)*(1.0 / (len(peakfreq)*len(peakfreq))))*1.2)
    print sup

    for l in peakfreq:
        peakfreq[l] = (peakfreq[l]* 1.0)/len(peakstr)
    #     print l, (peakfreq[l]* 1.0)/(peakend - peakini)
    #    print clpeaks[i][0]


    # Compute the sufix array
    rstr = Rstr_max()
    rstr.add_str(peakstr)

    r = rstr.go()

    # Compute the sequences that have minimum support
    lstrings = []

    for (offset_end, nb), (l, start_plage) in r.iteritems():
        ss = rstr.global_suffix[offset_end-l:offset_end]
        id_chaine = rstr.idxString[offset_end-1]
        s = rstr.array_str[id_chaine]
        #print '[%s] %d'%(ss.encode('utf-8'), nb)
        if nb > sup and len(ss.encode('utf-8')) > 1:
            lstrings.append((ss.encode('utf-8'), nb))

    lstrings = sorted(lstrings, key=operator.itemgetter(0), reverse=True)
    lstringsg = []
    rfile = open(rpath + 'maxseq-' + nfile + '.txt', 'w')
    for seq, s in lstrings:
        wstr = ''
        prob = 1.0
        if not '#' in seq:
            sigsym = []
            for c in range(len(seq)):
                #wstr += str(remap[voc.find(seq[c])-1])
                wstr += str(voc.find(seq[c]))
                #rmp = remap[voc.find(seq[c])-1]
                rmp = voc.find(seq[c])
                sigsym.append(rmp)
                prob *= peakfreq[seq[c]]
                if c < (len(seq)-1):
                    wstr += ' - '
            lstringsg.append((sigsym, prob, (s * 1.0) /(len(peakstr) - 1)))
            wstr += ' = ' + str(s) + ' ( ' + str(prob) + ' / ' + str((s * 1.0) /(len(peakstr) - 1)) + ' )'

            rfile.write(wstr+'\n')
    rfile.close()

    nsig = len(peakfreq)
    if '#' in peakfreq:
        nsig -= 1
    drawgraph(remap, lstringsg, nfile, nfile+' sup(%d)'%sup)



def max_peaks_edges(nexp, clpeaks, timepeaks, sup, gap=0):
    # Select the index of the experiment
    peakini = 0
    i = 0
    while i < nexp:
        exp = timepeaks[i]
        peakini += exp.shape[0]
        i += 1

    exp = timepeaks[nexp]
    peakend = peakini + exp.shape[0]

    # Build the sequence string
    peakstr = ''

    peakfreq = {'#': 0}

    for i in range(peakini, peakend):
        peakstr += voc[clpeaks[i][0]]
        if i < peakend-1 and gap != 0:
            if (timepeaks[nexp][i-peakini+1] - timepeaks[nexp][i-peakini]) > gap:
                peakstr += '#'
                peakfreq['#'] += 1

        if voc[clpeaks[i][0]] in peakfreq:
            peakfreq[voc[clpeaks[i][0]]] += 1
        else:
            peakfreq[voc[clpeaks[i][0]]] = 1

    print peakend - peakini, len(peakstr), len(peakstr) * (1.0 / (len(peakfreq) * len(peakfreq)))

    for l in peakfreq:
        peakfreq[l] = (peakfreq[l]* 1.0)/len(peakstr)
    #     print l, (peakfreq[l]* 1.0)/(peakend - peakini)
    #    print clpeaks[i][0]


    # Compute the sufix array
    rstr = Rstr_max()
    rstr.add_str(peakstr)

    r = rstr.go()

    # Compute the sequences that have minimum support
    lstrings = []

    for (offset_end, nb), (l, start_plage) in r.iteritems():
        ss = rstr.global_suffix[offset_end-l:offset_end]
        id_chaine = rstr.idxString[offset_end-1]
        s = rstr.array_str[id_chaine]
        #print '[%s] %d'%(ss.encode('utf-8'), nb)
        if nb > sup and len(ss.encode('utf-8')) > 1:
            lstrings.append((ss.encode('utf-8'), nb))

    lstrings = sorted(lstrings, key=operator.itemgetter(0))
    lstringsg = []
    for seq, s in lstrings:
        wstr = ''
        prob = 1.0
        if not '#' in seq:
            sigsym = []
            for c in range(len(seq)):
                #rmp = remap[voc.find(seq[c])-1]
                rmp = voc.find(seq[c])
                sigsym.append(rmp)
                prob *= peakfreq[seq[c]]
            lstringsg.append(sigsym)


    return lstringsg


def generate_sequences():
    remap = compute_frequency_remap(timepeaks, clpeaks)

    for exp, _, nfile in nfiles:
        max_seq_exp(exp, clpeaks, timepeaks, line+'-'+nfile, remap, gap=300)


def generate_sequences_long():

    remap = compute_frequency_remap(timepeaks, clpeaks)

    for exp, sup, nfile in nfiles:
        max_seq_long(exp, clpeaks, timepeaks, sup, line+'-'+nfile, remap, gap=300)


def generate_diff_sequences():

    remap = compute_frequency_remap(timepeaks, clpeaks)

    ledges1 = max_peaks_edges(1, clpeaks, timepeaks, 20, gap=300)
    ledges2 = max_peaks_edges(2, clpeaks, timepeaks, 25, gap=300)

    for e in ledges1:
        if e in ledges2:
            ledges2.remove(e)

    drawgraph_with_edges(remap, ledges2, 'dif-'+line+'-'+'ctrl2-capsa1')

#remap = [1,2,15,4,3,13,12,11,14,5,10,8,6,7,9]

cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/'
rpath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/'
ipath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/icons/'
ocpath = '/home/bejar/Documentos/Investigacion/cinvestav/'

nfiles = [(0, 15, 'ctrl1'), (1, 15, 'ctrl2'), (2, 20, 'capsa1'), (3, 20, 'capsa2'), (4, 20, 'capsa3'),
          (5, 15, 'lido1'), (6, 15, 'lido2'), (7, 15, 'lido3'), (8, 15, 'lido4'), (9, 15, 'lido5'), (10, 15, 'lido6')
          ]
# nfiles = [(0, 'ctrl1')
#           ]


aline = [('L4cd', 'k9.n5', 9),
         ('L4ci', 'k9.n1', 9),
        ('L5cd', 'k10.n6' , 10),
        #('L5rd', 'k20.n1' ),
        ('L5ci', 'k15.n1', 15),
        ('L5ri', 'k15.n9', 15),
        ('L6cd', 'k17.n1', 17),
        ('L6rd', 'k13.n9', 13),
        #('L6ci', 'k15.n1'),
        ('L6ri', 'k18.n4', 18),
        ('L7ri', 'k18.n4', 18)
        ]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# line = 'L6ri'  # 'L6rd' 'L5ci' 'L6ri'
# clust = '.k15.n1'  # '.k20.n5' '.k16.n4' '.k15.n1'

for line, clust, _ in aline:
    print line
    matpeaks = scipy.io.loadmat(cpath + 'Selected/centers.' + line + '.' + clust + '.mat')
    mattime = scipy.io.loadmat(cpath + '/WholeTime.' + line + '.mat')

    clpeaks = matpeaks['IDX']
    timepeaks = mattime['temps'][0]

    generate_sequences()

#generate_sequences_long()

#generate_sequences()

#generate_diff_sequences()