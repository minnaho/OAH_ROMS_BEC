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
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from mpl_toolkits.axes_grid1 import make_axes_locatable
import colormaps_ncview as cmaps
#plt.ion()


###########
# load grid
###########
path_grid = '/data/project3/kesf/ROMS/USSW1/grid/usw1_grd.nc'
grid_nc = Dataset(path_grid,'r')
lat_grid = grid_nc.variables['lat_rho'][:,:]
lon_grid = grid_nc.variables['lon_rho'][:,:]

mask_nc = grid_nc.variables['mask_rho'][:,:]
h_nc = grid_nc.variables['h'][:,:]

###################
# bounds of plot
###################
'''
# bight
y0 = 50
yE = 650
x0 = 440
xE = 770
'''
y0 = 0
yE = mask_nc.shape[0]
x0 = 0
xE = mask_nc.shape[1]

mask_grid = mask_nc[y0:yE,x0:xE]

h_grid = h_nc[y0:yE,x0:xE]




#############################
# load pteropods experiments
#############################
path_data = '/data/project3/kesf/tools_matlab/applications/pteropods/'


exp_files = ['pteropods_survival_0_200m.nc',
             'pteropods_shelldiss_mild_juvenile_0_200m_2001.nc',
             'pteropods_severe_diss_0_200m.nc']
'''
juvenile_days = 610
adult_days = 2732
'''
juvenile_days = 92
adult_days =92

exp_titles = ['Adult Survival 0-200 m depth May to Jun, Threshold: 0.95, Duration: 14 days',
              'Juvenile Mild Shell Dissolution 0-200 m depth Mar to May, Threshold: 1.5, Duration: 5 days',
              'Juvenile Severe Shell Dissolution 0-200 m depth Mar to May, Threshold: 1.2, Duration: 14 days']

exp_variables = ['Intensity',
                 'Duration',
                 'Severity']
''' 
omega_avg_file = 'om_juranek_L1_mean.nc'
omega_avg_nc = Dataset(path_data+omega_avg_file,'r')
omega_avg = np.transpose(omega_avg_nc.variables['var'][0,:,:])
'''


######################
# plot using grid
#####################

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
for exp_ind,exp in enumerate(exp_files):
    print('plotting '+str(exp))
    fig = plt.figure(figsize=[fig_w,fig_h])
    # loop over each variable to make maps
    for i,var in enumerate(exp_variables):
        nc_data = Dataset(path_data+exp,'r')
        variable_data_tr = np.transpose(nc_data.variables[var][:,:])
        variable_data = variable_data_tr[y0:yE,x0:xE]*mask_grid
        # make land white by setting values to nan
        # make all 0 data to NaN
        variable_data[variable_data==0] = np.nan
        # create subplots for each map and put it on one figure for each experiment
        ax = fig.add_subplot(1,3,i+1)
        #if var == 'Intensity':
        #    ax.set_title('Magnitude',fontsize=subplot_title_font) 
        #else:
        #    ax.set_title(var,fontsize=subplot_title_font) 
        ax.set_title(var,fontsize=subplot_title_font) 
        plt.contour(h_grid,baths,colors='k',linewidths=1)

        # check which experiment to divide by correct number of days
        if 'juvenile' in exp:
            num_days = juvenile_days
        elif 'juvenile' not in exp:
            num_days = adult_days

        if var == 'Duration':
            #cmap_plot = 'YlGnBu'
            cmap_plot = 'viridis_r'
            #vmin_plot = 0
            #vmax_plot = 300
            #p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            duration = (variable_data/num_days)*100
            p = plt.imshow(duration,cmap=cmap_plot,origin='lower')

            con_s = list(range(10,110,20))

            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            #cb.set_label('Total Time below Threshold (days)',fontsize=axis_font)
            cb.set_label('% time below threshold',fontsize=axis_font)
            cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
            cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)


        if var == 'Recovery':
            cmap_plot = cmaps.ssec
            #vmin_plot = 0
            #vmax_plot = 1000
            #p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower')
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Number of Days',fontsize=axis_font)

        if var == 'Frequency': 
            cmap_plot = 'rainbow'
            #vmin_plot = 0
            #vmax_plot = 30
            #p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower')
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Number of Events',fontsize=axis_font)

        if var == 'Intensity': 
            cmap_plot = 'gist_rainbow_r'
            #cmap_plot = 'gnuplot_r'
            #cmap_plot = 'seismic'
            #vmin_plot = 0
            #vmax_plot = .3
            #p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)
            p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower')
            con_i = list(np.arange(.1,1,0.05))
            #plt.contour(variable_data,con_i,colors='k')
            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            cb.set_label('Mean deviation of below-threshold conditions',fontsize=axis_font)
            cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
            cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

        if var == 'Severity': 
            #cmap_plot = 'gnuplot_r'
            #cmap_plot = 'seismic'
            cmap_plot = 'gist_rainbow_r'
            #vmin_plot = 0
            #vmax_plot = 150
            #p = plt.imshow(variable_data,cmap=cmap_plot,origin='lower',vmin=vmin_plot,vmax=vmax_plot)

            # severity is intensity * duration days
            # multiply by % duration instead
            p = plt.imshow((variable_data/num_days)*duration,cmap=cmap_plot,origin='lower')
            con_s = list(range(10,110,5))

            plt.grid(True)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            a = plt.gca()
            cb = fig.colorbar(p,ax=ax)
            #cb.set_label('% time with omega below threshold',fontsize=axis_font)
            cb.set_label('Mean deviation '+r'$\times$'+' % time below threshold',fontsize=axis_font)
            cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
            cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
            #cb.set_ticks(range(0,110,10))

        ##divider = make_axes_locatable(a)
        ##cax = divider.append_axes("right", size="5%", pad=0.5)  

    # plot omega averaged as 6th map
    #ax = fig.add_subplot(3,2,6)
    #ax.set_title('Omega Averaged over 6 Years',fontsize=subplot_title_font) 
    #plt.contour(h_grid,baths,colors='k')
    #p = plt.imshow(omega_avg,cmap='gist_rainbow',origin='lower')
    #plt.grid(True)
    #ax.xaxis.set_visible(False)
    #ax.yaxis.set_visible(False)
    #a = plt.gca()
    #cb = fig.colorbar(p,ax=ax)
    #cb.set_label('Omega',fontsize=axis_font)
    #cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    #cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

    plt.tight_layout()
    #plt.suptitle(exp[:exp.index('.n')],fontsize=title_font)
    plt.suptitle(exp_titles[exp_ind],fontsize=title_font)
    plt.subplots_adjust(top=.90)
    #plt.savefig(save_figs_path+exp[:exp.index('.n')]+'_zoom.png',bbox_inches='tight')
    plt.savefig(save_figs_path+exp[:exp.index('.n')]+'_0_200m_mean.png',bbox_inches='tight')
    plt.close('all')
