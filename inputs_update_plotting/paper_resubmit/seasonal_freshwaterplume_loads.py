import numpy as np
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pandas as pd

fig_path = './figs/'
# data paths
river_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc'
potw_major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'

###############
# river major data (10 yrs) 1997-2007
###############
river_nc = Dataset(river_path,'r')

river_time = num2date(np.array(river_nc.variables['time']),river_nc.variables['time'].units)

# convert real_datetime to datetime
river_time_l = []
for d_i in range(len(river_time)):
    river_time_l.append(river_time[d_i]+datetime.timedelta(0,1))

river_time_dt = np.array(river_time_l)

# divide flows

river_flo = np.array(river_nc.variables['flow']) # m3/s
river_nh4 = np.array(river_nc.variables['NH4']) # mmol/m3
river_no3 = np.array(river_nc.variables['NO3']) # mmol/m3

river_nh4[river_nh4>1E10] = np.nan
river_no3[river_no3>1E10] = np.nan
river_flo[river_flo>1E10] = np.nan

river_din = np.nansum((river_nh4,river_no3),axis=0)

l_river_din = river_flo*river_din
l_river_nh4 = river_flo*river_nh4
l_river_no3 = river_flo*river_no3

# 7/31/1999
p_st_r = 30
# 9/30/2000
p_en_r = 44+1 # +1 to end in 9/30

l_river_din_win = l_river_din[p_st_r:p_en_r][6:8+1]
l_river_din_spr = l_river_din[p_st_r:p_en_r][9:11+1]
l_river_din_sum = l_river_din[p_st_r:p_en_r][12:14+1]
l_river_din_fal = l_river_din[p_st_r:p_en_r][3:5+1]

l_river_nh4_win = l_river_nh4[p_st_r:p_en_r][6:8+1]
l_river_nh4_spr = l_river_nh4[p_st_r:p_en_r][9:11+1]
l_river_nh4_sum = l_river_nh4[p_st_r:p_en_r][12:14+1]
l_river_nh4_fal = l_river_nh4[p_st_r:p_en_r][3:5+1]

l_river_no3_win = l_river_no3[p_st_r:p_en_r][6:8+1]
l_river_no3_spr = l_river_no3[p_st_r:p_en_r][9:11+1]
l_river_no3_sum = l_river_no3[p_st_r:p_en_r][12:14+1]
l_river_no3_fal = l_river_no3[p_st_r:p_en_r][3:5+1]

total_river_din_win = np.nansum(l_river_din_win,axis=1)
total_river_nh4_win = np.nansum(l_river_nh4_win,axis=1)
total_river_no3_win = np.nansum(l_river_no3_win,axis=1)

total_river_din_spr = np.nansum(l_river_din_spr,axis=1)
total_river_nh4_spr = np.nansum(l_river_nh4_spr,axis=1)
total_river_no3_spr = np.nansum(l_river_no3_spr,axis=1)

total_river_din_sum = np.nansum(l_river_din_sum,axis=1)
total_river_nh4_sum = np.nansum(l_river_nh4_sum,axis=1)
total_river_no3_sum = np.nansum(l_river_no3_sum,axis=1)

total_river_din_fal = np.nansum(l_river_din_fal,axis=1)
total_river_nh4_fal = np.nansum(l_river_nh4_fal,axis=1)
total_river_no3_fal = np.nansum(l_river_no3_fal,axis=1)

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2010
potw_1997 = 312 # 1997-01-31
potw_2013 = major_potw_time.shape[0] # 2017-01-01

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l[potw_1997:potw_2013])

