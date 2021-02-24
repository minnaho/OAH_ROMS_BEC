import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import scipy.io
import cmocean as cmocean

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'
fig_path = './figs/'

#convert to kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# conversions mg/L to mmol/m3
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

major_time_dt = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False)
'''
# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)
'''


major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2']) # mmol/m3
major_on = np.array(major_nc.variables['organic_N']) # mmol/m3
major_bod = np.array(major_nc.variables['BOD']) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4']) # mmol/m3
major_op = np.array(major_nc.variables['organic_P']) # mmol/m3
major_fe  = np.array(major_nc.variables['dissolved_Fe'])  # mmol/m3
major_pH  = np.array(major_nc.variables['pH']) 
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_salt = np.array(major_nc.variables['salinity']) 
major_toc = np.array(major_nc.variables['total_organic_C']) 
major_tnn = np.array(major_nc.variables['total_N']) 


major_nh4[major_nh4>1E10] == np.nan
major_no3[major_no3>1E10] == np.nan
major_no2[major_no2>1E10] == np.nan
major_on[major_on>1E10] == np.nan

major_tn = major_nh4+major_no3+major_no2+major_on
major_din = major_nh4+major_no3+major_no2
major_tp = major_po4+major_op

major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_toc[major_toc>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

##############
# minor data
##############
minor_nc = Dataset(minor_path,'r')
minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(minor_nc.variables['NO2']) # mmol/m3
minor_on = np.array(minor_nc.variables['organic_N']) # mmol/m3
minor_bod = np.array(minor_nc.variables['BOD']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['PO4']) # mmol/m3
minor_op = np.array(minor_nc.variables['organic_P']) # mmol/m3
minor_fe  = np.array(minor_nc.variables['dissolved_Fe'])  # mmol/m3
minor_pH  = np.array(minor_nc.variables['pH']) 
minor_alk = np.array(minor_nc.variables['alkalinity']) 
minor_temp = np.array(minor_nc.variables['temperature']) 
minor_salt = np.array(minor_nc.variables['salinity']) 
minor_toc = np.array(minor_nc.variables['total_organic_C']) 

minor_nh4[minor_nh4>1E10] == np.nan
minor_no3[minor_no3>1E10] == np.nan
minor_no2[minor_no2>1E10] == np.nan
minor_on[minor_on>1E10] == np.nan

minor_tn = minor_nh4+minor_no3+minor_no2+minor_on
minor_din = minor_nh4+minor_no3+minor_no2
minor_tp = minor_po4+minor_op

minor_tn[minor_tn>1E20] = np.nan
minor_tp[minor_tp>1E20] = np.nan
minor_toc[minor_toc>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

# plotting major
figw = 12
#figw = 12
figh = 6
axis_tick_font = 14
axis_font = 14
savename_major = fig_path+'major_potw_ts_summed.png'
lw = 2

enin = 361

plt.ion()

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh+2])
axes.flat[0].plot(major_time_dt[:enin],np.nansum(major_flo[:enin,:],axis=1),linewidth=lw)
axes.flat[1].plot(major_time_dt[:enin],np.nansum(major_flo[:enin,:]*major_on[:enin,:]*s_to_d*mmol_to_mol*g_to_kg*g_N,axis=1),linewidth=lw)
axes.flat[2].plot(major_time_dt[:enin],np.nansum(major_flo[:enin,:]*major_din[:enin,:]*s_to_d*mmol_to_mol*g_to_kg*g_N,axis=1),linewidth=lw)
#axes.flat[0].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\nm$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('ON Flux\nkg d$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('DIN Flux\nkg d$^{-1}$',fontsize=axis_font)
for i in range(len(axes.flat)):
    #axes.flat[i].set_ybound(lower=0)
    axes.flat[i].tick_params(axis='both',which='major',labelsize=axis_tick_font)
    axes.flat[i].yaxis.set_ticks_position('both')
    axes.flat[i].xaxis.set_ticks_position('both')
        

axes.flat[1].yaxis.set_major_locator(mtick.MultipleLocator(10000))
axes.flat[2].yaxis.set_major_locator(mtick.MultipleLocator(10000))
#axes.flat[5].set_yscale('log')
#axes.flat[5].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
#axes.flat[5].set_ybound(lower=0,upper=1.7E5)
axes.flat[0].text(0,1.03,'a)',fontsize=axis_font,transform=axes.flat[0].transAxes)
axes.flat[1].text(0,1.03,'b)',fontsize=axis_font,transform=axes.flat[1].transAxes)
axes.flat[2].text(0,1.03,'c)',fontsize=axis_font,transform=axes.flat[2].transAxes)
fig.savefig(savename_major,bbox_inches='tight')


