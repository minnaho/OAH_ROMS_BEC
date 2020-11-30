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
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_updated_14_years_1997_2010_monthly.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc'

ocsd_data = '/data/project1/minnaho/potw_outfall_data/OO10-OCSD _REvised 06052020.xlsx'


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
major_nh4 = np.array(major_nc.variables['ammonium']) # mmol/m3
major_no3 = np.array(major_nc.variables['nitrate']) # mmol/m3
major_po4 = np.array(major_nc.variables['phosphate']) # mmol/m3
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_tn = np.array(major_nc.variables['total_nitrogen']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan


# turn to array so can sum all rivers in region up
# then reshape to (14,12) because this data set is 14 years
# then average over 14 years to get year average
ry0 = 14

r_major_flo = np.nanmean(np.nansum(np.nansum(np.array(major_flo),axis=1),axis=1).reshape(ry0,12),axis=0)

r_major_tnn = np.nanmean(np.nansum(np.nansum(np.array(major_tn)*np.array(major_flo),axis=1),axis=1).reshape(ry0,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol


##############
# river 24 yrs
##############
minor_nc = Dataset(minor_path,'r')

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time_dt = np.array(minor_time_l)

r_minor_st_in = 84 # index for start of 1997
r_minor_en_in = 251 # index for end of 2010

minor_flo = np.array(minor_nc.variables['flow'][r_minor_st_in:r_minor_en_in+1,:,:]) # m3/s
minor_nh4 = np.array(minor_nc.variables['ammonium'][r_minor_st_in:r_minor_en_in+1,:,:]) # mmol/m3
minor_no3 = np.array(minor_nc.variables['nitrate'][r_minor_st_in:r_minor_en_in+1,:,:]) # mmol/m3
minor_po4 = np.array(minor_nc.variables['phosphate'][r_minor_st_in:r_minor_en_in+1,:,:]) # mmol/m3
minor_tn = np.array(minor_nc.variables['total_nitrogen'][r_minor_st_in:r_minor_en_in+1,:,:])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

# turn to array so can sum all rivers in region up
# then reshape to (17,12) because this data set is 17 years (1997-2013)
# then average over 17 years to get year average
ry1 = 14

r_minor_flo = np.nanmean(np.nansum(np.nansum(np.array(minor_flo),axis=1),axis=1).reshape(ry1,12),axis=0)

# convert to kg/month, then sum months into season
r_minor_tnn = np.nanmean(np.nansum(np.nansum(np.array(minor_tn)*np.array(minor_flo),axis=1),axis=1).reshape(ry1,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol


# sum different river datasets
r_flo_sum = r_major_flo+r_minor_flo
r_tnn_sum = r_major_tnn+r_minor_tnn

r_season_flo = np.array([(r_flo_sum[11])+(r_flo_sum[1])+(r_flo_sum[0]),(r_flo_sum[2])+(r_flo_sum[3])+(r_flo_sum[4]),(r_flo_sum[5])+(r_flo_sum[6])+(r_flo_sum[7]),(r_flo_sum[8])+(r_flo_sum[9])+(r_flo_sum[10])])

r_season_tnn = np.array([(r_tnn_sum[11])+(r_tnn_sum[1])+(r_tnn_sum[0]),(r_tnn_sum[2])+(r_tnn_sum[3])+(r_tnn_sum[4]),(r_tnn_sum[5])+(r_tnn_sum[6])+(r_tnn_sum[7]),(r_tnn_sum[8])+(r_tnn_sum[9])+(r_tnn_sum[10])])

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2010
potw_1997 = 313 # 1997-01-31
potw_2013 = 481 # 2011-01-13

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l[potw_1997:potw_2013])

major_flo = np.array(potw_ma_nc.variables['flow'][potw_1997:potw_2013]) # m3/s
major_nh4 = np.array(potw_ma_nc.variables['NH4'][potw_1997:potw_2013]) # mmol/m3
major_no3 = np.array(potw_ma_nc.variables['NO3'][potw_1997:potw_2013]) # mmol/m3
major_no2 = np.array(potw_ma_nc.variables['NO2'][potw_1997:potw_2013]) # mmol/m3
major_on  = np.array(potw_ma_nc.variables['ON'][potw_1997:potw_2013]) # mmol/m3
major_po4 = np.array(potw_ma_nc.variables['PO4'][potw_1997:potw_2013]) # mmol/m3
major_op  = np.array(potw_ma_nc.variables['OP'][potw_1997:potw_2013]) # mmol/m3
major_fe  = np.array(potw_ma_nc.variables['Fe'][potw_1997:potw_2013])  # mmol/m3
major_pH  = np.array(potw_ma_nc.variables['pH'][potw_1997:potw_2013])
major_alk = np.array(potw_ma_nc.variables['alkalinity'][potw_1997:potw_2013])
major_temp = np.array(potw_ma_nc.variables['temperature'][potw_1997:potw_2013])
major_salt = np.array(potw_ma_nc.variables['salinity'][potw_1997:potw_2013])
major_toc  = np.array(potw_ma_nc.variables['TOC'][potw_1997:potw_2013])

major_tn = major_nh4+major_no3+major_no2+major_on
major_tp = major_po4+major_op

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan

# replace NO3/NO2 OCSD data with Martha's new calculations of NO3 + NO2
ocsd_df = pd.read_excel(ocsd_data,header=None,sheet_name='Sheet1')
# new NO3+NO2
# is it actually mg/L, not kg/m3? makes more sense as mg/L
kg_to_g = 1000
g_to_mol = 1./14
mol_to_mmol = 1000
mgL_to_mmolm3 = 1000./14

# starts at 12-1970 instead of 1-1971 [potw_1997+1:potw_2013+1]
ocsd_nox_l = list(ocsd_df[3][1:][potw_1997:potw_2013])

ocsd_nox = np.array(ocsd_nox_l).astype(float)*mgL_to_mmolm3

# replace ocsd major tn data with new calculations
major_tn[:,2,2] = major_nh4[:,2,2]+major_on[:,2,2]+ocsd_nox


# turn to array so can sum all potw in region up
# then reshape to (17,12) because this data set is 17 years
# then average over 17 years to get year average
ry0 = 14

p_major_flo = np.nanmean(np.nansum(np.nansum(np.array(major_flo),axis=1),axis=1).reshape(ry1,12),axis=0)

p_major_tnn = np.nanmean(np.nansum(np.nansum(np.array(major_tn)*np.array(major_flo),axis=1),axis=1).reshape(ry1,12),axis=0)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol


##############
# minor potw
##############

potw_mi_nc = Dataset(potw_minor_path,'r')

minor_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

minor_tn = minor_no3+minor_nh4+minor_no2

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

# inland POTW
# see Inland POTW excel for inland potw data
# kg/yr
inland_tnn = np.load('inland_potw_tnn_region.npy')
inland_tpp = np.load('inland_potw_tpp_region.npy')
inland_din = np.load('inland_potw_din_region.npy')
inland_dip = np.load('inland_potw_dip_region.npy')

# convert kg/yr to kg/month
nsd_tnn = np.array([inland_tnn[1]/12]*12)

# inland potw flow by region m3/yr
#ssd,nsd,occ,spp,smb,ven,sbb,scb
#inland_flows = [2348848,17432137,2564159,1.75E8,4941331,53495704,np.nan,255900740]
inland_flows = [2348592.5,17430240.42,2563880.146,175099510.9,4940793.908,53489884.95,np.nan,255872902.9]

# convert m3/yr to m3/s
nsd_flo = inland_flows[1]/(365*86400)

p_minor_flo = np.nansum(np.nansum(np.array(minor_flo[:12]),axis=1),axis=1)+nsd_flo

# convert to kg/month
p_minor_tnn = (np.nansum(np.nansum(np.array(minor_tn[:12])*np.array(minor_flo[:12]),axis=1),axis=1)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol)+nsd_tnn

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
axes.flat[0].text(-.4,62.3,'a)',fontsize=axis_tick_font)
axes.flat[1].text(-.4,5.82E6,'b)',fontsize=axis_tick_font)

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
axes.flat[0].legend(loc='best',fontsize=16)


fig.savefig(savename,bbox_inches='tight')
