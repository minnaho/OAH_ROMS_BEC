#######################
# remake minor inputs
# for 2013-2016
# including Hale Ave (discharges to San Elijo)
# Goleta (left out last time)
# Fallbrook+Camp Pendleton (discharges to Oceanside)
# remake South Bay to include both South Bay Reclamation+InternationalWWTP
# can't add inland ones to correct discharger because messes up 
# concentrations and fluxes, so add them as separate with same lat/lon
########################
from netCDF4 import Dataset,num2date,date2num
import numpy as np
import pandas as pd
import datetime as datetime

oldf = Dataset('../run_1997_2000/minor_potw_data_new.nc','r')

newf = Dataset('minor_potw_data_2013_2016.nc','w')

# read goleta data
mgd_to_m3s = 0.043812645072430365
mgL_to_mmolm3 = 1000./14 #mg/L N to mmol/m3

# change to 2013-2016
ind_end = 4*12 # 48 monthly points for 4 years 2013-2016
gdf = pd.read_excel('OO17-Goleta_2013_2017.xlsx',header=None)
gd_fl = np.array(gdf[1][1:ind_end+1]).astype(float)*mgd_to_m3s # flow 
gd_ph = np.array(gdf[2][1:ind_end+1]).astype(float) # pH
gd_nh = np.array(gdf[3][1:ind_end+1]).astype(float)*mgL_to_mmolm3 # ammonium
gd_tm = np.array(gdf[4][1:ind_end+1]).astype(float) # temperature
gd_lat = gdf[8][1]
gd_lon = gdf[9][1]

# datetime
gd_dat_l = []
for d_i in range(1,len(gdf[0][1:ind_end+1])+1):
    gd_dat_l.append(gdf[0][d_i].to_pydatetime())

gd_dat = np.array(gd_dat_l)

# monthly 2013-2017
numdat = date2num(gd_dat,'days since 2013-01-01')
nummon = len(numdat)

# read south bay reclamation
sbr_df = pd.read_excel('NPDESMonitoringData_CA0109045_SouthBayReclamation.xlsx',header=None,skiprows=7)
sbr_fl = np.array(sbr_df[52][3:ind_end+3].replace(to_replace='NODI: B',value=np.nan)).astype(float)*mgd_to_m3s
# take mean of max/min for pH
sbr_ph = np.nanmean((np.array(sbr_df[126][3:ind_end+3].replace(to_replace='NODI: B',value=np.nan)).astype(float),np.array(sbr_df[127][3:ind_end+3].replace(to_replace='NODI: B',value=np.nan)).astype(float)),axis=0)
# ug/L convert to mmol/m3
sbr_nh = np.array(sbr_df[76][3:ind_end+3].replace(to_replace='NODI: B',value=np.nan)).astype(float)*(1./1000)*mgL_to_mmolm3



#dimensions
tim_d = newf.createDimension('time',None)
lat_d = newf.createDimension('lat',16)
lon_d = newf.createDimension('lon',16)

#variables
tim_v = newf.createVariable('time',np.float32,('time'))
lat_v = newf.createVariable('latitude',np.float32,('lat'))
lon_v = newf.createVariable('longitude',np.float32,('lon'))
flow_v = newf.createVariable('flow',np.float64,('time','lat','lon'))
NO3_v = newf.createVariable('NO3',np.float64,('time','lat','lon'))
NH4_v = newf.createVariable('NH4',np.float64,('time','lat','lon'))
NO2_v = newf.createVariable('NO2',np.float64,('time','lat','lon'))
PO4_v = newf.createVariable('PO4',np.float64,('time','lat','lon'))
BOD_v = newf.createVariable('BOD',np.float64,('time','lat','lon'))
TOC_v = newf.createVariable('TOC',np.float64,('time','lat','lon'))
alkalinity_v = newf.createVariable('alkalinity',np.float64,('time','lat','lon'))
pH_v = newf.createVariable('pH',np.float64,('time','lat','lon'))
sulfate_v = newf.createVariable('sulfate',np.float64,('time','lat','lon'))
temperature_v = newf.createVariable('temperature',np.float64,('time','lat','lon'))

tim_v.units = 'days since 2013-01-01'
lat_v.units = oldf.variables['latitude'].units
lon_v.units = oldf.variables['longitude'].units
flow_v.units = oldf.variables['flow'].units
NO3_v.units = oldf.variables['NO3'].units
NH4_v.units = oldf.variables['NH4'].units
NO2_v.units = oldf.variables['NO2'].units
PO4_v.units = oldf.variables['PO4'].units
BOD_v.units = oldf.variables['BOD'].units
TOC_v.units = oldf.variables['TOC'].units
alkalinity_v.units = oldf.variables['alkalinity'].units
sulfate_v.units = oldf.variables['sulfate'].units
temperature_v.units = oldf.variables['temperature'].units

