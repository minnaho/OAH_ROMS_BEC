import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime

# data paths
freq = 'daily'
if freq == 'daily':
    major_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_daily.nc'
if freq == 'monthly':
    major_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc'

fig_path = './figs/'
###############
# major data (10 yrs)
###############
major_nc = Dataset(major_path,'r')

ind_1997_10 = 0   # index for start of 1997
ind_2007_10 = np.array((major_nc.variables['time'])).shape[0] # end 2017

major_time_dt = num2date(np.array(major_nc.variables['time'][ind_1997_10:ind_2007_10]),major_nc.variables['time'].units,only_use_cftime_datetimes=False)

major_flo = np.array(major_nc.variables['flow'][ind_1997_10:ind_2007_10]) # m3/s

# los angeles river, san gabriel, santa ana
indla = 32
indsg = 51
indsa = 60

ind_2007 = 3652
ind_2010 = 4748
ind_2017 = major_time_dt.shape[0]

major_flo_ind = np.array(major_nc.variables['flow'][ind_2007:ind_2017]) # m3/s
flola = np.nansum(major_flo_ind[:,indla])
flosg = np.nansum(major_flo_ind[:,indsg])
flosa = np.nansum(major_flo_ind[:,indsa])
floal = np.nansum(major_flo_ind)

perc = (flola+flosg+flosa)/floal


major_nh4 = np.array(major_nc.variables['NH4'][ind_1997_10:ind_2007_10]) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3'][ind_1997_10:ind_2007_10]) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4'][ind_1997_10:ind_2007_10]) # mmol/m3

major_tn = np.array(major_nc.variables['total_N'][ind_1997_10:ind_2007_10]) 
major_tp = np.array(major_nc.variables['total_P'][ind_1997_10:ind_2007_10]) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

major_allf = np.nansum(major_flo,axis=1)

major_nflux = major_flo*major_tn
major_alln = np.nansum(major_nflux,axis=1)

major_pflux = major_flo*major_tp
major_allp = np.nansum(major_pflux,axis=1)

r_allf = major_allf
r_alln = major_alln
r_allp = major_allp

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
#plt.ion()
if freq == 'monthly':
    savename_allsum = fig_path+'river_ts_all_sum_1997_2017_monthly.pdf'
    labela = 368
    labelb = 93000
if freq == 'daily':
    savename_allsum = fig_path+'river_ts_all_sum_1997_2017_daily.pdf'
    labela = 2770
    labelb = 560000
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
axes.flat[0].yaxis.set_ticks_position('both')
axes.flat[1].yaxis.set_ticks_position('both')
axes.flat[0].xaxis.set_ticks_position('both')
axes.flat[1].xaxis.set_ticks_position('both')
axes.flat[0].text(datetime.datetime(1996, 1, 1, 0, 0),labela,'a)',fontsize=axis_tick_font)
axes.flat[1].text(datetime.datetime(1996, 1, 1, 0, 0),labelb,'b)',fontsize=axis_tick_font)
fig.savefig(savename_allsum,bbox_inches='tight')
