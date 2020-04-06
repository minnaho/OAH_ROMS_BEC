############################
# plot Faycal's pteropods 
# experiments from L1 grid
# file contains
# duration
# severity
# intensity
# frequency
# recovery
#############################
from netCDF4 import Dataset, num2date
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from mpl_toolkits.axes_grid1 import make_axes_locatable
import colormaps_ncview as cmaps
import cmocean
from pycpt.load import gmtColormap # get color map from .cpt files
#plt.ion()

######################
# .cpt file path
######################
cpt_path = '/data/project3/kesf/tools_matlab/matlab_paths/cptcmap/cptfiles/'

cpt_path = '/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/'


###################
# bounds of plot
###################
y0 = 50
yE = 650
x0 = 440
xE = 770

###########
# load grid
###########
path_grid = '/data/project3/kesf/ROMS/USSW1/grid/usw1_grd.nc'
grid_nc = Dataset(path_grid,'r')
mask_grid = grid_nc.variables['mask_rho'][:,:]
mask = np.copy(mask_grid)
lat_grid = grid_nc.variables['lat_rho'][:,:]
lon_grid = grid_nc.variables['lon_rho'][:,:]
h_nc = grid_nc.variables['h'][:,:]
h_grid = h_nc[y0:yE,x0:xE]

#############################
# load pteropods experiments
#############################
path_data = '/data/project3/kesf/tools_matlab/applications/pteropods/'
'''
exp_files = ['pteropods_eggdev_2001.nc',
             'pteropods_shelldiss_mild_juvenile_2001.nc',
             'pteropods_survival_adult_2001.nc'
            ]
'''

'''
exp_files = ['pteropods_calcification_juvenile_2001.nc',
             'pteropods_growth_juvenile_2001.nc',
             'pteropods_shelldiss_severe_juvenile_2001.nc',
            ]
'''
'''
exp_files = ['pteropods_survival_adult_2001.nc',
             'pteropods_shelldiss_mild_adult_2001.nc',
             'pteropods_shelldiss_severe_adult_2001.nc',
             'pteropods_growth_adult_2001.nc'
            ]
'''

exp_files = ['pteropods_calcification_adult_2001_2002.nc',
             'pteropods_growth_adult_2001_2002.nc',
             'pteropods_survival_adult_2001_2002.nc'
             ]

'''
exp_files = ['pteropods_shelldiss_severe_adult_2001_2002.nc',
             'pteropods_shelldiss_mild_adult_2001_2002.nc'
             ]
'''

'''
exp_files = ['pteropods_shelldiss_severe_adult_2001_2002.nc',
             'pteropods_shelldiss_mild_adult_2001_2002.nc'
             ]
'''
'''
exp_variables = ['Duration',
                 'Recovery',                
                 'Frequency',
                 'Intensity',
                 'Severity']
'''

exp_variables = ['Intensity',
                 'Duration',
                 'Severity']

#omega_avg_file = 'om_juranek_L1_30m_2001.nc'
omega_avg_file = 'om_juranek_L1_200m_2001.nc'
#omega_avg_file = 'om_juranek_L1_200m_2001_2002.nc'
omega_avg_nc = Dataset(path_data+omega_avg_file,'r')
omega_avg = np.transpose(omega_avg_nc.variables['var'][0,:,:])


######################
# plot using grid
#####################
bounds = [440,770,50,650]
save_figs_path = '/data/project1/minnaho/pteropods/pteropod_figs/'


title_font = 20
cb_font = 16
axis_tick_size = 14
subplot_title_font = 16
axis_font = 15

fig_w = 16
fig_h = 8


baths = [5]

