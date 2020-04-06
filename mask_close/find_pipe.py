###########################
# look at grid and
# print out coordinates
# when clicking on picture
###########################

import numpy as np
from netCDF4 import Dataset
import matplotlib 
import matplotlib.pyplot as plt
plt.ion()

grid_path = 'roms_grd.nc'

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print('%d, %d'%(ix, iy))


data = Dataset(grid_path,'r')
mask = data.variables['mask_rho'][:,:]
lat_nc = data.variables['lat_rho'][:,:]
lon_nc = data.variables['lon_rho'][:,:]

# ocsd lat/lon of pipe diffuser
lat_data = [33.584061,33.57729,33.576667]
lon_data = [-117.994756,-117.99982,-118.01]

coord_i = []
coord_j = []
for coord in range(len(lat_data)):
    lat_you_want = lat_data[coord]
    lon_you_want = lon_data[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

fig = plt.figure(figsize=[9,15])
ax = fig.add_subplot(111)
ax.imshow(mask,origin='lower')
plt.plot(coord_i,coord_j,'-')
#cid = fig.canvas.mpl_connect('button_press_event',onclick)


coords = []
f = open('ocsd_pipe.txt','r',encoding='utf-8-sig')
for line in f:
    x,y = line.rstrip().split(', ')
    x = int(x)
    y = int(y)
    coords.append([y,x]) 
    plt.plot(x,y,'.')

'''
for c in coords:
    mask_copy[c[0],c[1]] = 2 

data_new = Dataset(grid_path+'mask_fix.nc','w') 
eta = data_new.createDimension('eta_rho',1502)
xi = data_new.createDimension('xi_rho',602)

land = data_new.createVariable('land_rho',np.float32,('eta_rho','xi_rho'))
land[:,:] = np.copy(mask_copy[:,:])

data_new.close()
'''
