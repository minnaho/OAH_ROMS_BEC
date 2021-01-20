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
import pandas as pd

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

v_data = pd.read_csv('validation_metadata.csv',header=None,skiprows=1)
lat_v = v_data[1]
lon_v = v_data[2]
nan_ind = np.where(np.isnan(lat_v))[0]

#oc mooring
oc_lat = 33.5735817
oc_lon = -118.00443268

# la mooring
la_lat = 33.73283
la_lon = -118.41

data_sources = ['LACSD moorings','OCSD ADCP','San Diego ADCP','POTW Monitoring','CalCOFI (bgc)','POTW stations (profiles)']


# grid
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])

lat_min = 32.4
lat_max = 34.6
lon_min = -120.5
lon_max = -117

###################
# plot inputs only
###################
axis_tick_size = 16

extent = [lon_min,lon_max,lat_min,lat_max]
rivers_10m = cpf.NaturalEarthFeature('physical','rivers_lake_centerlines','10m')
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
wsheds = shpreader.Reader('/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/basin_arcgis/wribasin.shp')

fig_w = 15
fig_h = 12

colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':20}
gl.ylabel_style = {'size':20}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')

# major rivers
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/MajorRiversAndCreeks'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# streams
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/fromabel_stream/Streams'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# river dots
m_size = 40
ax.scatter(lons_river,lats_river,s=m_size,marker='^',facecolors='lightgreen',edgecolor='green',lw=1,label='River',zorder=10)

# POTWs
m_size = 150
maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='maroon',lw=3,label='Large POTW')
#maj_potw_plt = ax.scatter(lons_major_potw,lats_major_potw,s=m_size,marker='o',facecolors='none',edgecolor='blue',lw=3)
min_potw_plt = ax.scatter(lons_minor_potw,lats_minor_potw,s=m_size,marker='s',facecolors='none',edgecolor='k',lw=2,label='Small POTW')
ax.text(-118.67,33.85,'HTP',color='maroon',fontsize=axis_tick_size-2)
ax.text(-118.5,33.58,'JWPCP',color='maroon',fontsize=axis_tick_size-2)
ax.text(-118.1,33.47,'OCSD',color='maroon',fontsize=axis_tick_size-2)
ax.text(-117.56,32.68,'PLWTP',color='maroon',fontsize=axis_tick_size-2)


ax.text(-120.3,34.24,'Santa Barbara',fontsize=axis_tick_size)
ax.text(-119.2,34.18,'Ventura',fontsize=axis_tick_size)
ax.text(-118.7,34.11,'Santa Monica',fontsize=axis_tick_size)
#ax.text(-118.4,33.51,'SP',fontsize=axis_tick_size)
ax.text(-118.37,33.8,'San Pedro',fontsize=axis_tick_size)
ax.text(-118.05,33.73,'Orange County',fontsize=axis_tick_size)
ax.text(-117.9,32.88,'San Diego',fontsize=axis_tick_size)

ax.text(-0.07, 0.55, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes,fontsize=axis_tick_size+4)
ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes,fontsize=axis_tick_size+4)

leg_size = 16
ax.legend(loc='lower left',fontsize=leg_size,labelspacing=1)

plt.savefig('figs/validation_updated_map_inputs.png',bbox_inches='tight')

###################
# plot monitoring only
###################
axis_tick_size = 16

extent = [lon_min,lon_max,lat_min,lat_max]
rivers_10m = cpf.NaturalEarthFeature('physical','rivers_lake_centerlines','10m')
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
wsheds = shpreader.Reader('/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/basin_arcgis/wribasin.shp')

fig_w = 15
fig_h = 12

colormaps = [cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal,cmocean.cm.thermal]

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':20}
gl.ylabel_style = {'size':20}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')

# major rivers
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/MajorRiversAndCreeks'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# streams
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/fromabel_stream/Streams'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# POTW monitoring
central_c = 'lightblue'
m_size_small = 40
central = ax.scatter(lon_v[nan_ind[6]+1:nan_ind[7]],lat_v[nan_ind[6]+1:nan_ind[7]],s=m_size_small,marker='o',color=central_c,label=data_sources[3],edgecolor='navy')

# SMBO
ax.scatter(-118.7051,33.9330,s=m_size,marker='X',facecolors='aqua',edgecolor='k',label='SMBO')

# SPOT
ax.scatter(-118.3996,33.5061,s=m_size,marker='P',facecolors='darkorchid',edgecolor='k',label='SPOT')

# oc mooring
m_size = 50
ax.scatter(oc_lon,oc_lat,s=m_size,marker='o',facecolor='None',edgecolor='teal',linewidth=3,label='OC-T-1')

# la mooring
m_size = 50
ax.scatter(la_lon,la_lat,s=m_size,marker='x',color='teal',linewidth=3,label='OC-T-1')

#calcofi = m.scatter(x_coords[nan_ind[8]+1:nan_ind[9]],y_coords[nan_ind[8]+1:nan_ind[9]],s=m_size_small,marker='o',color=calcofi_c,label=data_sources[4])

ax.text(-120.3,34.24,'Santa Barbara',fontsize=axis_tick_size)
ax.text(-119.2,34.18,'Ventura',fontsize=axis_tick_size)
ax.text(-118.7,34.11,'Santa Monica',fontsize=axis_tick_size)
#ax.text(-118.4,33.51,'SP',fontsize=axis_tick_size)
ax.text(-118.37,33.8,'San Pedro',fontsize=axis_tick_size)
ax.text(-118.05,33.73,'Orange County',fontsize=axis_tick_size)
ax.text(-117.9,32.88,'San Diego',fontsize=axis_tick_size)

ax.text(-0.07, 0.55, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes,fontsize=axis_tick_size+4)
ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes,fontsize=axis_tick_size+4)

leg_size = 16
ax.legend(loc='lower left',fontsize=leg_size,labelspacing=1)

plt.savefig('figs/validation_updated_map_obs.png',bbox_inches='tight')
