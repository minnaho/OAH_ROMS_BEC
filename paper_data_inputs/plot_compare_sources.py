import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import scipy.io

fig_path = './figs/'
# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_no_watershed_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
setting = 'bight'

################
# load atmos data
################
if setting == 'bight':
    grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
    atmos_data = Dataset(dataset_name,'r')

    grid_nc = Dataset(grid_path,'r')
    lat_nc = np.array(grid_nc.variables['lat_rho'])
    lon_nc = np.array(grid_nc.variables['lon_rho'])
    mask_nc = np.array(grid_nc.variables['mask_rho'])

    oxn = atmos_data.variables['NH4']
    redn = atmos_data.variables['NO3']
    alk = atmos_data.variables['alk']
    fe = atmos_data.variables['fe']

if setting == 'cal':
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/atmos_deposition_CMAQ_2002_2012.nc'
    atmos_data = Dataset(dataset_name,'r')

    lat_nc = np.array(atmos_data.variables['latitude'])
    lon_nc = np.array(atmos_data.variables['longitude'])

    oxn = atmos_data.variables['oxidized_nitrogen']
    redn = atmos_data.variables['reduced_nitrogen']
    alk = atmos_data.variables['alkalinity']
    fe = atmos_data.variables['iron']


# load per season (add up each 3 months in season) then sum over entire region 
if setting == 'bight':
    mat = scipy.io.loadmat('../maskt.mat') 
    m2_to_hectare = 10000
    oxn_season  = np.empty((4))
    redn_season = np.empty((4))
    alk_season  = np.empty((4))
    fe_season   = np.empty((4))

    oxn_win0 = np.array(oxn[11]+oxn[0]+oxn[1])*mask_nc*mat['maskt']*m2_to_hectare
    oxn_win0[oxn_win0==0] = np.nan
    oxn_winter = np.nansum(oxn_win0)

    oxn_spr0 = np.array(oxn[2]+oxn[3]+oxn[4])*mask_nc*mat['maskt']*m2_to_hectare
    oxn_spr0[oxn_spr0==0] = np.nan
    oxn_spring = np.nansum(oxn_spr0)

    oxn_sum0 = np.array(oxn[5]+oxn[6]+oxn[7])*mask_nc*mat['maskt']*m2_to_hectare
    oxn_sum0[oxn_sum0==0] = np.nan
    oxn_summer = np.nansum(oxn_sum0)

    oxn_aut0 = np.array(oxn[8]+oxn[9]+oxn[10])*mask_nc*mat['maskt']*m2_to_hectare
    oxn_aut0[oxn_aut0==0] = np.nan
    oxn_autumn = np.nansum(oxn_aut0)

    fe_win0 = np.array(fe[11]+fe[0]+fe[1])*mask_nc*mat['maskt']*m2_to_hectare
    fe_win0[fe_win0==0] = np.nan
    fe_winter = np.nansum(fe_win0)

    fe_spr0 = np.array(fe[2]+fe[3]+fe[4])*mask_nc*mat['maskt']*m2_to_hectare
    fe_spr0[fe_spr0==0] = np.nan
    fe_spring = np.nansum(fe_spr0)

    fe_sum0 = np.array(fe[5]+fe[6]+fe[7])*mask_nc*mat['maskt']*m2_to_hectare
    fe_sum0[fe_sum0==0] = np.nan
    fe_summer = np.nansum(fe_sum0)

    fe_aut0 = np.array(fe[8]+fe[9]+fe[10])*mask_nc*mat['maskt']*m2_to_hectare
    fe_aut0[fe_aut0==0] = np.nan
    fe_autumn = np.nansum(fe_aut0)

    alk_win0 = np.array(alk[11]+alk[0]+alk[1])*mask_nc*mat['maskt']*m2_to_hectare
    alk_win0[alk_win0==0] = np.nan
    alk_winter = np.nansum(alk_win0)

    alk_spr0 = np.array(alk[2]+alk[3]+alk[4])*mask_nc*mat['maskt']*m2_to_hectare
    alk_spr0[alk_spr0==0] = np.nan
    alk_spring = np.nansum(alk_spr0)

    alk_sum0 = np.array(alk[5]+alk[6]+alk[7])*mask_nc*mat['maskt']*m2_to_hectare
    alk_sum0[alk_sum0==0] = np.nan
    alk_summer = np.nansum(alk_sum0)

    alk_aut0 = np.array(alk[8]+alk[9]+alk[10])*mask_nc*mat['maskt']*m2_to_hectare
    alk_aut0[alk_aut0==0] = np.nan
    alk_autumn = np.nansum(alk_aut0)

    redn_win0 = np.array(redn[11]+redn[0]+redn[1])*mask_nc*mat['maskt']*m2_to_hectare
    redn_win0[redn_win0==0] = np.nan
    redn_winter = np.nansum(redn_win0)

    redn_spr0 = np.array(redn[2]+redn[3]+redn[4])*mask_nc*mat['maskt']*m2_to_hectare
    redn_spr0[redn_spr0==0] = np.nan
    redn_spring = np.nansum(redn_spr0)

    redn_sum0 = np.array(redn[5]+redn[6]+redn[7])*mask_nc*mat['maskt']*m2_to_hectare
    redn_sum0[redn_sum0==0] = np.nan
    redn_summer = np.nansum(redn_sum0)

    redn_aut0 = np.array(redn[8]+redn[9]+redn[10])*mask_nc*mat['maskt']*m2_to_hectare
    redn_aut0[redn_aut0==0] = np.nan
    redn_autumn = np.nansum(redn_aut0)

    oxn_season  = np.array([oxn_winter,oxn_spring,oxn_summer,oxn_autumn])
    redn_season = np.array([redn_winter,redn_spring,redn_summer,redn_autumn])
    alk_season  = np.array([alk_winter,alk_spring,alk_summer,alk_autumn])
    fe_season   = np.array([fe_winter,fe_spring,fe_summer,fe_autumn])

