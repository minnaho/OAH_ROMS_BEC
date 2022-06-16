# make roms psource file for major and minor POTWs
# for wastewater recycling scenarios
# PNDN and FNDN only
# Recycling scenarios only are in separate file
from netCDF4 import Dataset,num2date
import numpy as np
import pandas as pd
from PyCO2SYS import CO2SYS
import datetime as datetime

# scenario files
data_path = '/data/project1/minnaho/potw_outfall_data/wastewater_scenarios/'

treat = 'PNDN'

fol_alll = 'excel_pndn_fndn/'
fol_octi = 'excel_final_pndn_fndn/'

major_alll = 'major_all_'+treat+'_norecycle.xlsx'
minor_alll = 'minor_all_'+treat+'_norecycle.xlsx'

major_octi = 'major_all_'+treat+'_final.xlsx'
minor_octi = 'minor_all_'+treat+'_final.xlsx'

ncout = 'roms_psource_'+treat+'_only.nc'


# read in data, name of each sheet as a key
major_data_alll = pd.read_excel(data_path+fol_alll+major_alll,sheet_name=None)
minor_data = pd.read_excel(data_path+fol_alll+minor_alll,sheet_name=None)

major_data_octi = pd.read_excel(data_path+fol_octi+major_octi,sheet_name=None)
minor_data_octi = pd.read_excel(data_path+fol_octi+minor_octi,sheet_name=None)

# load excel data majors
major_htp_mon = major_data_alll['htp']
major_jwp_mon = major_data_alll['jwpcp']
major_plw_mon = major_data_alll['plwtp']

major_ocs_mon = major_data_octi['ocsd']

# roms psource file to copy and remake
file_path = '/data/project1/minnaho/psource/run_2013_2017/roms_psource_1997_2017.nc'
file_path_out = '/data/project1/minnaho/psource/wastewater_scenarios/'+ncout
file_nc = Dataset(file_path,'r')

Qbar_nc   = np.array(file_nc.variables['Qbar'][:,:])
# end psources before rivers to exclude rivers?
#end_ind = 96
# or include rivers 
end_ind = Qbar_nc.shape[0]

# psource time is actually days since 1994-01-01
psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
psrc_dt = num2date(psource_time_nc,'days since 1994-01-01',only_use_cftime_datetimes=False)

# psrc time starts at 1997-01-30
# only choose the last 12 months - 2017
# psrc_dt[180] is 2012-01-30 
# psrc_dt[204] is 2014-01-30 
# psrc_dt[204] is 2017-01-30 

# only choose Aug 2016 - Jul 2017
p_st = -17
p_en = -5

Qbar_nc   = np.array(file_nc.variables['Qbar'][:end_ind,p_st:p_en])

Qshape_nc = np.array(file_nc.variables['Qshape'][:,:end_ind])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][:end_ind])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][:end_ind])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][:end_ind])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,:end_ind])

# read in input file 
temp_nc = np.array(file_nc.variables['temp'][:end_ind,p_st:p_en])
salt_nc = np.array(file_nc.variables['salt'][:end_ind,p_st:p_en])
PO4_nc = np.array(file_nc.variables['PO4'][:end_ind,p_st:p_en])
NO3_nc = np.array(file_nc.variables['NO3'][:end_ind,p_st:p_en])
NH4_nc = np.array(file_nc.variables['NH4'][:end_ind,p_st:p_en])
Fe_nc  = np.array(file_nc.variables['Fe'][:end_ind,p_st:p_en])
O2_nc  = np.array(file_nc.variables['O2'][:end_ind,p_st:p_en])
DIC_nc = np.array(file_nc.variables['DIC'][:end_ind,p_st:p_en])
Alk_nc = np.array(file_nc.variables['Alk'][:end_ind,p_st:p_en])
DOC_nc = np.array(file_nc.variables['DOC'][:end_ind,p_st:p_en])
DON_nc = np.array(file_nc.variables['DON'][:end_ind,p_st:p_en])
DOP_nc = np.array(file_nc.variables['DOP'][:end_ind,p_st:p_en])
NO2_nc = np.array(file_nc.variables['NO2'][:end_ind,p_st:p_en])
SiO3_nc = np.array(file_nc.variables['SiO3'][:end_ind,p_st:p_en])


