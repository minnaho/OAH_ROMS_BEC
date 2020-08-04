import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pandas as pd

fig_path = './figs/'
# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc'

ocsd_data = '/data/project1/minnaho/potw_outfall_data/OO10-OCSD _REvised 06052020.xlsx'


atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
log_set = True

############
# load grid
############
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

# mask that is first 0-15km offshore
mask_mat = scipy.io.loadmat('../maskt.mat')['maskt'] 

################
# load atmos data
################
dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')
#m2_to_hectare = 10000
m2_resolution_grid = 330*330

oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_resolution_grid*mask_nc
redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_resolution_grid*mask_nc
alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_resolution_grid*mask_nc
fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_resolution_grid*mask_nc

# break into seasons
win_ind = [0,1,11]
spr_ind = [2,3,4]
sum_ind = [5,6,7]
aut_ind = [8,9,10]

oxn_season  = np.empty((4))
redn_season = np.empty((4))
alk_season  = np.empty((4))
fe_season   = np.empty((4))

oxn_win0 = np.array(oxn[win_ind[0]]+oxn[win_ind[1]]+oxn[win_ind[2]])
oxn_win0[oxn_win0==0] = np.nan
oxn_win_sum = np.nansum(oxn_win0)

oxn_spr0 = np.array(oxn[spr_ind[0]]+oxn[spr_ind[1]]+oxn[spr_ind[2]])
oxn_spr0[oxn_spr0==0] = np.nan
oxn_spr_sum = np.nansum(oxn_spr0)

oxn_sum0 = np.array(oxn[sum_ind[0]]+oxn[sum_ind[1]]+oxn[sum_ind[2]])
oxn_sum0[oxn_sum0==0] = np.nan
oxn_sum_sum = np.nansum(oxn_sum0)

oxn_aut0 = np.array(oxn[aut_ind[0]]+oxn[aut_ind[1]]+oxn[aut_ind[2]])
oxn_aut0[oxn_aut0==0] = np.nan
oxn_aut_sum = np.nansum(oxn_aut0)

redn_win0 = np.array(redn[win_ind[0]]+redn[win_ind[1]]+redn[win_ind[2]])
redn_win0[redn_win0==0] = np.nan
redn_win_sum = np.nansum(redn_win0)

redn_spr0 = np.array(redn[spr_ind[0]]+redn[spr_ind[1]]+redn[spr_ind[2]])
redn_spr0[redn_spr0==0] = np.nan
redn_spr_sum = np.nansum(redn_spr0)

redn_sum0 = np.array(redn[sum_ind[0]]+redn[sum_ind[1]]+redn[sum_ind[2]])
redn_sum0[redn_sum0==0] = np.nan
redn_sum_sum = np.nansum(redn_sum0)

redn_aut0 = np.array(redn[aut_ind[0]]+redn[aut_ind[1]]+redn[aut_ind[2]])
redn_aut0[redn_aut0==0] = np.nan
redn_aut_sum = np.nansum(redn_aut0)

alk_win0 = np.array(alk[win_ind[0]]+alk[win_ind[1]]+alk[win_ind[2]])
alk_win0[alk_win0==0] = np.nan
alk_win_sum = np.nansum(alk_win0)

alk_spr0 = np.array(alk[spr_ind[0]]+alk[spr_ind[1]]+alk[spr_ind[2]])
alk_spr0[alk_spr0==0] = np.nan
alk_spr_sum = np.nansum(alk_spr0)

alk_sum0 = np.array(alk[sum_ind[0]]+alk[sum_ind[1]]+alk[sum_ind[2]])
alk_sum0[alk_sum0==0] = np.nan
alk_sum_sum = np.nansum(alk_sum0)

alk_aut0 = np.array(alk[aut_ind[0]]+alk[aut_ind[1]]+alk[aut_ind[2]])
alk_aut0[alk_aut0==0] = np.nan
alk_aut_sum = np.nansum(alk_aut0)

fe_win0 = np.array(fe[win_ind[0]]+fe[win_ind[1]]+fe[win_ind[2]])
fe_win0[fe_win0==0] = np.nan
fe_win_sum = np.nansum(fe_win0)

