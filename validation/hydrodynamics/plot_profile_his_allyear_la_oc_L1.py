###########################
# map of surface currents
# vs model
###########################
import sys
sys.path.append('/data/project3/minnaho/global/')
import l1grid
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import pandas as pd
import ROMS_depths as rdepth
import matplotlib.pyplot as plt
import pickle as pickle

fig_path = './figs/'

# moorings
# oc
oc_lat = np.load('./moor_npy/oc_prof_lat.npy')
oc_lon = np.load('./moor_npy/oc_prof_lon.npy')

oc_prof_u = np.load('./moor_npy/oc_prof_u.npy')
oc_prof_v = np.load('./moor_npy/oc_prof_v.npy')

oc_win_u = np.load('./moor_npy/oc_prof_win_u.npy')
oc_sum_u = np.load('./moor_npy/oc_prof_sum_u.npy')

oc_win_v = np.load('./moor_npy/oc_prof_win_v.npy')
oc_sum_v = np.load('./moor_npy/oc_prof_sum_v.npy')

oc_dep = np.load('./moor_npy/oc_prof_dep_7_55.npy')

# la
la_lat = np.load('./moor_npy/la_lat.npy')
la_lon = np.load('./moor_npy/la_lon.npy')

la_tim = pickle.load(open('./moor_npy/la_moor_time.pkl','rb'))

la_prof_u = pickle.load(open('./moor_npy/la_u_prof.pkl','rb'))
la_prof_v = pickle.load(open('./moor_npy/la_v_prof.pkl','rb'))

la_dep = pickle.load(open('./moor_npy/la_dep_prof.pkl','rb'))



#######################
# ROMS-BEC outputs
#######################
# get 06-1999 - 06-2000 monthly average u/v
#out_path = '/data/project6/kesf/ROMS/L2SCB_AP/monthly/l2_scb_avg.'
out_path = '/data/project6/ROMS/USSW1/AVG_'
grid_nc = l1grid.grid_nc
lat_nc = l1grid.lat_nc
lon_nc = l1grid.lon_nc
h_nc = l1grid.h_nc
angle_nc = l1grid.angle_nc
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
    # find difference and square, then absolute value 
    # to find closest lat/lon in lat_nc and lon_nc
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

# la moorings has 9 stations with 20 depths each
# make nan values into array of nans so all same size
for u_i in range(len(la_prof_u)):
    try:
        a = len(la_prof_u[u_i])
        b = len(la_prof_v[u_i])
    except:
        la_prof_u[u_i] = np.empty((la_prof_u[0].shape[0]))
        la_prof_u[u_i].fill(np.nan)
        la_prof_v[u_i] = np.empty((la_prof_v[0].shape[0]))
        la_prof_v[u_i].fill(np.nan)

# this index is missing 1, so make same size with nan
la_prof_u[93] = np.empty((la_prof_u[0].shape[0]))
la_prof_u[93].fill(np.nan)

la_prof_v[93] = np.empty((la_prof_v[0].shape[0]))
la_prof_v[93].fill(np.nan)

# check 
for u_i in range(len(la_prof_u)):
    #print(str(len(la_prof_u[u_i])))
    if len(la_prof_u[u_i]) != len(la_prof_u[0]):
        print(u_i,'does not equal')

for v_i in range(len(la_prof_v)):
    #print(str(len(la_prof_v[v_i])))
    if len(la_prof_v[v_i]) != len(la_prof_v[0]):
        print(v_i,'does not eqval')

#convert to (num sensors, depths, time) array
la_u = np.array(la_prof_u).reshape(9,20,len(la_prof_u[0]))
la_v = np.array(la_prof_v).reshape(9,20,len(la_prof_v[0]))


