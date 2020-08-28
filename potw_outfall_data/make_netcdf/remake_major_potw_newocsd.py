from netCDF4 import Dataset
import numpy as np
import pandas as pd

oldf = Dataset('major_potw_data.nc','r')

newf = Dataset('major_potw_data_newocsd.nc','w')

ocsd_data = '/data/project1/minnaho/potw_outfall_data/OO10-OCSD _REvised 06052020.xlsx'
ocsd_df = pd.read_excel(ocsd_data,header=None,sheet_name='Sheet1')
# new NO3,NO2
# is it actually mg/L, not kg/m3? makes more sense as mg/L
mgL_to_mmolm3 = 1000./14

# starts at 12-1970 instead of 1-1971 [potw_1997+1:potw_2013+1]
ocsd_no3 = list(ocsd_df[2][1:])
ocsd_no2 = list(ocsd_df[3][1:]-ocsd_df[2][1:])
for i in range(len(np.array(oldf.variables['NH4'][:,2,2]))-len(ocsd_df[3][1:])):
    ocsd_no3.append(np.nan)
    ocsd_no2.append(np.nan)

ocsd_no3 = np.array(ocsd_no3).astype(float)*mgL_to_mmolm3
ocsd_no2 = np.array(ocsd_no2).astype(float)*mgL_to_mmolm3

#dimensions
tim_d = newf.createDimension('time',None)
lat_d = newf.createDimension('lat',4)
lon_d = newf.createDimension('lon',4)

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
Fe_v = newf.createVariable('Fe',np.float64,('time','lat','lon'))
ON_v = newf.createVariable('ON',np.float64,('time','lat','lon'))
OP_v = newf.createVariable('OP',np.float64,('time','lat','lon'))
so2_v = newf.createVariable('SO2',np.float64,('time','lat','lon'))
alkalinity_v = newf.createVariable('alkalinity',np.float64,('time','lat','lon'))
pH_v = newf.createVariable('pH',np.float64,('time','lat','lon'))
sulfate_v = newf.createVariable('sulfate',np.float64,('time','lat','lon'))
do_v = newf.createVariable('dissolved_oxygen',np.float64,('time','lat','lon'))
temperature_v = newf.createVariable('temperature',np.float64,('time','lat','lon'))
salt_v = newf.createVariable('salinity',np.float64,('time','lat','lon'))

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
Fe_v.units = oldf.variables['Fe'].units
ON_v.units = oldf.variables['ON'].units
OP_v.units = oldf.variables['OP'].units
so2_v.units = oldf.variables['SO2'].units
alkalinity_v.units = oldf.variables['alkalinity'].units
sulfate_v.units = oldf.variables['sulfate'].units
do_v.units = oldf.variables['dissolved_oxygen'].units
temperature_v.units = oldf.variables['temperature'].units
salt_v.units = oldf.variables['salinity'].units

tim_v[:] = np.array(oldf.variables['time'][:])
lat_v[:] = np.array(oldf.variables['latitude'][:])
lon_v[:] = np.array(oldf.variables['longitude'][:])

flow_v[:,:,:] = np.array(oldf.variables['flow'][:,:,:])
NO3_v[:,:,:] = np.array(oldf.variables['NO3'][:,:,:])
NO3_v[:,2,2] = np.array(ocsd_no3)
NH4_v[:,:,:] = np.array(oldf.variables['NH4'][:,:,:])
NO2_v[:,:,:] = np.array(oldf.variables['NO2'][:,:,:])
NO2_v[:,2,2] = np.array(ocsd_no2)
PO4_v[:,:,:] = np.array(oldf.variables['PO4'][:,:,:])
Fe_v[:,:,:] = np.array(oldf.variables['Fe'][:,:,:])
so2_v[:,:,:] = np.array(oldf.variables['SO2'][:,:,:])
BOD_v[:,:,:] = np.array(oldf.variables['BOD'][:,:,:])
TOC_v[:,:,:] = np.array(oldf.variables['TOC'][:,:,:])
ON_v[:,:,:] = np.array(oldf.variables['ON'][:,:,:])
OP_v[:,:,:] = np.array(oldf.variables['OP'][:,:,:])
alkalinity_v[:,:,:] = np.array(oldf.variables['alkalinity'][:,:,:])
pH_v[:,:,:] = np.array(oldf.variables['pH'][:,:,:])
sulfate_v[:,:,:] = np.array(oldf.variables['sulfate'][:,:,:])
temperature_v[:,:,:] = np.array(oldf.variables['temperature'][:,:,:])
do_v[:,:,:] = np.array(oldf.variables['dissolved_oxygen'][:,:,:])
salt_v[:,:,:] = np.array(oldf.variables['salinity'][:,:,:])

newf.title = 'Major Southern California Bight POTW (Hyperion, JWPCP, OCSD, PLWTP) interpolated data 1970-2014'
newf.source = 'Dr. Martha Sutula from Southern California Coastal Water Research Project'

newf.close()
