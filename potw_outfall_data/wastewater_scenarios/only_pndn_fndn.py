# calculate effluent constiutent values 
# for PNDN and FNDN scenarios
# for OCSD and Terminal Island
# because their current recycling increases
# the concentration of constituents
import numpy as np
import pandas as pd
import subprocess as subprocess

######################
# CHOICES of recycling
######################
# choose PNDN or FNDN
treat_type = 'PNDN'

# use flows from actual plant for ocsd and Terminal island
# pndn and fndn only
df_ac_oc = pd.read_excel('./excel_pndn_fndn/major_all_PNDN.xlsx',sheet_name='ocsd')
df_ac_ti = pd.read_excel('./excel_pndn_fndn/minor_all_PNDN.xlsx',sheet_name='TerminalIslandWaterReclamation')

flo_ac_oc = df_ac_oc['flow m3/s']
flo_ac_ti = df_ac_ti['flow m3/s']


# percent of influent going to recycling treatment plant
per_re_oc = .62
per_re_ti = .28

# water recovery efficiency
rec_eff_oc = 0.85
rec_eff_ti = 0.77

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
final_path = './excel_final_pndn_fndn/'

if treat_type == 'PNDN':
    major_excel = excel_path+'major_all_PNDN_norecycle.xlsx'
    minor_excel = excel_path+'minor_all_PNDN.xlsx'
    major_final = final_path+'major_all_PNDN_final.xlsx'
    minor_final = final_path+'minor_all_PNDN_final.xlsx'

if treat_type == 'FNDN':
    major_excel = excel_path+'major_all_FNDN_norecycle.xlsx'
    minor_excel = excel_path+'minor_all_FNDN.xlsx'
    major_final = final_path+'major_all_FNDN_final.xlsx'
    minor_final = final_path+'minor_all_FNDN_final.xlsx'

# read in excel files
major_sheet_names = pd.ExcelFile(major_excel).sheet_names
minor_sheet_names = pd.ExcelFile(minor_excel).sheet_names

major_writer = pd.ExcelWriter(major_final)
minor_writer = pd.ExcelWriter(minor_final)

###################
# OCSD
####################
major_df = pd.read_excel(major_excel,sheet_name='ocsd')


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

#####################
# water volume for recycling
#####################
vol_st = major_df['flow m3/s'] # volume of effluent going to recycling plant

#per_re_oc_end = [0.407339554,0.426583595,0.388450848,0.42273448,0.397790511,0.369021747,0.39301071,0.416106066,0.425249218,0.422956062,0.420051958,0.423683498,0.426113808,0.433309853,0.438786194,0.433386339,0.309762349,0.431281383,0.423339261,0.415951538,0.391271134,0.391242053,0.42699656,0.410639464,0.440519655,0.438204614,0.388071038,0.453532083,0.466639788,0.428752988,0.451052066,0.45500105,0.530682081,0.567089954,0.615260394,0.569720806,0.632171448,0.661851449,0.635187544,0.649714952,0.630083601,0.586179818,0.625418316,0.610825499,0.626193833,0.603365443,0.557521922,0.633868005,0.644514261,0.429580143,0.648743409,0.652144417,0.637649211,0.534589213,0.439157755,0.4926285,0.551562675,0.61803854,0.61994618,0.661831316,0.661609388,0.614311362,0.625659108,0.648942084,0.643453568]
#per_re_oc = ([0]*(len(vol_st)-len(per_re_oc_end)))+per_re_oc_end
per_re_oc = .62

vol_in = vol_st*per_re_oc # volume of influent going to recycling treatment plant
vol_br = vol_in*(1-rec_eff_oc) # return brine volume
vol_re = vol_in*rec_eff_oc # volume water recycled
vol_ef = vol_br+(vol_st-vol_in) # volume of final effluent

