"""
.. module:: misc

misc
*************

:Description: misc

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2014 13:37 

"""

__author__ = 'bejar'

import numpy as np


def find_time(exp, ini, step):
    """
    Find the index of the peak that is at step time from the ini peak
    :param exp:
    :param ini:
    :return:
    """
    i = ini + 1;
    while i < exp.shape[0] and exp[i] < exp[ini] + step:
        i += 1
    return i

def probability_matrix(peakstr, init, end, nsym, laplace=0.0):
    """
    Computes the probability matrix of transitions from a sequence between two points
    :param peakstr:
    :param init:
    :param end:
    :return:
    """

    pm = np.zeros((nsym, nsym)) + laplace
    for i in range(init, end-1):
        if peakstr[i] != -1 and peakstr[i+1] != -1:
            pm [peakstr[i]-1, peakstr[i+1]-1] += 1.0
#    print pm
    return pm/pm.sum()