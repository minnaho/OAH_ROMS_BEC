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

#setting = 'cal'
setting = 'bight'

##################################
# load atmospheric deposition data
##################################
#bight
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')

grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14


oxn  = np.array(atmos_data.variables['NH4'])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
redn = np.array(atmos_data.variables['NO3'])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
alk  = np.array(atmos_data.variables['alk'])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
fe   = np.array(atmos_data.variables['fe'])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

tn_plt = oxn+redn

season_n = ['Winter','Spring','Summer','Fall']
###################################
# PLOTTING
##################################


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
    savename = 'atmos_bight_clim_tn.pdf'
    h_space = 0.001
    fig_h = 12
    fig_w = 12
    parallels = np.arange(0,90,1)
    meridians = np.arange(180,360,2)

units = 'kg N m$^{-2}$ month$^{-1}$'
subplot_title_font = 16
axis_font = 14
axis_tick_size = 14

cb_w = 0.01

#plt.ion()
# oxidized nitrogen
#cmap_oxn = cmaps.hotres
cmap_oxn = 'gnuplot2_r'

v_min = 0
v_max = 2E-4

tn_s = np.empty((4,oxn.shape[1],oxn.shape[2]))
tn_s[0] = tn_plt[11]+tn_plt[0]+tn_plt[1]
tn_s[1] = tn_plt[2]+tn_plt[3]+tn_plt[4]
tn_s[2] = tn_plt[5]+tn_plt[6]+tn_plt[7]
tn_s[3] = tn_plt[8]+tn_plt[9]+tn_plt[10]

fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_g0,lon_0=lon_g0,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    p = m.pcolor(x,y,tn_s[ax_i],cmap=cmap_oxn,vmin=v_min,vmax=v_max,rasterized=True)
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
#cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1f')
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.2E')
#cb = fig.colorbar(p,ax=axes.ravel().tolist(),format='%.1f',orientation='vertical')
cb_im.set_label(units,fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
fig.savefig(save_figs_path+savename,bbox_inches='tight')
