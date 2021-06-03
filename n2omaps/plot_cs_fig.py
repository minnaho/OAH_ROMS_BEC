################################################
# plot cross section of particles
# with residence time x days
# consider all y points (not just one latitude line))
################################################
import sys
import os
sys.path.append('/data/project3/minnaho/global/')
import l0grid
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import ROMS_depths as depths
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cmocean
import datetime as datetime
import calendar

# plot fresh vs nutrients vs control vs full
#plt.ion()

savepath = './figs/cs/'

#linestr = 'Line 6, Newport Hydro'
#linestr = 'Line 9, Cape Mendocino'
#linestr = 'Line 11, San Francisco'
#linestr = 'Line 12, Monterey'
#linestr = 'Line 13, CalCOFI 80, Pt Conception'
linestr = 'Line 14, CalCOFI90, Catalina Islands'

# first lat/lon on land for line
if linestr == 'Line 6, Newport Hydro':
    lnsv = 'line06'
    lon_site = -124.1000       
    lat_site = 44.6517
    
    ind_st = -125.37
    ind_en = -124.05
    
    dp_st = -500
    dp_en = 0

if linestr == 'Line 9, Cape Mendocino':
    lnsv = 'line09'
    lon_site = -124.3753
    lat_site = 40.2513
    
    ind_st = -125.2012
    ind_en = -124.36
    
    dp_st = -500
    dp_en = 0

if linestr == 'Line 11, San Francisco':
    lnsv = 'line11'
    lon_site = -122.4459
    lat_site = 37.8923
    
    ind_st = -123
    ind_en = -122.59
    
    dp_st = -200
    dp_en = 0

if linestr == 'Line 12, Monterey':
    lnsv = 'line12'
    lon_site = -121.8178
    lat_site = 36.8098

    ind_st = -123.85
    ind_en = -121.8
    
    dp_st = -500
    dp_en = 0

if linestr == 'Line 13, CalCOFI 80, Pt Conception':
    lnsv = 'line13'
    lon_site = -120.4891
    lat_site = 34.4667

    ind_st = -121.8430
    ind_en = -120.48
    
    dp_st = -1000
    dp_en = 0

if linestr == 'Line 14, CalCOFI90, Catalina Islands':
    lnsv = 'line14'
    lon_site = -117.7474
    lat_site = 33.4946

    ind_st = -120.6387
    ind_en = -117.73
    
    dp_st = -1000
    dp_en = 0



# roms var
var_nc = 'N2O'
#cblabel = 'Density (kg m$^{-3}$)'
#cblabel = 'NO3 (mmol m$^{-3}$)'
cblabel = 'N2O (mmol m$^{-3}$)'
#cblabel = 'salt (PSU)'

# path of outputs
freshpath = '/data/project6/ROMS/USW4/monthly/'

# choose year and month
#year = 1999
#month = 9

start_year = 2017
end_year = 2017

# between 1 and 12
start_month = 6
end_month = 8


if var_nc == 'rho':
    rho0 = 1027.4
    clines = [1023.5,1024,1024.5,1025,1025.5,1026,1026.5]
if var_nc == 'NH4' or var_nc == 'NO3':
    clines = [0.5,1,5,10,13]
if var_nc == 'N2O':
    clines = [0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.7,0.85,0.9,0.95,1]
if var_nc == 'salt':
    clines = [32.75,33,33.25,33.5,33.75,34,34.25]

# max and min of color bar
if var_nc == 'N2O':
    v_max = 0.05
    #v_max = np.nanmax(roms_var_fresh)
    v_min = 0

ncfile = []
savename = []
for y in range(start_year,end_year+1):
    # if we are on the first year, starts at s_m
    if y == start_year:
        s_m = start_month
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y == end_year:
        e_m = end_month+1
    else:
        e_m = 13
    for m in range(s_m,e_m):
        year_month = 'Y'+str(y)+'M'+'%02d'%m
        ncfile.append('usw42_avg.'+year_month+'.nc')
        savename.append('cs_'+lnsv+'_'+var_nc+'_Y'+str(y)+'M'+'%02d'%m+'.png')

# outputs
freshnc = []

