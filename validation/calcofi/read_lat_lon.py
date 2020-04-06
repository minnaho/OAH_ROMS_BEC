import pandas as pd

read_file = pd.read_csv('lat_lon.csv',header=None)
unique_lat = list(set(list(read_file.iloc[:,0])))
