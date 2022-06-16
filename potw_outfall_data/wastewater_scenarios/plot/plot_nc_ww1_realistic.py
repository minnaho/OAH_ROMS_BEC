# plot loads of scenarios
# from netcdf files to check

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num

# set to True if nc changed to 28 month Aug 1 1997 to Nov 31 1999 
nc28 = True

#savepath = './figs/realistic_pndn_recy_'
savepath = './figs/realistic_pndn_'


ncpath = '/data/project1/minnaho/psource/wastewater_scenarios/'

# 2017 loads ww1 during 1997-1998
#ficurren = 'roms_psource_ww1.nc'
ficurren = '/data/project1/minnaho/psource/run_fixjwpcp/roms_psource_102020_full.767.nc'

#fipndnon = 'roms_psource_PNDN_only.nc'
#fifndnon = 'roms_psource_FNDN_only.nc'
fipndnon = 'roms_psource_PNDN_only_realistic.nc'
fifndnon = 'roms_psource_FNDN_only_realistic.nc'
#fipndnon = 'roms_psource_pndn50_realistic.nc'
#fifndnon = 'roms_psource_pndn90_realistic.nc'
#fipndnon = 'roms_psource_fndn50_realistic.nc'
#fifndnon = 'roms_psource_fndn90_realistic.nc'

fipndn50= 'roms_psource_PNDN_only.nc'
fipndn90= 'roms_psource_FNDN_only.nc'
#fifndn50 = 'roms_psource_pndn50.nc'
#fifndn90 = 'roms_psource_pndn90.nc'
fifndn50 = 'roms_psource_fndn50.nc'
fifndn90 = 'roms_psource_fndn90.nc'

mmols_to_kgd = (86400*14)/(1000*1000)

#excel_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/'

# reycle 50 and 90% paths
curren_nc = Dataset(ficurren,'r')

pndnon_nc = Dataset(ncpath+fipndnon,'r')
fndnon_nc = Dataset(ncpath+fifndnon,'r')

pndn50_nc = Dataset(ncpath+fipndn50,'r')
pndn90_nc = Dataset(ncpath+fipndn90,'r')
fndn50_nc = Dataset(ncpath+fifndn50,'r')
fndn90_nc = Dataset(ncpath+fifndn90,'r')
#fndn90_nc = Dataset(fifndn90,'r')

expnames = ['current','pndn_real','fndn_real','pndn','fndn','fndn50','fndn90']
#expnames = ['current','pndn50_real','pndn90_real','pndn','fndn','pndn50','pndn90']
#expnames = ['current','fndn50_real','fndn90_real','pndn','fndn','fndn50','fndn90']

ncfiles = [curren_nc,pndnon_nc,fndnon_nc,pndn50_nc,pndn90_nc,fndn50_nc,fndn90_nc]


################
# files by plant
################

axfont = 16

major_names = ['htp','jwpcp','ocsd','plwtp']

minor_names = ['AlisoCreekOceanOutfall','AvalonWWTF','CampPendleton','CarpinteriaSanitaryDistrictWWTP','ElEsteroWWTF','EncinaOceanOutfall','Fallbrook','GoletaSanitaryDistrict','HaleAveResource','MontecitoSanitaryDistrictWWTF','OceansideOceanOutfall','OxnardWWTP','SanClementeIsland','SanElijoReclamation','SanJuanCreekOutfall','SouthBayInternational','SouthBayReclamation','SummerlandSanitaryDistrict','TerminalIslandWaterReclamation']

htp_st = 0
htp_en = 28

jwp_st = 28
jwp_en = 56

ocs_st = 56
ocs_en = 70

plw_st = 70
plw_en = 96

