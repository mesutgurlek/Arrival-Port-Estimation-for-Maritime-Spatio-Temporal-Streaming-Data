#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 02:18:32 2018

@author: melih
"""

import pandas as pd
import numpy as np
from itertools import groupby
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

def get_counts(data):
    '''Returns total nnumber of transactions and data'''
    transaction_ids = set()
    ship_ids= data.loc[:, 'SHIP_ID'].tolist()
    [transaction_ids.add(x) for x in ship_ids]
    return len(transaction_ids), len(ship_ids)

def labels2onehot(labels):
    # encode class values as integers
    encoder = LabelEncoder()
    encoder.fit(labels)
    encoded_Y = encoder.transform(labels)
    # convert integers to dummy variables (i.e. one hot encoded)
    return np_utils.to_categorical(encoded_Y)

class Transaction_Reader():
        
    def __init__(self, file):
        self.data = pd.read_csv(file)
        self.batch = None
        self.total_transactions,total_data = get_counts(self.data)
        self.current_idx = 0
        self.current_batch = -1
        self.ship_ids = self.data.loc[:, 'SHIP_ID'].tolist()
        self.trans_freqs = [len(list(group)) for key, group in groupby(self.ship_ids)]
        self.labels_onehot = labels2onehot(self.data.loc[:, 'ARRIVAL_PORT_CALC'])
        
    def next_batch(self):
        ''' Returns rows of next transaction as 2-d numpy array'''
        self.current_batch += 1
        if self.current_batch >= self.total_transactions:
            return None
        next_idx = self.trans_freqs[self.current_batch]
        X = self.data.loc[self.current_idx:self.current_idx + next_idx - 1, 'SPEED':'HEADING']
        y = self.labels_onehot[self.current_idx:self.current_idx + next_idx - 1]
        self.current_idx += next_idx
        return np.array(X), np.array(y)
        
    def hasnext_batch(self):
        return self.current_batch < self.total_transactions
    