fe_spr0 = np.array(fe[spr_ind[0]]+fe[spr_ind[1]]+fe[spr_ind[2]])
fe_spr0[fe_spr0==0] = np.nan
fe_spr_sum = np.nansum(fe_spr0)

fe_sum0 = np.array(fe[sum_ind[0]]+fe[sum_ind[1]]+fe[sum_ind[2]])
fe_sum0[fe_sum0==0] = np.nan
fe_sum_sum = np.nansum(fe_sum0)

fe_aut0 = np.array(fe[aut_ind[0]]+fe[aut_ind[1]]+fe[aut_ind[2]])
fe_aut0[fe_aut0==0] = np.nan
fe_aut_sum = np.nansum(fe_aut0)

oxn_season  = np.array([oxn_win_sum,oxn_spr_sum,oxn_sum_sum,oxn_aut_sum])
redn_season = np.array([redn_win_sum,redn_spr_sum,redn_sum_sum,redn_aut_sum])
alk_season  = np.array([alk_win_sum,alk_spr_sum,alk_sum_sum,alk_aut_sum])
fe_season   = np.array([fe_win_sum,fe_spr_sum,fe_sum_sum,fe_aut_sum])

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
# then reshape to (10,12) because this data set is 10 years
# then average over 10 years to get year average
ry0 = 10

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
r_minor_en_in = 287 # index for end of 2013

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
ry1 = 17

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
ocsd_nox_l = list(ocsd_df[3][1:])
for i in range(len(major_nh4[:,2,2])-len(ocsd_df[3][1:])):
    ocsd_nox_l.append(np.nan)

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

p_minor_flo = np.nansum(np.nansum(np.array(minor_flo[:12]),axis=1),axis=1)

# convert to kg/month, then sum months into season
p_minor_tnn = np.nansum(np.nansum(np.array(minor_tn[:12])*np.array(minor_flo[:12]),axis=1),axis=1)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

# sum major and minor potw datasets
p_flo_sum = p_major_flo+p_minor_flo
p_tnn_sum = p_major_tnn+p_minor_tnn

p_season_flo = np.array([(p_flo_sum[11])+(p_flo_sum[1])+(p_flo_sum[0]),(p_flo_sum[2])+(p_flo_sum[3])+(p_flo_sum[4]),(p_flo_sum[5])+(p_flo_sum[6])+(p_flo_sum[7]),(p_flo_sum[8])+(p_flo_sum[9])+(p_flo_sum[10])])

p_season_tnn = np.array([(p_tnn_sum[11])+(p_tnn_sum[1])+(p_tnn_sum[0]),(p_tnn_sum[2])+(p_tnn_sum[3])+(p_tnn_sum[4]),(p_tnn_sum[5])+(p_tnn_sum[6])+(p_tnn_sum[7]),(p_tnn_sum[8])+(p_tnn_sum[9])+(p_tnn_sum[10])])


#p_season_tnn = p_season_tnn*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

#############
# plot
#############
atmo_n_season = (oxn_season+redn_season)*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

# broken y axis plot with kg/day units
savename = './figs/inputs_compare_season_1997_2013.pdf'

seasons = ['Winter','Spring','Summer','Fall']

