#############################################
# interpolate WRF pCO2 map to L2_SCB grid 
# L2_SCB_wrfout_pCO2_hourly_interp.nc
#####################################################
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from scipy import interpolate
import subprocess
import datetime

grid_path_L3 = '/data/project5/kesf/ROMS/L3_LAOC/grid/roms_grd.nc'

# grid data
grid_nc_L3 = Dataset(grid_path_L3,'r')
lat_nc_L3 = grid_nc_L3.variables['lat_rho'][:,:]
lon_nc_L3 = grid_nc_L3.variables['lon_rho'][:,:]
mask_nc_L3 = grid_nc_L3.variables['mask_rho'][:,:]
h_L3 = grid_nc_L3.variables['h'][:,:]


grid_path_L4 = '/data/project5/kesf/ROMS/L4_OC/grid/roms_grd.nc'

# grid data
grid_nc_L4 = Dataset(grid_path_L4,'r')
lat_nc_L4 = grid_nc_L4.variables['lat_rho'][:,:]
lon_nc_L4 = grid_nc_L4.variables['lon_rho'][:,:]
mask_nc_L4 = grid_nc_L4.variables['mask_rho'][:,:]

h_L4 = interpolate.griddata((lat_nc_L3.ravel(),lon_nc_L3.ravel()),h_L3.ravel(),(lat_nc_L4,lon_nc_L4),method='linear')

'''
# interpolate to L2 grid
for m_i in range(pco2_arr.shape[0]):
    print('interpolating grid for '+str(m_i)+' of '+str(pco2_arr.shape[0]))
    # multiply by mask to get rid of values on land
    interp_arr[m_i,:,:] = (interpolate.griddata((lats_a_plt.ravel(),lons_a_plt.ravel()),pco2_arr[m_i,:,:].ravel(),(lat_nc,lon_nc),method='linear'))*mask_nc

pco2_interp_arr[np.isnan(pco2_interp_arr)] = 0
'''

################
# make netCDF
################

eta_rho = lat_nc_L4.shape[0]
xi_rho = lat_nc_L4.shape[1]

data_interp = Dataset('L4_topo.nc','w')

eta_d = data_interp.createDimension('eta_rho',eta_rho)
xi_d = data_interp.createDimension('xi_rho',xi_rho)

h_nc = data_interp.createVariable('hraw',np.float32,('eta_rho','xi_rho')) 

h_nc[:,:] = h_L4
data_interp.close()

# remove h and hraw from old grid
#ncks -x -v h roms_grd_L4.nc roms_grd_L4.nc
#ncks -x -v hraw roms_grd_L4.nc roms_grd_L4.nc

# add hraw that was interpolated from h in L3 grid
#ncks -A -v hraw L4_topo.nc roms_grd_L4.nc

# add h same as hraw
#cp L4_topo.nc L4_topo_h.nc
#ncrename -v hraw,h L4_topo_h.nc
#ncks -A -v h L4_topo_h.nc roms_grd_L4.nc

# add units and long_name
#ncatted -a long_name,'hraw',c,c,'raw bathymetry at RHO-points' roms_grd_L4.nc
#ncatted -a units,'hraw',c,c,'meter' roms_grd_L4.nc

# remove history attribute
#ncatted -hO -a history,global,d,, roms_grd_L4.nc





