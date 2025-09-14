###################################################################
# read central bight data 
# Nov 15 2018 Minna Ho minnaho@ucla.edu
################################################################
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import seawater as sw
from scipy.signal import savgol_filter
plt.ion()

# choose variable
variable_name1 = 'temperature'
variable_name2 = 'salinity'

# choose months to look at
#month_chosen = [12,1,2]
month_chosen = [6,7,8]


# text of title of plot
#title_text = 'winter months OCSD'
title_text = 'summer months OCSD'

# save figs path
save_figs = './figs/'

##########################
# load observation data
#########################
#data_file = Dataset('central_bight_master_database_1998_2017_validation_2023.nc','r')
data_file = Dataset('central_bight_master_database_1998_2017.nc','r')

# time
time_num = data_file.variables['time']
time_unit = time_num.units

# locations
sites = np.asarray(data_file.variables['position'])
lats = np.asarray(data_file.variables['latitude'])
lons = np.asarray(data_file.variables['longitude'])

# depths
depths = np.array((data_file.variables['depth']))

# variable
var_data1 = np.asarray(data_file.variables[variable_name1])
var_data2 = np.asarray(data_file.variables[variable_name2])

# chosen month
##################
month_name = []
if type(month_chosen) is list:
    for m_n in month_chosen:
        month_name.append(calendar.month_abbr[m_n])
else:
    month_name.append(calendar.month_abbr[month_chosen])

