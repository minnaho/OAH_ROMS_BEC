###################################################################
# read calcofi data and other data net primary production and nitrification
# compare to L2 model 1997-2000
# Nov 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
import scipy.io as sio
#plt.ion()

# cut off depth
bin_d = 5
d_e_30 = 35
d_e_40 = 45
d_e_50 = 55


##########################
# load observation data
#########################
# calcofi
text_file = pd.read_csv('calcofi_database.csv',header=None,low_memory=False,skiprows=1)
time_unit = 'minutes since 1949-03-01 09:30:00'
# choose variable
var_name0 = 'O2'
var_name1 = 'nitrif'
#cc_n_unit = 'mg C/m2/s' # npp
#cc_n_unit = 'mg C/m3' # chla
cc_n_unit = 'mmol/m3' # no3,nh3,o2
#cc_n_unit = 'C' # temp
r_n_unit  = 'mg N/m3/s'
cc_num = 22 # 16 is int prim prod (npp) (change npp_conv_o), 
            # 30 is no3, 31 is nh3, 25 is chla, 20 is temp, 22 is O2
sec_day = 86400
#npp_conv_o = (1./sec_day) # for npp
npp_conv_o = (1/.022391) # for O2
#npp_conv_o = 1. # umol/L = mmol/m3
cc_chl = 25


# rate data from Karen (bight 13 and from literature)
rate_name = '/data/project1/minnaho/validation/ValidationRateData_mh.xlsx'
nitr_rate_df = pd.read_excel(rate_name,sheet_name='Nitrification and nut uptake')
#growth_df = pd.read_excel(rate_name,sheet_name='growth and grazing')

# model data 2 1997- 9 2000
model_path = './extract_zslice/'

fig_path = './npp_nitrif_figs/'


# choose years
yr_s = 1999
yr_e = 2000

# calcofi convert datetime numbers to dates
cc_time_num = np.array((text_file.iloc[:,1]))
cc_date_conv = num2date(cc_time_num,time_unit)


st_dt = num2date(0,'days since 1999-9-01')
en_dt = num2date(0,'days since 2000-9-30')
# get indexes of target years
print('getting indices of target years')
cc_yr_ind_l = []
for ind_d,d_i in enumerate(cc_date_conv):
    if d_i < en_dt and d_i > st_dt:
        cc_yr_ind_l.append(ind_d) 

# get specific period
#cc_yr_ind = np.array((cc_yr_ind_l))
cc_yr_ind = np.arange(cc_date_conv.shape[0]) # get all data instead

#obs_path = './obs_outputs/y1999/' # change cc_yr_ind 
obs_path = './obs_outputs/'

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


##########
# calcofi and bight 13 data
##########
cc_lat = np.array((text_file.iloc[:,2]))
cc_lon = np.array((text_file.iloc[:,3]))

cc_lat_ind = np.where((cc_lat>lat_min) & (cc_lat<lat_max))[0]
cc_lon_ind = np.where((cc_lon>lon_min) & (cc_lon<lon_max))[0]

# find intersection of index values
cc_loc_ind = np.asarray((list(set(cc_lat_ind).intersection(cc_lon_ind))))
# find years and locations that we want
cc_data_ind = np.asarray(sorted((list(set(cc_loc_ind).intersection(cc_yr_ind)))))

# data variable
cc_data_var = np.array((text_file.iloc[:,cc_num][cc_data_ind]))
cc_data_chl = np.array((text_file.iloc[:,cc_chl][cc_data_ind]))

cc_t_ind = np.where(~np.isnan(cc_data_var))[0]
cc_data_slice_nobight = cc_data_var[cc_t_ind]
cc_data_lat_nobight = cc_lat[cc_data_ind][cc_t_ind]
cc_data_lon_nobight = cc_lon[cc_data_ind][cc_t_ind]
cc_loc_u_nobight = np.unique(np.array((cc_data_lat_nobight,cc_data_lon_nobight)).transpose(),axis=0)

cc_data_depth_nobight = np.array((text_file.iloc[:,19][cc_data_ind]))[cc_t_ind]

cc_data_date_nobight = cc_date_conv[cc_data_ind][cc_t_ind]

