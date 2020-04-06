############################
# get agency survey csv data
# and organize into netCDF
##########################
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import pandas as pd
from collections import defaultdict


#####################
# read netCDF file
####################
f0 = Dataset('central_bight_master_database_1998_2017_1D.nc','r')
variables = list(f0.variables.keys())

# get unique date, lats, lons, depth
time_nc = f0.variables['date'][:]
lats_nc = f0.variables['latitude'][:]
lons_nc = f0.variables['longitude'][:]
depth_nc = f0.variables['depth'][:]

time_list = sorted(list(set(time_nc)))
depth_list = sorted(list(set(depth_nc)))

time_len = len(time_list)
depth_len = len(depth_list)

##########################################
# get sampling sites and lat/lon for each as position
# 382 sampling sites (from Stn_coords.csv)
##########################################
lat_lon_csv = pd.read_csv('Stn_coords.csv',sep=',')
lat_csv = np.copy(lat_lon_csv['Latitude'])
lon_csv = np.copy(lat_lon_csv['Longitude'])

lat_lon_pairs = np.empty((382,2))
for i in range(len(lat_csv)):
    lat_lon_pairs[i] = [lat_csv[i],lon_csv[i]]

nc_v = defaultdict(list)
#for var in range(len(variables)):
#    nc_v[variables[var]] = [ [] for i in range( ] 

# put data into 3D structure of (time,position,depth)
for v_i in variables:
    print(v_i)
    var_temp = np.empty((time_len,len(lat_csv),depth_len))
    data = f0.variables[v_i][:]
    # find data in position and match it to the index of time,lat/lon,depth
    # then make 3D array
    for d_i in range(len(data)):
        lat_value = lats_nc[d_i]
        lon_value = lons_nc[d_i]
        position_ind = np.where((lat_lon_pairs==(lat_value,lon_value)).all(axis=1))
        s = position_ind[0][0]
        t = np.where(time_list==time_nc[d_i])[0][0]
        d = np.where(depth_list==depth_nc[d_i])[0][0]
        var_temp[t,s,d] = data[d_i]
    # put into dictionary with variable name as key
    nc_v[v_i] = np.copy(var_temp)

############################## 
# make new netCDF with 3D structure
############################## 
f = Dataset('central_bight_master_database_1998_2017.nc','w')

f.title = 'Central Bight Master Database Sampling Data from POTW Agencies' 

# dimensions
time = f.createDimension('time',time_len)
position = f.createDimension('position',len(lat_csv))
depth = f.createDimension('depth',depth_len)

# create variables
times = f.createVariable('time',np.float64,('time',))
positions = f.createVariable('position',np.float64,('position',))
depths = f.createVariable('depth',np.float32,('depth',))

lats = f.createVariable('latitude',np.float32,('position',))
lons = f.createVariable('longitude',np.float32,('position',))

