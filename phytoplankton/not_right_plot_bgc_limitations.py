#############################################
# plot nutrient and light limitation
# from L2 model anthropogenic
#####################################################
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset, date2num, num2date, MFDataset
#import colormaps_ncview as cmaps
from mpl_toolkits.axes_grid1 import make_axes_locatable
import glob
import depths as depths
from time import strptime
#plt.ion()

# SP or DIAT
v_name = 'DIAT'

# depth 
d_i = -3

# slice or average from surface to that depth
method = 'slice'

# bounds for colormap in % limitation
var_vmin = 0
var_vmax = 100

if v_name == 'SP':
    var_n = ['SP_N_LIM','SP_LIGHT_LIM']

if v_name == 'DIAT':
    var_n = ['DIAT_N_LIM','DIAT_LIGHT_LIM']

###################
# FOLDER PATHS
####################
data_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/clim/'
save_figs_path = './figs/'

##################################
# load data
##################################
dataset = 'l2_scb_bgc_flux_avg.M??_1997_2000_bgc_limitation.nc'
file_names = sorted(glob.glob(data_path+dataset))

# load first file to get grid dimensions and make basemap
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid = Dataset(grid_path,'r')
lat_nc = np.array(grid.variables['lat_rho'])
lon_nc = np.array(grid.variables['lon_rho'])

############################
# make Basemap
############################
lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)
'''
# bight zoom
lat_min = 32
lat_max = 36
lon_min = -121.5
lon_max = -116
'''
# whole domain
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)


# draw latitude
parallels = np.arange(0,90,1)
# draw longitude
meridians = np.arange(180,360,1)
###################################
# PLOTTING
##################################
title_font = 20
cb_font = 16
axis_font = 16
axis_tick_size = 14
cmap_plot = 'viridis_r'

fig_h = 7
fig_w = 14

months = ['January','February','March','April','May','June','July','August','September','October','November','December']

for f_i in range(len(file_names)):
    print('loading data '+file_names[f_i])
    data = Dataset(file_names[f_i],'r')
    [z_sigmas,Cs] = depths.get_depths(file_names[f_i],grid_path,0,'r','new')
    # get indices for all depths outside of 0-desired depth 
    # to set to np.nan later and average over
    if method == 'average':
#        inds = np.array(np.where(~((z_sigmas>d_i) & (z_sigmas<1)))).transpose()
        inds = np.array(np.where(~((z_sigmas>d_i) & (z_sigmas<1))))
        plot_title = months[f_i] +' '+ v_name + ' % Limitation Averaged 0'+str(d_i)+' m'
    # get indices for all depths outside of desired value to set to np.nan later
    if method == 'slice':
#        inds = np.array(np.where(~((z_sigmas>d_i-1) & (z_sigmas<d_i+1)))).transpose()
        inds = np.array(np.where(~((z_sigmas>d_i-1) & (z_sigmas<d_i+1))))
        plot_title = months[f_i] +' '+ v_name + ' % Limitation at '+str(d_i*-1)+' m'

    fig,axes = plt.subplots(1,len(var_n),figsize=[fig_w,fig_h],sharey=True)
    #fig,axes = plt.subplots(1,len(var_n),sharey=True)

    for ax in range(len(axes)):
        # make map of domain of data using basemap
        map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes[ax])
        # get xy projected evenly space grid from netcdf lat/lon
        # compute map projection coords
        x,y = map_ax(lon_nc,lat_nc)
        var_d = np.array(data.variables[var_n[ax]][0])
        # remove fill value of 1E32
        var_d[var_d>2] = np.nan
        # set grid cells that are outside of depth range to nan
        var_d[inds[0],inds[1],inds[2]] = np.nan
        # multiply by 100 to get %
        plot_var = np.nanmean(var_d,axis=0)*100
        p = map_ax.pcolor(x,y,plot_var,cmap=cmap_plot,vmin=var_vmin,vmax=var_vmax)
        map_ax.drawstates()
        map_ax.drawcountries()
        map_ax.drawcoastlines()
        map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        axes[ax].xaxis.set_label_position('top')
        axes[ax].set_xlabel(var_n[ax],fontsize=axis_font)

    p0 = axes[0].get_position().get_points().flatten()
    p1 = axes[1].get_position().get_points().flatten()
    cb_ax = fig.add_axes([p0[0],0,p1[2]-p0[0],.04])
    cb = fig.colorbar(p,cax=cb_ax,orientation='horizontal')
    cb.set_label('% limitation',fontsize=axis_font)
    cb.ax.tick_params(labelsize=axis_tick_size)
    #plt.subplots_adjust(top=.99)
    plt.suptitle(plot_title,fontsize=axis_font)
    cb.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='minor',labelsize=axis_tick_size)
    fig.tight_layout()
    save_fig_name = v_name+'_'+method+'_'+'%02d'%strptime(months[f_i],'%B').tm_mon+'_'+str(d_i*-1)+'_limitation.png'
    plt.savefig(save_figs_path+save_fig_name,bbox_inches='tight')
    print('saved fig '+save_figs_path+save_fig_name)
    plt.close('all')
