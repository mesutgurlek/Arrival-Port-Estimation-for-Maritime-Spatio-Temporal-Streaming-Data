import csv

filename = 'debs2018_training_labeled.csv'

data = []
# read data
with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    
    for i, row in enumerate(reader):
	# skip header line
        if i == 0:
            continue
        data.append(row)
# sort w.r.t ship_ids
shipids = [x[0] for x in data]
ind = [i[0] for i in sorted(enumerate(shipids), key=lambda x:x[1])]
sortedData = [data[ind[i]] for i in range(len(data))]
# convert timestamps to numerical values