# find calcofi locations
#cc_x_coord = np.empty((len(cc_loc_u)))
#cc_y_coord = np.empty((len(cc_loc_u)))
#for l_i in range(len(cc_loc_u)):
#    min_l = np.abs( (lat_nc - cc_loc_u[l_i][0])**2 + (lon_nc - cc_loc_u[l_i][1])**2)
#    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
#    cc_x_coord[l_i] = x_site
#    cc_y_coord[l_i] = y_site

# bight 13 data NPP
bight_nc = Dataset('/data/project1/minnaho/validation/bight13/bight13.nc','r')
bight_d = np.array(bight_nc.variables['depth'])
bight_npp_ind = np.where(~np.isnan(bight_nc.variables['NPP_rate']))[0]

bight_t = num2date(np.array(bight_nc.variables['time']),bight_nc.variables['time'].units)[bight_npp_ind]
bight_dcm_depth = bight_d[bight_npp_ind]
bight_data_npp  = np.array(bight_nc.variables['NPP_rate'])[bight_npp_ind]
bight_lat = np.array(bight_nc.variables['latitude'])[bight_npp_ind]
bight_lon = np.array(bight_nc.variables['longitude'])[bight_npp_ind]

bight_loc_u = np.unique(np.array((bight_lat,bight_lon)).transpose(),axis=0)

# incorporate bight data to calcofi for large loop later
cc_data_slice = np.concatenate((cc_data_slice_nobight,bight_data_npp))
cc_data_lat = np.concatenate((cc_data_lat_nobight,bight_lat))
cc_data_lon = np.concatenate((cc_data_lon_nobight,bight_lon))
cc_loc_u = np.concatenate((cc_loc_u_nobight,bight_loc_u),axis=0)
cc_data_depth = np.concatenate((cc_data_depth_nobight,bight_dcm_depth))
cc_data_date = np.concatenate((cc_data_date_nobight,bight_t))

#plt.figure()
#plt.imshow(mask_nc,origin='lower')
#plt.scatter(cc_x_coord,cc_y_coord)

##########
# validationratedata
##########

r_lat = np.array(nitr_rate_df['Lat'])
r_lon = np.array(nitr_rate_df['Lon'])

r_lat_ind = np.where((r_lat>lat_min) & (r_lat<lat_max))[0]
r_lon_ind = np.where((r_lon>lon_min) & (r_lon<lon_max))[0]

r_loc_ind = np.asarray((list(set(r_lat_ind).intersection(r_lon_ind))))
#r_data_ind = np.asarray(sorted((list(set(r_loc_ind).intersection(rate_yr_ind)))))

r_depth = np.array(nitr_rate_df['Depth'])[r_loc_ind]
r_data  = np.array(nitr_rate_df['NitrRate'])[r_loc_ind]

r_lat_data = np.array(r_lat[r_loc_ind])
r_lon_data = np.array(r_lon[r_loc_ind])
r_date_data = pd.to_datetime(nitr_rate_df['Date'])[r_loc_ind]

r_loc_u = np.unique(np.array((r_lat_data,r_lon_data)).transpose(),axis=0)

# find rate data locations
r_x_coord = np.empty((len(r_loc_u)))
r_y_coord = np.empty((len(r_loc_u)))
for l_i in range(len(r_loc_u)):
    min_l = np.abs( (lat_nc - r_loc_u[l_i][0])**2 + (lon_nc - r_loc_u[l_i][1])**2)
    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
    r_x_coord[l_i] = x_site
    r_y_coord[l_i] = y_site

#########################
# statistics and analyses
#########################
# nitrification rate data
r_spring_ind_l = []
r_winter_ind_l = []
r_summer_ind_l = []
r_fall_ind_l = []

for d_i,pd_i in enumerate(r_date_data):
    m = pd_i.month
    if m == 12 or m == 1 or m == 2:
        r_winter_ind_l.append(d_i)
    if m == 3 or m == 4 or m == 5:
        r_spring_ind_l.append(d_i)
    if m == 6 or m == 7 or m == 8:
        r_summer_ind_l.append(d_i)
    if m == 9 or m == 10 or m == 11:
        r_fall_ind_l.append(d_i)

r_spring_ind = np.array(r_spring_ind_l)
r_winter_ind = np.array(r_winter_ind_l)
r_summer_ind = np.array(r_summer_ind_l)
r_fall_ind   = np.array(r_fall_ind_l)

