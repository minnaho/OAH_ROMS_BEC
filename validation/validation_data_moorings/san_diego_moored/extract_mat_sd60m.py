import numpy as np
import scipy.io as sio
from netCDF4 import Dataset,num2date,date2num
import glob as glob
import datetime as datetime

files_nc = ['SD_ADCP_60m.nc']

nc_file = Dataset(files_nc[0],'r')

time_nc = np.array(nc_file.variables['time'])

time_unit_st = nc_file.variables['time'].units

depth_nc = np.array(nc_file.variables['depth'])
lat_nc = np.array(nc_file.variables['latitude'])
lon_nc = np.array(nc_file.variables['longitude'])

# take surface value which is 100 m above surface
u_final = np.array(nc_file.variables['u'][:,:,-1])
v_final = np.array(nc_file.variables['v'][:,:,-1])

u_final[u_final==0] = np.nan
v_final[v_final==0] = np.nan

'''
time_arr_unit = 'minutes since '+time_unit_st
time_arr = np.empty((u_final.shape[0]))
for d_i in range(u_final.shape[0]):
    time_arr[d_i] = delta_t*d_i
'''

#var_key = ['depth','time_unit','time','u_interp','v_interp','latitude','longitude']
#var_save = [depth_nc,time_arr_unit,time_arr,u_final,v_final,lat_nc,lon_nc]
var_key = ['time','time_unit','u','v','latitude','longitude']
var_save = [time_nc,time_unit_st,u_final,v_final,lat_nc,lon_nc]


save_dict = {}
for k_i in range(len(var_key)):
    save_dict[var_key[k_i]] = var_save[k_i]
 
ind_nc = files_nc[0].index('.nc')
savename = files_nc[0][:ind_nc]+'_surf.mat'
sio.savemat(savename, save_dict)
