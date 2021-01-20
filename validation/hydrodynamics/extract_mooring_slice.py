###########################
# extract surface and deep currents
###########################
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import pandas as pd
import ROMS_depths as rdepth

################
# ORANGE COUNTY
################
# January 1, 2000, was 2451545
# take time variable in 
#/data/project1/minnaho/validation/ocsd_george_robertson/plume_tracking_mooring_data_1999_2000/Orange_netcdf
# and subtract that number to get days since 2000-01-01
oc_moor_path = '/data/project1/minnaho/validation/ocsd_george_robertson/plume_tracking_mooring_data_1999_2000/Orange_netcdf/*.nc'

oc_jul = 2451545
oc_unit = 'days since 2000-01-01'


oc_moor_file = glob.glob(oc_moor_path)

oc_lat = np.empty((len(oc_moor_file)))
oc_lon = np.empty((len(oc_moor_file)))
oc_dep = []
oc_date = []
oc_u = []
oc_v = []
for oc_i in range(len(oc_moor_file)):
    oc_nc = Dataset(oc_moor_file[oc_i],'r')
    oc_lat[oc_i] = float(np.array(oc_nc.variables['latitude']))
    oc_lon[oc_i] = float(np.array(oc_nc.variables['longitude']))
    oc_dep.append(np.array(oc_nc.variables['depth']))
    # all OC data is 1999-06 - 2000-06
    oc_date.append(num2date(np.array(oc_nc.variables['time'])-oc_jul,oc_unit,only_use_cftime_datetimes=False))
    # multiply by flag for interpolated values
    # interpolated values are 1, noninterpolated are 0
    # convert cm/s to m/s
    u_final = (np.array(oc_nc.variables['U_cmpt'])*np.array(oc_nc.variables['U_cmpt_flag']))/100
    u_final[u_final==0] = np.nan
    v_final = (np.array(oc_nc.variables['V_cmpt'])*np.array(oc_nc.variables['V_cmpt_flag']))/100
    v_final[v_final==0] = np.nan
    oc_u.append(u_final) 
    oc_v.append(v_final) 

# depths of 5 m in oc data
# oc_dep[1:7:2] # 5 m values
oc_dt_7m = list(oc_date[7])
oc_la_7m = oc_lat[7]
oc_lo_7m = oc_lon[7]
oc_7m_u = oc_u[7][:,24]
oc_7m_v = oc_v[7][:,24]

# find indices for each season
oc_win_7m = []
oc_sum_7m = []
for d_i in range(len(oc_dt_7m)):
    if (oc_dt_7m[d_i].month == 1 or oc_dt_7m[d_i].month == 2 or oc_dt_7m[d_i].month == 12):
        oc_win_7m.append(d_i)
    if (oc_dt_7m[d_i].month == 6 or oc_dt_7m[d_i].month == 7 or oc_dt_7m[d_i].month == 8):
        oc_sum_7m.append(d_i)

# 5m dates
oc_dt_5m_0 = oc_date[1:7:2][0]
oc_dt_5m_1 = oc_date[1:7:2][1]
oc_dt_5m_2 = oc_date[1:7:2][2]

# find indices for each season
oc_win_5m_0 = []
oc_sum_5m_0 = []
for d_i in range(len(oc_dt_5m_0)):
    if (oc_dt_5m_0[d_i].month == 1 or oc_dt_5m_0[d_i].month == 2 or oc_dt_5m_0[d_i].month == 12):
        oc_win_5m_0.append(d_i)
    if (oc_dt_5m_0[d_i].month == 6 or oc_dt_5m_0[d_i].month == 7 or oc_dt_5m_0[d_i].month == 8):
        oc_sum_5m_0.append(d_i)

oc_win_5m_1 = []
oc_sum_5m_1 = []
for d_i in range(len(oc_dt_5m_1)):
    if (oc_dt_5m_1[d_i].month == 1 or oc_dt_5m_1[d_i].month == 2 or oc_dt_5m_1[d_i].month == 12):
        oc_win_5m_1.append(d_i)
    if (oc_dt_5m_1[d_i].month == 6 or oc_dt_5m_1[d_i].month == 7 or oc_dt_5m_1[d_i].month == 8):
        oc_sum_5m_1.append(d_i)

