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

# read in mooring data
moor_path = '/data/project1/minnaho/validation/hydrodynamics/moor_npy/'

#oc
# lat/lon
oc_lat_7m = np.load(moor_path+'oc_lat_7m.npy')
oc_lon_7m = np.load(moor_path+'oc_lon_7m.npy')

oc_lat_50m = np.load(moor_path+'oc_lat_50m.npy')
oc_lon_50m = np.load(moor_path+'oc_lon_50m.npy')

oc_lat_5m_0 = np.load(moor_path+'oc_lat_5m_0.npy')
oc_lon_5m_0 = np.load(moor_path+'oc_lon_5m_0.npy')

oc_lat_5m_1 = np.load(moor_path+'oc_lat_5m_1.npy')
oc_lon_5m_1 = np.load(moor_path+'oc_lon_5m_1.npy')

oc_lat_5m_2 = np.load(moor_path+'oc_lat_5m_2.npy')
oc_lon_5m_2 = np.load(moor_path+'oc_lon_5m_2.npy')

# u/v
# average each location
oc_7m_sum_u = np.nanmean(np.load(moor_path+'oc_7m_sum_u.npy'))
oc_7m_sum_v = np.nanmean(np.load(moor_path+'oc_7m_sum_v.npy'))
                                                             
oc_7m_win_u = np.nanmean(np.load(moor_path+'oc_7m_win_u.npy'))
oc_7m_win_v = np.nanmean(np.load(moor_path+'oc_7m_win_v.npy'))

oc_5m_win_u0 =np.nanmean(np.load(moor_path+'oc_5m_win_u0.npy'))
oc_5m_win_v0 =np.nanmean(np.load(moor_path+'oc_5m_win_v0.npy'))

oc_5m_sum_u0 =np.nanmean(np.load(moor_path+'oc_5m_sum_u0.npy'))
oc_5m_sum_v0 =np.nanmean(np.load(moor_path+'oc_5m_sum_v0.npy'))

oc_5m_win_u1 =np.nanmean(np.load(moor_path+'oc_5m_win_u1.npy'))
oc_5m_win_v1 =np.nanmean(np.load(moor_path+'oc_5m_win_v1.npy'))

oc_5m_sum_u1 =np.nanmean(np.load(moor_path+'oc_5m_sum_u1.npy'))
oc_5m_sum_v1 =np.nanmean(np.load(moor_path+'oc_5m_sum_v1.npy'))

oc_5m_win_u2 =np.nanmean(np.load(moor_path+'oc_5m_win_u2.npy'))
oc_5m_win_v2 =np.nanmean(np.load(moor_path+'oc_5m_win_v2.npy'))

oc_5m_sum_u2 =np.nanmean(np.load(moor_path+'oc_5m_sum_u2.npy'))
oc_5m_sum_v2 =np.nanmean(np.load(moor_path+'oc_5m_sum_v2.npy'))

oc_50m_sum_u = np.nanmean(np.load(moor_path+'oc_50m_sum_u.npy'))
oc_50m_sum_v = np.nanmean(np.load(moor_path+'oc_50m_sum_v.npy'))

oc_50m_win_u = np.nanmean(np.load(moor_path+'oc_50m_win_u.npy'))
oc_50m_win_v = np.nanmean(np.load(moor_path+'oc_50m_win_v.npy'))


#la
# lat/lon
la_lat = np.load(moor_path+'la_lat.npy')
la_lon = np.load(moor_path+'la_lon.npy')

#u/v
la_u_sum_05m = np.nanmean(np.load(moor_path+'la_u_sum_05m.npy'),axis=1)
la_v_sum_05m = np.nanmean(np.load(moor_path+'la_v_sum_05m.npy'),axis=1)

la_u_win_05m = np.nanmean(np.load(moor_path+'la_u_win_05m.npy'),axis=1)
la_v_win_05m = np.nanmean(np.load(moor_path+'la_v_win_05m.npy'),axis=1)

