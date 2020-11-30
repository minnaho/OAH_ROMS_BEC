import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import cmocean as cmocean
import h5py
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.io import shapereader as shpreader
import cartopy.io.img_tiles as cimgt

plt.ion()

stamen_terrain = cimgt.Stamen('terrain-background')

# inputs
major_nc = Dataset('/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc','r')
lats_major_potw = np.array(major_nc.variables['latitude'])
lons_major_potw = np.array(major_nc.variables['longitude'])

minor_nc = Dataset('/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc','r')
lats_minor_potw = np.array(minor_nc.variables['latitude'])
lons_minor_potw = np.array(minor_nc.variables['longitude'])

river_nc = Dataset('/data/project1/minnaho/river_data/updated_2013_2017/rivers_2007_2017.nc','r')

lats_river = np.array(river_nc.variables['latitude'])
lons_river = np.array(river_nc.variables['longitude'])

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

all_regions = np.array((mask_ssd,mask_nsd,mask_oc,mask_sp,mask_sm,mask_v,mask_sb))
all_regions[all_regions==0] = np.nan


# grid
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])

lat_min = 33.5
lat_max = 34.1
lon_min = -118.9
lon_max = -117.5

# plot
axis_tick_size = 16
# latitudes to draw
parallels = np.arange(0,90,1)
# longitudes to draw
meridians = np.arange(180,360,1)

extent = [lon_min,lon_max,lat_min,lat_max]
rivers_10m = cpf.NaturalEarthFeature('physical','rivers_lake_centerlines','10m')
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
wsheds = shpreader.Reader('../paper_data_inputs/basin_arcgis/wribasin.shp')

fig_w = 15
fig_h = 12

colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))
# plot region masks
for m_i in range(len(all_regions)):
    ax.contourf(lon_nc,lat_nc,all_regions[m_i],transform=ccrs.PlateCarree(),cmap=colormaps[m_i],vmin=0,vmax=7)

ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':20}
gl.ylabel_style = {'size':20}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')

# major rivers
shpfile = '../paper_data_inputs/MajorRiversAndCreeks'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# streams
shpfile = '../paper_data_inputs/fromabel_stream/Streams'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# river dots
m_size = 20
ax.scatter(lons_river,lats_river,s=m_size,marker='o',facecolors='red',edgecolor='red',lw=1,label='River',zorder=10)

# POTWs
m_size = 150
maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='yellow',lw=3,label='Major POTW')
#maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='blue',lw=3)
min_potw_plt = ax.scatter(lons_minor_potw,lats_minor_potw,s=m_size,marker='s',facecolors='none',edgecolor='k',lw=2,label='Minor POTW')

# region names
#ax.text(36000,200000,'Santa Barbara',fontsize=axis_tick_size)
#ax.text(130000,160000,'Ventura',fontsize=axis_tick_size,rotation=-20)
#ax.text(195000,171000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
##ax.text(187000,143000,'Santa Monica',fontsize=axis_tick_size,rotation=-35)
#ax.text(213000,123000,'San Pedro',fontsize=axis_tick_size)
#ax.text(250000,81000,'Orange County',fontsize=axis_tick_size,rotation=-40)
#ax.text(262500,55000,'North San Diego',fontsize=axis_tick_size)
#ax.text(266000,15000,'South San Diego',fontsize=axis_tick_size)


#fill_legend = ax.fill(np.nan,np.nan,'black',alpha=0.9)
#fill_legend_mark = [(fill_legend[0],maj_potw_plt)]
#fill_legend_label = ['Major POTW']


#h1,l1 = ax.get_legend_handles_labels()
#h2 = h1+fill_legend_mark
#l2 = l1+fill_legend_label

leg_size = 16
ax.legend(loc='lower left',fontsize=leg_size,labelspacing=1)
#leg_ax = ax.legend(h2,l2,loc='lower left',fontsize=leg_size,labelspacing=1)
#leg_ax.get_patches()

plt.savefig('figs/inputs_updated_map.png',bbox_inches='tight')
