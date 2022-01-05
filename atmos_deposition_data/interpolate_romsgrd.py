#############################################
# interpolate 12km by 12km grid to ROMS grid 
# atmos_deposition_CMAQ_2002_2012.nc 
#####################################################
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from scipy import interpolate
from matplotlib import pyplot as plt
plt.ion()

#savename = 'L2SCB'
savename = 'USW4'

#L0 grid USW4
grid_path = '/data/project6/ROMS/USW4/organization/roms_grd.nc'

#L2 grid SCB
#grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc'

grid_nc = Dataset(grid_path,'r')
lat_nc = grid_nc.variables['lat_rho'][:,:]
lon_nc = grid_nc.variables['lon_rho'][:,:]

##################################
# load atmospheric deposition data
##################################
dataset_name = 'atmos_deposition_CMAQ_2002_2012.nc'
atmos_data = Dataset(dataset_name,'r')

lats_a = atmos_data.variables['latitude']
lons_a = atmos_data.variables['longitude']
lats_a_plt = np.copy(lats_a)
lons_a_plt = np.copy(lons_a)

oxn = atmos_data.variables['oxidized_nitrogen']
redn = atmos_data.variables['reduced_nitrogen']
alk = atmos_data.variables['alkalinity']
fe = atmos_data.variables['iron']

# find monthly climatologies
oxn_m = []
redn_m = []
alk_m = []
fe_m = []
for month in range(12):
    oxn_m.append(np.nanmean(oxn[month::12],axis=0))
    redn_m.append(np.nanmean(redn[month::12],axis=0))
    alk_m.append(np.nanmean(alk[month::12],axis=0))
    fe_m.append(np.nanmean(fe[month::12],axis=0))

oxn_arr = np.array(oxn_m)
redn_arr = np.array(redn_m)
alk_arr = np.array(alk_m)
fe_arr = np.array(fe_m)

oxn_interp_list = []
redn_interp_list = []
alk_interp_list = []
fe_interp_list = []

# interpolate to grid
for m_i in range(12):
    oxn_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),oxn_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    redn_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),redn_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    alk_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),alk_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    fe_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),fe_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')    
    # append each month to variable list
    oxn_interp_list.append(oxn_int_m)
    redn_interp_list.append(redn_int_m)
    alk_interp_list.append(alk_int_m)
    fe_interp_list.append(fe_int_m)

oxn_interp_arr = np.array(oxn_interp_list)
redn_interp_arr = np.array(redn_interp_list)
alk_interp_arr = np.array(alk_interp_list)
fe_interp_arr = np.array(fe_interp_list)

#oxn_test = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),oxn_arr[1,:,:].ravel(),(lat_nc,lon_nc),method='linear')
#plt.imshow(oxn_test,origin='lower')

################
# make netCDF
################
eta_rho = lat_nc.shape[0]
xi_rho = lat_nc.shape[1]

data_interp = Dataset(savename+'_atmos_deposition.nc','w')
data_interp.title = 'Atmospheric Deposition Monthly Climatologies from Reduced Nitrogen, Oxidized Nitrogen, Alkalinity, and Iron linearly interpolated to '+savename
data_interp.source = 'EPA Community Multiscale Air Quality modeling system (CMAQ) V5.0.2 monthly total deposition files 2002-2012 with adjusted wet deposition for continental US using 12km grids'
data_interp.description = '12 time steps, 1 for each month, January, February, March, etc'

time = data_interp.createDimension('time',12)
eta_d = data_interp.createDimension('eta_rho',eta_rho)
xi_d = data_interp.createDimension('xi_rho',xi_rho)

oxn_nc = data_interp.createVariable('NO3',np.float32,('time','eta_rho','xi_rho')) 
redn_nc = data_interp.createVariable('NH4',np.float32,('time','eta_rho','xi_rho'))
alk_nc = data_interp.createVariable('Alk',np.float32,('time','eta_rho','xi_rho'))
fe_nc = data_interp.createVariable('Fe',np.float32,('time','eta_rho','xi_rho'))

oxn_nc[:,:,:] = oxn_interp_arr
redn_nc[:,:,:] = redn_interp_arr
alk_nc[:,:,:] = alk_interp_arr
fe_nc[:,:,:] = fe_interp_arr

oxn_nc.units = 'mmol m-2 s-1'
redn_nc.units =  'mmol m2 s-1'
alk_nc.units = 'mmol m2 s-1'
fe_nc.units = 'mmol m2 s-1'

data_interp.close()