# break up diffuser flow
# HTP : 2 diffusers
Qbar_nc[0,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[1,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[2,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[17,:] = major_htp_mon['flow m3/s'][p_st:p_en]*(5./28) 

Qbar_nc[6,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[8,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[3,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[5,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[18,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[22,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 

Qbar_nc[4,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[7,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[9,:]  = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[19,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28)
Qbar_nc[20,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28)
Qbar_nc[21,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28)

Qbar_nc[23,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[26,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[14,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[16,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[13,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[11,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 

Qbar_nc[25,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[27,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[24,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[10,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[15,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[12,:] = major_htp_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 


# break up diffuser flow
# JWPCP : 3 diffusers
Qbar_nc[28,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*(5./14) 
Qbar_nc[29,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*(5./14) 
Qbar_nc[30,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*(5./14)
Qbar_nc[50,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*(5./14)
                                                         
Qbar_nc[34,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
Qbar_nc[32,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
Qbar_nc[37,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
Qbar_nc[39,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
Qbar_nc[38,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
Qbar_nc[41,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./2)/14) 
                                                        
Qbar_nc[33,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
Qbar_nc[35,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
Qbar_nc[31,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
Qbar_nc[36,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
Qbar_nc[42,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
Qbar_nc[40,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.65*((1./6)/14) 
                                                         
Qbar_nc[51,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
Qbar_nc[54,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
Qbar_nc[47,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
Qbar_nc[49,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
Qbar_nc[46,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
Qbar_nc[44,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./2)/14)
                                                        
Qbar_nc[43,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)
Qbar_nc[48,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)
Qbar_nc[45,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)
Qbar_nc[55,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)
Qbar_nc[53,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)
Qbar_nc[52,:] = major_jwp_mon['flow m3/s'][p_st:p_en]*.35*((1./6)/14)


# OCSD one pipe
Qbar_nc[56,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*(5./14) 
Qbar_nc[62,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*(5./14) 
                                                                  
Qbar_nc[60,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
Qbar_nc[65,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
Qbar_nc[63,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
Qbar_nc[66,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
Qbar_nc[61,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
Qbar_nc[58,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./2)/14)
                                                                  
Qbar_nc[59,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)
Qbar_nc[64,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)
Qbar_nc[57,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)
Qbar_nc[69,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)
Qbar_nc[68,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)
Qbar_nc[67,:] = major_ocs_mon['flow final effluent m3/s'][p_st:p_en]*((1./6)/14)


# PLWTP two diffusers
Qbar_nc[70,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[72,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[71,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(5./28) 
Qbar_nc[87,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(5./28) 
                                     
Qbar_nc[76,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[78,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[73,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[75,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[88,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[92,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(((1./2)+(1./6))/28) 
                                     
Qbar_nc[74,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[77,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[79,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[89,:] = major_plw_mon['flow m3/s'][p_st:p_en]*(((1./2)+(1./6))/28) 
Qbar_nc[90,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[91,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
                                     
Qbar_nc[83,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[81,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[86,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[84,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
Qbar_nc[95,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./2)/28) 
                        
Qbar_nc[80,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[85,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[82,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[93,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 
Qbar_nc[94,:] = major_plw_mon['flow m3/s'][p_st:p_en]*((1./6)/28) 


# set constituent values based on major POTW

# htp
htp_st = 0
htp_en = 28
temp_nc[htp_st:htp_en,:] = major_htp_mon['temperature C'][p_st:p_en]
salt_nc[htp_st:htp_en,:] = major_htp_mon['salinity PSU'][p_st:p_en]
NO3_nc[htp_st:htp_en,:]  = major_htp_mon['NO3 mmol/m3'][p_st:p_en]
NH4_nc[htp_st:htp_en,:]  = major_htp_mon['NH4 mmol/m3'][p_st:p_en]
NO2_nc[htp_st:htp_en,:]  = major_htp_mon['NO2 mmol/m3'][p_st:p_en]
PO4_nc[htp_st:htp_en,:]  = major_htp_mon['PO4 mmol/m3'][p_st:p_en]
Fe_nc[htp_st:htp_en,:]   = major_htp_mon['dissolved Fe mmol/m3'][p_st:p_en]
O2_nc[htp_st:htp_en,:]   = major_htp_mon['DO mmol/m3'][p_st:p_en]
Alk_nc[htp_st:htp_en,:]  = major_htp_mon['Alk mmol/m3'][p_st:p_en]
DOC_nc[htp_st:htp_en,:]  = major_htp_mon['TOC mmol/m3'][p_st:p_en]
DON_nc[htp_st:htp_en,:]  = major_htp_mon['ON mmol/m3'][p_st:p_en]
DOP_nc[htp_st:htp_en,:]  = major_htp_mon['OP mmol/m3'][p_st:p_en]
SiO3_nc[htp_st:htp_en,:]  = major_htp_mon['SiO4 mmol/m3'][p_st:p_en]

# pH var wasn't in old file, so make it
pH_nc = np.ones((DOP_nc.shape[0],DOP_nc.shape[1]))*np.nan
pH_nc[htp_st:htp_en,:]   = major_htp_mon['pH'][p_st:p_en]


# jwpcp
jwp_st = 28
jwp_en = 56
temp_nc[jwp_st:jwp_en,:] = major_jwp_mon['temperature C'][p_st:p_en]
salt_nc[jwp_st:jwp_en,:] = major_jwp_mon['salinity PSU'][p_st:p_en]
NO3_nc[jwp_st:jwp_en,:]  = major_jwp_mon['NO3 mmol/m3'][p_st:p_en]
NH4_nc[jwp_st:jwp_en,:]  = major_jwp_mon['NH4 mmol/m3'][p_st:p_en]
NO2_nc[jwp_st:jwp_en,:]  = major_jwp_mon['NO2 mmol/m3'][p_st:p_en]
PO4_nc[jwp_st:jwp_en,:]  = major_jwp_mon['PO4 mmol/m3'][p_st:p_en]
Fe_nc[jwp_st:jwp_en,:]   = major_jwp_mon['dissolved Fe mmol/m3'][p_st:p_en]
O2_nc[jwp_st:jwp_en,:]   = major_jwp_mon['DO mmol/m3'][p_st:p_en]
Alk_nc[jwp_st:jwp_en,:]  = major_jwp_mon['Alk mmol/m3'][p_st:p_en]
DOC_nc[jwp_st:jwp_en,:]  = major_jwp_mon['TOC mmol/m3'][p_st:p_en]
DON_nc[jwp_st:jwp_en,:]  = major_jwp_mon['ON mmol/m3'][p_st:p_en]
DOP_nc[jwp_st:jwp_en,:]  = major_jwp_mon['OP mmol/m3'][p_st:p_en]
SiO3_nc[jwp_st:jwp_en,:]  = major_jwp_mon['SiO4 mmol/m3'][p_st:p_en]

pH_nc[jwp_st:jwp_en,:]   = major_jwp_mon['pH'][p_st:p_en]

# ocsd
ocs_st = 56
ocs_en = 70
temp_nc[ocs_st:ocs_en,:] = major_ocs_mon['temperature C'][p_st:p_en]
salt_nc[ocs_st:ocs_en,:] = major_ocs_mon['salinity PSU'][p_st:p_en]
NO3_nc[ocs_st:ocs_en,:]  = major_ocs_mon['NO3 mmol/m3'][p_st:p_en]
NH4_nc[ocs_st:ocs_en,:]  = major_ocs_mon['NH4 mmol/m3'][p_st:p_en]
NO2_nc[ocs_st:ocs_en,:]  = major_ocs_mon['NO2 mmol/m3'][p_st:p_en]
PO4_nc[ocs_st:ocs_en,:]  = major_ocs_mon['PO4 mmol/m3'][p_st:p_en]
Fe_nc[ocs_st:ocs_en,:]   = major_ocs_mon['dissolved Fe mmol/m3'][p_st:p_en]
O2_nc[ocs_st:ocs_en,:]   = major_ocs_mon['DO mmol/m3'][p_st:p_en]
Alk_nc[ocs_st:ocs_en,:]  = major_ocs_mon['Alk mmol/m3'][p_st:p_en]
DOC_nc[ocs_st:ocs_en,:]  = major_ocs_mon['TOC mmol/m3'][p_st:p_en]
DON_nc[ocs_st:ocs_en,:]  = major_ocs_mon['ON mmol/m3'][p_st:p_en]
DOP_nc[ocs_st:ocs_en,:]  = major_ocs_mon['OP mmol/m3'][p_st:p_en]
SiO3_nc[ocs_st:ocs_en,:]  = major_ocs_mon['SiO4 mmol/m3'][p_st:p_en]

pH_nc[ocs_st:ocs_en,:]   = major_ocs_mon['pH'][p_st:p_en]

# plwtp
plw_st = 70
plw_en = 96
temp_nc[plw_st:plw_en,:] = major_plw_mon['temperature C'][p_st:p_en]
salt_nc[plw_st:plw_en,:] = major_plw_mon['salinity PSU'][p_st:p_en]
NO3_nc[plw_st:plw_en,:]  = major_plw_mon['NO3 mmol/m3'][p_st:p_en]
NH4_nc[plw_st:plw_en,:]  = major_plw_mon['NH4 mmol/m3'][p_st:p_en]
NO2_nc[plw_st:plw_en,:]  = major_plw_mon['NO2 mmol/m3'][p_st:p_en]
PO4_nc[plw_st:plw_en,:]  = major_plw_mon['PO4 mmol/m3'][p_st:p_en]
Fe_nc[plw_st:plw_en,:]   = major_plw_mon['dissolved Fe mmol/m3'][p_st:p_en]
O2_nc[plw_st:plw_en,:]   = major_plw_mon['DO mmol/m3'][p_st:p_en]
Alk_nc[plw_st:plw_en,:]  = major_plw_mon['Alk mmol/m3'][p_st:p_en]
DOC_nc[plw_st:plw_en,:]  = major_plw_mon['TOC mmol/m3'][p_st:p_en]
DON_nc[plw_st:plw_en,:]  = major_plw_mon['ON mmol/m3'][p_st:p_en]
DOP_nc[plw_st:plw_en,:]  = major_plw_mon['OP mmol/m3'][p_st:p_en]
SiO3_nc[plw_st:plw_en,:]  = major_plw_mon['SiO4 mmol/m3'][p_st:p_en]

pH_nc[plw_st:plw_en,:]   = major_plw_mon['pH'][p_st:p_en]

# calculate DIC separately
# calculate pH from CO2SYS
par1type =  1 # first input parameter - Alk
par2type = 3 # second input parameter - pH
pHscale = 2 # sea water scale
k1k2c = 14 # Millero et al, 2010 sea water scale
kso4c = 1 # KSO4 of Dickson & TB of Uppstrom 1979
saltt = 33 
sill = np.copy(SiO3_nc[:,:])
sill[sill>400] = 400

# hyp
for t_i in range(Alk_nc.shape[1]):
    CO2dict = CO2SYS(
        Alk_nc[htp_st,t_i],
        pH_nc[htp_st,t_i],
        par1type,
        par2type,
        saltt,
        temp_nc[htp_st,t_i],
        np.nan,
        0,
        np.nan,
        sill[htp_st,t_i],
        #SiO3_nc[htp_st,t_i],
        PO4_nc[htp_st,t_i],
        pHscale,
        k1k2c,
        kso4c)
    # only need to take one value and populate all 
    DIC_nc[htp_st:htp_en,t_i] = CO2dict['TCO2']

    CO2dict = CO2SYS(
        Alk_nc[jwp_st,t_i],
        pH_nc[jwp_st,t_i],
        par1type,
        par2type,
        saltt,
        temp_nc[jwp_st,t_i],
        np.nan,
        0,
        np.nan,
        sill[jwp_st,t_i],
        #SiO3_nc[jwp_st,t_i],
        PO4_nc[jwp_st,t_i],
        pHscale,
        k1k2c,
        kso4c)
    DIC_nc[jwp_st:jwp_en,t_i] = CO2dict['TCO2']

    CO2dict = CO2SYS(
        Alk_nc[ocs_st,t_i],
        pH_nc[ocs_st,t_i],
        par1type,
        par2type,
        saltt,
        temp_nc[ocs_st,t_i],
        np.nan,
        0,
        np.nan,
        sill[ocs_st,t_i],
        #SiO3_nc[ocs_st,t_i],
        PO4_nc[ocs_st,t_i],
        pHscale,
        k1k2c,
        kso4c)
    DIC_nc[ocs_st:ocs_en,t_i] = CO2dict['TCO2']

    CO2dict = CO2SYS(
        Alk_nc[plw_st,t_i],
        pH_nc[plw_st,t_i],
        par1type,
        par2type,
        saltt,
        temp_nc[plw_st,t_i],
        np.nan,
        0,
        np.nan,
        sill[plw_st,t_i],
        #SiO3_nc[plw_st,t_i],
        PO4_nc[plw_st,t_i],
        pHscale,
        k1k2c,
        kso4c)
    DIC_nc[plw_st:plw_en,t_i] = CO2dict['TCO2']


# minor POTWs

# set N values based on minor POTWs
minor_names = list(minor_data.keys())
for p_i in range(len(minor_names)):
    if minor_names[p_i] != 'TerminalIslandWaterReclamation':
        minor_mon = minor_data[minor_names[p_i]]
    if minor_names[p_i] == 'TerminalIslandWaterReclamation':
        minor_mon = minor_data_octi[minor_names[p_i]]
    Qbar_nc[plw_en+p_i,:] = minor_mon['flow m3/s'][p_st:p_en]
    temp_nc[plw_en+p_i,:] = minor_mon['temperature C'][p_st:p_en]
    salt_nc[plw_en+p_i,:] = minor_mon['salinity PSU'][p_st:p_en]
    NO3_nc[plw_en+p_i,:]  = minor_mon['NO3 mmol/m3'][p_st:p_en]
    NH4_nc[plw_en+p_i,:]  = minor_mon['NH4 mmol/m3'][p_st:p_en]
    NO2_nc[plw_en+p_i,:]  = minor_mon['NO2 mmol/m3'][p_st:p_en]
    PO4_nc[plw_en+p_i,:]  = minor_mon['PO4 mmol/m3'][p_st:p_en]
    Fe_nc[plw_en+p_i,:]   = minor_mon['dissolved Fe mmol/m3'][p_st:p_en]
    O2_nc[plw_en+p_i,:]   = minor_mon['DO mmol/m3'][p_st:p_en]
    Alk_nc[plw_en+p_i,:]  = minor_mon['Alk mmol/m3'][p_st:p_en]
    DOC_nc[plw_en+p_i,:]  = minor_mon['TOC mmol/m3'][p_st:p_en]
    DON_nc[plw_en+p_i,:]  = minor_mon['ON mmol/m3'][p_st:p_en]
    DOP_nc[plw_en+p_i,:]  = minor_mon['OP mmol/m3'][p_st:p_en]
    SiO3_nc[plw_en+p_i,:] = minor_mon['SiO4 mmol/m3'][p_st:p_en]

    # no pH values, so use 7.5 (consistent with Faycal's method)
    phh = 7.5 

    for t_i in range(Alk_nc.shape[1]):
        CO2dict = CO2SYS(
            Alk_nc[plw_en+p_i,t_i],
            phh,
            par1type,
            par2type,
            saltt,
            temp_nc[plw_en+p_i,t_i],
            np.nan,
            0,
            np.nan,
            #SiO3_nc[plw_en+p_i,t_i],
            sill[plw_en+p_i,t_i],
            PO4_nc[plw_en+p_i,t_i],
            pHscale,
            k1k2c,
            kso4c)
        DIC_nc[plw_en+p_i,t_i] = CO2dict['TCO2']


# make new netcdf

file_out = Dataset(file_path_out,'w')
Nsrc_dim = file_out.createDimension('Nsrc',Qbar_nc.shape[0])
Npas_dim = file_out.createDimension('Npas',Lsrc_nc.shape[0])
s_rho_dim = file_out.createDimension('s_rho',Qshape_nc.shape[0])

# loop over this time for Aug 1 1997 to Nov 31 1999 
# start Aug 1 2016, last time step is Nov 1 1999

# add 2 to time values because the times are at end of months 
# so simulation will start at beginning of month
# Jul 30 --> Aug 1
#psrc_final = psource_time_nc[6:27+7]+2 
# no need to change start time because ROMS interpolates

# 6 is Jul 30 1997 and ends in Nov 29 1999
psrc_final = psource_time_nc[6:27+8]

psrc_time_dim = file_out.createDimension('psrc_time',psrc_final.shape[0])

psrc_time_var = file_out.createVariable('psrc_time','float64',('psrc_time'))
psrc_time_var.units = 'days'
psrc_time_var.longname = 'point source time from 1994-1-1'
# psource loads for Aug 1 2016 to Jul 31 2017
#psrc_time_var[:] = psource_time_nc[p_st:p_en]
# loop over this time for Aug 1 1997 to Nov 31 1999 
# start Aug 1 2016, last time step is Nov 1 1999
#psrc_time_var[:] = psource_time_nc
psrc_time_var[:] = psrc_final

# time steps to add to loop the time
lp = 5

# put variables in new netcdf
# append same time series + last 5 times againt to get 28 months
Qbar_var = file_out.createVariable('Qbar','float32',('Nsrc','psrc_time'))
Qbar_var.units = 'meter3 second-1'
Qbar_var.longname = 'vertically integrated mass transport of point'
#Qbar_var[:,:] = Qbar_nc
Qbar_var[:,:] = np.append(np.append(Qbar_nc,Qbar_nc,axis=1),Qbar_nc[:,:lp],axis=1)

Qshape_var = file_out.createVariable('Qshape','float32',('s_rho','Nsrc'))
Qshape_var.units = 'no units'
Qshape_var.longname = 'Vertical weight of the flux for each psource cell'
Qshape_var[:,:] = Qshape_nc

Isrc_var = file_out.createVariable('Isrc','float32',('Nsrc'))
Isrc_var.units = 'no units'
Isrc_var.longname = 'global xi-directional grid number of the point sources'
Isrc_var[:] = Isrc_nc

Jsrc_var = file_out.createVariable('Jsrc','float32',('Nsrc'))
Jsrc_var.units = 'no units'
Jsrc_var.longname = 'global xi-directional grid number of the point sources'
Jsrc_var[:] = Jsrc_nc

Dsrc_var = file_out.createVariable('Dsrc','float32',('Nsrc'))
Dsrc_var.units = 'no units'
Dsrc_var.longname = 'flag to determine direction of the mass point source'
Dsrc_var[:] = Dsrc_nc

Lsrc_var = file_out.createVariable('Lsrc','float32',('Npas','Nsrc'))
Lsrc_var.units = 'no units'
Lsrc_var.longname = 'logical switch for any tracers at every point source locations'
Lsrc_var[:,:] = Lsrc_nc

temp_var = file_out.createVariable('temp','float32',('Nsrc','psrc_time'))
temp_var.units = 'Degrees Celsius'
temp_var.longname = 'Temperature at point source'
#temp_var[:,:] = temp_nc
temp_var[:,:] = np.append(np.append(temp_nc,temp_nc,axis=1),temp_nc[:,:lp],axis=1)

salt_var = file_out.createVariable('salt','float32',('Nsrc','psrc_time'))
salt_var.units = 'psu'
salt_var.longname = 'Salinity at point source'
#salt_var[:,:] = salt_nc
salt_var[:,:] = np.append(np.append(salt_nc,salt_nc,axis=1),salt_nc[:,:lp],axis=1)

PO4_var = file_out.createVariable('PO4','float32',('Nsrc','psrc_time'))
PO4_var.units = 'mmol P m-3'
PO4_var.longname = 'averaged Phosphate'
#PO4_var[:,:] = PO4_nc
PO4_var[:,:] = np.append(np.append(PO4_nc,PO4_nc,axis=1),PO4_nc[:,:lp],axis=1)

NO3_var = file_out.createVariable('NO3','float32',('Nsrc','psrc_time'))
NO3_var.units = 'mmol N m-3'
NO3_var.longname = 'averaged Nitrate'
#NO3_var[:,:] = NO3_nc
NO3_var[:,:] = np.append(np.append(NO3_nc,NO3_nc,axis=1),NO3_nc[:,:lp],axis=1)

NH4_var = file_out.createVariable('NH4','float32',('Nsrc','psrc_time'))
NH4_var.units = 'mmol N m-3'
NH4_var.longname = 'averaged Ammonium'
#NH4_var[:,:] = NH4_nc
NH4_var[:,:] = np.append(np.append(NH4_nc,NH4_nc,axis=1),NH4_nc[:,:lp],axis=1)

Fe_var = file_out.createVariable('Fe','float32',('Nsrc','psrc_time'))
Fe_var.units = 'mmol Fe m-3'
Fe_var.longname = 'averaged Iron'
#Fe_var[:,:] = Fe_nc
Fe_var[:,:] = np.append(np.append(Fe_nc,Fe_nc,axis=1),Fe_nc[:,:lp],axis=1)

O2_var = file_out.createVariable('O2','float32',('Nsrc','psrc_time'))
O2_var.units = 'mmol O2 m-3'
O2_var.longname = 'averaged Oxygen'
#O2_var[:,:] = O2_nc
O2_var[:,:] = np.append(np.append(O2_nc,O2_nc,axis=1),O2_nc[:,:lp],axis=1)

DIC_var = file_out.createVariable('DIC','float32',('Nsrc','psrc_time'))
DIC_var.units = 'mmol C m-3'
DIC_var.longname = 'averaged Dissolved inorganic carbon'
#DIC_var[:,:] = DIC_nc
DIC_var[:,:] = np.append(np.append(DIC_nc,DIC_nc,axis=1),DIC_nc[:,:lp],axis=1)

Alk_var = file_out.createVariable('Alk','float32',('Nsrc','psrc_time'))
Alk_var.units = 'mmol m-3'
Alk_var.longname = 'averaged alkalinity'
#Alk_var[:,:] = Alk_nc
Alk_var[:,:] = np.append(np.append(Alk_nc,Alk_nc,axis=1),Alk_nc[:,:lp],axis=1)

DOC_var = file_out.createVariable('DOC','float32',('Nsrc','psrc_time'))
DOC_var.units = 'mmol C m-3'
DOC_var.longname = 'averaged Dissolved organic carbon'
#DOC_var[:,:] = DOC_nc
DOC_var[:,:] = np.append(np.append(DOC_nc,DOC_nc,axis=1),DOC_nc[:,:lp],axis=1)

DON_var = file_out.createVariable('DON','float32',('Nsrc','psrc_time'))
DON_var.units = 'mmol N m-3'
DON_var.longname = 'averaged Dissolved organic nitrogen'
#DON_var[:,:] = DON_nc
DON_var[:,:] = np.append(np.append(DON_nc,DON_nc,axis=1),DON_nc[:,:lp],axis=1)

DOP_var = file_out.createVariable('DOP','float32',('Nsrc','psrc_time'))
DOP_var.units = 'mmol P m-3'
DOP_var.longname = 'averaged Dissolved organic phosphorus'
#DOP_var[:,:] = DOP_nc
DOP_var[:,:] = np.append(np.append(DOP_nc,DOP_nc,axis=1),DOP_nc[:,:lp],axis=1)

NO2_var = file_out.createVariable('NO2','float32',('Nsrc','psrc_time'))
NO2_var.units = 'mmol N m-3'
NO2_var.longname = 'averaged Nitrite'
#NO2_var[:,:] = NO2_nc
NO2_var[:,:] = np.append(np.append(NO2_nc,NO2_nc,axis=1),NO2_nc[:,:lp],axis=1)

SO3_var = file_out.createVariable('SiO3','float32',('Nsrc','psrc_time'))
SO3_var.units = 'mmol N m-3'
SO3_var.longname = 'averaged Silicate'
#SO3_var[:,:] = NO2_nc
SO3_var[:,:] = np.append(np.append(SiO3_nc,SiO3_nc,axis=1),SiO3_nc[:,:lp],axis=1)

# pH doesn't matter because not input into model
pH_var = file_out.createVariable('pH','float32',('Nsrc','psrc_time'))
pH_var.units = 'pH units'
pH_var.longname = 'averaged pH'
#pH_var[:,:] = pH_nc
pH_var[:,:] = np.append(np.append(pH_nc,pH_nc,axis=1),pH_nc[:,:lp],axis=1)

file_out.close()
