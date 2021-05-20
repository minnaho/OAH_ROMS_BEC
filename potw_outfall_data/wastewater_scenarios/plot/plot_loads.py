# plot loads of scenarios

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

major_reg_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/'
minor_reg_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/'

savepath = './figs/'

# contains PNDN and FNDN only scenarios for all plants EXCEPT ocsd and terminal island
pndnfndn_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/excel_pndn_fndn/'

# contains ocsd and terminal island PNDN and FNDN only
norecy_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/excel_final_pndn_fndn/'

mmols_to_kgd = (86400*14)/(1000*1000)

excel_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/'

# reycle 50 and 90% paths
major_excel_fndn50 = excel_path+'excel_fndn50/major_all_fndn50.xlsx'
minor_excel_fndn50 = excel_path+'excel_fndn50/minor_all_fndn50.xlsx'

major_excel_fndn90 = excel_path+'excel_fndn90/major_all_fndn90.xlsx'
minor_excel_fndn90 = excel_path+'excel_fndn90/minor_all_fndn90.xlsx'
                                                       
major_excel_pndn90 = excel_path+'excel_pndn90/major_all_pndn90.xlsx'
minor_excel_pndn90 = excel_path+'excel_pndn90/minor_all_pndn90.xlsx'
                                                      
major_excel_pndn50 = excel_path+'excel_pndn50/major_all_pndn50.xlsx'
minor_excel_pndn50 = excel_path+'excel_pndn50/minor_all_pndn50.xlsx'

# PNDN and FNDN only for all plants except ocsd and ti
major_excel_fndnno = pndnfndn_path+'major_all_FNDN_norecycle.xlsx'
minor_excel_fndnno = pndnfndn_path+'minor_all_FNDN_norecycle.xlsx'

major_excel_pndnno = pndnfndn_path+'major_all_PNDN_norecycle.xlsx'
minor_excel_pndnno = pndnfndn_path+'minor_all_PNDN_norecycle.xlsx'


# only OCSD and Terminal Island PNDN/FNDN
major_excel_fndnre = norecy_path+'major_all_FNDN_final.xlsx'
minor_excel_fndnre = norecy_path+'minor_all_FNDN_final.xlsx'

major_excel_pndnre = norecy_path+'major_all_PNDN_final.xlsx'
minor_excel_pndnre = norecy_path+'minor_all_PNDN_final.xlsx'

# PNDN and FNDN only for all plants except ocsd and ti
ndn_paths_major = [major_excel_fndnno,major_excel_pndnno]
ndn_paths_minor = [minor_excel_fndnno,minor_excel_pndnno]

# only OCSD and Terminal Island PNDN/FNDN
nore_paths_major = [major_excel_fndnre,major_excel_pndnre]
nore_paths_minor = [minor_excel_fndnre,minor_excel_pndnre]

# reycle 50 and 90% paths
recy_paths_major = [major_excel_fndn50,major_excel_fndn90,major_excel_pndn90,major_excel_pndn50]
recy_paths_minor = [minor_excel_fndn50,minor_excel_fndn90,minor_excel_pndn90,minor_excel_pndn50]

major_excel_reg = major_reg_path+'major_potw_1971_2017_monthly.xlsx'

minor_excel_reg = minor_reg_path+'minor_potw_1997_2017_monthly.xlsx'

################
# files by plant
################

# majors without ocsd
major_path = [major_excel_fndnno,major_excel_pndnno,major_excel_fndn50,major_excel_fndn90,major_excel_pndn90,major_excel_pndn50]

# minors without ocsd
minor_path = [minor_excel_fndnno,minor_excel_pndnno,minor_excel_fndn50,minor_excel_fndn90,minor_excel_pndn90,minor_excel_pndn50]

#  ocsd
ocsd_path = [major_excel_fndnre,major_excel_pndnre,major_excel_fndn50,major_excel_fndn90,major_excel_pndn90,major_excel_pndn50]

#  term
term_path = [minor_excel_fndnre,minor_excel_pndnre,minor_excel_fndn50,minor_excel_fndn90,minor_excel_pndn90,minor_excel_pndn50]

# last 2 years
mnth = -20

axfont = 16

# plot majors
sheetnames = pd.ExcelFile(major_path[0]).sheet_names
for s_i in range(len(sheetnames)):
    if sheetnames[s_i] != 'ocsd':
        fig,ax = plt.subplots(2,1,figsize=[12,10])
        ax[0].set_title(sheetnames[s_i],fontsize=axfont)

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

        for f_i in range(len(major_path)):
            df = pd.read_excel(major_path[f_i],sheetnames[s_i])
            try:
                vol_ef = df['flow m3/s'][mnth:]
            except:
                vol_ef = df['flow final effluent m3/s'][mnth:]
            dt = df['date'][mnth:]
            nh4_ef = df['NH4 mmol/m3'][mnth:]
            no3_ef = df['NO3 mmol/m3'][mnth:]
            no2_ef = df['NO2 mmol/m3'][mnth:]
            nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
            no3_ld = vol_ef*no3_ef*mmols_to_kgd
            no2_ld = vol_ef*no2_ef*mmols_to_kgd
            din_ld = nh4_ld+no3_ld+no2_ld

            # plot
            if len(major_path[f_i]) < 100:
                lname = major_path[f_i][major_path[f_i].index('.')-6:major_path[f_i].index('.')]
            if len(major_path[f_i]) > 100:
                lname = major_path[f_i][88:88+4]
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
        fig.savefig(savepath+sheetnames[s_i],bbox_inches='tight')
        plt.close('all')


