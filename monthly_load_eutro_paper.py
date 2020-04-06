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


# sb = coastal region
lat0_sb = 33.45
lat1_sb = 34.27

# sm = santa monica
lat0_sm = 33.77
lat1_sm = 34.48

# sp = san pedro
lat0_sp = 33.45
lat1_sp = 33.78

# rb = santa barbara (real one)
lat0_rb = 34.05
lat1_rb = 34.3

#grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
#grid_nc = Dataset(grid_path,'r')
#lat_nc = np.array(grid_nc.variables['lat_rho'])
#lon_nc = np.array(grid_nc.variables['lat_rho'])
#mask_nc = np.array(grid_nc.variables['mask_rho'])

###############################
# load major potw, minor potw, rivers netcdf
##############################
#potw
major_nc = Dataset('./potw_outfall_data/major_potw_data.nc','r')
minor_nc = Dataset('./potw_outfall_data/minor_potw_data.nc','r')
# river
#nc_10 = Dataset('../river_data/south_coast_rivers_10_years_no_watershed_new.nc','r')
#nc_24 = Dataset('../river_data/south_coast_rivers_24_years_new.nc','r')
nc_10 = Dataset('./river_data/south_coast_rivers_10_years_monthly_new.nc','r')
nc_24 = Dataset('./river_data/south_coast_rivers_24_years_monthly_new.nc','r')

## atmos dep
#atmos_path = Dataset('/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc')
#atmos_nc = Dataset(atmos_path,'r')
#atmos_nh4 = atmos_nc.variables['NH4']
#atmos_no3 = atmos_nc.variables['NO3']

# times
time_ma = num2date(major_nc.variables['time'][:],major_nc.variables['time'].units)
time_mi = num2date(minor_nc.variables['time'][:],minor_nc.variables['time'].units)
time_10 = nc_10.variables['time']
time_24 = nc_24.variables['time']
date_10 = num2date(np.asarray(time_10),time_10.units)
date_24 = num2date(np.asarray(time_24),time_24.units)


# time indexes start and end for major pipes 1997-2000 only
t_st = 314 # 2 1997
t_en = 349 # 1 2000

# conversions
sec2day = 86400
mol_wt_N = 14
mg_to_kg = 1./1e6
kg_to_Mg = 1/1e3
# seconds in a month
#s_to_m = 2628000
s_to_m = 1

########################
# major potw individual
########################
lon_ma = np.array(major_nc.variables['longitude'][:])
lat_ma = np.array(major_nc.variables['latitude'][:])

ind_ma_sb = np.where((lat_ma>lat0_sb)&(lat_ma<lat1_sb))[0]
ind_ma_sm = np.where((lat_ma>lat0_sm)&(lat_ma<lat1_sm))[0]
ind_ma_sp = np.where((lat_ma>lat0_sp)&(lat_ma<lat1_sp))[0]
ind_ma_rb = np.where((lat_ma>lat0_rb)&(lat_ma<lat1_rb))[0]

flow_ma = major_nc.variables['flow'][t_st:t_en,:,:]
nh4_ma  = major_nc.variables['NH4'][t_st:t_en,:,:]
no3_ma  = major_nc.variables['NO3'][t_st:t_en,:,:]
no2_ma  = major_nc.variables['NO2'][t_st:t_en,:,:]
on_ma  = major_nc.variables['ON'][t_st:t_en,:,:]

flux_ma_nh4_all = np.nanmean(np.nansum(np.nansum(flow_ma*nh4_ma,axis=1),axis=1))*s_to_m
flux_ma_no3_all = np.nanmean(np.nansum(np.nansum(flow_ma*no3_ma,axis=1),axis=1))*s_to_m
flux_ma_no2_all = np.nanmean(np.nansum(np.nansum(flow_ma*no2_ma,axis=1),axis=1))*s_to_m
flux_ma_on_all  = np.nanmean(np.nansum(np.nansum(flow_ma*on_ma,axis=1),axis=1))*s_to_m

