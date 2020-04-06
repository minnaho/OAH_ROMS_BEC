#############################################
# plot_pCO2.py
# plot data from 
# hourly pCO2 data 
#####################################################
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.dates as mdate 
import datetime
from netCDF4 import Dataset, date2num, num2date, MFDataset
import colormaps_ncview as cmaps
from mpl_toolkits.axes_grid1 import make_axes_locatable
import glob
import calendar

###################
# FOLDER PATHS
####################
data_path = '/data/project1/kesf/data_kesf/Feng/ex_2015_d03/'
save_figs_path = './pCO2_figs/'

##################################
# load pCO2 data
##################################
dataset = 'wrfout_d01_2015-'
file_names = sorted(glob.glob(data_path+dataset+'*'))

# load first file to get grid dimensions and make basemap
grid = Dataset(file_names[0],'r')
lat_nc = grid.variables['lat']
lon_nc = grid.variables['lon']
lat = np.copy(lat_nc)
lon = np.copy(lon_nc)

############################
# make Basemap
############################
lat_mean = np.mean(lat)
lon_mean = np.mean(lon)

# bight zoom
lat_min = 32
lat_max = 36
lon_min = -121.5
lon_max = -116


# make map of domain of data using basemap
m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)


# get xy projected evenly space grid from netcdf lat/lon
# compute map projection coords
x,y = m(lon,lat)

# draw latitude
parallels = np.arange(0,90,1)
# draw longitude
meridians = np.arange(180,360,1)
###################################
# PLOTTING
##################################
title_font = 20
cb_font = 16
axis_tick_size = 15
cmap_plot = cmaps.hotres

fig_h = 10
fig_w = 14

pco2_vmin = -2
pco2_vmax = 200

cb_label = 'pCO2 ppmv'

for f in file_names:
    print('loading data '+f)
    data = Dataset(f,'r')
    pco2 = data.variables['co2ff']
    plot_pco2 = pco2[0,:,:]

    # find date for title using file name
    year_ind = f.index('2015-') 
    month_ind = year_ind+5 # +5 to move past 2015
    day_ind = month_ind+2 # +2 to move past month
    year = f[year_ind:month_ind-1]
    month = calendar.month_abbr[int(f[month_ind:day_ind])]
    day = f[day_ind+1:day_ind+3]
    hour = f[day_ind+4:day_ind+6]
    plot_title = 'Los Angeles Anthropogenic pCO2 '+hour+':00 PST '+day+' '+month+' '+year
     
    fig = plt.figure(figsize=[fig_w,fig_h])
    p = m.pcolor(x,y,plot_pco2,cmap=cmap_plot,vmin=pco2_vmin,vmax=pco2_vmax)
    #m.pcolor(x,y,plot_pco2,cmap=cmap_plot)
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    cb = plt.colorbar() 
    plt.title(plot_title,fontsize=title_font)
    cb.set_label('pCO2 ppmv',size=cb_font)     
    cb.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='minor',labelsize=axis_tick_size)
    save_fig_name = 'pCO2_'+year+'_'+f[month_ind:day_ind]+'_'+day+'_'+hour
    plt.savefig(save_figs_path+save_fig_name,bbox_inches='tight')
    print('saved fig '+save_figs_path+save_fig_name)
    plt.close('all')



