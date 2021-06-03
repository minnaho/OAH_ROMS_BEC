# plot loads of scenarios
# from netcdf files to check

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num

major_reg_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/'
minor_reg_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/'

savepath = './figs/'


ncpath = '/data/project1/minnaho/psource/wastewater_scenarios/'

fipndnon = 'roms_psource_PNDN_only.nc'
fifndnon = 'roms_psource_FNDN_only.nc'

fipndn50 = 'roms_psource_pndn50.nc'
fipndn90 = 'roms_psource_pndn90.nc'
fifndn50 = 'roms_psource_fndn50.nc'
fifndn90 = 'roms_psource_fndn90.nc'


## contains PNDN and FNDN only scenarios for all plants EXCEPT ocsd and terminal island
#pndnfndn_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/excel_pndn_fndn/'
#
## contains ocsd and terminal island PNDN and FNDN only
#norecy_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/excel_final_pndn_fndn/'

mmols_to_kgd = (86400*14)/(1000*1000)

#excel_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/'

# reycle 50 and 90% paths
pndnon_nc = Dataset(ncpath+fipndnon,'r')
fndnon_nc = Dataset(ncpath+fifndnon,'r')

pndn50_nc = Dataset(ncpath+fipndn50,'r')
pndn90_nc = Dataset(ncpath+fipndn90,'r')
fndn50_nc = Dataset(ncpath+fifndn50,'r')
fndn90_nc = Dataset(ncpath+fifndn90,'r')

ncfiles = [pndnon_nc,fndnon_nc,pndn50_nc,pndn90_nc,fndn50_nc,fndn90_nc]

expnames = ['pndn','fndn','pndn50','pndn90','fndn50','fndn90']

major_excel_reg = major_reg_path+'major_potw_1971_2017_monthly.xlsx'
minor_excel_reg = minor_reg_path+'minor_potw_1997_2017_monthly.xlsx'
mnth = -12


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

dateunit = pndn50_nc.variables['psrc_time'].units
psrc_time = np.array(pndn50_nc.variables['psrc_time'])
dt = num2date(psrc_time,dateunit,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# plot majors
for s_i in range(len(major_names)):
    fig,ax = plt.subplots(2,1,figsize=[12,10])
    ax[0].set_title(major_names[s_i],fontsize=axfont)

    # current loads
    major_reg = pd.read_excel(major_excel_reg,sheet_name=s_i)
    vol_ef_reg = major_reg['flow m3/s'][mnth:]
    nh4_ef_reg = major_reg['NH4 mmol/m3'][mnth:]
    no3_ef_reg = major_reg['NO3 mmol/m3'][mnth:]
    no2_ef_reg = major_reg['NO2 mmol/m3'][mnth:]
    nh4_ld_reg = vol_ef_reg*nh4_ef_reg*mmols_to_kgd
    no3_ld_reg = vol_ef_reg*no3_ef_reg*mmols_to_kgd
    no2_ld_reg = vol_ef_reg*no2_ef_reg*mmols_to_kgd
    din_ld_reg = nh4_ld_reg+no3_ld_reg+no2_ld_reg

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

        # plot
        lname = expnames[f_i]
        ax[0].plot(dt,vol_ef,label=lname)
        ax[0].set_ylabel('Flow m$^3$/s',fontsize=axfont)
        ax[1].plot(dt,din_ld)
        ax[1].set_ylabel('DIN kg/d',fontsize=axfont)

    ax[0].plot(dt,vol_ef_reg,label='Current')
    ax[1].plot(dt,din_ld_reg,label='Current')
    ax[0].tick_params(axis='x',labelsize=axfont)
    ax[0].tick_params(axis='y',labelsize=axfont)
    ax[1].tick_params(axis='x',labelsize=axfont)
    ax[1].tick_params(axis='y',labelsize=axfont)
    ax[0].legend(loc='center left',fontsize=axfont)
    fig.savefig(savepath+major_names[s_i],bbox_inches='tight')
    plt.close('all')

# plot minors
for s_i in range(len(minor_names)):
    fig,ax = plt.subplots(2,1,figsize=[12,10])
    ax[0].set_title(minor_names[s_i],fontsize=axfont)

    # current loads
    minor_reg = pd.read_excel(minor_excel_reg,sheet_name=s_i)
    vol_ef_reg = minor_reg['flow m3/s'][mnth:]
    nh4_ef_reg = minor_reg['NH4 mmol/m3'][mnth:]
    no3_ef_reg = minor_reg['NO3 mmol/m3'][mnth:]
    no2_ef_reg = minor_reg['NO2 mmol/m3'][mnth:]
    nh4_ld_reg = vol_ef_reg*nh4_ef_reg*mmols_to_kgd
    no3_ld_reg = vol_ef_reg*no3_ef_reg*mmols_to_kgd
    no2_ld_reg = vol_ef_reg*no2_ef_reg*mmols_to_kgd
    din_ld_reg = nh4_ld_reg+no3_ld_reg+no2_ld_reg

    for f_i in range(len(ncfiles)):
        vol_ef = np.array(ncfiles[f_i].variables['Qbar'])[plw_en+s_i,:]
        nh4_ef = np.array(ncfiles[f_i].variables['NH4'])[plw_en+s_i]
        no3_ef = np.array(ncfiles[f_i].variables['NO3'])[plw_en+s_i]
        no2_ef = np.array(ncfiles[f_i].variables['NO2'])[plw_en+s_i]
        nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
        no3_ld = vol_ef*no3_ef*mmols_to_kgd
        no2_ld = vol_ef*no2_ef*mmols_to_kgd
        din_ld = nh4_ld+no3_ld+no2_ld

        # plot
        lname = expnames[f_i]
        ax[0].plot(dt,vol_ef,label=lname)
        ax[0].set_ylabel('Flow m$^3$/s',fontsize=axfont)
        ax[1].plot(dt,din_ld)
        ax[1].set_ylabel('DIN kg/d',fontsize=axfont)

    ax[0].plot(dt,vol_ef_reg,label='Current')
    ax[1].plot(dt,din_ld_reg,label='Current')
    ax[0].tick_params(axis='x',labelsize=axfont)
    ax[0].tick_params(axis='y',labelsize=axfont)
    ax[1].tick_params(axis='x',labelsize=axfont)
    ax[1].tick_params(axis='y',labelsize=axfont)
    ax[0].legend(loc='center left',fontsize=axfont)
    fig.savefig(savepath+minor_names[s_i],bbox_inches='tight')
    plt.close('all')