'''
offset1 = 1000
offset0 = 1000000

# y0: upper lim of bottom axis, y1: lower lim of top axis
y0 = 30000
#y1 = 9500000
y1 = 500000
#y2 = np.max(p_yr_kg)+offset0
y2 = 2E7

figw = 12
figh = 8
width = .2
axis_font = 16

plt.ion()
fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
x_ind = np.arange(len(seasons))
axes[1].bar(x_ind,atmo_n_season,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
axes[0].bar(x_ind,atmo_n_season,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
axes[0].bar(x_ind+width,p_season_tnn,color='orange',width=width,label='All POTWs')
axes[1].bar(x_ind+width,p_season_tnn,color='orange',width=width,label='All POTWs')
axes[0].bar(x_ind+(2*width),r_season_tnn,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
axes[1].bar(x_ind+(2*width),r_season_tnn,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
axes[0].set_xticks([width,1+width,2+width,3+width])
axes[0].set_xticklabels(seasons)

axes[0].set_ylim(y1, y2)
axes[1].set_ylim(0, y0)
axes[1].legend().set_visible(False)

d = .01  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
axes[0].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
axes[0].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=axes[1].transAxes)  # switch to the bottom axes
axes[1].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
axes[1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagona

axes[0].legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)
axes[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes[1].tick_params(axis='both',which='major',labelsize=axis_font)
#fig.add_subplot(111, frameon=False)
## hide tick and tick label of the big axis
#plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
#plt.xlabel('Region')
#plt.ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_font)
axes[0].set_ylabel('Total N Flux kg',fontsize=axis_font)
axes[1].set_xlabel('Season',fontsize=axis_font)
# set top plot to log scale
if log_set == True:
    axes[0].set_yscale('log')
    axes[0].set_ybound(lower=y1,upper=y2)
# put numbers above bars
#axes[0].text(x_ind[-1],a_yr_kg[-1]+10000,str(np.floor(a_yr_kg[-1]).astype(int)),fontsize=12,rotation=90,horizontalalignment='center')
for i in range(len(atmo_n_season)):
    axes[1].text(x_ind[i],atmo_n_season[i]+offset1,format(np.floor(atmo_n_season[i]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

# manually set bars that are too close to border
# or need to go within bar
axes[0].text(x_ind[0]+(2*width),r_season_tnn[0]+offset0-100000,format(np.floor(r_season_tnn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[1]+(2*width),r_season_tnn[1]+(offset0-800000),format(np.floor(r_season_tnn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[2]+(2*width),r_season_tnn[2]+(offset0-900000),format(np.floor(r_season_tnn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[3]+(2*width),r_season_tnn[3]+(offset0-900000),format(np.floor(r_season_tnn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')


axes[0].text(x_ind[0]+(width),p_season_tnn[0]-(offset0*12),format(np.floor(p_season_tnn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[1]+(width),p_season_tnn[1]-(offset0*12),format(np.floor(p_season_tnn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[2]+(width),p_season_tnn[2]-(offset0*11),format(np.floor(p_season_tnn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
axes[0].text(x_ind[3]+(width),p_season_tnn[3]-(offset0*11),format(np.floor(p_season_tnn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

fig.subplots_adjust(hspace=0.1)
'''
figw = 12
figh = 8
width = .2
axis_font = 16

#plt.ion()
#fig,ax = plt.subplots(1,1,sharex=True,figsize=[figw,figh])
#x_ind = np.arange(len(seasons))
#ax.bar(x_ind,atmo_n_season,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
#ax.bar(x_ind+width,p_season_tnn,color='orange',width=width,label='All POTWs')
#ax.bar(x_ind+(2*width),r_season_tnn,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
#ax.set_xticks([width,1+width,2+width,3+width])
#ax.set_xticklabels(seasons)

offset1 = 200000
plt.ion()
fig,ax = plt.subplots(1,1,figsize=[figw,figh])
x_ind = np.arange(len(seasons))
ax.bar(x_ind,atmo_n_season,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
ax.bar(x_ind+width,p_season_tnn,color='orange',width=width,label='All POTWs')
ax.bar(x_ind+(2*width),r_season_tnn,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
ax.set_xticks([width,1+width,2+width,3+width])
ax.set_xticklabels(['Winter','Spring','Summer','Fall'])
#ax.set_yscale('log')
#ax.set_ybound(lower=10E-1,upper=10E5)
ax.set_ybound(lower=0)
ax.set_ylabel('Total N Flux kg per season$',fontsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
#ax.tick_params(axis='both',which='minor',labelsize=axis_font)
ax.legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)
ax.ticklabel_format(style='plain',axis='y')
for i in range(len(atmo_n_season)):
    ax.text(x_ind[i],atmo_n_season[i]+offset1,format(np.floor(atmo_n_season[i]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
    ax.text(x_ind[i]+width,p_season_tnn[i]-(offset1*13),format(np.floor(p_season_tnn[i]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
    ax.text(x_ind[i]+(2*width),r_season_tnn[i]+offset1,format(np.floor(r_season_tnn[i]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

plt.savefig(savename,bbox_inches='tight')