oc_win_5m_2 = []
oc_sum_5m_2 = []
for d_i in range(len(oc_dt_5m_2)):
    if (oc_dt_5m_2[d_i].month == 1 or oc_dt_5m_2[d_i].month == 2 or oc_dt_5m_2[d_i].month == 12):
        oc_win_5m_2.append(d_i)
    if (oc_dt_5m_2[d_i].month == 6 or oc_dt_5m_2[d_i].month == 7 or oc_dt_5m_2[d_i].month == 8):
        oc_sum_5m_2.append(d_i)

# assign values
oc_la_5m_0 = oc_lat[1:7:2][0]
oc_la_5m_1 = oc_lat[1:7:2][1]
oc_la_5m_2 = oc_lat[1:7:2][2]

oc_lo_5m_0 = oc_lon[1:7:2][0]
oc_lo_5m_1 = oc_lon[1:7:2][1]
oc_lo_5m_2 = oc_lon[1:7:2][2]

oc_5m_u0 = np.squeeze(oc_u[1:7:2][0])
oc_5m_u1 = np.squeeze(oc_u[1:7:2][1])
oc_5m_u2 = np.squeeze(oc_u[1:7:2][2])

oc_5m_v0 = np.squeeze(oc_v[1:7:2][0])
oc_5m_v1 = np.squeeze(oc_v[1:7:2][1])
oc_5m_v2 = np.squeeze(oc_v[1:7:2][2])

# get u/v values

oc_7m_win_u = oc_7m_u[oc_win_7m]
oc_7m_win_v = oc_7m_v[oc_win_7m]
oc_7m_sum_u = oc_7m_u[oc_sum_7m]
oc_7m_sum_v = oc_7m_v[oc_sum_7m]

oc_5m_win_u0 = oc_5m_u0[oc_win_5m_0]
oc_5m_win_v0 = oc_5m_v0[oc_win_5m_0]
oc_5m_sum_u0 = oc_5m_u0[oc_sum_5m_0]
oc_5m_sum_v0 = oc_5m_v0[oc_sum_5m_0]

oc_5m_win_u1 = oc_5m_u1[oc_win_5m_1]
oc_5m_win_v1 = oc_5m_v1[oc_win_5m_1]
oc_5m_sum_u1 = oc_5m_u1[oc_sum_5m_1]
oc_5m_sum_v1 = oc_5m_v1[oc_sum_5m_1]

oc_5m_win_u2 = oc_5m_u2[oc_win_5m_2]
oc_5m_win_v2 = oc_5m_v2[oc_win_5m_2]
oc_5m_sum_u2 = oc_5m_u2[oc_sum_5m_2]
oc_5m_sum_v2 = oc_5m_v2[oc_sum_5m_2]

# depths of 50 m in oc data
# same lat/lon and time as 7m
oc_50m_u = oc_u[7][:,2]
oc_50m_v = oc_v[7][:,2]
oc_50m_win_u = oc_50m_u[oc_win_7m]
oc_50m_win_v = oc_50m_v[oc_win_7m]
oc_50m_sum_u = oc_50m_u[oc_sum_7m]
oc_50m_sum_v = oc_50m_v[oc_sum_7m]

np.save('./moor_npy/oc_lat_7m.npy',oc_la_7m)
np.save('./moor_npy/oc_lon_7m.npy',oc_lo_7m)
np.save('./moor_npy/oc_7m_win_u.npy',oc_7m_win_u)
np.save('./moor_npy/oc_7m_win_v.npy',oc_7m_win_v)
np.save('./moor_npy/oc_7m_sum_u.npy',oc_7m_sum_u)
np.save('./moor_npy/oc_7m_sum_v.npy',oc_7m_sum_v)

