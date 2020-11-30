import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import pandas as pd
import matplotlib.ticker as mticker


fig_path = './figs/'
# data paths
#major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc'
major_path ='/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc' 
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'
 



###############
# river major data (10 yrs) 1997-2007
###############
# convert to kg/month, then sum months into season
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

# divide flows

major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3']) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4']) # mmol/m3
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_tn = np.array(major_nc.variables['total_N']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan


# turn to array so can sum all rivers in region up
# then reshape to (14,12) because this data set is 14 years
# then average over 14 years to get year average
ry0 = 21

r_major_flo = np.nanmean(np.nansum(np.array(major_flo),axis=1).reshape(ry0,12),axis=0)

r_major_tnn = np.nanmean(np.nansum(np.array(major_tn)*np.array(major_flo),axis=1).reshape(ry0,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

# sum different river datasets
r_flo_sum = r_major_flo
r_tnn_sum = r_major_tnn

r_season_flo = np.array([(r_flo_sum[11])+(r_flo_sum[1])+(r_flo_sum[0]),(r_flo_sum[2])+(r_flo_sum[3])+(r_flo_sum[4]),(r_flo_sum[5])+(r_flo_sum[6])+(r_flo_sum[7]),(r_flo_sum[8])+(r_flo_sum[9])+(r_flo_sum[10])])

r_season_tnn = np.array([(r_tnn_sum[11])+(r_tnn_sum[1])+(r_tnn_sum[0]),(r_tnn_sum[2])+(r_tnn_sum[3])+(r_tnn_sum[4]),(r_tnn_sum[5])+(r_tnn_sum[6])+(r_tnn_sum[7]),(r_tnn_sum[8])+(r_tnn_sum[9])+(r_tnn_sum[10])])

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2010
potw_1997 = 312 # 1997-01-31
potw_2013 = 564 # 2017-12-31

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l[potw_1997:potw_2013])

major_flo = np.array(potw_ma_nc.variables['flow'][potw_1997:potw_2013]) # m3/s
major_nh4 = np.array(potw_ma_nc.variables['NH4'][potw_1997:potw_2013]) # mmol/m3
major_no3 = np.array(potw_ma_nc.variables['NO3'][potw_1997:potw_2013]) # mmol/m3
major_no2 = np.array(potw_ma_nc.variables['NO2'][potw_1997:potw_2013]) # mmol/m3
major_on  = np.array(potw_ma_nc.variables['organic_N'][potw_1997:potw_2013]) # mmol/m3
major_po4 = np.array(potw_ma_nc.variables['PO4'][potw_1997:potw_2013]) # mmol/m3
major_op  = np.array(potw_ma_nc.variables['organic_P'][potw_1997:potw_2013]) # mmol/m3
major_pH  = np.array(potw_ma_nc.variables['pH'][potw_1997:potw_2013])
major_alk = np.array(potw_ma_nc.variables['alkalinity'][potw_1997:potw_2013])
major_temp = np.array(potw_ma_nc.variables['temperature'][potw_1997:potw_2013])
major_salt = np.array(potw_ma_nc.variables['salinity'][potw_1997:potw_2013])

major_nh4[major_nh4>1E20] = np.nan
major_no3[major_no3>1E20] = np.nan
major_no2[major_no2>1E20] = np.nan
major_on[major_on>1E20] = np.nan
major_tn = np.nansum((major_no3,major_nh4,major_no2,major_on),axis=0)
major_tp = major_po4+major_op

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan


# turn to array so can sum all potw in region up
# then reshape to (17,12) because this data set is 17 years
# then average over 17 years to get year average
ry1 = 21

p_major_flo = np.nanmean(np.nansum(np.array(major_flo),axis=1).reshape(ry1,12),axis=0)

p_major_tnn = np.nanmean(np.nansum(np.array(major_tn)*np.array(major_flo),axis=1).reshape(ry1,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol


##############
# minor potw
##############

potw_mi_nc = Dataset(potw_minor_path,'r')

minor_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_onn = np.array(potw_mi_nc.variables['organic_N']) # mmol/m3
minor_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

minor_nh4[minor_nh4>1E20] = np.nan
minor_no3[minor_no3>1E20] = np.nan
minor_no2[minor_no2>1E20] = np.nan
minor_onn[minor_onn>1E20] = np.nan
minor_tn = np.nansum((minor_no3,minor_nh4,minor_no2,minor_onn),axis=0)

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

p_minor_flo = np.nanmean(np.nansum(np.array(minor_flo),axis=1).reshape(ry1,12),axis=0)

# convert to kg/month
p_minor_tnn = np.nanmean(np.nansum(np.array(minor_tn)*np.array(minor_flo),axis=1).reshape(ry1,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

# sum major and minor potw datasets
p_flo_sum = p_major_flo+p_minor_flo
p_tnn_sum = p_major_tnn+p_minor_tnn

p_season_flo = np.array([(p_flo_sum[11])+(p_flo_sum[1])+(p_flo_sum[0]),(p_flo_sum[2])+(p_flo_sum[3])+(p_flo_sum[4]),(p_flo_sum[5])+(p_flo_sum[6])+(p_flo_sum[7]),(p_flo_sum[8])+(p_flo_sum[9])+(p_flo_sum[10])])

p_season_tnn = np.array([(p_tnn_sum[11])+(p_tnn_sum[1])+(p_tnn_sum[0]),(p_tnn_sum[2])+(p_tnn_sum[3])+(p_tnn_sum[4]),(p_tnn_sum[5])+(p_tnn_sum[6])+(p_tnn_sum[7]),(p_tnn_sum[8])+(p_tnn_sum[9])+(p_tnn_sum[10])])


#p_season_tnn = p_season_tnn*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

#############
# plot
#############
plt.ion()

months = 12
mon_l = range(1,13)
mon_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
pcol='darkorange'
rcol='blue'

figw = 8
figh = 8
axis_tick_font = 16

savename = fig_path+'potw_river_flux_compare.pdf'
fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(mon_name,p_flo_sum,color=pcol,label='Ocean Outfalls')
axes.flat[0].plot(np.nan,np.nan,color=rcol,linestyle='--',label='Rivers')
#axes.flat[0].plot(mon_name,r_flo_sum,color='blue',linestyle='--',label='Rivers')
ax0 = axes.flat[0].twinx()
ax0.plot(mon_name,r_flo_sum,color=rcol,linestyle='--',label='Rivers')

axes.flat[0].tick_params(axis='y',labelcolor=pcol)
ax0.tick_params(axis='y',labelcolor=rcol)

axes.flat[1].plot(mon_name,p_tnn_sum,color='orange',label='Ocean Outfalls')
#axes.flat[1].plot(mon_name,r_tnn_sum,color='blue',linestyle='--',label='Rivers')
ax1 = axes.flat[1].twinx()
ax1.plot(mon_name,r_tnn_sum,color='blue',linestyle='--',label='Rivers')

#axes.flat[1].yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e'))
#ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1e'))

#axes.flat[1].ticklabel_format(axis='y',style='scientific',scilimits=(0,0))
#ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
axes.flat[0].text(-.4,50.4,'a)',fontsize=axis_tick_font)
axes.flat[1].text(-.4,5.185E6,'b)',fontsize=axis_tick_font)

class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt
    def __call__(self, x, pos=None):
        s = self.fmt % x
        decimal_point = '.'
        positive_sign = '+'
        tup = s.split('e')
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, '')
        exponent = tup[1][1:].lstrip('0')
        if exponent:
            exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s =  r'%s{\times}%s' % (significand, exponent)
        else:
            s =  r'%s%s' % (significand, exponent)
        return "${}$".format(s)

# Format with 2 decimal places
axes.flat[1].yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax1.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))

axes.flat[1].tick_params(axis='y',labelcolor=pcol)
ax1.tick_params(axis='y',labelcolor=rcol)

axes.flat[1].set_xticklabels(mon_name,rotation=45)


#axes.flat[0].set_ybound(lower=0)
#axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux kg month$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
ax0.tick_params(axis='both',which='major',labelsize=axis_tick_font)
ax1.tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].yaxis.set_ticks_position('both')
axes.flat[1].yaxis.set_ticks_position('both')
axes.flat[0].xaxis.set_ticks_position('both')
axes.flat[1].xaxis.set_ticks_position('both')
axes.flat[0].legend(loc='best',fontsize=16)


fig.savefig(savename,bbox_inches='tight')