flux_ma_nh4_sb = np.nanmean(np.nansum(flow_ma[:,ind_ma_sb,ind_ma_sb]*nh4_ma[:,ind_ma_sb,ind_ma_sb],axis=1))*s_to_m
flux_ma_no3_sb = np.nanmean(np.nansum(flow_ma[:,ind_ma_sb,ind_ma_sb]*no3_ma[:,ind_ma_sb,ind_ma_sb],axis=1))*s_to_m
flux_ma_no2_sb = np.nanmean(np.nansum(flow_ma[:,ind_ma_sb,ind_ma_sb]*no2_ma[:,ind_ma_sb,ind_ma_sb],axis=1))*s_to_m
flux_ma_on_sb = np.nanmean(np.nansum(flow_ma[:,ind_ma_sb,ind_ma_sb]*on_ma[:,ind_ma_sb,ind_ma_sb],axis=1))*s_to_m

flux_ma_nh4_sm = np.nanmean(np.nansum(flow_ma[:,ind_ma_sm,ind_ma_sm]*nh4_ma[:,ind_ma_sm,ind_ma_sm],axis=1))*s_to_m
flux_ma_no3_sm = np.nanmean(np.nansum(flow_ma[:,ind_ma_sm,ind_ma_sm]*no3_ma[:,ind_ma_sm,ind_ma_sm],axis=1))*s_to_m
flux_ma_no2_sm = np.nanmean(np.nansum(flow_ma[:,ind_ma_sm,ind_ma_sm]*no2_ma[:,ind_ma_sm,ind_ma_sm],axis=1))*s_to_m
flux_ma_on_sm = np.nanmean(np.nansum(flow_ma[:,ind_ma_sm,ind_ma_sm]*on_ma[:,ind_ma_sm,ind_ma_sm],axis=1))*s_to_m

flux_ma_nh4_sp = np.nanmean(np.nansum(flow_ma[:,ind_ma_sp,ind_ma_sp]*nh4_ma[:,ind_ma_sp,ind_ma_sp],axis=1))*s_to_m
flux_ma_no3_sp = np.nanmean(np.nansum(flow_ma[:,ind_ma_sp,ind_ma_sp]*no3_ma[:,ind_ma_sp,ind_ma_sp],axis=1))*s_to_m
flux_ma_no2_sp = np.nanmean(np.nansum(flow_ma[:,ind_ma_sp,ind_ma_sp]*no2_ma[:,ind_ma_sp,ind_ma_sp],axis=1))*s_to_m
flux_ma_on_sp = np.nanmean(np.nansum(flow_ma[:,ind_ma_sp,ind_ma_sp]*on_ma[:,ind_ma_sp,ind_ma_sp],axis=1))*s_to_m

#flux_ma_nh4_rb = np.nanmean(np.nansum(flow_ma[:,ind_ma_rb,ind_ma_rb]*nh4_ma[:,ind_ma_rb,ind_ma_rb],axis=1))*s_to_m
#flux_ma_no3_rb = np.nanmean(np.nansum(flow_ma[:,ind_ma_rb,ind_ma_rb]*no3_ma[:,ind_ma_rb,ind_ma_rb],axis=1))*s_to_m
#flux_ma_no2_rb = np.nanmean(np.nansum(flow_ma[:,ind_ma_rb,ind_ma_rb]*no2_ma[:,ind_ma_rb,ind_ma_rb],axis=1))*s_to_m
#flux_ma_on_rb = np.nanmean(np.nansum(flow_ma[:,ind_ma_rb,ind_ma_rb]*on_ma[:,ind_ma_rb,ind_ma_rb],axis=1))*s_to_m
flux_ma_nh4_rb = 0
flux_ma_no3_rb =0
flux_ma_no2_rb =0
flux_ma_on_rb = 0



