from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
 
psource_f = 'roms_psource.nc'

grid_nc = Dataset(grid_path,'r')
mask_nc = np.array(grid_nc.variables['mask_rho'])
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])

psource_nc = Dataset(psource_f,'r')
i_coords = np.array(psource_nc.variables['Isrc'])
j_coords = np.array(psource_nc.variables['Jsrc'])

mask_new = np.copy(mask_nc)
for c_i in range(len(i_coords)):
    mask_new[int(j_coords[c_i]),int(i_coords[c_i])] = 2

plt.ion()
ax = plt.figure(figsize=[14,9])
#im = plt.imshow(mask_nc,origin='lower')
#im = plt.imshow(mask_new,origin='lower',extent=[y0,yE,x0,xE])
im = plt.imshow(mask_new,origin='lower')
plt.grid(b=True,which='both',linestyle='--')
plt.minorticks_on()
#plt.savefig('huntington_beach_stations_gridded.png',bbox_inches='tight')

