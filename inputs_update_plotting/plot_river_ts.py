import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime

# data paths
#major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_no_watershed_new.nc'
major_path = '/data/project1/minnaho/river_data/inputs_1997_2000/south_coast_rivers_updated_14_years_1997_2010_monthly.nc'
minor_path = '/data/project1/minnaho/river_data/inputs_1997_2000/south_coast_rivers_24_years_monthly_new.nc'

fig_path = './figs/'
###############
# major data (10 yrs)
###############
major_nc = Dataset(major_path,'r')

ind_1997_10 = 0   # index for start of 1997
ind_2007_10 = 132   # index for end of 2007

major_time_dt = num2date(np.array(major_nc.variables['time'][ind_1997_10:ind_2007_10]),major_nc.variables['time'].units,only_use_cftime_datetimes=False)

major_flo = np.array(major_nc.variables['flow'][ind_1997_10:ind_2007_10]) # m3/s
major_nh4 = np.array(major_nc.variables['ammonium'][ind_1997_10:ind_2007_10]) # mmol/m3
major_no3 = np.array(major_nc.variables['nitrate'][ind_1997_10:ind_2007_10]) # mmol/m3
major_po4 = np.array(major_nc.variables['phosphate'][ind_1997_10:ind_2007_10]) # mmol/m3

major_tn = np.array(major_nc.variables['total_nitrogen'][ind_1997_10:ind_2007_10]) 
major_tp = np.array(major_nc.variables['total_phosphorus'][ind_1997_10:ind_2007_10]) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

major_allf = np.nansum(np.nansum(major_flo,axis=1),axis=1)

major_nflux = major_flo*major_tn
major_alln = np.nansum(np.nansum(major_nflux,axis=1),axis=1)

major_pflux = major_flo*major_tp
major_allp = np.nansum(np.nansum(major_pflux,axis=1),axis=1)

##############
# 24 yrs
##############
ind_1997 = 84   # index for start of 1997
ind_2010 = 215   # index for end of 2007

minor_nc = Dataset(minor_path,'r')

minor_time_dt = num2date(np.array(minor_nc.variables['time'][ind_1997:ind_2010+1]),minor_nc.variables['time'].units,only_use_python_datetimes=True)

minor_flo = np.array(minor_nc.variables['flow'][ind_1997:ind_2010+1]) # m3/s
minor_nh4 = np.array(minor_nc.variables['ammonium'][ind_1997:ind_2010+1]) # mmol/m3
minor_no3 = np.array(minor_nc.variables['nitrate'][ind_1997:ind_2010+1]) # mmol/m3
minor_po4 = np.array(minor_nc.variables['phosphate'][ind_1997:ind_2010+1]) # mmol/m3
minor_tn = np.array(minor_nc.variables['total_nitrogen'][ind_1997:ind_2010+1])
minor_tp = np.array(minor_nc.variables['total_phosphorus'][ind_1997:ind_2010+1])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_tp[minor_tp>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

minor_allf = np.nansum(np.nansum(minor_flo,axis=1),axis=1)

minor_nflux = minor_flo*minor_tn
minor_alln = np.nansum(np.nansum(minor_nflux,axis=1),axis=1)

minor_pflux = minor_flo*minor_tp
minor_allp = np.nansum(np.nansum(minor_pflux,axis=1),axis=1)

r_allf = minor_allf+major_allf
r_alln = minor_alln+major_alln
r_allp = minor_allp+major_allp

s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14


# plotting
figw = 12
figh =8 
axis_tick_font = 14
#major_names = ['HTP','JWPCP','OCSD','PLWTP']
#major_linesty = ['-','--','-.',':']
lw = 2

# 10 and 24 yrs cumulative flux
plt.ion()
savename_allsum = fig_path+'river_ts_all_sum_1997_2010.pdf'
#fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt,r_allf,linewidth=lw)
axes.flat[1].plot(major_time_dt,r_alln,linewidth=lw)
#axes.flat[2].plot(major_time_dt,r_allp,linewidth=lw)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
#axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('TN kg month$^{-1}$',fontsize=axis_tick_font)
#axes.flat[2].set_ylabel('TP kg month$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].grid(True)
#axes.flat[1].grid(True)
#axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_allsum,bbox_inches='tight')

'''
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
'''
