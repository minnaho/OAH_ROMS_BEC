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
import cmocean as cmocean

fig_path = './figs/'

#######################
# ROMS-BEC outputs
#######################
# get 06-1999 - 06-2000 monthly average u/v
#out_path = '/data/project1/minnaho/validation/hydrodynamics/roms_slices/zslice_1997_2000_his/'
out_path = '/data/project1/minnaho/validation/hydrodynamics/roms_slices/zslice_40m_1997_2000/'
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'
grid_nc = Dataset(grid_path)
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
h_nc = np.array(grid_nc.variables['h'])
h_nc[h_nc<15] = np.nan
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

    u_arr_05[r_i,:] = 0.5*(u_nc[1:,:]+u_nc[:Ly_nc-1,:])
    v_arr_05[r_i,:] = 0.5*(v_nc[:,1:]+v_nc[:,:Lx_nc-1])

u_arr_05[u_arr_05>1E10] = np.nan
v_arr_05[v_arr_05>1E10] = np.nan

# pad endings to have same shape as lat_nc/lon_nc
u_arr_05_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
v_arr_05_rho = np.empty((len(rom_fi),Ly_nc,Lx_nc))
u_arr_05_rho.fill(np.nan)
v_arr_05_rho.fill(np.nan)

u_arr_05_rho[:,:-1,:-1] = u_arr_05[:,:,:]
v_arr_05_rho[:,:-1,:-1] = v_arr_05[:,:,:]

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


# avg u and v win and sum
u_sum_05 = np.nanmean(u_rot_05[sum_in,:,:],axis=0)
v_sum_05 = np.nanmean(v_rot_05[sum_in,:,:],axis=0)

u_win_05 = np.nanmean(u_rot_05[win_in,:,:],axis=0)
v_win_05 = np.nanmean(v_rot_05[win_in,:,:],axis=0)

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
               

u_sum_05_plt[u_sum_05_plt==0] = np.nan
v_sum_05_plt[v_sum_05_plt==0] = np.nan
            
u_win_05_plt[u_win_05_plt==0] = np.nan
v_win_05_plt[v_win_05_plt==0] = np.nan
            
# reduce nuber of arrows by plotting every xth arrow
freq_rom = 15
freq_hff = 5
# start index (changes which arrows are plotted)
in_rom = 10
in_hff = 10

# bightwide
#lat_min = 32.4
#lat_max = 34.6
#lon_min = -120.5
#lon_max = -117
# la and oc
lat_min = 33.5
lat_max = 34.1
lon_min = -119
lon_max = -117.5
# la and oc zoomed
#lat_min = 33.5
#lat_max = 33.9
#lon_min = -118.6
#lon_max = -117.8
plt_extent = [lon_min,lon_max,lat_min,lat_max]
lat_ind = np.where((lat_nc>lat_min)&(lat_nc<lat_max))
lon_ind = np.where((lon_nc>lon_min)&(lon_nc<lon_max))

fig_w = 14
fig_h = 10

axis_font = 16

# line widths
lw_hff = 2
lw_rom = 0.1

xkey_quiv = .72
ykey_quiv = .83

quivscale = 30
shaft_w = .002
hwidth = 10
hlength = 10

h_c = [100,500,750,1000,1500]


# plot contours and bathymetery
#c_map = cmocean.cm.deep
#v_min = 10
#v_max = 750
#axes.flat[0].pcolormesh(lon_nc,lat_nc,h_nc,cmap=c_map,vmin=v_min,vmax=v_max)
#bathy = axes.flat[1].pcolormesh(lon_nc,lat_nc,h_nc,cmap=c_map,vmin=v_min,vmax=v_max)

# plot quivers
qcolor = 'k'
fcolor = 'k'

# get angle of arrows
# add pi because they are going the opposite direction
theta_sum = np.arctan(v_sum_05_plt/u_sum_05_plt)+np.pi 
theta_win = np.arctan(v_win_05_plt/u_win_05_plt)+np.pi 