for n_i in range(len(ncfile)):
    freshnc.append(Dataset(freshpath+ncfile[n_i],'r'))


# grid path
grid_nc = l0grid.grid_nc
lat_nc = l0grid.lat_nc
lon_nc = l0grid.lon_nc
h_nc = l0grid.h_nc


# calculate i and j
min_1D = np.abs( (lat_nc - lat_site)**2 + (lon_nc - lon_site)**2)
y_site, x_site = np.unravel_index(min_1D.argmin(), min_1D.shape)

# get longitudinal slice
lon_slice = lon_nc[y_site,:]
h_slice = h_nc[y_site,:]

# reshape to match z_r
# 60 by 602 in L2
lon_slice_l = list(lon_slice)*freshnc[0].variables[var_nc].shape[1]
lon_reshape = np.array(lon_slice_l).reshape(freshnc[0].variables[var_nc].shape[1],lon_nc.shape[1]) 

# bounds to draw contours
ind_st_p = np.nanmin(np.unique(np.where((lon_reshape[:,:]>=ind_st)&(lon_reshape<=ind_en))[1]))-1
ind_en_p = np.nanmax(np.unique(np.where((lon_reshape[:,:]>=ind_st)&(lon_reshape<=ind_en))[1]))+1

figw = 14
figh = 7.2
c_map = cmocean.cm.dense

axis_tick_size = 14

for n_i in range(len(ncfile)):
    fig,ax = plt.subplots(1,1,figsize=[figw,figh])
    # roms field from output at y_site slice
    roms_var_fresh = np.array(freshnc[n_i].variables[var_nc][0,:,y_site,:])
    roms_var_fresh[roms_var_fresh>1E10] = np.nan
    
    
    # get depths at this y_site slice for each scenario
    z_r_fresh = depths.get_zr_zw_tind(freshnc[n_i],grid_nc,0,[y_site-1,y_site+1,0,freshnc[n_i].variables[var_nc].shape[3]])[0][:,1,:]
    
    z_r_fresh[z_r_fresh>1E10] = np.nan
    
    #ax.plot(-1*h_slice,color='k') # bottom depth  
    p_plot_fresh = ax.pcolor(lon_slice,z_r_fresh,roms_var_fresh,cmap=c_map,vmin=v_min,vmax=v_max)
    
    p0 = ax.get_position().get_points().flatten()
    p1 = ax.get_position().get_points().flatten()
    cb_ax = fig.add_axes([p0[2]+.015,p1[1],.01,p0[3]-p1[1]])
    
    cb = fig.colorbar(p_plot_fresh,cax=cb_ax,orientation='vertical',format='%.3f')
    cb.set_label(cblabel,fontsize=axis_tick_size)
    cb.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    ax.set_xlim([ind_st,ind_en])
    ax.set_ylim([dp_st,dp_en])
    
    # plot contours
    clinecolor = 'k'
    c_plt_fresh = ax.contour(lon_reshape[:,ind_st_p:ind_en_p],z_r_fresh[:,ind_st_p:ind_en_p],roms_var_fresh[:,ind_st_p:ind_en_p],clines,colors=clinecolor,linewidths=1)
    
    ax.clabel(c_plt_fresh,fontsize=9,fmt='%.3f',inline=1)
    ax.set_ylabel('Depth (m)',fontsize=axis_tick_size)
    ax.set_xlabel('Longitude',fontsize=axis_tick_size)

    # set x ticks equal to bounds of map
    ax.set_xticks(np.linspace(ind_st,ind_en,10))
    
    # tick spacing 
    #tick_spacingx = 0.04
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacingx))
    
    #tick_spacingy = 15
    #ax.flat[0].yaxis.set_major_locator(ticker.MultipleLocator(tick_spacingy))
    
    # remove labels
    
    fig.suptitle(linestr+' '+calendar.month_name[int(savename[n_i][savename[n_i].index('M')+1:savename[n_i].index('M')+1+2])]+' '+savename[n_i][savename[n_i].index('Y')+1:savename[n_i].index('Y')+1+4]+' Average',fontsize=axis_tick_size)
    
    ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    
    fig.savefig(savepath+savename[n_i],bbox_inches='tight')
    print(savename)
    plt.close()

