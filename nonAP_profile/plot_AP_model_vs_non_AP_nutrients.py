###################################################################
# read NH4, PO4, NO3, NO2 
# L2 SCB and compare to L2 SCB (300 m) AP (anthropogenic input) model
# Oct 3 2018 Minna Ho minnaho@ucla.edu
################################################################
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset
import glob
import datetime
import depths as depths
import calendar
#plt.ion()

save_figs = './profile_figs/'

##########################
# change nutrients and months/time period 
#########################
nutrients = ['DIATCHL','SPCHL']
month_chosen = [2,3]
month_name = []
if type(month_chosen) is list:
    for m_n in month_chosen:
        month_name.append(calendar.month_abbr[m_n])
else:
    month_name.append(calendar.month_abbr[month_chosen])

######################
# load L2 AP model data
######################
# L2 grid file
grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc'
nc_grid = Dataset(grid_path,'r')
lon_nc  = nc_grid.variables['lon_rho'][:,:]
lat_nc  = nc_grid.variables['lat_rho'][:,:]

# lat/lon of outfalls, order: PLWTP, OCSD, JWPCP, HTP 
lat_data = [32.671985,33.576667,33.6892,33.920667]
lon_data = [-117.325802,-118.01,-118.3167,-118.52975]

# get grid point of OCSD
coord_i = []
coord_j = []
for coord in range(len(lat_data)):
    lat_you_want = lat_data[coord]
    lon_you_want = lon_data[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)


# 1997-05-02 L2_SCB file

#output_path = '/data/project3/kesf/ROMS/L2_SCB/DAILY/'
# one month of output
if type(month_chosen) is list:
    roms_files = []
    for m_l in month_chosen:
        output_path = '/data/project3/kesf/ROMS/L2_SCB_AP/AVG_Y1997M'+'%02d'%m_l+'/'
        file_name = 'l2_scb_avg.*'
        roms_files.append(sorted(glob.glob(output_path+file_name)))
    roms_files = [j for i in roms_files for j in i]
else:
    output_path = '/data/project3/kesf/ROMS/L2_SCB_AP/AVG_Y1997M'+'%02d'%month_chosen+'/'
    file_name = 'l2_scb_avg.*'
    roms_files = sorted(glob.glob(output_path+file_name))

# (day, location, grid point, s_rho)
temp_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
salt_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
depth_outfalls = np.empty((len(roms_files),len(coord_i),9,60))

print('reading nutrients: '+nutrients[0]+', '+nutrients[1])
for f_f,f_i in enumerate(roms_files):
    print('reading '+f_i)
    nc_roms = Dataset(f_i,'r')
    temp_nc = nc_roms.variables[nutrients[0]]
    salt_nc = nc_roms.variables[nutrients[1]]
    
    for loc_i in range(len(coord_i)):
        temp_outfalls[f_f,loc_i,0,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,1,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,2,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,3,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,4,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]-1] 
        temp_outfalls[f_f,loc_i,5,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,6,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]-1] 
        temp_outfalls[f_f,loc_i,7,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,8,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]-1] 
 
        salt_outfalls[f_f,loc_i,0,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,1,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,2,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,3,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,4,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]-1] 
        salt_outfalls[f_f,loc_i,5,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,6,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]-1] 
        salt_outfalls[f_f,loc_i,7,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,8,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]-1] 

        # z_sigmas = (s_rho,Ly,Lx)
        # returns the depths of each sigma level from bottom to top
        [z_sigmas,Cs] = depths.get_depths(f_i,grid_path,0,'r','new')
        depth_outfalls[f_f,loc_i,0,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,1,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,2,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,3,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,4,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]-1]*-1
        depth_outfalls[f_f,loc_i,5,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,6,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]-1]*-1
        depth_outfalls[f_f,loc_i,7,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,8,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]-1]*-1

temp_min_AP = np.empty((4,60))
temp_max_AP = np.empty((4,60))
temp_avg_AP= np.empty((4,60))
salt_min_AP = np.empty((4,60))
salt_max_AP = np.empty((4,60))
salt_avg_AP = np.empty((4,60))
depth_min_AP = np.empty((4,60))
depth_max_AP = np.empty((4,60))
depth_avg_AP = np.empty((4,60))