np.save('./moor_npy/oc_lat_50m.npy',oc_la_7m)
np.save('./moor_npy/oc_lon_50m.npy',oc_lo_7m)
np.save('./moor_npy/oc_50m_win_u.npy',oc_50m_win_u)
np.save('./moor_npy/oc_50m_win_v.npy',oc_50m_win_v)
np.save('./moor_npy/oc_50m_sum_u.npy',oc_50m_sum_u)
np.save('./moor_npy/oc_50m_sum_v.npy',oc_50m_sum_v)

np.save('./moor_npy/oc_lat_5m_0.npy',oc_la_5m_0)
np.save('./moor_npy/oc_lat_5m_1.npy',oc_la_5m_1)
np.save('./moor_npy/oc_lat_5m_2.npy',oc_la_5m_2)

np.save('./moor_npy/oc_lon_5m_0.npy',oc_lo_5m_0)
np.save('./moor_npy/oc_lon_5m_1.npy',oc_lo_5m_1)
np.save('./moor_npy/oc_lon_5m_2.npy',oc_lo_5m_2)

np.save('./moor_npy/oc_5m_win_u0.npy',oc_5m_win_u0)
np.save('./moor_npy/oc_5m_win_v0.npy',oc_5m_win_v0)
np.save('./moor_npy/oc_5m_sum_u0.npy',oc_5m_sum_u0)
np.save('./moor_npy/oc_5m_sum_v0.npy',oc_5m_sum_v0)

np.save('./moor_npy/oc_5m_win_u1.npy',oc_5m_win_u1)
np.save('./moor_npy/oc_5m_win_v1.npy',oc_5m_win_v1)
np.save('./moor_npy/oc_5m_sum_u1.npy',oc_5m_sum_u1)
np.save('./moor_npy/oc_5m_sum_v1.npy',oc_5m_sum_v1)

np.save('./moor_npy/oc_5m_win_u2.npy',oc_5m_win_u2)
np.save('./moor_npy/oc_5m_win_v2.npy',oc_5m_win_v2)
np.save('./moor_npy/oc_5m_sum_u2.npy',oc_5m_sum_u2)
np.save('./moor_npy/oc_5m_sum_v2.npy',oc_5m_sum_v2)


#####################
# PALOS VERDES LACSD
#####################
la_moor_path = '/data/project1/minnaho/validation/validation_data_moorings/PV_moored/A[1-9]*.xlsx'
la_moor_file = glob.glob(la_moor_path)

la_unit = 'minutes since 2000-11-20 00:15'


la_lat = np.empty((len(la_moor_file)))
la_lon = np.empty((len(la_moor_file)))
la_u_05m = []
la_v_05m = []
la_u_50m = []
la_v_50m = []
for la_i in range(len(la_moor_file)):
    xl05 = pd.read_excel(la_moor_file[la_i],sheet_name='5m')
    la_lat[la_i] = xl05['latitude'][1]
    la_lon[la_i] = xl05['longitude'][1]
    u_final_05 = np.array(xl05['EW_velocity']/100) # cm/s to m/s
    u_final_05[u_final_05<-99] = np.nan
    v_final_05 = np.array(xl05['NS_velocity']/100)
    v_final_05[v_final_05<-99] = np.nan
    la_u_05m.append(u_final_05) 
    la_v_05m.append(v_final_05) 
    xl50 = pd.read_excel(la_moor_file[la_i],sheet_name='50m')
    try:
        u_final_50 = np.array(xl50['EW_velocity']/100)
        v_final_50 = np.array(xl50['NS_velocity']/100)
        u_final_50[u_final_50<-99] = np.nan
        v_final_50[v_final_50<-99] = np.nan
    except:
        u_final_50 = np.nan
        v_final_50 = np.nan
    la_u_50m.append(u_final_50) 
    la_v_50m.append(v_final_50) 

# la time
la_date = np.empty((u_final_05.shape[0]))
# make time array; 15 minute intervals
for d_i in range(len(u_final_05)):
    la_date[d_i] = 15*d_i

