import numpy as np
import pandas as pd

riv = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/daily_flow_2007_2018_santa_margarita.txt',skiprows=44,header=None,sep='\t')

#interpolate temp values
temp_min = riv[13][2:].astype(float).interpolate().values.ravel().tolist()
temp_max = riv[11][2:].astype(float).interpolate().values.ravel().tolist()
temp_mean = np.nanmean((temp_min,temp_max),axis=0)

#interpolate pH values
ph_min = riv[31][2:].astype(float).interpolate().values.ravel().tolist()
ph_max = riv[29][2:].astype(float).interpolate().values.ravel().tolist()
ph_mean = np.nanmean((ph_min,ph_max),axis=0)

#interpolate do values
do_min = riv[25][2:].astype(float).interpolate().values.ravel().tolist()
do_max = riv[23][2:].astype(float).interpolate().values.ravel().tolist()
do_mean = np.nanmean((do_min,do_max),axis=0)
# first few values still nan
do_mean[:3] = do_mean[3]

text_file = open('sm_temp.txt','w')
for i in temp_mean:
    text_file.write(str(i)+'\n')

text_file = open('sm_ph.txt','w')
for i in ph_mean:
    text_file.write(str(i)+'\n')

text_file = open('sm_do.txt','w')
for i in do_mean:
    text_file.write(str(i)+'\n')
