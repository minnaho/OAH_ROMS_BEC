################################
# plot time series
# of mean wind magnitude/direction in a box
# around Catalina island 
# from ROMS file
###############################
import numpy as np
import datetime
from netCDF4 import num2date, date2num
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import scipy.io as sio

# load wind data from ROMS bgc model
# /data/project1/ROMS/students/
# data is axis 0: 12 months and axis 1: 746 hours
data_path_1999 = '/data/project1/ROMS/students/TSwnd1999.mat'
wind_mat_1999 = sio.loadmat(data_path_1999)
wind_1999 = wind_mat_1999['TSwnd']

data_path_2007 = '/data/project1/ROMS/students/TSwnd2007.mat'
wind_mat_2007 = sio.loadmat(data_path_2007)
wind_2007 = wind_mat_2007['TSwnd']

save_figs = '/wind_timeseries/'

#######################################
# create dates for separate time series
#######################################
unit_1999 = 'hours since 1999-1-1'
n_hours_1999 = 365*24 # hours in a year
range_1999 = np.array(range(n_hours_1999))
dates_1999 = num2date(range_1999,unit_1999)

unit_2007 = 'hours since 2007-1-1'
n_hours_2007 = 365*24 # hours in a year
range_2007 = np.array(range(n_hours_2007))
dates_2007 = num2date(range_2007,unit_2007)

################################################
# flatten array to plot 
################################################
wind_1999_flat = wind_1999.flatten()
wind_2007_flat = wind_2007.flatten()

##############
# PLOT DATA
#############
xlabel_size = 18
ylabel_size = 16
title_size = 20

x_tick_size = 14
y_tick_size = 14

rot = 15
title = 'Hourly Wind Speed between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)'

f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1999,wind_1999_flat[:n_hours_1999])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.set_ylabel('Wind Speed m $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax1.grid(True)

#locator = mdate.YearLocator()
#ax1.xaxis.set_major_locator(locator)
#ax1.set_xlabel('Days')

ax2.plot(dates_2007,wind_2007_flat[:n_hours_2007])
#locator = mdate.YearLocator()
#ax1.gca().xaxis.set_major_locator(locator)
#ax1.gcf().autofmt_xdate()
plt.setp(ax2.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax2.get_yticklabels(),fontsize=y_tick_size)
#ax2.set_xlabel('Days',fontsize=xlabel_size)
ax2.set_ylabel('Wind Speed m $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle(title,fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+'wind_timeseries_full.png',bbox_inches='tight')


################################################
# plot for Feb 1 - June 30 1999 
#################################################
feb1 = 600 
jun30 = 4199
f=plt.figure(figsize=[14,8])
plt.plot(dates_1999[feb1:jun30],wind_1999_flat[feb1:jun30])
ax = plt.gca()
plt.setp(ax.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
#plt.setp(ax.get_xticklabels(),fontsize=x_tick_size)
plt.setp(ax.get_yticklabels(),fontsize=y_tick_size)
plt.ylabel('Wind Speed m $s^{\mathregular{-1}}$',fontsize=ylabel_size)
locator = mdate.MonthLocator()
plt.gca().xaxis.set_major_locator(locator)
#plt.gcf().autofmt_xdate()

#plt.grid(True)
#f.autofmt_xdate()
plt.title(title,fontsize=title_size)
ax.grid(True)

plt.savefig(save_figs+'wind_timeseries_full_1999.png',bbox_inches='tight')