###########
# minor potw data
###########
lon_mi = np.array(minor_nc.variables['longitude'][:])
lat_mi = np.array(minor_nc.variables['latitude'][:])
ind_mi_sb = np.where((lat_mi>lat0_sb)&(lat_mi<lat1_sb))[0]
ind_mi_sm = np.where((lat_mi>lat0_sm)&(lat_mi<lat1_sm))[0]
ind_mi_sp = np.where((lat_mi>lat0_sp)&(lat_mi<lat1_sp))[0]
ind_mi_rb = np.where((lat_mi>lat0_rb)&(lat_mi<lat1_rb))[0]

flow_mi = minor_nc.variables['flow'][:12,:,:]
nh4_mi  = minor_nc.variables['NH4'][:12,:,:]
no3_mi  = minor_nc.variables['NO3'][:12,:,:]
no2_mi  = minor_nc.variables['NO2'][:12,:,:]

flux_mi_nh4_all = np.nanmean(np.nansum(np.nansum(flow_mi*nh4_mi,axis=1),axis=1))*s_to_m
flux_mi_no3_all = np.nanmean(np.nansum(np.nansum(flow_mi*no3_mi,axis=1),axis=1))*s_to_m
flux_mi_no2_all = np.nanmean(np.nansum(np.nansum(flow_mi*no2_mi,axis=1),axis=1))*s_to_m


flux_mi_nh4_sb = np.nanmean(np.nansum(flow_mi[:,ind_mi_sb,ind_mi_sb]*nh4_mi[:,ind_mi_sb,ind_mi_sb],axis=1))*s_to_m
flux_mi_no3_sb = np.nanmean(np.nansum(flow_mi[:,ind_mi_sb,ind_mi_sb]*no3_mi[:,ind_mi_sb,ind_mi_sb],axis=1))*s_to_m
flux_mi_no2_sb = np.nanmean(np.nansum(flow_mi[:,ind_mi_sb,ind_mi_sb]*no2_mi[:,ind_mi_sb,ind_mi_sb],axis=1))*s_to_m

flux_mi_nh4_sm = np.nanmean(np.nansum(flow_mi[:,ind_mi_sm,ind_mi_sm]*nh4_mi[:,ind_mi_sm,ind_mi_sm],axis=1))*s_to_m
flux_mi_no3_sm = np.nanmean(np.nansum(flow_mi[:,ind_mi_sm,ind_mi_sm]*no3_mi[:,ind_mi_sm,ind_mi_sm],axis=1))*s_to_m
flux_mi_no2_sm = np.nanmean(np.nansum(flow_mi[:,ind_mi_sm,ind_mi_sm]*no2_mi[:,ind_mi_sm,ind_mi_sm],axis=1))*s_to_m

flux_mi_nh4_sp = np.nanmean(np.nansum(flow_mi[:,ind_mi_sp,ind_mi_sp]*nh4_mi[:,ind_mi_sp,ind_mi_sp],axis=1))*s_to_m
flux_mi_no3_sp = np.nanmean(np.nansum(flow_mi[:,ind_mi_sp,ind_mi_sp]*no3_mi[:,ind_mi_sp,ind_mi_sp],axis=1))*s_to_m
flux_mi_no2_sp = np.nanmean(np.nansum(flow_mi[:,ind_mi_sp,ind_mi_sp]*no2_mi[:,ind_mi_sp,ind_mi_sp],axis=1))*s_to_m

flux_mi_nh4_rb = np.nanmean(np.nansum(flow_mi[:,ind_mi_rb,ind_mi_rb]*nh4_mi[:,ind_mi_rb,ind_mi_rb],axis=1))*s_to_m
flux_mi_no3_rb = np.nanmean(np.nansum(flow_mi[:,ind_mi_rb,ind_mi_rb]*no3_mi[:,ind_mi_rb,ind_mi_rb],axis=1))*s_to_m
flux_mi_no2_rb = np.nanmean(np.nansum(flow_mi[:,ind_mi_rb,ind_mi_rb]*no2_mi[:,ind_mi_rb,ind_mi_rb],axis=1))*s_to_m

