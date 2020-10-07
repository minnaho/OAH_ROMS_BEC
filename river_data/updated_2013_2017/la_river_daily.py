# turn hourly LA river flow to daily
import numpy as np
import pandas as pd

path = '/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/'
fi = '/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/hourly_flow_2002_2018_los_angeles_river.csv'

riv = pd.read_csv(fi,header=None,skiprows=2)
form = '%m/%d/%Y %H:%M:%S'
riv[0] = pd.to_datetime(riv[0]+' '+riv[1],format=form)
riv.set_index(riv[0],inplace=True)

del riv[1]
del riv[3]

daily = riv.resample('D').mean()

daily_2007_2018 = daily['2007':'2018']

df = pd.DataFrame({'flow cfs':daily_2007_2018[2]})
df.to_csv(path+'daily_flow_2007_2018_los_angeles_river.txt')