# loop over each experiment
for exp in exp_files:
    print('plotting '+str(exp))
    fig = plt.figure(figsize=[fig_w,fig_h])
    # loop over each variable to make maps
    for i,var in enumerate(exp_variables):
        nc_data = Dataset(path_data+exp,'r')
        variable_data_tr = np.transpose(nc_data.variables[var][:,:])
        variable_data = variable_data_tr[y0:yE,x0:xE]*mask[y0:yE,x0:xE]
        variable_data[variable_data==0]=np.nan
        # make land white by setting values to nan
        #variable_data[h_grid<5] = np.nan
        # create subplots for each map and put it on one figure for each experiment
        ax = fig.add_subplot(1,3,i+1)
        ax.set_title(var,fontsize=subplot_title_font) 
        plt.contour(h_grid,baths,colors='k',linewidths=1)

        if var == 'Duration':
            #cmap_plot = cmaps.ssec
            cmap_plot = 'YlGnBu' 
            vmin_plot = 0
            if '2001.nc' in exp:
                vmax_plot = 60 
            if 'egg' in exp:
                vmax_plot = 30
            if '2002' in exp:
                vmax_plot = 273
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot,extent=bounds)
            plt.xlim([x0,xE])
            plt.ylim([y0,yE])
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Total Time below Threshold (days)',fontsize=axis_font)

        if var == 'Recovery':
            #cmap_plot = cmaps.ssec_r
            #cmap_plot = 'cool'
            cmap_plot = 'YlGnBu' 
            vmin_plot = 0
            vmax_plot = 50
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Number of Days',fontsize=axis_font)

        if var == 'Frequency': 
            #cmap_plot = 'rainbow'
            cmap_plot = 'YlGnBu' 
            vmin_plot = 0
            vmax_plot = 1
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Number of Events',fontsize=axis_font)

        if var == 'Intensity': 
            #cmap_plot = cmaps.ssec
            cmap_plot = 'gist_rainbow'
            #cmap_plot = cmocean.cm.haline 
            vmin_plot = 0
            if exp == 'pteropods_eggdev_2001.nc':
                vmax_plot = .06
            if exp == 'pteropods_shelldiss_mild_juvenile_2001.nc':
                vmax_plot = .66
            if exp == 'pteropods_survival_adult_2001.nc':
                vmax_plot = .2
   
            if exp == 'pteropods_calcification_adult_2001_2002.nc' or exp == 'pteropods_growth_adult_2001_2002.nc' or exp == 'pteropods_survival_adult_2001_2002.nc':
                vmax_plot = .22

            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot,extent=bounds)
            plt.xlim([x0,xE])
            plt.ylim([y0,yE])
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Omega',fontsize=axis_font)

        if var == 'Severity': 
            #cmap_plot = cmaps.ssec
            #cmap_plot = 'YlGnBu' 
            cmap_plot = 'gist_rainbow' 
            vmin_plot = 0
            if exp == 'pteropods_eggdev_2001.nc':
                vmax_plot = 1.8
            if exp == 'pteropods_shelldiss_mild_juvenile_2001.nc':
                vmax_plot = 45
            if exp == 'pteropods_survival_adult_2001.nc':
                vmax_plot = 15
            if exp == 'pteropods_calcification_adult_2001_2002.nc' or exp == 'pteropods_growth_adult_2001_2002.nc' or exp == 'pteropods_survival_adult_2001_2002.nc':
                vmax_plot = 60
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot,extent=bounds)
            plt.xlim([x0,xE])
            plt.ylim([y0,yE])
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Omega day',fontsize=axis_font)

        cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
        ##divider = make_axes_locatable(a)
        ##cax = divider.append_axes("right", size="5%", pad=0.5)  

    # plot omega averaged as 6th map
#    ax = fig.add_subplot(1,3,3)
#    if omega_avg_file == 'om_juranek_L1_200m_2001.nc':
#        ax.set_title('Omega Averaged over 1 Year',fontsize=subplot_title_font) 
#    if omega_avg_file == 'om_juranek_L1_200m_2001_2002.nc':
#        ax.set_title('Omega Averaged over 2 Years',fontsize=subplot_title_font) 
#    plt.contour(h_grid,baths,colors='k')
#    p = plt.imshow(omega_avg,cmap='gist_rainbow',origin='lower')
#    plt.grid(True)
#    ax.xaxis.set_visible(False)
#    ax.yaxis.set_visible(False)
#    a = plt.gca()
#    cb = fig.colorbar(p,ax=ax)
#    cb.set_label('Omega',fontsize=axis_font)
#    cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
#    cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

    plt.tight_layout()
    plt.suptitle(exp[:exp.index('.')],fontsize=title_font)
    plt.subplots_adjust(top=.93)
    plt.savefig(save_figs_path+exp[:exp.index('.')]+'.png',bbox_inches='tight')
    plt.close('all')

