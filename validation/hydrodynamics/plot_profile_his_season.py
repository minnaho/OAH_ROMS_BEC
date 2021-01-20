###########################
# map of surface currents
# vs model
###########################
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import pandas as pd
import ROMS_depths as rdepth
import matplotlib.pyplot as plt

fig_path = './figs/'

# moorings
oc_lat = np.load('./moor_npy/oc_prof_lat.npy')
oc_lon = np.load('./moor_npy/oc_prof_lon.npy')

oc_prof_u = np.load('./moor_npy/oc_prof_u.npy')
oc_prof_v = np.load('./moor_npy/oc_prof_v.npy')

oc_win_u = np.load('./moor_npy/oc_prof_win_u.npy')
oc_sum_u = np.load('./moor_npy/oc_prof_sum_u.npy')

oc_win_v = np.load('./moor_npy/oc_prof_win_v.npy')
oc_sum_v = np.load('./moor_npy/oc_prof_sum_v.npy')

oc_dep = np.load('./moor_npy/oc_prof_dep_7_55.npy')

la_lat = np.load('./moor_npy/la_lat.npy')
la_lon = np.load('./moor_npy/la_lon.npy')

#######################
# ROMS-BEC outputs
#######################
# get 06-1999 - 06-2000 monthly average u/v
#out_path = '/data/project6/kesf/ROMS/L2SCB_AP/monthly/l2_scb_avg.'
out_path = '/data/project6/kesf/ROMS/L2SCB_AP/AVG_' 
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'
grid_nc = Dataset(grid_path)
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
h_nc = np.array(grid_nc.variables['h'])
angle_nc = np.array(grid_nc.variables['angle'])
[Ly_all,Lx_all] = grid_nc.variables['pm'].shape

# oc find i,j values 
lat_you_want = oc_lat
lon_you_want = oc_lon
# find difference and square, then absolute value to find closest lat/lon in lat_nc and lon_nc
temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
oc_coord_i = int(xi_coord)
oc_coord_j = int(eta_coord)

# la find i,j values 
la_coord_i = np.arange((la_lat.shape[0]))
la_coord_j = np.arange((la_lat.shape[0]))
for l_i in range(len(la_lat)):
    lat_you_want = la_lat[l_i]
    lon_you_want = la_lon[l_i]
    # find difference and square, then absolute value to find closest lat/lon in lat_nc and lon_nc
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    la_coord_i[l_i] = int(xi_coord)
    la_coord_j[l_i] = int(eta_coord)


st_yr = 1999
en_yr = 2000

st_mo = 6
en_mo = 6

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

roms_files = glob.glob('./roms_slices/zslice_5_50m/*.nc')

# oc mooring has 1 with dpeth
roms_u_win_oc = np.empty((3,60))
roms_v_win_oc = np.empty((3,60))

roms_u_sum_oc = np.empty((4,60))
roms_v_sum_oc = np.empty((4,60))

roms_u_win_oc.fill(np.nan)
roms_v_win_oc.fill(np.nan)
             
roms_u_sum_oc.fill(np.nan)
roms_v_sum_oc.fill(np.nan)

z_r_win_oc = np.empty((3,60))
z_r_sum_oc = np.empty((4,60))

z_r_win_oc.fill(np.nan)
z_r_sum_oc.fill(np.nan)

# la moorings has 9 stations
roms_u_win_la = np.empty((3,9,60))
roms_v_win_la = np.empty((3,9,60))

roms_u_sum_la = np.empty((4,9,60))
roms_v_sum_la = np.empty((4,9,60))

roms_u_win_la.fill(np.nan)
roms_v_win_la.fill(np.nan)
             
roms_u_sum_la.fill(np.nan)
roms_v_sum_la.fill(np.nan)

z_r_win_la = np.empty((3,9,60))
z_r_sum_la = np.empty((4,9,60))

z_r_win_la.fill(np.nan)
z_r_sum_la.fill(np.nan)

