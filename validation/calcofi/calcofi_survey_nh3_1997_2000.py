###################################################################
# read calcofi data and bight survey data NH3 and create netcdf
# maps of 1997-2000 on L2 map for validation
# Oct 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
import depths as depths
#plt.ion()

# save figs path
save_figs = './figs/'

##########################
# load observation data
#########################
# calcofi
text_file = pd.read_csv('calcofi_database.csv',header=None,low_memory=False,skiprows=1)
time_unit = 'minutes since 1949-03-01 09:30:00'
# choose variable
variable_name = 'NH3'
cc_n_unit = 'umol/L'
cc_num = 31

# central bight surveys 
cb_data = '/data/project1/minnaho/validation/central_bight/central_bight_master_database_1998_2017_1D_new.nc'
cb_v = np.array(Dataset(cb_data,'r').variables['ammonia-N'])
cb_t = np.array(Dataset(cb_data,'r').variables['date'])
cb_d = np.array(Dataset(cb_data,'r').variables['depth'])
cb_n_unit = 'mg/L'
cb_t_unit = 'days since 1998-07-07'

# choose years
yr_s = 1997
yr_e = 2000

# calcofi convert datetime numbers to dates
cc_time_num = np.array((text_file.iloc[:,1]))
cc_date_conv = num2date(cc_time_num,time_unit)

# survey convert datetime numbers to dates
cb_date_conv = num2date(cb_t,cb_t_unit)

# get indexes of target years
print('getting indices of target years')
cc_yr_ind_l = []
for ind_d,d_i in enumerate(cc_date_conv):
    if d_i.year in list(range(yr_s,yr_e+1)):
        cc_yr_ind_l.append(ind_d) 

cb_yr_ind_l = []
for ind_d,d_i in enumerate(cb_date_conv):
    if d_i.year in list(range(yr_s,yr_e+1)):
        cb_yr_ind_l.append(ind_d) 

cc_yr_ind = np.array((cc_yr_ind_l))
cb_yr_ind = np.array((cb_yr_ind_l))

#####################################################
# load L2 grid and get grid locations of all sites within year range
#####################################################
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
nc_grid = Dataset(grid_path,'r')

lon_nc = nc_grid.variables['lon_rho'][:,:]
lat_nc = nc_grid.variables['lat_rho'][:,:]
mask_nc = nc_grid.variables['mask_rho'][:,:]

# choose between what lat/lon
# L2 domain 
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)

# calcofi
cc_lat = np.array((text_file.iloc[:,2]))
cc_lon = np.array((text_file.iloc[:,3]))

cc_lat_ind = np.where((cc_lat>lat_min) & (cc_lat<lat_max))[0]
cc_lon_ind = np.where((cc_lon>lon_min) & (cc_lon<lon_max))[0]

# find intersection of index values
cc_loc_ind = np.asarray((list(set(cc_lat_ind).intersection(cc_lon_ind))))
# find years and locations that we want
cc_data_ind = np.asarray(sorted((list(set(cc_loc_ind).intersection(cc_yr_ind)))))

# survey data
cb_lat = np.array(Dataset(cb_data,'r').variables['latitude'])
cb_lon = np.array(Dataset(cb_data,'r').variables['longitude'])
cb_lat_ind = np.where((cb_lat>lat_min) & (cb_lat<lat_max))[0]
cb_lon_ind = np.where((cb_lon>lon_min) & (cb_lon<lon_max))[0]

# find intersection of index values
cb_loc_ind = np.asarray((list(set(cb_lat_ind).intersection(cb_lon_ind))))
# find years and locations that we want
cb_data_ind = np.asarray(sorted((list(set(cb_loc_ind).intersection(cb_yr_ind)))))

# find closest grid point
# pair of lat,lon and find unique pair
cc_loc = np.unique(np.array((cc_lat[cc_data_ind],cc_lon[cc_data_ind])).transpose(),axis=0)
cb_loc = np.unique(np.array((cb_lat[cb_data_ind],cb_lon[cb_data_ind])).transpose(),axis=0)