#r_ind_00 = np.where((r_depth<10)&(r_depth>0))[0]
r_ind_03 = np.where((r_depth<=30)&(r_depth>=0))[0]
r_ind_45 = np.where((r_depth<=45)&(r_depth>30))[0]
r_ind_46 = np.where((r_depth<=60)&(r_depth>45))[0]
r_ind_00 = np.where((r_depth<=5+bin_d)&(r_depth>5-bin_d))[0]
r_ind_10 = np.where((r_depth<=15+bin_d)&(r_depth>15-bin_d))[0]
r_ind_20 = np.where((r_depth<=25+bin_d)&(r_depth>25-bin_d))[0]
r_ind_30 = np.where((r_depth<=d_e_30+bin_d)&(r_depth>d_e_30-bin_d))[0]
r_ind_40 = np.where((r_depth<=d_e_40+bin_d)&(r_depth>d_e_40-bin_d))[0]
r_ind_50 = np.where((r_depth<=d_e_50+bin_d)&(r_depth>d_e_50-bin_d))[0]
r_ind_60 = np.where((r_depth<=65+bin_d)&(r_depth>65-bin_d))[0]
r_ind_70 = np.where((r_depth<=75+bin_d)&(r_depth>75-bin_d))[0]
r_ind_80 = np.where((r_depth<=85+bin_d)&(r_depth>85-bin_d))[0]
r_ind_90 = np.where((r_depth<=95+bin_d)&(r_depth>95-bin_d))[0]

r_spring_03_ind = np.asarray((list(set(r_ind_03).intersection(r_spring_ind))))
r_winter_03_ind = np.asarray((list(set(r_ind_03).intersection(r_winter_ind))))
r_summer_03_ind = np.asarray((list(set(r_ind_03).intersection(r_summer_ind))))
r_fall_03_ind   = np.asarray((list(set(r_ind_03).intersection(r_fall_ind))))

r_spring_45_ind = np.asarray((list(set(r_ind_45).intersection(r_spring_ind))))
r_winter_45_ind = np.asarray((list(set(r_ind_45).intersection(r_winter_ind))))
r_summer_45_ind = np.asarray((list(set(r_ind_45).intersection(r_summer_ind))))
r_fall_45_ind   = np.asarray((list(set(r_ind_45).intersection(r_fall_ind))))

r_spring_46_ind = np.asarray((list(set(r_ind_46).intersection(r_spring_ind))))
r_winter_46_ind = np.asarray((list(set(r_ind_46).intersection(r_winter_ind))))
r_summer_46_ind = np.asarray((list(set(r_ind_46).intersection(r_summer_ind))))
r_fall_46_ind   = np.asarray((list(set(r_ind_46).intersection(r_fall_ind))))

r_spring_00_ind = np.asarray((list(set(r_ind_00).intersection(r_spring_ind))))
r_winter_00_ind = np.asarray((list(set(r_ind_00).intersection(r_winter_ind))))
r_summer_00_ind = np.asarray((list(set(r_ind_00).intersection(r_summer_ind))))
r_fall_00_ind = np.asarray((list(set(r_ind_00).intersection(r_fall_ind))))

r_spring_10_ind = np.asarray((list(set(r_ind_10).intersection(r_spring_ind))))
r_winter_10_ind = np.asarray((list(set(r_ind_10).intersection(r_winter_ind))))
r_summer_10_ind = np.asarray((list(set(r_ind_10).intersection(r_summer_ind))))
r_fall_10_ind = np.asarray((list(set(r_ind_10).intersection(r_fall_ind))))

r_spring_20_ind = np.asarray((list(set(r_ind_20).intersection(r_spring_ind))))
r_winter_20_ind = np.asarray((list(set(r_ind_20).intersection(r_winter_ind))))
r_summer_20_ind = np.asarray((list(set(r_ind_20).intersection(r_summer_ind))))
r_fall_20_ind = np.asarray((list(set(r_ind_20).intersection(r_fall_ind))))

r_spring_30_ind = np.asarray((list(set(r_ind_30).intersection(r_spring_ind))))
r_winter_30_ind = np.asarray((list(set(r_ind_30).intersection(r_winter_ind))))
r_summer_30_ind = np.asarray((list(set(r_ind_30).intersection(r_summer_ind))))
r_fall_30_ind = np.asarray((list(set(r_ind_30).intersection(r_fall_ind))))

