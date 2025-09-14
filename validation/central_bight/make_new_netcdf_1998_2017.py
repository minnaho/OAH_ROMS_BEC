############################
# get agency survey csv data
# and organize into netCDF
##########################
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import pandas as pd
from collections import defaultdict
import datetime


#####################
# read netCDF file
####################
f0 = Dataset('central_bight_master_database_1998_2019_1D_validation_2023.nc','r')
variables = list(f0.variables.keys())

# get unique date, lats, lons, depth
time_nc = f0.variables['date'][:]
lats_nc = f0.variables['latitude'][:]
lons_nc = f0.variables['longitude'][:]
depth_nc = f0.variables['depth'][:]

# find data between these dates
#dtend = date2num(datetime.datetime(2017,12,31),'days since 1996-01-16')
#dtstart = date2num(datetime.datetime(1997,1,1),'days since 1996-01-16')
#
#time_rd = time_nc[(time_nc>dtstart)&(time_nc<dtend)]

# round depth to nearest whole number
depth_nc = np.round(depth_nc)

time_list = sorted(list(set(time_nc)))
depth_list = sorted(list(set(depth_nc)))

time_len = len(time_list)
depth_len = len(depth_list)

##########################################
# get sampling sites and lat/lon for each as position
# 382 sampling sites (from Stn_coords.csv)
##########################################
#lat_lon_csv = pd.read_csv('Stn_coords.csv',sep=',')
#lat_csv = np.copy(lat_lon_csv['Latitude'])
#lon_csv = np.copy(lat_lon_csv['Longitude'])

lat_lon_nc = np.array((lats_nc,lons_nc)).T
lat_lon_pairs = np.unique(lat_lon_nc,axis=0)

#lat_lon_pairs = np.empty((382,2))
#for i in range(len(lat_csv)):
#    lat_lon_pairs[i] = [lat_csv[i],lon_csv[i]]

nc_v = defaultdict(list)
#for var in range(len(variables)):
#    nc_v[variables[var]] = [ [] for i in range( ] 

# put data into 3D structure of (time,position,depth)
for v_i in variables:
    var_temp = np.empty((time_len,len(lat_lon_pairs),depth_len))
    data = f0.variables[v_i][:]
    # find data in position and match it to the index of time,lat/lon,depth
    # then make 3D array
    for d_i in range(len(data)):
        print(v_i+' '+str(d_i)+' of '+str(len(data)))
        lat_value = lats_nc[d_i]
        lon_value = lons_nc[d_i]
        position_ind = np.where((lat_lon_pairs==(lat_value,lon_value)))
        s = position_ind[0][0]
        t = np.where(time_list==time_nc[d_i])[0][0]
        d = np.where(depth_list==depth_nc[d_i])[0][0]
        var_temp[t,s,d] = data[d_i]
    # put into dictionary with variable name as key
    nc_v[v_i] = np.copy(var_temp)

############################## 
# make new netCDF with 3D structure
############################## 
f = Dataset('central_bight_master_database_1998_2017_validation_2023.nc','w')

f.title = 'Central Bight Master Database Sampling Data from POTW Agencies' 

# dimensions
time = f.createDimension('time',time_len)
position = f.createDimension('position',len(lat_lon_pairs))
depth = f.createDimension('depth',depth_len)

# create variables
times = f.createVariable('time',np.float64,('time',))
positions = f.createVariable('position',np.float64,('position',))
depths = f.createVariable('depth',np.float32,('depth',))

lats = f.createVariable('latitude',np.float32,('position',))
lons = f.createVariable('longitude',np.float32,('position',))

CDOM                = f.createVariable('CDOM',np.float32,('time','position','depth'))
CDOM_voltage    = f.createVariable('CDOM_voltage',np.float32,('time','position','depth'))
Chl_a               = f.createVariable('Chl-a',np.float32,('time','position','depth'))
Chl_a_voltage   = f.createVariable('Chl-a_voltage',np.float32,('time','position','depth'))
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
times.units = f0.variables['date'].units
positions.units = 'sampling site, each index matches to lat/lon index'
depths.units = 'm'

lats.units = 'degrees north'
lons.units = 'degrees east'

CDOM.units                = 'ug/L'
Chl_a.units               = 'ug/L'
Chl_a_voltage.units       = 'V'
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

# long names (if necessary)
Chl_a.long_name = 'chlorophyll-a'
delta_T.long_name = 'change in temperature'


# assign values to variables
times[:] = np.array(time_list)
positions[:] = np.arange(len(lat_lon_pairs))
depths[:] = np.array(depth_list)

lats[:] = lat_lon_pairs[:,0]
lons[:] = lat_lon_pairs[:,1]

v_ind = 0 
CDOM[:,:,:]                = nc_v[variables[v_ind]]
CDOM_voltage[:,:,:]        = nc_v[variables[v_ind+1]]
Chl_a[:,:,:]               = nc_v[variables[v_ind+2]]
Chl_a_voltage[:,:,:]       = nc_v[variables[v_ind+3]]
E_coli[:,:,:]              = nc_v[variables[v_ind+4]]
Enterococci[:,:,:]         = nc_v[variables[v_ind+5]]
ammonia[:,:,:]             = nc_v[variables[v_ind+6]]
beam_C[:,:,:]              = nc_v[variables[v_ind+7]]
conductivity[:,:,:]        = nc_v[variables[v_ind+8]]
# skip v_ind+9 because that's the date variable
delta_T[:,:,:]             = nc_v[variables[v_ind+10]]
# skip v_ind+11 because that's the depth variable
descent_rate[:,:,:]        = nc_v[variables[v_ind+12]]
# skip v_ind+13 because that's the dim_0 variable
dissolved_oxygen[:,:,:]    = nc_v[variables[v_ind+14]]
fecal_coliforms[:,:,:]     = nc_v[variables[v_ind+15]]
irradiance[:,:,:]          = nc_v[variables[v_ind+16]]
irradiance_norm[:,:,:]     = nc_v[variables[v_ind+17]]
# skip v_ind+18 because that's the latitude variable
light_transmission[:,:,:]  = nc_v[variables[v_ind+19]]
# skip v_ind+20 because that's the longitude variable
oxygen_saturation_mg_L[:,:,:]    = nc_v[variables[v_ind+21]]
oxygen_saturation_percent[:,:,:] = nc_v[variables[v_ind+22]]
pH[:,:,:]                        = nc_v[variables[v_ind+23]]
salinity[:,:,:]                  = nc_v[variables[v_ind+24]]
specific_density[:,:,:]          = nc_v[variables[v_ind+25]]
stability[:,:,:]                 = nc_v[variables[v_ind+26]]
surface_irradiance[:,:,:]        = nc_v[variables[v_ind+27]]
temperature[:,:,:]               = nc_v[variables[v_ind+28]]
total_coliforms[:,:,:]           = nc_v[variables[v_ind+29]]
transmissivity[:,:,:]            = nc_v[variables[v_ind+30]]

f.close()

