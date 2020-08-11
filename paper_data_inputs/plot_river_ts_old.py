import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime

# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_no_watershed_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_new.nc'

fig_path = './figs/short_'
###############
# major data (10 yrs)
###############
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['ammonium']) # mmol/m3
major_no3 = np.array(major_nc.variables['nitrate']) # mmol/m3
major_po4 = np.array(major_nc.variables['phosphate']) # mmol/m3
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 

major_tn = np.array(major_nc.variables['total_nitrogen']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan
major_allf = np.nansum(np.nansum(major_flo,axis=1),axis=1)
major_alln = np.nansum(np.nansum(major_tn,axis=1),axis=1)
major_allp = np.nansum(np.nansum(major_po4,axis=1),axis=1)

##############
# 24 yrs
##############
minor_nc = Dataset(minor_path,'r')

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time_dt = np.array(minor_time_l)

minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['ammonium']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['nitrate']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['phosphate']) # mmol/m3
minor_tn = np.array(minor_nc.variables['total_nitrogen'])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan
minor_allf = np.nansum(np.nansum(minor_flo,axis=1),axis=1)
minor_alln = np.nansum(np.nansum(minor_tn,axis=1),axis=1)
minor_allp = np.nansum(np.nansum(minor_po4,axis=1),axis=1)

# plotting
figw = 10
figh = 8
axis_tick_font = 14
#major_names = ['HTP','JWPCP','OCSD','PLWTP']
#major_linesty = ['-','--','-.',':']
lw = 2

