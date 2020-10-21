from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

# load grid

grd_nc = Dataset('/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc','r')
lat_nc = np.array(grd_nc.variables['lat_rho'])
lon_nc = np.array(grd_nc.variables['lon_rho'])
mask_nc = np.array(grd_nc.variables['mask_rho'])


ncf = Dataset('mexican_potw_estimates_1997_2017_monthly.nc','r')

lat_fi = np.array(ncf.variables['latitude'])
lon_fi = np.array(ncf.variables['longitude'])

coord_i = []
coord_j = []
for coord in range(len(lat_fi)):
    lat_you_want = lat_fi[coord]
    lon_you_want = lon_fi[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

plt.ion()
plt.imshow(mask_nc,origin='lower')
plt.scatter(coord_i,coord_j)

# new lat/lon (so they are on land)
coord_j[3] = coord_j[3]-1

lat_nc[coord_j,coord_i]