r_spring_40_ind = np.asarray((list(set(r_ind_40).intersection(r_spring_ind))))
r_winter_40_ind = np.asarray((list(set(r_ind_40).intersection(r_winter_ind))))
r_summer_40_ind = np.asarray((list(set(r_ind_40).intersection(r_summer_ind))))
r_fall_40_ind = np.asarray((list(set(r_ind_40).intersection(r_fall_ind))))

r_spring_50_ind = np.asarray((list(set(r_ind_50).intersection(r_spring_ind))))
r_winter_50_ind = np.asarray((list(set(r_ind_50).intersection(r_winter_ind))))
r_summer_50_ind = np.asarray((list(set(r_ind_50).intersection(r_summer_ind))))
r_fall_50_ind = np.asarray((list(set(r_ind_50).intersection(r_fall_ind))))

r_spring_60_ind = np.asarray((list(set(r_ind_60).intersection(r_spring_ind))))
r_winter_60_ind = np.asarray((list(set(r_ind_60).intersection(r_winter_ind))))
r_summer_60_ind = np.asarray((list(set(r_ind_60).intersection(r_summer_ind))))
r_fall_60_ind = np.asarray((list(set(r_ind_60).intersection(r_fall_ind))))

r_spring_70_ind = np.asarray((list(set(r_ind_70).intersection(r_spring_ind))))
r_winter_70_ind = np.asarray((list(set(r_ind_70).intersection(r_winter_ind))))
r_summer_70_ind = np.asarray((list(set(r_ind_70).intersection(r_summer_ind))))
r_fall_70_ind   = np.asarray((list(set(r_ind_70).intersection(r_fall_ind))))

r_spring_80_ind = np.asarray((list(set(r_ind_80).intersection(r_spring_ind))))
r_winter_80_ind = np.asarray((list(set(r_ind_80).intersection(r_winter_ind))))
r_summer_80_ind = np.asarray((list(set(r_ind_80).intersection(r_summer_ind))))
r_fall_80_ind   = np.asarray((list(set(r_ind_80).intersection(r_fall_ind))))

r_spring_90_ind = np.asarray((list(set(r_ind_90).intersection(r_spring_ind))))
r_winter_90_ind = np.asarray((list(set(r_ind_90).intersection(r_winter_ind))))
r_summer_90_ind = np.asarray((list(set(r_ind_90).intersection(r_summer_ind))))
r_fall_90_ind   = np.asarray((list(set(r_ind_90).intersection(r_fall_ind))))

# integrated primary productivity data calcofi
cc_spring_ind_l = []
cc_winter_ind_l = []
cc_summer_ind_l = []
cc_fall_ind_l = []

for d_i in range(len(cc_data_date)):
    m = cc_data_date[d_i].month
    if m == 12 or m == 1 or m == 2:
        cc_winter_ind_l.append(d_i)
    if m == 3 or m == 4 or m == 5:
        cc_spring_ind_l.append(d_i)
    if m == 6 or m == 7 or m == 8:
        cc_summer_ind_l.append(d_i)
    if m == 9 or m == 10 or m == 11:
        cc_fall_ind_l.append(d_i)

cc_spring_ind = np.array(cc_spring_ind_l)
cc_winter_ind = np.array(cc_winter_ind_l)
cc_summer_ind = np.array(cc_summer_ind_l)
cc_fall_ind   = np.array(cc_fall_ind_l)

cc_ind_03 = np.where((cc_data_depth<=30)&(cc_data_depth>=0))[0]
cc_ind_45 = np.where((cc_data_depth<=45)&(cc_data_depth>30))[0]
cc_ind_46 = np.where((cc_data_depth<=60)&(cc_data_depth>45))[0]
cc_ind_00 = np.where((cc_data_depth<=5+bin_d)&(cc_data_depth>5-bin_d))[0]
cc_ind_10 = np.where((cc_data_depth<=15+bin_d)&(cc_data_depth>15-bin_d))[0]
cc_ind_20 = np.where((cc_data_depth<=25+bin_d)&(cc_data_depth>25-bin_d))[0]
cc_ind_30 = np.where((cc_data_depth<=d_e_30+bin_d)&(cc_data_depth>d_e_30-bin_d))[0]
cc_ind_40 = np.where((cc_data_depth<=d_e_40+bin_d)&(cc_data_depth>d_e_40-bin_d))[0]
cc_ind_45 = np.where((cc_data_depth<=45)&(cc_data_depth>30))[0]
cc_ind_50 = np.where((cc_data_depth<=d_e_50+bin_d)&(cc_data_depth>d_e_50-bin_d))[0]
cc_ind_60 = np.where((cc_data_depth<=65+bin_d)&(cc_data_depth>65-bin_d))[0]
cc_ind_70 = np.where((cc_data_depth<=75+bin_d)&(cc_data_depth>75-bin_d))[0]
cc_ind_80 = np.where((cc_data_depth<=85+bin_d)&(cc_data_depth>85-bin_d))[0]
cc_ind_90 = np.where((cc_data_depth<=95+bin_d)&(cc_data_depth>95-bin_d))[0]

