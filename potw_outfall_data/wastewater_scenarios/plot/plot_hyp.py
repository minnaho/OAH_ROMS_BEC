# plot loads of scenarios

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

major_reg_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/'

norecy_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/excel_pndn_fndn/'

mmols_to_kgd = (86400*14)/(1000*1000)

excel_path = '../'

major_excel_fndn50 = excel_path+'excel_fndn50/major_all_fndn50.xlsx'
minor_excel_fndn50 = excel_path+'excel_fndn50/minor_all_fndn50.xlsx'

major_excel_fndn90 = excel_path+'excel_fndn90/major_all_fndn90.xlsx'
minor_excel_fndn90 = excel_path+'excel_fndn90/minor_all_fndn90.xlsx'
                                                       
major_excel_pndn90 = excel_path+'excel_pndn90/major_all_pndn90.xlsx'
minor_excel_pndn90 = excel_path+'excel_pndn90/minor_all_pndn90.xlsx'
                                                      
major_excel_pndn50 = excel_path+'excel_pndn50/major_all_pndn50.xlsx'
minor_excel_pndn50 = excel_path+'excel_pndn50/minor_all_pndn50.xlsx'

recy_paths_major = [major_excel_fndn50,major_excel_fndn90,major_excel_pndn90,major_excel_pndn50]
recy_paths_minor = [minor_excel_fndn50,minor_excel_fndn90,minor_excel_pndn90,minor_excel_pndn50]

major_excel_fndnno = norecy_path+'major_all_FNDN_norecycle.xlsx'
minor_excel_fndnno = norecy_path+'minor_all_FNDN_norecycle.xlsx'

major_excel_pndnno = norecy_path+'major_all_PNDN_norecycle.xlsx'
minor_excel_pndnno = norecy_path+'minor_all_PNDN_norecycle.xlsx'

no_recy_paths = [ major_excel_fndnno ,minor_excel_fndnno ,major_excel_pndnno ,minor_excel_pndnno]


# last 2 years
mnth = -24

major_sheet_names_recy = pd.ExcelFile(recy_paths_major[0]).sheet_names
minor_sheet_names_recy = pd.ExcelFile(recy_paths_minor[0]).sheet_names

major_excel_reg = major_reg_path+'major_potw_1971_2017_monthly.xlsx'
major_reg = pd.read_excel(major_excel_reg,sheet_name=0)
vol_ef_reg = major_reg['flow m3/s'][mnth:]
nh4_ef_reg = major_reg['NH4 mmol/m3'][mnth:]
no3_ef_reg = major_reg['NO3 mmol/m3'][mnth:]
no2_ef_reg = major_reg['NO2 mmol/m3'][mnth:]
nh4_ld_reg = vol_ef_reg*nh4_ef_reg*mmols_to_kgd
no3_ld_reg = vol_ef_reg*no3_ef_reg*mmols_to_kgd
no2_ld_reg = vol_ef_reg*no2_ef_reg*mmols_to_kgd
din_ld_reg = nh4_ld_reg+no3_ld_reg+no2_ld_reg

major_pndnno = pd.read_excel(major_excel_pndnno,sheet_name=0)
vol_ef_pndnno = major_pndnno['flow final effluent m3/s'][mnth:]
nh4_ef_pndnno = major_pndnno['NH4 mmol/m3'][mnth:]
no3_ef_pndnno = major_pndnno['NO3 mmol/m3'][mnth:]
no2_ef_pndnno = major_pndnno['NO2 mmol/m3'][mnth:]
nh4_ld_pndnno = vol_ef_pndnno*nh4_ef_pndnno*mmols_to_kgd
no3_ld_pndnno = vol_ef_pndnno*no3_ef_pndnno*mmols_to_kgd
no2_ld_pndnno = vol_ef_pndnno*no2_ef_pndnno*mmols_to_kgd
din_ld_pndnno = nh4_ld_pndnno+no3_ld_pndnno+no2_ld_pndnno

major_fndnno = pd.read_excel(major_excel_fndnno,sheet_name=0)
vol_ef_fndnno = major_fndnno['flow final effluent m3/s'][mnth:]
nh4_ef_fndnno = major_fndnno['NH4 mmol/m3'][mnth:]
no3_ef_fndnno = major_fndnno['NO3 mmol/m3'][mnth:]
no2_ef_fndnno = major_fndnno['NO2 mmol/m3'][mnth:]
nh4_ld_fndnno = vol_ef_fndnno*nh4_ef_fndnno*mmols_to_kgd
no3_ld_fndnno = vol_ef_fndnno*no3_ef_fndnno*mmols_to_kgd
no2_ld_fndnno = vol_ef_fndnno*no2_ef_fndnno*mmols_to_kgd
din_ld_fndnno = nh4_ld_fndnno+no3_ld_fndnno+no2_ld_fndnno

major_fndn50 = pd.read_excel(major_excel_fndn50,sheet_name=0)
vol_ef_fndn50 = major_fndn50['flow final effluent m3/s'][mnth:]
nh4_ef_fndn50 = major_fndn50['NH4 mmol/m3'][mnth:]
no3_ef_fndn50 = major_fndn50['NO3 mmol/m3'][mnth:]
no2_ef_fndn50 = major_fndn50['NO2 mmol/m3'][mnth:]
nh4_ld_fndn50 = vol_ef_fndn50*nh4_ef_fndn50*mmols_to_kgd
no3_ld_fndn50 = vol_ef_fndn50*no3_ef_fndn50*mmols_to_kgd
no2_ld_fndn50 = vol_ef_fndn50*no2_ef_fndn50*mmols_to_kgd
din_ld_fndn50 = nh4_ld_fndn50+no3_ld_fndn50+no2_ld_fndn50

