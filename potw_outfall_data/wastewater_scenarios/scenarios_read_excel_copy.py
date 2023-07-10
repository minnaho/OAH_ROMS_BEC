# calculate effluent constiutent values 
# and RO reject values based on
# water treatment recovery efficiency
# % TIN removal
# water recycling goals
import numpy as np
import pandas as pd

######################
# CHOICES of recycling
######################
# choose PNDN or FNDN
treat_type = 'PNDN'

# percent of influent going to recycling treatment plant
# set both of these to the same
per_re = .5
per_re_st = .5
#per_re = .9

# water recovery efficiency
rec_eff = 0.8

# DIN percent removal (rest goes to RO permeate)
nh4_rem = .95
no3_rem = .85
no2_rem = .85

# all other constituent removal
# salt, iron, and organic matter 100% removed
# DO concentration kept the same
sal_rem = 1 # .96 instead?
dfe_rem = 1
tfe_rem = 1
#bod_rem = 1
toc_rem = 0.97
onn_rem = 0.97
opp_rem = 0.97
po4_rem = 0.95
sil_rem = 0.95
alk_rem = 0.95

# excel folder with PNDN and FNDN files
excel_path = './excel_pndn_fndn/'

if treat_type == 'PNDN':
    major_excel = excel_path+'major_all_PNDN_norecycle.xlsx'
    minor_excel = excel_path+'minor_all_PNDN_norecycle.xlsx'
    major_excel_recy = './excel_pndn'+str(int(per_re*100))+'/major_all_pndn'+str(int(per_re*100))+'.xlsx'
    minor_excel_recy = './excel_pndn'+str(int(per_re*100))+'/minor_all_pndn'+str(int(per_re*100))+'.xlsx'

if treat_type == 'FNDN':
    major_excel = excel_path+'major_all_FNDN_norecycle.xlsx'
    minor_excel = excel_path+'minor_all_FNDN_norecycle.xlsx'
    major_excel_recy = './excel_fndn'+str(int(per_re*100))+'/major_all_fndn'+str(int(per_re*100))+'.xlsx'
    minor_excel_recy = './excel_fndn'+str(int(per_re*100))+'/minor_all_fndn'+str(int(per_re*100))+'.xlsx'

# read in excel files
major_sheet_names = pd.ExcelFile(major_excel).sheet_names
minor_sheet_names = pd.ExcelFile(minor_excel).sheet_names

major_writer = pd.ExcelWriter(major_excel_recy)
minor_writer = pd.ExcelWriter(minor_excel_recy)

###################
# majors/large POTWs
####################
for s_i in range(len(major_sheet_names)):
    major_df = pd.read_excel(major_excel,major_sheet_names[s_i])
    if major_sheet_names[s_i] == 'ocsd':
        rec_eff = 0.85 # water recovery efficiency
    else:
        rec_eff = 0.8
    if major_sheet_names[s_i] == 'ocsd' and per_re_st == .5:
        rec_eff = 0.85 # water recovery efficiency
        per_re = .62 # median percent recycle in 2016-2017
    else:
        rec_eff = 0.8
        per_re = per_re_st
    ######################
    # constituents
    #######################
    # nitrogen
    nh4_in = major_df['NH4 mmol/m3']
    no3_in = major_df['NO3 mmol/m3']
    no2_in = major_df['NO2 mmol/m3']
    din_in = nh4_in+no3_in+no2_in
    # all others
    dat_in = major_df['date']
    doo_in = major_df['DO mmol/m3']
    #bod_in = major_df['BOD mmol/m3']
    tpp_in = major_df['TP mmol/m3'] # final TP will be sum of PO4 and OP
    phh_in = major_df['pH'] # final pH stays the same
    tnn_in = major_df['TN mmol/m3']
    po4_in = major_df['PO4 mmol/m3']
    opp_in = major_df['OP mmol/m3']
    toc_in = major_df['TOC mmol/m3']
    onn_in = major_df['ON mmol/m3']
    sil_in = major_df['SiO4 mmol/m3']
    alk_in = major_df['Alk mmol/m3']
    sal_in = major_df['salinity PSU']
    dfe_in = major_df['dissolved Fe mmol/m3']
    tfe_in = major_df['total Fe mmol/m3']
    tem_in = major_df['temperature C']
    lat_in = major_df['latitude']
    lon_in = major_df['longitude']

