###########################
# extract surface and deep currents
###########################
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import pandas as pd
import ROMS_depths as rdepth
import pickle as pickle

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

oc_dt_7m = list(oc_date[7])


# find indices for each season
oc_win_7m = []
oc_sum_7m = []
for d_i in range(len(oc_dt_7m)):
    if (oc_dt_7m[d_i].month == 1 or oc_dt_7m[d_i].month == 2 or oc_dt_7m[d_i].month == 12):
        oc_win_7m.append(d_i)
    if (oc_dt_7m[d_i].month == 6 or oc_dt_7m[d_i].month == 7 or oc_dt_7m[d_i].month == 8):
        oc_sum_7m.append(d_i)

# depths of 50 m in oc data
# same lat/lon and time as 7m
oc_la_7m = oc_lat[7]
oc_lo_7m = oc_lon[7]
oc_prof_u = oc_u[7]
oc_prof_v = oc_v[7]
oc_prof_win_u = oc_prof_u[oc_win_7m,:]
oc_prof_win_v = oc_prof_v[oc_win_7m,:]
oc_prof_sum_u = oc_prof_u[oc_sum_7m,:]
oc_prof_sum_v = oc_prof_v[oc_sum_7m,:]

np.save('./moor_npy/oc_prof_lat.npy',oc_la_7m)
np.save('./moor_npy/oc_prof_lon.npy',oc_lo_7m)
np.save('./moor_npy/oc_prof_u.npy',oc_prof_u)
np.save('./moor_npy/oc_prof_v.npy',oc_prof_v)
np.save('./moor_npy/oc_prof_win_u.npy',oc_prof_win_u)
np.save('./moor_npy/oc_prof_win_v.npy',oc_prof_win_v)
np.save('./moor_npy/oc_prof_sum_u.npy',oc_prof_sum_u)
np.save('./moor_npy/oc_prof_sum_v.npy',oc_prof_sum_v)
np.save('./moor_npy/oc_prof_dep_7_55.npy',oc_dep[7])

#####################
# PALOS VERDES LACSD
#####################
la_moor_path = '/data/project1/minnaho/validation/validation_data_moorings/PV_moored/A[1-9]*.xlsx'
la_moor_file = glob.glob(la_moor_path)

la_unit = 'minutes since 2000-11-20 00:15'

la_lat = np.empty((len(la_moor_file)))
la_lon = np.empty((len(la_moor_file)))
la_dep_prof = []
#la_u_prof = np.empty((len(la_moor_file),262560)) # time length
#la_v_prof = np.empty((len(la_moor_file),262560)) 
#la_u_prof.fill(np.nan)
#la_v_prof.fill(np.nan)

la_u_prof = []
la_v_prof = []
for la_i in range(len(la_moor_file)):
    xl = pd.ExcelFile(la_moor_file[la_i])
    sheetnms = xl.sheet_names
    str_list = [s.strip('m') for s in sheetnms]
    flt_list = [float(i) for i in str_list]
    la_dep_prof.append(flt_list)
    for s_i in range(len(sheetnms)):
        df = pd.read_excel(la_moor_file[la_i],sheet_name=sheetnms[s_i])
        try:
            la_lat[la_i] = df['latitude'][1]
            la_lon[la_i] = df['longitude'][1]
            u_final = np.array(df['EW_velocity']/100) # cm/s to m/s
            u_final[u_final<-99] = np.nan
            v_final = np.array(df['NS_velocity']/100)
            v_final[v_final<-99] = np.nan
        except:
            u_final = np.nan
            v_final = np.nan
        la_u_prof.append(u_final)
        la_v_prof.append(v_final)

pickle.dump(la_u_prof,open('la_u_prof.pkl','wb'))
pickle.dump(la_v_prof,open('la_v_prof.pkl','wb'))
pickle.dump(la_dep_prof,open('la_dep_prof.pkl','wb'))

# la time
la_date = np.empty((len(la_u_prof[0])))
# make time array; 15 minute intervals
for d_i in range(len(la_u_prof[0])):
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

np.save('./moor_npy/la_win_ind.npy',np.array(la_win_dt))
np.save('./moor_npy/la_sum_ind.npy',np.array(la_sum_dt))

pickle.dump(la_dt,open('la_moor_time.pkl','wb'))

np.save('./moor_npy/la_moor_time.npy',la_dt)
np.save('./moor_npy/la_lat.npy',la_lat)
np.save('./moor_npy/la_lon.npy',la_lon)

