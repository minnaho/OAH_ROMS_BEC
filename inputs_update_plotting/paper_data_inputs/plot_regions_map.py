import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import cmocean as cmocean
import scipy.io as sio

plt.ion()

# masks
region_mask = Dataset('../make_masks/mask_scb.nc','r')
mask_ssd = np.array(region_mask.variables['mask_ssd'])
mask_nsd = np.array(region_mask.variables['mask_nsd'])*2
mask_oc = np.array(region_mask.variables['mask_oc'])*3
mask_sp = np.array(region_mask.variables['mask_sp'])*4
# my SM mask
#mask_sm = np.array(region_mask.variables['mask_sm'])*5
# faycal's SM mask from PNAS paper
#mask_sm = np.array()*5
mask_v = np.array(region_mask.variables['mask_v'])*6
mask_sb = np.array(region_mask.variables['mask_sb'])*7

all_regions = np.array((mask_ssd,mask_nsd,mask_oc,mask_sp,mask_sm,mask_v,mask_sb))
all_regions[all_regions==0] = np.nan

grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
mask_nc = np.array(grid_nc.variables['mask_rho'])
mask_nc[mask_nc==0.0] = np.nan

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])

lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)

lat_min = 32.4
lat_max = 34.6
lon_min = -120.8
lon_max = -117

# plot
axis_tick_size = 14
# latitudes to draw
parallels = np.arange(0,90,1)
# longitudes to draw
meridians = np.arange(180,360,1)

m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)
x,y = m(lon_nc,lat_nc)

colormaps = [cmocean.cm.ice_r,cmocean.cm.solar,cmocean.cm.dense,cmocean.cm.turbid,'Greys','Purples',cmocean.cm.deep]
colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig_w = 15
fig_h = 12

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h])
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)

for m_i in range(len(all_regions)):
    ax.pcolor(x,y,all_regions[m_i],cmap=colormaps[m_i],vmin=0,vmax=7)

ax.text(63000,200000,'SB',fontsize=axis_tick_size)
ax.text(134000,167000,'Ventura',fontsize=axis_tick_size)
ax.text(191000,153500,'SM',fontsize=axis_tick_size)
ax.text(225000,125000,'SP',fontsize=axis_tick_size)
ax.text(263000,96000,'OC',fontsize=axis_tick_size)
ax.text(302000,55000,'NSD',fontsize=axis_tick_size)
ax.text(307000,15000,'SSD',fontsize=axis_tick_size)

plt.savefig('figs/region_masks.png',bbox_inches='tight')
