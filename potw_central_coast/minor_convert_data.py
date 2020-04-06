import pandas as pd
from netCDF4 import Dataset,date2num
import time
import numpy as np

data_xl = pd.ExcelFile('potw_central_mh.xlsx')
sheetnames = data_xl.sheet_names

rem = 1 # sheets to remove from total (1st is metadata)

data_lat = np.empty((len(sheetnames)-rem))
data_lon = np.empty((len(sheetnames)-rem))
data_dep = np.empty((len(sheetnames)-rem))
data_flo = np.empty((12,len(sheetnames)-rem))
data_temp = np.empty((12,len(sheetnames)-rem))
data_salt = np.empty((12,len(sheetnames)-rem))
data_turb = np.empty((12,len(sheetnames)-rem))
data_tss = np.empty((12,len(sheetnames)-rem))
data_pH = np.empty((12,len(sheetnames)-rem))
data_nh3 = np.empty((12,len(sheetnames)-rem))
data_bod = np.empty((12,len(sheetnames)-rem))

fill = np.nan
for s_i in range(rem,len(sheetnames)):
    df = data_xl.parse(sheetnames[s_i],header=None)
    data_lat[s_i-rem] = df[3][1]
    data_lon[s_i-rem] = df[4][1]
    data_dep[s_i-rem] = df[5][1]
    for d_i in range(len(df[0])-1):
        if df[1][d_i+1] == 'ND':
            df[1][d_i+1] = fill
            data_flo[d_i,s_i-rem]  = df[1][d_i+1]
        else:
            data_flo[d_i,s_i-rem]  = df[1][d_i+1]
        if df[8][d_i+1] == 'ND':
            df[8][d_i+1] = fill
            data_temp[d_i,s_i-rem] = df[8][d_i+1]
        else:
            data_temp[d_i,s_i-rem] = df[8][d_i+1]
        if df[11][d_i+1] == 'ND':
            df[11][d_i+1] = fill
            data_salt[d_i,s_i-rem] = df[11][d_i+1]
        else:
            data_salt[d_i,s_i-rem] = df[11][d_i+1]
        if df[7][d_i+1] == 'ND':
            df[7][d_i+1] = fill
            data_turb[d_i,s_i-rem] = df[7][d_i+1]
        else:
            data_turb[d_i,s_i-rem] = df[7][d_i+1]
        if df[6][d_i+1] == 'ND':
            df[6][d_i+1] = fill
            data_tss[d_i,s_i-rem]  = df[6][d_i+1]
        else:
            data_tss[d_i,s_i-rem]  = df[6][d_i+1]
        if df[9][d_i+1] == 'ND':
            df[9][d_i+1] = fill
            data_pH[d_i,s_i-rem]   = df[9][d_i+1]
        else:
            data_pH[d_i,s_i-rem]   = df[9][d_i+1]
        if df[10][d_i+1] == 'ND':
            df[10][d_i+1] = fill
            data_nh3[d_i,s_i-rem]  = df[10][d_i+1]
        else:
            data_nh3[d_i,s_i-rem]  = df[10][d_i+1]
        if df[12][d_i+1] == 'ND':
            df[12][d_i+1] = fill
            data_bod[d_i,s_i-rem]  = df[12][d_i+1]
        else:
            data_bod[d_i,s_i-rem]  = df[12][d_i+1]

date_unit = 'days since 2015-01-01' 
data_time = date2num(np.array(df[0][1:]),date_unit)


# convert mg/L to mmol/m3
data_nh3_c = data_nh3*1000*(1./14) # N mmol/m3
data_bod_c = data_bod*1000*(1./12) # C mmol/m3

# make netcdf
dataset = Dataset('minor_potw_central_coast.nc','w')
dataset.title = 'Minor POTWs between Point Conception and San Francisco Bay'
dataset.source = 'Heal the Ocean Outfall Database'
dataset.history = 'Created '+time.ctime(time.time())
dataset.description = 'Pismo Beach, South San Luis Obispo County, Avila Beach, Morro Bay, San Simeon, Ragged Point, Carmel Area, Monterey Area, Watsonville, Santa Cruz, Halfmoon Bay (SAM), SF Oceanside, North San Mateo (Daly City), Mendocino County (Anchor Bay)'
#dataset.description = 'Pismo Beach, South San Luis Obispo County, Avila Beach, Morro Bay, San Simeon, Ragged Point, Carmel Area, Monterey Area, Watsonville, Santa Cruz, Halfmoon Bay (SAM), North San Mateo (Daly City), Mendocino County (Anchor Bay)'

# dimensions
time_d = dataset.createDimension('time',None)
loc_d = dataset.createDimension('location',data_lat.shape[0])

# variables
time_v = dataset.createVariable('time',np.float64,('time'))
lat_v = dataset.createVariable('latitude',np.float32,('location'))
lon_v = dataset.createVariable('longitude',np.float32,('location'))
dep_v = dataset.createVariable('depth',np.float32,('location'))

flo_v  = dataset.createVariable('flow',np.float32,('time','location'))
temp_v = dataset.createVariable('temp',np.float32,('time','location'))
salt_v = dataset.createVariable('salt',np.float32,('time','location'))
nh3_v  = dataset.createVariable('nh3',np.float32,('time','location'))
pH_v   = dataset.createVariable('pH',np.float32,('time','location'))
turb_v = dataset.createVariable('turbidity',np.float32,('time','location'))
tss_v  = dataset.createVariable('TSS',np.float32,('time','location'))
bod_v  = dataset.createVariable('bod',np.float32,('time','location'))

time_v[:] = data_time
lat_v[:] = data_lat
lon_v[:] = data_lon
dep_v[:] = data_dep
flo_v[:,:] = data_flo
temp_v[:,:]  = data_temp 
salt_v[:,:]  = data_salt 
nh3_v[:,:]   = data_nh3_c
pH_v[:,:]    = data_pH
turb_v[:,:]  = data_turb
tss_v[:,:]   = data_tss
bod_v[:,:]   = data_bod_c

time_v.units = date_unit
dep_v.units = 'm'
flo_v.units = 'm3 s-1'
temp_v.units = 'C'
salt_v.units = 'PSU'
nh3_v.units = 'mmol m-3'
turb_v.units = 'NTU'
tss_v.units = 'mg L-1'
bod_v.units = 'mmol C m-3'

dataset.close()
