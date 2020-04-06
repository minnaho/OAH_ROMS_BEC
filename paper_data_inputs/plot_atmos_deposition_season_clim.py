#############################################
# plot_atmos_deposition.py
# plot data from 
# atmos_deposition_CMAQ_2002_2012.nc 
#####################################################
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
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
save_figs_path = './figs/'

setting = 'cal'
#setting = 'bight'

##################################
# load atmospheric deposition data
##################################
#bight
if setting == 'bight':
    grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
    atmos_data = Dataset(dataset_name,'r')
    
    grid_nc = Dataset(grid_path,'r')
    lat_nc = np.array(grid_nc.variables['lat_rho'])
    lon_nc = np.array(grid_nc.variables['lon_rho'])
    mask_nc = np.array(grid_nc.variables['mask_rho'])
    
    oxn = atmos_data.variables['NH4']
    redn = atmos_data.variables['NO3']
    alk = atmos_data.variables['alk']
    fe = atmos_data.variables['fe']

# full california 
if setting == 'cal':
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/atmos_deposition_CMAQ_2002_2012.nc'
    atmos_data = Dataset(dataset_name,'r')
    
    lat_nc = np.array(atmos_data.variables['latitude'])
    lon_nc = np.array(atmos_data.variables['longitude'])
    
    oxn = atmos_data.variables['oxidized_nitrogen']
    redn = atmos_data.variables['reduced_nitrogen']
    alk = atmos_data.variables['alkalinity']
    fe = atmos_data.variables['iron']

season_n = ['Winter','Spring','Summer','Fall']
###################################
# PLOTTING
##################################

# california zoom
if setting=='cal':
    lat_min = 31.5
    lat_max = 42.5
    lon_min = -125
    lon_max = -115
    lat_g0 = np.nanmean(lat_nc)
    lon_g0 = np.nanmean(lon_nc)
# bight zoom with land values
#    lat_min = 31.5
#    lat_max = 35.2
#    lon_max = -116.5
#    lon_min = -122
#    lat_g0 = np.mean([lat_min,lat_max])
#    lon_g0 = np.mean([lon_min,lon_max])

# bight zoom
if setting=='bight':
    lat_min = np.min(lat_nc)
    lat_max = np.max(lat_nc)
    lon_min = np.min(lon_nc)
    lon_max = np.max(lon_nc)
    lat_g0 = np.nanmean(lat_nc)
    lon_g0 = np.nanmean(lon_nc)

#######################
# PLOT CLIMATOLOGY
#######################
if setting=='cal':
    savename = 'cal_clim_season.pdf'
#    savename = 'bight_clim_season.pdf'
    h_space = 0.15
    fig_h = 10
#    fig_w = 12
    fig_w = 8
    plt.ion()
    parallels = np.arange(0,90,2.5)
    meridians = np.arange(180,360,4)
#    parallels = np.arange(0,90,1)
#    meridians = np.arange(180,360,2)

if setting=='bight':
    savename = 'bight_clim.pdf'
    h_space = 0.001
    fig_h = 8
    fig_w = 12
    parallels = np.arange(0,90,1)
    meridians = np.arange(180,360,2)

units = 'mmol km$^{-2}$ s$^{-1}$'
subplot_title_font = 16
axis_font = 14
axis_tick_size = 14

cb_w = 0.01


# convert m2 to km2
m2_to_km2 = 1E6

# oxidized nitrogen
#cmap_oxn = cmaps.hotres
cmap_oxn = 'gnuplot2_r'
oxn_vmin = 0
oxn_vmax = 8