#    # ocsd PNDN and FNDN is same as with 50% recycling because already recycles 50%
#    if major_sheet_names[s_i] == 'ocsd' and per_re == .5:
#        vol_ef = major_df['flow m3/s'] # volume of effluent going to recycling plant
#        nh4_fi = nh4_in
#        no3_fi = no3_in
#        no2_fi = no2_in
#        bod_fi = bod_in
#        po4_fi = po4_in 
#        opp_fi = opp_in
#        toc_fi = toc_in
#        onn_fi = onn_in
#        sil_fi = sil_in 
#        alk_fi = alk_in 
#        sal_fi = sal_in 
#        dfe_fi = dfe_in
#        tfe_fi = tfe_in 
#    else:

    #####################
    # water volume for recycling
    #####################
    vol_st = major_df['flow m3/s'] # volume of effluent going to recycling plant
    vol_in = vol_st*per_re # volume of influent going to recycling treatment plant
    vol_br = vol_in*(1-rec_eff) # return brine volume
    vol_re = vol_in*rec_eff # volume water recycled
    vol_ef = vol_br+(vol_st-vol_in) # volume of final effluent

    # RO permeate cocentration
    nh4_pm = nh4_in*(1-nh4_rem)
    no3_pm = no3_in*(1-no3_rem)
    no2_pm = no2_in*(1-no2_rem)
    din_pm = nh4_pm+no3_pm+no2_pm
    #bod_pm = bod_in*(1-bod_rem)
    po4_pm = po4_in*(1-po4_rem)
    opp_pm = opp_in*(1-opp_rem)
    toc_pm = toc_in*(1-toc_rem)
    onn_pm = onn_in*(1-onn_rem)
    sil_pm = sil_in*(1-sil_rem)
    alk_pm = alk_in*(1-alk_rem)
    sal_pm = sal_in*(1-sal_rem)
    dfe_pm = dfe_in*(1-dfe_rem)
    tfe_pm = tfe_in*(1-tfe_rem)

    # RO reject cocentration
    nh4_rj = (nh4_in-nh4_pm)/(1-rec_eff)
    no3_rj = (no3_in-no3_pm)/(1-rec_eff)
    no2_rj = (no2_in-no2_pm)/(1-rec_eff)
    din_rj = nh4_rj+no3_rj+no2_rj
    #bod_rj = (bod_in-bod_pm)/(1-rec_eff)
    po4_rj = (po4_in-po4_pm)/(1-rec_eff)
    opp_rj = (opp_in-opp_pm)/(1-rec_eff)
    toc_rj = (toc_in-toc_pm)/(1-rec_eff)
    onn_rj = (onn_in-onn_pm)/(1-rec_eff)
    sil_rj = (sil_in-sil_pm)/(1-rec_eff)
    alk_rj = (alk_in-alk_pm)/(1-rec_eff)
    sal_rj = (sal_in-sal_pm)/(1-rec_eff)
    dfe_rj = (dfe_in-dfe_pm)/(1-rec_eff)
    tfe_rj = (tfe_in-tfe_pm)/(1-rec_eff)

    ###############
    # final effluent
    ##############
    nh4_fi = ((nh4_rj*vol_br)+((vol_st-vol_in)*nh4_in))/vol_ef
    no3_fi = ((no3_rj*vol_br)+((vol_st-vol_in)*no3_in))/vol_ef
    no2_fi = ((no2_rj*vol_br)+((vol_st-vol_in)*no2_in))/vol_ef
    #bod_fi = ((bod_rj*vol_br)+((vol_st-vol_in)*bod_in))/vol_ef
    po4_fi = ((po4_rj*vol_br)+((vol_st-vol_in)*po4_in))/vol_ef
    opp_fi = ((opp_rj*vol_br)+((vol_st-vol_in)*opp_in))/vol_ef
    toc_fi = ((toc_rj*vol_br)+((vol_st-vol_in)*toc_in))/vol_ef
    onn_fi = ((onn_rj*vol_br)+((vol_st-vol_in)*onn_in))/vol_ef
    sil_fi = ((sil_rj*vol_br)+((vol_st-vol_in)*sil_in))/vol_ef
    alk_fi = ((alk_rj*vol_br)+((vol_st-vol_in)*alk_in))/vol_ef
    sal_fi = ((sal_rj*vol_br)+((vol_st-vol_in)*sal_in))/vol_ef
    dfe_fi = ((dfe_rj*vol_br)+((vol_st-vol_in)*dfe_in))/vol_ef
    tfe_fi = ((tfe_rj*vol_br)+((vol_st-vol_in)*tfe_in))/vol_ef
    
    print(major_sheet_names[s_i])
    print('nh4_fi',str(np.nanmean(nh4_fi*(14/1000))))
    print('no3_fi',str(np.nanmean(no3_fi*(14/1000))))
    print('no2_fi',str(np.nanmean(no2_fi*(14/1000))))
    print('po4_fi',str(np.nanmean(po4_fi)))
    print('opp_fi',str(np.nanmean(opp_fi)))
    print('toc_fi',str(np.nanmean(toc_fi)))
    print('onn_fi',str(np.nanmean(onn_fi)))
    print('sil_fi',str(np.nanmean(sil_fi)))
    print('alk_fi',str(np.nanmean(alk_fi)))
    print('sal_fi',str(np.nanmean(sal_fi)))
    print('dfe_fi',str(np.nanmean(dfe_fi)))
    print('tfe_fi',str(np.nanmean(tfe_fi)))
        