if setting == 'cal': 
    oxn_monthly = np.empty((12,oxn.shape[1],oxn.shape[2]))
    for m_i in range(12):
        oxn_monthly[m_i] = np.nanmean(oxn[m_i::12,:,:])
        
        

###############
# river major data (10 yrs)
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
# river 24 yrs
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
figw = 12
figh = 8
axis_tick_font = 10
#major_names = ['HTP','JWPCP','OCSD','PLWTP']
#major_linesty = ['-','--','-.',':']
lw = 2

# combine rivers 10 yrs and 24 yrs
# find days at beginning and end  
num_st = major_time_dt[0]-minor_time_dt[0]
num_en = minor_time_dt[-1]-major_time_dt[-1]

a = []
b = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_tn[num_st.days:-num_en.days,m_i,m_i])
    b.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_po4[num_st.days:-num_en.days,m_i,m_i])
# a,b shape (24,3650)
# sum up all rivers
minor_fluxn = np.nansum(np.array(a),axis=0)
minor_fluxp = np.nansum(np.array(b),axis=0)
minor_flo_short = np.nansum(np.nansum(minor_flo[num_st.days:-num_en.days,:,:],axis=1),axis=1)

a = []
b = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])
    b.append(major_flo[:,m_i,m_i]*major_po4[:,m_i,m_i])

# sum up all rivers
major_fluxn = np.nansum(np.array(a),axis=0)
major_fluxp = np.nansum(np.array(b),axis=0)
major_flo_sum = np.nansum(np.nansum(major_flo[:,:,:],axis=1),axis=1)

r_flo = major_flo_sum+minor_flo_short
r_fluxn = major_fluxn+minor_fluxn
r_fluxp = major_fluxp+minor_fluxp # mmol/s

# find indices for each season
r_1 = []
r_2 = []
r_3 = []
r_4 = []
r_5 = []
r_6 = []
r_7 = []
r_8 = []
r_9 = []
r_10 = []
r_11 = []
r_12 = []
for d_i in range(len(major_time_dt)):
    if major_time_dt[d_i].month == 1:  
        r_1.append(d_i)
    if major_time_dt[d_i].month == 2:  
        r_2.append(d_i)
    if major_time_dt[d_i].month == 3:  
        r_3.append(d_i)
    if major_time_dt[d_i].month == 4:  
        r_4.append(d_i)
    if major_time_dt[d_i].month == 5:  
        r_5.append(d_i)
    if major_time_dt[d_i].month == 6:  
        r_6.append(d_i)
    if major_time_dt[d_i].month == 7:  
        r_7.append(d_i)
    if major_time_dt[d_i].month == 8:  
        r_8.append(d_i)
    if major_time_dt[d_i].month == 9:  
        r_9.append(d_i)
    if major_time_dt[d_i].month == 10:  
        r_10.append(d_i)
    if major_time_dt[d_i].month == 11:  
        r_11.append(d_i)
    if major_time_dt[d_i].month == 12:  
        r_12.append(d_i)