la_u_sum_50m = np.nanmean(np.load(moor_path+'la_u_sum_50m.npy'),axis=1)
la_v_sum_50m = np.nanmean(np.load(moor_path+'la_v_sum_50m.npy'),axis=1)

la_u_win_50m = np.nanmean(np.load(moor_path+'la_u_win_50m.npy'),axis=1)
la_v_win_50m = np.nanmean(np.load(moor_path+'la_v_win_50m.npy'),axis=1)


'''
print(oc_lat_7m)
print(oc_lon_7m)
print(oc_lat_50m)
print(oc_lon_50m)
print(oc_lat_5m_0)
print(oc_lon_5m_0)
print(oc_lat_5m_1)
print(oc_lon_5m_1)
print(oc_lat_5m_2)
print(oc_lon_5m_2)

ax.scatter(oc_lon_7m,oc_lat_7m)
ax.scatter(oc_lon_5m_0,oc_lat_5m_0)
ax.scatter(oc_lon_5m_1,oc_lat_5m_1)
ax.scatter(oc_lon_5m_2,oc_lat_5m_2)
ax.scatter(la_lon,la_lat)
'''

########
# plot
########
plt.ion()

coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')

# reshape lat/lon and u and v to be same shapes
#lat_plt = lat_nc[:-1,:-1]
#lon_plt = lon_nc[:-1,:-1]
lat_plt = lat_nc
lon_plt = lon_nc

#u_sum_05_plt = u_sum_05[:-1,:]
#v_sum_05_plt = v_sum_05[:,:-1]
#               
#u_win_05_plt = u_win_05[:-1,:]
#v_win_05_plt = v_win_05[:,:-1]
#               
#u_sum_50_plt = u_sum_50[:-1,:]
#v_sum_50_plt = v_sum_50[:,:-1]
#                   
#u_win_50_plt = u_win_50[:-1,:]
#v_win_50_plt = v_win_50[:,:-1]

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
freq = 30
in_st = 10

# bightwide
#lat_min = 32.4
#lat_max = 34.6
#lon_min = -120.5
#lon_max = -117
# la and oc
#lat_min = 33.35
#lat_max = 34.05
#lon_min = -118.9
#lon_max = -117.6
# la and oc zoomed
lat_min = 33.5
lat_max = 33.9
lon_min = -118.6
lon_max = -117.8
extent = [lon_min,lon_max,lat_min,lat_max]

fig_w = 18
fig_h = 12

xkey = .72
ykey = .81

