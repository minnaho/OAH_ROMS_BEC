#############################################
# plot_atmos_deposition.py
# plot data from 
# atmos_deposition_CMAQ_2002_2012.nc 
#####################################################
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
from matplotlib.colors import LogNorm
import datetime
from netCDF4 import Dataset, date2num, num2date
#import colormaps_ncview as cmaps
from mpl_toolkits.axes_grid1 import make_axes_locatable

###################
# FOLDER PATHS
####################
save_figs_path = './atmos_deposition_figs/'


##################################
# load atmospheric deposition data
##################################
#dataset_name = 'atmos_deposition_CMAQ_2002_2012.nc'
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
dataset_name = 'L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')

grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

oxn = atmos_data.variables['NH4']
redn = atmos_data.variables['NO3']
alk = atmos_data.variables['alk']
fe = atmos_data.variables['fe']


###################################
# PLOTTING
##################################
# lat/lon min and max of grid
'''
#lat_min = lats_a[0,0]
lat_min = 30
#lat_max = lats_a[-1,-1]
lat_max = 50
#lon_min = lons_a[0,-1]
lon_min = -130
lon_max = lons_a[-1,0]
'''
'''
# california zoom
lat_min = 31.5
lat_max = 42.5
lon_min = -125
lon_max = -115
'''


# bight zoom
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)
lat_g0 = np.nanmean(lat_nc)
lon_g0 = np.nanmean(lon_nc)


# map of usw1_grd
#m = Basemap(projection='stere',resolution='h',lat_0=35.5,lon_0=-120,llcrnrlat=lat_nc[0,0],urcrnrlat=lat_nc[Ly-1,Lx-1],llcrnrlon=lon_nc[Ly-1,0],urcrnrlon=lon_nc[0,Lx-1])

# map of domain of data
#m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)

# get xy projected evenly space grid from netcdf lat/lon
# compute map projection coords
#x,y = m(lon_nc,lat_nc)

#######################
# PLOT CLIMATOLOGY
#######################
savename = 'bight_clim.png'
units = 'mmol km$^{-2}$ s$^{-1}$'
subplot_title_font = 16
axis_font = 14
axis_tick_size = 14

fig_h = 8
fig_w = 12
cb_w = 0.01

# number of months in a year
months = 12
# convert m2 to km2
m2_to_km2 = 1E6

# oxidized nitrogen
#cmap_oxn = cmaps.hotres
cmap_oxn = 'gnuplot2_r'
oxn_vmin = 0
oxn_vmax = 8

parallels = np.arange(0,90,1)
meridians = np.arange(180,360,2)


print('NH4')
fig,axes = plt.subplots(3,4,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    oxn_m = oxn[ax_i] 
#    p = m.pcolor(x,y,oxn_m*m2_to_km2,cmap=cmap_oxn,vmin=oxn_vmin,vmax=oxn_vmax)
    p = m.pcolor(x,y,oxn_m*m2_to_km2*mask_nc,cmap=cmap_oxn)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(datetime.date(1990,ax_i+1,1).strftime('%b'),fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 4 or ax_i == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=0.001)
p0 = axes.flat[0].get_position().get_points().flatten()
p1 = axes.flat[-1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p1[2]+0.02,p1[1],cb_w,p0[3]-p1[1]])
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1f')
#cb = fig.colorbar(p,ax=axes.ravel().tolist(),format='%.1f',orientation='vertical')
cb_im.set_label('NH4 ('+units+')',fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
plt.savefig(save_figs_path+'nh4_'+savename,bbox_inches='tight')
plt.close('all')

# NO3
print('NO3')
fig,axes = plt.subplots(3,4,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    redn_m = redn[ax_i] 
    p = m.pcolor(x,y,redn_m*m2_to_km2*mask_nc,cmap=cmap_oxn)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(datetime.date(1990,ax_i+1,1).strftime('%b'),fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 4 or ax_i == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=0.001)
p0 = axes.flat[0].get_position().get_points().flatten()
p1 = axes.flat[-1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p1[2]+0.02,p1[1],cb_w,p0[3]-p1[1]])
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1f')
#cb = fig.colorbar(p,ax=axes.ravel().tolist(),format='%.1f',orientation='vertical')
cb_im.set_label('NO3 ('+units+')',fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
plt.savefig(save_figs_path+'no3_'+savename,bbox_inches='tight')
plt.close('all')


# alk
print('alk')
cmap_alk = 'gnuplot2' 
alk_vmin = -5
alk_vmax = 5
fig,axes = plt.subplots(3,4,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    alk_m = alk[ax_i] 
    p = m.pcolor(x,y,alk_m*m2_to_km2*mask_nc,cmap=cmap_alk)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(datetime.date(1990,ax_i+1,1).strftime('%b'),fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 4 or ax_i == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=0.001)
p0 = axes.flat[0].get_position().get_points().flatten()
p1 = axes.flat[-1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p1[2]+0.02,p1[1],cb_w,p0[3]-p1[1]])
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1f')
#cb = fig.colorbar(p,ax=axes.ravel().tolist(),format='%.1f',orientation='vertical')
cb_im.set_label('Alkalinity ('+units+')',fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
plt.savefig(save_figs_path+'alk_'+savename,bbox_inches='tight')
plt.close('all')

# Fe
print('fe')
fig,axes = plt.subplots(3,4,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    fe_m = fe[ax_i] 
    p = m.pcolor(x,y,fe_m*m2_to_km2*mask_nc,cmap=cmap_oxn)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(datetime.date(1990,ax_i+1,1).strftime('%b'),fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 4 or ax_i == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=0.001)
p0 = axes.flat[0].get_position().get_points().flatten()
p1 = axes.flat[-1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p1[2]+0.02,p1[1],cb_w,p0[3]-p1[1]])
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1e')
#cb = fig.colorbar(p,ax=axes.ravel().tolist(),format='%.1f',orientation='vertical')
cb_im.set_label('Fe ('+units+')',fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
plt.savefig(save_figs_path+'fe_'+savename,bbox_inches='tight')
plt.close('all')


