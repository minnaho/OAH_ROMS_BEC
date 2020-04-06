import numpy as np
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import datetime as dt

df_raw = pd.read_excel('ocsd_1km_CTD.xlsx',header=None,skiprows=1)

date_str = np.array(df_raw[0].astype(str))
hr_str = np.array(df_raw[1].astype(str))

date_l = []
for d_i in range(len(date_str)):
    date_l.append(dt.datetime.strptime(date_str[d_i]+hr_str[d_i],'%Y-%m-%d%H:%M:%S'))

date_arr = np.array(date_l)
time_unit = 'minutes since 2002-10-22 11:06'

time_num = date2num(date_arr,time_unit)

site1_ind = [] 
site2_ind = [] 
site3_ind = [] 
site4_ind = [] 
site5_ind = [] 
site6_ind = [] 
site7_ind = [] 
site8_ind = [] 
site9_ind = [] 

sites_lat = [33.57186,33.57061,33.56930,33.57365,33.57495,33.57621,33.58056,33.57935,33.57801]
sites_lon = [-118.01155,-118.00545,-117.99936,-117.99808,-118.00418,-118.01025,-118.00895,-118.00288,-117.99685]

lats_df = []
lons_df = []
for data_i in range(len(df_raw[2])):
    if df_raw[2][data_i] == 'DS-1':
        lats_df.append(sites_lat[0])
        lons_df.append(sites_lon[0])
    if df_raw[2][data_i] == 'DS-2':
        lats_df.append(sites_lat[1])
        lons_df.append(sites_lon[1])
    if df_raw[2][data_i] == 'DS-3':
        lats_df.append(sites_lat[2])
        lons_df.append(sites_lon[2])
    if df_raw[2][data_i] == 'DS-4':
        lats_df.append(sites_lat[3])
        lons_df.append(sites_lon[3])
    if df_raw[2][data_i] == 'DS-5':
        lats_df.append(sites_lat[4])
        lons_df.append(sites_lon[4])
    if df_raw[2][data_i] == 'DS-6':
        lats_df.append(sites_lat[5])
        lons_df.append(sites_lon[5])
    if df_raw[2][data_i] == 'DS-7':
        lats_df.append(sites_lat[6])
        lons_df.append(sites_lon[6])
    if df_raw[2][data_i] == 'DS-8':
        lats_df.append(sites_lat[7])
        lons_df.append(sites_lon[7])
    if df_raw[2][data_i] == 'DS-9':
        lats_df.append(sites_lat[8])
        lons_df.append(sites_lon[8])

lats_arr = np.array(lats_df)
lons_arr = np.array(lons_df)

# size is time, locations (sites), depths (maximum is 67 m with 1 m frequency)            
temp_df = np.array(df_raw[7])
dens_df = np.array(df_raw[8])
salt_df = np.array(df_raw[9])
pH_df = np.array(df_raw[10])
oxygen_df = np.array(df_raw[11])
oxygen_sat_df = np.array(df_raw[12])
beamc_df = np.array(df_raw[15])
chl_df = np.array(df_raw[16])
NH3_df = np.array(df_raw[18])
coliform_df = np.array(df_raw[20])
depth_df = np.array(df_raw[3])

########################
# make netCDF
########################
nc_file = Dataset('ocsd_1km_grid_CTD.nc','w')
nc_file.title = '9 CTD moorings 1 km apart around OCSD pipe'
nc_file.source = 'George Robertson, OCSD scientist'
nc_file.description = '1D data (index of each measurement matches index of time/lat/lon/depth'

index_nc = nc_file.createDimension('index',time_num.shape[0])

time_nc = nc_file.createVariable('time',np.float32,('index'))
lat_nc = nc_file.createVariable('latitude',np.float32,('index'))
lon_nc = nc_file.createVariable('longitude',np.float32,('index'))
depth_nc = nc_file.createVariable('depth',np.float32,('index'))
temp_nc = nc_file.createVariable('temp',np.float32,('index'))
dens_nc = nc_file.createVariable('density',np.float32,('index'))
salt_nc =nc_file.createVariable('salinity',np.float32,('index')) 
pH_nc = nc_file.createVariable('pH',np.float32,('index'))
oxygen_nc =nc_file.createVariable('oxygen',np.float32,('index')) 
oxygen_sat_nc = nc_file.createVariable('oxygen_saturation',np.float32,('index'))
beamc_nc = nc_file.createVariable('beam_c',np.float32,('index'))
chl_nc =nc_file.createVariable('Chl-a',np.float32,('index'))
NH3_nc =nc_file.createVariable('ammonia-N',np.float32,('index')) 
coliform_nc =nc_file.createVariable('total_coliforms',np.float32,('index'))

time_nc[:]  = time_num
lat_nc[:]   = lats_arr
lon_nc[:]   = lons_arr
depth_nc[:] = depth_df
temp_nc[:]  = temp_df
dens_nc[:]  = dens_df
salt_nc[:]  = salt_df
pH_nc[:]    = pH_df
oxygen_nc[:] = oxygen_df
oxygen_sat_nc[:] = oxygen_sat_df
beamc_nc[:] = beamc_df
chl_nc[:] = chl_df
NH3_nc[:] = NH3_df
coliform_nc[:] = coliform_df

time_nc.units = time_unit
lat_nc.units = 'degrees north'
lon_nc.units = 'degrees east'
depth_nc.units = 'meter'
temp_nc.units = 'degrees C'
dens_nc.units = 'kg m-3'
salt_nc.units = 'PSU'
oxygen_nc.units = 'mg/L'
oxygen_sat_nc.units = 'mg/L'
beamc_nc.units = '1/m'
chl_nc.units = 'ug/L'
chl_nc.longname = 'chlorophyll-a'
NH3_nc.units = 'mg/L'
coliform_nc.units = 'MPN/100mL'

nc_file.close()
