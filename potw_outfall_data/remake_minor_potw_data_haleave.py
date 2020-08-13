from netCDF4 import Dataset
import numpy as np

oldf = Dataset('minor_potw_data_new.nc','r')

newf = Dataset('minor_potw_data_new_haleave.nc','w')

#dimensions
tim_d = newf.createDimension('time',None)
lat_d = newf.createDimension('lat',15)
lon_d = newf.createDimension('lon',15)

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

tim_v.units = oldf.variables['time'].units
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
lt_minpotw = np.array((list(np.array(oldf.variables['latitude']))+[hlat]))
ln_minpotw = np.array((list(np.array(oldf.variables['longitude']))+[hlon]))

# MGD to m3/s
mgd_to_m3s = 0.043812645072430365

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

h_flo = np.array((list(hale_discharge)*16))

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
NO3_v[:,14,14] = np.empty((192)).fill(np.nan)
NO2_v[:,14,14] = np.empty((192)).fill(np.nan)
TOC_v[:,14,14] = np.empty((192)).fill(np.nan)
alkalinity_v[:,14,14] = np.empty((192)).fill(np.nan)
pH_v[:,14,14] = np.array(oldf.variables['pH'][:,13,13])
sulfate_v[:,14,14] = np.empty((192)).fill(np.nan)
temperature_v[:,14,14] = np.array(oldf.variables['temperature'][:,13,13])




tim_v[:] = np.array(oldf.variables['time'][:])
lat_v[:] = lt_minpotw
lon_v[:] = ln_minpotw
flow_v[:,:14,:14] = np.array(oldf.variables['flow'][:,:,:])
NO3_v[:,:14,:14] = np.array(oldf.variables['NO3'][:,:,:])
NH4_v[:,:14,:14] = np.array(oldf.variables['NH4'][:,:,:])
NO2_v[:,:14,:14] = np.array(oldf.variables['NO2'][:,:,:])
PO4_v[:,:14,:14] = np.array(oldf.variables['PO4'][:,:,:])
BOD_v[:,:14,:14] = np.array(oldf.variables['BOD'][:,:,:])
TOC_v[:,:14,:14] = np.array(oldf.variables['TOC'][:,:,:])
alkalinity_v[:,:14,:14] = np.array(oldf.variables['alkalinity'][:,:,:])
pH_v[:,:14,:14] = np.array(oldf.variables['pH'][:,:,:])
sulfate_v[:,:14,:14] = np.array(oldf.variables['sulfate'][:,:,:])
temperature_v[:,:14,:14] = np.array(oldf.variables['temperature'][:,:,:])

newf.title = 'includes Hale Ave. treatmeent plant, Escondido, CORRECT LAT/LON, Minor POTW interpolated data converted to mmol/m3'
newf.source = 'Dr. Martha Sutula from Southern California Coastal Water Research Project'

newf.description = 'Minor POTWs of South Bay Ocean Outfall, Hale Ave. Resource Recovery, San Clemente Island, San Elijo Ocean Outfall, Encina Ocean Outfall, Oceanside Ocean Outfall, Avalon WWTF, San Juan Creek Outfall, Aliso Creek Ocean Outfall, Terminal Island WWTP, Oxnard WWTP, Carpinteria WWTP, El Estero WWTP, Montecito WWTP, and Summerland WWTP' 

newf.close()
