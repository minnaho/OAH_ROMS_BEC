#############################################
# interpolate WRF pCO2 map to L2_SCB grid 
# L2_SCB_wrfout_pCO2_hourly_climatology.nc
#####################################################
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from scipy import interpolate

grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = grid_nc.variables['lat_rho'][:,:]
lon_nc = grid_nc.variables['lon_rho'][:,:]
mask_nc = grid_nc.variables['mask_rho'][:,:]

##################################
# load atmospheric deposition data
##################################
dataset_name = 'wrfout_d01_2015_hourly_climatology_08.nc'
atmos_data = Dataset(dataset_name,'r')

lats_a = atmos_data.variables['lat'][0,:,:]
lons_a = atmos_data.variables['lon'][0,:,:]
lats_a_plt = np.copy(lats_a)
lons_a_plt = np.copy(lons_a)

pco2_arr = atmos_data.variables['co2ff'][:,0,:,:]
#pressure_arr = atmos_data.variables['p'][:,0,:,:]
#height_arr = atmos_data.variables['z'][:,0,:,:]

pco2_interp_list = []
#pressure_interp_list = []
#height_interp_list = []

# interpolate to L2 grid
for m_i in range(24):
    pco2_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),pco2_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    #pressure_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),pressure_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    #height_int_m = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),height_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear')
    # append each month to variable list
    pco2_interp_list.append(pco2_int_m)
    #pressure_interp_list.append(pressure_int_m)
    #height_interp_list.append(height_int_m)

pco2_interp_arr_land = np.array(pco2_interp_list)
#pressure_interp_arr = np.array(pressure_interp_list)
#height_interp_arr = np.array(height_interp_list)

#pco2_test = interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),pco2_arr[1,:,:].ravel(),(lat_nc,lon_nc),method='linear')
#plt.imshow(pco2_test,origin='lower')

# multiply by mask to get rid of values on land
pco2_interp_arr = pco2_interp_arr_land * mask_nc
pco2_interp_arr[np.isnan(pco2_interp_arr)] = 0

################
# make netCDF
################

eta_rho = lat_nc.shape[0]
xi_rho = lat_nc.shape[1]

data_interp = Dataset('L2_SCB_wrfout_pCO2_hourly_climatology_08.nc','w')
data_interp.title = 'Anthropogenic pCO2 ppmv linearly interpolated to L2 grid (300 m) Southern California Bight'
data_interp.source = 'Sha Feng anthropogenic pCO2 model output from WRF over Los Angeles'
data_interp.description = '24 time steps, 1 for each hour of the day (hourly climatology)'

time = data_interp.createDimension('time',24)
eta_d = data_interp.createDimension('eta_rho',eta_rho)
xi_d = data_interp.createDimension('xi_rho',xi_rho)

pco2_nc = data_interp.createVariable('co2ff',np.float32,('time','eta_rho','xi_rho')) 
#pressure_nc = data_interp.createVariable('p',np.float32,('time','eta_rho','xi_rho'))
#height_nc = data_interp.createVariable('z',np.float32,('time','eta_rho','xi_rho'))

pco2_nc[:,:,:] = pco2_interp_arr
#pressure_nc[:,:,:] = pressure_interp_arr
#height_nc[:,:,:] = height_interp_arr

pco2_nc.units = 'ppmv'
pco2_nc.description = 'mixing ratio of anthropogenic CO2'
#pressure_nc.units =  'hPa'
#pressure_nc.description = 'Pressure'
#height_nc.units = 'm'
#pressure_nc.description = 'Height'

data_interp.close()