# calcofi
cc_nsites = cc_loc.shape[0]
cc_x = np.empty(cc_nsites)
cc_y = np.empty(cc_nsites)
for s in range(cc_nsites):
    print('finding cc grid coordinate '+str(s))
    # find sites in gridpoints
    min_1D = np.abs( (lat_nc - cc_loc[s][0])**2 + (lon_nc - cc_loc[s][1])**2)
    y_site, x_site = np.unravel_index(min_1D.argmin(), min_1D.shape)
    cc_x[s] = x_site
    cc_y[s] = y_site

# survey
cb_nsites = cb_loc.shape[0]
cb_x = np.empty(cb_nsites)
cb_y = np.empty(cb_nsites)
for s in range(cb_nsites):
    print('finding cb grid coordinate '+str(s))
    # find sites in gridpoints
    min_1D = np.abs( (lat_nc - cb_loc[s][0])**2 + (lon_nc - cb_loc[s][1])**2)
    y_site, x_site = np.unravel_index(min_1D.argmin(), min_1D.shape)
    cb_x[s] = x_site
    cb_y[s] = y_site

cb_maxx = max(cb_x)
cb_maxy = max(cb_y)
cc_maxx = max(cc_x)
cc_maxy = max(cc_y)

###################################################
# find indices to separate into monthly averages and put into netcdf
################################################# 

# make netcdf
nc_file = Dataset('nh3_calcofi_potw_survey_1997_2000.nc','w')
nc_file.title = 'CalCOFI and POTW survey (central bight database) monthly averaged data for NH3 mapped to the ROMS L2 SCB domain'

time = nc_file.createDimension('time',None)
sigma = nc_file.createDimension('s_rho',60)
eta = nc_file.createDimension('eta_rho',lat_nc.shape[0])
xi = nc_file.createDimension('xi_rho',lat_nc.shape[1])

cc_nh3 = nc_file.createVariable('cc_ammonia',np.float32,('time','s_rho','eta_rho','xi_rho'))
cc_nh3.longname = 'CalCOFI NH3'
cc_nh3.units = 'mmol m-3'

cb_nh3 = nc_file.createVariable('cb_ammonia',np.float32,('time','s_rho','eta_rho','xi_rho'))
cb_nh3.longname = 'POTW Survey NH3'
cc_nh3.units = 'mmol m-3'

#depths 
cc_data_depth = np.array((text_file.iloc[:,19][cc_data_ind]))
cb_data_depth = np.array((cb_d[cb_data_ind]))

# data variable
cc_data_var = np.array((text_file.iloc[:,cc_num][cc_data_ind]))
cb_data_var = np.array((cb_v[cb_data_ind]))

#file_names = list(sorted(glob.glob('/data/project5/kesf/ROMS/L2SCB_AP/V3/monthly/l2_scb_avg.Y*')))
file_name = '/data/project5/kesf/ROMS/L2SCB_AP/V3/monthly/l2_scb_avg.Y'

# umol/L to mmol/m3
cc_conv = 1

# mg/L to mmol/m3
cb_conv = 1000./14

start_month = 2
end_month = 9
months = range(1,13)
m_i = 7
yr = 1998
l_i = 0

# create space in memory
del text_file
del cc_time_num
del cc_yr_ind_l 
del cb_yr_ind_l

del cc_lat_ind
del cb_lat_ind
del cc_lon_ind
del cb_lon_ind

del cc_loc_ind
del cb_loc_ind

del cc_nsites
del cc_x
del cc_y
del cb_nsites
del cb_x
del cb_y

del cb_v
del cb_d
del cb_t

