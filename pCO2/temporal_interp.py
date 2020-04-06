#############################################
# interpolate L2 WRF pCO2 map temporally so no gaps between days
#####################################################
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from scipy import interpolate
import datetime

output_path = '/data/project1/minnaho/pCO2/'

##################################
# load pCO2 data
##################################
dataset_name = 'L2_wrfout_d01_2015_avg_2hr.nc'
atmos_data = Dataset(output_path+dataset_name,'r')

time_arr = atmos_data.variables['hour'][:]
pco2_arr = atmos_data.variables['co2ff'][:,:,:]

Ly = range(pco2_arr.shape[1])
Lx = range(pco2_arr.shape[2])

pco2_interp_list = []

# interpolate 
interpolate.RectBivariateSpline(Ly,Lx,
for m_i in range(pco2_arr.shape[0]):
    
    pco2_interp_list.append(pco2_int_m)

pco2_interp_arr_land = np.array(pco2_interp_list)

'''
# multiply by mask to get rid of values on land
pco2_interp_arr = pco2_interp_arr_land * mask_nc
pco2_interp_arr[np.isnan(pco2_interp_arr)] = 0
'''

################
# make netCDF
################

eta_rho = lat_nc.shape[0]
xi_rho = lat_nc.shape[1]

data_interp = Dataset('L2_wrfout_d01_2015_avg_2hr.nc','w')
data_interp.title = 'Anthropogenic pCO2 ppmv linearly interpolated to L2 grid (300 m) Southern California Bight'
data_interp.source = 'Sha Feng anthropogenic pCO2 model output from WRF over Los Angeles'
data_interp.description = '2 hourly average'

time = data_interp.createDimension('time',pco2_interp_arr.shape[0])
eta_d = data_interp.createDimension('eta_rho',eta_rho)
xi_d = data_interp.createDimension('xi_rho',xi_rho)

time_var = data_interp.createVariable('hour',np.float32,('time'))
pco2_nc = data_interp.createVariable('co2ff',np.float32,('time','eta_rho','xi_rho')) 
#pressure_nc = data_interp.createVariable('p',np.float32,('time','eta_rho','xi_rho'))
#height_nc = data_interp.createVariable('z',np.float32,('time','eta_rho','xi_rho'))

pco2_nc[:,:,:] = pco2_interp_arr
time_var[:] = date_nc
#pressure_nc[:,:,:] = pressure_interp_arr
#height_nc[:,:,:] = height_interp_arr

pco2_nc.units = 'ppmv'
pco2_nc.description = 'mixing ratio of anthropogenic CO2'
time_var.units = time_units
#pressure_nc.units =  'hPa'
#pressure_nc.description = 'Pressure'
#height_nc.units = 'm'
#pressure_nc.description = 'Height'

data_interp.close()

