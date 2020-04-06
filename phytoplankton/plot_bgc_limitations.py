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
import calendar as calendar
#plt.ion()

depth_str = '_surface'
#depth_str = '_0_40'
#depth_str = '_40_100'

lim_type = ['N_LIM','LIGHT_LIM']

# SP or DIAT
#v_name = 'DIAT'
v_name = 'SP'
#v_name = 'all'

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
data_path = '/data/project4/kesf/Diagnostics/L2SCB_AP/monthly/'
save_figs_path = './figs/'

##################################
# load data
##################################

# load first file to get grid dimensions and make basemap
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid = Dataset(grid_path,'r')
lat_nc = np.array(grid.variables['lat_rho'])
lon_nc = np.array(grid.variables['lon_rho'])
mask_nc = np.array(grid.variables['mask_rho'])
mask_nc[np.where(mask_nc==0)[0],np.where(mask_nc==0)[1]]=np.nan

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
cmap_plot = 'seismic'

fig_h = 7
fig_w = 14

# change year and month of folder that files are in
start_year = 1999
end_year = 2000
# enter as digit month e.g. 1,2,3,...,12
start_month = 9
end_month = 9

for year in list(range(start_year,end_year+1)):
    # if we are on the first year, starts at s_m
    if year == start_year:
        s_m = start_month
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if year == end_year:
        e_m = end_month+1
    else:
        e_m = 13
    for m_i in range(s_m,e_m):
        file_data = data_path+'l2_scb_bgc_flux_avg.Y'+str(year)+'M'+'%02d'%m_i+depth_str+'.nc'
        data_nc = Dataset(file_data,'r')

        fig,axes = plt.subplots(1,len(lim_type),figsize=[fig_w,fig_h],sharey=True)
        for ax in range(len(axes)):
            # make map of domain of data using basemap
            map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes[ax])
            x,y = map_ax(lon_nc,lat_nc)
            if v_name == 'SP' or v_name == 'DIAT':
                l_type = lim_type[ax]
                var_d = np.array(data_nc.variables[var_n[ax]])
            if v_name == 'all':
                l_type = lim_type[ax]
                # DIAZ doesn't have N_LIM
                if ax == 0:
                    var_d = np.array(data_nc.variables['SP_'+l_type])+np.array(data_nc.variables['DIAT_'+l_type])
                else:
                    var_d = np.array(data_nc.variables['SP_'+l_type])+np.array(data_nc.variables['DIAT_'+l_type])+np.array(data_nc.variables['DIAZ_'+l_type])

            # remove fill value of 1E32 (everything is 0-1)
            var_d[var_d>1E10] = np.nan
            # multiply by 100 to get %
            plot_var = np.squeeze((1-var_d)*100)*mask_nc
            p = map_ax.pcolor(x,y,plot_var,cmap=cmap_plot,vmin=var_vmin,vmax=var_vmax)
            map_ax.drawstates()
            map_ax.drawcountries()
            map_ax.drawcoastlines()
            map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
            map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
            axes[ax].xaxis.set_label_position('top')
            axes[ax].set_xlabel(l_type,fontsize=axis_font)

        if depth_str == '_surface':
            plot_title = calendar.month_name[m_i]+' '+v_name+' % Limitation at surface'
        if depth_str == '_0_40' or depth_str == '_40_100':
            plot_title = calendar.month_name[m_i]+' '+v_name+' % Limitation Averaged '+depth_str+' m'
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
        save_fig_name = v_name+depth_str+'_Y'+str(year)+'M'+'%02d'%m_i+'_limitation.png'
        plt.savefig(save_figs_path+save_fig_name,bbox_inches='tight')
        print('saved fig '+save_figs_path+save_fig_name)
        plt.close('all')

###########
# seasonal
###########
#spring
m_files0 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y2000M0[3-5]'+depth_str+'.nc')
m_files1 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y2000M0[6-8]'+depth_str+'.nc')
m_files2_1 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y1999M09'+depth_str+'.nc')
m_files2_2 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y1999M1[0-1]'+depth_str+'.nc')
m_files2_3 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y2000M09'+depth_str+'.nc')
m_files2 = m_files2_1+m_files2_2+m_files2_3
m_files3_1 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y1999M12'+depth_str+'.nc')
m_files3_2 = glob.glob(data_path+'l2_scb_bgc_flux_avg.Y2000M0[1-2]'+depth_str+'.nc')
m_files3 = m_files3_1+m_files3_2

seasons = [m_files0,m_files1,m_files2,m_files3]
season_str = ['Spring','Summer','Fall','Winter']

var_l = []
for s_i in range(len(seasons)):
    fig,axes = plt.subplots(1,len(lim_type),figsize=[fig_w,fig_h],sharey=True)
    for ax in range(len(axes)):
        map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes[ax])
        x,y = map_ax(lon_nc,lat_nc)
        # append model data then average
        for f_i in seasons[s_i]:
            data_nc = Dataset(f_i,'r')
            var_l.append(np.squeeze(np.array(data_nc.variables[var_n[ax]])))

        season_avg = np.nanmean(np.array(var_l),axis=0)
        # remove fill value of 1E32 (everything is 0-1)
        season_avg[season_avg>1E10] = np.nan
        # multiply by 100 to get %
        plot_var = np.squeeze((1-season_avg)*100)*mask_nc
        p = map_ax.pcolor(x,y,plot_var,cmap=cmap_plot,vmin=var_vmin,vmax=var_vmax)
        map_ax.drawstates()
        map_ax.drawcountries()
        map_ax.drawcoastlines()
        map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        axes[ax].xaxis.set_label_position('top')
        axes[ax].set_xlabel(lim_type[ax],fontsize=axis_font)
    if depth_str == '_surface':
        title_d_str = ' at surface'
    if depth_str == '_0_40': 
        title_d_str = 'Averaged 0 to 40 m'
    if depth_str == '_40_100':
        title_d_str = 'Averaged 40 to 100 m'
    if v_name == 'SP':
        title_v_str = 'Small Phytoplankton'
    if v_name == 'DIAT':
        title_v_str = 'Diatom'
    plot_title = season_str[s_i]+' '+title_v_str+' % Limitation '+title_d_str
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
    save_fig_name = v_name+depth_str+'_'+season_str[s_i]+'_limitation.png'
    plt.savefig(save_figs_path+save_fig_name,bbox_inches='tight')
    print('saved fig '+save_figs_path+save_fig_name)
    plt.close('all')
