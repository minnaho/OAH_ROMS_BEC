#############################################
# plot_south_coast_rivers.py
# plot data from Final River Compilation and
# rational methods file (SCB_RIVERS.mat)  
# from netcdf files 
# south_coast_rivers_10_years_no_watershed.nc
# south_coast_rivers_24_years.nc
#####################################################
import numpy as np
import pickle
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
import cftime
import datetime
import copy
from collections import defaultdict
from netCDF4 import Dataset, date2num, num2date
import openpyxl
from openpyxl import Workbook

# makes matplotlib register real_datetime as datetime objects 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
matplotlib.units.registry[cftime.real_datetime] = matplotlib.units.registry[datetime.datetime]
###################
# FOLDER PATHS
####################
save_figs_path = './river_figs/'

################################
# CALL DATA FROM netcdf files  
################################

# load river netcdf files
nc_10 = Dataset('south_coast_rivers_10_years_no_watershed_new.nc','r')
nc_24 = Dataset('south_coast_rivers_24_years_new.nc','r')

time_10 = nc_10.variables['time']
lats_10 = nc_10.variables['latitude']
lons_10 = nc_10.variables['longitude']
flow_10 = nc_10.variables['flow']
NH4_10 = nc_10.variables['ammonium']
NO3_10 = nc_10.variables['nitrate']
PO4_10 = nc_10.variables['phosphate']
TN_10 = nc_10.variables['total_nitrogen']
TP_10 = nc_10.variables['total_phosphorus']

date_10 = num2date(np.asarray(time_10),time_10.units)

time_24 = nc_24.variables['time']
lats_24 = nc_24.variables['latitude']
lons_24 = nc_24.variables['longitude']
flow_24 = nc_24.variables['flow']
NH4_24 = nc_24.variables['ammonium']
NO3_24 = nc_24.variables['nitrate']
PO4_24 = nc_24.variables['phosphate']
TN_24 = nc_24.variables['total_nitrogen']
TP_24 = nc_24.variables['total_phosphorus']

date_24 = num2date(np.asarray(time_24),time_24.units)

mol_wt_N = 14.007 # total nitrogen
seconds_in_day = 86400
mg_to_kg = 1./1e6

#########################
# PLOT SUM DAILY LOAD OF ALL RIVERS IN ONE YEAR (1997)
#########################
st = 0
en = 340
sum_N_10 = np.array(np.nansum(np.nansum(NH4_10[st:en],axis=1),axis=1))
sum_N_24 = np.array(np.nansum(np.nansum(NH4_24[2557+st:2557+en],axis=1),axis=1))
sum_N_all = sum_N_10 + sum_N_24
sum_flow_10 = np.array(np.nansum(np.nansum(flow_10[st:en],axis=1),axis=1))
sum_flow_24 = np.array(np.nansum(np.nansum(flow_24[2557+st:2557+en],axis=1),axis=1))
sum_flow_all = sum_flow_10 + sum_flow_24

# flux of N kg/day
kg_to_Mg = 1/1e3
flux_N = sum_N_all * sum_flow_all * seconds_in_day*mol_wt_N*mg_to_kg*kg_to_Mg

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
xlabel_size = 16
ylabel_size = 16
title_size = 16
# date indexes for date_24: 1997-1-1 to 2013-12-31
start_ind = 2557
end_ind = 8766
fig_w = 10
fig_h = 8
tick_label_size = 12
adjust_top = .95
hspace = 0

fig = plt.figure(figsize=[fig_w,fig_h])
plt.ylabel('NH4 Mg day$^{-1}$',fontsize=ylabel_size)
plt.plot(date_10[st:en],flux_N,linewidth=2)
locator = mdate.MonthLocator()
ax = plt.gca()
ax.xaxis.set_major_locator(locator)
ax.axes.xaxis.set_ticklabels(months)
ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
ax.grid(True)
#plt.yticks(np.arange(0, max(flux_N)+1, 500.0))
plt.savefig(save_figs_path+'flux_NH4_short.png',bbox_inches='tight')

