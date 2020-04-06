from netCDF4 import Dataset
import numpy as np
from netCDF4 import num2date, date2num
import matplotlib
import matplotlib.pyplot as plt
plt.ion()
############
# CALL GRID
############
grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid/'
grid_name = 'roms_grd.nc'

data = Dataset(grid_path+grid_name,'r')
mask = data.variables['mask_rho']
mask_copy = np.copy(mask)

lat_nc = data.variables['lat_rho']
lon_nc = data.variables['lon_rho']


#############################
# CALL LAT/LON COORDS OF INPUTS
############################
river      = np.load('river_lat_lon.npy')
major_potw = np.load('major_potw_lat_lon.npy')
minor_potw = np.load('minor_potw_lat_lon.npy')

lat_data = list(river[0]),list(major_potw[0]),list(minor_potw[0])
lon_data = list(river[1]),list(major_potw[1]),list(minor_potw[1])

# flatten lists
lat_data = [i for j in lat_data for i in j]
lon_data = [i for j in lon_data for i in j]

coord_i = []
coord_j = []
for coord in range(len(lat_data)):
    lat_you_want = lat_data[coord]
    lon_you_want = lon_data[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

# check if any potw locations are on land
n = 0
for i in range(len(coord_i)):
    if mask_copy[coord_j[i],coord_i[i]] == 0:
        n+=1

####################
# CHECK BY PLOTTING
####################
def plot_inputs(x_coords, y_coords, msize):
    [plt.plot(x_coords[n], y_coords[n],'o',markeredgecolor='green',mfc='green',markersize=msize) for n in range(len(x_coords))]


plt.imshow(mask_copy,origin='lower')
plot_inputs(coord_i[:4],coord_j[:4],3)

'''
# move potw locations that are on land offshore in x direction
# to first grid cell in ocean
for i in range(len(potw_coord_x)):
    while mask[potw_coord_y[i],potw_coord_x[i]] == 0:
        potw_coord_x[i] -= 1
'''  