oxn_vmin = 0
oxn_vmax = 3.5
oxn_m = np.empty((12,oxn.shape[1],oxn.shape[2]))
oxn_s = np.empty((4,oxn.shape[1],oxn.shape[2]))
print('NH4')
fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    if setting=='bight':
        oxn_m = oxn[ax_i]*mask_nc
        p = m.pcolor(x,y,oxn_m*m2_to_km2,cmap=cmap_oxn,rasterized=True)
    if setting=='cal':
        for mon_i in range(12):
            oxn_m[mon_i] = np.nanmean(oxn[mon_i::12,:,:],axis=0)
        oxn_s[0] = oxn_m[11]+oxn_m[0]+oxn_m[1]
        oxn_s[1] = oxn_m[2]+oxn_m[3]+oxn_m[4]
        oxn_s[2] = oxn_m[5]+oxn_m[6]+oxn_m[7]
        oxn_s[3] = oxn_m[8]+oxn_m[9]+oxn_m[10]
            
        p = m.pcolor(x,y,oxn_s[ax_i]*m2_to_km2,cmap=cmap_oxn,vmin=oxn_vmin,vmax=oxn_vmax,rasterized=True)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(season_n[ax_i],fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 2: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 1: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=h_space)
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
redn_vmin = 0
redn_vmax = 3.5
cmap_redn = 'gnuplot2_r'
print('NO3')
redn_m = np.empty((12,redn.shape[1],redn.shape[2]))
redn_s = np.empty((4,redn.shape[1],redn.shape[2]))
fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    if setting=='bight':
        redn_m = redn[ax_i]*mask_nc
        p = m.pcolor(x,y,redn_m*m2_to_km2,cmap=cmap_redn,rasterized=True)
    if setting=='cal':
        for mon_i in range(12):
            redn_m[mon_i] = np.nanmean(redn[mon_i::12],axis=0)
        redn_s[0] = redn_m[11]+redn_m[0]+redn_m[1]
        redn_s[1] = redn_m[2]+redn_m[3]+redn_m[4]
        redn_s[2] = redn_m[5]+redn_m[6]+redn_m[7]
        redn_s[3] = redn_m[8]+redn_m[9]+redn_m[10] 
        p = m.pcolor(x,y,redn_s[ax_i]*m2_to_km2,cmap=cmap_redn,vmin=redn_vmin,vmax=redn_vmax,rasterized=True)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(season_n[ax_i],fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 2: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 1: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=h_space)
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
if setting == 'cal':
#    cmap_alk = 'gnuplot2'
    cmap_alk = 'seismic'
if setting == 'bight':
    cmap_alk = 'gnuplot2'
#alk_vmin = -10
#alk_vmax = 0
alk_vmin = -10
alk_vmax = 10
alk_m = np.empty((12,alk.shape[1],alk.shape[2]))
alk_s = np.empty((4,alk.shape[1],alk.shape[2]))
fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    if setting=='bight':
        alk_m = alk[ax_i]*mask_nc
        p = m.pcolor(x,y,alk_m*m2_to_km2,cmap=cmap_alk,rasterized=True)
    if setting=='cal':
        for mon_i in range(12):
            alk_m[mon_i] = np.nanmean(alk[mon_i::12],axis=0)
        alk_s[0] = alk_m[11]+alk_m[0]+alk_m[1]
        alk_s[1] = alk_m[2]+alk_m[3]+alk_m[4]
        alk_s[2] = alk_m[5]+alk_m[6]+alk_m[7]
        alk_s[3] = alk_m[8]+alk_m[9]+alk_m[10]            
#        p = m.pcolor(x,y,alk_s[ax_i]*m2_to_km2,cmap=cmap_alk,rasterized=True)
        p = m.pcolor(x,y,alk_s[ax_i]*m2_to_km2,cmap=cmap_alk,vmin=alk_vmin,vmax=alk_vmax,rasterized=True)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(season_n[ax_i],fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 2: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 1: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=h_space)
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
fe_vmin = 0
fe_vmax = 2E-2
cmap_fe = 'gnuplot2_r'
print('fe')
fe_m = np.empty((12,fe.shape[1],fe.shape[2]))
fe_s = np.empty((4,fe.shape[1],fe.shape[2]))
fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    if setting=='bight':
        fe_m = fe[ax_i]*mask_nc
        p = m.pcolor(x,y,fe_m*m2_to_km2,cmap=cmap_fe,rasterized=True)
    if setting=='cal':
        for mon_i in range(12):
            fe_m[mon_i] = np.nanmean(fe[mon_i::12],axis=0)
        fe_s[0] = fe_m[11]+fe_m[0]+fe_m[1]
        fe_s[1] = fe_m[2]+fe_m[3]+fe_m[4]
        fe_s[2] = fe_m[5]+fe_m[6]+fe_m[7]
        fe_s[3] = fe_m[8]+fe_m[9]+fe_m[10]
            
        p = m.pcolor(x,y,fe_s[ax_i]*m2_to_km2,cmap=cmap_fe,vmin=fe_vmin,vmax=fe_vmax,rasterized=True)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    axes.flat[ax_i].set_title(season_n[ax_i],fontsize=subplot_title_font) 
    if ax_i == 0 or ax_i == 2: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    if ax_i > 1: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 

fig.subplots_adjust(hspace=h_space)
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


