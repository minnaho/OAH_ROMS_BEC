###################################
# concatenate all OCSD mooring data
# also make netCDF 1D
###################################
import numpy as np
from netCDF4 import Dataset,num2date,date2num

m18 = Dataset('OCSD_M18.nc','r')
m19 = Dataset('OCSD_M19.nc','r')
m20 = Dataset('OCSD_M20.nc','r')
m21 = Dataset('OCSD_M21.nc','r')

time_nc_18 = m18.variables['time']
time_unit_18 = time_nc_18.units
time_nc_19 = m19.variables['time']
time_unit_19 = time_nc_19.units
time_nc_20 = m20.variables['time']
time_unit_20 = time_nc_20.units
time_nc_21 = m21.variables['time']
time_unit_21 = time_nc_21.units

time_18 = m18.variables['time'][:]
time_19 = m19.variables['time'][:]
time_20 = m20.variables['time'][:]
time_21 = m21.variables['time'][:]

date_18 = num2date(time_18,time_unit_18)
date_19 = num2date(time_19,time_unit_19)
date_20 = num2date(time_20,time_unit_20)
date_21 = num2date(time_21,time_unit_21)

date_len = len(date_19)+len(date_20)+len(date_21)+len(date_18)

depth_18 = m18.variables['depth'][:]
depth_19 = m19.variables['depth'][:]
depth_20 = m20.variables['depth'][:]
depth_21 = m21.variables['depth'][:]

lat_18 = m18.variables['latitude'][:]
lat_19 = m19.variables['latitude'][:]
lat_20 = m20.variables['latitude'][:]
lat_21 = m21.variables['latitude'][:]

lon_18 = m18.variables['longitude'][:]
lon_19 = m19.variables['longitude'][:]
lon_20 = m20.variables['longitude'][:]
lon_21 = m21.variables['longitude'][:]

u_18 = m18.variables['u'][:,:] 
u_19 = m19.variables['u'][:,:]
u_20 = m20.variables['u'][:,:]
u_21 = m21.variables['u'][:,:]

v_18 = m18.variables['v'][:,:]
v_19 = m19.variables['v'][:,:]
v_20 = m20.variables['v'][:,:]
v_21 = m21.variables['v'][:,:]

w_18 = m18.variables['w'][:,:]
w_19 = m19.variables['w'][:,:]
w_20 = m20.variables['w'][:,:]
w_21 = m21.variables['w'][:,:]

u_1d = []
u_1d_19 = []
u_1d_20 = []
u_1d_21 = []

v_1d = []
v_1d_19 = []
v_1d_20 = []
v_1d_21 = []

w_1d = []
w_1d_19 = []
w_1d_20 = []
w_1d_21 = []

depth_1d = []
depth_1d_19 = []
depth_1d_20 = []
depth_1d_21 = []

time_1d = []
time_1d_19 = []
time_1d_20 = []
time_1d_21 = []

lat_1d = []
lat_1d_19 = []
lat_1d_20 = []
lat_1d_21 = []

lon_1d = []
lon_1d_19 = []
lon_1d_20 = []
lon_1d_21 = []

print('1D M18')
for u_i in range(time_18.shape[0]):
    for d_i in range(depth_18.shape[0]):
        u_1d.append(u_18[u_i,d_i])
        v_1d.append(v_18[u_i,d_i])
        w_1d.append(w_18[u_i,d_i])
        depth_1d.append(depth_18[d_i]) 
        time_1d.append(date_18[u_i])
        lat_1d.append(lat_18[0])
        lon_1d.append(lon_18[0])

print('1D M19')
for u_i in range(time_19.shape[0]):
    for d_i in range(depth_19.shape[0]):
        u_1d.append(u_19[u_i,d_i])
        v_1d.append(v_19[u_i,d_i])
        w_1d.append(w_19[u_i,d_i])
        depth_1d.append(depth_19[d_i]) 
        time_1d.append(date_19[u_i])
        lat_1d.append(lat_19[0])
        lon_1d.append(lon_19[0])

print('1D M20')
for u_i in range(time_20.shape[0]):
    for d_i in range(depth_20.shape[0]):
        u_1d.append(u_20[u_i,d_i])
        v_1d.append(v_20[u_i,d_i])
        w_1d.append(w_20[u_i,d_i])
        depth_1d.append(depth_20[d_i]) 
        time_1d.append(date_20[u_i])
        lat_1d.append(lat_20[0])
        lon_1d.append(lon_20[0])

print('1D M21')
for u_i in range(time_21.shape[0]):
    for d_i in range(depth_21.shape[0]):
        u_1d.append(u_21[u_i,d_i])
        v_1d.append(v_21[u_i,d_i])
        w_1d.append(w_21[u_i,d_i])
        depth_1d.append(depth_21[d_i]) 
        time_1d.append(date_21[u_i])
        lat_1d.append(lat_21[0])
        lon_1d.append(lon_21[0])

u_1d_arr = np.array(u_1d)
v_1d_arr = np.array(v_1d)
w_1d_arr = np.array(w_1d)
depth_1d_arr = np.array(depth_1d)
time_1d_arr = date2num(np.array(time_1d),time_unit_19)
lat_1d_arr = np.array(lat_1d)
lon_1d_arr = np.array(lon_1d)

#################
# make netcdf
################