# convert datetime numbers to dates
time_num_arr = np.asarray(time_num)
date_conv = num2date(time_num_arr,time_unit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# get indexes of target months
month_ind_l = []
for ind_d,d_i in enumerate(date_conv):
    if d_i.month in month_chosen:
        month_ind_l.append(ind_d) 

month_ind = np.array((month_ind_l))

# choose between what lat/lon
##############################

# bight
'''
lat_min = 33
lat_max = 34
lon_min = -119
lon_max = -117.2
'''


# OCSD (no calcofi sampling sites in this range)
lat_min = 33.55
lat_max = 33.6
lon_min = -118.05
lon_max = -117.97

lat_ind = np.where((lats>lat_min) & (lats<lat_max))[0]
lon_ind = np.where((lons>lon_min) & (lons<lon_max))[0]

# find intersection of index values
loc_ind = np.asarray((list(set(lat_ind).intersection(lon_ind))))

# find months and locations that we want
#########################################
data_slice1 = var_data1[month_ind][:,loc_ind,:]
data_slice1[data_slice1==0] = np.nan
data_slice2 = var_data2[month_ind][:,loc_ind,:]
data_slice2[data_slice2==0] = np.nan

# get time and location mean
#temp_avg = np.nanmean(np.nanmean(data_slice1,axis=0),axis=0)
#salt_avg = np.nanmean(np.nanmean(data_slice2,axis=0),axis=0)
temp_avg = np.nanmean(data_slice1,axis=(0,1))
salt_avg = np.nanmean(data_slice2,axis=(0,1))

# get standard deviation
temp_std = np.nanstd(data_slice1,axis=(0,1))
salt_std = np.nanstd(data_slice2,axis=(0,1))
#depths = range(1,101)
#depths = range(1,len(temp_avg)+1)

# smooth the data
temp_smooth = savgol_filter(temp_avg,11,3)
salt_smooth = savgol_filter(salt_avg,11,3)

#np.save('ocsd_summer_temp_obs.npy',data_slice1)
#np.save('ocsd_summer_salt_obs.npy',data_slice2)
#np.save('ocsd_winter_temp_obs.npy',data_slice1)
#np.save('ocsd_winter_salt_obs.npy',data_slice2)

#################
# PLOTTING
#################
suptitle_size = 20
xy_labels = 16
tick_size = 14
legend_size = 14

N = 60

fig1, (ax1, ax2) = plt.subplots(1,2,sharey=True,figsize=(16,9))
fig1.suptitle(title_text,fontsize=suptitle_size)

ax1.plot(temp_avg[:N],depths[:N],color='red')
ax1.plot(temp_smooth[:N],depths[:N],color='red',linestyle='--')
ax1.plot(temp_avg[:N]-temp_std[:N],depths[:N],color='blue')
ax1.plot(temp_avg[:N]+temp_std[:N],depths[:N],color='blue')
#ax1.fill_betweenx(range(len(temp_avg)),temp_avg-temp_std,temp_avg+temp_std)
ax1.xaxis.set_label_position('top') # this moves the label to the top
#ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax1.set_xlabel('Temperature (C)',fontsize=xy_labels)
ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
ax1.tick_params(axis='both',which='major',labelsize=tick_size)
ax1.grid(True)
#ax1.invert_yaxis()
#ax1.set_ylim(ax1.get_ylim()[::-1])

ax2.plot(salt_avg[:N],depths[:N],color='red')
ax2.plot(salt_smooth[:N],depths[:N],color='red',linestyle='--')
ax2.plot(salt_avg[:N]-salt_std[:N],depths[:N],color='blue')
ax2.plot(salt_avg[:N]+salt_std[:N],depths[:N],color='blue')
#ax2.fill_betweenx(range(len(salt_avg)),salt_avg-salt_std,salt_avg+salt_std)
ax2.xaxis.set_label_position('top') # this moves the label to the top
#ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax2.set_xlabel('Salinity (PSU)',fontsize=xy_labels)
ax2.set_ylabel('Depth (m)',fontsize=xy_labels)
ax2.tick_params(axis='both',which='major',labelsize=tick_size)
ax2.grid(True)
ax2.invert_yaxis()
#ax2.set_ylim(ax1.get_ylim()[::-1])
#plt.savefig('winter_pipe_OCSD.png',bbox_inches='tight')
plt.savefig('summer_pipe_OCSD.png',bbox_inches='tight')

#dens = sw.dens0(salt_avg[:N],temp_avg[:N])
dens = sw.dens0(salt_smooth[:64],temp_smooth[:64])
fig3,ax3 = plt.subplots(1,1,figsize=[6,8])
ax3.plot(dens,depths[:64])
ax3.invert_yaxis()
#dens_smooth = savgol_filter(dens,11,3)
#ax3.plot(dens_smooth,depths[:N])

np.savetxt('ocsd_typical_summer_temp.txt',temp_smooth[:64],fmt='%.18f')
np.savetxt('ocsd_typical_summer_salt.txt',salt_smooth[:64],fmt='%.18f')
#np.savetxt('ocsd_typical_winter_temp.txt',temp_smooth[:64],fmt='%.18f')
#np.savetxt('ocsd_typical_winter_salt.txt',salt_smooth[:64],fmt='%.18f')

utemp = temp_smooth-11
utemp[63] = 0.01
# the top of the thermocline is ~F = 0.1 and goes to F = 0 at
# the bottom of the domain
usmall = utemp[:64]*0.84*0.01 # scale it smaller magnitude and to m/s
ubar_small = np.nanmean(usmall)

fig4,ax4 = plt.subplots(1,1,figsize=[6,8])
ax4.plot(usmall,depths[:64])
ax4.invert_yaxis()

utemp = temp_smooth[:64]-5
# the top of the thermocline is ~F = 1 and goes to F = 0.1 at
# the bottom of the domain
ularge = utemp[:64]*1.11*0.01 # scale it  and to m/s
ularge[:11] = ularge[:11]*(1/1.055555)
ularge[11:15] = ularge[11:15]*(1/1.03)
ularge_smooth = savgol_filter(ularge,11,3)
ubar_large = np.nanmean(ularge_smooth)

fig4,ax4 = plt.subplots(1,1,figsize=[6,8])
#ax4.plot(ularge,depths[:64])
ax4.plot(ularge_smooth,depths[:64])
ax4.invert_yaxis()

np.savetxt('ocsd_typical_summer_u_F0_F01.txt',usmall,fmt='%.18f')
np.savetxt('ocsd_typical_summer_u_F01_F1.txt',ularge_smooth,fmt='%.18f')
