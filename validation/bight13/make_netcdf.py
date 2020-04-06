import numpy as np
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import datetime as dt

# station IDs
# 2903  LACSD ocean outfall (JWPC)
# 3053  LACSD Off-Outfall (northern current) 
# 3003  LACSD Off-Outfall (northern current) 
# 2803  LACSD Off-Outfall (southern current) 
# 2602  Long Beach Harbor Shelf (LA County) 
# 2205  OCSD Ocean Outfall 
# 2306  OCSD Off-Outfall (northern current) 
# 2103  OCSD Off-Outfall (southern current) 
# 1903  Orange County Southern Transect Line 
# CP1   Northern San Diego County- on shelf 
# CP2   Northern San Diego County- continental slope 
# SPOTS San Pedro Ocean Time Series (LA County Offshore)
# 9030  CALCOFI station 9030 (Orange County Offshore) 

station_IDs = [
'2903',
'3053',
'3003',
'2803',
'2602',
'2205',
'2306',
'2103',
'1903',
'CP1',
'CP2',
'SPOTS',
'9030']

lats_st = [
33.6985, 
33.73, 
33.7573, 
33.6685, 
33.694, 
33.5756, 
33.5812, 
33.5848, 
33.546, 
33.2154, 
33.1838, 
33.6067, 
33.4194]  

lons_st = [
-118.336,
-118.402,
-118.441,
-118.297,
-118.191,
-118.005,
-118.052,
-117.945,
-117.836,
-117.481,
-117.523,
-118.409,
-117.912]


time_units = 'days since 2014-08-25'

data_raw = pd.read_csv('ProcessStudiesFull_minna_edit.csv',header=None)

date_l = []
for d_i in range(len(data_raw[5][1:])):
    date_l.append(dt.datetime.strptime(data_raw[5][1+d_i],'%m/%d/%Y'))
date_arr = date2num(date_l,time_units)


lats_data = np.empty((len(data_raw[2][1:])))
lons_data = np.empty((len(data_raw[2][1:])))
for site in range(len(data_raw[2][1:])):
    for stat_ind in range(len(station_IDs)):
        if data_raw[2][site+1] == station_IDs[stat_ind]:
            lats_data[site] = lats_st[stat_ind]
            lons_data[site] = lons_st[stat_ind]

nitr_rate_df = np.array(data_raw[34][1:].astype(float))
depth_df = np.array(data_raw[8][1:].astype(float))

# find chlorophyll max depth indexes to assign primary production data
chl_ind = np.where(data_raw[7][1:]=='CHL max')[0]
pp_data = np.full(len(depth_df),np.nan)

# manually add primary production data from PP_ResR.xlsx to match order of station IDs 
# in ProcessStudiesFull.csv
pp_xl = [85.52,110.33,np.nan,132.87,122.11,np.nan,107.02,66.15,65.34,115.00, # summer 2014
    532.74,854.43,np.nan,884.14,1346.69,np.nan,483.39,903.71,990.33,2201.64, # spring 2015
    604.29,1097.07,np.nan,666.15,1186.54,np.nan,1093.11,1822.24,523.67,816.68, # summer 2015
    1199.69,118.23,np.nan,1206.37,129.75,np.nan,719.49,660.74,2842.17,1724.41] # spring 2016

pp_data[chl_ind] = pp_xl


# make netcdf

data_nc = Dataset('bight13.nc','w')
data_nc.title = 'SCCWRP Bight 13 Process Studies'
data_nc.description = '1-D data, each variable index matches with each other'

index = data_nc.createDimension('index',len(data_raw[2][1:]))

time_nc = data_nc.createVariable('time',np.float64,('index'))
lat_nc          = data_nc.createVariable('latitude',np.float32,('index'))
lon_nc          = data_nc.createVariable('longitude',np.float32,('index'))
depth_nc        = data_nc.createVariable('depth',np.float32,('index'))
nitr_nc         = data_nc.createVariable('nitr_rate',np.float32,('index'))
pp_nc         = data_nc.createVariable('NPP_rate',np.float32,('index'))

time_nc.units = time_units
lat_nc.units = 'degrees north'
lon_nc.units = 'degrees east'
depth_nc.units = 'm'
nitr_nc.units = 'nmol L-1 d-1'
nitr_nc.longname = 'nitrification rate'
pp_nc.units = 'mg C m-2 d-1'
pp_nc.longname = 'primary production rate'
pp_nc.description = 'integrated primary production over the euphotic zone with assumption that the euphotic zone is from the surface to the deep chlorophyll maximum'

time_nc[:] = date_arr
lat_nc[:]  = lats_data
lon_nc[:]  = lons_data
depth_nc[:] = depth_df
nitr_nc[:] = nitr_rate_df
pp_nc[:] = pp_data

data_nc.close()





