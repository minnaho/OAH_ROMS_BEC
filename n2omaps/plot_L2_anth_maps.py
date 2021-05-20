import sys
import os
sys.path.append(os.path.abspath('/data/project3/minnaho/global/'))
import l2grid
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import pandas as pd
import cmocean as cmocean
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.io import shapereader as shpreader
import cartopy.io.img_tiles as cimgt

#plt.ion()

stamen_terrain = cimgt.Stamen('terrain-background')

month = 8
depth = '300m'

savename = 'n2o_L2_anth_'+depth+'_M'+'%02d'%month+'.png'

if month == 6:
    titlestr = 'June Average ANTH '+depth+' 2013-2017'
if month == 7:
    titlestr = 'July Average ANTH '+depth+' 2013-2017'
if month == 8:
    titlestr = 'August Average ANTH '+depth+' 2013-2017'

file_nc = '/data/project4/minnaho/extract_roms/l2_ap/slices/l2_scb_avg.M'+'%02d'%month+'_2013_2017_'+depth+'.nc'
#v_max = 0.01

if depth == 'surf':
    v_max = 0.005 # surf
if depth == '100m':
    v_max = 0.03 # 100m
if depth == '300m':
    v_max = 0.055 # 300m 


# load n2o file
data_nc = np.squeeze(np.array(Dataset(file_nc,'r').variables['N2O']))
data_nc[data_nc>1E10] = np.nan

# load WCOA 2016 locations
wcoa = pd.read_excel('/data/project1/data/WCOA/WCOA_2007-2016.xlsx',sheet_name='2016')
wcoa_lat = wcoa['Lat']
wcoa_lon = wcoa['Long']

###################################
# load grid
###################################
#grid_nc = l2grid.grid_nc
lat_nc = l2grid.lat_nc
lon_nc = l2grid.lon_nc
h_nc = l2grid.h_nc

lat_min = np.nanmin(lat_nc)
lat_max = np.nanmax(lat_nc)
lon_min = np.nanmin(lon_nc)
lon_max = np.nanmax(lon_nc)


# plot
axis_tick_size = 16

extent = [lon_min,lon_max,lat_min,lat_max]
#rivers_10m = cpf.NaturalEarthFeature('physical','rivers_lake_centerlines','10m')
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
#wsheds = shpreader.Reader('../paper_data_inputs/basin_arcgis/wribasin.shp')

fig_w = 9
fig_h = 10

c_map = cmocean.cm.thermal

fig,ax = plt.subplots(1,1,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))
# plot region masks
plot_im = ax.pcolormesh(lon_nc,lat_nc,data_nc,transform=ccrs.PlateCarree(),cmap=c_map,vmin=0,vmax=v_max)
#plot_im = ax.pcolormesh(lon_nc,lat_nc,data_nc,transform=ccrs.PlateCarree(),cmap=c_map,vmin=0)

# bathymetry contours
h_c1 = [200]
hplt1 = ax.contour(lon_nc,lat_nc,h_nc,h_c1,colors='gray')
ax.clabel(hplt1,colors='gray',inline=True,inline_spacing=1,fmt='%d')

# WCOA cruise line
ax.scatter(wcoa_lon,wcoa_lat,facecolor='None',edgecolor='white',zorder=10)

ax.set_extent(extent)
gl = ax.gridlines(draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':axis_tick_size}
gl.ylabel_style = {'size':axis_tick_size}
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')
ax.add_feature(cpf.BORDERS,edgecolor='k')
p0 = ax.get_position().get_points().flatten()
cb_ax = fig.add_axes([p0[2]+.015,p0[1],.01,p0[3]-p0[1]])
cb = fig.colorbar(plot_im,cax=cb_ax,orientation='vertical')
cb.set_label('N2O mmol/m3',fontsize=axis_tick_size)
cb.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
ax.set_title(titlestr,fontsize=axis_tick_size)
ax.set_ylabel('Latitude',fontsize=axis_tick_size)
ax.set_xlabel('Longitude',fontsize=axis_tick_size)

plt.savefig('./figs/'+savename,bbox_inches='tight')