# plot ocsd
# current loads
s_i = 'ocsd'
fig,ax = plt.subplots(2,1,figsize=[12,10])
ax[0].set_title(s_i,fontsize=axfont)
major_reg = pd.read_excel(major_excel_reg,sheet_name=s_i)
vol_ef_reg = major_reg['flow m3/s'][mnth:]
nh4_ef_reg = major_reg['NH4 mmol/m3'][mnth:]
no3_ef_reg = major_reg['NO3 mmol/m3'][mnth:]
no2_ef_reg = major_reg['NO2 mmol/m3'][mnth:]
nh4_ld_reg = vol_ef_reg*nh4_ef_reg*mmols_to_kgd
no3_ld_reg = vol_ef_reg*no3_ef_reg*mmols_to_kgd
no2_ld_reg = vol_ef_reg*no2_ef_reg*mmols_to_kgd
din_ld_reg = nh4_ld_reg+no3_ld_reg+no2_ld_reg

for f_i in range(len(ocsd_path)):
    df = pd.read_excel(ocsd_path[f_i],sheet_name=s_i)
    try:
        vol_ef = df['flow m3/s'][mnth:]
    except:
        vol_ef = df['flow final effluent m3/s'][mnth:]
    dt = df['date'][mnth:]
    nh4_ef = df['NH4 mmol/m3'][mnth:]
    no3_ef = df['NO3 mmol/m3'][mnth:]
    no2_ef = df['NO2 mmol/m3'][mnth:]
    nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
    no3_ld = vol_ef*no3_ef*mmols_to_kgd
    no2_ld = vol_ef*no2_ef*mmols_to_kgd
    din_ld = nh4_ld+no3_ld+no2_ld

    # plot
    if len(ocsd_path[f_i]) > 100:
        lname = ocsd_path[f_i][ocsd_path[f_i].index('.')-10:ocsd_path[f_i].index('.')-6]
    if len(ocsd_path[f_i]) < 100:
        lname = ocsd_path[f_i][85:85+6]
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
fig.savefig(savepath+s_i,bbox_inches='tight')



# plot minors
sheetnames = pd.ExcelFile(minor_path[0]).sheet_names
for s_i in range(len(sheetnames)):
    if sheetnames[s_i] != 'TerminalIslandWaterReclamation':
        fig,ax = plt.subplots(2,1,figsize=[12,10])
        ax[0].set_title(sheetnames[s_i],fontsize=axfont)

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

        for f_i in range(len(minor_path)):
            df = pd.read_excel(minor_path[f_i],sheetnames[s_i])
            try:
                vol_ef = df['flow m3/s'][mnth:]
            except:
                vol_ef = df['flow final effluent m3/s'][mnth:]
            dt = df['date'][mnth:]
            nh4_ef = df['NH4 mmol/m3'][mnth:]
            no3_ef = df['NO3 mmol/m3'][mnth:]
            no2_ef = df['NO2 mmol/m3'][mnth:]
            nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
            no3_ld = vol_ef*no3_ef*mmols_to_kgd
            no2_ld = vol_ef*no2_ef*mmols_to_kgd
            din_ld = nh4_ld+no3_ld+no2_ld

            # plot
            if len(minor_path[f_i]) < 100:
                lname = minor_path[f_i][minor_path[f_i].index('.')-6:minor_path[f_i].index('.')]
            if len(minor_path[f_i]) > 100:
                lname = minor_path[f_i][88:88+4]
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
        fig.savefig(savepath+sheetnames[s_i],bbox_inches='tight')
        plt.close('all')


# plot term
# current loads
s_i = 'TerminalIslandWaterReclamation'
fig,ax = plt.subplots(2,1,figsize=[12,10])
ax[0].set_title(s_i,fontsize=axfont)
minor_reg = pd.read_excel(minor_excel_reg,sheet_name=s_i)
vol_ef_reg = minor_reg['flow m3/s'][mnth:]
nh4_ef_reg = minor_reg['NH4 mmol/m3'][mnth:]
no3_ef_reg = minor_reg['NO3 mmol/m3'][mnth:]
no2_ef_reg = minor_reg['NO2 mmol/m3'][mnth:]
nh4_ld_reg = vol_ef_reg*nh4_ef_reg*mmols_to_kgd
no3_ld_reg = vol_ef_reg*no3_ef_reg*mmols_to_kgd
no2_ld_reg = vol_ef_reg*no2_ef_reg*mmols_to_kgd
din_ld_reg = nh4_ld_reg+no3_ld_reg+no2_ld_reg

for f_i in range(len(term_path)):
    df = pd.read_excel(term_path[f_i],sheet_name=s_i)
    try:
        vol_ef = df['flow m3/s'][mnth:]
    except:
        vol_ef = df['flow final effluent m3/s'][mnth:]
    dt = df['date'][mnth:]
    nh4_ef = df['NH4 mmol/m3'][mnth:]
    no3_ef = df['NO3 mmol/m3'][mnth:]
    no2_ef = df['NO2 mmol/m3'][mnth:]
    nh4_ld = vol_ef*nh4_ef*mmols_to_kgd
    no3_ld = vol_ef*no3_ef*mmols_to_kgd
    no2_ld = vol_ef*no2_ef*mmols_to_kgd
    din_ld = nh4_ld+no3_ld+no2_ld

    # plot
    if len(term_path[f_i]) > 100:
        lname = term_path[f_i][term_path[f_i].index('.')-10:term_path[f_i].index('.')-6]
    if len(term_path[f_i]) < 100:
        lname = term_path[f_i][85:85+6]
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
fig.savefig(savepath+s_i,bbox_inches='tight')

'''



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