###########
# river data
###########
#st = 0
#en = 340
st = 1
en = 36 # 1997 - 1999
t24 = 84 # start at t index 84 for 1997
# find rivers between these longitudes
lat_10 = np.array(nc_10.variables['latitude'][0,:])
lat_24 = np.array(nc_24.variables['latitude'][0,:])
lon_10 = np.array(nc_10.variables['longitude'][0,:])
lon_24 = np.array(nc_24.variables['longitude'][0,:])

ind_10_sb = np.where((lat_10>lat0_sb)&(lat_10<lat1_sb))[0]
ind_10_sm = np.where((lat_10>lat0_sm)&(lat_10<lat1_sm))[0]
ind_10_sp = np.where((lat_10>lat0_sp)&(lat_10<lat1_sp))[0]
ind_10_rb = np.where((lat_10>lat0_rb)&(lat_10<lat1_rb))[0]

ind_24_sb = np.where((lat_24>lat0_sb)&(lat_24<lat1_sb))[0]
ind_24_sm = np.where((lat_24>lat0_sm)&(lat_24<lat1_sm))[0]
ind_24_sp = np.where((lat_24>lat0_sp)&(lat_24<lat1_sp))[0]
ind_24_rb = np.where((lat_24>lat0_rb)&(lat_24<lat1_rb))[0]

flow_10 = nc_10.variables['flow'][st:en,:,:]
nh4_10  = nc_10.variables['ammonium'][st:en,:,:]
no3_10  = nc_10.variables['nitrate'][st:en,:,:]
tn_10   = nc_10.variables['total_nitrogen'][st:en,:,:]

flow_24 = nc_24.variables['flow'][st+t24:en+t24,:,:]
nh4_24  = nc_24.variables['ammonium'][st+t24:en+t24,:,:]
no3_24  = nc_24.variables['nitrate'][st+t24:en+t24,:,:]
tn_24   = nc_24.variables['total_nitrogen'][st+t24:en+t24,:,:]

flow_10[flow_10>1E10] = np.nan
flow_24[flow_24>1E10] = np.nan
nh4_10[nh4_10>1E10] = np.nan
nh4_24[nh4_24>1E10] = np.nan
no3_10[no3_10>1E10] = np.nan
no3_24[no3_24>1E10] = np.nan
tn_10[tn_10>1E10] = np.nan
tn_24[tn_24>1E10] = np.nan


flux_10_nh4_all = np.nanmean(np.nansum(np.nansum(flow_10*nh4_10,axis=1),axis=1))*s_to_m
flux_10_no3_all = np.nanmean(np.nansum(np.nansum(flow_10*no3_10,axis=1),axis=1))*s_to_m
flux_10_tn_all  = np.nanmean(np.nansum(np.nansum(flow_10*tn_10,axis=1),axis=1))*s_to_m

flux_10_nh4_sb = np.nanmean(np.nansum(flow_10[:,ind_10_sb,ind_10_sb]*nh4_10[:,ind_10_sb,ind_10_sb],axis=1))*s_to_m
flux_10_no3_sb = np.nanmean(np.nansum(flow_10[:,ind_10_sb,ind_10_sb]*no3_10[:,ind_10_sb,ind_10_sb],axis=1))*s_to_m
flux_10_tn_sb = np.nanmean(np.nansum(flow_10[:,ind_10_sb,ind_10_sb]*tn_10[:,ind_10_sb,ind_10_sb],axis=1))*s_to_m

flux_10_nh4_sm = np.nanmean(np.nansum(flow_10[:,ind_10_sm,ind_10_sm]*nh4_10[:,ind_10_sm,ind_10_sm],axis=1))*s_to_m
flux_10_no3_sm = np.nanmean(np.nansum(flow_10[:,ind_10_sm,ind_10_sm]*no3_10[:,ind_10_sm,ind_10_sm],axis=1))*s_to_m
flux_10_tn_sm = np.nanmean(np.nansum(flow_10[:,ind_10_sm,ind_10_sm]*tn_10[:,ind_10_sm,ind_10_sm],axis=1))*s_to_m

