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
df = read_csv(dataset_path,  parse_dates = ['TIMESTAMP'], index_col=False, date_parser=parse)
df.drop('SHIPTYPE', axis=1, inplace=True)
df.drop('ARRIVAL_PORT_CALC', axis=1, inplace=True)
df.drop('ARRIVAL_CALC', axis=1, inplace=True)

# manually specify column names
df.columns = ['SHIP_ID', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'DEPARTURE_PORT_NAME', 'REPORTED_DRAUGHT']
dataset = df.sort_values(by=['SHIP_ID', 'TIMESTAMP'])

# save to file
dataset.to_csv('../Dataset/preprocess_outputs/processed.csv')
