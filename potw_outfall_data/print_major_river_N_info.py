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


# time indexes start and end for major pipes 1997-2000 only
t_st = 313
t_en = 361

years = 4

# conversions
sec2day = 86400
mol_wt_N = 14
mg_to_kg = 1./1e6
kg_to_Mg = 1/1e3

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
# divide by number of years
nh4_flux_ma_yr = np.nansum(flow_ma_t*nh4_ma_t,axis=1)/4
no3_flux_ma_yr = np.nansum(flow_ma_t*no3_ma_t,axis=1)/4
no2_flux_ma_yr = np.nansum(flow_ma_t*no2_ma_t,axis=1)/4


###########
# all major potw
###########

# flux N average per year
# Mg/day
#flux_ma_NH4 = sum_flow_ma * sum_nh4_ma * sec2day*mol_wt_N*mg_to_kg*kg_to_Mg
#flux_ma_NH4 = flow_ma_all * nh4_ma_all * sec2day*mol_wt_N*mg_to_kg*kg_to_Mg
# mmol/s
nh4_flux_ma_all_yr = np.nansum(nh4_flux_ma_yr) 
no3_flux_ma_all_yr = np.nansum(no3_flux_ma_yr) 
no2_flux_ma_all_yr = np.nansum(no2_flux_ma_yr) 

# total N flux
TN_flux_ma_yr  = nh4_flux_ma_yr+no3_flux_ma_yr+no2_flux_ma_yr

TN_flux_ma_all_yr = nh4_flux_ma_all_yr+no3_flux_ma_all_yr+no2_flux_ma_all_yr

print('average yearly calculated between 1997-2000')
print('average yearly nh4 flux mmol/s')
print('OCSD:     ',nh4_flux_ma_yr[0])
print('Hyperion: ',nh4_flux_ma_yr[1])
print('JWPCP:    ',nh4_flux_ma_yr[2])
print('PLWTP:    ',nh4_flux_ma_yr[3])
print('Total:    ',nh4_flux_ma_all_yr)

print('\naverage monthly nh4 flux mmol/s')
print('OCSD:     ',nh4_flux_ma_yr[0]/12)
print('Hyperion: ',nh4_flux_ma_yr[1]/12)
print('JWPCP:    ',nh4_flux_ma_yr[2]/12)
print('PLWTP:    ',nh4_flux_ma_yr[3]/12)
print('Total:    ',nh4_flux_ma_all_yr/12)

print('\naverage yearly no3 flux mmol/s')
print('OCSD:     ',no3_flux_ma_yr[0])
print('Hyperion: ',no3_flux_ma_yr[1])
print('JWPCP:    ',no3_flux_ma_yr[2])
print('PLWTP:    ',no3_flux_ma_yr[3])
print('Total:    ',no3_flux_ma_all_yr)

print('\naverage monthly no3 flux mmol/s')
print('OCSD:     ',no3_flux_ma_yr[0]/12)
print('Hyperion: ',no3_flux_ma_yr[1]/12)
print('JWPCP:    ',no3_flux_ma_yr[2]/12)
print('PLWTP:    ',no3_flux_ma_yr[3]/12)
print('Total:    ',no3_flux_ma_all_yr/12)

print('average yearly TN flux mmol/s')
print('OCSD:     ',TN_flux_ma_yr[0])
print('Hyperion: ',TN_flux_ma_yr[1])
print('JWPCP:    ',TN_flux_ma_yr[2])
print('PLWTP:    ',TN_flux_ma_yr[3])
print('Total:    ',TN_flux_ma_all_yr)

print('average monthly TN flux mmol/s')
print('OCSD:     ',TN_flux_ma_yr[0]/12)
print('Hyperion: ',TN_flux_ma_yr[1]/12)
print('JWPCP:    ',TN_flux_ma_yr[2]/12)
print('PLWTP:    ',TN_flux_ma_yr[3]/12)
print('Total:    ',TN_flux_ma_all_yr/12)

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

###########
# river data
###########
#st = 0
#en = 340
st = 0
en = 48 # 1997 - 2000 4 years in months
t24 = 84 # start at t index 84 for 1997
# find rivers between these longitudes
lat_10 = np.array(nc_10.variables['latitude'][0,:])
lat_24 = np.array(nc_24.variables['latitude'][0,:])
lon_10 = np.array(nc_10.variables['longitude'][0,:])
lon_24 = np.array(nc_24.variables['longitude'][0,:])
# santa barbara
ind_sb_10 =np.where((lon_10>lon1_sb)&(lon_10<lon0_sb))[0]
ind_sb_24 =np.where((lon_24>lon1_sb)&(lon_24<lon0_sb))[0]