cc_spring_03_ind = np.asarray((list(set(cc_ind_03).intersection(cc_spring_ind))))
cc_winter_03_ind = np.asarray((list(set(cc_ind_03).intersection(cc_winter_ind))))
cc_summer_03_ind = np.asarray((list(set(cc_ind_03).intersection(cc_summer_ind))))
cc_fall_03_ind   = np.asarray((list(set(cc_ind_03).intersection(cc_fall_ind))))

cc_spring_45_ind = np.asarray((list(set(cc_ind_45).intersection(cc_spring_ind))))
cc_winter_45_ind = np.asarray((list(set(cc_ind_45).intersection(cc_winter_ind))))
cc_summer_45_ind = np.asarray((list(set(cc_ind_45).intersection(cc_summer_ind))))
cc_fall_45_ind   = np.asarray((list(set(cc_ind_45).intersection(cc_fall_ind))))

cc_spring_46_ind = np.asarray((list(set(cc_ind_46).intersection(cc_spring_ind))))
cc_winter_46_ind = np.asarray((list(set(cc_ind_46).intersection(cc_winter_ind))))
cc_summer_46_ind = np.asarray((list(set(cc_ind_46).intersection(cc_summer_ind))))
cc_fall_46_ind   = np.asarray((list(set(cc_ind_46).intersection(cc_fall_ind))))

cc_spring_00_ind = np.asarray((list(set(cc_ind_00).intersection(cc_spring_ind))))
cc_winter_00_ind = np.asarray((list(set(cc_ind_00).intersection(cc_winter_ind))))
cc_summer_00_ind = np.asarray((list(set(cc_ind_00).intersection(cc_summer_ind))))
cc_fall_00_ind   = np.asarray((list(set(cc_ind_00).intersection(cc_fall_ind))))

cc_spring_10_ind = np.asarray((list(set(cc_ind_10).intersection(cc_spring_ind))))
cc_winter_10_ind = np.asarray((list(set(cc_ind_10).intersection(cc_winter_ind))))
cc_summer_10_ind = np.asarray((list(set(cc_ind_10).intersection(cc_summer_ind))))
cc_fall_10_ind   = np.asarray((list(set(cc_ind_10).intersection(cc_fall_ind))))

cc_spring_20_ind = np.asarray((list(set(cc_ind_20).intersection(cc_spring_ind))))
cc_winter_20_ind = np.asarray((list(set(cc_ind_20).intersection(cc_winter_ind))))
cc_summer_20_ind = np.asarray((list(set(cc_ind_20).intersection(cc_summer_ind))))
cc_fall_20_ind   = np.asarray((list(set(cc_ind_20).intersection(cc_fall_ind))))

cc_spring_30_ind = np.asarray((list(set(cc_ind_30).intersection(cc_spring_ind))))
cc_winter_30_ind = np.asarray((list(set(cc_ind_30).intersection(cc_winter_ind))))
cc_summer_30_ind = np.asarray((list(set(cc_ind_30).intersection(cc_summer_ind))))
cc_fall_30_ind   = np.asarray((list(set(cc_ind_30).intersection(cc_fall_ind))))

cc_spring_40_ind = np.asarray((list(set(cc_ind_40).intersection(cc_spring_ind))))
cc_winter_40_ind = np.asarray((list(set(cc_ind_40).intersection(cc_winter_ind))))
cc_summer_40_ind = np.asarray((list(set(cc_ind_40).intersection(cc_summer_ind))))
cc_fall_40_ind   = np.asarray((list(set(cc_ind_40).intersection(cc_fall_ind))))

cc_spring_50_ind = np.asarray((list(set(cc_ind_50).intersection(cc_spring_ind))))
cc_winter_50_ind = np.asarray((list(set(cc_ind_50).intersection(cc_winter_ind))))
cc_summer_50_ind = np.asarray((list(set(cc_ind_50).intersection(cc_summer_ind))))
cc_fall_50_ind   = np.asarray((list(set(cc_ind_50).intersection(cc_fall_ind))))

