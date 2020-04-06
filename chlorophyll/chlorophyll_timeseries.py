################################
# plot time series
# of mean chlorophyll in a box
# around Catalina island 
# from ROMS file
###############################
from netCDF4 import Dataset
import numpy as np
import datetime
from netCDF4 import num2date, date2num
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

save_figs = './chlorophyll_timeseries/'

# load data from ROMS bgc model
# /data/project1/ROMS/students/CHLA_L1.nc
data_path = '/data/project1/ROMS/students/CHLA_L1.nc'
chla = Dataset(data_path,'r')
chlorophyll = chla.variables['var']
chl = np.copy(chlorophyll)


# load usw1_grd.nc for lat/lon variables
grid_path = '/data/project1/ROMS/OAH/Faycal/grid/USSW1/usw1_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc_grid = grid_nc.variables['lat_rho']
lon_nc_grid = grid_nc.variables['lon_rho']

lat_nc = np.copy(lat_nc_grid)
lon_nc = np.copy(lon_nc_grid)
#######################
# get domain of data
#######################
# get grid coordinates for lat/lon of desired domain
lat_b = [33.15,33.25]
lon_b = [-119.05,-118.9]

x_coord = []
y_coord = []

for i in range(len(lat_b)):
    lat_you_want = lat_b[i]
    lon_you_want = lon_b[i]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    x_coord.append(xi_coord)
    y_coord.append(eta_coord)    

# box of data
bx = chl[:,x_coord[0]:x_coord[1]+1,y_coord[1]:y_coord[0]+1]

# take mean across y and x axis
m = np.mean(bx,axis=2)
ts = np.mean(m,axis=1)

###########################
# separate time series
###########################
unit_1997 = 'days since 1997-1-1'
n_days_1997 = 1095
range_1997 = np.array(range(n_days_1997))
dates_1997 = num2date(range_1997,unit_1997)

unit_2006 = 'days since 2006-1-1'
n_days_2006 = len(ts)-n_days_1997
range_2006 = np.array(range(n_days_2006))
dates_2006 = num2date(range_2006,unit_2006)

##############
# PLOT DATA
#############
xlabel_size = 18
ylabel_size = 16
title_size = 22

x_tick_size = 14
y_tick_size = 14

rot = 30

f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997,ts[:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax1.grid(True)

#locator = mdate.YearLocator()
#ax1.xaxis.set_major_locator(locator)
#ax1.set_xlabel('Days')

ax2.plot(dates_2006,ts[n_days_1997:])
#locator = mdate.YearLocator()
#ax1.gca().xaxis.set_major_locator(locator)
#ax1.gcf().autofmt_xdate()
plt.setp(ax2.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax2.get_yticklabels(),fontsize=y_tick_size)
#ax2.set_xlabel('Days',fontsize=xlabel_size)
ax2.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries.png',bbox_inches='tight')

################################################
# plot for year 1999 and 2007 to compare to winds
#################################################
f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997[730:],ts[730:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax1.grid(True)

#locator = mdate.YearLocator()
#ax1.xaxis.set_major_locator(locator)
#ax1.set_xlabel('Days')

ax2.plot(dates_2006[365:],ts[n_days_1997+365:])
#locator = mdate.YearLocator()
#ax1.gca().xaxis.set_major_locator(locator)
#ax1.gcf().autofmt_xdate()
plt.setp(ax2.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax2.get_yticklabels(),fontsize=y_tick_size)
#ax2.set_xlabel('Days',fontsize=xlabel_size)
ax2.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries_1999_2007.png',bbox_inches='tight')


################################################
# plot for Feb 1 - June 30 1999 
#################################################
f=plt.figure(figsize=[14,8])
plt.plot(dates_1997[761:910],ts[761:910])
ax = plt.gca()
#plt.setp(ax.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax.get_xticklabels(),fontsize=x_tick_size)
plt.setp(ax.get_yticklabels(),fontsize=y_tick_size)
plt.ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
locator = mdate.MonthLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()

#plt.grid(True)
#f.autofmt_xdate()
plt.title('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries_1999.png',bbox_inches='tight')


#########################################
# PLOT DATA with annual mean + 5% line
########################################
# calculate annual mean + 5%
med_1999_calc = np.median(ts[730:n_days_1997]) * 1.05
#med_1999 = np.full((ts[730:n_days_1997].shape),med_1999_calc)
med_1999 = np.ones((ts.shape)) * med_1999_calc


xlabel_size = 18
ylabel_size = 16
title_size = 22

x_tick_size = 14
y_tick_size = 14

legend_label = '1999 annual median + 5%'

rot = 15

f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997,ts[:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.plot(dates_1997,med_1999[:n_days_1997],label=legend_label,color='red')
ax1.legend(loc='best')
ax1.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax1.grid(True)

#locator = mdate.YearLocator()
#ax1.xaxis.set_major_locator(locator)
#ax1.set_xlabel('Days')

ax2.plot(dates_2006,ts[n_days_1997:])
#locator = mdate.YearLocator()
#ax1.gca().xaxis.set_major_locator(locator)
#ax1.gcf().autofmt_xdate()
plt.setp(ax2.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax2.get_yticklabels(),fontsize=y_tick_size)
ax2.plot(dates_2006,med_1999[n_days_1997:],label=legend_label,color='red')
#ax2.set_xlabel('Days',fontsize=xlabel_size)
ax2.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries_median.png',bbox_inches='tight')

################################################
# plot for year 1999 and 2007 to compare to winds
#################################################
f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997[730:],ts[730:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.plot(dates_1997[730:],med_1999[730:n_days_1997],label=legend_label,color='red')
ax1.legend(loc='best')
ax1.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax1.grid(True)

#locator = mdate.YearLocator()
#ax1.xaxis.set_major_locator(locator)
#ax1.set_xlabel('Days')

ax2.plot(dates_2006[365:],ts[n_days_1997+365:])
#locator = mdate.YearLocator()
#ax1.gca().xaxis.set_major_locator(locator)
#ax1.gcf().autofmt_xdate()
plt.setp(ax2.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax2.get_yticklabels(),fontsize=y_tick_size)
ax2.plot(dates_2006[365:],med_1999[n_days_1997+365:],label=legend_label,color='red')
#ax2.set_xlabel('Days',fontsize=xlabel_size)
ax2.set_ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries_median_1999_2007.png',bbox_inches='tight')


################################################
# plot for Feb 1 - June 30 1999 
#################################################
f=plt.figure(figsize=[14,8])
plt.plot(dates_1997[761:910],ts[761:910])
ax = plt.gca()
#plt.setp(ax.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax.get_xticklabels(),fontsize=x_tick_size)
plt.setp(ax.get_yticklabels(),fontsize=y_tick_size)
plt.plot(dates_1997[761:910],med_1999[761:910],label=legend_label,color='red')
plt.legend(loc='best')
plt.ylabel('Chlorophyll mg C $m^{\mathregular{-2}}$ $s^{\mathregular{-1}}$',fontsize=ylabel_size)
locator = mdate.MonthLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()

#plt.grid(True)
#f.autofmt_xdate()
plt.title('Average Chlorophyll between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax.grid(True)

plt.savefig(save_figs+'chlorophyll_timeseries_median_1999.png',bbox_inches='tight')