# individual rivers
savename_ind = fig_path+'river_ts_ind.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for m_i in range(major_flo.shape[1]):
    axes.flat[0].plot(major_time_dt,major_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt,major_tn[:,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(major_time_dt,major_po4[:,m_i,m_i],linewidth=lw)
for m_i in range(minor_flo.shape[1]):
    axes.flat[0].plot(minor_time_dt,minor_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(minor_time_dt,minor_tn[:,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(minor_time_dt,minor_po4[:,m_i,m_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_ind,bbox_inches='tight')

# cumulative rivers 
savename_sum = fig_path+'river_ts_sum.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt,major_allf,linewidth=lw)
axes.flat[0].plot(minor_time_dt,minor_allf,linewidth=lw)
axes.flat[1].plot(major_time_dt,major_alln,linewidth=lw)
axes.flat[1].plot(minor_time_dt,minor_alln,linewidth=lw)
axes.flat[2].plot(major_time_dt,major_allp,linewidth=lw)
axes.flat[2].plot(minor_time_dt,minor_allp,linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_sum,bbox_inches='tight')

# individual rivers flux
savename_fluxind = fig_path+'river_ts_ind_flux.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for m_i in range(major_flo.shape[1]):
    axes.flat[0].plot(major_time_dt,major_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt,major_tn[:,m_i,m_i]*major_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(major_time_dt,major_po4[:,m_i,m_i]*major_flo[:,m_i,m_i],linewidth=lw)
for m_i in range(minor_flo.shape[1]):
    axes.flat[0].plot(minor_time_dt,minor_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(minor_time_dt,minor_tn[:,m_i,m_i]*minor_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(minor_time_dt,minor_po4[:,m_i,m_i]*minor_flo[:,m_i,m_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_fluxind,bbox_inches='tight')

# cumulative river flux 
savename_fluxsum = fig_path+'river_ts_sum_flux.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(minor_time_dt,minor_allf,linewidth=lw)
a = []
b = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])
    b.append(major_flo[:,m_i,m_i]*major_po4[:,m_i,m_i])
major_fluxn = np.nansum(np.array(a),axis=0)
major_fluxp = np.nansum(np.array(b),axis=0)
axes.flat[1].plot(major_time_dt,major_fluxn,linewidth=lw)
axes.flat[2].plot(major_time_dt,major_fluxp,linewidth=lw)

axes.flat[0].plot(major_time_dt,major_allf,linewidth=lw)

a = []
b = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[:,m_i,m_i]*minor_tn[:,m_i,m_i])
    b.append(minor_flo[:,m_i,m_i]*minor_po4[:,m_i,m_i])
minor_fluxn = np.nansum(np.array(a),axis=0)
minor_fluxp = np.nansum(np.array(b),axis=0)
axes.flat[1].plot(minor_time_dt,minor_fluxn,linewidth=lw)
axes.flat[2].plot(minor_time_dt,minor_fluxp,linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol Flux s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_fluxsum,bbox_inches='tight')

# combine 10 yrs and 24 yrs
# find days at beginning and end to put empty indices in 10 yr data
num_st = major_time_dt[0]-minor_time_dt[0]
num_en = minor_time_dt[-1]-major_time_dt[-1]


# append zeros to beginning and end to have same indices
major_f_l = list(major_allf)
for i_i in range(num_st.days):
    major_f_l.insert(0,0)
for i_i in range(num_en.days):
    major_f_l.append(0)
major_long_allf = np.array(major_f_l)

major_n_l = list(major_alln)
for i_i in range(num_st.days):
    major_n_l.insert(0,0)
for i_i in range(num_en.days):
    major_n_l.append(0)
major_long_alln = np.array(major_n_l)

major_p_l = list(major_allp)
for i_i in range(num_st.days):
    major_p_l.insert(0,0)
for i_i in range(num_en.days):
    major_p_l.append(0)
major_long_allp = np.array(major_p_l)


major_n_f = list(major_fluxn)
for i_i in range(num_st.days):
    major_n_f.insert(0,0)
for i_i in range(num_en.days):
    major_n_f.append(0)
major_long_fluxn = np.array(major_n_f)

major_p_f = list(major_fluxp)
for i_i in range(num_st.days):
    major_p_f.insert(0,0)
for i_i in range(num_en.days):
    major_p_f.append(0)
major_long_fluxp = np.array(major_p_f)

r_allf = major_long_allf+minor_allf
r_alln = major_long_alln+minor_alln
r_allp = major_long_allp+minor_allp

# 10 and 24 yrs cumulative 
savename_allsum = fig_path+'river_ts_all_sum.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(minor_time_dt,r_allf,linewidth=lw)
axes.flat[1].plot(minor_time_dt,r_alln,linewidth=lw)
axes.flat[2].plot(minor_time_dt,r_allp,linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_allsum,bbox_inches='tight')

# 10 and 24 yrs cumulative flux
savename_allflux = fig_path+'river_ts_all_flux.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(minor_time_dt,r_allf,linewidth=lw)
#axes.flat[1].plot(minor_time_dt,r_alln*r_allf,linewidth=lw)
#axes.flat[2].plot(minor_time_dt,r_allp*r_allf,linewidth=lw)
axes.flat[1].plot(minor_time_dt,major_long_fluxn+minor_fluxn,linewidth=lw)
axes.flat[2].plot(minor_time_dt,major_long_fluxp+minor_fluxp,linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_allflux,bbox_inches='tight')

# 10 and 24 yrs cumulative flux 1997-2007
savename_allflux_short = fig_path+'river_ts_all_flux_19972007.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(minor_time_dt[num_st.days:-num_en.days],r_allf[num_st.days:-num_en.days],linewidth=lw)
axes.flat[1].plot(minor_time_dt[num_st.days:-num_en.days],major_long_fluxn[num_st.days:-num_en.days]+minor_fluxn[num_st.days:-num_en.days],linewidth=lw)
axes.flat[2].plot(minor_time_dt[num_st.days:-num_en.days],major_long_fluxp[num_st.days:-num_en.days]+minor_fluxp[num_st.days:-num_en.days],linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_allflux_short,bbox_inches='tight')


# individual rivers flux 1997-2007
savename_fluxind_short = fig_path+'river_ts_ind_flux_19972007.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for m_i in range(major_flo.shape[1]):
    axes.flat[0].plot(major_time_dt,major_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt,major_tn[:,m_i,m_i]*major_flo[:,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(major_time_dt,major_po4[:,m_i,m_i]*major_flo[:,m_i,m_i],linewidth=lw)
for m_i in range(minor_flo.shape[1]):
    axes.flat[0].plot(minor_time_dt[num_st.days:-num_en.days],minor_flo[num_st.days:-num_en.days,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(minor_time_dt[num_st.days:-num_en.days],minor_tn[num_st.days:-num_en.days,m_i,m_i]*minor_flo[num_st.days:-num_en.days,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(minor_time_dt[num_st.days:-num_en.days],minor_po4[num_st.days:-num_en.days,m_i,m_i]*minor_flo[num_st.days:-num_en.days,m_i,m_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
fig.savefig(savename_fluxind_short,bbox_inches='tight')

# monthly clim of all rivers summed
mon_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
r_mon_flo = np.load('river_monthly_flo_all.npy')
r_mon_nflux = np.load('river_monthly_nflux_all.npy')
r_mon_pflux = np.load('river_monthly_pflux_all.npy')

savename_allflux_clim = fig_path+'river_ts_all_flux_clim.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(mon_name,r_mon_flo,linewidth=lw)
axes.flat[1].plot(mon_name,r_mon_nflux,linewidth=lw)
axes.flat[2].plot(mon_name,r_mon_pflux,linewidth=lw)

#axes.flat[0].set_ybound(lower=0)
#axes.flat[1].set_ybound(lower=0)
#axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_allflux_clim,bbox_inches='tight')