t_nc = 0
for yr in range(yr_s,yr_e+1):
    if yr == yr_s:
        s_m = start_month
    else:
        s_m = 1 
    if yr == yr_e:
        e_m = end_month
    else:
        e_m = 13 
    for m_i in range(s_m,e_m):
        print('calculating nh3 for month '+str(m_i)+' '+str(yr))
        # these lists are to check if same depth and location in a month 
        # and year has been seen before and to then average it
        cc_sites_x = []
        cc_sites_y = []
        cc_sites_z = []
        cb_sites_x = []
        cb_sites_y = []
        cb_sites_z = []
        # time indices that match selected year and month 
        # and are not NaN in variable ata
        cb_t_ind = np.where(~np.isnan(cb_data_var[np.where((pd.to_datetime(cb_date_conv[cb_data_ind]).year==yr) & (pd.to_datetime(cb_date_conv[cb_data_ind]).month==m_i))[0]]))[0]
        cc_t_ind = np.where(~np.isnan(cc_data_var[np.where((pd.to_datetime(cc_date_conv[cc_data_ind]).year==yr) & (pd.to_datetime(cc_date_conv[cc_data_ind]).month==m_i))[0]]))[0]
        [z_sigmas,Cs] = depths.get_depths(file_name+str(yr)+'M'+'%02d'%m_i+'.nc',grid_path,0,'r','new')
        cb_temp = np.empty((cb_nh3.shape[1],int(cb_maxy),int(cb_maxx),20))
        cc_temp = np.empty((cb_nh3.shape[1],int(cc_maxy),int(cc_maxx),20))
        # find lat/lon and corresponding i,j
        c_i = 0
        for l_i in range(len(cb_t_ind)):
            if len(cb_t_ind) != 0:
                min_1D_l = np.abs( (lat_nc - cb_lat[cb_data_ind][cb_t_ind][l_i])**2 + (lon_nc - cb_lon[cb_data_ind][cb_t_ind][l_i])**2)
                y_site, x_site = np.unravel_index(min_1D_l.argmin(), min_1D_l.shape)
                dep_z = z_sigmas[:,y_site,x_site]
                min_1D_z = np.abs((dep_z - cb_data_depth[cb_t_ind][l_i])**2)
                z_site = min_1D_z.argmin()
                # check if same location and depth to average over
                cb_sites_x.append(x_site)
                cb_sites_y.append(y_site)
                cb_sites_z.append(z_site) 
                if np.where(np.array(cb_sites_y)==y_site)[0].shape[0] > 1 and np.where(np.array(cb_sites_x)==x_site)[0].shape[0] > 1 and np.where(np.array(cb_sites_z)==z_site)[0].shape[0] > 1:   
                    cb_temp[z_site,y_site,x_site,c_i] = cb_data_var[cb_t_ind][l_i]*cb_conv
                    c_i += 1
                else:
                    cb_nh3[t_nc,z_site,y_site,x_site] = cb_data_var[cb_t_ind][l_i]*cb_conv
            else:
                continue
        # average over duplicates
        for dup_i in range(len(cb_sites_y)):
            if len(cb_sites_y) != 0:
                cb_temp[cb_sites_z[dup_i],cb_sites_y[dup_i],cb_sites_x[dup_i],-1] = cb_nh3[t_nc,cb_sites_z[dup_i],cb_sites_y[dup_i],cb_sites_x[dup_i]]
                cb_nh3[t_nc,cb_sites_z[dup_i],cb_sites_y[dup_i],cb_sites_x[dup_i]] = np.nanmean(cb_temp[cb_sites_z[dup_i],cb_sites_y[dup_i],cb_sites_x[dup_i]])
        c_i = 0
        for l_i in range(len(cc_t_ind)):
            if len(cc_t_ind) != 0:
                min_1D_l = np.abs( (lat_nc - cc_lat[cc_data_ind][cc_t_ind][l_i])**2 + (lon_nc - cc_lon[cc_data_ind][cc_t_ind][l_i])**2)
                y_site, x_site = np.unravel_index(min_1D_l.argmin(), min_1D_l.shape)
                dep_z = z_sigmas[:,y_site,x_site]
                min_1D_z = np.abs((dep_z - cc_data_depth[cc_t_ind][l_i])**2)
                z_site = min_1D_z.argmin()
                # check if same location and depth to average over
                cc_sites_x.append(x_site)
                cc_sites_y.append(y_site)
                cc_sites_z.append(z_site) 
                if np.where(np.array(cc_sites_y)==y_site)[0].shape[0] > 1 and np.where(np.array(cc_sites_x)==x_site)[0].shape[0] > 1 and np.where(np.array(cc_sites_z)==z_site)[0].shape[0] > 1:   
                    cc_temp[z_site,y_site,x_site,c_i] = cc_data_var[cc_t_ind][l_i]*cc_conv
                    c_i += 1
                else:
                    cc_nh3[t_nc,z_site,y_site,x_site] = cc_data_var[cc_t_ind][l_i]*cc_conv
            else:
                continue
        for dup_i in range(len(cc_sites_y)):
            if len(cc_sites_y) != 0:
                cc_temp[cc_sites_z[dup_i],cc_sites_y[dup_i],cc_sites_x[dup_i],-1] = cc_nh3[t_nc,cc_sites_z[dup_i],cc_sites_y[dup_i],cc_sites_x[dup_i]]
                cc_nh3[t_nc,cc_sites_z[dup_i],cc_sites_y[dup_i],cc_sites_x[dup_i]] = np.nanmean(cc_temp[cc_sites_z[dup_i],cc_sites_y[dup_i],cc_sites_x[dup_i]])
        t_nc += 1
        del cb_temp 
        del cc_temp 

