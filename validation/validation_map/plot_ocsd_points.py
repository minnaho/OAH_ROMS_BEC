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
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker



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
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')

lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
h_nc = np.array(grid_nc.variables['h'])

lat_min = 33.45
lat_max = 33.71
lon_min = -118.4
lon_max = -117.7

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

# major rivers
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/MajorRiversAndCreeks'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# streams
shpfile = '/data/project1/minnaho/inputs_update_plotting/paper_data_inputs/fromabel_stream/Streams'
rivershp = cpf.ShapelyFeature(shpreader.Reader(shpfile).geometries(),ccrs.PlateCarree(),edgecolor='dodgerblue',facecolor='None',alpha=0.5)
ax.add_feature(rivershp)

# POTW monitoring

lon_potw = np.array(lon_v[nan_ind[6]+1:nan_ind[7]])
lat_potw = np.array(lat_v[nan_ind[6]+1:nan_ind[7]])

m_size_small = 40
#central = ax.scatter(lon_v[nan_ind[6]+1:nan_ind[7]],lat_v[nan_ind[6]+1:nan_ind[7]],s=m_size_small,marker='o',color=central_c,label=data_sources[3],edgecolor='navy')

# oxnard
#v_ind = np.where(lon_potw<-118.85)[0]
#ax.scatter(lon_potw[v_ind],lat_potw[v_ind],s=m_size_small,marker='o',color='lightblue',label='City of Oxnard Stations',edgecolor='navy')

# city of LA
#c_ind = np.where((lon_potw>-118.85)&(lat_potw>33.78))[0]
#ax.scatter(lon_potw[c_ind],lat_potw[c_ind],s=m_size_small,marker='o',color='palegreen',label='City of LA Stations',edgecolor='darkgreen')

# LACSD
#l_ind = np.where(((lon_potw<-118.129032)&(lat_potw>33.629462)&(lat_potw<33.783))|((lon_potw<-118.12464)&(lat_potw>33.629462)&(lat_potw<33.783))|((lon_potw<-118.111321)&(lat_potw>33.721832)&(lat_potw<33.783)))[0]
#ax.scatter(lon_potw[l_ind],lat_potw[l_ind],s=m_size_small,marker='o',color='lightcoral',label='LACSD Stations',edgecolor='maroon')

#OCSD
o_ind = np.where(((lon_potw>-118.12464)&(lat_potw<33.629462)&(lat_potw>33.3))|((lon_potw>-118.111321)&(lat_potw<33.721832)&(lat_potw>33.3)))[0]
ax.scatter(lon_potw[o_ind],lat_potw[o_ind],s=m_size_small,marker='o',color='orange',label='OCSD Stations',edgecolor='k')
h_c = [30,50,100,200,300]
h_plt = ax.contour(lon_nc,lat_nc,h_nc,h_c,colors='k')
ax.clabel(h_plt,fontsize=9,inline=True,fmt='%d')

# San Diego
#s_ind = np.where(lat_potw<33)[0]
#ax.scatter(lon_potw[s_ind],lat_potw[s_ind],s=m_size_small,marker='o',color='orchid',label='City of San Diego Stations',edgecolor='k')

# SMBO
#m_size = 100
#ax.scatter(-118.7051,33.9330,s=m_size,marker='*',facecolors='aqua',edgecolor='k',label='SMBO')

# SPOT
#ax.scatter(-118.3996,33.5061,s=m_size,marker='P',facecolors='darkorchid',edgecolor='k',label='SPOT')

# oc mooring
#m_size = 50
#ax.scatter(oc_lon,oc_lat,s=m_size,marker='o',facecolor='None',edgecolor='teal',linewidth=3,label='OC-T-1 ADCP')

# la mooring
#m_size = 50
#ax.scatter(la_lon,la_lat,s=m_size,marker='X',color='teal',edgecolor='k',label='LACSD A3 ADCP')

# calcofi
# fake plot for legend
#ax.scatter([],[],marker=(6,2,0),s=80,color='blue',label='CalCOFI')

# calcofi line 83.3 station 42
#star_font = 20
#ax.text(-119.51,34.18,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-119.57,34.12,'83.3',fontsize=14,color='blue')
##ax.scatter(-119.51,34.18,marker='d',s=m_size,color='blue')
#
## calcofi line 86.7
#cal_86_lon = [-118.49, -118.63, -118.98, -119.32, -119.66, -120.01, -120.35]
#cal_86_lat = [33.89, 33.82, 33.66, 33.49, 33.32, 33.16, 32.99]
#ax.plot(cal_86_lon,cal_86_lat,'blue')
#ax.text(-118.49,33.89,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.63,33.82,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.98,33.66,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.98,33.62,'    86.7',fontsize=14,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-119.32,33.49,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-119.66,33.32,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-120.01,33.16,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-120.35,32.99,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#
## calcofi line 90
#cal_90_lon = [-117.77, -117.91, -118.25, -118.94, -119.48, -119.96]
#cal_90_lat = [33.49, 33.42, 33.25, 32.92, 32.65, 32.42]
#ax.plot(cal_90_lon,cal_90_lat,'blue')
#ax.text(-117.77,33.49,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-117.91,33.42,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.25,33.25,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.25,33.21,'    90',fontsize=14,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-118.94,32.92,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-119.48,32.65,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#ax.text(-119.96,32.42,'*',fontsize=star_font,color='blue',verticalalignment='center',horizontalalignment='center')
#
#ax.text(-120.45,34.24,'Santa Barbara Channel',fontsize=axis_tick_size)
#ax.text(-119.2,34.18,'Ventura',fontsize=axis_tick_size)
#ax.text(-118.7,34.11,'Santa Monica',fontsize=axis_tick_size)
##ax.text(-118.4,33.51,'SP',fontsize=axis_tick_size)
#ax.text(-118.37,33.8,'San Pedro',fontsize=axis_tick_size)
#ax.text(-118.05,33.73,'Orange County',fontsize=axis_tick_size)
#ax.text(-117.9,32.6,'San Diego',fontsize=axis_tick_size)

#ax.text(-0.07, 0.55, 'Latitude', va='bottom', ha='center',
#        rotation='vertical', rotation_mode='anchor',
#        transform=ax.transAxes,fontsize=axis_tick_size+4)
#ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
#        rotation='horizontal', rotation_mode='anchor',
#        transform=ax.transAxes,fontsize=axis_tick_size+4)

step_lon = 0.1
step_lat = 0.1
gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':axis_tick_size}
gl.ylabel_style = {'size':axis_tick_size}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')
gl.xlocator = mticker.FixedLocator(list(np.arange(lon_min,lon_max+step_lon,step_lon)))
gl.ylocator = mticker.FixedLocator(list(np.arange(lat_min,lat_max+step_lat,step_lat)))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.set_extent(extent)


plt.savefig('figs/ocsd_obs_contour.png',bbox_inches='tight')
