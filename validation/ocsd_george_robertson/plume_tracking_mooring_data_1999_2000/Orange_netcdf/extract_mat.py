import numpy as np
import scipy.io as sio
from netCDF4 import Dataset,num2date,date2num
import glob as glob
import datetime as datetime

#files_nc = glob.glob('*.nc')
files_nc = ['ocaq1c_d.nc']
#files_nc = ['ocat1c_d.nc']

nc_file = Dataset(files_nc[0],'r')

time_unit_st = nc_file.Start_Time
st_dt = datetime.datetime.strptime(time_unit_st, "%Y-%m-%d %H:%M:%S")
delta_t = np.array(nc_file.variables['delta_t'])

depth_nc = np.array(nc_file.variables['InstDepth'])
lat_nc = np.array(nc_file.variables['latitude'])
lon_nc = np.array(nc_file.variables['longitude'])

u_nc = np.array(nc_file.variables['U_cmpt'])/100 # convert to m/s
v_nc = np.array(nc_file.variables['V_cmpt'])/100 # convert to m/s

# interpolated values are 1, noninterpolated are 0
v_map = np.array(nc_file.variables['V_cmpt_flag'])
u_map = np.array(nc_file.variables['U_cmpt_flag'])

u_final = np.squeeze(u_nc*u_map)
v_final = np.squeeze(v_nc*v_map)

u_final[u_final==0] = np.nan
v_final[v_final==0] = np.nan

time_arr_unit = 'minutes since '+time_unit_st
time_arr = np.empty((u_final.shape[0]))
for d_i in range(u_final.shape[0]):
    time_arr[d_i] = delta_t*d_i

var_key = ['depth','time_unit','time','u_interp','v_interp','latitude','longitude']
var_save = [depth_nc,time_arr_unit,time_arr,u_final,v_final,lat_nc,lon_nc]

save_dict = {}
for k_i in range(len(var_key)):
    save_dict[var_key[k_i]] = var_save[k_i]
 
ind_nc = files_nc[0].index('.nc')
savename = files_nc[0][:ind_nc]+'.mat'
sio.savemat(savename, save_dict)