cc_spring_60_ind = np.asarray((list(set(cc_ind_60).intersection(cc_spring_ind))))
cc_winter_60_ind = np.asarray((list(set(cc_ind_60).intersection(cc_winter_ind))))
cc_summer_60_ind = np.asarray((list(set(cc_ind_60).intersection(cc_summer_ind))))
cc_fall_60_ind   = np.asarray((list(set(cc_ind_60).intersection(cc_fall_ind))))

cc_spring_70_ind = np.asarray((list(set(cc_ind_70).intersection(cc_spring_ind))))
cc_winter_70_ind = np.asarray((list(set(cc_ind_70).intersection(cc_winter_ind))))
cc_summer_70_ind = np.asarray((list(set(cc_ind_70).intersection(cc_summer_ind))))
cc_fall_70_ind   = np.asarray((list(set(cc_ind_70).intersection(cc_fall_ind))))

cc_spring_80_ind = np.asarray((list(set(cc_ind_80).intersection(cc_spring_ind))))
cc_winter_80_ind = np.asarray((list(set(cc_ind_80).intersection(cc_winter_ind))))
cc_summer_80_ind = np.asarray((list(set(cc_ind_80).intersection(cc_summer_ind))))
cc_fall_80_ind   = np.asarray((list(set(cc_ind_80).intersection(cc_fall_ind))))

cc_spring_90_ind = np.asarray((list(set(cc_ind_90).intersection(cc_spring_ind))))
cc_winter_90_ind = np.asarray((list(set(cc_ind_90).intersection(cc_winter_ind))))
cc_summer_90_ind = np.asarray((list(set(cc_ind_90).intersection(cc_summer_ind))))
cc_fall_90_ind   = np.asarray((list(set(cc_ind_90).intersection(cc_fall_ind))))

################
# model data and plotting
################
c_conv = 12
n_conv  = 14
npp_conv_m = c_conv # mmol/m3/s to mg C/m2/s
#nit_conv = (1./sec_day)*(1./1000) # nmol/L/day to mmol/m3/s
nit_conv_o = (1./sec_day)*(1./1000)*n_conv # nmol/L/day to mg N/m3/s
nit_conv_m = n_conv

h_plot = 9
w_plot = 16
axistick = 14

nit_cmap = 'gnuplot'
npp_cmap = 'viridis'

axis_tick_size = 14
axis_font = 16
m_size = 200

min_c = 0
max_c = 0.004

min_r = 0
max_r = 10E-6

# basemap
lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)

parallels = np.arange(0,90,1)
meridians = np.arange(180,360,1)

################
# plotting
################
# observation data
num_vars_c = [
cc_spring_03_ind,
cc_spring_45_ind,
cc_spring_46_ind,
cc_spring_00_ind, 
cc_spring_10_ind, 
cc_spring_20_ind, 
cc_spring_30_ind,
cc_spring_40_ind,
cc_spring_50_ind,
cc_spring_60_ind,
cc_spring_70_ind,
cc_spring_80_ind,
cc_spring_90_ind,

cc_winter_03_ind,
cc_winter_45_ind,
cc_winter_46_ind,
cc_winter_00_ind,
cc_winter_10_ind,
cc_winter_20_ind,
cc_winter_30_ind,
cc_winter_40_ind,
cc_winter_50_ind,
cc_winter_60_ind,
cc_winter_70_ind,
cc_winter_80_ind,
cc_winter_90_ind,

cc_summer_03_ind,
cc_summer_45_ind,
cc_summer_46_ind,
cc_summer_00_ind,
cc_summer_10_ind,
cc_summer_20_ind,
cc_summer_30_ind,
cc_summer_40_ind,
cc_summer_50_ind,
cc_summer_60_ind,
cc_summer_70_ind,
cc_summer_80_ind,
cc_summer_90_ind,

cc_fall_03_ind,  
cc_fall_45_ind, 
cc_fall_46_ind,  
cc_fall_00_ind,
cc_fall_10_ind,
cc_fall_20_ind,
cc_fall_30_ind, 
cc_fall_40_ind, 
cc_fall_50_ind,
cc_fall_60_ind,
cc_fall_70_ind,
cc_fall_80_ind,
cc_fall_90_ind]