la_dt = num2date(la_date,la_unit,only_use_cftime_datetimes=False)

# get indices only until 12/2000
#en_ind = 5951

# get indices only until 9/2001
#en_ind = 30000

# get indices until 9/2002
en_ind =64400

la_win_dt = []
la_sum_dt = []
for d_i in range(len(la_dt[:en_ind])):
    if (la_dt[d_i].month == 1 or la_dt[d_i].month == 2 or la_dt[d_i].month == 12):
        la_win_dt.append(d_i)
    if (la_dt[d_i].month == 6 or la_dt[d_i].month == 7 or la_dt[d_i].month == 8):
        la_sum_dt.append(d_i)

mon = []
for d_i in range(len(la_dt)):
    mon.append(la_dt[d_i].month)

mon = np.unique(np.array(mon))
    
la_u_win_05m = np.empty((len(la_u_05m),len(la_u_05m[0][la_win_dt])))
la_v_win_05m = np.empty((len(la_v_05m),len(la_v_05m[0][la_win_dt])))
la_u_sum_05m = np.empty((len(la_u_05m),len(la_u_05m[0][la_sum_dt])))
la_v_sum_05m = np.empty((len(la_v_05m),len(la_v_05m[0][la_sum_dt])))

la_u_win_50m = np.empty((len(la_u_50m),len(la_u_50m[0][la_win_dt])))
la_v_win_50m = np.empty((len(la_v_50m),len(la_v_50m[0][la_win_dt])))
la_u_sum_50m = np.empty((len(la_u_50m),len(la_u_50m[0][la_sum_dt])))
la_v_sum_50m = np.empty((len(la_v_50m),len(la_v_50m[0][la_sum_dt])))

# shape is number of moorings by time
for l_i in range(la_u_win_50m.shape[0]):
    try:
        la_u_win_05m[l_i,:] = la_u_05m[l_i][la_win_dt]
        la_v_win_05m[l_i,:] = la_v_05m[l_i][la_win_dt]
        la_u_sum_05m[l_i,:] = la_u_05m[l_i][la_sum_dt]
        la_v_sum_05m[l_i,:] = la_v_05m[l_i][la_sum_dt]
    except:
        la_u_win_05m[l_i,:] = np.nan
        la_v_win_05m[l_i,:] = np.nan
        la_u_sum_05m[l_i,:] = np.nan
        la_v_sum_05m[l_i,:] = np.nan
    try:
        la_u_win_50m[l_i,:] = la_u_50m[l_i][la_win_dt]
        la_v_win_50m[l_i,:] = la_v_50m[l_i][la_win_dt]
        la_u_sum_50m[l_i,:] = la_u_50m[l_i][la_sum_dt]
        la_v_sum_50m[l_i,:] = la_v_50m[l_i][la_sum_dt]
    except:
        la_u_win_50m[l_i,:] = np.nan
        la_v_win_50m[l_i,:] = np.nan
        la_u_sum_50m[l_i,:] = np.nan
        la_v_sum_50m[l_i,:] = np.nan

np.save('./moor_npy/la_u_win_05m.npy',la_u_win_05m)
np.save('./moor_npy/la_v_win_05m.npy',la_v_win_05m)

np.save('./moor_npy/la_u_sum_05m.npy',la_u_sum_05m)
np.save('./moor_npy/la_v_sum_05m.npy',la_v_sum_05m)

np.save('./moor_npy/la_u_win_50m.npy',la_u_win_50m)
np.save('./moor_npy/la_v_win_50m.npy',la_v_win_50m)

np.save('./moor_npy/la_u_sum_50m.npy',la_u_sum_50m)
np.save('./moor_npy/la_v_sum_50m.npy',la_v_sum_50m)

np.save('./moor_npy/la_moor_time.npy',la_dt)
np.save('./moor_npy/la_lat.npy',la_lat)
np.save('./moor_npy/la_lon.npy',la_lon)