r_months_ind = [r_1,r_2,r_3,r_4,r_5,r_6,r_7,r_8,r_9,r_10,r_11,r_12]

r_flo_mon = np.empty((12))
r_n_mon = np.empty((12))
r_p_mon = np.empty((12))
for r_i in range(len(r_months_ind)):
    r_n_mon[r_i] = np.nanmean(r_fluxn[r_i])
    r_p_mon[r_i] = np.nanmean(r_fluxp[r_i])
    r_flo_mon[r_i] = np.nanmean(r_flo[r_i])

np.save('river_monthly_flo_all.npy',r_flo_mon)
np.save('river_monthly_nflux_all.npy',r_n_mon)
np.save('river_monthly_pflux_all.npy',r_p_mon)
    
r_season_n = np.array([(r_n_mon[11])+(r_n_mon[1])+(r_n_mon[0]),(r_n_mon[2])+(r_n_mon[3])+(r_n_mon[4]),(r_n_mon[5])+(r_n_mon[6])+(r_n_mon[7]),(r_n_mon[8])+(r_n_mon[9])+(r_n_mon[10])])

r_season_p = np.array([(r_p_mon[11])+(r_p_mon[1])+(r_p_mon[0]),(r_p_mon[2])+(r_p_mon[3])+(r_p_mon[4]),(r_p_mon[5])+(r_p_mon[6])+(r_p_mon[7]),(r_p_mon[8])+(r_p_mon[9])+(r_p_mon[10])])
   
##################
# potws
##################
potw_ma_nc = Dataset(potw_major_path,'r')
potw_mi_nc = Dataset(potw_minor_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l)


major_potw_flo = np.array(potw_ma_nc.variables['flow']) # m3/s
major_potw_nh4 = np.array(potw_ma_nc.variables['NH4']) # mmol/m3
major_potw_no3 = np.array(potw_ma_nc.variables['NO3']) # mmol/m3
major_potw_no2 = np.array(potw_ma_nc.variables['NO2']) # mmol/m3
major_potw_po4 = np.array(potw_ma_nc.variables['PO4']) # mmol/m3

minor_potw_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_potw_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_potw_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_potw_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_potw_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

major_potw_tn = major_potw_no3+major_potw_nh4+major_potw_no2

major_potw_flo[major_potw_flo>1E20] = np.nan
major_potw_tn[major_potw_tn>1E20] = np.nan
major_potw_po4[major_potw_po4>1E20] = np.nan
major_potw_allf = np.nansum(np.nansum(major_potw_flo,axis=1),axis=1)
major_potw_alln = np.nansum(np.nansum(major_potw_tn,axis=1),axis=1)
major_potw_allp = np.nansum(np.nansum(major_potw_po4,axis=1),axis=1)

minor_potw_tn = minor_potw_no3+minor_potw_nh4+minor_potw_no2

minor_potw_flo[minor_potw_flo>1E20] = np.nan
minor_potw_tn[minor_potw_tn>1E20] = np.nan
minor_potw_po4[minor_potw_po4>1E20] = np.nan
minor_potw_allf = np.nansum(np.nansum(minor_potw_flo,axis=1),axis=1)
minor_potw_alln = np.nansum(np.nansum(minor_potw_tn,axis=1),axis=1)
minor_potw_allp = np.nansum(np.nansum(minor_potw_po4,axis=1),axis=1)

# loads of all potws
a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_tn[:,m_i,m_i])
major_potw_fluxalln = np.nansum(np.array(a),axis=0)

a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_po4[:,m_i,m_i])
major_potw_fluxallp = np.nansum(np.array(a),axis=0)

# already in monthly clim
iend_minor = 12
a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_tn[:iend_minor,m_i,m_i])
minor_potw_fluxalln = np.nansum(np.array(a),axis=0)

a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_po4[:iend_minor,m_i,m_i])
minor_potw_fluxallp = np.nansum(np.array(a),axis=0)