'''
# oc mooring has 1 with depth
roms_u_sum_oc = np.empty((13,60)) # num of months
roms_v_sum_oc = np.empty((13,60)) # 1999/06 - 2000-/06

roms_u_sum_oc.fill(np.nan)
roms_v_sum_oc.fill(np.nan)

z_r_sum_oc = np.empty((13,60))

z_r_sum_oc.fill(np.nan)

# roms la
roms_u_sum_la = np.empty((13,9,60))
roms_v_sum_la = np.empty((13,9,60))
             
roms_u_sum_la.fill(np.nan)
roms_v_sum_la.fill(np.nan)

z_r_sum_la = np.empty((13,9,60))

z_r_sum_la.fill(np.nan)

# get ROMS vertical profile at each mooring
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
        print('month: ',m_i)
        fi_dt = 'Y'+str(y_i)+'M'+'%02d'%m_i
        fi_name = glob.glob(out_path+fi_dt+'/'+'ussw1_his.*.nc')
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
        z_r_sum_oc[s_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,oc_coord_j,oc_coord_i])
        for l_i in range(len(la_coord_i)):
            u_rho = 0.5*(np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(u_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]+1]))
            v_rho = 0.5*(np.squeeze(v_nc[0,:,la_coord_j[l_i],la_coord_i[l_i]])+np.squeeze(v_nc[0,:,la_coord_j[l_i]+1,la_coord_i[l_i]]))

            u_rot = (u_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))-(v_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))
            v_rot = (v_rho*np.cos(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))+(u_rho*np.sin(angle_nc[la_coord_j[l_i],la_coord_i[l_i]]))

            roms_u_sum_la[s_i,l_i,:] = u_rot
            roms_v_sum_la[s_i,l_i,:] = v_rot

            z_r_sum_la[s_i,l_i,:] = np.squeeze(rdepth.get_zr_zw_tind(out_nc,grid_nc,0,[0,Ly_all,0,Lx_all])[0][:,la_coord_j[l_i],la_coord_i[l_i]])
        s_i += 1

# save roms u/v/z arrays
np.save('./moor_npy/roms_u_oc_L1.npy',roms_u_sum_oc)
np.save('./moor_npy/roms_v_oc_L1.npy',roms_v_sum_oc)
np.save('./moor_npy/z_r_oc_L1.npy',z_r_sum_oc)

np.save('./moor_npy/roms_u_la_L1.npy',roms_u_sum_la)
np.save('./moor_npy/roms_v_la_L1.npy',roms_v_sum_la)
np.save('./moor_npy/z_r_la_L1.npy',z_r_sum_la)
'''

# load roms u/v/z arrays

roms_u_sum_oc = np.load('./moor_npy/roms_u_oc_L1.npy')
roms_v_sum_oc = np.load('./moor_npy/roms_v_oc_L1.npy')
z_r_sum_oc    = np.load('./moor_npy/z_r_oc_L1.npy')   
                
roms_u_sum_la = np.load('./moor_npy/roms_u_la_L1.npy')
roms_v_sum_la = np.load('./moor_npy/roms_v_la_L1.npy')
z_r_sum_la    = np.load('./moor_npy/z_r_la_L1.npy')   

    
# plot oc
oc_avg_u_sum = np.nanmean(oc_prof_u,axis=0)
oc_avg_v_sum = np.nanmean(oc_prof_v,axis=0)

#oc_std_u_sum = np.nanstd(oc_prof_u,axis=0)
#oc_std_v_sum = np.nanstd(oc_prof_v,axis=0)
oc_std_u_sum_low = np.nanpercentile(oc_prof_u,5,axis=0)
oc_std_v_sum_low = np.nanpercentile(oc_prof_v,5,axis=0)
oc_std_u_sum_high = np.nanpercentile(oc_prof_u,95,axis=0)
oc_std_v_sum_high = np.nanpercentile(oc_prof_v,95,axis=0)

oc_dep_plt = oc_dep*-1

# plot la
# average across time
la_u_avg = np.nanmean(la_u,axis=2)
la_v_avg = np.nanmean(la_v,axis=2)

la_u_std_low = np.nanpercentile(la_u,5,axis=2)
la_v_std_low = np.nanpercentile(la_v,5,axis=2)

