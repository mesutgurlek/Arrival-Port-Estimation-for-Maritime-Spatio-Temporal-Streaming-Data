from matplotlib import pyplot
from pandas import read_csv
from datetime import datetime


# Load Dataset
def parse(timestamp):
    date = ''
    format_type = True if len(timestamp.split('-')) > 1 else False
    if format_type:
        try:
            date = datetime.strptime(timestamp, "%d-%m-%y %H:%M")
        except Exception as e:
            print("Got Exception 1: ", timestamp)
    else:
        try:
            date = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
        except Exception as e:
            print("Got Exception 2: ", timestamp)

    return date

dataset_path  = '../Dataset/training_dataset.csv'
df = read_csv(dataset_path,  parse_dates = ['TIMESTAMP'],  index_col=False, date_parser=parse)
df.drop('SHIPTYPE', axis=1, inplace=True)
df.drop('ARRIVAL_PORT_CALC', axis=1, inplace=True)
df.drop('ARRIVAL_CALC', axis=1, inplace=True)

# manually specify column names
df.columns = ['SHIP_ID', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'DEPARTURE_PORT_NAME', 'REPORTED_DRAUGHT']
dataset = df.sort_values(by=['SHIP_ID', 'TIMESTAMP'])

# save to file
dataset.to_csv(path_or_buf='../Dataset/preprocess_outputs/processed.csv', index=False)


values = dataset.values
# specify columns to plot
groups = [1, 2, 3, 5, 6, 8]
i = 1
# plot each column
pyplot.figure()
for group in groups:
    pyplot.subplot(len(groups), 1, i)
    pyplot.plot(values[:, group])
    pyplot.title(dataset.columns[group], y=0.5, loc='right')
    i += 1
pyplot.show()