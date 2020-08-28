#############################################
# plot_potw.py
# plot data from POTW_INTERP-ms edits_Minna_edits.xlsx
# converted to python data through open_excel_potw.py 
#####################################################
import numpy as np
from netCDF4 import Dataset,num2date
import matplotlib
import cftime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
import datetime

# makes matplotlib register real_datetime as datetime objects 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
matplotlib.units.registry[cftime.real_datetime] = matplotlib.units.registry[datetime.datetime]

###############################
# load major potw, minor potw, rivers netcdf
##############################
#potw
major_nc = Dataset('major_potw_data.nc','r')
minor_nc = Dataset('minor_potw_data.nc','r')
# river
#nc_10 = Dataset('../river_data/south_coast_rivers_10_years_no_watershed_new.nc','r')
#nc_24 = Dataset('../river_data/south_coast_rivers_24_years_new.nc','r')
nc_10 = Dataset('../river_data/south_coast_rivers_10_years_monthly_new.nc','r')
nc_24 = Dataset('../river_data/south_coast_rivers_24_years_monthly_new.nc','r')

# times
time_ma = num2date(major_nc.variables['time'][:],major_nc.variables['time'].units)
time_mi = num2date(minor_nc.variables['time'][:],minor_nc.variables['time'].units)
time_10 = nc_10.variables['time']
time_24 = nc_24.variables['time']
date_10 = num2date(np.asarray(time_10),time_10.units)
date_24 = num2date(np.asarray(time_24),time_24.units)


# time indexes start and end for major pipes 1997-end 
t_st = 313
t_en = -1

# conversions
sec2day = 86400
mol_wt_N = 14
mg_to_kg = 1./1e6
kg_to_Mg = 1/1e3
conv = sec2day*(mol_wt_N/1000)*(1/(1000*1000)) # flux Mg/day

# major potw individual
# ocsd 
flow_ma_o = major_nc.variables['flow'][t_st:t_en,2,2]
nh4_ma_o = major_nc.variables['NH4'][t_st:t_en,2,2]
no3_ma_o = major_nc.variables['NO3'][t_st:t_en,2,2]
no2_ma_o = major_nc.variables['NO2'][t_st:t_en,2,2]
# hyperion 
flow_ma_h = major_nc.variables['flow'][t_st:t_en,0,0]
nh4_ma_h = major_nc.variables['NH4'][t_st:t_en,0,0]
no3_ma_h = major_nc.variables['NO3'][t_st:t_en,0,0]
no2_ma_h = major_nc.variables['NO2'][t_st:t_en,0,0]
# jwpcp
flow_ma_j = major_nc.variables['flow'][t_st:t_en,1,1]
nh4_ma_j = major_nc.variables['NH4'][t_st:t_en,1,1]
no3_ma_j = major_nc.variables['NO3'][t_st:t_en,1,1]
no2_ma_j = major_nc.variables['NO2'][t_st:t_en,1,1]
# plwtp
flow_ma_p = major_nc.variables['flow'][t_st:t_en,3,3]
nh4_ma_p = major_nc.variables['NH4'][t_st:t_en,3,3]
no3_ma_p = major_nc.variables['NO3'][t_st:t_en,3,3]
no2_ma_p = major_nc.variables['NO2'][t_st:t_en,3,3]

# put them into an array shape (4,48) (outfall,month)
flow_ma_t = np.array((flow_ma_o,flow_ma_h,flow_ma_j,flow_ma_p))
nh4_ma_t = np.array((nh4_ma_o,nh4_ma_h,nh4_ma_j,nh4_ma_p))
no3_ma_t = np.array((no3_ma_o,no3_ma_h,no3_ma_j,no3_ma_p))
no2_ma_t = np.array((no2_ma_o,no2_ma_h,no2_ma_j,no2_ma_p))

# flux per year each outfall
nh4_flux_ma = flow_ma_t*nh4_ma_t * conv
no3_flux_ma = flow_ma_t*no3_ma_t * conv
no2_flux_ma = flow_ma_t*no2_ma_t * conv
TN_flux_ma  = nh4_flux_ma + no3_flux_ma + no2_flux_ma * conv


###########
# minor potw data
###########
# santa barbara minor potw between these longitudes
lon0_sb = -119.51
lon1_sb = -120
lon_mi = np.array(minor_nc.variables['longitude'][:])
ind_mi = np.where((lon_mi>lon1_sb)&(lon_mi<lon0_sb))[0]

flow_mi = minor_nc.variables['flow'][:12,ind_mi,ind_mi]
nh4_mi = minor_nc.variables['NH4'][:12,ind_mi,ind_mi]
no3_mi = minor_nc.variables['NO3'][:12,ind_mi,ind_mi]
no2_mi = minor_nc.variables['NO2'][:12,ind_mi,ind_mi]

flux_mi_nh4 = np.nansum(flow_mi*nh4_mi)
flux_mi_no3 = np.nansum(flow_mi*no3_mi)
flux_mi_no2 = np.nansum(flow_mi*no2_mi)

flux_mi_TN = flux_mi_nh4+flux_mi_no3+flux_mi_no2

print('Santa Barbara POTW flux average per year mmol/s')
print('NH4 flux:    ',flux_mi_nh4)
print('NO3 flux:    ',flux_mi_no3)
print('TN flux:     ',flux_mi_TN)

###############################################################
# plot one major N flux and sum of all minor N flux
###############################################################
subplot_title_font = 16
fig_w = 12
fig_h = 14
tick_label_size = 14
color_line = 'navy'
lw = 3
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']

plt.ion()
# plot major potw NH4 and TN flux sum of all 
fig = plt.figure(figsize=[14,9])
#plot just OCSD index 0
plt.plot(time_ma[t_st:t_en],nh4_flux_ma[0],linewidth=lw,color='navy')
plt.ylabel('NH4 Mg day$^{-1}$',fontsize=subplot_title_font)
#plt.ylim([0,max(flux_ma_NH4_yrs)+100])
#plt.yticks(np.arange(0,max(flux_ma_NH4_yrs)+10,100))
plt.xticks(rotation=45)
#fig.autofmt_xdate()
ax = plt.gca()
ax.grid(True)
ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
locator = mdate.YearLocator(2)
ax.xaxis.set_major_locator(locator)
#ax.axes.xaxis.set_ticklabels(months)
plt.savefig('ocsd_NH4_flux.png',bbox_inches='tight')

fig = plt.figure(figsize=[14,9])
#plot just OCSD index 0
plt.plot(time_ma[t_st:t_en],TN_flux_ma[0],linewidth=lw,color='navy',label='All Rivers')
plt.ylabel('Total N Mg day$^{-1}$',fontsize=subplot_title_font)
#plt.ylim([0,max(flux_ma_TN_yrs)+10])
#plt.yticks(np.arange(0,max(flux_ma_TN_yrs)+10,100))
plt.xticks(rotation=45)
ax = plt.gca()
ax.grid(True)
ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
locator = mdate.YearLocator(2)
ax.xaxis.set_major_locator(locator)
#ax.axes.xaxis.set_ticklabels(months)
plt.savefig('ocsd_TN_flux.png',bbox_inches='tight')