la_u_std_high = np.nanpercentile(la_u,95,axis=2)
la_v_std_high = np.nanpercentile(la_v,95,axis=2)

la_dep_plt = np.array(la_dep[:la_u_avg.shape[1]])*-1

# plot roms
# oc
roms_avg_u_sum_oc = np.nanmean(roms_u_sum_oc,axis=0)
roms_avg_v_sum_oc = np.nanmean(roms_v_sum_oc,axis=0)

#roms_std_u_sum_oc = np.nanstd(roms_u_sum_oc,axis=0)
#roms_std_v_sum_oc = np.nanstd(roms_v_sum_oc,axis=0)
roms_std_u_sum_oc_low = np.nanpercentile(roms_u_sum_oc,5,axis=0)
roms_std_v_sum_oc_low = np.nanpercentile(roms_v_sum_oc,5,axis=0)
roms_std_u_sum_oc_high = np.nanpercentile(roms_u_sum_oc,95,axis=0)
roms_std_v_sum_oc_high = np.nanpercentile(roms_v_sum_oc,95,axis=0)

roms_dep_sum_oc = np.nanmean(z_r_sum_oc,axis=0)

# la
roms_avg_u_sum_la = np.nanmean(roms_u_sum_la,axis=0)
roms_avg_v_sum_la = np.nanmean(roms_v_sum_la,axis=0)

#roms_std_u_sum_la = np.nanstd(roms_u_sum_la,axis=0)
#roms_std_v_sum_la = np.nanstd(roms_v_sum_la,axis=0)
roms_std_u_sum_la_low = np.nanpercentile(roms_u_sum_la,5,axis=0)
roms_std_v_sum_la_low = np.nanpercentile(roms_v_sum_la,5,axis=0)
roms_std_u_sum_la_high = np.nanpercentile(roms_u_sum_la,95,axis=0)
roms_std_v_sum_la_high = np.nanpercentile(roms_v_sum_la,95,axis=0)

roms_dep_sum_la = np.nanmean(z_r_sum_la,axis=0)

roms_c = 'k'
moor_c = 'r'
avg_l = '-'
std_l = '--'

moor_lw = 3
#roms_lw = 2

figw = 16
figh = 6

axis_font = 16

# all year
# oc cut out below 55 m
in_sum_dep = np.where((roms_dep_sum_oc>-55)&(roms_dep_sum_oc<-6))[0]
roms_dep_sum_oc = roms_dep_sum_oc[in_sum_dep]

roms_avg_u_sum_oc = roms_avg_u_sum_oc[in_sum_dep]
#roms_std_u_sum_oc = roms_std_u_sum_oc[in_sum_dep]

roms_std_u_sum_oc_low = roms_std_u_sum_oc_low[in_sum_dep]
roms_std_u_sum_oc_high = roms_std_u_sum_oc_high[in_sum_dep]

roms_avg_v_sum_oc = roms_avg_v_sum_oc[in_sum_dep]
#roms_std_v_sum_oc = roms_std_v_sum_oc[in_sum_dep]

roms_std_v_sum_oc_low = roms_std_v_sum_oc_low[in_sum_dep]
roms_std_v_sum_oc_high = roms_std_v_sum_oc_high[in_sum_dep]

# la choose one mooring
la_ch = 5

roms_dep_sum_la = np.nanmean(z_r_sum_la,axis=0)
in_la_dep = np.where((roms_dep_sum_la[la_ch]>la_dep_plt[-1])&(roms_dep_sum_la[la_ch]<la_dep_plt[0]))

roms_dep_sum_la_plt = np.squeeze(roms_dep_sum_la[la_ch,in_la_dep])

roms_avg_u_sum_la_plt = roms_avg_u_sum_la[la_ch][in_la_dep]
roms_avg_v_sum_la_plt = roms_avg_v_sum_la[la_ch][in_la_dep]

roms_std_u_sum_la_low_plt  = roms_std_u_sum_la_low[la_ch][in_la_dep]  
roms_std_v_sum_la_low_plt  = roms_std_v_sum_la_low[la_ch][in_la_dep]  
                         