flow_sb_10 = np.array(nc_10.variables['flow'][st:en,ind_sb_10,ind_sb_10])
flow_sb_24 = np.array(nc_24.variables['flow'][t24+st:t24+en,ind_sb_24,ind_sb_24])
NH4_sb_10 = np.array(nc_10.variables['ammonium'][st:en,ind_sb_10,ind_sb_10])
NH4_sb_24 = np.array(nc_24.variables['ammonium'][t24+st:t24+en,ind_sb_24,ind_sb_24])
NO3_sb_10 = np.array(nc_10.variables['nitrate'][st:en,ind_sb_10,ind_sb_10])
NO3_sb_24 = np.array(nc_24.variables['nitrate'][t24+st:t24+en,ind_sb_24,ind_sb_24])
TN_sb_10 = np.array(nc_10.variables['total_nitrogen'][st:en,ind_sb_10,ind_sb_10])
TN_sb_24 = np.array(nc_24.variables['total_nitrogen'][t24+st:t24+en,ind_sb_24,ind_sb_24])

flow_sb_10[flow_sb_10>1E10] = np.nan
flow_sb_24[flow_sb_24>1E10] = np.nan
NH4_sb_10[NH4_sb_10>1E10] = np.nan
NH4_sb_24[NH4_sb_24>1E10] = np.nan
NO3_sb_10[NO3_sb_10>1E10] = np.nan
NO3_sb_24[NO3_sb_24>1E10] = np.nan
TN_sb_10[TN_sb_10>1E10] = np.nan
TN_sb_24[TN_sb_24>1E10] = np.nan

# find sum of river data
flux_sb_r_nh4 = np.nansum(flow_sb_10*NH4_sb_10)+np.nansum(flow_sb_24*NH4_sb_24)
flux_sb_r_no3 = np.nansum(flow_sb_10*NO3_sb_10)+np.nansum(flow_sb_24*NO3_sb_24)
flux_sb_r_TN = np.nansum(flow_sb_10*TN_sb_10)+np.nansum(flow_sb_24*TN_sb_24)

# santa monica
lon0_sm = -118.36
lon1_sm = -118.81
ind_sm_10 =np.where((lon_10>lon1_sm)&(lon_10<lon0_sm))[0]
ind_sm_24 =np.where((lon_24>lon1_sm)&(lon_24<lon0_sm))[0]

flow_sm_10 = np.array(nc_10.variables['flow'][st:en,ind_sm_10,ind_sm_10])
flow_sm_24 = np.array(nc_24.variables['flow'][t24+st:t24+en,ind_sm_24,ind_sm_24])
NH4_sm_10 = np.array(nc_10.variables['ammonium'][st:en,ind_sm_10,ind_sm_10])
NH4_sm_24 = np.array(nc_24.variables['ammonium'][t24+st:t24+en,ind_sm_24,ind_sm_24])
NO3_sm_10 = np.array(nc_10.variables['nitrate'][st:en,ind_sm_10,ind_sm_10])
NO3_sm_24 = np.array(nc_24.variables['nitrate'][t24+st:t24+en,ind_sm_24,ind_sm_24])
TN_sm_10 = np.array(nc_10.variables['total_nitrogen'][st:en,ind_sm_10,ind_sm_10])
TN_sm_24 = np.array(nc_24.variables['total_nitrogen'][t24+st:t24+en,ind_sm_24,ind_sm_24])

flow_sm_10[flow_sm_10>1E10] = np.nan
flow_sm_24[flow_sm_24>1E10] = np.nan
NH4_sm_10[NH4_sm_10>1E10] = np.nan
NH4_sm_24[NH4_sm_24>1E10] = np.nan
NO3_sm_10[NO3_sm_10>1E10] = np.nan
NO3_sm_24[NO3_sm_24>1E10] = np.nan
TN_sm_10[TN_sm_10>1E10] = np.nan
TN_sm_24[TN_sm_24>1E10] = np.nan

# find sum of river data
flux_sm_r_nh4 = np.nansum(flow_sm_10*NH4_sm_10)+np.nansum(flow_sm_24*NH4_sm_24)
flux_sm_r_no3 = np.nansum(flow_sm_10*NO3_sm_10)+np.nansum(flow_sm_24*NO3_sm_24)
flux_sm_r_TN = np.nansum(flow_sm_10*TN_sm_10)+np.nansum(flow_sm_24*TN_sm_24)

