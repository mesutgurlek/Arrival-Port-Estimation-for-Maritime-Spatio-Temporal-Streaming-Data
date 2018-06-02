#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 18:52:26 2018

@author: melih
"""

import pandas as pd
import numpy as np

class Predictor():
    
    def __init__(self, learner):
        self._learner = learner
        
    def predict(self, start_ports, test_targets):
        test_port_idxs = np.array([self._learner.port2index[port] for port in start_ports])
        test_target_idxs = np.array([self._learner.port2index[port] for port in test_targets])
        pred_idxs = np.argmax(self._learner.prob_mat[test_port_idxs], axis=1)
        pred_ports = np.array([self._learner.index2port[pred] for pred in pred_idxs])
        acc = np.mean((test_target_idxs == pred_idxs))
        return acc, pred_ports