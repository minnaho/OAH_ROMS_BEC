###################################################################
# read calcofi data
# and compate to L2 SCB (300 m) AP (anthropogenic input) model
# Nov 9 2018 Minna Ho minnaho@ucla.edu
################################################################
import numpy as np
#import matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import depths as depths
import calendar
#plt.ion()

# save figs path
save_figs = './figs/'

##########################
# load observation data
#########################
text_file = pd.read_csv('calcofi_database.csv',header=None,low_memory=False,skiprows=1)

time_unit = 'minutes since 1949-03-01 09:30:00'

# choose variable
##################
variable_name = 'temperature'
var_unit = 'degrees C'
var_num = 20

# chosen month
##################
month_chosen = [2,3]
month_name = []
if type(month_chosen) is list:
    for m_n in month_chosen:
        month_name.append(calendar.month_abbr[m_n])
else:
    month_name.append(calendar.month_abbr[month_chosen])

# convert datetime numbers to dates
time_num = np.array((text_file.iloc[:,1]))
date_conv = num2date(time_num,time_unit)

# get indexes of target months
month_ind_l = []
for ind_d,d_i in enumerate(date_conv):
    if d_i.month in month_chosen:
        month_ind_l.append(ind_d) 

month_ind = np.array((month_ind_l))

# choose between what lat/lon
##############################

# bight
lat_min = 33
lat_max = 34
lon_min = -119
lon_max = -117.2

'''
# OCSD (no calcofi sampling sites in this range)
lat_min = 33.47
lat_max = 33.55
lon_min = -118.1
lon_max = -117.8
'''

lat_col = np.array((text_file.iloc[:,2]))
lon_col = np.array((text_file.iloc[:,3]))

lat_ind = np.where((lat_col>lat_min) & (lat_col<lat_max))[0]
lon_ind = np.where((lon_col>lon_min) & (lon_col<lon_max))[0]

# find intersection of index values
loc_ind = np.asarray((list(set(lat_ind).intersection(lon_ind))))

# find months and locations that we want
#########################################
data_ind = np.asarray(sorted((list(set(loc_ind).intersection(month_ind)))))

# get variable data and depths for these months and locations
######################################################
data_var = np.array((text_file.iloc[:,var_num][data_ind]))
data_depths = np.array((text_file.iloc[:,19][data_ind]))

################################################
# find where depth = 0 to separate profiles and 
# take 25% and 75% 
################################################
profile_ind = np.where(data_depths==0)[0]

max_indices = max([profile_ind[i+1]-profile_ind[i] for i in range(len(profile_ind)-1)])

data_profiles = np.empty((len(profile_ind)-1,max_indices))
data_profiles.fill(np.nan)
depth_profiles = np.empty((len(profile_ind)-1,max_indices))
depth_profiles.fill(np.nan)
 
for p_i in range(len(data_profiles)):
    data_profiles[p_i,:len(data_var[profile_ind[p_i]:profile_ind[p_i+1]])] = data_var[profile_ind[p_i]:profile_ind[p_i+1]]
    depth_profiles[p_i,:len(data_depths[profile_ind[p_i]:profile_ind[p_i+1]])] = data_depths[profile_ind[p_i]:profile_ind[p_i+1]]

# unsure if can find 25% and 75% because of wildly differing depths
# would have to make depth array with depths 0 - max(depth) every meter
# find 25% and 75%
data_profiles_25 = np.nanpercentile(data_profiles,25,axis=0)
temp_ocsd_25 = np.nanpercentile(temp_ocsd,25,axis=0)
temp_jwpcp_25 = np.nanpercentile(temp_jwpcp,25,axis=0)
temp_htp_25 = np.nanpercentile(temp_htp,25,axis=0)

salt_plwtp_25 = np.nanpercentile(salt_plwtp,25,axis=0)
salt_ocsd_25 = np.nanpercentile(salt_ocsd,25,axis=0)
salt_jwpcp_25 = np.nanpercentile(salt_jwpcp,25,axis=0)
salt_htp_25 = np.nanpercentile(salt_htp,25,axis=0)

depth_plwtp_25 = np.nanpercentile(depth_plwtp,25,axis=0)
depth_ocsd_25 = np.nanpercentile(depth_ocsd,25,axis=0)
depth_jwpcp_25 = np.nanpercentile(depth_jwpcp,25,axis=0)
depth_htp_25 = np.nanpercentile(depth_htp,25,axis=0)

temp_plwtp_75 = np.nanpercentile(temp_plwtp,75,axis=0)
temp_ocsd_75 = np.nanpercentile(temp_ocsd,75,axis=0)
temp_jwpcp_75 = np.nanpercentile(temp_jwpcp,75,axis=0)
temp_htp_75 = np.nanpercentile(temp_htp,75,axis=0)

salt_plwtp_75 = np.nanpercentile(salt_plwtp,75,axis=0)
salt_ocsd_75 = np.nanpercentile(salt_ocsd,75,axis=0)
salt_jwpcp_75 = np.nanpercentile(salt_jwpcp,75,axis=0)
salt_htp_75 = np.nanpercentile(salt_htp,75,axis=0)

