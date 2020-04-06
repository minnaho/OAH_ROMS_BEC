#############################################
# plot_atmos_deposition.py
# plot data from 
# atmos_deposition_CMAQ_2002_2012.nc 
#####################################################
import numpy as np
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
from matplotlib.colors import LogNorm
import datetime
import copy
from collections import defaultdict
from netCDF4 import Dataset, date2num, num2date
import colormaps_ncview as cmaps
from mpl_toolkits.axes_grid1 import make_axes_locatable

###################
# FOLDER PATHS
####################
save_figs_path = './atmos_deposition_figs/'
oxn_path = 'oxidized_nitrogen/'
redn_path = 'reduced_nitrogen/'
fe_path = 'iron/'
alk_path = 'alkalinity/'


##################################
# load atmospheric deposition data
##################################
dataset_name = 'atmos_deposition_CMAQ_2002_2012.nc'
atmos_data = Dataset(dataset_name,'r')
time_a = atmos_data.variables['time']
time_a_plt = np.copy(time_a)

#convert time values to dates
dtime = num2date(time_a_plt,time_a.units)

lats_a = atmos_data.variables['latitude']
lons_a = atmos_data.variables['longitude']
lats_a_plt = np.copy(lats_a)
lons_a_plt = np.copy(lons_a)

oxn = atmos_data.variables['oxidized_nitrogen']
redn = atmos_data.variables['reduced_nitrogen']
alk = atmos_data.variables['alkalinity']
fe = atmos_data.variables['iron']


###################################
# PLOTTING
##################################
title_font = 18
axis_font = 15
axis_tick_size = 13

lat_mean = np.mean(lats_a_plt)
lon_mean = np.mean(lons_a_plt)

# lat/lon min and max of grid
'''
#lat_min = lats_a[0,0]
lat_min = 30
#lat_max = lats_a[-1,-1]
lat_max = 50
#lon_min = lons_a[0,-1]
lon_min = -130
lon_max = lons_a[-1,0]
'''
'''
# california zoom
lat_min = 31.5
lat_max = 42.5
lon_min = -125
lon_max = -115
'''


# bight zoom
lat_min = 31.5
lat_max = 35
lon_min = -121
lon_max = -115


# map of usw1_grd
#m = Basemap(projection='stere',resolution='h',lat_0=35.5,lon_0=-120,llcrnrlat=lat_nc[0,0],urcrnrlat=lat_nc[Ly-1,Lx-1],llcrnrlon=lon_nc[Ly-1,0],urcrnrlon=lon_nc[0,Lx-1])

# map of domain of data
m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max)


# get xy projected evenly space grid from netcdf lat/lon
# compute map projection coords
x,y = m(lons_a_plt,lats_a_plt)

