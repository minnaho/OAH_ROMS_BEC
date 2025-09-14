import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
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

river_nc = Dataset('/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc','r')

lats_river = np.array(river_nc.variables['latitude'])
lons_river = np.array(river_nc.variables['longitude'])

# region masks
region_mask = Dataset('../../make_masks/mask_scb.nc','r')
mask_ssd = np.array(region_mask.variables['mask_ssd'])
mask_nsd = np.array(region_mask.variables['mask_nsd'])*2
mask_oc = np.array(region_mask.variables['mask_oc'])*3
mask_sp = np.array(region_mask.variables['mask_sp'])*4
# my SM mask
mask_sm = np.array(region_mask.variables['mask_sm'])*5
# faycal's SM mask from PNAS paper
#mask_sm = np.transpose(np.array(h5py.File('../masksm.mat','r')['masksm']))
mask_v = np.array(region_mask.variables['mask_v'])*6
mask_sb = np.array(region_mask.variables['mask_sb'])*7

all_regions = np.array((mask_ssd,mask_nsd,mask_oc,mask_sp,mask_sm,mask_v,mask_sb))
all_regions[all_regions==0] = np.nan


# grid
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])

lat_min = 32
lat_max = 34.6
lon_min = -120.5
lon_max = -116.9

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
#for m_i in range(len(all_regions)):
#    ax.contourf(lon_nc,lat_nc,all_regions[m_i],transform=ccrs.PlateCarree(),cmap=colormaps[m_i],vmin=0,vmax=7)
#
ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':20}
gl.ylabel_style = {'size':20}
#ax.add_feature(coast_10m,facecolor='None',edgecolor='k')
#ax.add_feature(cpf.BORDERS,edgecolor='k')

# major rivers
shpfile = '../paper_data_inputs/MajorRiversAndCreeks.shp'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# streams
shpfile = '../paper_data_inputs/fromabel_stream/Streams.shp'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# river dots
m_size = 40
ax.scatter(lons_river,lats_river,s=m_size,marker='^',facecolors='lightgreen',edgecolor='green',lw=1,label='U.S. Rivers',zorder=10)

# POTWs
m_size = 150
maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='maroon',lw=3,label='U.S. Deep Outfalls')
#maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='blue',lw=3)
min_potw_plt = ax.scatter(lons_minor_potw,lats_minor_potw,s=m_size,marker='s',facecolors='none',edgecolor='k',lw=2,label='U.S. Shallow Outfalls')

# mexican beach outfalls
min_potw_plt = ax.scatter([-117.119917,-117.063056],[32.470508,32.346722],s=m_size,marker='s',facecolors='coral',label='Mexican Beach Outfalls')

shpfilename = shpreader.natural_earth(resolution='10m',
                                      category='cultural',
                                      name='admin_0_countries')
reader = shpreader.Reader(shpfilename)

for country in reader.records():
    if country.attributes['NAME'] == 'Mexico':
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor='lightgray', edgecolor='k', linewidth=0.5, zorder=0)
        break

# Original features should be added AFTER the custom geometries
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')
ax.add_feature(cpf.BORDERS,edgecolor='k')

# region names
ax.text(-120.3,34.24,'Santa Barbara Channel',fontsize=axis_tick_size)
ax.text(-119.1,34.21,'Ventura',fontsize=axis_tick_size)
ax.text(-118.7,34.1,'Santa Monica',fontsize=axis_tick_size)
ax.text(-118.36,33.8,'San Pedro',fontsize=axis_tick_size)
ax.text(-118,33.7,'Orange County',fontsize=axis_tick_size)
ax.text(-117.8,32.62,'San Diego',fontsize=axis_tick_size)

ax.text(-118.71,33.85,'HTP',fontsize=axis_tick_size,color='maroon')
ax.text(-118.42,33.59,'JWPCP',fontsize=axis_tick_size,color='maroon')
ax.text(-118.15,33.48,'OC San',fontsize=axis_tick_size,color='maroon')
ax.text(-117.53,32.72,'PLWTP',fontsize=axis_tick_size,color='maroon')
ax.text(-117.68,32.36,'San Antonio de\n los Buenos',fontsize=axis_tick_size,color='coral')
ax.text(-117.6,32.26,'Rosarito Norte',fontsize=axis_tick_size,color='coral')



leg_size = 20
ax.legend(loc='lower left',fontsize=leg_size,labelspacing=1)
ax.set_xlabel('Latitude',fontsize=axis_tick_size)
ax.set_ylabel('Longitude',fontsize=axis_tick_size)
#leg_ax = ax.legend(h2,l2,loc='lower left',fontsize=leg_size,labelspacing=1)
#leg_ax.get_patches()

plt.savefig('figs/inputs_updated_map_noregions_mex.png',bbox_inches='tight')