num_vars_r = [
r_spring_03_ind,
r_spring_45_ind,
r_spring_46_ind,
r_spring_00_ind, 
r_spring_10_ind, 
r_spring_20_ind, 
r_spring_30_ind,
r_spring_40_ind,
r_spring_50_ind,
r_spring_60_ind,
r_spring_70_ind,
r_spring_80_ind,
r_spring_90_ind,

r_winter_03_ind,
r_winter_45_ind,
r_winter_46_ind,
r_winter_00_ind,
r_winter_10_ind,
r_winter_20_ind,
r_winter_30_ind,
r_winter_40_ind,
r_winter_50_ind,
r_winter_60_ind,
r_winter_70_ind,
r_winter_80_ind,
r_winter_90_ind,

r_summer_03_ind,
r_summer_45_ind,
r_summer_46_ind,
r_summer_00_ind,
r_summer_10_ind,
r_summer_20_ind,
r_summer_30_ind,
r_summer_40_ind,
r_summer_50_ind,
r_summer_60_ind,
r_summer_70_ind,
r_summer_80_ind,
r_summer_90_ind,

r_fall_03_ind,  
r_fall_45_ind, 
r_fall_46_ind,  
r_fall_00_ind,
r_fall_10_ind,
r_fall_20_ind,
r_fall_30_ind, 
r_fall_40_ind, 
r_fall_50_ind,
r_fall_60_ind,
r_fall_70_ind,
r_fall_80_ind,
r_fall_90_ind]

# number of depth slices
m_depths = ['_0_30','_30_45','_45_60','_surf','_10','_20','_30','_40','_50','_60','_70','_80','_90']

npp_list = []
nit_list = []

for n_i in range(len(num_vars_c)):
    # observation data
    if num_vars_c[n_i].shape[0]==0:
        npp_obs = []
        lat_c = []
        lon_c = []
    else:
        npp_obs = []
        lat_c = []
        lon_c = []
        lat_temp = cc_data_lat[num_vars_c[n_i]]
        lon_temp = cc_data_lon[num_vars_c[n_i]]
        # get average value at each location and depth range
        for l_c in range(len(cc_loc_u)):
            loc_c = np.where((lat_temp==cc_loc_u[l_c][0])&(lon_temp==cc_loc_u[l_c][1]))[0]
            npp_app = np.nanmean(cc_data_slice[num_vars_c[n_i]][loc_c]*npp_conv_o)
            npp_obs.append(npp_app)
            lat_c.append(cc_loc_u[l_c][0])
            lon_c.append(cc_loc_u[l_c][1])

    if num_vars_r[n_i].shape[0]==0:
        nit_obs = []
        lat_r = []
        lon_r = []
    else:
        nit_obs = []
        lat_r = []
        lon_r = []
        lat_temp = r_lat_data[num_vars_r[n_i]]
        lon_temp = r_lon_data[num_vars_r[n_i]]
        # get average value at each location and depth range
        for l_r in range(len(r_loc_u)):
            loc_r = np.where((lat_temp==r_loc_u[l_r][0])&(lon_temp==r_loc_u[l_r][1]))[0]
            nit_app = np.nanmean(r_data[num_vars_r[n_i]][loc_r]*nit_conv_o)
            nit_obs.append(nit_app)
            lat_r.append(r_loc_u[l_r][0])
            lon_r.append(r_loc_u[l_r][1])

    if n_i<len(m_depths):
        season_str = 'spring'
    if n_i<(len(m_depths)*2) and n_i>=len(m_depths):     
        season_str = 'winter'
    if n_i<(len(m_depths)*3) and n_i>=(len(m_depths)*2):     
        season_str = 'summer'
    if n_i<(len(m_depths)*4) and n_i>=(len(m_depths)*3):     
        season_str = 'fall'
    depth_str = m_depths[n_i%len(m_depths)]
    var0_dict = {'lat':lat_c,'lon':lon_c,'var':npp_obs,'unit':cc_n_unit}
#    var1_dict = {'lat':lat_r,'lon':lon_r,'var':nit_obs,'unit':r_n_unit}
    sio.savemat(obs_path+var_name0+'_'+season_str+depth_str+'.mat',var0_dict)
#    sio.savemat(obs_path+var_name1+'_'+season_str+depth_str+'.mat',var1_dict)

