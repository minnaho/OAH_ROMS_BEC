import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from netCDF4 import Dataset,num2date
plt.ion()

monthly_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
monthly_data_m3_s = Dataset(monthly_path,'r').variables['flow'][:,2,2]

time_nc = Dataset(monthly_path,'r').variables['time']
time_arr = time_nc[:]
monthly_date = num2date(time_arr,time_nc.units)

df_raw = pd.read_excel('OCSD_hourly_effluent_minna_edits.xlsx',sheet_name=0,header=None,skiprows=1,usecols='A,C:D')

#flow_gal_day = np.array(df_raw[3]*1000000.)
flow_gal_day = np.array(df_raw[3])
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

monthly_data = (monthly_data_m3_s*(264.172052*86400))/1000000.
#flow_m3_s = flow_gal_day/(264.172052*86400)
flow_m3_s = flow_gal_day

# monthly average of hourly data (732 is approx how many hours in a month)
flow_monthly = np.empty((flow_m3_s[::732].shape[0]))
for i in range(flow_m3_s[::732].shape[0]):
    flow_monthly[i] = np.nanmean(flow_m3_s[i*732:(i+1)*732])
    

#################
# plotting
################
title_font = 18
axis_font = 16
legend_size = 16

hours = mdates.HourLocator(interval=2)
h_fmt = mdates.DateFormatter('%H:%M')

plt.figure(figsize=[14,10])
#plt.plot(date_hr[52500:55000],flow_m3_s[52500:55000])
plt.plot(date_hr,flow_m3_s,color='lightblue',label='Hourly flow')
plt.plot(date_hr[::732],flow_monthly,color='red',label='Monthly averaged')
#plt.plot(monthly_date[200:],monthly_data[200:],color='red')
#plt.plot(date_hr[-72:-1],flow_m3_s[-72:-1])
ax = plt.gca()
ax.grid()
#ax.xaxis.set_major_locator(hours)
#ax.xaxis.set_major_formatter(h_fmt)
plt.xticks(rotation=50)
plt.xlabel('Time (hourly)',fontsize=axis_font)
#plt.ylabel('Flow (m$^3$/s)',fontsize=axis_font)
plt.ylabel('Flow (MGD)',fontsize=axis_font)
plt.title('Hourly and Monthly Flow OCSD',fontsize=title_font)
plt.legend(loc='best',fontsize=legend_size)
plt.tick_params(axis='both',which='major',labelsize=axis_font)
plt.savefig('hourly_monthly_flow_ocsd_new.png',bbox_inches='tight')
    


