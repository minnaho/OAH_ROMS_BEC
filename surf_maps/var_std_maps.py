import subprocess
import glob
from netCDF4 import Dataset
import numpy as np

path_output = '/data/project3/kesf/tools_matlab/applications/xyt/outputs/'
path_save = '/data/project1/minnaho/surf_maps/'
'''
file_name = 'L1S*'

files = glob.glob1(path_output,file_name)
ind = files[0].index('_')+1
files[0][ind:].index('_')
'''

files = ['DIC_sigma_60.nc',
         'L1S_NO3_sigma_60.nc',
         'L1S_O2_sigma_60.nc',
         'L1S_pCO2_sigma_60.nc',
         'L1S_PH_sigma_60.nc',
         'salt_sigma_60.nc',
         'temp_sigma_60.nc'
        ]

# variable names different for each
variables = ['DIC','NO3','O2','pCO2','PH','salt','temp']

'''
# find standard deviation
for idx,f_i in enumerate(files):
    print(f_i)
    nc_file = Dataset(path_output+f_i,'r')
    lat_shape = nc_file.variables[variables[idx]].shape[1]
    lon_shape = nc_file.variables[variables[idx]].shape[2]
    var_unit = nc_file.variables[variables[idx]].units
    data_std = np.nanstd(nc_file.variables[variables[idx]],axis=0) 
    if 'L1' in f_i:
        ind = f_i.index('_')+1
        save_name_temp = f_i[ind:]
        ind_end = save_name_temp.index('_')
        save_name = save_name_temp[:ind_end] 
    if 'L1' not in f_i:
        ind_end = f_i.index('_')
        save_name = f_i[:ind_end] 

    # create netcdf
    nc_file_new = Dataset(save_name+'_surf_std_1997_2007.nc','w')
    nc_file_new.title = 'standard deviation of daily ROMS-BEC output 1997-2007 of '+save_name
    nc_file_new.source = 'Faycal Kessouri, UCLA, ROMS-BEC model 2018'
    
    #dimensions
    time = nc_file_new.createDimension('ocean_time',1)
    lat = nc_file_new.createDimension('latitude',lat_shape)
    lon = nc_file_new.createDimension('longitude',lon_shape)
    
    #variable
    var = nc_file_new.createVariable('var',np.float32,('ocean_time','latitude','longitude'))
    var.units = var_unit
    
    var[:,:,:] = data_std
    nc_file_new.close()
'''
# find variance
for idx,f_i in enumerate(files):
    print(f_i)
    nc_file = Dataset(path_output+f_i,'r')
    lat_shape = nc_file.variables[variables[idx]].shape[1]
    lon_shape = nc_file.variables[variables[idx]].shape[2]
    var_unit = nc_file.variables[variables[idx]].units
    data_std = np.nanvar(nc_file.variables[variables[idx]],axis=0) 
    if 'L1' in f_i:
        ind = f_i.index('_')+1
        save_name_temp = f_i[ind:]
        ind_end = save_name_temp.index('_')
        save_name = save_name_temp[:ind_end] 
    if 'L1' not in f_i:
        ind_end = f_i.index('_')
        save_name = f_i[:ind_end] 

    # create netcdf
    nc_file_new = Dataset(save_name+'_surf_var_1997_2007.nc','w')
    nc_file_new.title = 'variance of daily ROMS-BEC output 1997-2007 of '+save_name
    nc_file_new.source = 'Faycal Kessouri, UCLA, ROMS-BEC model 2018'
    
    #dimensions
    time = nc_file_new.createDimension('ocean_time',1)
    lat = nc_file_new.createDimension('latitude',lat_shape)
    lon = nc_file_new.createDimension('longitude',lon_shape)
    
    #variable
    var = nc_file_new.createVariable('var',np.float32,('ocean_time','latitude','longitude'))
    var.units = var_unit
    
    var[:,:,:] = data_std
    nc_file_new.close()

    