'''
# PLOT OXIDIZED NITROGEN
cmap_oxn = cmaps.hotres
oxn_vmin = 0
oxn_vmax = 8E-6

for t in range(len(dtime)):
    fig = plt.figure(figsize=[9,11])
    plt.title('Atmospheric Deposition of Oxidized Nitrogen '+datetime.datetime.strftime(dtime[t],'%b %Y'),fontsize=title_font) 
    # plot on basemap created earlier
    p = m.pcolor(x,y,oxn[t],cmap=cmap_oxn,vmin=oxn_vmin,vmax=oxn_vmax) 
    ax = plt.gca()
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    # draw longitude
    meridians = np.arange(180,360,2.5)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1) 
    cb_oxn = plt.colorbar(p,format='%.1e',cax=cax) 
    cb_oxn.set_label('Oxidized Nitrogen (mmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
    cb_oxn.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    cb_oxn.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
    plt.savefig(save_figs_path+oxn_path+datetime.datetime.strftime(dtime[t],'%Y_%m'),bbox_inches='tight')
    print('oxn plotted date '+str(dtime[t].date())+' of '+str(dtime[-1].date()))
    plt.clf()
    plt.cla()
    plt.close('all')


# PLOT REDUCED NITROGEN
cmap_redn = cmaps.hotres
redn_vmin = 0
redn_vmax = 4E-6
for t in range(len(dtime)):
    fig = plt.figure(figsize=[9,11])
    plt.title('Atmospheric Deposition of Reduced Nitrogen '+datetime.datetime.strftime(dtime[t],'%b %Y'),fontsize=title_font) 
    p = m.pcolor(x,y,redn[t],cmap=cmap_redn,vmin=redn_vmin,vmax=redn_vmax) 
    ax = plt.gca()
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    # draw longitude
    meridians = np.arange(180,360,2.5)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1) 
    cb = plt.colorbar(p,format='%.1e',cax=cax) 
    cb.set_label('Reduced Nitrogen (mmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
    cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
    plt.savefig(save_figs_path+redn_path+datetime.datetime.strftime(dtime[t],'%Y_%m'),bbox_inches='tight')
    print('redn plotted date '+str(dtime[t].date())+' of '+str(dtime[-1].date()))
    plt.clf()
    plt.cla()
    plt.close('all')


# PLOT ALKALINITY 
cmap_alk = 'seismic'
alk_vmin = -5E-6
alk_vmax = 5E-6

for t in range(len(dtime)):
    fig = plt.figure(figsize=[9,11])
    plt.title('Atmospheric Deposition of Alkalinity '+datetime.datetime.strftime(dtime[t],'%b %Y'),fontsize=title_font) 
    p = m.pcolor(x,y,alk[t],cmap=cmap_alk,vmin=alk_vmin,vmax=alk_vmax) 
    ax = plt.gca()
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    # draw longitude
    meridians = np.arange(180,360,2.5)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1) 
    cb = plt.colorbar(p,format='%.1e',cax=cax) 
    cb.set_label('Alkalinity (mmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
    cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
    plt.savefig(save_figs_path+alk_path+datetime.datetime.strftime(dtime[t],'%Y_%m'),bbox_inches='tight')
    print('alk plotted date '+str(dtime[t].date())+' of '+str(dtime[-1].date()))
    plt.clf()
    plt.cla()
    plt.close('all')


# PLOT IRON
cmap_fe = cmaps.hotres
fe_vmin = 0
fe_vmax = 1.5E-7

for t in range(len(dtime)):
    fig = plt.figure(figsize=[9,11])
    plt.title('Atmospheric Deposition of Iron '+datetime.datetime.strftime(dtime[t],'%b %Y'),fontsize=title_font) 
    p = m.pcolor(x,y,fe[t],cmap=cmap_fe,vmin=fe_vmin,vmax=fe_vmax) 
    ax = plt.gca()
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    # draw longitude
    meridians = np.arange(180,360,2.5)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1) 
    cb = plt.colorbar(p,format='%.1e',cax=cax) 
    cb.set_label('Iron (mmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
    cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
    plt.savefig(save_figs_path+fe_path+datetime.datetime.strftime(dtime[t],'%Y_%m'),bbox_inches='tight')
    print('fe plotted date '+str(dtime[t].date())+' of '+str(dtime[-1].date()))
    plt.clf()
    plt.cla()
    plt.close('all')
'''

