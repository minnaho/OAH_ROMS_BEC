#############################################
# interpolate npp satellite data to L2_SCB grid 
#############################################
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from scipy import interpolate
import glob as glob
import matplotlib.pyplot as plt
plt.ion()

grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'][:,:])
lon_nc = np.array(grid_nc.variables['lon_rho'][:,:])
mask_nc = np.array(grid_nc.variables['mask_rho'][:,:])

##################################
# load npp data
##################################
# 1997-2000 SeaWiFS only
# vgpm or cbpm
st_t = 1997
en_t = 2000
alg_name_u = 'VGPM'
alg_name_l = 'vgpm'
#alg_name_u = 'CbPM'
#alg_name_l = 'cbpm'
dataset_path = '/data/project1/data/'+alg_name_u+'_NPP/SeaWiFS/'
dataset_name = alg_name_l+'.'
data_files1 = list(sorted(glob.glob(dataset_path+dataset_name+'1997*')))
data_files2 = list(sorted(glob.glob(dataset_path+dataset_name+'1998*')))
data_files3 = list(sorted(glob.glob(dataset_path+dataset_name+'1999*')))
data_files4 = list(sorted(glob.glob(dataset_path+dataset_name+'2000*')))
#data_files = data_files1+data_files2
#atmos_data = Dataset(dataset_path+dataset_name,'r')

# lat lon data
lat_lon_path = '/data/project1/data/'+alg_name_u+'_NPP/lat_lon_sat.nc'
lat_lon_d = Dataset(lat_lon_path,'r')
lats_a = np.array(lat_lon_d.variables['Lat'][:,:])
lons_a = np.array(lat_lon_d.variables['Lon'][:,:])

data_interp_list = []

# interpolate to L2 grid
for m_i in range(len(data_files2)):
    print(str(m_i)+' of '+str(len(data_files2)-1))
    data_arr2 = np.array(Dataset(data_files2[m_i],'r').variables['npp'])
    data_arr3 = np.array(Dataset(data_files3[m_i],'r').variables['npp'])
    data_arr4 = np.array(Dataset(data_files4[m_i],'r').variables['npp'])
    data_arr2[data_arr2<0]=np.nan
    data_arr3[data_arr3<0]=np.nan
    data_arr4[data_arr4<0]=np.nan
    # 1997 only has oct, nov, dec
    if m_i >= 9:
        data_arr1 = np.array(Dataset(data_files1[m_i-9],'r').variables['npp'])
        data_arr1[data_arr1<0]=np.nan
        data_arr = (data_arr1+data_arr2+data_arr3+data_arr4)/4.0 # mean of two arrays
    if m_i < 9:
        data_arr = (data_arr4+data_arr2+data_arr3)/3.0 # mean of two arrays
    data_int_m = interpolate.griddata((lats_a.ravel(),lons_a.ravel()),data_arr.ravel(),(lat_nc,lon_nc),method='linear')
    # append each month to variable list
    data_interp_list.append(data_int_m)

data_interp_arr_land = np.array(data_interp_list)
#plt.imshow(pco2_test,origin='lower')

# multiply by mask to get rid of values on land
data_interp_arr = data_interp_arr_land * mask_nc
data_interp_arr[data_interp_arr==0] = np.nan
data_interp_arr[data_interp_arr<0] = np.nan
#pco2_interp_arr[np.isnan(pco2_interp_arr)] = 0

################
# make netCDF
################

eta_rho = lat_nc.shape[0]
xi_rho = lat_nc.shape[1]

data_interp = Dataset('npp_'+alg_name_u+'_'+str(st_t)+'_'+str(en_t)+'.nc','w')
data_interp.title = alg_name_u+' npp linearly interpolated to L2 grid (300 m) Southern California Bight'

if alg_name_u == 'VGPM':
    data_interp.source = 'http://sites.science.oregonstate.edu/ocean.productivity/vgpm.model.php'
else:
    data_interp.source = 'http://sites.science.oregonstate.edu/ocean.productivity/carbon2.model.php'


data_interp.description = 'monthly climatology data'

time = data_interp.createDimension('time',len(data_files2))
eta_d = data_interp.createDimension('eta_rho',eta_rho)
xi_d = data_interp.createDimension('xi_rho',xi_rho)

data_nc = data_interp.createVariable('npp',np.float32,('time','eta_rho','xi_rho')) 
#pressure_nc = data_interp.createVariable('p',np.float32,('time','eta_rho','xi_rho'))
#height_nc = data_interp.createVariable('z',np.float32,('time','eta_rho','xi_rho'))

data_nc[:,:,:] = data_interp_arr
#pressure_nc[:,:,:] = pressure_interp_arr
#height_nc[:,:,:] = height_interp_arr

data_nc.units = 'mg C m^-2 day^-1'
data_nc.description = 'Net Primary Production'

data_interp.close()