depth_plwtp_75 = np.nanpercentile(depth_plwtp,75,axis=0)
depth_ocsd_75 = np.nanpercentile(depth_ocsd,75,axis=0)
depth_jwpcp_75 = np.nanpercentile(depth_jwpcp,75,axis=0)
depth_htp_75 = np.nanpercentile(depth_htp,75,axis=0)

######################
# load model data
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
        output_path = '/data/project5/kesf/ROMS/L2_SCB_AP/AVG_Y1997M'+'%02d'%m_l+'/'
        file_name = 'l2_scb_avg.*'
        roms_files.append(sorted(glob.glob(output_path+file_name)))
    roms_files = [j for i in roms_files for j in i] # join all lists within list into one
else:
    output_path = '/data/project3/kesf/ROMS/L2_SCB_AP/AVG_Y1997M'+'%02d'%month_chosen+'/'
    file_name = 'l2_scb_avg.*'
    roms_files = sorted(glob.glob(output_path+file_name))

# (day, location, grid point, s_rho)
temp_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
salt_outfalls = np.empty((len(roms_files),len(coord_i),9,60))
depth_outfalls = np.empty((len(roms_files),len(coord_i),9,60))

nutrients = ['temp','salt']

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

temp_min = np.empty((4,60))
temp_max = np.empty((4,60))
temp_avg= np.empty((4,60))
salt_min = np.empty((4,60))
salt_max = np.empty((4,60))
salt_avg = np.empty((4,60))
depth_min = np.empty((4,60))
depth_max = np.empty((4,60))
depth_avg = np.empty((4,60))