'''
#############################
# make basemap to plot nicely
#############################
lat_mean = np.mean(lat_grid)
lon_mean = np.mean(lon_grid)

lat_min = 31.5
lat_max = 42.5
lon_min = -127
lon_max = -115


# draw latitude
parallels = np.arange(0,90,2)
# draw longitude
meridians = np.arange(180,360,2)

#m = Basemap(projection='stere',resolution='l',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)

lat_mean = 34
lon_mean = -122
cali_height = 1200000
cali_width = 1000000
#m = Basemap(projection='aeqd',resolution='l',lat_0=lat_mean,lon_0=lon_mean,width=cali_width,height=cali_height)

m = Basemap(projection='rotpole',resolution='l',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,o_lon_p=-122,o_lat_p=35)


# get xy projected evenly space grid from netcdf lat/lon
# compute map projection coords
#x,y = m(lon_grid,lat_grid)
#######################
# plot each experiment
#######################
save_figs_path = '/data/project1/minnaho/pteropods/pteropod_figs/'


title_font = 20
cb_font = 16
axis_tick_size = 15
subplot_title_font = 16
axis_font = 15

fig_h = 14
fig_w = 8

cmap_plot = 'rainbow'

d_vmin = 0

# loop over each experiment
for exp in exp_files:
    print('plotting '+str(exp))
    fig = plt.figure(figsize=[fig_w,fig_h])
    # loop over each variable to make maps
    for i,var in enumerate(exp_variables):
        nc_data = Dataset(path_data+exp,'r')
        variable_data = np.transpose(nc_data.variables[var][:,:])
        # create subplots for each map and put it on one figure for each experiment
        ax = fig.add_subplot(3,2,i+1)
        ax.set_title(var,fontsize=subplot_title_font) 
        #p = m.pcolor(x,y,variable_data,cmap=cmap_plot)
        p = m.imshow(variable_data,cmap=cmap_plot)
        m.drawstates()
        m.drawcountries()
        m.drawcoastlines()
        # draw latitude
        if i == 0 or i == 2 or i == 4: 
            m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        else:
            m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
        # draw longitude
        if i > 2: 
            m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        else:
            m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)       
        a = plt.gca()
        cb = fig.colorbar(p,format='%.1f',ax=ax)
        #cb.set_label('Iron (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
        #cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        #cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
        ##divider = make_axes_locatable(a)
        ##cax = divider.append_axes("right", size="5%", pad=0.5)  
    plt.tight_layout()
    plt.suptitle(exp,fontsize=title_font)
    plt.subplots_adjust(top=.93)
    plt.savefig(save_figs_path+exp+'.png',bbox_inches='tight')
    plt.close('all')
'''
'''
# loop over each experiment
for exp in exp_files:
    print('plotting '+str(exp))
    fig = plt.figure(figsize=[fig_w,fig_h])
    # loop over each variable to make maps
    for i,var in enumerate(exp_variables):
        nc_data = Dataset(path_data+exp,'r')
        variable_data = np.transpose(nc_data.variables[var][:,:])
        # create subplots for each map and put it on one figure for each experiment
        ax = fig.add_subplot(3,2,i+1)
        ax.set_title(var,fontsize=subplot_title_font) 
        p = m.pcolor(x,y,variable_data,cmap=cmap_plot)
        m.drawstates()
        m.drawcountries()
        m.drawcoastlines()
        # draw latitude
        if i == 0 or i == 2 or i == 4: 
            m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        else:
            m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
        # draw longitude
        if i > 2: 
            m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        else:
            m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)       
        a = plt.gca()
        # add axes at position [left,bottom,width,height] in fractions of figure width and height
        cax = fig.add_axes([.93,.025,.04,.9])
        #fig.subplots_adjust(right=0.9)
        # plot colorbar in new axes position
        cb = fig.colorbar(p,format='%.1f',cax=cax)
        #cb.set_label('Iron (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
        #cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        #cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
        ##divider = make_axes_locatable(a)
        ##cax = divider.append_axes("right", size="5%", pad=0.5)  
    plt.tight_layout()
    plt.suptitle(exp,fontsize=title_font)
    plt.subplots_adjust(top=1.1)
    plt.savefig(save_figs_path+exp+'.png',bbox_inches='tight')
    plt.close('all')
'''



