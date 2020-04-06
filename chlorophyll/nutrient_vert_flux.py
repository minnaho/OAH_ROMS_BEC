################################
# plot time series
# of mean chlorophyll in a box
# around Catalina island 
# from ROMS file
###############################
import os
import glob
from netCDF4 import Dataset
import numpy as np
import datetime
from netCDF4 import num2date, date2num
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

# file numbers in glob path that calculations need to be done on
i = 7
f_numbers = [0,1,4,7,8,9,10,11]
f = f_numbers[i]

# save figs path
save_figs = './nutrient_vert_flux_figs/'

# load data from ROMS bgc model
data_path = '/data/project1/ROMS/students/W*_L1*.nc'
glob_paths = glob.glob(data_path)
data = glob_paths[f]
data_nc = Dataset(data,'r')
var_nc = data_nc.variables['var']
chl = np.copy(var_nc)

# file name for saving figures
file_name = os.path.basename(data)
ind_end = file_name.index('.')
data_file = file_name[0:ind_end]+'_'

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
y_label = 'Nutrient Vertical Flux $m^{\mathregular{3}}$ $s^{\mathregular{-1}}$'

f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997,ts[:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.set_ylabel(y_label,fontsize=ylabel_size)
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
ax2.set_ylabel(y_label,fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Nutrient Vertical Flux between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

'''
f.add_subplot(111,frameon=False)
plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
plt.grid(False)
plt.ylabel(y_label,fontsize=ylabel_size)
'''

plt.savefig(save_figs+data_file+'nutrient_vert_flux_timeseries_full.png',bbox_inches='tight')
print('saved timeseries')

################################################
# plot for year 1999 and 2007 to compare to winds
#################################################
f, (ax1,ax2) = plt.subplots(2,1,figsize=(14,8),sharey=True)
ax1.plot(dates_1997[730:],ts[730:n_days_1997])
plt.setp(ax1.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax1.get_yticklabels(),fontsize=y_tick_size)
ax1.set_ylabel(y_label,fontsize=ylabel_size)
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
ax2.set_ylabel(y_label,fontsize=ylabel_size)
ax2.grid(True)

#f.autofmt_xdate()
f.subplots_adjust(hspace=.35)
plt.suptitle('Average Nutrient Vertical Flux between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax = plt.gca()
ax.grid(True)

plt.savefig(save_figs+data_file+'nutrient_vert_flux_timeseries_1999_2007.png',bbox_inches='tight')
print('saved 1999 2007')

################################################
# plot for Feb 1 - June 30 1999 
#################################################
f=plt.figure(figsize=[14,8])
plt.plot(dates_1997[761:910],ts[761:910])
ax = plt.gca()
#plt.setp(ax.get_xticklabels(),fontsize=x_tick_size,rotation=rot)
plt.setp(ax.get_xticklabels(),fontsize=x_tick_size)
plt.setp(ax.get_yticklabels(),fontsize=y_tick_size)
plt.ylabel(y_label,fontsize=ylabel_size)
locator = mdate.MonthLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()

#plt.grid(True)
#f.autofmt_xdate()
plt.title('Average Nutrient Vertical Flux between (33.15$\degree$,-119.05$\degree$), (33.25$\degree$,-118.9$\degree$)',fontsize=title_size)
ax.grid(True)

plt.savefig(save_figs+data_file+'nutrient_vert_flux_timeseries_1999.png',bbox_inches='tight')
print('saved 1999')
