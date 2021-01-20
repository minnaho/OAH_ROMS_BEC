###########################
# map of surface currents
# vs model
###########################
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import pandas as pd
import ROMS_depths as rdepth
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pickle as pickle

fig_path = './figs/'

#######################
# ROMS-BEC outputs
#######################
# get 06-1999 - 06-2000 monthly average u/v
#out_path = '/data/project1/minnaho/validation/hydrodynamics/roms_slices/zslice_1997_2000_his/'
out_path = '/data/project1/minnaho/validation/hydrodynamics/roms_slices/zslice_1997_2000_avg/'
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'
grid_nc = Dataset(grid_path)
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
h_nc = np.array(grid_nc.variables['h'])
angle_nc = np.array(grid_nc.variables['angle'])
Lx_nc = lat_nc.shape[1]
Ly_nc = lat_nc.shape[0]

rom_fi = glob.glob(out_path+'*.nc')

# u and v arrays have 1 less on the xi/eta respectively
u_arr_05 = np.empty((len(rom_fi),h_nc.shape[0]-1,h_nc.shape[1]-1))
v_arr_05 = np.empty((len(rom_fi),h_nc.shape[0]-1,h_nc.shape[1]-1))
u_arr_50 = np.empty((len(rom_fi),h_nc.shape[0]-1,h_nc.shape[1]-1))
v_arr_50 = np.empty((len(rom_fi),h_nc.shape[0]-1,h_nc.shape[1]-1))

u_arr_05.fill(np.nan)
v_arr_05.fill(np.nan)
u_arr_50.fill(np.nan)
v_arr_50.fill(np.nan)


# calculate rho u and v
for r_i in range(len(rom_fi)):
    out_nc = Dataset(rom_fi[r_i],'r')
    u_nc = np.array(out_nc.variables['u'])
    v_nc = np.array(out_nc.variables['v'])

    u_nc[u_nc>1E10] = np.nan
    v_nc[v_nc>1E10] = np.nan

    u_arr_05[r_i,:] = 0.5*(u_nc[0][1:,:]+u_nc[0][:Ly_nc-1,:])
    v_arr_05[r_i,:] = 0.5*(v_nc[0][:,1:]+v_nc[0][:,:Lx_nc-1])
    u_arr_50[r_i,:] = 0.5*(u_nc[1][1:,:]+u_nc[1][:Ly_nc-1,:])
    v_arr_50[r_i,:] = 0.5*(v_nc[1][:,1:]+v_nc[1][:,:Lx_nc-1])

u_arr_05[u_arr_05>1E10] = np.nan
v_arr_05[v_arr_05>1E10] = np.nan
u_arr_50[u_arr_50>1E10] = np.nan
v_arr_50[v_arr_50>1E10] = np.nan

# pad endings to have same shape as lat_nc/lon_nc
u_arr_05_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
v_arr_05_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
u_arr_05_rho.fill(np.nan)
v_arr_05_rho.fill(np.nan)

u_arr_05_rho[:,:-1,:-1] = u_arr_05[:,:,:]
v_arr_05_rho[:,:-1,:-1] = v_arr_05[:,:,:]

u_arr_50_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
v_arr_50_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
u_arr_50_rho.fill(np.nan)
v_arr_50_rho.fill(np.nan)

u_arr_50_rho[:,:-1,:-1] = u_arr_50[:,:,:]
v_arr_50_rho[:,:-1,:-1] = v_arr_50[:,:,:]

sum_in = []
win_in = []
# find summer and winter inds
# get month number from name
# slicing for string of month number e.g., 06/07/08
for r_i in range(len(rom_fi)):
    nm_in = rom_fi[r_i].index('M')
    if (
        rom_fi[r_i][nm_in+1:nm_in+3] == '06' or
        rom_fi[r_i][nm_in+1:nm_in+3] == '07' or
        rom_fi[r_i][nm_in+1:nm_in+3] == '08'):
        sum_in.append(r_i)
 
    if (
        rom_fi[r_i][nm_in+1:nm_in+3] == '01' or
        rom_fi[r_i][nm_in+1:nm_in+3] == '02' or
        rom_fi[r_i][nm_in+1:nm_in+3] == '12'):
        win_in.append(r_i)

# rotate angle to true east and north
u_rot_05 = (u_arr_05_rho*np.cos(angle_nc))-(v_arr_05_rho*np.sin(angle_nc))
v_rot_05 = (v_arr_05_rho*np.cos(angle_nc))+(u_arr_05_rho*np.sin(angle_nc))

u_rot_50 = (u_arr_50_rho*np.cos(angle_nc))-(v_arr_50_rho*np.sin(angle_nc))
v_rot_50 = (v_arr_50_rho*np.cos(angle_nc))+(u_arr_50_rho*np.sin(angle_nc))


# avg u and v win and sum
u_sum_05 = np.nanmean(u_rot_05[sum_in,:,:],axis=0)
v_sum_05 = np.nanmean(v_rot_05[sum_in,:,:],axis=0)

u_win_05 = np.nanmean(u_rot_05[win_in,:,:],axis=0)
v_win_05 = np.nanmean(v_rot_05[win_in,:,:],axis=0)

u_sum_50 = np.nanmean(u_rot_50[sum_in,:,:],axis=0)
v_sum_50 = np.nanmean(v_rot_50[sum_in,:,:],axis=0)
                              
u_win_50 = np.nanmean(u_rot_50[win_in,:,:],axis=0)
v_win_50 = np.nanmean(v_rot_50[win_in,:,:],axis=0)

