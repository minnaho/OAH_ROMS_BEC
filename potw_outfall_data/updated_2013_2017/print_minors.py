# put minor dataset into excel
# each sheet as outfall

import numpy as np
from netCDF4 import Dataset,num2date
import pandas as pd

mgd_to_m3s = 0.043812645072430365
mgL_n = 1000./14 #mg/L N to mmol/m3
mgL_o = 1000./16 # mg/L O to mmol/m3 O
mgL_c = 1000./12 # mg/L C to mmol/m3 C
mgL_p = 1000./30.97 # mg/L C to mmol/m3 C
mgL_s = 1000./32.065 # mg/L C to mmol/m3 C

names = ['South Bay Reclamation Ocean Outfall', 'San Clemente Island', 'San Elijo Ocean Outfall', 'Encina Ocean Outfall', 'Oceanside Ocean Outfall', 'Avalon WWTF', 'San Juan Creek Outfall', 'Aliso Creek Ocean Outfall', 'Terminal Island WWTP', 'Oxnard WWTP', 'Carpinteria WWTP', 'El Estero WWTP', 'Montecito WWTP', 'Summerland WWTP', 'Hale Ave. Resource Recovery(discharges to San Elijo)', 'Goleta WWTP', 'South Bay International (discharges to South Bay)', 'Fallbrook (discharges to Oceanside)', 'Camp Pendleton (discharges to Oceanside)']

minors_nc = Dataset('minor_potw_data_2013_2017.nc','r')
dates = num2date(minors_nc.variables['time'],minors_nc.variables['time'].units,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# sbr
flow = (np.array(minors_nc.variables['flow'])[:,0,0])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,0,0])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,0,0])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,0,0])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,0,0])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,0,0])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,0,0])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,0,0])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,0,0]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,0,0])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,0,0]

sbr_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# sci
flow = (np.array(minors_nc.variables['flow'])[:,1,1])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,1,1])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,1,1])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,1,1])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,1,1])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,1,1])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,1,1])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,1,1])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,1,1]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,1,1])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,1,1]

sci_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# seo
flow = (np.array(minors_nc.variables['flow'])[:,2,2])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,2,2])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,2,2])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,2,2])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,2,2])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,2,2])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,2,2])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,2,2])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,2,2]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,2,2])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,2,2]

seo_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# eoo
flow = (np.array(minors_nc.variables['flow'])[:,3,3])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,3,3])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,3,3])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,3,3])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,3,3])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,3,3])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,3,3])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,3,3])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,3,3]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,3,3])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,3,3]

eoo_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# ocn
flow = (np.array(minors_nc.variables['flow'])[:,4,4])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,4,4])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,4,4])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,4,4])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,4,4])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,4,4])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,4,4])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,4,4])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,4,4]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,4,4])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,4,4]

ocn_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# ava
flow = (np.array(minors_nc.variables['flow'])[:,5,5])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,5,5])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,5,5])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,5,5])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,5,5])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,5,5])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,5,5])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,5,5])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,5,5]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,5,5])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,5,5]

ava_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# sjc
flow = (np.array(minors_nc.variables['flow'])[:,6,6])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,6,6])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,6,6])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,6,6])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,6,6])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,6,6])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,6,6])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,6,6])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,6,6]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,6,6])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,6,6]

sjc_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)


# ali
flow = (np.array(minors_nc.variables['flow'])[:,7,7])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,7,7])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,7,7])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,7,7])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,7,7])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,7,7])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,7,7])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,7,7])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,7,7]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,7,7])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,7,7]

ali_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# ter
flow = (np.array(minors_nc.variables['flow'])[:,8,8])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,8,8])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,8,8])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,8,8])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,8,8])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,8,8])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,8,8])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,8,8])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,8,8]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,8,8])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,8,8]

ter_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# oxn
flow = (np.array(minors_nc.variables['flow'])[:,9,9])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,9,9])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,9,9])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,9,9])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,9,9])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,9,9])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,9,9])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,9,9])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,9,9]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,9,9])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,9,9]

oxn_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# car
flow = (np.array(minors_nc.variables['flow'])[:,10,10])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,10,10])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,10,10])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,10,10])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,10,10])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,10,10])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,10,10])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,10,10])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,10,10]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,10,10])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,10,10]