roms_std_u_sum_la_high_plt = roms_std_u_sum_la_high[la_ch][in_la_dep] 
roms_std_v_sum_la_high_plt = roms_std_v_sum_la_high[la_ch][in_la_dep] 

# plot oc u
#plt.ion()

# plot one la profile
fig0,axes0 = plt.subplots(1,4,figsize=[figw,figh])

axes0.flat[0].plot(roms_avg_u_sum_la_plt,roms_dep_sum_la_plt,color=roms_c,label='ROMS')
axes0.flat[0].plot(roms_std_u_sum_la_low_plt,roms_dep_sum_la_plt,color=roms_c,linestyle=std_l)
axes0.flat[0].plot(roms_std_u_sum_la_high_plt,roms_dep_sum_la_plt,color=roms_c,linestyle=std_l)
axes0.flat[0].plot(la_u_avg[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,label='ADCP')
axes0.flat[0].plot(la_u_std_low[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
axes0.flat[0].plot(la_u_std_high[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
    
axes0.flat[1].plot(roms_avg_v_sum_la_plt,roms_dep_sum_la_plt,color=roms_c)
axes0.flat[1].plot(roms_std_v_sum_la_low_plt,roms_dep_sum_la_plt,color=roms_c,linestyle=std_l)
axes0.flat[1].plot(roms_std_v_sum_la_high_plt,roms_dep_sum_la_plt,color=roms_c,linestyle=std_l)
axes0.flat[1].plot(la_v_avg[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,label='ADCP')
axes0.flat[1].plot(la_v_std_low[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
axes0.flat[1].plot(la_v_std_high[la_ch],la_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
    
axes0.flat[0].set_xlabel('u (m s$^{-1})$',fontsize=axis_font)
axes0.flat[0].set_ylabel('Depth (m)',fontsize=axis_font)
axes0.flat[1].set_xlabel('v (m s$^{-1})$',fontsize=axis_font)

axes0.flat[2].plot(roms_avg_u_sum_oc,roms_dep_sum_oc,color=roms_c,label='ROMS')
axes0.flat[2].plot(roms_std_u_sum_oc_low,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes0.flat[2].plot(roms_std_u_sum_oc_high,roms_dep_sum_oc,color=roms_c,linestyle=std_l)

axes0.flat[2].plot(oc_avg_u_sum,oc_dep_plt,color=moor_c,linewidth=moor_lw,label='ADCP')
axes0.flat[2].plot(oc_std_u_sum_low,oc_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
axes0.flat[2].plot(oc_std_u_sum_high,oc_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)

axes0.flat[2].set_xlabel('u (m s$^{-1}$)',fontsize=axis_font)
#axes0.flat[2].set_ylabel('Depth (m)',fontsize=axis_font)


axes0.flat[3].plot(roms_avg_v_sum_oc,roms_dep_sum_oc,color=roms_c)
axes0.flat[3].plot(roms_std_v_sum_oc_low,roms_dep_sum_oc,color=roms_c,linestyle=std_l)
axes0.flat[3].plot(roms_std_v_sum_oc_high,roms_dep_sum_oc,color=roms_c,linestyle=std_l)

axes0.flat[3].plot(oc_avg_v_sum,oc_dep_plt,color=moor_c,linewidth=moor_lw)
axes0.flat[3].plot(oc_std_v_sum_low,oc_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)
axes0.flat[3].plot(oc_std_v_sum_high,oc_dep_plt,color=moor_c,linewidth=moor_lw,linestyle=std_l)

axes0.flat[3].set_xlabel('v (m s$^{-1}$)',fontsize=axis_font)

axes0.flat[0].legend(loc='lower right',fontsize=axis_font,ncol=1,borderaxespad=0.,handlelength=1.5)
#axes0.flat[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0.3,1.02,0.33,.102],ncol=2,mode='expand',borderaxespad=0.,handlelength=1.5)
#axes0.flat[1].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0.3,1.02,0.3,.102],ncol=2,mode='expand',borderaxespad=0.,handlelength=1.5)

for i in range(len(axes0.flat)):
    axes0.flat[i].tick_params(axis='both',which='major',labelsize=axis_font)

xkey = 0
ykey = 1.02
axes0.flat[0].text(xkey,ykey,'c) LACSD ADCP A'+str(la_ch+1)+' (X)',transform=axes0.flat[0].transAxes,fontsize=axis_font)
axes0.flat[1].text(xkey,ykey,'d) LACSD ADCP A'+str(la_ch+1)+' (X)',transform=axes0.flat[1].transAxes,fontsize=axis_font)
axes0.flat[2].text(xkey,ykey,'e) OC-T-1 (O)',transform=axes0.flat[2].transAxes,fontsize=axis_font)
axes0.flat[3].text(xkey,ykey,'f) OC-T-1 (O)',transform=axes0.flat[3].transAxes,fontsize=axis_font)

fig0.savefig(fig_path+'la_oc_vertical_allyear_his_L1_A'+str(la_ch+1)+'.png',bbox_inches='tight')



# plot all la profiles to see 
figw = 10
figh = 18
fig0,axes0 = plt.subplots(3,2,figsize=[figw,figh])

a_p = 0
b_p = 0
for a_i in range(0,len(axes0.flat),2):
    axes0.flat[a_i].plot(roms_avg_u_sum_la[a_p],roms_dep_sum_la[a_p],color=roms_c,label='ROMS')
    axes0.flat[a_i].plot(roms_std_u_sum_la_low[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    axes0.flat[a_i].plot(roms_std_u_sum_la_high[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    axes0.flat[a_i].plot(la_u_avg[a_p],la_dep_plt,color=moor_c,label='ADCP')
    axes0.flat[a_i].plot(la_u_std_low[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
    axes0.flat[a_i].plot(la_u_std_high[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
    a_p += 1
    
for b_i in range(1,len(axes0.flat),2):
    axes0.flat[b_i].plot(roms_avg_v_sum_la[b_p],roms_dep_sum_la[b_p],color=roms_c)
    axes0.flat[b_i].plot(roms_std_v_sum_la_low[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    axes0.flat[b_i].plot(roms_std_v_sum_la_high[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    axes0.flat[b_i].plot(la_v_avg[b_p],la_dep_plt,color=moor_c)
    axes0.flat[b_i].plot(la_v_std_low[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
    axes0.flat[b_i].plot(la_v_std_high[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
    b_p += 1
    

#axes0.flat[a_i].set_xlabel('u m s$^{-1}$',fontsize=axis_font)
#axes0.flat[a_i].set_ylabel('Depth',fontsize=axis_font)
#axes0.flat[1].set_xlabel('v m s$^{-1}$',fontsize=axis_font)

#axes0.flat[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0,1.02,2.2,.102],ncol=2,mode='expand',borderaxes0pad=0.,handlelength=3)
axes0.flat[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0.6,1.02,1.1,.102],ncol=2,mode='expand',borderaxespad=0.,handlelength=3)

for i in range(len(axes0.flat)):
    axes0.flat[i].tick_params(axis='both',which='major',labelsize=axis_font)

fig0.savefig(fig_path+'la_vertical_allyear_his_L1_0-2.png',bbox_inches='tight')


fig0,axes0 = plt.subplots(3,2,figsize=[figw,figh])

a_p = 3
b_p = 3
for a_i in range(0,len(axes0.flat),2):
    axes0.flat[a_i].plot(roms_avg_u_sum_la[a_p],roms_dep_sum_la[a_p],color=roms_c,label='ROMS')
    axes0.flat[a_i].plot(roms_std_u_sum_la_low[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    axes0.flat[a_i].plot(roms_std_u_sum_la_high[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    if a_p == 4:
        axes0.flat[a_i].plot(np.array(pd.Series(la_u_avg[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,label='ADCP')
        axes0.flat[a_i].plot(np.array(pd.Series(la_u_std_low[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,linestyle=std_l)
        axes0.flat[a_i].plot(np.array(pd.Series(la_u_std_high[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,linestyle=std_l)
    else:
        axes0.flat[a_i].plot(la_u_avg[a_p],la_dep_plt,color=moor_c,label='ADCP')
        axes0.flat[a_i].plot(la_u_std_low[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
        axes0.flat[a_i].plot(la_u_std_high[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
    a_p += 1
    
for b_i in range(1,len(axes0.flat),2):
    axes0.flat[b_i].plot(roms_avg_v_sum_la[b_p],roms_dep_sum_la[b_p],color=roms_c)
    axes0.flat[b_i].plot(roms_std_v_sum_la_low[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    axes0.flat[b_i].plot(roms_std_v_sum_la_high[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    if b_p == 4:
        axes0.flat[b_i].plot(np.array(pd.Series(la_v_avg[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,label='ADCP')
        axes0.flat[b_i].plot(np.array(pd.Series(la_v_std_low[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,linestyle=std_l)
        axes0.flat[b_i].plot(np.array(pd.Series(la_v_std_high[a_p]).interpolate().tolist()),la_dep_plt,color=moor_c,linestyle=std_l)
    else:
        axes0.flat[b_i].plot(la_v_avg[b_p],la_dep_plt,color=moor_c)
        axes0.flat[b_i].plot(la_v_std_low[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
        axes0.flat[b_i].plot(la_v_std_high[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
    b_p += 1

axes0.flat[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0.6,1.02,1.1,.102],ncol=2,mode='expand',borderaxespad=0.,handlelength=3)

for i in range(len(axes0.flat)):
    axes0.flat[i].tick_params(axis='both',which='major',labelsize=axis_font)

fig0.savefig(fig_path+'la_vertical_allyear_his_L1_3-5.png',bbox_inches='tight')

fig0,axes0 = plt.subplots(3,2,figsize=[figw,figh])

a_p = 6
b_p = 6
for a_i in range(0,len(axes0.flat),2):
    axes0.flat[a_i].plot(roms_avg_u_sum_la[a_p],roms_dep_sum_la[a_p],color=roms_c,label='ROMS')
    axes0.flat[a_i].plot(roms_std_u_sum_la_low[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    axes0.flat[a_i].plot(roms_std_u_sum_la_high[a_p],roms_dep_sum_la[a_p],color=roms_c,linestyle=std_l)
    axes0.flat[a_i].plot(la_u_avg[a_p],la_dep_plt,color=moor_c,label='ADCP')
    axes0.flat[a_i].plot(la_u_std_low[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
    axes0.flat[a_i].plot(la_u_std_high[a_p],la_dep_plt,color=moor_c,linestyle=std_l)
    a_p += 1
    
for b_i in range(1,len(axes0.flat),2):
    axes0.flat[b_i].plot(roms_avg_v_sum_la[b_p],roms_dep_sum_la[b_p],color=roms_c)
    axes0.flat[b_i].plot(roms_std_v_sum_la_low[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    axes0.flat[b_i].plot(roms_std_v_sum_la_high[b_p],roms_dep_sum_la[b_p],color=roms_c,linestyle=std_l)
    axes0.flat[b_i].plot(la_v_avg[b_p],la_dep_plt,color=moor_c)
    axes0.flat[b_i].plot(la_v_std_low[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
    axes0.flat[b_i].plot(la_v_std_high[b_p],la_dep_plt,color=moor_c,linestyle=std_l)
    b_p += 1

axes0.flat[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=[0.6,1.02,1.1,.102],ncol=2,mode='expand',borderaxespad=0.,handlelength=3)

for i in range(len(axes0.flat)):
    axes0.flat[i].tick_params(axis='both',which='major',labelsize=axis_font)

fig0.savefig(fig_path+'la_vertical_allyear_his_L1_6-8.png',bbox_inches='tight')