# read in hf data
hf_path = 'LTA_USWC-month-LTA-6km.nc'
hf_nc = Dataset(hf_path,'r')
hf_lat = np.array(hf_nc.variables['lat'])
hf_lon = np.array(hf_nc.variables['lon'])
hf_u_avg = np.array(hf_nc.variables['u_mean'])
hf_v_avg = np.array(hf_nc.variables['v_mean'])
hf_time_nc = np.array(hf_nc.variables['time'])
hf_timeunit = hf_nc.variables['time'].units

hf_u_avg[hf_u_avg<-32000] = np.nan
hf_v_avg[hf_v_avg<-32000] = np.nan

hf_dt = num2date(hf_time_nc,hf_timeunit,only_use_cftime_datetimes=False)

hf_sum_ind = []
hf_win_ind = []
for h_i in range(len(hf_dt)):
    m_i = hf_dt[h_i].month
    if (m_i == 6 or
        m_i == 7 or
        m_i == 8):
        hf_sum_ind.append(h_i)
    if (m_i == 1 or
        m_i == 2 or
        m_i == 12):
        hf_win_ind.append(h_i)

# seasonal average
hf_u_sum = np.nanmean(hf_u_avg[hf_sum_ind],axis=0)
hf_v_sum = np.nanmean(hf_v_avg[hf_sum_ind],axis=0)

hf_u_win = np.nanmean(hf_u_avg[hf_win_ind],axis=0)
hf_v_win = np.nanmean(hf_v_avg[hf_win_ind],axis=0)

# load adcp and profile data



########
# plot
########
plt.ion()

coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')

lat_plt = lat_nc
lon_plt = lon_nc


u_sum_05_plt = u_sum_05
v_sum_05_plt = v_sum_05
               
u_win_05_plt = u_win_05
v_win_05_plt = v_win_05
               
u_sum_50_plt = u_sum_50
v_sum_50_plt = v_sum_50
                   
u_win_50_plt = u_win_50
v_win_50_plt = v_win_50

u_sum_05_plt[u_sum_05_plt==0] = np.nan
v_sum_05_plt[v_sum_05_plt==0] = np.nan
            
u_win_05_plt[u_win_05_plt==0] = np.nan
v_win_05_plt[v_win_05_plt==0] = np.nan
            
u_sum_50_plt[u_sum_50_plt==0] = np.nan
v_sum_50_plt[v_sum_50_plt==0] = np.nan
            
u_win_50_plt[u_win_50_plt==0] = np.nan
v_win_50_plt[v_win_50_plt==0] = np.nan

# reduce nuber of arrows by plotting every xth arrow
freq_rom = 60
freq_hff = 5
# start index (changes which arrows are plotted)
in_rom = 10
in_hff = 10

# bightwide
lat_min = 32.4
lat_max = 34.6
lon_min = -120.5
lon_max = -117
# la and oc
#lat_min = 33.35
#lat_max = 34.05
#lon_min = -118.9
#lon_max = -117.6
# la and oc zoomed
#lat_min = 33.5
#lat_max = 33.9
#lon_min = -118.6
#lon_max = -117.8
extent = [lon_min,lon_max,lat_min,lat_max]

fig_w = 16
fig_h = 12

# line widths
lw_hff = 2
lw_rom = .5

xkey = .72
ykey = .81

quivscale = 2
shaft_w = .001
hwidth = 10
hlength = 10

fig,axes = plt.subplots(1,2,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

##################
# 5 m
##################
# summer
# plot roms
q_plt_5m_roms_sum = axes.flat[0].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],u_sum_05_plt[in_rom::freq_rom,in_rom::freq_rom],v_sum_05_plt[in_rom::freq_rom,in_rom::freq_rom],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor='k',linewidth=lw_rom)

# plot hf
q_plt_5m_hf_sum = axes.flat[0].quiver(hf_lon[::freq_hff],hf_lat[::freq_hff],hf_u_sum[::freq_hff,::freq_hff],hf_v_sum[::freq_hff,::freq_hff],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor='r',linewidth=lw_hff)


# winter
# plot roms
q_plt_5m_roms_win = axes.flat[1].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],u_win_05_plt[in_rom::freq_rom,in_rom::freq_rom],v_win_05_plt[in_rom::freq_rom,in_rom::freq_rom],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor='k',linewidth=lw_rom)

# plot hf
q_plt_5m_hf_win = axes.flat[1].quiver(hf_lon[::freq_hff],hf_lat[::freq_hff],hf_u_win[::freq_hff,::freq_hff],hf_v_win[::freq_hff,::freq_hff],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor='r',linewidth=lw_hff)

# quiver key
axes.flat[0].quiverkey(q_plt_5m_roms_sum,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[0].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[0].transAxes,fontsize=18)

axes.flat[1].quiverkey(q_plt_5m_roms_win,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[1].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[1].transAxes,fontsize=18)

axes.flat[0].set_title('summer surface',fontsize=18)
axes.flat[1].set_title('winter surface',fontsize=18)

step_lon = 0.75
step_lat = 0.3
for i in range(len(axes.flat)):
    gl = axes.flat[i].gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlabel_style = {'size':18}
    gl.ylabel_style = {'size':18}
    axes.flat[i].add_feature(coast_10m,facecolor='None',edgecolor='k')
    gl.xlocator = mticker.FixedLocator(list(np.arange(lon_min,lon_max+step_lon,step_lon)))
    gl.ylocator = mticker.FixedLocator(list(np.arange(lat_min,lat_max+step_lat,step_lat)))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    axes.flat[i].set_extent(extent)

fig.savefig(fig_path+'hf_map_season.png',bbox_inches='tight')