hlat = 33.005833333333335
hlon = -117.3025
lt_minpotw = np.array((list(np.array(oldf.variables['latitude']))+[hlat]+[gd_lat]))
ln_minpotw = np.array((list(np.array(oldf.variables['longitude']))+[hlon]+[gd_lon]))

# san elijo discharge should be same as hale ave
lt_minpotw[2] = hlat
ln_minpotw[2] = hlon

# MGD to m3/s

hale_discharge = np.array((
12.9,
13.9,
12.9,
12.4,
12.6,
12.5,
12.5,
12.5,
12.3,
12.3,
12.2,
12.4))*mgd_to_m3s

h_flo = np.array((list(hale_discharge)*(int(nummon/12)))) # repeat discharage

yr_to_s = 86400*365
lb_to_mmol_n = 1000/(453.59237*14)
lb_to_mmol_p = 1000/(453.59237*30.97)
lb_to_mmol_c = 1000/(453.59237*14)

h_nh4 = ((508370.7318*lb_to_mmol_n)/yr_to_s)/h_flo
h_po4 = ((1934.5*lb_to_mmol_p)/yr_to_s)/h_flo
h_bod = ((348946.6045*lb_to_mmol_c)/yr_to_s)/h_flo

flow_v[:,14,14] = h_flo
NH4_v[:,14,14] = h_nh4
PO4_v[:,14,14] = h_po4
BOD_v[:,14,14] = h_bod
NO3_v[:,14,14] = np.empty((nummon)).fill(np.nan)
NO2_v[:,14,14] = np.empty((nummon)).fill(np.nan)
TOC_v[:,14,14] = np.empty((nummon)).fill(np.nan)
alkalinity_v[:,14,14] = np.empty((nummon)).fill(np.nan)
pH_v[:,14,14] = np.array(oldf.variables['pH'][:nummon,2,2]) # copy San Elijo
sulfate_v[:,14,14] = np.empty((nummon)).fill(np.nan)
temperature_v[:,14,14] = np.array(oldf.variables['temperature'][:nummon,2,2])

flow_v[:,15,15] = gd_fl
NH4_v[:,15,15] = gd_nh
pH_v[:,15,15] = gd_ph
temperature_v[:,15,15] = gd_tm
PO4_v[:,15,15] = np.empty((nummon)).fill(np.nan)
BOD_v[:,15,15] = np.empty((nummon)).fill(np.nan)
NO3_v[:,15,15] = np.empty((nummon)).fill(np.nan)
NO2_v[:,15,15] = np.empty((nummon)).fill(np.nan)
TOC_v[:,15,15] = np.empty((nummon)).fill(np.nan)
alkalinity_v[:,15,15] = np.empty((nummon)).fill(np.nan)
sulfate_v[:,15,15] = np.empty((nummon)).fill(np.nan)

# number of years to take from old data, since repeating that data
# old data from 2014?
tim_v[:] = numdat
lat_v[:] = lt_minpotw
lon_v[:] = ln_minpotw
flow_v[:,:14,:14] = np.array(oldf.variables['flow'][:nummon,:,:])
NO3_v[:,:14,:14] = np.array(oldf.variables['NO3'][:nummon,:,:])
NH4_v[:,:14,:14] = np.array(oldf.variables['NH4'][:nummon,:,:])
NO2_v[:,:14,:14] = np.array(oldf.variables['NO2'][:nummon,:,:])
PO4_v[:,:14,:14] = np.array(oldf.variables['PO4'][:nummon,:,:])
BOD_v[:,:14,:14] = np.array(oldf.variables['BOD'][:nummon,:,:])
TOC_v[:,:14,:14] = np.array(oldf.variables['TOC'][:nummon,:,:])
alkalinity_v[:,:14,:14] = np.array(oldf.variables['alkalinity'][:nummon,:,:])
pH_v[:,:14,:14] = np.array(oldf.variables['pH'][:nummon,:,:])
sulfate_v[:,:14,:14] = np.array(oldf.variables['sulfate'][:nummon,:,:])
temperature_v[:,:14,:14] = np.array(oldf.variables['temperature'][:nummon,:,:])

newf.title = 'Minor POTW 2013-2017 inputs'
newf.source = 'Dr. Martha Sutula from Southern California Coastal Water Research Project, EPA ECHO'

newf.description = 'Minor POTWs, in order: South Bay Ocean Outfall, San Clemente Island, San Elijo Ocean Outfall, Encina Ocean Outfall, Oceanside Ocean Outfall, Avalon WWTF, San Juan Creek Outfall, Aliso Creek Ocean Outfall, Terminal Island WWTP, Oxnard WWTP, Carpinteria WWTP, El Estero WWTP, Montecito WWTP, and Summerland WWTP, Hale Ave. Resource Recovery(same discharge location as San Elijo), Goleta WWTP' 

newf.close()