#######################
# PLOT CLIMATOLOGY
#######################
subplot_title_font = 16
# number of months in a year
months = 12
# convert mmol to kmol
mmol_to_kmol = 1E6
'''
# oxidized nitrogen
cmap_oxn = cmaps.hotres
oxn_vmin = 0
oxn_vmax = 8

fig = plt.figure(figsize=[12,12])

for mon in range(months):
    oxn_m = np.nanmean(oxn[mon::12],axis=0) 
    ax = fig.add_subplot(3,4,mon+1)
    ax.set_title(datetime.datetime.strftime(dtime[mon],'%B'),fontsize=subplot_title_font) 
    p = m.pcolor(x,y,oxn_m*mmol_to_kmol,cmap=cmap_oxn,vmin=oxn_vmin,vmax=oxn_vmax) 
    #ax.yaxis.labelpad = 2
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    if mon == 0 or mon == 4 or mon == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    # draw longitude
    meridians = np.arange(180,360,5)
    if mon > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size-2)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 
    #fig.subplots_adjust(hspace=0.2) 
plt.tight_layout()
plt.suptitle('Atmospheric Deposition of Oxidized Nitrogen Climatology 2002-2012',fontsize=title_font) 
# make room for suptitle
plt.subplots_adjust(top=.93)
a = plt.gca()
# add axes at position [left,bottom,width,height] in fractions of figure width and height
cax = fig.add_axes([.93,.025,.04,.9])
fig.subplots_adjust(right=0.9)
#cb = fig.colorbar(p,format='%.1e',cax=cax)
cb = fig.colorbar(p,format='%.1f',cax=cax)
cb.set_label('Oxidized Nitrogen (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
#divider = make_axes_locatable(a)
#cax = divider.append_axes("right", size="5%", pad=0.5)  
plt.savefig(save_figs_path+oxn_path+'climatology',bbox_inches='tight')


# reduced nitrogen
cmap_redn = cmaps.hotres
redn_vmin = 0
redn_vmax = 4

fig = plt.figure(figsize=[12,12])

for mon in range(months):
    redn_m = np.nanmean(redn[mon::12],axis=0) 
    ax = fig.add_subplot(3,4,mon+1)
    ax.set_title(datetime.datetime.strftime(dtime[mon],'%B'),fontsize=subplot_title_font) 
    p = m.pcolor(x,y,redn_m*mmol_to_kmol,cmap=cmap_redn,vmin=redn_vmin,vmax=redn_vmax) 
    #ax.yaxis.labelpad = 2
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    if mon == 0 or mon == 4 or mon == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    # draw longitude
    meridians = np.arange(180,360,5)
    if mon > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size-2)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 
    #fig.subplots_adjust(hspace=0.2) 
plt.tight_layout()
plt.suptitle('Atmospheric Deposition of Reduced Nitrogen Climatology 2002-2012',fontsize=title_font) 
# make room for suptitle
plt.subplots_adjust(top=.93)
a = plt.gca()
# add axes at position [left,bottom,width,height] in fractions of figure width and height
cax = fig.add_axes([.93,.025,.04,.9])
fig.subplots_adjust(right=0.9)
# plot colorbar in new axes position
#cb = fig.colorbar(p,format='%.1e',cax=cax)
cb = fig.colorbar(p,format='%.1f',cax=cax)
cb.set_label('Reduced Nitrogen (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
#divider = make_axes_locatable(a)
#cax = divider.append_axes("right", size="5%", pad=0.5)  
plt.savefig(save_figs_path+redn_path+'climatology',bbox_inches='tight')


# alkalinity 
cmap_alk = 'seismic' 
alk_vmin = -5
alk_vmax = 5

fig = plt.figure(figsize=[12,12])

for mon in range(months):
    alk_m = np.nanmean(alk[mon::12],axis=0) 
    ax = fig.add_subplot(3,4,mon+1)
    ax.set_title(datetime.datetime.strftime(dtime[mon],'%B'),fontsize=subplot_title_font) 
    p = m.pcolor(x,y,alk_m*mmol_to_kmol,cmap=cmap_alk,vmin=alk_vmin,vmax=alk_vmax) 
    #ax.yaxis.labelpad = 2
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    if mon == 0 or mon == 4 or mon == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    # draw longitude
    meridians = np.arange(180,360,5)
    if mon > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size-2)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 
    #fig.subplots_adjust(hspace=0.2) 
plt.tight_layout()
plt.suptitle('Atmospheric Deposition of Alkalinity Climatology 2002-2012',fontsize=title_font) 
# make room for suptitle
plt.subplots_adjust(top=.93)
a = plt.gca()
# add axes at position [left,bottom,width,height] in fractions of figure width and height
cax = fig.add_axes([.93,.025,.04,.9])
fig.subplots_adjust(right=0.9)
# plot colorbar in new axes position
#cb = fig.colorbar(p,format='%.1e',cax=cax)
cb = fig.colorbar(p,format='%.1f',cax=cax)
cb.set_label('Alkalinity (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
#divider = make_axes_locatable(a)
#cax = divider.append_axes("right", size="5%", pad=0.5)  
plt.savefig(save_figs_path+alk_path+'climatology',bbox_inches='tight')

'''
# iron
cmap_fe = cmaps.hotres
fe_vmin = 0 
fe_vmax = .5

fig = plt.figure(figsize=[12,12])

for mon in range(months):
    fe_m = np.nanmean(fe[mon::12],axis=0) 
    ax = fig.add_subplot(3,4,mon+1)
    ax.set_title(datetime.datetime.strftime(dtime[mon],'%B'),fontsize=subplot_title_font) 
    p = m.pcolor(x,y,fe_m*mmol_to_kmol,cmap=cmap_fe,vmin=fe_vmin,vmax=fe_vmax) 
    #ax.yaxis.labelpad = 2
    # draw details on map
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    # draw latitude
    parallels = np.arange(0,90,2.5)
    if mon == 0 or mon == 4 or mon == 8: 
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    else:
        m.drawparallels(parallels,labels=[0,0,0,0],fontsize=axis_tick_size) 
    # draw longitude
    meridians = np.arange(180,360,5)
    if mon > 7: 
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size-2)
    else:
        m.drawmeridians(meridians,labels=[0,0,0,0],fontsize=axis_tick_size-2) 
    #fig.subplots_adjust(hspace=0.2) 
plt.tight_layout()
plt.suptitle('Atmospheric Deposition of Iron Climatology 2002-2012',fontsize=title_font) 
# make room for suptitle
plt.subplots_adjust(top=.93)
a = plt.gca()
# add axes at position [left,bottom,width,height] in fractions of figure width and height
cax = fig.add_axes([.93,.025,.04,.9])
fig.subplots_adjust(right=0.9)
# plot colorbar in new axes position
#cb = fig.colorbar(p,format='%.1e',cax=cax)
cb = fig.colorbar(p,format='%.1f',cax=cax)
cb.set_label('Iron (kmol m$^{-2}$ s$^{-1}$)',fontsize=axis_font)
cb.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_tick_size)
cb.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_tick_size)
#divider = make_axes_locatable(a)
#cax = divider.append_axes("right", size="5%", pad=0.5)  
plt.savefig(save_figs_path+fe_path+'climatology',bbox_inches='tight')