# summer/winter
# get vertical profile at each mooring
w_i = 0
s_i = 0
for y_i in range(st_yr,en_yr+1):
    print('year: ',y_i)
    if y_i == st_yr:
        s_m = st_mo
    else:
        s_m = 1
    if y_i == en_yr:
        e_m = en_mo+1
    else:
        e_m = 13
    for m_i in range(s_m,e_m):
        if (m_i == 6 or m_i == 7 or m_i == 8):
            print('month: ',m_i)
            fi_dt = 'Y'+str(y_i)+'M'+'%02d'%m_i
            fi_name = glob.glob(out_path+fi_dt+'/'+'l2_scb_his.*.nc')
            #out_nc = Dataset(out_path+fi_dt+'.nc','r')
            out_nc = Dataset(fi_name[0],'r')
            u_nc = np.array(out_nc.variables['u'])
            v_nc = np.array(out_nc.variables['v'])
            u_nc[u_nc>1E10] = np.nan
            v_nc[v_nc>1E10] = np.nan
            u_rho = 0.5*(np.squeeze(u_nc[0,:,oc_coord_j,oc_coord_i])+np.squeeze(u_nc[0,:,oc_coord_j,oc_coord_i+1]))
            v_rho = 0.5*(np.squeeze(v_nc[0,:,oc_coord_j,oc_coord_i])+np.squeeze(v_nc[0,:,oc_coord_j+1,oc_coord_i]))

            u_rot = (u_rho*np.cos(angle_nc[oc_coord_j,oc_coord_i]))-(v_rho*np.sin(angle_nc[oc_coord_j,oc_coord_i]))
            v_rot = (v_rho*np.cos(angle_nc[oc_coord_j,oc_coord_i]))+(u_rho*np.sin(angle_nc[oc_coord_j,oc_coord_i]))

            roms_u_sum_oc[s_i,:] = u_rot
            roms_v_sum_oc[s_i,:] = v_rot
            #roms_u_sum_oc[s_i,:] = np.squeeze(out_file.variables['u'][0,:,oc_coord_j,oc_coord_i])
            #roms_v_sum_oc[s_i,:] = np.squeeze(out_file.variables['v'][0,:,oc_coord_j,oc_coord_i])
            z_r_sum_oc[s_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,oc_coord_j,oc_coord_i])
            #for l_i in range(len(la_coord_i)):
            #    u_rho = 0.5*(np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]+1]))
            #    v_rho = 0.5*(np.squeeze(v_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(v_nc[0,:,la_coord_j[l_i]+1,la_coord_i[l_i]]))

            #    u_rot = (u_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))-(v_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))
            #    v_rot = (v_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))+(u_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))

            #    roms_u_sum_la[s_i,:] = u_rot
            #    roms_v_sum_la[s_i,:] = v_rot

            #    #roms_u_sum_la[s_i,l_i,:] = np.squeeze(out_file.variables['u'][0,:,la_coord_j[l_i],la_coord_i[l_i]])
            #    #roms_v_sum_la[s_i,l_i,:] = np.squeeze(out_file.variables['v'][0,:,la_coord_j[l_i],la_coord_i[l_i]])
            #    z_r_sum_la[s_i,l_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,la_coord_j[l_i],la_coord_i[l_i]])
            s_i += 1
        if (m_i == 12 or m_i == 1 or m_i == 2):
            print('month: ',m_i)
            fi_dt = 'Y'+str(y_i)+'M'+'%02d'%m_i
            fi_name = glob.glob(out_path+fi_dt+'/'+'l2_scb_his.*.nc')
            #out_nc = Dataset(out_path+fi_dt+'.nc','r')
            out_nc = Dataset(fi_name[0],'r')
            u_nc = np.array(out_nc.variables['u'])
            v_nc = np.array(out_nc.variables['v'])
            u_nc[u_nc>1E10] = np.nan
            v_nc[v_nc>1E10] = np.nan

            u_rho = 0.5*(np.squeeze(u_nc[0,:,oc_coord_j,oc_coord_i])+np.squeeze(u_nc[0,:,oc_coord_j,oc_coord_i+1]))
            v_rho = 0.5*(np.squeeze(v_nc[0,:,oc_coord_j,oc_coord_i])+np.squeeze(v_nc[0,:,oc_coord_j+1,oc_coord_i]))

            u_rot = (u_rho*np.cos(angle_nc[oc_coord_j,oc_coord_i]))-(v_rho*np.sin(angle_nc[oc_coord_j,oc_coord_i]))
            v_rot = (v_rho*np.cos(angle_nc[oc_coord_j,oc_coord_i]))+(u_rho*np.sin(angle_nc[oc_coord_j,oc_coord_i]))

            roms_u_win_oc[w_i,:] = u_rot
            roms_v_win_oc[w_i,:] = v_rot
            #roms_u_win_oc[w_i,:] = np.squeeze(out_file.variables['u'][0,:,oc_coord_j,oc_coord_i])
            #roms_v_win_oc[w_i,:] = np.squeeze(out_file.variables['v'][0,:,oc_coord_j,oc_coord_i])
            z_r_win_oc[w_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,oc_coord_j,oc_coord_i])
            #for l_i in range(len(la_coord_i)):
            #    u_rho = 0.5*(np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]+1]))
            #    v_rho = 0.5*(np.squeeze(v_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(v_nc[0,:,la_coord_j[l_i]+1,la_coord_i[l_i]]))

            #    u_rot = (u_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))-(v_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))
            #    v_rot = (v_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))+(u_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))

            #    roms_u_win_la[w_i,:] = u_rot
            #    roms_v_win_la[w_i,:] = v_rot
            #    #roms_u_win_la[w_i,l_i,:] = np.squeeze(out_file.variables['u'][0,:,la_coord_j[l_i],la_coord_i[l_i]])
            #    #roms_v_win_la[w_i,l_i,:] = np.squeeze(out_file.variables['v'][0,:,la_coord_j[l_i],la_coord_i[l_i]])
            #    z_r_win_la[w_i,l_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,la_coord_j[l_i],la_coord_i[l_i]])
            w_i += 1

    
