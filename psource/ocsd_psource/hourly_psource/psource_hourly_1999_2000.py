import numpy as np
import xarray as xr
from netCDF4 import num2date,date2num,Dataset
from datetime import datetime,timedelta

# read in psource data
filein = 'roms_psource.nc'
#fileout = 'roms_psource_hourly_1999_2000.nc'

filein_nc = xr.open_dataset(filein)


# read in ocsd hourly data
ocsd_hourly_path = '/data/project1/minnaho/potw_outfall_data/ocsd_hourly.nc'
ocsd_hourly_nc = Dataset(ocsd_hourly_path,'r')

# ocsd time units are 'hours since 1999-01-31 00:00'
ocsd_time = ocsd_hourly_nc.variables['time'].units
ocsd_st_dt = datetime(1999,1,31,0,0)
ocsd_en_dt = num2date(ocsd_hourly_nc.variables['time'].shape[0],ocsd_time)

ocsd_flow = np.array(ocsd_hourly_nc.variables['flow'])

# psrc time
time_unit_orig = 'days since 1994-1-1 00:00'
time_unit_hourly = 'hours since 1994-1-1 00:00'

# convert to datetime so can sample hourly
numtime = np.array(filein_nc['psrc_time'])
dt_time = num2date(numtime,time_unit_orig)

# edit unit to be right and assign datetime as psrc_time value
filein_nc['psrc_time'].attrs['units']= time_unit_orig
filein_nc['psrc_time'].values = dt_time
# resample data to hourly
hourly_nc = filein_nc.resample(psrc_time='1H').interpolate('linear')

# psrc_time goes from 1996-12-31 00:00 to 2016-03-02 00:00
dt_hourly = np.arange(datetime(1996,12,31,0,0),datetime(2016,3,2,1,0),timedelta(hours=1)).astype(datetime)
#num_hourly = date2num(dt_hourly,time_unit_hourly)
# make psrc_time value and units in days
num_hourly = date2num(dt_hourly,time_unit_orig)

# get date for 1999-12-31 23:00 and 2000-09-01 00:00
t1999 = dt_hourly[26303]
t2000 = dt_hourly[32160]
#subprocess.subprocess('ncea -d psrc_time,26303,32160 roms_psource_hourly.nc roms_psource_hourly_1999_2000.nc',shell=True)

hourly_nc['psrc_time'].values = num_hourly
hourly_nc['psrc_time'].attrs['units'] = time_unit_orig

# edit psource file to put hourly ocsd flows in correct times
# psource file has ocsd indices Nsrc 56 to 69

# ocsd start and end indices in psource file
st_in = np.where(dt_hourly==ocsd_st_dt)[0][0]
en_in = np.where(dt_hourly==ocsd_en_dt)[0][0]

# assign real hourly values to psource file
hourly_nc['Qbar'].values[56,st_in:en_in] = ocsd_flow*(5./14)
hourly_nc['Qbar'].values[62,st_in:en_in] = ocsd_flow*(5./14)

hourly_nc['Qbar'].values[60,st_in:en_in] = ocsd_flow*((1./2)/14) 
hourly_nc['Qbar'].values[65,st_in:en_in] = ocsd_flow*((1./2)/14) 
hourly_nc['Qbar'].values[63,st_in:en_in] = ocsd_flow*((1./2)/14) 
hourly_nc['Qbar'].values[66,st_in:en_in] = ocsd_flow*((1./2)/14) 
hourly_nc['Qbar'].values[61,st_in:en_in] = ocsd_flow*((1./2)/14) 
hourly_nc['Qbar'].values[58,st_in:en_in] = ocsd_flow*((1./2)/14) 

hourly_nc['Qbar'].values[59,st_in:en_in] = ocsd_flow*((1./6)/14) 
hourly_nc['Qbar'].values[64,st_in:en_in] = ocsd_flow*((1./6)/14) 
hourly_nc['Qbar'].values[57,st_in:en_in] = ocsd_flow*((1./6)/14) 
hourly_nc['Qbar'].values[69,st_in:en_in] = ocsd_flow*((1./6)/14) 
hourly_nc['Qbar'].values[68,st_in:en_in] = ocsd_flow*((1./6)/14) 
hourly_nc['Qbar'].values[67,st_in:en_in] = ocsd_flow*((1./6)/14) 

# write to new netcdf file
#hourly_nc.to_netcdf(fileout)
