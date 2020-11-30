import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import cmocean as cmocean
import h5py

plt.ion()

# inputs
major_potw = np.load('../inputs_map/major_potw_lat_lon.npy')
minor_potw = np.load('../inputs_map/minor_potw_lat_lon.npy')
rivers = np.load('../inputs_map/river_lat_lon.npy')
lats_major_potw = major_potw[0]
lons_major_potw = major_potw[1]

lats_minor_potw = minor_potw[0]
lons_minor_potw = minor_potw[1]

lats_river = rivers[0]
lons_river = rivers[1]

# mpa masks
mpa1 = np.transpose(np.array(h5py.File('mpa1.mat','r')['mpa1']))
mpa2 = np.transpose(np.array(h5py.File('mpa2.mat','r')['mpa2']))
mpa3 = np.transpose(np.array(h5py.File('mpa3.mat','r')['mpa3']))
mpa4 = np.transpose(np.array(h5py.File('mpa4.mat','r')['mpa4']))
mpa5 = np.transpose(np.array(h5py.File('mpa5.mat','r')['mpa5']))
mpa6 = np.transpose(np.array(h5py.File('mpa6.mat','r')['mpa6']))

all_mpas = np.array((mpa1,mpa2,mpa3,mpa4,mpa5,mpa6))*.9
all_mpas[all_mpas==0] = np.nan
np.nan_to_num(all_mpas,copy=False,nan=0)

# region masks
region_mask = Dataset('../make_masks/mask_scb.nc','r')
mask_ssd = np.array(region_mask.variables['mask_ssd'])
mask_nsd = np.array(region_mask.variables['mask_nsd'])*2
mask_oc = np.array(region_mask.variables['mask_oc'])*3
mask_sp = np.array(region_mask.variables['mask_sp'])*4
# my SM mask
#mask_sm = np.array(region_mask.variables['mask_sm'])*5
# faycal's SM mask from PNAS paper
mask_sm = np.transpose(np.array(h5py.File('masksm.mat','r')['masksm']))
mask_v = np.array(region_mask.variables['mask_v'])*6
mask_sb = np.array(region_mask.variables['mask_sb'])*7

mask_la = np.transpose(np.array(h5py.File('maskgla.mat','r')['maskgla']))
np.nan_to_num(mask_la,copy=False,nan=0)

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
axis_tick_size = 16
# latitudes to draw
parallels = np.arange(0,90,1)
# longitudes to draw
meridians = np.arange(180,360,1)

m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)
x,y = m(lon_nc,lat_nc)

# potw locs
x_major_potw,y_major_potw = m(lons_major_potw,lats_major_potw)
x_minor_potw,y_minor_potw = m(lons_minor_potw,lats_minor_potw)
x_river,y_river = m(lons_river,lats_river)

colormaps = [cmocean.cm.ice_r,cmocean.cm.solar,cmocean.cm.dense,cmocean.cm.turbid,'Greys','Purples',cmocean.cm.deep]
colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig_w = 15
fig_h = 12

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h])
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size+4)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size+4)

# plot region masks
for m_i in range(len(all_regions)):
    ax.pcolor(x,y,all_regions[m_i],cmap=colormaps[m_i],vmin=0,vmax=7)

# plot MPA masks
for m_i in range(len(all_mpas)):
    #ax.contour(x,y,all_mpas[m_i],1,cmap='Greys')
    ax.contour(x,y,all_mpas[m_i],1,colors='lightslategrey')
    #ax.pcolor(x,y,all_mpas[m_i],cmap='Greens',hatch='/',alpha=0)

# greater LA
ax.contour(x,y,mask_la,1,colors='mediumspringgreen')

# plot POTWs
m_size = 150
maj_potw_plt = m.scatter(x_major_potw,y_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='white',lw=3)
min_potw_plt = m.scatter(x_minor_potw,y_minor_potw,s=m_size,marker='o',facecolors='none',edgecolor='k',lw=2,label='Minor POTW')

# plot rivers
m_size = 20
river_plt = m.scatter(x_river,y_river,s=m_size,marker='o',facecolors='red',edgecolor='red',lw=1,label='River',zorder=10)

# region names
ax.text(36000,200000,'Santa Barbara',fontsize=axis_tick_size)
ax.text(130000,160000,'Ventura',fontsize=axis_tick_size,rotation=-20)
ax.text(195000,171000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
#ax.text(187000,143000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
ax.text(213000,123000,'San Pedro',fontsize=axis_tick_size)
ax.text(250000,81000,'Orange County',fontsize=axis_tick_size,rotation=-40)
ax.text(262500,55000,'North San Diego',fontsize=axis_tick_size)
ax.text(266000,15000,'South San Diego',fontsize=axis_tick_size)
ax.text(215000,155000,'Greater Los Angeles',fontsize=axis_tick_size+4,rotation=-35)

# MPA names
ax.text(85700,225000,'MPA1',fontsize=axis_tick_size)
ax.text(173000,185000,'MPA2',fontsize=axis_tick_size)
ax.text(225500,150000,'MPA3',fontsize=axis_tick_size,rotation=50)
ax.text(276500,123000,'MPA4',fontsize=axis_tick_size,rotation=-40)
ax.text(330000,46000,'MPA5',fontsize=axis_tick_size,rotation=50)
ax.text(333000,38000,'MPA6',fontsize=axis_tick_size,rotation=50)

fill_legend = ax.fill(np.nan,np.nan,'black',alpha=0.9)
fill_legend_mark = [(fill_legend[0],maj_potw_plt)]
fill_legend_label = ['Major POTW']

line_legend = ax.plot(np.nan,np.nan,'lightslategrey',linewidth=3)
line_legend_mark = [(line_legend[0],line_legend[0])]
line_legend_label = ['MPA']

h1,l1 = ax.get_legend_handles_labels()
h2 = h1+fill_legend_mark+line_legend_mark
l2 = l1+fill_legend_label+line_legend_label
#h2 = h1[1:]+[h1[0]]
#l2 = l1[1:]+[l1[0]]

leg_size = 16
leg_ax = ax.legend(h2,l2,loc='upper right',fontsize=leg_size,labelspacing=1)
leg_ax.get_patches()

plt.savefig('figs/region_masks.png',bbox_inches='tight')