# divide flows
major_flo = np.array(potw_ma_nc.variables['flow']) # m3/s
major_nh4 = np.array(potw_ma_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(potw_ma_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(potw_ma_nc.variables['NO2']) # mmol/m3

major_nh4[major_nh4>1E10] = np.nan
major_no3[major_no3>1E10] = np.nan
major_no2[major_no2>1E10] = np.nan
major_flo[major_flo>1E10] = np.nan

major_din = np.nansum((major_nh4,major_no3,major_no2),axis=0)

l_major_din = major_flo*major_din
l_major_nh4 = major_flo*major_nh4
l_major_no3 = major_flo*major_no3

# large potw
# 7/31/1999
p_st_r = 30
# 9/30/2000
p_en_r = 44+1 # +1 to end in 9/30

l_major_din_win = l_major_din[p_st_r:p_en_r][6:8+1]
l_major_din_spr = l_major_din[p_st_r:p_en_r][9:11+1]
l_major_din_sum = l_major_din[p_st_r:p_en_r][12:14+1]
l_major_din_fal = l_major_din[p_st_r:p_en_r][3:5+1]

l_major_nh4_win = l_major_nh4[p_st_r:p_en_r][6:8+1]
l_major_nh4_spr = l_major_nh4[p_st_r:p_en_r][9:11+1]
l_major_nh4_sum = l_major_nh4[p_st_r:p_en_r][12:14+1]
l_major_nh4_fal = l_major_nh4[p_st_r:p_en_r][3:5+1]

l_major_no3_win = l_major_no3[p_st_r:p_en_r][6:8+1]
l_major_no3_spr = l_major_no3[p_st_r:p_en_r][9:11+1]
l_major_no3_sum = l_major_no3[p_st_r:p_en_r][12:14+1]
l_major_no3_fal = l_major_no3[p_st_r:p_en_r][3:5+1]

total_major_din_win = np.nansum(l_major_din_win,axis=1)
total_major_nh4_win = np.nansum(l_major_nh4_win,axis=1)
total_major_no3_win = np.nansum(l_major_no3_win,axis=1)

total_major_din_spr = np.nansum(l_major_din_spr,axis=1)
total_major_nh4_spr = np.nansum(l_major_nh4_spr,axis=1)
total_major_no3_spr = np.nansum(l_major_no3_spr,axis=1)

total_major_din_sum = np.nansum(l_major_din_sum,axis=1)
total_major_nh4_sum = np.nansum(l_major_nh4_sum,axis=1)
total_major_no3_sum = np.nansum(l_major_no3_sum,axis=1)

total_major_din_fal = np.nansum(l_major_din_fal,axis=1)
total_major_nh4_fal = np.nansum(l_major_nh4_fal,axis=1)
total_major_no3_fal = np.nansum(l_major_no3_fal,axis=1)


##############
# minor potw
##############
potw_mi_nc = Dataset(potw_minor_path,'r')

# divide flows
minor_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3

minor_nh4[minor_nh4>1E10] = np.nan
minor_no3[minor_no3>1E10] = np.nan
minor_no2[minor_no2>1E10] = np.nan
minor_flo[minor_flo>1E10] = np.nan

minor_din = np.nansum((minor_nh4,minor_no3,minor_no2),axis=0)

l_minor_din = minor_flo*minor_din
l_minor_nh4 = minor_flo*minor_nh4
l_minor_no3 = minor_flo*minor_no3

# small potw
# 7/31/1999
p_st_r = 30
# 9/30/2000
p_en_r = 44+1 # +1 to end in 9/30

l_minor_din_win = l_minor_din[p_st_r:p_en_r][6:8+1]
l_minor_din_spr = l_minor_din[p_st_r:p_en_r][9:11+1]
l_minor_din_sum = l_minor_din[p_st_r:p_en_r][12:14+1]
l_minor_din_fal = l_minor_din[p_st_r:p_en_r][3:5+1]

l_minor_nh4_win = l_minor_nh4[p_st_r:p_en_r][6:8+1]
l_minor_nh4_spr = l_minor_nh4[p_st_r:p_en_r][9:11+1]
l_minor_nh4_sum = l_minor_nh4[p_st_r:p_en_r][12:14+1]
l_minor_nh4_fal = l_minor_nh4[p_st_r:p_en_r][3:5+1]

l_minor_no3_win = l_minor_no3[p_st_r:p_en_r][6:8+1]
l_minor_no3_spr = l_minor_no3[p_st_r:p_en_r][9:11+1]
l_minor_no3_sum = l_minor_no3[p_st_r:p_en_r][12:14+1]
l_minor_no3_fal = l_minor_no3[p_st_r:p_en_r][3:5+1]

total_minor_din_win = np.nansum(l_minor_din_win,axis=1)
total_minor_nh4_win = np.nansum(l_minor_nh4_win,axis=1)
total_minor_no3_win = np.nansum(l_minor_no3_win,axis=1)

total_minor_din_spr = np.nansum(l_minor_din_spr,axis=1)
total_minor_nh4_spr = np.nansum(l_minor_nh4_spr,axis=1)
total_minor_no3_spr = np.nansum(l_minor_no3_spr,axis=1)

total_minor_din_sum = np.nansum(l_minor_din_sum,axis=1)
total_minor_nh4_sum = np.nansum(l_minor_nh4_sum,axis=1)
total_minor_no3_sum = np.nansum(l_minor_no3_sum,axis=1)

total_minor_din_fal = np.nansum(l_minor_din_fal,axis=1)
total_minor_nh4_fal = np.nansum(l_minor_nh4_fal,axis=1)
total_minor_no3_fal = np.nansum(l_minor_no3_fal,axis=1)

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14
g_P = 30.97

fal_river_no3 = np.nansum(total_river_no3_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_river_no3 = np.nansum(total_river_no3_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_river_no3 = np.nansum(total_river_no3_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_river_no3 = np.nansum(total_river_no3_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_river_nh4 = np.nansum(total_river_nh4_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_river_nh4 = np.nansum(total_river_nh4_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_river_nh4 = np.nansum(total_river_nh4_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_river_nh4 = np.nansum(total_river_nh4_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_river_din = np.nansum(total_river_din_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_river_din = np.nansum(total_river_din_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_river_din = np.nansum(total_river_din_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_river_din = np.nansum(total_river_din_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)


fal_major_no3 = np.nansum(total_major_no3_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_major_no3 = np.nansum(total_major_no3_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_major_no3 = np.nansum(total_major_no3_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_major_no3 = np.nansum(total_major_no3_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_major_nh4 = np.nansum(total_major_nh4_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_major_nh4 = np.nansum(total_major_nh4_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_major_nh4 = np.nansum(total_major_nh4_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_major_nh4 = np.nansum(total_major_nh4_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_major_din = np.nansum(total_major_din_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_major_din = np.nansum(total_major_din_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_major_din = np.nansum(total_major_din_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_major_din = np.nansum(total_major_din_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)


fal_minor_no3 = np.nansum(total_minor_no3_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_minor_no3 = np.nansum(total_minor_no3_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_minor_no3 = np.nansum(total_minor_no3_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_minor_no3 = np.nansum(total_minor_no3_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_minor_nh4 = np.nansum(total_minor_nh4_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_minor_nh4 = np.nansum(total_minor_nh4_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_minor_nh4 = np.nansum(total_minor_nh4_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_minor_nh4 = np.nansum(total_minor_nh4_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

fal_minor_din = np.nansum(total_minor_din_fal*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
win_minor_din = np.nansum(total_minor_din_win*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
spr_minor_din = np.nansum(total_minor_din_spr*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)
sum_minor_din = np.nansum(total_minor_din_sum*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)

print('fal_river_no3',fal_river_no3)
print('win_river_no3',win_river_no3)
print('spr_river_no3',spr_river_no3)
print('sum_river_no3',sum_river_no3)
                                   
print('fal_river_nh4',fal_river_nh4)
print('win_river_nh4',win_river_nh4)
print('spr_river_nh4',spr_river_nh4)
print('sum_river_nh4',sum_river_nh4)
                                   
print('fal_river_din',fal_river_din)
print('win_river_din',win_river_din)
print('spr_river_din',spr_river_din)
print('sum_river_din',sum_river_din)
                                   
                                  
print('fal_major_no3',fal_major_no3)
print('win_major_no3',win_major_no3)
print('spr_major_no3',spr_major_no3)
print('sum_major_no3',sum_major_no3)
                                  
print('fal_major_nh4',fal_major_nh4)
print('win_major_nh4',win_major_nh4)
print('spr_major_nh4',spr_major_nh4)
print('sum_major_nh4',sum_major_nh4)
                                  
print('fal_major_din',fal_major_din)
print('win_major_din',win_major_din)
print('spr_major_din',spr_major_din)
print('sum_major_din',sum_major_din)
                                  
                                  
print('fal_minor_no3',fal_minor_no3)
print('win_minor_no3',win_minor_no3)
print('spr_minor_no3',spr_minor_no3)
print('sum_minor_no3',sum_minor_no3)
                                  
print('fal_minor_nh4',fal_minor_nh4)
print('win_minor_nh4',win_minor_nh4)
print('spr_minor_nh4',spr_minor_nh4)
print('sum_minor_nh4',sum_minor_nh4)
                                  
print('fal_minor_din',fal_minor_din)
print('win_minor_din',win_minor_din)
print('spr_minor_din',spr_minor_din)
print('sum_minor_din',sum_minor_din)
