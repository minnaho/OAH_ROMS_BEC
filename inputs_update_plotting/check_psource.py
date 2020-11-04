import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import cmocean as cmocean
from scipy import spatial


plt.ion()

psource_nc = Dataset('/data/project3/minnaho/roms_psource_102020_R3.nc','r')


# grid
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

# i,j places where mask == 1 (water)
mask_i = np.where(mask_nc==1)[1]
mask_j = np.where(mask_nc==1)[0]
# pairs of i,j arrays (([i,j],[i,j],...))
mask_1 = np.column_stack((mask_i,mask_j))

# i,j places where mask == 0 (land)
# pairs of i,j arrays (([i,j],[i,j],...))
mask_0 = np.column_stack((np.where(mask_nc==0)[1],np.where(mask_nc==0)[0]))


# 113 is where rivers start
p_i = np.array(psource_nc.variables['Isrc'])[113:]
p_j = np.array(psource_nc.variables['Jsrc'])[113:]
lcheck = mask_nc[p_j.astype(int),p_i.astype(int)]

# plot
axis_tick_size = 16

fig_w = 7
fig_h = 12

#fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))
fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h])
# plot region masks
ax.imshow(mask_nc,cmap=cmocean.cm.ice_r,origin='lower',vmin=0,vmax=2)
ax.scatter(p_i,p_j,color='k')
#for i in range(len(n)):
#    ax.annotate(str(n[i]),(coord_i_land_arr[i+r1],coord_j_land_arr[i+r1]),color='k')

# automatically find coastal water (water one grid point off land) 
# closest to river i,j found from lat,lon
coord_i_new = []
coord_j_new = []
for pt in range(len(p_i)):
    print('rivers: '+str(pt)+' of '+str(len(p_i)))
    #mask_pt = mask_1[spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))[1]]
    #distance,index = spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))
    index = spatial.KDTree(mask_1).query(np.array((p_i[pt],p_i[pt])))[1]
    coord_i_new.append(mask_1[index][0])
    coord_j_new.append(mask_1[index][1])