'''
    # print to excel file
    df = pd.DataFrame({'date':dat_in,
    'flow pre-recycle m3/s':vol_in,
    'flow brine m3/s':vol_br,
    'flow final effluent m3/s':vol_ef,
    'NH4 mmol/m3':nh4_fi,
    'NO3 mmol/m3':no3_fi,
    'NO2 mmol/m3':no2_fi,
    'DO mmol/m3':doo_in,
    'temperature C':tem_in,
    #'BOD mmol/m3':bod_fi,
    'pH':phh_in,
    'TP mmol/m3':po4_fi+opp_fi,
    'PO4 mmol/m3':po4_fi,
    'OP mmol/m3':opp_fi,
    'TOC mmol/m3':toc_fi,
    'ON mmol/m3':onn_fi,
    'TN mmol/m3':nh4_fi+no3_fi+no2_fi+onn_fi,
    'total Fe mmol/m3':tfe_fi,
    'SiO4 mmol/m3':sil_fi,
    'Alk mmol/m3':alk_fi,
    'salinity PSU':sal_fi,
    'dissolved Fe mmol/m3':dfe_fi,
    'latitude':lat_in,
    'longitude':lon_in},index=None,columns=None)
    df.to_excel(major_writer,sheet_name=major_sheet_names[s_i])
    
major_writer.save()
    
#####################
# minors/small POTWs
#####################
for s_i in range(len(minor_sheet_names)):
    minor_df = pd.read_excel(minor_excel,minor_sheet_names[s_i])
    #####################
    # water volume for recycling
    #####################
    # volume of effluent going to recycling plant
    vol_st = minor_df['flow m3/s']
    # volume of influent going to recycling treatment plant
    vol_in = vol_st*per_re
    # return brine volume
    vol_br = vol_in*(1-rec_eff)
    # volume water recycled
    vol_re = vol_in*rec_eff
    # volume of final effluent
    vol_ef = vol_br+(vol_st-vol_in)
    ######################
    # constituents
    #######################
    # nitrogen
    nh4_in = minor_df['NH4 mmol/m3']
    no3_in = minor_df['NO3 mmol/m3']
    no2_in = minor_df['NO2 mmol/m3']
    din_in = nh4_in+no3_in+no2_in
    # all others
    dat_in = minor_df['date']
    doo_in = minor_df['DO mmol/m3']
    #bod_in = minor_df['BOD mmol/m3']
    tpp_in = minor_df['TP mmol/m3'] # final TP will be sum of PO4 and OP
    phh_in = minor_df['pH'] # final pH stays the same
    tnn_in = minor_df['TN mmol/m3']
    po4_in = minor_df['PO4 mmol/m3']
    opp_in = minor_df['OP mmol/m3']
    toc_in = minor_df['TOC mmol/m3']
    onn_in = minor_df['ON mmol/m3']
    sil_in = minor_df['SiO4 mmol/m3']
    alk_in = minor_df['Alk mmol/m3']
    sal_in = minor_df['salinity PSU']
    dfe_in = minor_df['dissolved Fe mmol/m3']
    tfe_in = minor_df['total Fe mmol/m3']
    tem_in = minor_df['temperature C']
    lat_in = minor_df['latitude']
    lon_in = minor_df['longitude']

    # RO permeate cocentration
    nh4_pm = nh4_in*(1-nh4_rem)
    no3_pm = no3_in*(1-no3_rem)
    no2_pm = no2_in*(1-no2_rem)
    din_pm = nh4_pm+no3_pm+no2_pm
    #bod_pm = bod_in*(1-bod_rem)
    po4_pm = po4_in*(1-po4_rem)
    opp_pm = opp_in*(1-opp_rem)
    toc_pm = toc_in*(1-toc_rem)
    onn_pm = onn_in*(1-onn_rem)
    sil_pm = sil_in*(1-sil_rem)
    alk_pm = alk_in*(1-alk_rem)
    sal_pm = sal_in*(1-sal_rem)
    dfe_pm = dfe_in*(1-dfe_rem)
    tfe_pm = tfe_in*(1-tfe_rem)

    # RO reject cocentration
    nh4_rj = (nh4_in-nh4_pm)/(1-rec_eff)
    no3_rj = (no3_in-no3_pm)/(1-rec_eff)
    no2_rj = (no2_in-no2_pm)/(1-rec_eff)
    din_rj = nh4_rj+no3_rj+no2_rj
    #bod_rj = (bod_in-bod_pm)/(1-rec_eff)
    po4_rj = (po4_in-po4_pm)/(1-rec_eff)
    opp_rj = (opp_in-opp_pm)/(1-rec_eff)
    toc_rj = (toc_in-toc_pm)/(1-rec_eff)
    onn_rj = (onn_in-onn_pm)/(1-rec_eff)
    sil_rj = (sil_in-sil_pm)/(1-rec_eff)
    alk_rj = (alk_in-alk_pm)/(1-rec_eff)
    sal_rj = (sal_in-sal_pm)/(1-rec_eff)
    dfe_rj = (dfe_in-dfe_pm)/(1-rec_eff)
    tfe_rj = (tfe_in-tfe_pm)/(1-rec_eff)

    ###############
    # final effluent
    ##############
    nh4_fi = ((nh4_rj*vol_br)+((vol_st-vol_in)*nh4_in))/vol_ef
    no3_fi = ((no3_rj*vol_br)+((vol_st-vol_in)*no3_in))/vol_ef
    no2_fi = ((no2_rj*vol_br)+((vol_st-vol_in)*no2_in))/vol_ef
    #bod_fi = ((bod_rj*vol_br)+((vol_st-vol_in)*bod_in))/vol_ef
    po4_fi = ((po4_rj*vol_br)+((vol_st-vol_in)*po4_in))/vol_ef
    opp_fi = ((opp_rj*vol_br)+((vol_st-vol_in)*opp_in))/vol_ef
    toc_fi = ((toc_rj*vol_br)+((vol_st-vol_in)*toc_in))/vol_ef
    onn_fi = ((onn_rj*vol_br)+((vol_st-vol_in)*onn_in))/vol_ef
    sil_fi = ((sil_rj*vol_br)+((vol_st-vol_in)*sil_in))/vol_ef
    alk_fi = ((alk_rj*vol_br)+((vol_st-vol_in)*alk_in))/vol_ef
    sal_fi = ((sal_rj*vol_br)+((vol_st-vol_in)*sal_in))/vol_ef
    dfe_fi = ((dfe_rj*vol_br)+((vol_st-vol_in)*dfe_in))/vol_ef
    tfe_fi = ((tfe_rj*vol_br)+((vol_st-vol_in)*tfe_in))/vol_ef

    
    # print to excel file
    df = pd.DataFrame({'date':dat_in,
    'flow pre-recycle m3/s':vol_in,
    'flow brine m3/s':vol_br,
    'flow final effluent m3/s':vol_ef,
    'NH4 mmol/m3':nh4_fi,
    'NO3 mmol/m3':no3_fi,
    'NO2 mmol/m3':no2_fi,
    'DO mmol/m3':doo_in,
    'temperature C':tem_in,
    #'BOD mmol/m3':bod_fi,
    'pH':phh_in,
    'TP mmol/m3':po4_fi+opp_fi,
    'PO4 mmol/m3':po4_fi,
    'OP mmol/m3':opp_fi,
    'TOC mmol/m3':toc_fi,
    'ON mmol/m3':onn_fi,
    'TN mmol/m3':nh4_fi+no3_fi+no2_fi+onn_fi,
    'total Fe mmol/m3':tfe_fi,
    'SiO4 mmol/m3':sil_fi,
    'Alk mmol/m3':alk_fi,
    'salinity PSU':sal_fi,
    'dissolved Fe mmol/m3':dfe_fi,
    'latitude':lat_in,
    'longitude':lon_in},index=None,columns=None)
    df.to_excel(minor_writer,sheet_name=minor_sheet_names[s_i])
    
minor_writer.save()
'''    
