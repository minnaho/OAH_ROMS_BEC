import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import pandas as pd

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017.nc'
fig_path = './figs/'

#convert to kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# other constituents
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855
mg_l_a = 1000/100.09 # mg/L CaCO3 to mmol/m3


###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False)

in_st = 13149 # 2007-01-01
in_en = major_time.shape[0]

major_time_dt = major_time[in_st:in_en]

major_flo = np.array(major_nc.variables['flow'][in_st:in_en,2]) # m3/s
major_nh4 = np.array(major_nc.variables['NH4'][in_st:in_en,2]) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3'][in_st:in_en,2]) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2'][in_st:in_en,2]) # mmol/m3
major_on = np.array(major_nc.variables['organic_N'][in_st:in_en,2]) # mmol/m3
major_bod  = np.array(major_nc.variables['BOD'][in_st:in_en,2]) 
major_alk = np.array(major_nc.variables['alkalinity'][in_st:in_en,2]) 
major_toc = np.array(major_nc.variables['total_organic_C'][in_st:in_en,2]) 
major_bod  = np.array(major_nc.variables['BOD'][in_st:in_en,2])  # mmol/m3
major_sil  = np.array(major_nc.variables['SiO4'][in_st:in_en,2])  # mmol/m3
major_alk  = np.array(major_nc.variables['alkalinity'][in_st:in_en,2])  # mmol/m3
major_sal  = np.array(major_nc.variables['salinity'][in_st:in_en,2])  # PSU


major_nh4[major_nh4>1E10] == np.nan
major_no3[major_no3>1E10] == np.nan
major_no2[major_no2>1E10] == np.nan
major_on[major_on>1E10] == np.nan

major_bod[major_bod>1E10] == np.nan
major_toc[major_toc>1E10] == np.nan
major_bod[major_bod>1E10] == np.nan
major_sil[major_sil>1E10] == np.nan
major_alk[major_alk>1E10] == np.nan

major_tn = major_nh4+major_no3+major_no2+major_on
major_din = major_nh4+major_no3+major_no2

major_tn[major_tn>1E20] = np.nan

#############
# plot
#############
plt.ion()

figw = 10
figh = 12
axis_tick_font = 16

pcol = 'black'
rcol = 'blue'

savename = fig_path+'ocsd_ts.pdf'
fig,axes = plt.subplots(5,1,sharex=True,figsize=[figw,figh])

axes.flat[0].plot(major_time_dt,major_flo,color=pcol)
ax0 = axes.flat[0].twinx()
ax0.plot(major_time_dt,major_sal,color=rcol,linestyle='--')

axes.flat[1].plot(major_time_dt,major_on*(1./mg_l_n),color=pcol)
ax1 = axes.flat[1].twinx()
ax1.plot(major_time_dt,major_bod*(1./mg_l_o),color=rcol,linestyle='--')

axes.flat[2].plot(major_time_dt,major_nh4*(1./mg_l_n),color=pcol)
ax2 = axes.flat[2].twinx()
ax2.plot(major_time_dt,major_no3*(1./mg_l_n),color=rcol,linestyle='--')

axes.flat[3].plot(major_time_dt,major_alk*(1./mg_l_a),color=pcol)
ax3 = axes.flat[3].twinx()
ax3.plot(major_time_dt,major_sil*(1./mg_l_s),color=rcol,linestyle='--')

axes.flat[4].plot(major_time_dt,major_flo*major_din*s_to_d*mmol_to_mol*g_to_kg*g_N,color=pcol)

axes.flat[0].set_ylabel('Volume Flux\nm$^3$ s$^{-1}$',fontsize=axis_tick_font)
ax0.set_ylabel('Salinity PSU',fontsize=axis_tick_font,color=rcol)

axes.flat[1].set_ylabel('ON mg L$^{-1}$',fontsize=axis_tick_font)
ax1.set_ylabel('BOD mg L$^{-1}$',fontsize=axis_tick_font,color=rcol)

axes.flat[2].set_ylabel('NH4 mg L$^{-1}$',fontsize=axis_tick_font)
ax2.set_ylabel('NO3 mg L$^{-1}$',fontsize=axis_tick_font,color=rcol)

axes.flat[3].set_ylabel('Alk mg L$^{-1}$',fontsize=axis_tick_font)
ax3.set_ylabel('SiO4 mg L$^{-1}$',fontsize=axis_tick_font,color=rcol)

axes.flat[4].set_ylabel('DIN Flux kg d$^{-1}$',fontsize=axis_tick_font)

axes.flat[0].tick_params(axis='y',labelcolor=pcol)
ax0.tick_params(axis='y',labelcolor=rcol)
axes.flat[1].tick_params(axis='y',labelcolor=pcol)
ax1.tick_params(axis='y',labelcolor=rcol)
axes.flat[2].tick_params(axis='y',labelcolor=pcol)
ax2.tick_params(axis='y',labelcolor=rcol)
axes.flat[3].tick_params(axis='y',labelcolor=pcol)
ax3.tick_params(axis='y',labelcolor=rcol)


axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[4].tick_params(axis='both',which='major',labelsize=axis_tick_font)

ax0.tick_params(axis='both',which='major',labelsize=axis_tick_font)
ax1.tick_params(axis='both',which='major',labelsize=axis_tick_font)
ax2.tick_params(axis='both',which='major',labelsize=axis_tick_font)
ax3.tick_params(axis='both',which='major',labelsize=axis_tick_font)

axes.flat[1].xaxis.set_ticks_position('both')
axes.flat[2].xaxis.set_ticks_position('both')
axes.flat[3].xaxis.set_ticks_position('both')
axes.flat[4].xaxis.set_ticks_position('both')
axes.flat[4].yaxis.set_ticks_position('both')

fig.savefig(savename,bbox_inches='tight')
