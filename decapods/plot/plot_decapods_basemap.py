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
import glob as glob


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

#############################
# load pteropods experiments
#############################
path_data = '/data/project1/minnaho/decapods/decapods_nc/'
extract_data_0   = '../extract_nc/pH_co2sys_L1_0m_slice_avg.nc'
extract_data_30  = '../extract_nc/pH_co2sys_L1_30m_slice_avg.nc'
extract_data_50  = '../extract_nc/pH_co2sys_L1_50m_slice_avg.nc'
extract_data_100 = '../extract_nc/pH_co2sys_L1_100m_slice_avg.nc'
extract_data_150 = '../extract_nc/pH_co2sys_L1_150m_slice_avg.nc'
extract_data_300 = '../extract_nc/pH_co2sys_L1_300m_slice_avg.nc'

#exp_files = ['decapods_juvenile_mort_50m_1997_2007.nc',
#             'decapods_adult_searching_50m_1997_2007.nc']
exp_files = list(sorted(glob.glob(path_data+'*')))

#juvenile_days = 30
#adult_days = 9

juvenile_days = 3955
adult_days = 3955

exp_titles = [
'Adult Mortality 100 m depth',
'Adult Mortality 150 m depth',
'Adult Mortality 50 m depth',
'Adult Mortality 50 m depth',
'Adult Searching 50 m depth',
'Juvenile Mortality 100 m depth',
'Juvenile Mortality 150 m depth',
'Juvenile Mortality 50 m depth',
'Larval Mortality 100 m depth',
'Larval Mortality 50 m depth',
]

exp_variables = ['Duration',
                 'Recovery',
                 'Frequency',
                 'Intensity',
                 'Severity']

# full length of L1 simulation 1997-2000
num_days = 3955

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
parallels = np.arange(0,90,2)
# draw longitude
meridians = np.arange(180,360,4)


######################
# plot using grid
#####################

save_figs_path = '/data/project1/minnaho/decapods/plot/figs/'

title_font = 20
cb_font = 16
axis_tick_size = 14
subplot_title_font = 16
axis_font = 15

fig_w = 14
fig_h = 9
cb_w = 0.01


baths = [200]

# loop over each experiment
for exp_i in range(len(exp_files)):
    print('plotting '+str(exp_files[exp_i]))
    nc_data = Dataset(exp_files[exp_i],'r')
    fig,axes = plt.subplots(2,3,figsize=[fig_w,fig_h],sharex=True,sharey=True)
    # loop over each variable to make maps
    for var in range(len(exp_variables)):
        map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[var])
        x,y = map_ax(lon_grid,lat_grid)
        variable_data_tr = np.transpose(nc_data.variables[exp_variables[var]][:,:])
        variable_data = variable_data_tr[y0:yE,x0:xE]*mask_grid
        # make land white by setting values to nan
        variable_data[variable_data==0] = np.nan
        axes.flat[var].set_title(exp_variables[var],fontsize=subplot_title_font) 
        h_plt = map_ax.contour(x,y,h_grid,baths,colors='k',linewidths=1)
        plt.clabel(h_plt,fontsize=9,fmt='%1i')
        map_ax.drawstates()
        map_ax.drawcountries()
        map_ax.drawcoastlines()
        if var == 0 or var == 3:
            map_ax.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
        else:
            map_ax.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size)
        if var > 2:    
            map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
        else:
            map_ax.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size)
        if exp_variables[var] == 'Duration':
            cmap_plot = cmocean.cm.ice_r
            variable_data_orig = np.copy(variable_data)
            duration = (variable_data/num_days)*100
            variable_data = (variable_data/num_days)*100
            cb_label = '% time below threshold'
        if exp_variables[var] == 'Recovery':
            cmap_plot = cmocean.cm.matter
            cb_label = 'Number of Days'
        if exp_variables[var] == 'Frequency':
            cmap_plot = cmocean.cm.turbid
            cb_label = 'Number of Events'
        if exp_variables[var] == 'Intensity':
            cmap_plot = cmocean.cm.thermal_r
            cb_label = 'Mean value below threshold'
        if exp_variables[var] == 'Severity':
            cmap_plot = cmocean.cm.haline_r
            variable_data = (variable_data/variable_data_orig)*duration
            cb_label = '% time omega below threshold'
        p = map_ax.pcolor(x,y,variable_data,cmap=cmap_plot)
        p0 = axes.flat[var].get_position().get_points().flatten()
        cb_ax = fig.add_axes([p0[2]+0.01,p0[1],cb_w,p0[3]-p0[1]])
        cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical')
        cb_im.set_label(cb_label,fontsize=axis_font)
        cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
        cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)

    # plot pH averaged as 6th map
    map_ax = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes.flat[-1])
    cmap_plot = cmocean.cm.dense
    axes.flat[-1].set_title('Average pH 1997-2007',fontsize=subplot_title_font) 
    cb_label = 'pH'
    if '_0m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_0,'r').variables['var'][0,:,:])
    if '_30m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_30,'r').variables['var'][0,:,:])
    if '_50m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_50,'r').variables['var'][0,:,:])
    if '_100m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_100,'r').variables['var'][0,:,:])
    if '_150m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_150,'r').variables['var'][0,:,:])
    if '_300m_' in exp_files[exp_i]:
        ph_data = np.array(Dataset(extract_data_300,'r').variables['var'][0,:,:])
    p = map_ax.pcolor(x,y,ph_data,cmap=cmap_plot)
    h_plt = map_ax.contour(x,y,h_grid,baths,colors='k',linewidths=1)
    plt.clabel(h_plt,fontsize=9,fmt='%1i')
    map_ax.drawstates()
    map_ax.drawcountries()
    map_ax.drawcoastlines()
    map_ax.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size)
    map_ax.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    p0 = axes.flat[-1].get_position().get_points().flatten()
    cb_ax = fig.add_axes([p0[2]+0.01,p0[1],cb_w,p0[3]-p0[1]])
    cb_im = fig.colorbar(p,cax=cb_ax,orientation='vertical')
    cb_im.set_label(cb_label,fontsize=axis_font)
    cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
        
    #fig.tight_layout()
    #fig.suptitle(exp_titles[exp_i]+' pH '+nc_data.description+' days',fontsize=title_font)
    #fig.subplots_adjust(top=.90)
    fig.savefig(save_figs_path+exp_files[exp_i][len(path_data):exp_files[exp_i].index('.n')]+'.png',bbox_inches='tight')
    plt.close('all')

