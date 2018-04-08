from pandas import read_csv
from datetime import datetime
from matplotlib import pyplot

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

dataset_path  = '../Dataset/training_dataset.csv' ## apply on transactional_labeled.csv
df = read_csv(dataset_path,  parse_dates = ['TIMESTAMP'], index_col=False, date_parser=parse)
df.drop('SHIPTYPE', axis=1, inplace=True)
df.drop('ARRIVAL_PORT_CALC', axis=1, inplace=True)
#df.drop('ARRIVAL_CALC', axis=1, inplace=True)
df.drop('REPORTED_DRAUGHT', axis=1, inplace=True)
df.drop('DEPARTURE_PORT_NAME', axis=1, inplace=True)


# manually specify column names
df.columns = ['SHIP_ID', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'ARRIVAL_PORT_CALC']
dataset = df.sort_values(by=['SHIP_ID', 'TIMESTAMP'])
dataset.drop('SHIP_ID', axis=1, inplace=True)

# save to file
dataset.to_csv('../Dataset/preprocess_outputs/arrival_calc_processed.csv', index=False)

values = dataset.values
# specify columns to plot
groups = [0, 1, 2, 3, 4, 5]
i = 1
# plot each column
print('plot')
pyplot.figure()
for group in groups:
    pyplot.subplot(len(groups), 1, i)
    pyplot.plot(values[:, group])
    pyplot.tight_layout(pad=0.1)
    pyplot.title(dataset.columns[group], y=1.0, loc='right')
    i += 1
pyplot.show()
