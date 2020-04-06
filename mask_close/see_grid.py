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

grid_path = '/data/project3/kesf/ROMS/L2_SCB/grid/'
grid_name = 'mask_fix.nc'

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print('%d, %d'%(ix, iy))


data = Dataset(grid_path+grid_name,'r')
mask = data.variables['land_rho']
mask_copy = np.copy(mask)


fig = plt.figure(figsize=[9,15])
ax = fig.add_subplot(111)
ax.imshow(mask_copy,origin='lower')
#cid = fig.canvas.mpl_connect('button_press_event',onclick)
'''

coords = []
f = open(grid_path+'grid_fix.txt','r',encoding='utf-8-sig')
for line in f:
    x,y = line.rstrip().split(', ')
    x = int(x)
    y = int(y)
    coords.append([y,x]) 

for c in coords:
    mask_copy[c[0],c[1]] = 2 

data_new = Dataset(grid_path+'mask_fix.nc','w') 
eta = data_new.createDimension('eta_rho',1502)
xi = data_new.createDimension('xi_rho',602)

land = data_new.createVariable('land_rho',np.float32,('eta_rho','xi_rho'))
land[:,:] = np.copy(mask_copy[:,:])

data_new.close()
'''
