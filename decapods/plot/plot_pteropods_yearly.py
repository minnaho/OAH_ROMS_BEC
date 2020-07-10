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
#import colormaps_ncview as cmaps
import cmocean as cmocean
import datetime as datetime
import glob as glob

#species = 'decapod'
#species = 'echinoderm'
species = 'pteropod'
path_data = '../pteropods_nc/yearly/'
#path_data = '../'+species+'s_nc/'
save_figs_path = '/data/project1/minnaho/decapods/plot/'+species+'_figs/'

###########
# load grid
###########
path_grid = '/data/project3/kesf/ROMS/USSW1/grid/usw1_grd.nc'
grid_nc = Dataset(path_grid,'r')
lat_grid = np.array(grid_nc.variables['lat_rho'][:,:])
lon_grid = np.array(grid_nc.variables['lon_rho'][:,:])

mask_nc = np.array(grid_nc.variables['mask_rho'][:,:])
h_nc = np.array(grid_nc.variables['h'][:,:])

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
# for echinoderm bottom 5 m, set depths >500m to 0
h_echino = np.copy(h_grid)
h_echino[h_echino>500] = 0
h_echino[h_echino>0] = 1

#############################
# load experiments
#############################
exp_files_notunique = list(sorted(glob.glob(path_data+'*.nc')))
exp_files = list(set([sub[:-7] for sub in exp_files_notunique]))



# full length of L1 simulation 1997-2007

exp_variables = ['Duration',
                 #'Recovery',
                 'Frequency',
                 'Intensity']
                 #'Severity']


# basemap
lat_mean = np.mean(lat_grid)
lon_mean = np.mean(lon_grid)

#lat_min = np.min(lat_grid)
lat_min = 30
lat_max = np.max(lat_grid)
lon_max = np.max(lon_grid)
lon_min = -126
#lon_min = np.min(lon_grid)

# draw latitude
parallels = np.arange(0,90,3)
# draw longitude
meridians = np.arange(180,360,6)


######################
# plot using grid
#####################


title_font = 20
cb_font = 16
axis_tick_size = 12
subplot_title_font = 12
axis_font = 15
h_space = 0.1
w_space = 0.1

fig_w = 30
fig_h = 10
cb_w = 0.01


baths = [200]

# loop over each experiment

