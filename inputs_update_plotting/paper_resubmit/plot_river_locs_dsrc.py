import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import cmocean as cmocean
from scipy import spatial


plt.ion()

river_nc = Dataset('/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc','r')

lat_riv = np.array(river_nc.variables['latitude'])
lon_riv = np.array(river_nc.variables['longitude'])

# grid
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])
mask_ncpsi = np.array(grid_nc.variables['mask_rho'])

# plot
axis_tick_size = 16

fig_w = 7
fig_h = 12

mask_0 = np.column_stack((np.where(mask_nc==0)[1],np.where(mask_nc==0)[0]))

coord_i = []
coord_j = []

for coord in range(len(lat_riv)):
    lat_you_want = lat_riv[coord]
    lon_you_want = lon_riv[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

# find closest land point to river
coord_i_land_l = []
coord_j_land_l = []
for pt in range(len(coord_i)):
    print('land: '+str(pt)+' of '+str(len(coord_i)))
    index = spatial.KDTree(mask_0).query([coord_i[pt],coord_j[pt]])[1]
    coord_i_land_l.append(mask_0[index][0])
    coord_j_land_l.append(mask_0[index][1])

coord_i_land_arr = np.array(coord_i_land_l)
coord_j_land_arr = np.array(coord_j_land_l)

#fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))
fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h])
# plot region masks
ax.imshow(mask_nc,cmap=cmocean.cm.ice_r,origin='lower',vmin=0,vmax=2)
#n = range(len(coord_i))
r1 = 70
r2 = 75
n = range(r1,r2)
ax.scatter(coord_i_land_arr[r1:r2],coord_j[r1:r2],color='k')
for i in range(len(n)):
    ax.annotate(str(n[i]),(coord_i_land_arr[i+r1],coord_j_land_arr[i+r1]),color='k')