flux_10_nh4_sp = np.nanmean(np.nansum(flow_10[:,ind_10_sp,ind_10_sp]*nh4_10[:,ind_10_sp,ind_10_sp],axis=1))*s_to_m
flux_10_no3_sp = np.nanmean(np.nansum(flow_10[:,ind_10_sp,ind_10_sp]*no3_10[:,ind_10_sp,ind_10_sp],axis=1))*s_to_m
flux_10_tn_sp = np.nanmean(np.nansum(flow_10[:,ind_10_sp,ind_10_sp]*tn_10[:,ind_10_sp,ind_10_sp],axis=1))*s_to_m

flux_10_nh4_rb = np.nanmean(np.nansum(flow_10[:,ind_10_rb,ind_10_rb]*nh4_10[:,ind_10_rb,ind_10_rb],axis=1))*s_to_m
flux_10_no3_rb = np.nanmean(np.nansum(flow_10[:,ind_10_rb,ind_10_rb]*no3_10[:,ind_10_rb,ind_10_rb],axis=1))*s_to_m
flux_10_tn_rb = np.nanmean(np.nansum(flow_10[:,ind_10_rb,ind_10_rb]*tn_10[:,ind_10_rb,ind_10_rb],axis=1))*s_to_m

flux_24_nh4_all = np.nanmean(np.nansum(np.nansum(flow_24*nh4_24,axis=1),axis=1))*s_to_m
flux_24_no3_all = np.nanmean(np.nansum(np.nansum(flow_24*no3_24,axis=1),axis=1))*s_to_m
flux_24_tn_all  = np.nanmean(np.nansum(np.nansum(flow_24*tn_24,axis=1),axis=1))*s_to_m

flux_24_nh4_sb = np.nanmean(np.nansum(flow_24[:,ind_24_sb,ind_24_sb]*nh4_24[:,ind_24_sb,ind_24_sb],axis=1))*s_to_m
flux_24_no3_sb = np.nanmean(np.nansum(flow_24[:,ind_24_sb,ind_24_sb]*no3_24[:,ind_24_sb,ind_24_sb],axis=1))*s_to_m
flux_24_tn_sb = np.nanmean(np.nansum(flow_24[:,ind_24_sb,ind_24_sb]*tn_24[:,ind_24_sb,ind_24_sb],axis=1))*s_to_m

flux_24_nh4_sm = np.nanmean(np.nansum(flow_24[:,ind_24_sm,ind_24_sm]*nh4_24[:,ind_24_sm,ind_24_sm],axis=1))*s_to_m
flux_24_no3_sm = np.nanmean(np.nansum(flow_24[:,ind_24_sm,ind_24_sm]*no3_24[:,ind_24_sm,ind_24_sm],axis=1))*s_to_m
flux_24_tn_sm = np.nanmean(np.nansum(flow_24[:,ind_24_sm,ind_24_sm]*tn_24[:,ind_24_sm,ind_24_sm],axis=1))*s_to_m

flux_24_nh4_sp = np.nanmean(np.nansum(flow_24[:,ind_24_sp,ind_24_sp]*nh4_24[:,ind_24_sp,ind_24_sp],axis=1))*s_to_m
flux_24_no3_sp = np.nanmean(np.nansum(flow_24[:,ind_24_sp,ind_24_sp]*no3_24[:,ind_24_sp,ind_24_sp],axis=1))*s_to_m
flux_24_tn_sp = np.nanmean(np.nansum(flow_24[:,ind_24_sp,ind_24_sp]*tn_24[:,ind_24_sp,ind_24_sp],axis=1))*s_to_m