# plot oc
oc_avg_u_sum = np.nanmean(oc_sum_u,axis=0)
oc_avg_v_sum = np.nanmean(oc_sum_v,axis=0)

#oc_std_u_sum = np.nanstd(oc_sum_u,axis=0)
#oc_std_v_sum = np.nanstd(oc_sum_v,axis=0)
oc_std_u_sum_low = np.nanpercentile(oc_sum_u,5,axis=0)
oc_std_v_sum_low = np.nanpercentile(oc_sum_v,5,axis=0)
oc_std_u_sum_high = np.nanpercentile(oc_sum_u,95,axis=0)
oc_std_v_sum_high = np.nanpercentile(oc_sum_v,95,axis=0)

oc_avg_u_win = np.nanmean(oc_win_u,axis=0)
oc_avg_v_win = np.nanmean(oc_win_v,axis=0)

#oc_std_u_win = np.nanstd(oc_win_u,axis=0)
#oc_std_v_win = np.nanstd(oc_win_v,axis=0)
oc_std_u_win_low = np.nanpercentile(oc_win_u,5,axis=0)
oc_std_v_win_low = np.nanpercentile(oc_win_v,5,axis=0)
oc_std_u_win_high = np.nanpercentile(oc_win_u,95,axis=0)
oc_std_v_win_high = np.nanpercentile(oc_win_v,95,axis=0)

oc_dep_plt = oc_dep*-1

roms_avg_u_sum_oc = np.nanmean(roms_u_sum_oc,axis=0)
roms_avg_v_sum_oc = np.nanmean(roms_v_sum_oc,axis=0)

#roms_std_u_sum_oc = np.nanstd(roms_u_sum_oc,axis=0)
#roms_std_v_sum_oc = np.nanstd(roms_v_sum_oc,axis=0)
roms_std_u_sum_oc_low = np.nanpercentile(roms_u_sum_oc,5,axis=0)
roms_std_v_sum_oc_low = np.nanpercentile(roms_v_sum_oc,5,axis=0)
roms_std_u_sum_oc_high = np.nanpercentile(roms_u_sum_oc,95,axis=0)
roms_std_v_sum_oc_high = np.nanpercentile(roms_v_sum_oc,95,axis=0)

roms_avg_u_win_oc = np.nanmean(roms_u_win_oc,axis=0)
roms_avg_v_win_oc = np.nanmean(roms_v_win_oc,axis=0)

#roms_std_u_win_oc = np.nanstd(roms_u_win_oc,axis=0)
#roms_std_v_win_oc = np.nanstd(roms_v_win_oc,axis=0)
roms_std_u_win_oc_low = np.nanpercentile(roms_u_win_oc,5,axis=0)
roms_std_v_win_oc_low = np.nanpercentile(roms_v_win_oc,5,axis=0)
roms_std_u_win_oc_high = np.nanpercentile(roms_u_win_oc,95,axis=0)
roms_std_v_win_oc_high = np.nanpercentile(roms_v_win_oc,95,axis=0)

roms_dep_sum_oc = np.nanmean(z_r_sum_oc,axis=0)
roms_dep_win_oc = np.nanmean(z_r_win_oc,axis=0)

roms_c = 'k'
moor_c = 'r'
avg_l = '-'
std_l = '--'

figw = 12
figh = 12


# season
# oc cut out below 55 m
in_sum_dep = np.where((roms_dep_sum_oc>-55)&(roms_dep_sum_oc<-6))[0]
in_win_dep = np.where((roms_dep_win_oc>-55)&(roms_dep_win_oc<-6))[0]
roms_dep_sum_oc = roms_dep_sum_oc[in_sum_dep]
roms_dep_win_oc = roms_dep_win_oc[in_win_dep]

roms_avg_u_sum_oc = roms_avg_u_sum_oc[in_sum_dep]
roms_std_u_sum_oc_low  = roms_std_u_sum_oc_low[in_sum_dep]
roms_std_u_sum_oc_high = roms_std_u_sum_oc_high[in_sum_dep]

roms_avg_v_sum_oc = roms_avg_v_sum_oc[in_sum_dep]
roms_std_v_sum_oc_low  = roms_std_v_sum_oc_low[in_sum_dep]
roms_std_v_sum_oc_high = roms_std_v_sum_oc_high[in_sum_dep]

