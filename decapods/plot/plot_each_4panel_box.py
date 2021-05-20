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

species = 'decapod'
#species = 'echinoderm'
#species = 'pteropod'
#path_data = '../pteropods_nc/avg_yearly/'
path_data = '../'+species+'s_nc/'
save_figs_path = '/data/project1/minnaho/decapods/plot/'+species+'_figs/'

# SF bay
ij_ptsf_0 = [990,620]
ij_ptsf_1 = [1140,710]
# channel island
ij_ptci_0 = [265,600]
ij_ptci_1 = [575,650]

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
#exp_files = list(sorted(glob.glob(path_data+'*.nc')))
exp_files = [path_data+'decapods_juvenile_mort_150m_1997_2007.nc']
plt.ion()


# full length of L1 simulation 1997-2007
if 'avg_yearly' in path_data:
    dt_st = datetime.datetime(1998,1,1)
    dt_en = datetime.datetime(1998,12,31)
    str_en = '_yearlyavg_box'
else:
    dt_st = datetime.datetime(1997,2,1)
    dt_en = datetime.datetime(2007,11,30)
    str_en = '_box'

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

exp_variables = ['Duration',
                 #'Recovery',
                 'Frequency',
                 'Intensity',
                 'Severity']


# basemap
lat_mean = np.mean(lat_grid)
lon_mean = np.mean(lon_grid)

# lines to plot

lon_plt = np.array(([np.min([lon_grid[ij_ptsf_0[0],ij_ptsf_0[1]],lon_grid[ij_ptsf_1[0],ij_ptsf_0[1]],lon_grid[ij_ptsf_0[0],ij_ptsf_1[1]],lon_grid[ij_ptsf_1[0],ij_ptsf_1[1]]]),
          np.max([lon_grid[ij_ptsf_0[0],ij_ptsf_0[1]],lon_grid[ij_ptsf_1[0],ij_ptsf_0[1]],lon_grid[ij_ptsf_0[0],ij_ptsf_1[1]],lon_grid[ij_ptsf_1[0],ij_ptsf_1[1]]])],
         [np.min([lon_grid[ij_ptci_0[0],ij_ptci_0[1]],lon_grid[ij_ptci_1[0],ij_ptci_0[1]],lon_grid[ij_ptci_0[0],ij_ptci_1[1]],lon_grid[ij_ptci_1[0],ij_ptci_1[1]]]),
          np.max([lon_grid[ij_ptci_0[0],ij_ptci_0[1]],lon_grid[ij_ptci_1[0],ij_ptci_0[1]],lon_grid[ij_ptci_0[0],ij_ptci_1[1]],lon_grid[ij_ptci_1[0],ij_ptci_1[1]]])]))


lat_plt = np.array(([np.min([lat_grid[ij_ptsf_0[0],ij_ptsf_0[1]],lat_grid[ij_ptsf_1[0],ij_ptsf_0[1]],lat_grid[ij_ptsf_0[0],ij_ptsf_1[1]],lat_grid[ij_ptsf_1[0],ij_ptsf_1[1]]]),
          np.max([lat_grid[ij_ptsf_0[0],ij_ptsf_0[1]],lat_grid[ij_ptsf_1[0],ij_ptsf_0[1]],lat_grid[ij_ptsf_0[0],ij_ptsf_1[1]],lat_grid[ij_ptsf_1[0],ij_ptsf_1[1]]])],
         [np.min([lat_grid[ij_ptci_0[0],ij_ptci_0[1]],lat_grid[ij_ptci_1[0],ij_ptci_0[1]],lat_grid[ij_ptci_0[0],ij_ptci_1[1]],lat_grid[ij_ptci_1[0],ij_ptci_1[1]]]),
          np.max([lat_grid[ij_ptci_0[0],ij_ptci_0[1]],lat_grid[ij_ptci_1[0],ij_ptci_0[1]],lat_grid[ij_ptci_0[0],ij_ptci_1[1]],lat_grid[ij_ptci_1[0],ij_ptci_1[1]]])]))

#lat_min = np.min(lat_grid)
lat_min = 30
lat_max = np.max(lat_grid)
lon_max = np.max(lon_grid)
lon_min = -126
#lon_min = np.min(lon_grid)

# draw latitude
parallels = np.arange(0,90,2)
# draw longitude
meridians = np.arange(180,360,4)


######################
# plot using grid
#####################


title_font = 20
cb_font = 16
axis_tick_size = 14
subplot_title_font = 16
axis_font = 15
h_space = 0.1
w_space = 0.1

fig_w = 12
fig_h = 12
cb_w = 0.01


baths = [200]

# loop over each experiment
for exp_i in range(len(exp_files)):
    print('plotting '+str(exp_files[exp_i]))
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
    nc_data = Dataset(exp_files[exp_i],'r')
    fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],sharex=True,sharey=True)
    fig.subplots_adjust(wspace=w_space,hspace=h_space)
    # loop over each variable to make maps
    for var in range(len(exp_variables)):
        map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[var])
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
        axes.flat[var].set_title(exp_variables[var],fontsize=subplot_title_font) 
        h_plt = map_ax.contour(x,y,h_grid,baths,colors='k',linewidths=1)
        plt.clabel(h_plt,fontsize=9,fmt='%1i')
        map_ax.drawstates()
        map_ax.drawcountries()
        map_ax.drawcoastlines()
        if var == 0 or var == 2:
            map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        else:
            map_ax.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size)
        if var > 1:    
            map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        else:
            map_ax.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)
        if exp_variables[var] == 'Intensity':
            cmap_plot = cmocean.cm.thermal_r
            cb_label = 'Mean value below threshold'
        if exp_variables[var] == 'Duration':
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
            if 'avg_yearly' in path_data:
                cb_label = 'Yearly Avg Number of Events'
            else:
                cb_label = 'Number of Events'
        if exp_variables[var] == 'Severity':
            cmap_plot = cmocean.cm.haline_r
            variable_data = (variable_data/variable_data_orig)*duration
            cb_label = '% time omega below threshold'
        p = map_ax.pcolor(x,y,variable_data,cmap=cmap_plot)
        i_plt,j_plt = map_ax(lon_plt,lat_plt)
        for p_i in range(len(i_plt)):
            map_ax.plot([i_plt[p_i,0],i_plt[p_i,0]],[j_plt[p_i,1],j_plt[p_i,0]],color='k',linestyle='--')
            map_ax.plot([i_plt[p_i,1],i_plt[p_i,1]],[j_plt[p_i,1],j_plt[p_i,0]],color='k',linestyle='--')
            map_ax.plot([i_plt[p_i,0],i_plt[p_i,1]],[j_plt[p_i,1],j_plt[p_i,1]],color='k',linestyle='--')
            map_ax.plot([i_plt[p_i,0],i_plt[p_i,1]],[j_plt[p_i,0],j_plt[p_i,0]],color='k',linestyle='--')
        p0 = axes.flat[var].get_position().get_points().flatten()
        cb_ax = fig.add_axes([p0[2]+0.01,p0[1],cb_w,p0[3]-p0[1]])
        cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical')
        cb_im.set_label(cb_label,fontsize=axis_font)
        cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

    fig.savefig(save_figs_path+exp_files[exp_i][len(path_data):exp_files[exp_i].index('.n')]+'_4panel'+str_en+'.png',bbox_inches='tight')
    #plt.close('all')