major_fndn90 = pd.read_excel(major_excel_fndn90,sheet_name=0)
vol_ef_fndn90 = major_fndn90['flow final effluent m3/s'][mnth:]
nh4_ef_fndn90 = major_fndn90['NH4 mmol/m3'][mnth:]
no3_ef_fndn90 = major_fndn90['NO3 mmol/m3'][mnth:]
no2_ef_fndn90 = major_fndn90['NO2 mmol/m3'][mnth:]
nh4_ld_fndn90 = vol_ef_fndn90*nh4_ef_fndn90*mmols_to_kgd
no3_ld_fndn90 = vol_ef_fndn90*no3_ef_fndn90*mmols_to_kgd
no2_ld_fndn90 = vol_ef_fndn90*no2_ef_fndn90*mmols_to_kgd
din_ld_fndn90 = nh4_ld_fndn90+no3_ld_fndn90+no2_ld_fndn90

major_pndn90 = pd.read_excel(major_excel_pndn90,sheet_name=0)
vol_ef_pndn90 = major_pndn90['flow final effluent m3/s'][mnth:]
nh4_ef_pndn90 = major_pndn90['NH4 mmol/m3'][mnth:]
no3_ef_pndn90 = major_pndn90['NO3 mmol/m3'][mnth:]
no2_ef_pndn90 = major_pndn90['NO2 mmol/m3'][mnth:]
nh4_ld_pndn90 = vol_ef_pndn90*nh4_ef_pndn90*mmols_to_kgd
no3_ld_pndn90 = vol_ef_pndn90*no3_ef_pndn90*mmols_to_kgd
no2_ld_pndn90 = vol_ef_pndn90*no2_ef_pndn90*mmols_to_kgd
din_ld_pndn90 = nh4_ld_pndn90+no3_ld_pndn90+no2_ld_pndn90

major_pndn50 = pd.read_excel(major_excel_pndn50,sheet_name=0)
vol_ef_pndn50 = major_pndn50['flow final effluent m3/s'][mnth:]
nh4_ef_pndn50 = major_pndn50['NH4 mmol/m3'][mnth:]
no3_ef_pndn50 = major_pndn50['NO3 mmol/m3'][mnth:]
no2_ef_pndn50 = major_pndn50['NO2 mmol/m3'][mnth:]
nh4_ld_pndn50 = vol_ef_pndn50*nh4_ef_pndn50*mmols_to_kgd
no3_ld_pndn50 = vol_ef_pndn50*no3_ef_pndn50*mmols_to_kgd
no2_ld_pndn50 = vol_ef_pndn50*no2_ef_pndn50*mmols_to_kgd
din_ld_pndn50 = nh4_ld_pndn50+no3_ld_pndn50+no2_ld_pndn50

plt.ion()
fig,ax = plt.subplots(2,1,figsize=[14,8])
ax[0].plot(major_reg['date'][-24:],vol_ef_reg,label='Current')
ax[0].plot(major_reg['date'][-24:],vol_ef_pndnno,label='PNDN')
ax[0].plot(major_reg['date'][-24:],vol_ef_pndn50,label='PNDN 50')
ax[0].plot(major_reg['date'][-24:],vol_ef_pndn90,label='PNDN 90')
ax[0].plot(major_reg['date'][-24:],vol_ef_fndnno,label='FNDN')
ax[0].plot(major_reg['date'][-24:],vol_ef_fndn50,label='FNDN 50')
ax[0].plot(major_reg['date'][-24:],vol_ef_fndn90,label='FNDN 90')
ax[0].set_ylim(bottom=0)
ax[0].legend(loc='left',fontsize='large')
ax[0].set_ylabel('Flow m3/s',fontsize='14')

ax[1].plot(major_reg['date'][-24:],din_ld_reg,label='Current')
ax[1].plot(major_reg['date'][-24:],din_ld_pndnno,label='PNDN')
ax[1].plot(major_reg['date'][-24:],din_ld_pndn50,label='PNDN 50')
ax[1].plot(major_reg['date'][-24:],din_ld_pndn90,label='PNDN 90')
ax[1].plot(major_reg['date'][-24:],din_ld_fndnno,label='FNDN')
ax[1].plot(major_reg['date'][-24:],din_ld_fndn50,label='FNDN 50')
ax[1].plot(major_reg['date'][-24:],din_ld_fndn90,label='FNDN 90')
ax[1].set_ylim(bottom=0)
ax[1].set_ylabel('DIN kg/day',fontsize='14')


ax[0].tick_params(axis='x',labelsize=14)
ax[0].tick_params(axis='y',labelsize=14)
ax[1].tick_params(axis='x',labelsize=14)
ax[1].tick_params(axis='y',labelsize=14)


'''
for f_i in range(len(recy_paths_major)):
    for s_i in range(len(major_sheet_names)):
        major_df = pd.read_excel(major_excel,major_sheet_names[s_i])
        vol_ef = major_df['flow final effluent m3/s'][mnth:]
        nh4_ef = major_df['NH4 mmol/m3'][mnth:]
        no3_ef = major_df['NO3 mmol/m3'][mnth:]
        no2_ef = major_df['NO2 mmol/m3'][mnth:]
        nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
        no3_ld = vol_ef*no3_ef*mmols_to_kgd
        no2_ld = vol_ef*no2_ef*mmols_to_kgd
'''