for var in range(len(exp_variables)):
    fig,axes = plt.subplots(1,11,figsize=[fig_w,fig_h],sharex=True,sharey=True)
    #fig.subplots_adjust(wspace=w_space,hspace=h_space)
    for exp_i in range(len(exp_files)):
        # loop over each year to make maps
        for id_i,y_i in enumerate(range(1997,2008)):
            print('plotting '+exp_files[exp_i]+str(y_i)+'.nc')
            nc_data = Dataset(exp_files[exp_i]+str(y_i)+'.nc','r')
            if y_i==1997:
                dt_st = datetime.datetime(1997,2,1)
                dt_en = datetime.datetime(1997,12,31)
            if y_i==2007:
                dt_st = datetime.datetime(2007,1,1)
                dt_en = datetime.datetime(2007,11,30)
            else:
                dt_st = datetime.datetime(1998,1,1)
                dt_en = datetime.datetime(1998,12,31)
            # make array of all dates
            date_range = np.array([dt_st+datetime.timedelta(days=n) for n in range(int ((dt_en+datetime.timedelta(days=1)-dt_st).days))])
            num_days_mar_may = 0
            num_days_jun_sep = 0
            num_days_apr_aug = 0
            num_days_mar_jul = 0
            num_days_apr_jul = 0
            num_days_jun_nov = 0
            # find number of days with selected months
            for d_i in range(len(date_range)):
                if date_range[d_i].month >= 3 and date_range[d_i].month <= 5:
                    num_days_mar_may += 1
                if date_range[d_i].month >= 6 and date_range[d_i].month <= 9:
                    num_days_jun_sep += 1
                if date_range[d_i].month >= 4 and date_range[d_i].month <= 8:
                    num_days_apr_aug += 1
                if date_range[d_i].month >= 3 and date_range[d_i].month <= 7:
                    num_days_mar_jul += 1
                if date_range[d_i].month >= 4 and date_range[d_i].month <= 7:
                    num_days_apr_jul += 1
                if date_range[d_i].month >= 6 and date_range[d_i].month <= 11:
                    num_days_jun_nov += 1
            num_days_full = len(date_range)
            if 'jun_sep' in exp_files[exp_i]:
                num_days_select = num_days_jun_sep
            if 'mar_may' in exp_files[exp_i]:
                num_days_select = num_days_mar_may
            if 'jun_nov' in exp_files[exp_i]:
                num_days_select = num_days_jun_nov
            if 'upwell' in exp_files[exp_i] and 'echinoderm' in exp_files[exp_i]:
                num_days_select = num_days_apr_jul
            if 'upwell' in exp_files[exp_i] and 'mort' in exp_files[exp_i] and 'decapod' in exp_files[exp_i]:
                num_days_select = num_days_mar_jul
            if 'upwell' in exp_files[exp_i] and 'diss' in exp_files[exp_i] and 'decapod' in exp_files[exp_i]:
                num_days_select = num_days_apr_aug
            else:
                num_days_select = num_days_full
            map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[id_i])
            x,y = map_ax(lon_grid,lat_grid)
            # pteropods
            if (species == 'pteropod') or ('bottom' in exp_files[exp_i] and 'deep' not in exp_files[exp_i]):
                variable_data = np.array(nc_data.variables[exp_variables[var]][:,:])[y0:yE,x0:xE]*mask_grid
            # echinoderms
            else:
                variable_data_tr = np.transpose(nc_data.variables[exp_variables[var]][:,:])
                variable_data = variable_data_tr[y0:yE,x0:xE]*mask_grid
            # make land white by setting values to nan
            if species=='echinoderm' and 'bottom' in exp_files[exp_i]: 
                variable_data = variable_data*h_echino
            variable_data[variable_data==0] = np.nan
            axes.flat[id_i].set_title(str(y_i),fontsize=subplot_title_font) 
            h_plt = map_ax.contour(x,y,h_grid,baths,colors='k',linewidths=1)
            plt.clabel(h_plt,fontsize=9,fmt='%1i')
            map_ax.drawstates()
            map_ax.drawcountries()
            map_ax.drawcoastlines()
            if id_i == 0:
                map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
            else:
                map_ax.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size)
            if id_i >= 0:    
                map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
            else:
                map_ax.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)
            if exp_variables[var] == 'Intensity':
                cmap_plot = cmocean.cm.thermal_r
                cb_label = 'Mean value below threshold'
                v_min = 0
                v_max = 0.15
            if exp_variables[var] == 'Duration':
                v_min = 0
                v_max = 71
                cmap_plot = cmocean.cm.ice_r
                variable_data_orig = np.copy(variable_data)
                duration = (variable_data/num_days_select)*100
                variable_data = (variable_data/num_days_select)*100
                cb_label = '% time below threshold'
            if exp_variables[var] == 'Recovery':
                cmap_plot = cmocean.cm.matter
                cb_label = 'Number of Days'
            if exp_variables[var] == 'Frequency':
                cmap_plot = cmocean.cm.turbid
                v_min = 0
                v_max = 20
                if 'avg_yearly' in path_data:
                    cb_label = 'Yearly Avg Number of Events'
                else:
                    cb_label = 'Number of Events'
            if exp_variables[var] == 'Severity':
                cmap_plot = cmocean.cm.haline_r
                variable_data = (variable_data/variable_data_orig)*duration
                if species == 'pteropod':
                    cb_label = '% time omega below threshold'
                else:
                    cb_label = '% time pH below threshold'
            p = map_ax.pcolor(x,y,variable_data,cmap=cmap_plot,vmin=v_min,vmax=v_max)
        p0 = axes.flat[id_i].get_position().get_points().flatten()
        cb_ax = fig.add_axes([p0[2]+0.01,p0[1],cb_w,p0[3]-p0[1]])
        cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical')
        cb_im.set_label(cb_label,fontsize=axis_font)
        cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

        fig.savefig(save_figs_path+exp_files[exp_i][23:]+exp_variables[var]+'_byyear.png',bbox_inches='tight')
        plt.close('all')

