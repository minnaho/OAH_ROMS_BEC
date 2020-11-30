import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import cmocean as cmocean
import h5py
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.io import shapereader as shpreader
import pandas as pd

plt.ion()

# central bight database
v_data = pd.read_csv('/data/project1/minnaho/validation/validation_metadata.csv',header=None,skiprows=1)
sd_data = pd.read_csv('/data/project1/minnaho/validation/central_bight/SD_StationCoordinates.csv',header=None)
sd_lat = np.array(sd_data[3][1:]).astype(float)
sd_lon = np.array(sd_data[4][1:]).astype(float)

# indices where nan (changes source of data)
lat_v = v_data[1][1:]
lon_v = v_data[2][1:]
nan_ind = np.where(np.isnan(lat_v))[0]

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

extent = [lon_min,lon_max,lat_min,lat_max]
rivers_10m = cpf.NaturalEarthFeature('physical','rivers_lake_centerlines','10m')
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
wsheds = shpreader.Reader('./basin_arcgis/wribasin.shp')

fig_w = 15
fig_h = 12

colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

# plot MPA masks
#for m_i in range(len(all_mpas)):
#    ax.contour(lon_nc,lat_nc,all_mpas[m_i],levels=1,colors='lightslategrey',linewidths=2,transform=ccrs.PlateCarree())

ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':20}
gl.ylabel_style = {'size':20}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')

# plot observational points
m_size_small = 50
sd_points = ax.scatter(sd_lon,sd_lat,s=m_size_small,marker='o',facecolors='yellow',edgecolor='darkgrey',label='San Diego')
central = ax.scatter(lon_v[nan_ind[5]+1:nan_ind[6]],lat_v[nan_ind[5]+1:nan_ind[6]],s=m_size_small,marker='o',facecolors='purple',edgecolor='darkgrey')

# major rivers
shpfile = 'MajorRiversAndCreeks'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)


# actual MPAs
#shpfile = './fromabel/Project_MPA_CA_Existing_160301'
#mpashp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='purple')
#ax.add_feature(mpashp)

# counties
#shpfile = './fromabel/Project_Counties'
#countyshp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='pink',facecolor='None')
#ax.add_feature(countyshp)

# towns
#shpfile = './fromabel/Project_city_UTM_zone11_region'
#regionshp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='gold')
#ax.add_feature(regionshp)

# watersheds
shpfile = './fromabel/Project_HUC_250k'
hucshp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='navy',facecolor='None')
ax.add_feature(hucshp)

# streams
shpfile = './fromabel_stream/Streams'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# river dots
m_size = 20
ax.scatter(lons_river,lats_river,s=m_size,marker='o',facecolors='red',edgecolor='red',lw=1,label='River',zorder=10)

# POTWs
m_size = 150
maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='s',facecolors='none',edgecolor='grey',lw=3)
min_potw_plt = ax.scatter(lons_minor_potw,lats_minor_potw,s=m_size,marker='o',facecolors='none',edgecolor='k',lw=2,label='Minor POTW')

# validation locations

# region names
#ax.text(36000,200000,'Santa Barbara',fontsize=axis_tick_size)
#ax.text(130000,160000,'Ventura',fontsize=axis_tick_size,rotation=-20)
#ax.text(195000,171000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
##ax.text(187000,143000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
#ax.text(213000,123000,'San Pedro',fontsize=axis_tick_size)
#ax.text(250000,81000,'Orange County',fontsize=axis_tick_size,rotation=-40)
#ax.text(262500,55000,'North San Diego',fontsize=axis_tick_size)
#ax.text(266000,15000,'South San Diego',fontsize=axis_tick_size)
#ax.text(215000,155000,'Greater Los Angeles',fontsize=axis_tick_size+4,rotation=-35)
#
## MPA names
#ax.text(85700,225000,'MPA1',fontsize=axis_tick_size)
#ax.text(173000,185000,'MPA2',fontsize=axis_tick_size)
#ax.text(225500,150000,'MPA3',fontsize=axis_tick_size,rotation=50)
#ax.text(276500,123000,'MPA4',fontsize=axis_tick_size,rotation=-40)
#ax.text(330000,46000,'MPA5',fontsize=axis_tick_size,rotation=50)
#ax.text(333000,38000,'MPA6',fontsize=axis_tick_size,rotation=50)

fill_legend = ax.fill(np.nan,np.nan,'black',alpha=0.9)
fill_legend_mark = [(fill_legend[0],maj_potw_plt)]
fill_legend_label = ['Major POTW']


h1,l1 = ax.get_legend_handles_labels()
h2 = h1+fill_legend_mark
l2 = l1+fill_legend_label

leg_size = 16
leg_ax = ax.legend(h2,l2,loc='lower left',fontsize=leg_size,labelspacing=1)
leg_ax.get_patches()

plt.savefig('figs/watersheds_inputs_map.png',bbox_inches='tight')
