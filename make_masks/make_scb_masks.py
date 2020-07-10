# make netcdf of masks 
# for regions in SCB
# full bight, greater LA region (santa ana river to top of santa monica bay)
# south san diego, north san diego,
# orange county, san pedro, santa monica,
# ventura, 
# santa barbara (+ rest of northern domain)

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import scipy.io

############
# load grid
############
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

# mask that is first 0-15km offshore
mask_mat = scipy.io.loadmat('../maskt.mat')['maskt']

# regions
# south sd, north sd, oc, sp, sm, v, sb
# chosen visually
j_locs = np.array((164,264,500,610,740,948))
maskarr = np.zeros((len(j_locs)+1,mask_nc.shape[0],mask_nc.shape[1]))
maskarr[0,:j_locs[0],:] = 1
maskarr[1,j_locs[0]:j_locs[1],:] = 1
maskarr[2,j_locs[1]:j_locs[2],:] = 1
maskarr[3,j_locs[2]:j_locs[3],:] = 1
maskarr[4,j_locs[3]:j_locs[4],:] = 1
maskarr[5,j_locs[4]:j_locs[5],:] = 1
maskarr[6,j_locs[5]:,:] = 1

#33.629595,-117.958189 to 34.042741,-118.938089
# lat/lon of santa ana river to slightly north of Santa monica to make 
# greater LA mask
la_lat = [33.629595,34.042741]
la_lon = [-117.958189,-118.938089]
l_coord_i = []
l_coord_j = []
for coord in range(len(la_lat)):
    lat_you_want = la_lat[coord]
    lon_you_want = la_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    l_coord_i.append(xi_coord)
    l_coord_j.append(eta_coord)


mask_la = np.zeros((mask_nc.shape[0],mask_nc.shape[1]))
mask_la[l_coord_j[0]:l_coord_j[1]] = 1
mask_la = mask_la*mask_mat

# multiply masks by 0-15km mask to exclude offshore 
for j_i in range(maskarr.shape[0]):
    maskarr[j_i] = maskarr[j_i]*mask_mat

# create netcdf of masks
mask_scb = Dataset('mask_scb.nc','w')
mask_scb.description = 'Southern California Bight masks, all exclude land'

# create dimensions
eta_coord = mask_scb.createDimension('eta_rho',mask_nc.shape[0])
xi_coord = mask_scb.createDimension('xi_rho',mask_nc.shape[1])

# create variables
b_mask = mask_scb.createVariable('mask_bight',np.float32,('eta_rho','xi_rho'))
coast_mask = mask_scb.createVariable('mask_coast',np.float32,('eta_rho','xi_rho'))
la_mask = mask_scb.createVariable('mask_la',np.float32,('eta_rho','xi_rho'))
ssd_mask = mask_scb.createVariable('mask_ssd',np.float32,('eta_rho','xi_rho'))
nsd_mask = mask_scb.createVariable('mask_nsd',np.float32,('eta_rho','xi_rho'))
oc_mask = mask_scb.createVariable('mask_oc',np.float32,('eta_rho','xi_rho'))
sp_mask = mask_scb.createVariable('mask_sp',np.float32,('eta_rho','xi_rho'))
sm_mask = mask_scb.createVariable('mask_sm',np.float32,('eta_rho','xi_rho'))
v_mask = mask_scb.createVariable('mask_v',np.float32,('eta_rho','xi_rho'))
sb_mask = mask_scb.createVariable('mask_sb',np.float32,('eta_rho','xi_rho'))

b_mask.longname = 'full bight'
coast_mask.longname = '0-15 km coastal band'
la_mask.longname = 'greater Los Angeles'
ssd_mask.longname = 'southern San Diego'
nsd_mask.longname = 'northern San Diego'
oc_mask.longname = 'Orange County'
sp_mask.longname = 'San Pedro'
sm_mask.longname = 'Santa Monica'
v_mask.longname = 'Ventura'
sb_mask.longname = 'Santa Barbara + rest of northern region'

b_mask[:,:] = mask_nc
coast_mask[:,:] = mask_mat
la_mask[:,:] = mask_la
ssd_mask[:,:] = maskarr[0]
nsd_mask[:,:] = maskarr[1]
oc_mask[:,:] = maskarr[2]
sp_mask[:,:] = maskarr[3]
sm_mask[:,:] = maskarr[4]
v_mask[:,:] = maskarr[5]
sb_mask[:,:] = maskarr[6]

mask_scb.close()



ln_minpotw = [-117.188,
-118.548, 
-117.299, 
-117.351, 
-117.393, 
-118.363, 
-117.699, 
-117.815, 
-118.254, 
-119.189, 
-119.531, 
-119.671, 
-119.656, 
-119.609]

lt_minpotw = [32.5373,
33.0102, 
33.0048, 
33.1103, 
33.1611, 
33.3049, 
33.4362, 
33.5453, 
33.7154, 
34.1262, 
34.3849, 
34.3888, 
34.4098, 
34.4122]

l_coord_i = []
l_coord_j = []
for coord in range(len(lt_minpotw)):
    lat_you_want = lt_minpotw[coord]
    lon_you_want = ln_minpotw[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    l_coord_i.append(xi_coord)
    l_coord_j.append(eta_coord)


plt.ion()
plt.imshow(mask_nc,origin='lower',cmap='spring')
plt.scatter(l_coord_i,l_coord_j)
#for i in range(len(maskarr)):
#    plt.imshow(maskarr[i]*mask_nc,cmap=colors[i],origin='lower')