CDOM                = f.createVariable('CDOM',np.float32,('time','position','depth'))
CDOM_ECO            = f.createVariable('CDOM_ECO',np.float32,('time','position','depth'))
CDOM_Turner         = f.createVariable('CDOM_Turner',np.float32,('time','position','depth'))
CDOM_WET            = f.createVariable('CDOM_WET',np.float32,('time','position','depth'))
CDOM_voltage        = f.createVariable('CDOM_voltage',np.float32,('time','position','depth'))
CDOM_voltage_ECO    = f.createVariable('CDOM_voltage_ECO',np.float32,('time','position','depth'))
CDOM_voltage_Turner = f.createVariable('CDOM_voltage_Turner',np.float32,('time','position','depth'))
CDOM_voltage_WET    = f.createVariable('CDOM_voltage_WET',np.float32,('time','position','depth'))
Chl_a               = f.createVariable('Chl-a',np.float32,('time','position','depth'))
Chl_a_ECO           = f.createVariable('Chl-a_ECO',np.float32,('time','position','depth'))
Chl_a_USC_UCLA      = f.createVariable('Chl-a_USC_UCLA',np.float32,('time','position','depth'))
Chl_a_WET           = f.createVariable('Chl-a_WET',np.float32,('time','position','depth'))
Chl_a_discrete      = f.createVariable('Chl-a_discrete',np.float32,('time','position','depth'))
Chl_a_voltage_ECO   = f.createVariable('Chl-a_voltage_ECO',np.float32,('time','position','depth'))
Chl_a_voltage_WET   = f.createVariable('Chl-a_voltage_WET',np.float32,('time','position','depth'))
E_coli              = f.createVariable('E_coli',np.float32,('time','position','depth'))
Enterococci         = f.createVariable('Enterococci',np.float32,('time','position','depth'))
ammonia             = f.createVariable('ammonia-N',np.float32,('time','position','depth'))
beam_C              = f.createVariable('beam_C',np.float32,('time','position','depth'))
conductivity        = f.createVariable('conductivity',np.float32,('time','position','depth'))
delta_T             = f.createVariable('delta_T',np.float32,('time','position','depth'))
descent_rate        = f.createVariable('descent_rate',np.float32,('time','position','depth'))
dissolved_oxygen    = f.createVariable('dissolved_oxygen',np.float32,('time','position','depth'))
fecal_coliforms     = f.createVariable('fecal_coliforms',np.float32,('time','position','depth'))
irradiance          = f.createVariable('irradiance',np.float32,('time','position','depth'))
irradiance_norm     = f.createVariable('irradiance_norm',np.float32,('time','position','depth'))
light_transmission  = f.createVariable('light_transmission',np.float32,('time','position','depth'))
oxygen_saturation_mg_L    = f.createVariable('oxygen_saturation_mg_L',np.float32,('time','position','depth'))
oxygen_saturation_percent = f.createVariable('oxygen_saturation_percent',np.float32,('time','position','depth'))
pH                        = f.createVariable('pH',np.float32,('time','position','depth'))
salinity                  = f.createVariable('salinity',np.float32,('time','position','depth'))
specific_density          = f.createVariable('specific_density',np.float32,('time','position','depth'))
stability                 = f.createVariable('stability',np.float32,('time','position','depth'))
surface_irradiance        = f.createVariable('surface_irradiance',np.float32,('time','position','depth'))
temperature               = f.createVariable('temperature',np.float32,('time','position','depth'))
total_coliforms           = f.createVariable('total_coliforms',np.float32,('time','position','depth'))
transmissivity            = f.createVariable('transmissivity',np.float32,('time','position','depth'))

# units
times.units = 'days since 1998-07-07'
positions.units = 'sampling site, each index matches to lat/lon index'
depths.units = 'm'

lats.units = 'degrees north'
lons.units = 'degrees east'

CDOM.units                = 'ug/L'
CDOM_ECO.units            = 'ug/L'
CDOM_Turner.units         = 'ug/L'
CDOM_WET.units            = 'ug/L'
CDOM_voltage.units        = 'V'
CDOM_voltage_ECO.units    = 'V'
CDOM_voltage_Turner.units = 'V'
CDOM_voltage_WET.units    = 'V'
Chl_a.units               = 'ug/L'
Chl_a_ECO.units           = 'ug/L'
Chl_a_USC_UCLA.units      = 'ug/L'
Chl_a_WET.units           = 'ug/L'
Chl_a_discrete.units      = 'ug/L'
Chl_a_voltage_ECO.units   = 'V'
Chl_a_voltage_WET.units   = 'V'
E_coli.units              = 'MPN/100mL'
Enterococci.units         = 'MPN/100mL'
ammonia.units             = 'mg/L'
beam_C.units              = '1/m'
conductivity.units        = 'S/m'
delta_T.units             = 'degrees Celsius/m'
descent_rate.units        = 'm/s'
dissolved_oxygen.units    = 'mg/L'
fecal_coliforms.units     = 'MPN/100mL'
irradiance.units          = 'uE/cm2/s'
irradiance_norm.units     = '%'
light_transmission.units  = '%'
oxygen_saturation_mg_L.units    = 'mg/L'
oxygen_saturation_percent.units = '%'
salinity.units                  = 'psu'
specific_density.units          = 'kg/m3'
stability.units                 = 'kg/m3/m'
surface_irradiance.units        = 'uE/cm2/s'
temperature.units               = 'degrees Celsius'
total_coliforms.units           = 'MPN/100mL'
transmissivity.units            = '%'