#dateunit = pndn50_nc.variables['psrc_time'].units
dateunit = 'days since 1994-01-01'
psrc_time = np.array(pndn50_nc.variables['psrc_time'])
dt = num2date(psrc_time,dateunit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# for double checking current day run loading
psrc_time_current = np.array(pndn90_nc.variables['psrc_time'])
dt_current = num2date(psrc_time_current,dateunit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# plot majors
for s_i in range(len(major_names)):
    fig,ax = plt.subplots(2,1,figsize=[12,10])
    ax[0].set_title(major_names[s_i],fontsize=axfont)

    for f_i in range(len(ncfiles)):
        if s_i == 0:
            stp = htp_st
            enp = htp_en
        if s_i == 1:
            stp = jwp_st
            enp = jwp_en
        if s_i == 2:
            stp = ocs_st
            enp = ocs_en
        if s_i == 3:
            stp = plw_st
            enp = plw_en
        vol_ef = np.nansum(np.array(ncfiles[f_i].variables['Qbar'])[stp:enp,:],axis=0)
        nh4_ef = np.array(ncfiles[f_i].variables['NH4'])[stp]
        no3_ef = np.array(ncfiles[f_i].variables['NO3'])[stp]
        no2_ef = np.array(ncfiles[f_i].variables['NO2'])[stp]
        nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
        no3_ld = vol_ef*no3_ef*mmols_to_kgd
        no2_ld = vol_ef*no2_ef*mmols_to_kgd
        din_ld = nh4_ld+no3_ld+no2_ld
        if expnames[f_i] == 'kesfpsource':
            vol_ef = vol_ef[mnth_st:mnth_en]
            din_ld = din_ld[mnth_st:mnth_en]

        # datetime
        dateunit = 'days since 1994-01-01'
        psrc_time = np.array(ncfiles[f_i].variables['psrc_time'])
        dt = num2date(psrc_time,dateunit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)


        # plot
        lname = expnames[f_i]
        if expnames[f_i] == 'kesfpsource':
            ax[0].plot(dt,vol_ef,label=lname,linestyle='--',zorder=10)
        else:
            ax[0].plot(dt,vol_ef,label=lname)
        ax[0].set_ylabel('Flow m$^3$/s',fontsize=axfont)
        if expnames[f_i] == 'kesfpsource':
            ax[1].plot(dt,din_ld,linestyle='--',zorder=10)
        else:
            ax[1].plot(dt,din_ld)
        ax[1].set_ylabel('DIN kg/d',fontsize=axfont)

    ax[0].tick_params(axis='x',labelsize=axfont)
    ax[0].tick_params(axis='y',labelsize=axfont)
    ax[1].tick_params(axis='x',labelsize=axfont)
    ax[1].tick_params(axis='y',labelsize=axfont)
    ax[0].legend(loc='lower center',fontsize=axfont)
    fig.savefig(savepath+major_names[s_i],bbox_inches='tight')
    plt.close('all')

# plot minors
for s_i in range(len(minor_names)):
    fig,ax = plt.subplots(2,1,figsize=[12,10])
    ax[0].set_title(minor_names[s_i],fontsize=axfont)

    for f_i in range(len(ncfiles)):
        vol_ef = np.array(ncfiles[f_i].variables['Qbar'])[plw_en+s_i,:]
        nh4_ef = np.array(ncfiles[f_i].variables['NH4'])[plw_en+s_i]
        no3_ef = np.array(ncfiles[f_i].variables['NO3'])[plw_en+s_i]
        no2_ef = np.array(ncfiles[f_i].variables['NO2'])[plw_en+s_i]
        nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
        no3_ld = vol_ef*no3_ef*mmols_to_kgd
        no2_ld = vol_ef*no2_ef*mmols_to_kgd
        din_ld = nh4_ld+no3_ld+no2_ld

        if expnames[f_i] == 'kesfpsource':
            vol_ef = vol_ef[mnth_st:mnth_en]
            din_ld = din_ld[mnth_st:mnth_en]

        # datetime
        dateunit = 'days since 1994-01-01'
        psrc_time = np.array(ncfiles[f_i].variables['psrc_time'])
        dt = num2date(psrc_time,dateunit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)


        # plot
        lname = expnames[f_i]
        if expnames[f_i] == 'kesfpsource':
            ax[0].plot(dt,vol_ef,label=lname,linestyle='--',zorder=10)
        else:
            ax[0].plot(dt,vol_ef,label=lname)
        ax[0].set_ylabel('Flow m$^3$/s',fontsize=axfont)
        if expnames[f_i] == 'kesfpsource':
            ax[1].plot(dt,din_ld,linestyle='--',zorder=10)
        else:
            ax[1].plot(dt,din_ld)
        ax[1].set_ylabel('DIN kg/d',fontsize=axfont)

    ax[0].tick_params(axis='x',labelsize=axfont)
    ax[0].tick_params(axis='y',labelsize=axfont)
    ax[1].tick_params(axis='x',labelsize=axfont)
    ax[1].tick_params(axis='y',labelsize=axfont)
    ax[0].legend(loc='lower center',fontsize=axfont)
    fig.savefig(savepath+minor_names[s_i],bbox_inches='tight')
    plt.close('all')