cb_nh3 = cb_nh3*mask_nc
cc_nh3 = cc_nh3*mask_nc

'''
months = range(1,13)
cc_ind_m01 = []
cc_ind_m02 = []
cc_ind_m03 = []
cc_ind_m04 = []
cc_ind_m05 = []
cc_ind_m06 = []
cc_ind_m07 = []
cc_ind_m08 = []
cc_ind_m09 = []
cc_ind_m10 = []
cc_ind_m11 = []
cc_ind_m12 = []

cb_ind_m01 = []
cb_ind_m02 = []
cb_ind_m03 = []
cb_ind_m04 = []
cb_ind_m05 = []
cb_ind_m06 = []
cb_ind_m07 = []
cb_ind_m08 = []
cb_ind_m09 = []
cb_ind_m10 = []
cb_ind_m11 = []
cb_ind_m12 = []

for t_i in range(len(cc_data_ind)):
    if cc_date_conv[cc_data_ind[t_i]].month == 1:
        cc_ind_m01.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 2:
        cc_ind_m02.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 3:
        cc_ind_m03.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 4:
        cc_ind_m04.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 5:
        cc_ind_m05.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 6:
        cc_ind_m06.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 7:
        cc_ind_m07.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 8:
        cc_ind_m08.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 9:
        cc_ind_m09.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 10:
        cc_ind_m10.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 11:
        cc_ind_m11.append(cc_data_ind[t_i])
    if cc_date_conv[cc_data_ind[t_i]].month == 12:
        cc_ind_m12.append(cc_data_ind[t_i])

for t_i in range(len(cb_data_ind)):
    if cb_date_conv[cb_data_ind[t_i]].month == 1:
        cb_ind_m01.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 2:
        cb_ind_m02.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 3:
        cb_ind_m03.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 4:
        cb_ind_m04.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 5:
        cb_ind_m05.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 6:
        cb_ind_m06.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 7:
        cb_ind_m07.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 8:
        cb_ind_m08.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 9:
        cb_ind_m09.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 10:
        cb_ind_m10.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 11:
        cb_ind_m11.append(cb_data_ind[t_i])
    if cb_date_conv[cb_data_ind[t_i]].month == 12:
        cb_ind_m12.append(cb_data_ind[t_i])

# find where depth = 0 to separate profiles
profile_ind = np.where(cc_data_depths==0)[0]

max_indices = max([profile_ind[i+1]-profile_ind[i] for i in range(len(profile_ind)-1)])

data_profiles = np.empty((len(profile_ind)-1,max_indices))
data_profiles.fill(np.nan)
depth_profiles = np.empty((len(profile_ind)-1,max_indices))
depth_profiles.fill(np.nan)
 
for p_i in range(len(data_profiles)):
    data_profiles[p_i,:len(data_var[profile_ind[p_i]:profile_ind[p_i+1]])] = data_var[profile_ind[p_i]:profile_ind[p_i+1]]
    depth_profiles[p_i,:len(data_depths[profile_ind[p_i]:profile_ind[p_i+1]])] = data_depths[profile_ind[p_i]:profile_ind[p_i+1]]

'''
