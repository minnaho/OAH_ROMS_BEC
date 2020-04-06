##########################
# plot OCSD ADCP data
# plot depth vs time 2d ocean profile 
##########################
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import calendar
import cmocean
plt.ion()

#######################################
# time incorrect because
# imshow extent spaces out
# time to be evently spaced,
# not the time the data is actually at
#######################################

##############################
# CHANGE FILE AND MONTHS HERE
##############################
#month_chosen = [1,2,3,4,5,6,7,8,9,10,11,12]
month_chosen = [11,12,1]
nc_file = 'OCSD_M18.nc'
mooring = 'OCSD M18'

data_path = '/data/project1/minnaho/validation/validation_data_moorings/OCSD_ADCP/'

data_nc = Dataset(data_path+nc_file,'r')

time_nc = np.array(data_nc.variables['time'][:])
time_unit = data_nc.variables['time'].units
depth_nc = np.array(data_nc.variables['depth'][:])

u_nc = np.array(data_nc.variables['u'][:])
v_nc = np.array(data_nc.variables['v'][:])
w_nc = np.array(data_nc.variables['w'][:])

speed = (u_nc**2 + v_nc**2)**.5

lat_nc = np.array(data_nc.variables['latitude'])[0]
lon_nc = np.array(data_nc.variables['longitude'])[0]

month_name = []
if type(month_chosen) is list:
    for m_n in month_chosen:
        month_name.append(calendar.month_abbr[m_n])
else:
    month_name.append(calendar.month_abbr[month_chosen])

# convert datetime numbers to dates
date_conv = num2date(time_nc,time_unit)

# get indexes of target months
month_ind_l = []
for ind_d,d_i in enumerate(date_conv):
    if d_i.month in month_chosen:
        month_ind_l.append(ind_d)

month_ind = np.array((month_ind_l))

# flip array because it is meters from the bottom
#u_plot = u_nc[:,::-1]
#v_plot = v_nc[:,::-1]
#w_plot = w_nc[:,::-1]

u_plot = np.transpose(u_nc[month_ind,:])
v_plot = np.transpose(v_nc[month_ind,:])
speed_plot = np.transpose(speed[month_ind,:])

time_plot = time_nc[month_ind]

date_spliced = date_conv[month_ind]
date_plot = matplotlib.dates.date2num(date_spliced)
mpl_date = matplotlib.dates.num2date(date_plot)

v_min = -1.
v_max = 1.
# for contourf
#level_range = np.linspace(v_min,v_max,20+1)

# plot
axis_size = 14

c_map = cmocean.cm.speed
c_map_u_v = 'seismic'
c_map_speed = 'viridis'

fig1, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(14,9),sharex=True,sharey=True)
fig1.suptitle(month_name[0]+' - '+month_name[-1]+' '+mooring+' ADCP '+str(lat_nc)+', '+str(lon_nc),fontsize=20)
'''
#plt1 = ax1.contourf(time_plot,depth_nc,u_plot,levels=level_range,cmap=c_map,vmin=v_min,vmax=v_max)
#plt2 = ax2.contourf(time_plot,depth_nc,v_plot,levels=level_range,cmap=c_map,vmin=v_min,vmax=v_max)
plt1 = ax1.pcolormesh(time_plot,depth_nc,u_plot,cmap=c_map,vmin=v_min,vmax=v_max)
plt2 = ax2.pcolormesh(time_plot,depth_nc,v_plot,cmap=c_map,vmin=v_min,vmax=v_max)
#ax1.set_ylim(ax1.get_ylim()[::-1])

'''
plt1 = ax1.imshow(u_plot,cmap=c_map_u_v,aspect='auto',vmin=v_min,vmax=v_max,extent=[date_plot[0],date_plot[-1],u_plot.shape[0],0])
plt2 = ax2.imshow(v_plot,cmap=c_map_u_v,aspect='auto',vmin=v_min,vmax=v_max,extent=[date_plot[0],date_plot[-1],u_plot.shape[0],0])
plt3 = ax3.imshow(speed_plot,cmap=c_map_speed,aspect='auto',vmin=0,vmax=v_max,extent=[date_plot[0],date_plot[-1],u_plot.shape[0],0])



#ax3.xaxis_date()
#date_format = matplotlib.dates.DateFormatter('%Y-%m')
#ax3.xaxis.set_major_formatter(date_format)

ax1.set_ylim(ax1.get_ylim()[::-1])
ax2.set_ylim(ax2.get_ylim()[::-1])
ax3.set_ylim(ax3.get_ylim()[::-1])

ax2.set_ylabel('meters from the bottom',fontsize=axis_size)
ax3.set_xlabel('Time (hours)',fontsize=axis_size)
ax1.set_title('u (East-West velocity) m/s',fontsize=axis_size)
ax2.set_title('v (North-South velocity) m/s',fontsize=axis_size)
ax3.set_title('Speed m/s',fontsize=axis_size)

ax1.tick_params(axis='both',which='major',labelsize=14)
ax2.tick_params(axis='both',which='major',labelsize=14)
ax3.tick_params(axis='both',which='major',labelsize=14,rotation=45)

#cbar1 = fig1.colorbar(plt1,ax=ax1)
#cbar2 = fig1.colorbar(plt2,ax=ax2)
#cbar2 = fig1.colorbar(plt1,ax=ax1,aspect=9)
cbar1 = fig1.colorbar(plt2,ax=[ax1,ax2])
cbar3 = fig1.colorbar(plt3,ax=ax3,aspect=9)
cbar1.ax.tick_params(labelsize=14)
cbar3.ax.tick_params(labelsize=14)
#cbar2.ax.tick_params(labelsize=14)
cbar1.set_label('magnitude',size=axis_size)
cbar3.set_label('magnitude',size=axis_size)
#plt.savefig('test.png',bbox_inches='tight')
