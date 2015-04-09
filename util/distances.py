"""
.. module:: distances

distances
*************

:Description: distances

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2014 13:01 

"""

__author__ = 'bejar'

import numpy as np


def sKLD(m1, m2):
    """
    Simetrized Kullback-Leibler divergence between two probability matrices
    :param m1:
    :param m2:
    :return:
    """
    lm1 = np.log(m1)
    lm2 = np.log(m2)
    lquot12 = np.log(m1 / m2)
    lquot21 = np.log(m2 / m1)
    dkl12 = lm1 * lquot12
    dkl21 = lm2 * lquot21
    return dkl12.sum() + dkl21.sum()


def renyihalf(m1, m2):
    """
    Renyi divergence for parameter 1/2
    :param m1:
    :param m2:
    :return:
    """

    pm = m1 * m2
    spm = np.sqrt(pm)

    return -2 * np.log(spm.sum())


def square_frobenius(m1, m2):
    """
    Square frobenius distance between two matrices
    :param m1:
    :param m2:
    :return:
    """
    c = m1 - m2
    c = c * c
    return c.sum()