fig,axes = plt.subplots(2,2,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

##################
# 5 m
##################
# summer
# plot roms
q_plt_5m_roms_sum = axes.flat[0].quiver(lon_plt[in_st::freq,in_st::freq],lat_plt[in_st::freq,in_st::freq],u_sum_05_plt[in_st::freq,in_st::freq],v_sum_05_plt[in_st::freq,in_st::freq],transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='k',linewidth=0.5)

# plot oc
q_plt_7m_sum = axes.flat[0].quiver(oc_lon_7m,oc_lat_7m,oc_7m_sum_u,oc_7m_sum_v,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

q_plt_oc_5m_0_sum = axes.flat[0].quiver(oc_lon_5m_0,oc_lat_5m_0,oc_5m_sum_u0,oc_5m_sum_v0,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)
q_plt_oc_5m_1_sum = axes.flat[0].quiver(oc_lon_5m_1,oc_lat_5m_1,oc_5m_sum_u1,oc_5m_sum_v1,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)
q_plt_oc_5m_2_sum = axes.flat[0].quiver(oc_lon_5m_2,oc_lat_5m_2,oc_5m_sum_u2,oc_5m_sum_v2,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

# plot la
q_plt_la_05m_sum = axes.flat[0].quiver(la_lon,la_lat,la_u_sum_05m,la_v_sum_05m,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)


# winter
# plot roms
q_plt_5m_roms_win = axes.flat[1].quiver(lon_plt[in_st::freq,in_st::freq],lat_plt[in_st::freq,in_st::freq],u_win_05_plt[in_st::freq,in_st::freq],v_win_05_plt[in_st::freq,in_st::freq],transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='k',linewidth=0.5)

# plot oc
q_plt_7m_win = axes.flat[1].quiver(oc_lon_7m,oc_lat_7m,oc_7m_win_u,oc_7m_win_v,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

q_plt_5m_0_win = axes.flat[1].quiver(oc_lon_5m_0,oc_lat_5m_0,oc_5m_win_u0,oc_5m_win_v0,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)
q_plt_5m_1_win = axes.flat[1].quiver(oc_lon_5m_1,oc_lat_5m_1,oc_5m_win_u1,oc_5m_win_v1,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)
q_plt_5m_2_win = axes.flat[1].quiver(oc_lon_5m_2,oc_lat_5m_2,oc_5m_win_u2,oc_5m_win_v2,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

# plot la
q_plt_la_05m_win = axes.flat[1].quiver(la_lon,la_lat,la_u_win_05m,la_v_win_05m,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)


#spd = np.sqrt(u_sum_05_plt[::freq,::freq]**2 + v_sum_05_plt[::freq,::freq]**2)

# quiver key
axes.flat[0].quiverkey(q_plt_5m_roms_sum,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[0].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[0].transAxes,fontsize=18)

axes.flat[1].quiverkey(q_plt_5m_roms_win,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[1].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[1].transAxes,fontsize=18)


##################
# 50 m
##################
# summer
# plot roms
q_plt_50m_roms_sum = axes.flat[2].quiver(lon_plt[in_st::freq,in_st::freq],lat_plt[in_st::freq,in_st::freq],u_sum_50_plt[in_st::freq,in_st::freq],v_sum_50_plt[in_st::freq,in_st::freq],transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='k',linewidth=0.5)

# plot oc
q_plt_oc_50m_sum = axes.flat[2].quiver(oc_lon_50m,oc_lat_50m,oc_50m_sum_u,oc_50m_sum_v,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

# plot la
q_plt_la_50m_sum = axes.flat[2].quiver(la_lon,la_lat,la_u_sum_50m,la_v_sum_50m,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)


# winter
# plot roms
q_plt_50m_roms_win = axes.flat[3].quiver(lon_plt[in_st::freq,in_st::freq],lat_plt[in_st::freq,in_st::freq],u_win_50_plt[in_st::freq,in_st::freq],v_win_50_plt[in_st::freq,in_st::freq],transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='k',linewidth=0.5)

# plot oc
q_plt_oc_50m_win = axes.flat[3].quiver(oc_lon_50m,oc_lat_50m,oc_50m_win_u,oc_50m_win_v,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

# plot la
q_plt_la_50m_win = axes.flat[3].quiver(la_lon,la_lat,la_u_win_50m,la_v_win_50m,transform=ccrs.PlateCarree(),scale=2,width=.001,headwidth=6,edgecolor='purple',linewidth=0.5)

#spd = np.sqrt(u_sum_05_plt[::freq,::freq]**2 + v_sum_05_plt[::freq,::freq]**2)

# quiver key
axes.flat[2].quiverkey(q_plt_50m_roms_sum,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[2].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[2].transAxes,fontsize=18)

axes.flat[3].quiverkey(q_plt_50m_roms_win,X=.8,Y=.8,U=.2,label=None,labelpos='N')
axes.flat[3].text(xkey,ykey,'0.2 m s$^{-1}$',transform=axes.flat[3].transAxes,fontsize=18)

axes.flat[0].set_title('summer 5 m',fontsize=18)
axes.flat[1].set_title('winter 5 m',fontsize=18)
axes.flat[2].set_title('summer 50 m',fontsize=18)
axes.flat[3].set_title('winter 50 m',fontsize=18)


step_lon = .2
step_lat = .1
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

fig.savefig(fig_path+'uv_map_zoom_1997_2000.png',bbox_inches='tight')
