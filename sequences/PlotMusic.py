"""
.. module:: PlotMusic

PlotMusic
*************

:Description: PlotMusic

    

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 12:02 

"""

__author__ = 'bejar'
import numpy as np
import matplotlib.pyplot as plt
from pyx import *
import scipy.io

from config.paths import datapathnew, seqpath


freq = 1.6  # Khz
window = 60000  # ms
cols = ['r', 'g', 'b', 'y', 'm', 'c', 'b', 'r', 'g', 'b']

lines = [  # 'L4cd',
           'L4ci',
           'L5cd',
           #'L5rd',
           'L5ci', 'L5ri', 'L6cd', 'L6rd', 'L6ci',
           'L6ri', 'L7ri']

mattime = scipy.io.loadmat(datapathnew + '/Symbols/peaks-' + 'L5cd' + '.mat')
data = mattime['E02capsa1']

c = canvas.canvas()

y = 1.8

p = path.line(1, y, 28, y)
c.stroke(p)
p = path.line(1, y, 1, y + 10)
c.stroke(p)
scale = 0.05
nc = 10

c.text(12, 10, 'L5CD Capsa1', [text.size(3)])

for i in range(180):
    print data[i],
    x = data[i, 1] / 1600.0
    col = (data[i, 0] / (nc + 1.0))
    print x, col
    p = path.rect(1 + x, y, scale, 50 * scale)
    c.stroke(p, [deco.filled([color.rgb(0, col / 2, col)])])

maxt = data[i, 1] / 1600
print maxt

cnt = 0
i = 0
while i < maxt + 1:
    p = path.rect(1 + (i), y - 0.2, 0, 2 * scale)
    c.stroke(p)
    if cnt % 5 == 0:
        c.text(1 + (i), y - 0.8, str(i) + 's', [text.size(-1)])
    i += 1
    cnt += 1
d = document.document([document.page(c)])

d.writePDFfile(seqpath + "/plot-music-L5CD-capsa1")
