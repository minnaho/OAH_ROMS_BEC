from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc' 
site = ['E',
         'U2',
         'U4',
         'D2',
         'D4',
         'O2',
         'O4']

lat_site = [33.636469,
            33.647558,
            33.660586,
            33.626793,
            33.617764,
            33.62528,
            33.61026]

lon_site = [-117.987677,
            -118.005844,
            -118.022696,
            -117.97026,
            -117.953662,
            -117.997415,
            -118.00988]

grid_nc = Dataset(grid_path,'r')
mask_nc = grid_nc.variables['mask_rho']
lat_nc = np.copy(grid_nc.variables['lat_rho'])
lon_nc = np.copy(grid_nc.variables['lon_rho'])

coord_i = []
coord_j = []

for coord in range(len(lat_site)):
    lat_you_want = lat_site[coord]
    lon_you_want = lon_site[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

mask_new = np.copy(mask_nc)
for c_i in range(len(coord_i)):
    mask_new[coord_j[c_i],coord_i[c_i]] = 2

y0 = 450+20
yE = 600-90
x0 = 520+30
xE = 580

#plt.ion()
ax = plt.figure(figsize=[14,9])
im = plt.imshow(mask_new[y0:yE,x0:xE],origin='lower')
#im = plt.imshow(mask_new,origin='lower',extent=[y0,yE,x0,xE])
plt.grid(b=True,which='both',linestyle='--')
plt.minorticks_on()
plt.savefig('huntington_beach_stations_gridded.png',bbox_inches='tight')