# find minimum across each day and 9 grid points
for loc_m in range(len(coord_i)):
    temp_min[loc_m,:] = np.min(np.min(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_max[loc_m,:] = np.max(np.max(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    temp_avg[loc_m,:] = np.average(np.average(temp_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_min[loc_m,:] = np.min(np.min(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_max[loc_m,:] = np.max(np.max(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    salt_avg[loc_m,:] = np.average(np.average(salt_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_min[loc_m,:] = np.min(np.min(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    #depth_max[loc_m,:] = np.max(np.max(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
    depth_avg[loc_m,:] = np.average(np.average(depth_outfalls[:,loc_m,:,:],axis=0),axis=0)
 

#################
# PLOTTING
#################
suptitle_size = 20
xy_labels = 16
tick_size = 14
legend_size = 14

obs_label = 'Observation'
label_25 = 'Obs 25th percentile'
label_75 = 'Obs 75th percentile'

model_avg_label = 'Model average'
model_avg_c = 'blue'
model_min_label = 'Model minimum'
model_min_c = 'teal'
model_max_label = 'Model maximum'
model_max_c = 'teal'


obs_c_25 = 'dimgrey'
obs_c_75 = 'dimgrey'

obs_name = ['PLWTP','OCSD','JWPCP','HTP']

line_style_obs = 'o-'
marker_size_obs = 5

# plot 25 and 75 percentile observations
# loop over 4 outfalls
for o_i in range(len(temp_min)):
    # Two-panel plot
    fig1, (ax1, ax2) = plt.subplots(1,2,sharey=True,figsize=(14,9))
    # plot observation
    # Temperature
    ax1.plot(temp_avg[o_i],depth_avg[o_i],line_style_obs,label=model_avg_label,color=model_avg_c)
    ax1.plot(temp_min[o_i],depth_avg[o_i],line_style_obs,label=model_min_label,color=model_min_c)
    ax1.plot(temp_max[o_i],depth_avg[o_i],line_style_obs,label=model_max_label,color=model_max_c)
    if o_i == 0:
        ax1.plot(temp_plwtp_25,depth_plwtp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax1.plot(temp_plwtp_75,depth_plwtp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 1:
        ax1.plot(temp_ocsd_25,depth_ocsd_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax1.plot(temp_ocsd_75,depth_ocsd_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 2:
        ax1.plot(temp_jwpcp_25,depth_jwpcp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax1.plot(temp_jwpcp_75,depth_jwpcp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 3:
        ax1.plot(temp_htp_25,depth_htp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax1.plot(temp_htp_75,depth_htp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)


    ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax1.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    ax1.set_xlabel('Temperature (C)',fontsize=xy_labels)
    ax1.xaxis.set_label_position('top') # this moves the label to the top
    ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax1.tick_params(axis='both',which='major',labelsize=tick_size)
    #ax1.legend(loc='best',fontsize=legend_size)
    ax1.grid(True)

    # Salinity
    ax2.plot(salt_avg[o_i],depth_avg[o_i],line_style_obs,label=model_avg_label,color=model_avg_c)
    ax2.plot(salt_min[o_i],depth_avg[o_i],line_style_obs,label=model_min_label,color=model_min_c)
    ax2.plot(salt_max[o_i],depth_avg[o_i],line_style_obs,label=model_max_label,color=model_max_c)
    if o_i == 0:
        ax2.plot(salt_plwtp_25,depth_plwtp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax2.plot(salt_plwtp_75,depth_plwtp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 1:
        ax2.plot(salt_ocsd_25,depth_ocsd_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax2.plot(salt_ocsd_75,depth_ocsd_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 2:
        ax2.plot(salt_jwpcp_25,depth_jwpcp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax2.plot(salt_jwpcp_75,depth_jwpcp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)
    if o_i == 3:
        ax2.plot(salt_htp_25,depth_htp_25,line_style_obs,label=label_25,color=obs_c_25,markersize=marker_size_obs)
        ax2.plot(salt_htp_75,depth_htp_75,line_style_obs,label=label_75,color=obs_c_75,markersize=marker_size_obs)

    ax2.grid(True)
    ax2.set_xlabel('Salinity (psu)',fontsize=16)
    #plt.xticks(fontsize=14)
    #plt.yticks(fontsize=14)
    ax2.xaxis.set_label_position('top') # this moves the label to the top
    ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax2.tick_params(axis='both',which='major',labelsize=tick_size)
    #ax2.yaxis.set_visible(False) # This erases the y ticks
    ax2.legend(loc='upper right',fontsize=legend_size,bbox_to_anchor=(1.3,1))
    
    title_info = ' Observation vs Anthropogenic Input Model '
    save_name = 'percentile_obs_model_AP_'
    if type(month_chosen) is list:
        obs_info = ' '+month_name[0]+'-'+month_name[-1]+' 2004-2017'
        plt.suptitle(obs_name[o_i]+obs_info+title_info+month_name[0]+'-'+month_name[-1]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+month_name[-1]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')
    else:
        obs_info = month_name[0]+' 2004-2017'
        plt.suptitle(obs_name[o_i]+obs_info+title_info+month_name[0]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')
'''
line_style_obs = 'o'
# loop over 4 outfalls
for o_i in range(len(temp_min)):
    # Two-panel plot
    fig1, (ax1, ax2) = plt.subplots(1,2,sharey=True,figsize=(14,9))
    # plot observation
    # Temperature
    ax1.plot(temp_avg[o_i],depth_avg[o_i],line_style_obs,label=model_avg_label,color=model_avg_c)
    ax1.plot(temp_min[o_i],depth_avg[o_i],line_style_obs,label=model_min_label,color=model_min_c)
    ax1.plot(temp_max[o_i],depth_avg[o_i],line_style_obs,label=model_max_label,color=model_max_c)
    if o_i == 0:
        ax1.plot(temp_plwtp,depth_plwtp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 1:
        ax1.plot(temp_ocsd,depth_ocsd,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 2:
        ax1.plot(temp_jwpcp,depth_jwpcp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 3:
        ax1.plot(temp_htp,depth_htp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)


    ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
    ax1.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    ax1.set_xlabel('Temperature (C)',fontsize=xy_labels)
    ax1.xaxis.set_label_position('top') # this moves the label to the top
    ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax1.tick_params(axis='both',which='major',labelsize=tick_size)
    #ax1.legend(loc='best',fontsize=legend_size)
    ax1.grid(True)

    # Salinity
    ax2.plot(salt_avg[o_i],depth_avg[o_i],line_style_obs,label=model_avg_label,color=model_avg_c)
    ax2.plot(salt_min[o_i],depth_avg[o_i],line_style_obs,label=model_min_label,color=model_min_c)
    ax2.plot(salt_max[o_i],depth_avg[o_i],line_style_obs,label=model_max_label,color=model_max_c)
    if o_i == 0:
        ax2.plot(salt_plwtp,depth_plwtp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 1:
        ax2.plot(salt_ocsd,depth_ocsd,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 2:
        ax2.plot(salt_jwpcp,depth_jwpcp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)
    if o_i == 3:
        ax2.plot(salt_htp,depth_htp,line_style_obs,label=obs_label,color=obs_c,markersize=marker_size_obs)

    ax2.set_xlabel('Salinity (psu)',fontsize=16)

    #plt.xticks(fontsize=14)
    #plt.yticks(fontsize=14)
    ax2.xaxis.set_label_position('top') # this moves the label to the top
    ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
    ax2.tick_params(axis='both',which='major',labelsize=tick_size)
    #ax2.yaxis.set_visible(False) # This erases the y ticks
    
    title_info = ' Observation vs Anthropogenic Input Model '
    save_name = 'obs_model_AP_'
    if type(month_chosen) is list:
        obs_info = month_name[0]+'-'+month_name[-1]+' 2004-2017'
        plt.suptitle(obs_info+obs_name[o_i]+title_info+month_name[0]+'-'+month_name[-1]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+month_name[-1]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')
    else:
        obs_info = month_name[0]+' 2004-2017'
        plt.suptitle(obs_info+obs_name[o_i]+title_info+month_name[0]+' 1997',fontsize=suptitle_size)
        plt.savefig(save_figs+save_name+nutrients[0]+'_'+nutrients[1]+'_'+month_name[0]+'_'+obs_name[o_i]+'.png',bbox_inches='tight')
'''