car_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# ele
flow = (np.array(minors_nc.variables['flow'])[:,11,11])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,11,11])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,11,11])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,11,11])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,11,11])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,11,11])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,11,11])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,11,11])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,11,11]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,11,11])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,11,11]

ele_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# mon
flow = (np.array(minors_nc.variables['flow'])[:,12,12])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,12,12])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,12,12])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,12,12])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,12,12])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,12,12])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,12,12])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,12,12])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,12,12]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,12,12])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,12,12]

mon_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# sum
flow = (np.array(minors_nc.variables['flow'])[:,13,13])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,13,13])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,13,13])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,13,13])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,13,13])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,13,13])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,13,13])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,13,13])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,13,13]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,13,13])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,13,13]

sum_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# hal
flow = (np.array(minors_nc.variables['flow'])[:,14,14])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,14,14])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,14,14])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,14,14])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,14,14])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,14,14])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,14,14])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,14,14])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,14,14]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,14,14])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,14,14]

hal_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# gol
flow = (np.array(minors_nc.variables['flow'])[:,15,15])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,15,15])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,15,15])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,15,15])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,15,15])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,15,15])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,15,15])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,15,15])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,15,15]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,15,15])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,15,15]

gol_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# sbi
flow = (np.array(minors_nc.variables['flow'])[:,16,16])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,16,16])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,16,16])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,16,16])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,16,16])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,16,16])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,16,16])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,16,16])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,16,16]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,16,16])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,16,16]

sbi_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# fal
flow = (np.array(minors_nc.variables['flow'])[:,17,17])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,17,17])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,17,17])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,17,17])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,17,17])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,17,17])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,17,17])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,17,17])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,17,17]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,17,17])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,17,17]

fal_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# cmp
flow = (np.array(minors_nc.variables['flow'])[:,18,18])*(1./mgd_to_m3s) # convert back to MGD
no3 = (np.array(minors_nc.variables['NO3'])[:,18,18])*(1./mgL_n) # convert back to MGD
nh4 = (np.array(minors_nc.variables['NH4'])[:,18,18])*(1./mgL_n) # convert back to mg/L
no2 = (np.array(minors_nc.variables['NO2'])[:,18,18])*(1./mgL_n) # convert back to mg/L 
po4 = (np.array(minors_nc.variables['PO4'])[:,18,18])*(1./mgL_p) # convert back to mg/L 
bod = (np.array(minors_nc.variables['BOD'])[:,18,18])*(1./mgL_c) # convert back to mg/L 
toc = (np.array(minors_nc.variables['TOC'])[:,18,18])*(1./mgL_c) # convert back to mg/L 
alk = (np.array(minors_nc.variables['alkalinity'])[:,18,18])*(1./mgL_c) # convert back to mg/L
pH = np.array(minors_nc.variables['pH'])[:,18,18]
sulfate = (np.array(minors_nc.variables['sulfate'])[:,18,18])*(1./mgL_s)
tem = np.array(minors_nc.variables['temperature'])[:,18,18]

cmp_df = pd.DataFrame({'date':dates,'flow MGD':flow,'NO3 mg/L':no3,'NH4 mg/L':nh4,'NO2 mg/L':no2,'PO4 mg/L':po4,'BOD mg/L':bod,'TOC mg/L':toc,'Alkalinity mg/L':alk,'pH':pH,'SO4 mg/L':sulfate,'Temperature C':tem},index=None)

# write to excel
writer = pd.ExcelWriter('minor_potw_2013_2017.xlsx')
sbr_df.to_excel(writer,names[0])
sci_df.to_excel(writer,names[1])
seo_df.to_excel(writer,names[2])
eoo_df.to_excel(writer,names[3])
ocn_df.to_excel(writer,names[4])
ava_df.to_excel(writer,names[5])
sjc_df.to_excel(writer,names[6])
ali_df.to_excel(writer,names[7])
ter_df.to_excel(writer,names[8])
oxn_df.to_excel(writer,names[9])
car_df.to_excel(writer,names[10])
ele_df.to_excel(writer,names[11])
mon_df.to_excel(writer,names[12])
sum_df.to_excel(writer,names[13])
hal_df.to_excel(writer,names[14])
gol_df.to_excel(writer,names[15])
sbi_df.to_excel(writer,names[16])
fal_df.to_excel(writer,names[17])
cmp_df.to_excel(writer,names[18])
writer.save()