# find minimum across each day and 9 grid points
for loc_m in range(len(coord_i)):
    temp_min_AP[loc_m,:] = np.min(np.min(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_max_AP[loc_m,:] = np.max(np.max(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_avg_AP[loc_m,:] = np.average(np.average(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_min_AP[loc_m,:] = np.min(np.min(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_max_AP[loc_m,:] = np.max(np.max(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_avg_AP[loc_m,:] = np.average(np.average(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_min[loc_m,:] = np.min(np.min(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_max[loc_m,:] = np.max(np.max(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    depth_avg_AP[loc_m,:] = np.average(np.average(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
 
# prevent negative values
temp_min_AP[temp_min_AP<0] = 0
salt_min_AP[temp_min_AP<0] = 0

#######################
# load L2_SCB model (non anthropogenic)
#######################

# one month of output
if type(month_chosen) is list:
    roms_files = []
    for m_l in month_chosen:
        output_path = '/data/project3/kesf/ROMS/L2_SCB/AVG_Y1997M'+'%02d'%m_l+'/'
        file_name = 'l2_scb_avg.*'
        roms_files.append(sorted(glob.glob(output_path+file_name)))
    roms_files = [j for i in roms_files for j in i]
else:
    output_path = '/data/project3/kesf/ROMS/L2_SCB/AVG_Y1997M'+'%02d'%month_chosen+'/'
    file_name = 'l2_scb_avg.*'
    roms_files = sorted(glob.glob(output_path+file_name))

# (day, location, grid point, s_rho)
temp_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
salt_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
depth_outfalls = np.empty((len(roms_files),len(coord_i),9,60))


for f_f,f_i in enumerate(roms_files):
    print('reading '+f_i)
    nc_roms = Dataset(f_i,'r')
    temp_nc = nc_roms.variables[nutrients[0]]
    salt_nc = nc_roms.variables[nutrients[1]]
    
    for loc_i in range(len(coord_i)):
        temp_outfalls[f_f,loc_i,0,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,1,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,2,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]] 
        temp_outfalls[f_f,loc_i,3,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,4,:] = temp_nc[0,:,coord_j[loc_i],coord_i[loc_i]-1] 
        temp_outfalls[f_f,loc_i,5,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,6,:] = temp_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]-1] 
        temp_outfalls[f_f,loc_i,7,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]+1] 
        temp_outfalls[f_f,loc_i,8,:] = temp_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]-1] 
 
        salt_outfalls[f_f,loc_i,0,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,1,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,2,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]] 
        salt_outfalls[f_f,loc_i,3,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,4,:] = salt_nc[0,:,coord_j[loc_i],coord_i[loc_i]-1] 
        salt_outfalls[f_f,loc_i,5,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,6,:] = salt_nc[0,:,coord_j[loc_i]+1,coord_i[loc_i]-1] 
        salt_outfalls[f_f,loc_i,7,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]+1] 
        salt_outfalls[f_f,loc_i,8,:] = salt_nc[0,:,coord_j[loc_i]-1,coord_i[loc_i]-1] 

        # z_sigmas = (s_rho,Ly,Lx)
        # returns the depths of each sigma level from bottom to top
        [z_sigmas,Cs] = depths.get_depths(f_i,grid_path,0,'r','new')
        depth_outfalls[f_f,loc_i,0,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,1,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,2,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]]*-1
        depth_outfalls[f_f,loc_i,3,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,4,:] = z_sigmas[:,coord_j[loc_i],coord_i[loc_i]-1]*-1
        depth_outfalls[f_f,loc_i,5,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,6,:] = z_sigmas[:,coord_j[loc_i]+1,coord_i[loc_i]-1]*-1
        depth_outfalls[f_f,loc_i,7,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]+1]*-1
        depth_outfalls[f_f,loc_i,8,:] = z_sigmas[:,coord_j[loc_i]-1,coord_i[loc_i]-1]*-1

temp_min_NAP = np.empty((4,60))
temp_max_NAP = np.empty((4,60))
temp_avg_NAP= np.empty((4,60))
salt_min_NAP = np.empty((4,60))
salt_max_NAP = np.empty((4,60))
salt_avg_NAP = np.empty((4,60))
depth_min_NAP = np.empty((4,60))
depth_max_NAP = np.empty((4,60))
depth_avg_NAP = np.empty((4,60))

# find minimum across each day and 9 grid points
for loc_m in range(len(coord_i)):
    temp_min_NAP[loc_m,:] = np.min(np.min(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_max_NAP[loc_m,:] = np.max(np.max(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_avg_NAP[loc_m,:] = np.average(np.average(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_min_NAP[loc_m,:] = np.min(np.min(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_max_NAP[loc_m,:] = np.max(np.max(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_avg_NAP[loc_m,:] = np.average(np.average(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_min[loc_m,:] = np.min(np.min(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_max[loc_m,:] = np.max(np.max(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    depth_avg_NAP[loc_m,:] = np.average(np.average(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
 
# prevent negative values
temp_min_NAP[temp_min_NAP<0] = 0
salt_min_NAP[temp_min_NAP<0] = 0



#################
# PLOTTING
#################
suptitle_size = 20
xy_labels = 16
tick_size = 14
legend_size = 14

model_avg_label = 'Non-AP Model average'
model_avg_c = 'blue'
#model_min_label = 'Model minimum'
model_min_label = 'Non-AP Model min/max'
model_min_c = 'teal'
#model_max_label = 'Model maximum'
model_max_c = 'teal'

model_avg_AP_l= 'AP Model average'
model_min_AP_l= 'AP Model min/max'
model_avg_AP_c = 'red'
model_min_AP_c = 'coral' 
model_max_AP_c = 'coral' 

obs_c = 'grey'

obs_name = ['PLWTP','OCSD','JWPCP','HTP']

line_style_m = 'o-'
line_style_obs = 'o'
marker_size_obs = 3
space = '                    '
# loop over 4 outfalls
for o_i in range(len(temp_min_AP)):
    # Two-panel plot
    fig1, (ax1, ax2, ax3, ax4) = plt.subplots(1,4,sharey=True,figsize=(15,9))
    # Non-AP run
    # Temperature
    ax1.plot(temp_avg_NAP[o_i],depth_avg_NAP[o_i],line_style_m,label=model_avg_label,color=model_avg_c)
    ax1.plot(temp_min_NAP[o_i],depth_avg_NAP[o_i],line_style_m,label=model_min_label,color=model_min_c)
    ax1.plot(temp_max_NAP[o_i],depth_avg_NAP[o_i],line_style_m,color=model_max_c)

    ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax1.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    ax1.set_xlabel(space+nutrients[0]+' (mmol m$^{-3}$)',fontsize=xy_labels)
    ax1.xaxis.set_label_position('top') # this moves the label to the top
    ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax1.tick_params(axis='both',which='major',labelsize=tick_size)
    #ax1.legend(loc='best',fontsize=legend_size)
    ax1.grid(True)

    # Temp AP run
    ax2.plot(temp_avg_AP[o_i],depth_avg_AP[o_i],line_style_m,label=model_avg_AP_l,color=model_avg_AP_c)
    ax2.plot(temp_min_AP[o_i],depth_avg_AP[o_i],line_style_m,label=model_min_AP_l,color=model_min_AP_c)
    ax2.plot(temp_max_AP[o_i],depth_avg_AP[o_i],line_style_m,color=model_max_AP_c)

    #ax2.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax2.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    #ax2.set_xlabel(nutrients[0]+' (mmol m$^{-3}$)',fontsize=xy_labels)
    ax2.xaxis.set_label_position('top') # this moves the label to the top
    ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax2.tick_params(axis='both',which='major',labelsize=tick_size)
    ax2.grid(True)

    # Non_AP run
    # Salinity
    ax3.plot(salt_avg_NAP[o_i],depth_avg_NAP[o_i],line_style_m,label=model_avg_label,color=model_avg_c)
    ax3.plot(salt_min_NAP[o_i],depth_avg_NAP[o_i],line_style_m,label=model_min_label,color=model_min_c)
    ax3.plot(salt_max_NAP[o_i],depth_avg_NAP[o_i],line_style_m,color=model_max_c)

    ax3.set_xlabel(space+nutrients[1]+' (mmol m$^{-3}$)',fontsize=16)

    ax3.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax3.xaxis.set_label_position('top') # this moves the label to the top
    ax3.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax3.tick_params(axis='both',which='major',labelsize=tick_size)
    ax3.grid(True)

    # AP run
    # put these np.nan plots to plot the lines in the legend
    ax4.plot(np.nan,line_style_m,label=model_avg_label,color=model_avg_c)
    ax4.plot(np.nan,line_style_m,label=model_min_label,color=model_min_c)

    ax4.plot(salt_avg_AP[o_i],depth_avg_AP[o_i],line_style_m,label=model_avg_AP_l,color=model_avg_AP_c)
    ax4.plot(salt_min_AP[o_i],depth_avg_AP[o_i],line_style_m,label=model_min_AP_l,color=model_min_AP_c)
    ax4.plot(salt_max_AP[o_i],depth_avg_AP[o_i],line_style_m,color=model_max_AP_c)

    #ax4.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax4.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    #ax4.set_xlabel(nutrients[1]+' (mmol m$^{-3}$)',fontsize=xy_labels)
    ax4.xaxis.set_label_position('top') # this moves the label to the top
    ax4.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax4.tick_params(axis='both',which='major',labelsize=tick_size)
    ax4.legend(loc='upper right',fontsize=legend_size,bbox_to_anchor=(1.5,1))
    ax4.grid(True)

    title_info = ' 300 m Non-Anthropogenic run vs Anthropogenic Input run '
    save_name = 'profile_non_AP_vs_AP_'
    if type(month_chosen) is list:
        plt.suptitle(obs_name[o_i]+title_info+month_name[0]+'-'+month_name[-1]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+month_name[-1]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')
    else:
        plt.suptitle(obs_name[o_i]+title_info+month_name[0]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')

'''
fig1, (ax1, ax2) = plt.subplots(1,2,sharey=True,figsize=(14,9))
# plot observation
# Temperature
if o_i = 0:
ax1.plot(temp1,depth1,'o-',label='Observation',color='blue')
#ax1.plot(temp2,depth2,'o-',label='Model',color='red')
ax1.plot(temp_m_avg,depth2,'o-',label=model_avg_label,color=model_avg_c)
ax1.plot(temp_min,depth2,'--',label=model_min_label,color=model_min_c)
ax1.plot(temp_max,depth2,'--',label=model_max_label,color=model_max_c)
                                                                                                                                
ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
ax1.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
ax1.set_xlabel('Temperature (C)',fontsize=xy_labels)
ax1.xaxis.set_label_position('top') # this moves the label to the top
ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax1.tick_params(axis='both',which='major',labelsize=tick_size)
ax1.legend(loc='best',fontsize=legend_size)
ax1.grid(True)
# Salinity
ax2.plot(salt1,depth1,'o-r',label='Observation',color='blue')
#ax2.plot(salt2,depth2,'o-r',label='Model',color='red')
ax2.plot(salt_m_avg,depth2,'o-',label=model_avg_label,color=model_avg_c)
ax2.plot(salt_min,depth2,'--',label=model_min_label,color=model_min_c)
ax2.plot(salt_max,depth2,'--',label=model_max_label,color=model_max_c)
                                                                                                                                
ax2.set_xlabel('Salinity (psu)',fontsize=16)
#plt.xticks(fontsize=14)
#plt.yticks(fontsize=14)
ax2.xaxis.set_label_position('top') # this moves the label to the top
ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax2.tick_params(axis='both',which='major',labelsize=tick_size)
#ax2.yaxis.set_visible(False) # This erases the y ticks
ax2.legend(loc='best',fontsize=legend_size)
ax2.grid(True)
#plt.suptitle('OCSD Observation at 2004-05-02 vs 300 m Anthropogenic Input Model at 1997-05-02',fontsize=20)
plt.suptitle('OCSD Observation at 2004-02-05 vs Averaged 300 m Anthropogenic Input Model at 1997-02-05',fontsize=suptitle_size)
plt.savefig('obs_model_OCSD_AP_max_min.png',bbox_inches='tight')
#plt.show()
'''