speed_sum = np.hypot(u_sum_05_plt,v_sum_05_plt)
speed_win = np.hypot(u_win_05_plt,v_win_05_plt)
#speed_sum = np.sqrt(u_sum_05_plt**2 + v_sum_05_plt**2)

v_min = 0
v_max = .2
qnorm = matplotlib.colors.Normalize(vmin=v_min,vmax=v_max,clip=False)

c_map = cmocean.cm.speed
#c_map = 'viridis'

fig,axes = plt.subplots(1,2,figsize=[fig_w,fig_h],subplot_kw=dict(projection=ccrs.PlateCarree()))

# summer
#q_plt_5m_roms_sum = axes.flat[0].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],u_sum_05_plt[in_rom::freq_rom,in_rom::freq_rom],v_sum_05_plt[in_rom::freq_rom,in_rom::freq_rom],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor=qcolor,facecolor=fcolor,linewidth=lw_rom)

# plot current direction only with arrow color as magnitude
q_plt_5m_roms_sum = axes.flat[0].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],np.cos(theta_sum)[in_rom::freq_rom,in_rom::freq_rom],np.sin(theta_sum)[in_rom::freq_rom,in_rom::freq_rom],speed_sum[in_rom::freq_rom,in_rom::freq_rom],cmap=c_map,norm=qnorm,scale=quivscale,transform=ccrs.PlateCarree(),width=shaft_w,headwidth=hwidth,headlength=hlength,linewidth=lw_rom,edgecolor=qcolor)
# without edgecolor
#q_plt_5m_roms_sum = axes.flat[0].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],np.cos(theta_sum)[in_rom::freq_rom,in_rom::freq_rom],np.sin(theta_sum)[in_rom::freq_rom,in_rom::freq_rom],speed_sum[in_rom::freq_rom,in_rom::freq_rom],cmap=c_map,norm=qnorm,scale=quivscale,transform=ccrs.PlateCarree(),width=shaft_w,headwidth=hwidth,headlength=hlength)

# winter
#q_plt_5m_roms_win = axes.flat[1].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],u_win_05_plt[in_rom::freq_rom,in_rom::freq_rom],v_win_05_plt[in_rom::freq_rom,in_rom::freq_rom],transform=ccrs.PlateCarree(),scale=quivscale,width=shaft_w,headwidth=hwidth,headlength=hlength,edgecolor=qcolor,facecolor=fcolor,linewidth=lw_rom)

# plot current direction only with arrow color as magnitude
q_plt_5m_roms_win = axes.flat[1].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],np.cos(theta_win)[in_rom::freq_rom,in_rom::freq_rom],np.sin(theta_win)[in_rom::freq_rom,in_rom::freq_rom],speed_win[in_rom::freq_rom,in_rom::freq_rom],cmap=c_map,norm=qnorm,scale=quivscale,transform=ccrs.PlateCarree(),width=shaft_w,headwidth=hwidth,headlength=hlength,linewidth=lw_rom,edgecolor=qcolor)
# without edgecolor
#q_plt_5m_roms_win = axes.flat[1].quiver(lon_plt[in_rom::freq_rom,in_rom::freq_rom],lat_plt[in_rom::freq_rom,in_rom::freq_rom],np.cos(theta_win)[in_rom::freq_rom,in_rom::freq_rom],np.sin(theta_win)[in_rom::freq_rom,in_rom::freq_rom],speed_win[in_rom::freq_rom,in_rom::freq_rom],cmap=c_map,norm=qnorm,scale=quivscale,transform=ccrs.PlateCarree(),width=shaft_w,headwidth=hwidth,headlength=hlength)