# san pedro
lon0_sp = -118.1
lon1_sp = -118.36
ind_sp_10 =np.where((lon_10>lon1_sp)&(lon_10<lon0_sp))[0]
ind_sp_24 =np.where((lon_24>lon1_sp)&(lon_24<lon0_sp))[0]

flow_sp_10 = np.array(nc_10.variables['flow'][st:en,ind_sp_10,ind_sp_10])
flow_sp_24 = np.array(nc_24.variables['flow'][t24+st:t24+en,ind_sp_24,ind_sp_24])
NH4_sp_10 = np.array(nc_10.variables['ammonium'][st:en,ind_sp_10,ind_sp_10])
NH4_sp_24 = np.array(nc_24.variables['ammonium'][t24+st:t24+en,ind_sp_24,ind_sp_24])
NO3_sp_10 = np.array(nc_10.variables['nitrate'][st:en,ind_sp_10,ind_sp_10])
NO3_sp_24 = np.array(nc_24.variables['nitrate'][t24+st:t24+en,ind_sp_24,ind_sp_24])
TN_sp_10 = np.array(nc_10.variables['total_nitrogen'][st:en,ind_sp_10,ind_sp_10])
TN_sp_24 = np.array(nc_24.variables['total_nitrogen'][t24+st:t24+en,ind_sp_24,ind_sp_24])

flow_sp_10[flow_sp_10>1E10] = np.nan
flow_sp_24[flow_sp_24>1E10] = np.nan
NH4_sp_10[NH4_sp_10>1E10] = np.nan
NH4_sp_24[NH4_sp_24>1E10] = np.nan
NO3_sp_10[NO3_sp_10>1E10] = np.nan
NO3_sp_24[NO3_sp_24>1E10] = np.nan
TN_sp_10[TN_sp_10>1E10] = np.nan
TN_sp_24[TN_sp_24>1E10] = np.nan

# find sum of river data
flux_sp_r_nh4 = np.nansum(flow_sp_10*NH4_sp_10)+np.nansum(flow_sp_24*NH4_sp_24)
flux_sp_r_no3 = np.nansum(flow_sp_10*NO3_sp_10)+np.nansum(flow_sp_24*NO3_sp_24)
flux_sp_r_TN = np.nansum(flow_sp_10*TN_sp_10)+np.nansum(flow_sp_24*TN_sp_24)

print('Santa Barbara river flux average per year: ')
print('NH4 flux:    ',flux_sb_r_nh4)
print('NO3 flux:    ',flux_sb_r_no3)
print('TN flux:     ',flux_sb_r_TN)

print('Santa Monica river flux average per year: ')
print('NH4 flux:    ',flux_sm_r_nh4)
print('NO3 flux:    ',flux_sm_r_no3)
print('TN flux:     ',flux_sm_r_TN)

print('San Pedro river flux average per year: ')
print('NH4 flux:    ',flux_sp_r_nh4)
print('NO3 flux:    ',flux_sp_r_no3)
print('TN flux:     ',flux_sp_r_TN)
'''
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

# plot major potw NH4 and TN flux sum of all 
fig = plt.figure(figsize=[14,9])
plt.plot(time_ma[:505],flux_ma_NH4_yrs,linewidth=lw,color='navy',label='All Major POTW')
plt.ylabel('NH4 Mg day$^{-1}$',fontsize=subplot_title_font)
plt.ylim([0,max(flux_ma_NH4_yrs)+100])
plt.yticks(np.arange(0,max(flux_ma_NH4_yrs)+10,100))
plt.xticks(rotation=45)
#fig.autofmt_xdate()
ax = plt.gca()
ax.grid(True)
ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
locator = mdate.YearLocator(2)
ax.xaxis.set_major_locator(locator)
#ax.axes.xaxis.set_ticklabels(months)
plt.savefig('all_major_potw_NH4.png',bbox_inches='tight')

fig = plt.figure(figsize=[14,9])
plt.plot(time_ma[:505],flux_ma_TN_yrs,linewidth=lw,color='navy',label='All Rivers')
plt.ylabel('Total N Mg day$^{-1}$',fontsize=subplot_title_font)
plt.ylim([0,max(flux_ma_TN_yrs)+10])
plt.yticks(np.arange(0,max(flux_ma_TN_yrs)+10,100))
plt.xticks(rotation=45)
ax = plt.gca()
ax.grid(True)
ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
locator = mdate.YearLocator(2)
ax.xaxis.set_major_locator(locator)
#ax.axes.xaxis.set_ticklabels(months)
plt.savefig('all_major_potw_TN.png',bbox_inches='tight')
'''
