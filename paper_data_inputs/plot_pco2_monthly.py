#############################################
# plot_pCO2.py
# plot data from 
# hourly pCO2 data 
#####################################################
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
import datetime
from netCDF4 import Dataset
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cmocean as cmocean
plt.ion()

###################
# FOLDER PATHS
####################
data_path = '/data/project1/minnaho/pCO2/pCO2_avg_monthly.nc'
save_figs_path = './figs/'

##################################
# load pCO2 data
##################################
data_nc = Dataset(data_path,'r')
lat_nc = np.array(data_nc.variables['lat'][0,:,:])
lon_nc = np.array(data_nc.variables['lon'][0,:,:])

# find seasonal clim
pco2_clim = np.empty((4,data_nc['co2ff'][:,0,:,:].shape[1],data_nc['co2ff'][:,0,:,:].shape[2]))

pco2_clim[0] = np.array(data_nc['co2ff'][11,0,:,:]) + np.array(data_nc['co2ff'][0,0,:,:])+ np.array(data_nc['co2ff'][0,1,:,:])
pco2_clim[1] = np.array(data_nc['co2ff'][2,0,:,:]) + np.array(data_nc['co2ff'][3,0,:,:])+ np.array(data_nc['co2ff'][4,1,:,:])
pco2_clim[2] = np.array(data_nc['co2ff'][5,0,:,:]) + np.array(data_nc['co2ff'][6,0,:,:])+ np.array(data_nc['co2ff'][7,1,:,:])
pco2_clim[3] = np.array(data_nc['co2ff'][10,0,:,:]) + np.array(data_nc['co2ff'][9,0,:,:])+ np.array(data_nc['co2ff'][8,1,:,:])

############################
# make Basemap
############################
lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)

# bight zoom
#lat_min = 32
#lat_max = 36
#lon_min = -121.5
#lon_max = -116
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)


###################################
# PLOTTING
##################################
# draw latitude
parallels = np.arange(0,90,1)
# draw longitude
meridians = np.arange(180,360,2)
cb_font = 16
axis_tick_size = 16
#cmap_plot = cmocean.cm.deep
cmap_plot = cmocean.cm.dense

fig_h = 8
fig_w = 8

pco2_vmin = 0
pco2_vmax = 200
cb_w = 0.01
cb_label = 'pCO2 ppmv'
season_n = ['Winter','Spring','Summer','Fall']

savename = 'pco2_clim.pdf'
fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h])
for ax_i in range(len(axes.flat)):
    m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[ax_i])
    x,y = m(lon_nc,lat_nc)
    p = m.pcolor(x,y,pco2_clim[ax_i],cmap=cmap_plot,vmin=pco2_vmin,vmax=pco2_vmax,rasterized=True)
    axes.flat[ax_i].set_title(season_n[ax_i],fontsize=axis_tick_size)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    if ax_i == 0 or ax_i == 2:
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size)
    if ax_i > 1:
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)

p0 = axes.flat[0].get_position().get_points().flatten()
p1 = axes.flat[-1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p1[2]+0.02,p1[1],cb_w,p0[3]-p1[1]])
#cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical',format='%.1f')
cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical')
cb_im.set_label(cb_label,size=cb_font)     
cb_im.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
cb_im.ax.tick_params(axis='both',which='minor',labelsize=axis_tick_size)
fig.subplots_adjust(wspace=0.001)
fig.subplots_adjust(hspace=0.13)
plt.savefig(save_figs_path+savename,bbox_inches='tight')

