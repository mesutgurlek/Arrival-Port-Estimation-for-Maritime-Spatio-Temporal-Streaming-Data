import csv

filename = 'training_labeled.csv'

data = []
header = []
# read data
with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    
    for i, row in enumerate(reader):
	# skip header line
        if i == 0:
            header = row
        data.append(row)
# sort w.r.t ship_ids
shipids = [x[0] for x in data]
ind = [i[0] for i in sorted(enumerate(shipids), key=lambda x:x[1])]
sortedData = [data[ind[i]] for i in range(len(data))]

with open('sorted_' + filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(header)
    for dat in sortedData:
        writer.writerow(dat)
        


# convert timestamps to numerical values

# not working because of timestamp datatype
def isSorted(data):
    for i in range(len(data) - 1):
        if data[i][0] == data[i + 1][0] and (not data[i][7] < data[i + 1][7]):
            print(i)
            print(data[i][0], data[i + 1][0])
            print(data[i][7], data[i + 1][7]) # should be numerical
            return False
    return True
        