# find indices for each season
r_potw_1 = []
r_potw_2 = []
r_potw_3 = []
r_potw_4 = []
r_potw_5 = []
r_potw_6 = []
r_potw_7 = []
r_potw_8 = []
r_potw_9 = []
r_potw_10 = []
r_potw_11 = []
r_potw_12 = []
for d_i in range(len(major_potw_time_dt)):
    if major_potw_time_dt[d_i].month == 1:  
        r_potw_1.append(d_i)
    if major_potw_time_dt[d_i].month == 2:  
        r_potw_2.append(d_i)
    if major_potw_time_dt[d_i].month == 3:  
        r_potw_3.append(d_i)
    if major_potw_time_dt[d_i].month == 4:  
        r_potw_4.append(d_i)
    if major_potw_time_dt[d_i].month == 5:  
        r_potw_5.append(d_i)
    if major_potw_time_dt[d_i].month == 6:  
        r_potw_6.append(d_i)
    if major_potw_time_dt[d_i].month == 7:  
        r_potw_7.append(d_i)
    if major_potw_time_dt[d_i].month == 8:  
        r_potw_8.append(d_i)
    if major_potw_time_dt[d_i].month == 9:  
        r_potw_9.append(d_i)
    if major_potw_time_dt[d_i].month == 10:  
        r_potw_10.append(d_i)
    if major_potw_time_dt[d_i].month == 11:  
        r_potw_11.append(d_i)
    if major_potw_time_dt[d_i].month == 12:  
        r_potw_12.append(d_i)


potw_months_ind = [r_potw_1,r_potw_2,r_potw_3,r_potw_4,r_potw_5,r_potw_6,r_potw_7,r_potw_8,r_potw_9,r_potw_10,r_potw_11,r_potw_12]

potw_flo_mon = np.empty((12))
potw_n_mon = np.empty((12))
potw_p_mon = np.empty((12))
for r_i in range(len(potw_months_ind)):
    potw_n_mon[r_i] = np.nanmean(major_potw_fluxalln[r_i])
    potw_p_mon[r_i] = np.nanmean(major_potw_fluxallp[r_i])
    
major_potw_season_n = np.array([(potw_n_mon[11])+(potw_n_mon[1])+(potw_n_mon[0]),(potw_n_mon[2])+(potw_n_mon[3])+(potw_n_mon[4]),(potw_n_mon[5])+(potw_n_mon[6])+(potw_n_mon[7]),(potw_n_mon[8])+(potw_n_mon[9])+(potw_n_mon[10])])

major_potw_season_p = np.array([(potw_p_mon[11])+(potw_p_mon[1])+(potw_p_mon[0]),(potw_p_mon[2])+(potw_p_mon[3])+(potw_p_mon[4]),(potw_p_mon[5])+(potw_p_mon[6])+(potw_p_mon[7]),(potw_p_mon[8])+(potw_p_mon[9])+(potw_p_mon[10])])

all_potw_n_mon = potw_n_mon+minor_potw_fluxalln
all_potw_p_mon = potw_p_mon+minor_potw_fluxallp

all_potw_season_n = np.array([(all_potw_n_mon[11])+(all_potw_n_mon[1])+(all_potw_n_mon[0]),(all_potw_n_mon[2])+(all_potw_n_mon[3])+(all_potw_n_mon[4]),(all_potw_n_mon[5])+(all_potw_n_mon[6])+(all_potw_n_mon[7]),(all_potw_n_mon[8])+(all_potw_n_mon[9])+(all_potw_n_mon[10])])

all_potw_season_p = np.array([(all_potw_p_mon[11])+(all_potw_p_mon[1])+(all_potw_p_mon[0]),(all_potw_p_mon[2])+(all_potw_p_mon[3])+(all_potw_p_mon[4]),(all_potw_p_mon[5])+(all_potw_p_mon[6])+(all_potw_p_mon[7]),(all_potw_p_mon[8])+(all_potw_p_mon[9])+(all_potw_p_mon[10])])

#############
# plot
#############
atmo_n_season = oxn_season+redn_season

figw = 12
figh = 8
seasons = ['Winter','Spring','Summer','Fall']
width = 0.15
axis_font = 18
#savename = './figs/inputs_compare_nolog.pdf'
#savename = './figs/inputs_compare.png'
savename = './figs/inputs_compare.pdf'

plt.ion()
fig,ax = plt.subplots(1,1,figsize=[figw,figh])
x_ind = np.arange(len(seasons))
ax.bar(x_ind,atmo_n_season,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
ax.bar(x_ind+width,all_potw_season_n,color='orange',width=width,label='All POTWs')
ax.bar(x_ind+(2*width),r_season_n,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
ax.set_xticks([width,1+width,2+width,3+width])
ax.set_xticklabels(['Winter','Spring','Summer','Fall'])
ax.set_yscale('log')
ax.set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
#ax.tick_params(axis='both',which='minor',labelsize=axis_font)
ax.legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)

plt.savefig(savename,bbox_inches='tight')