# quiver key
#axes.flat[0].quiverkey(q_plt_5m_roms_sum,X=.8,Y=.8,U=.2,label=None,labelpos='N')
#axes.flat[0].text(xkey_quiv,ykey_quiv,'0.2 m s$^{-1}$',transform=axes.flat[0].transAxes,fontsize=axis_font)
#
#axes.flat[1].quiverkey(q_plt_5m_roms_win,X=.8,Y=.8,U=.2,label=None,labelpos='N')
#axes.flat[1].text(xkey_quiv,ykey_quiv,'0.2 m s$^{-1}$',transform=axes.flat[1].transAxes,fontsize=axis_font)

axes.flat[0].set_title('summer 40 m',fontsize=axis_font+2)
axes.flat[1].set_title('winter 40 m',fontsize=axis_font+2)


step_lon = .4
step_lat = .1

gl = axes.flat[0].gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlabel_style = {'size':axis_font}
gl.ylabel_style = {'size':axis_font}
axes.flat[0].add_feature(coast_10m,facecolor='None',edgecolor='k')
gl.xlocator = mticker.FixedLocator(list(np.arange(lon_min,lon_max+step_lon,step_lon)))
gl.ylocator = mticker.FixedLocator(list(np.arange(lat_min,lat_max+step_lat,step_lat)))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
axes.flat[0].set_extent(plt_extent)

gl = axes.flat[1].gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.ylabels_left = False
gl.xlabel_style = {'size':axis_font}
gl.ylabel_style = {'size':axis_font}
axes.flat[1].add_feature(coast_10m,facecolor='None',edgecolor='k')
gl.xlocator = mticker.FixedLocator(list(np.arange(lon_min,lon_max+step_lon,step_lon)))
gl.ylocator = mticker.FixedLocator(list(np.arange(lat_min,lat_max+step_lat,step_lat)))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
axes.flat[1].set_extent(plt_extent)


h_plt0 = axes.flat[0].contour(lon_nc,lat_nc,h_nc,h_c,colors='k',extent=plt_extent,alpha=0.7,linewidths=1)
h_plt1 = axes.flat[1].contour(lon_nc,lat_nc,h_nc,h_c,colors='k',extent=plt_extent,alpha=0.7,linewidths=1)

axes.flat[0].clabel(h_plt0,h_c,fontsize=9,inline=True,fmt='%d',manual=True)
#axes.flat[1].clabel(h_plt1,h_c,fontsize=9,inline=True,fmt='%d',manual=True)

# plot bathymetry contours
#h_plt0 = axes.flat[0].contour(lon_nc,lat_nc,h_nc,h_c,colors='navy',extent=plt_extent)
#axes.flat[0].clabel(h_plt0,h_c,fontsize=9,inline=True,fmt='%d')
#
#h_plt1 = axes.flat[1].contour(lon_nc,lat_nc,h_nc,h_c,colors='navy',extent=plt_extent)
#axes.flat[1].clabel(h_plt1,h_c,fontsize=9,inline=True,fmt='%d')

# colorbar
p0 = axes.flat[1].get_position().get_points().flatten()
cb_ax = fig.add_axes([p0[2]+0.01,p0[1],0.01,p0[3]-p0[1]])
cb_im = fig.colorbar(q_plt_5m_roms_win,cax=cb_ax,orientation='vertical')
cb_im.set_label('Speed (m s$^{-1}$)',fontsize=axis_font)
cb_im.ax.tick_params(axis='both',which='major',direction='in',labelsize=axis_font)
cb_im.ax.tick_params(axis='both',which='minor',direction='in',labelsize=axis_font)
#cb_im.ax.locator_params(nbins=6)
#cb_tick = mticker.MaxNLocator(nbins=8)
#cb_im.locator = cb_tick
#cb_im.update_ticks()


xkey = 0
ykey = 1.02
axes.flat[0].text(xkey,ykey,'a)',transform=axes.flat[0].transAxes,fontsize=axis_font)
axes.flat[1].text(xkey,ykey,'b)',transform=axes.flat[1].transAxes,fontsize=axis_font)


#fig.savefig(fig_path+'roms_40m_map_season.png',bbox_inches='tight')