# long names (if necessary(
Chl_a.long_name = 'chlorophyll-a'
delta_T.long_name = 'change in temperature'


# assign values to variables
times[:] = np.array(time_list)
positions[:] = np.arange(len(lat_csv))
depths[:] = np.array(depth_list)

lats[:] = lat_csv
lons[:] = lon_csv

v_ind = 0 
CDOM[:,:,:]                = nc_v[variables[v_ind]]
CDOM_ECO[:,:,:]            = nc_v[variables[v_ind+1]]
CDOM_Turner[:,:,:]         = nc_v[variables[v_ind+2]]
CDOM_WET[:,:,:]            = nc_v[variables[v_ind+3]]
CDOM_voltage[:,:,:]        = nc_v[variables[v_ind+4]]
CDOM_voltage_ECO[:,:,:]    = nc_v[variables[v_ind+5]]
CDOM_voltage_Turner[:,:,:] = nc_v[variables[v_ind+6]]
CDOM_voltage_WET[:,:,:]    = nc_v[variables[v_ind+7]]
Chl_a[:,:,:]               = nc_v[variables[v_ind+8]]
Chl_a_ECO[:,:,:]           = nc_v[variables[v_ind+9]]
Chl_a_USC_UCLA[:,:,:]      = nc_v[variables[v_ind+10]]
Chl_a_WET[:,:,:]           = nc_v[variables[v_ind+11]]
Chl_a_discrete[:,:,:]      = nc_v[variables[v_ind+12]]
Chl_a_voltage_ECO[:,:,:]   = nc_v[variables[v_ind+13]]
Chl_a_voltage_WET[:,:,:]   = nc_v[variables[v_ind+14]]
E_coli[:,:,:]              = nc_v[variables[v_ind+15]]
Enterococci[:,:,:]         = nc_v[variables[v_ind+16]]
ammonia[:,:,:]             = nc_v[variables[v_ind+17]]
beam_C[:,:,:]              = nc_v[variables[v_ind+18]]
conductivity[:,:,:]        = nc_v[variables[v_ind+19]]
delta_T[:,:,:]             = nc_v[variables[v_ind+20]]
descent_rate[:,:,:]        = nc_v[variables[v_ind+21]]
dissolved_oxygen[:,:,:]    = nc_v[variables[v_ind+22]]
fecal_coliforms[:,:,:]     = nc_v[variables[v_ind+23]]
irradiance[:,:,:]          = nc_v[variables[v_ind+24]]
irradiance_norm[:,:,:]     = nc_v[variables[v_ind+25]]
light_transmission[:,:,:]  = nc_v[variables[v_ind+26]]
oxygen_saturation_mg_L[:,:,:]    = nc_v[variables[v_ind+27]]
oxygen_saturation_percent[:,:,:] = nc_v[variables[v_ind+28]]
pH[:,:,:]                        = nc_v[variables[v_ind+29]]
salinity[:,:,:]                  = nc_v[variables[v_ind+30]]
specific_density[:,:,:]          = nc_v[variables[v_ind+31]]
stability[:,:,:]                 = nc_v[variables[v_ind+32]]
surface_irradiance[:,:,:]        = nc_v[variables[v_ind+33]]
temperature[:,:,:]               = nc_v[variables[v_ind+34]]
total_coliforms[:,:,:]           = nc_v[variables[v_ind+35]]
transmissivity[:,:,:]            = nc_v[variables[v_ind+36]]

f.close()

