#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 16:11:10 2018

@author: melih
"""

import csv

filename = '../Dataset/sorted_training_dataset.csv'

data = []
header = []
# read data
with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    
    for i, row in enumerate(reader):
	# skip header line
        if i == 0:
            header = row
            continue
        data.append(row)

transactional_data = []
# first data's departure port
depart = data[0][8]
ship_id = data[0][0]
transaction_id = 1
i = 0
for entry in data:
    if (entry[11] == ''): # drop missing rows for arrival port
        continue
    if (entry[6] == ''): # drop missing rows for heading
        continue
    if entry[8] != depart or entry[0] != ship_id: # if transaction changes
        transaction_id += 1
        depart = entry[8]
        ship_id = entry[0]
    transaction_entry = [transaction_id] + entry[1:] #remove ship_id
    transactional_data.append(transaction_entry)

with open('../Dataset/preprocess_outputs/transactional_labeled.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(header)
    for dat in transactional_data:
        writer.writerow(dat)
      