roms_avg_u_win_oc = roms_avg_u_win_oc[in_win_dep]
roms_std_u_win_oc_low  = roms_std_u_win_oc_low[in_win_dep]
roms_std_u_win_oc_high = roms_std_u_win_oc_high[in_win_dep]

roms_avg_v_win_oc = roms_avg_v_win_oc[in_win_dep]
roms_std_v_win_oc_low  = roms_std_v_win_oc_low[in_win_dep]
roms_std_v_win_oc_high = roms_std_v_win_oc_high[in_win_dep]

# plot oc u
fig1,axes = plt.subplots(2,2,figsize=[figw,figh])
axes.flat[0].plot(roms_avg_u_sum_oc,roms_dep_sum_oc,color=roms_c)
#axes.flat[0].plot(roms_avg_u_sum_oc-roms_std_u_sum_oc,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
#axes.flat[0].plot(roms_avg_u_sum_oc+roms_std_u_sum_oc,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[0].plot(roms_std_u_sum_oc_low,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[0].plot(roms_std_u_sum_oc_high,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[0].plot(oc_avg_u_sum,oc_dep_plt,color=moor_c)
#axes.flat[0].plot(oc_avg_u_sum-oc_std_u_sum,oc_dep_plt,color=moor_c,linestyle=std_l)
#axes.flat[0].plot(oc_avg_u_sum+oc_std_u_sum,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[0].plot(oc_std_u_sum_low,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[0].plot(oc_std_u_sum_high,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[0].set_xlabel('summer u')
axes.flat[0].set_ylabel('depth')

axes.flat[1].plot(roms_avg_v_sum_oc,roms_dep_sum_oc,color=roms_c)
#axes.flat[1].plot(roms_avg_v_sum_oc-roms_std_v_sum_oc,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
#axes.flat[1].plot(roms_avg_v_sum_oc+roms_std_v_sum_oc,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[1].plot(roms_std_v_sum_oc_low,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[1].plot(roms_std_v_sum_oc_high,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes.flat[1].plot(oc_avg_v_sum,oc_dep_plt,color=moor_c)
#axes.flat[1].plot(oc_avg_v_sum-oc_std_v_sum,oc_dep_plt,color=moor_c,linestyle=std_l)
#axes.flat[1].plot(oc_avg_v_sum+oc_std_v_sum,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[1].plot(oc_std_v_sum_low,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[1].plot(oc_std_v_sum_high,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[1].set_xlabel('summer v')
axes.flat[1].set_ylabel('depth')

axes.flat[2].plot(roms_avg_u_win_oc,roms_dep_win_oc,color=roms_c)
#axes.flat[2].plot(roms_avg_u_win_oc-roms_std_u_win_oc,roms_dep_win_oc,color=roms_c,linestyle=std_l)
#axes.flat[2].plot(roms_avg_u_win_oc+roms_std_u_win_oc,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[2].plot(roms_std_u_win_oc_low,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[2].plot(roms_std_u_win_oc_high,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[2].plot(oc_avg_u_win,oc_dep_plt,color=moor_c)
#axes.flat[2].plot(oc_avg_u_win-oc_std_u_win,oc_dep_plt,color=moor_c,linestyle=std_l)
#axes.flat[2].plot(oc_avg_u_win+oc_std_u_win,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[2].plot(oc_std_u_win_low,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[2].plot(oc_std_u_win_high,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[2].set_xlabel('winter u')
axes.flat[2].set_ylabel('depth')

axes.flat[3].plot(roms_avg_v_win_oc,roms_dep_win_oc,color=roms_c)
#axes.flat[3].plot(roms_avg_v_win_oc-roms_std_v_win_oc,roms_dep_win_oc,color=roms_c,linestyle=std_l)
#axes.flat[3].plot(roms_avg_v_win_oc+roms_std_v_win_oc,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[3].plot(roms_std_v_win_oc_low,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[3].plot(roms_std_v_win_oc_high,roms_dep_win_oc,color=roms_c,linestyle=std_l)
axes.flat[3].plot(oc_avg_v_win,oc_dep_plt,color=moor_c)
#axes.flat[3].plot(oc_avg_v_win-oc_std_v_win,oc_dep_plt,color=moor_c,linestyle=std_l)
#axes.flat[3].plot(oc_avg_v_win+oc_std_v_win,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[3].plot(oc_std_v_win_low,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[3].plot(oc_std_v_win_high,oc_dep_plt,color=moor_c,linestyle=std_l)
axes.flat[3].set_xlabel('winter v')
axes.flat[3].set_ylabel('depth')

fig1.savefig(fig_path+'oc_vertical_season_his.png',bbox_inches='tight')