flux_24_nh4_rb = np.nanmean(np.nansum(flow_24[:,ind_24_rb,ind_24_rb]*nh4_24[:,ind_24_rb,ind_24_rb],axis=1))*s_to_m
flux_24_no3_rb = np.nanmean(np.nansum(flow_24[:,ind_24_rb,ind_24_rb]*no3_24[:,ind_24_rb,ind_24_rb],axis=1))*s_to_m
flux_24_tn_rb = np.nanmean(np.nansum(flow_24[:,ind_24_rb,ind_24_rb]*tn_24[:,ind_24_rb,ind_24_rb],axis=1))*s_to_m

flux_r_nh4_all = flux_24_nh4_all+flux_10_nh4_all
flux_r_no3_all = flux_24_no3_all+flux_10_no3_all
flux_r_tn_all = flux_24_tn_all+flux_10_tn_all
flux_r_on_all = flux_r_tn_all-(flux_r_nh4_all+flux_r_no3_all)

flux_r_nh4_sb = flux_24_nh4_sb+flux_10_nh4_sb
flux_r_no3_sb = flux_24_no3_sb+flux_10_no3_sb
flux_r_tn_sb = flux_24_tn_sb+flux_10_tn_sb
flux_r_on_sb = flux_r_tn_sb-(flux_r_nh4_sb+flux_r_no3_sb)

flux_r_nh4_sm = flux_24_nh4_sb+flux_10_nh4_sm
flux_r_no3_sm = flux_24_no3_sb+flux_10_no3_sm
flux_r_tn_sm = flux_24_tn_sb+flux_10_tn_sm
flux_r_on_sm = flux_r_tn_sm-(flux_r_nh4_sm+flux_r_no3_sm)

flux_r_nh4_sp = flux_24_nh4_sb+flux_10_nh4_sp
flux_r_no3_sp = flux_24_no3_sb+flux_10_no3_sp
flux_r_tn_sp = flux_24_tn_sb+flux_10_tn_sp
flux_r_on_sp = flux_r_tn_sp-(flux_r_nh4_sp+flux_r_no3_sp)

flux_r_nh4_rb = flux_24_nh4_sb+flux_10_nh4_rb
flux_r_no3_rb = flux_24_no3_sb+flux_10_no3_rb
flux_r_tn_rb = flux_24_tn_sb+flux_10_tn_rb
flux_r_on_rb = flux_r_tn_rb-(flux_r_nh4_rb+flux_r_no3_rb)

flux_o_nh4_all = flux_ma_nh4_all+flux_ma_nh4_all
flux_o_no3_all = flux_ma_no3_all+flux_ma_no3_all
flux_o_on_all = flux_ma_on_all

flux_o_nh4_sb = flux_ma_nh4_sb+flux_mi_nh4_sb
flux_o_no3_sb = flux_ma_no3_sb+flux_mi_no3_sb
flux_o_on_sb = flux_ma_on_sb

flux_o_nh4_sm = flux_ma_nh4_sm+flux_mi_nh4_sm
flux_o_no3_sm = flux_ma_no3_sm+flux_mi_no3_sm
flux_o_on_sm = flux_ma_on_sm

flux_o_nh4_sp = flux_ma_nh4_sp+flux_mi_nh4_sp
flux_o_no3_sp = flux_ma_no3_sp+flux_mi_no3_sp
flux_o_on_sp = flux_ma_on_sp

flux_o_nh4_rb = flux_ma_nh4_rb+flux_mi_nh4_rb
flux_o_no3_rb = flux_ma_no3_rb+flux_mi_no3_rb
flux_o_on_rb = flux_ma_on_rb

# print values
num_dec = 4
print('coast river nh4 flux (mmol/month): ','%.2E'%flux_r_nh4_sb)
print('coast river no3 flux (mmol/month): ','%.2E'%flux_r_no3_sb)
print('coast river on flux (mmol/month): ','%.2E'%flux_r_on_sb)

