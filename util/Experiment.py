"""
.. module:: Experiment

Experiment
*************

:Description: Experiment

    

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 11:44 

"""

__author__ = 'bejar'


class Experiment():
    """
    Class for the experiments
    """
    name = None
    sampling = None
    datafiles = None
    sensors = None
    dpath = None

    def __init__(self, dpath, name, sampling, datafiles, sensors):
        self.name = name
        self.sampling = sampling
        self.datafiles = datafiles
        self.sensors = sensors
        self.dpath = dpath