vol_ac_oc = np.array(flo_ac_oc[-len(vol_st):])


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
nh4_rj = (nh4_in-nh4_pm)/(1-rec_eff_oc)
no3_rj = (no3_in-no3_pm)/(1-rec_eff_oc)
no2_rj = (no2_in-no2_pm)/(1-rec_eff_oc)
din_rj = nh4_rj+no3_rj+no2_rj
#bod_rj = (bod_in-bod_pm)/(1-rec_eff_oc)
po4_rj = (po4_in-po4_pm)/(1-rec_eff_oc)
opp_rj = (opp_in-opp_pm)/(1-rec_eff_oc)
toc_rj = (toc_in-toc_pm)/(1-rec_eff_oc)
onn_rj = (onn_in-onn_pm)/(1-rec_eff_oc)
sil_rj = (sil_in-sil_pm)/(1-rec_eff_oc)
alk_rj = (alk_in-alk_pm)/(1-rec_eff_oc)
sal_rj = (sal_in-sal_pm)/(1-rec_eff_oc)
dfe_rj = (dfe_in-dfe_pm)/(1-rec_eff_oc)
tfe_rj = (tfe_in-tfe_pm)/(1-rec_eff_oc)

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
'flow final effluent m3/s':vol_ac_oc,
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
df.to_excel(major_writer,sheet_name='ocsd')
    
major_writer.save()
    

# do nothing for Terminal Island 
# PNDN for TI already met, just set FNDN values for TI FNDN
subprocess.call('cp ./excel_pndn_fndn/minor_all_PNDN.xlsx ./excel_final_pndn_fndn/minor_all_PNDN_final.xlsx',shell=True)
subprocess.call('cp ./excel_pndn_fndn/minor_all_FNDN.xlsx ./excel_final_pndn_fndn/minor_all_FNDN_final.xlsx',shell=True)


''''
#####################
# Terminal Island - PNDN is same as current
#####################
if treat_type = 'PNDN':
minor_df = pd.read_excel(minor_excel,sheet_name='TerminalIslandWaterReclamation')
minor_df = pd.read_excel(minor_excel,sheet_name='TerminalIslandWaterReclamation')
#####################
# water volume for recycling
#####################
# volume of effluent going to recycling plant
vol_st = minor_df['flow m3/s']
# volume of influent going to recycling treatment plant
vol_in = vol_st*per_re_ti
# return brine volume
vol_br = vol_in*(1-rec_eff_ti)
# volume water recycled
vol_re = vol_in*rec_eff_ti
# volume of final effluent
vol_ef = vol_br+(vol_st-vol_in)


vol_ac_ti = np.array(flo_ac_ti[-len(vol_st):])

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
nh4_rj = (nh4_in-nh4_pm)/(1-rec_eff_ti)
no3_rj = (no3_in-no3_pm)/(1-rec_eff_ti)
no2_rj = (no2_in-no2_pm)/(1-rec_eff_ti)
din_rj = nh4_rj+no3_rj+no2_rj
#bod_rj = (bod_in-bod_pm)/(1-rec_eff_ti)
po4_rj = (po4_in-po4_pm)/(1-rec_eff_ti)
opp_rj = (opp_in-opp_pm)/(1-rec_eff_ti)
toc_rj = (toc_in-toc_pm)/(1-rec_eff_ti)
onn_rj = (onn_in-onn_pm)/(1-rec_eff_ti)
sil_rj = (sil_in-sil_pm)/(1-rec_eff_ti)
alk_rj = (alk_in-alk_pm)/(1-rec_eff_ti)
sal_rj = (sal_in-sal_pm)/(1-rec_eff_ti)
dfe_rj = (dfe_in-dfe_pm)/(1-rec_eff_ti)
tfe_rj = (tfe_in-tfe_pm)/(1-rec_eff_ti)

################
## final effluent
###############
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
'flow final effluent m3/s':vol_ac_ti,
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
df.to_excel(minor_writer,sheet_name='TerminalIslandWaterReclamation')
    
minor_writer.save()
    
'''
