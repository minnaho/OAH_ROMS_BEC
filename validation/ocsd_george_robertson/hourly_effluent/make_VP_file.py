import pandas as pd
import numpy as np
import datetime as dt
from netCDF4 import Dataset,num2date

monthly_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
monthly_data = Dataset(monthly_path,'r').variables['flow'][:,2,2]

time_nc = Dataset(monthly_path,'r').variables['time']
time_arr = time_nc[:]
monthly_date = num2date(time_arr,time_nc.units)

df_raw = pd.read_excel('OCSD_hourly_effluent_minna_edits.xlsx',sheet_name=0,header=None,skiprows=1,usecols='A,C:D')

flow_gal_day = np.array(df_raw[3]*1000000.)
date_str = np.array(df_raw[0].astype(str))

date_no_hr_l = []
for d_i in date_str:
    date_no_hr_l.append(dt.datetime.strptime(d_i,'%Y-%m-%d'))

date_no_hr = np.array(date_no_hr_l)

date_hr_l = []
for d_i in range(len(date_no_hr)):
    add_hours = dt.timedelta(hours=float(df_raw[2][d_i]))
    date_hr_l.append(date_no_hr[d_i] + add_hours)

date_hr = np.array(date_hr_l)

flow_m3_s = flow_gal_day/(264.172052*86400)

####################
# write file
####################
file_name = 'hourly_effluent.flo'
f = open(file_name,'w')
f.write('1.0 '+str(len(flow_m3_s))+' m3/s '+file_name+'\n')
for i in flow_m3_s:
    f.write(str(i)+'\n')
