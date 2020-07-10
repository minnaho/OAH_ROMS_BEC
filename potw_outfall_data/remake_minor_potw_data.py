from netCDF4 import Dataset
import numpy as np

oldf = Dataset('minor_potw_data.nc','r')

newf = Dataset('minor_potw_data_new.nc','w')
#dimensions
tim_d = newf.createDimension('time',None)
lat_d = newf.createDimension('lat',14)
lon_d = newf.createDimension('lon',14)

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

ln_minpotw = [-117.188,
-118.548,
-117.299,
-117.351,
-117.393,
-118.363,
-117.699,
-117.815,
-118.254,
-119.189,
-119.531,
-119.671,
-119.656,
-119.609]

lt_minpotw = [32.5373,
33.0102, 
33.0048, 
33.1103, 
33.1611, 
33.3049, 
33.4362, 
33.5453, 
33.7154, 
34.1262, 
34.3849, 
34.3888, 
34.4098, 
34.4122]

tim_v[:] = np.array(oldf.variables['time'][:])
lat_v[:] = lt_minpotw
lon_v[:] = ln_minpotw
flow_v[:,:,:] = np.array(oldf.variables['flow'][:,:,:])
NO3_v[:,:,:] = np.array(oldf.variables['NO3'][:,:,:])
NH4_v[:,:,:] = np.array(oldf.variables['NH4'][:,:,:])
NO2_v[:,:,:] = np.array(oldf.variables['NO2'][:,:,:])
PO4_v[:,:,:] = np.array(oldf.variables['PO4'][:,:,:])
BOD_v[:,:,:] = np.array(oldf.variables['BOD'][:,:,:])
TOC_v[:,:,:] = np.array(oldf.variables['TOC'][:,:,:])
alkalinity_v[:,:,:] = np.array(oldf.variables['alkalinity'][:,:,:])
pH_v[:,:,:] = np.array(oldf.variables['pH'][:,:,:])
sulfate_v[:,:,:] = np.array(oldf.variables['sulfate'][:,:,:])
temperature_v[:,:,:] = np.array(oldf.variables['temperature'][:,:,:])

newf.title = 'CORRECT LAT/LON, Minor POTW interpolated data converted to mmol/m3'
newf.source = 'Dr. Martha Sutula from Southern California Coastal Water Research Project'

newf.description = 'Minor POTWs of South Bay Ocean Outfall, San Clemente Island, San Elijo Ocean Outfall, Encina Ocean Outfall, Oceanside Ocean Outfall, Avalon WWTF, San Juan Creek Outfall, Aliso Creek Ocean Outfall, Terminal Island WWTP, Oxnard WWTP, Carpinteria WWTP, El Estero WWTP, Montecito WWTP, and Summerland WWTP' 

newf.close()