print('coast outfall nh4 flux (mmol/month): ','%.2E'%flux_o_nh4_sb)
print('coast outfall no3 flux (mmol/month): ','%.2E'%flux_o_no3_sb)
print('coast outfall on flux (mmol/month): ','%.2E'%flux_o_on_sb)

print('sm river nh4 flux (mmol/month): ','%.2E'%flux_r_nh4_sm)
print('sm river no3 flux (mmol/month): ','%.2E'%flux_r_no3_sm)
print('sm river on flux (mmol/month): ','%.2E'%flux_r_on_sm)

print('sm outfall nh4 flux (mmol/month): ','%.2E'%flux_o_nh4_sm)
print('sm outfall no3 flux (mmol/month): ','%.2E'%flux_o_no3_sm)
print('sm outfall on flux (mmol/month): ','%.2E'%flux_o_on_sm)

print('sp river nh4 flux (mmol/month): ','%.2E'%flux_r_nh4_sp)
print('sp river no3 flux (mmol/month): ','%.2E'%flux_r_no3_sp)
print('sp river on flux (mmol/month): ','%.2E'%flux_r_on_sp)

print('sp outfall nh4 flux (mmol/month): ','%.2E'%flux_o_nh4_sp)
print('sp outfall no3 flux (mmol/month): ','%.2E'%flux_o_no3_sp)
print('sp outfall on flux (mmol/month): ','%.2E'%flux_o_on_sp)

print('rb river nh4 flux (mmol/month): ','%.2E'%flux_r_nh4_rb)
print('rb river no3 flux (mmol/month): ','%.2E'%flux_r_no3_rb)
print('rb river on flux (mmol/month): ','%.2E'%flux_r_on_rb)

print('rb outfall nh4 flux (mmol/month): ','%.2E'%flux_o_nh4_rb)
print('rb outfall no3 flux (mmol/month): ','%.2E'%flux_o_no3_rb)
print('rb outfall on flux (mmol/month): ','%.2E'%flux_o_on_rb)

print('all river nh4 flux (mmol/month): ','%.2E'%flux_r_nh4_all)
print('all river no3 flux (mmol/month): ','%.2E'%flux_r_no3_all)
print('all river on flux (mmol/month): ','%.2E'%flux_r_on_all)

print('all outfall nh4 flux (mmol/month): ','%.2E'%flux_o_nh4_all)
print('all outfall no3 flux (mmol/month): ','%.2E'%flux_o_no3_all)
print('all outfall on flux (mmol/month): ','%.2E'%flux_o_on_all)


'''
print('coast river nh4 flux (mmol/month): ',flux_r_nh4_sb)
print('coast river no3 flux (mmol/month): ',flux_r_no3_sb)
print('coast river on flux (mmol/month): ',flux_r_on_sb)

print('coast outfall nh4 flux (mmol/month): ',flux_o_nh4_sb)
print('coast outfall no3 flux (mmol/month): ',flux_o_no3_sb)
print('coast outfall on flux (mmol/month): ',flux_o_on_sb)

print('coast river nh4 flux (mmol/month): ',flux_r_nh4_sm)
print('coast river no3 flux (mmol/month): ',flux_r_no3_sm)
print('coast river on flux (mmol/month): ',flux_r_on_sm)

print('coast outfall nh4 flux (mmol/month): ',flux_o_nh4_sm)
print('coast outfall no3 flux (mmol/month): ',flux_o_no3_sm)
print('coast outfall on flux (mmol/month): ',flux_o_on_sm)

print('coast river nh4 flux (mmol/month): ',flux_r_nh4_sp)
print('coast river no3 flux (mmol/month): ',flux_r_no3_sp)
print('coast river on flux (mmol/month): ',flux_r_on_sp)

print('coast outfall nh4 flux (mmol/month): ',flux_o_nh4_sp)
print('coast outfall no3 flux (mmol/month): ',flux_o_no3_sp)
print('coast outfall on flux (mmol/month): ',flux_o_on_sp)
'''
