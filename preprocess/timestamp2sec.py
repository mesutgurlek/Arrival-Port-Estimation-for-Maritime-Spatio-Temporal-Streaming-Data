#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# convert timestamp to seconds
# --------------------------------------------------------

from datetime import datetime
import time
import csv


filepath = '../Dataset/training_dataset.csv'

# Read data
dataset = []
with open(filepath) as File:
    reader = csv.DictReader(File)
    for row in reader:
        dataset.append(row)

# Modify Dataset
for idx, row in enumerate(dataset):
    timestamp = row['TIMESTAMP']
    format_type = True if len(timestamp.split('-')) > 1 else False
    if format_type:
        d = datetime.strptime(timestamp, "%d-%m-%y %H:%M")
    else:
        d = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
    sec = time.mktime(d.timetuple())
    dataset[idx]['TIMESTAMP'] = sec

# Write dataset into csv
with open('../Dataset/preprocess_outputs/timestamp2sec.csv', 'w') as csvfile:
    fieldnames = ['SHIP_ID', 'SHIPTYPE', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'DEPARTURE_PORT_NAME', 'REPORTED_DRAUGHT', 'ARRIVAL_CALC', 'ARRIVAL_PORT_CALC']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset)
