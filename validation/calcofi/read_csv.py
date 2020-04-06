############################
# get agency survey csv data
# and organize into netCDF
##########################
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num
from collections import defaultdict
from scipy.stats import mode
from scipy import io as sio
################
# load data
################
# get lat/lon/date/wind/etc csv file
cast_csv = pd.read_csv('CalCOFI_Cast.csv',sep=',',parse_dates=True,low_memory=False)

# get bottle data file (water quality, temp, salinity, etc.)
bottle_csv = pd.read_csv('CalCOFI_Bottle.csv',low_memory=False,encoding='ISO-8859-1')

############################
# time, lat/lon, depth data
###########################
# change all null times to 00:00:00
for i,t in enumerate(cast_csv['Time']):
    if pd.isnull(t) == True:
        cast_csv['Time'][i] = '00:00:00'

# get dates and time and turn to datetime objects
cast_csv['datetime'] = pd.to_datetime(cast_csv['Date']+' '+cast_csv['Time'],format='%m/%d/%Y %H:%M:%S')
# convert dates to num
date_list = list(cast_csv['datetime'])
time_nc = date2num(date_list,'minutes since 1949-03-01 09:30:00')

# get unique depths
depth_all = np.copy(bottle_csv['Depthm'])
depth_unique = np.copy(sorted(list(set(depth_all))))

# get unique station IDs for lat/lon
station_all = np.copy(cast_csv['Sta_ID'])
station_unique = np.copy(sorted(list(set(station_all))))

# find all lat/lon for each station ID 
# and take mode to get lat/lon of each station
lat_unique = np.empty((len(station_unique)))
lon_unique = np.empty((len(station_unique)))
for i_ind,i_sta in enumerate(station_unique):
    # find indexes where station IDs match match
    lat_lon_inds = np.where(cast_csv['Sta_ID']==i_sta)
    # make list of latitudes/longs associated with that station ID
    lat_list = [np.copy(cast_csv['Lat_Dec'][x]) for x in lat_lon_inds]
    lon_list = [np.copy(cast_csv['Lon_Dec'][x]) for x in lat_lon_inds]
    # find mode in each lat/lon list
    lat_mode = mode(lat_list)
    lon_mode = mode(lon_list)
    # assign the mode of the lat/lon to each station ID (by same index)
    lat_unique[i_ind] = lat_mode[0][0][0]
    lon_unique[i_ind] = lon_mode[0][0][0]
     

####################################
# slice variables in both datasets
###################################

# remove unnecessary variables from bottle_csv
bottle_csv = bottle_csv.drop(['Btl_Cnt','Depth_ID','Oxy_µmol/Kg','BtlNum','RecInd','T_prec','T_qual','S_prec','S_qual','P_qual','O_qual','SThtaq','O2Satq','Chlqua','Phaqua','PO4q','SiO3qu','NO2q','NO3q','NH3q','C14As1','C14A1p','C14A1q','C14As2','C14A2p','C14A2q','DarkAs','DarkAp','DarkAq','MeanAp','MeanAq','IncTim','R_Depth','R_TEMP','R_POTEMP','R_SALINITY','R_SIGMA','R_SVA', 'R_DYNHT', 'R_O2', 'R_O2Sat', 'R_SIO3', 'R_PO4', 'R_NO3','R_NO2', 'R_NH4', 'R_CHLA', 'R_PHAEO', 'R_PRES', 'R_SAMP','R_Oxy_µmol/Kg','DIC2','TA2','pH2','DIC Quality Comment'],axis=1)

# list of variables to save into netCDF4 from cast_csv
# that are not lat/lon
cast_vars = ['Bottom_D','IntChl','IntC14','Wave_Dir','Wave_Ht','Wave_Prd','Wind_Dir','Wind_Spd','Barometer','Dry_T','Wet_T','Wea','Cloud_Typ','Cloud_Amt', 'Visibility']

# variables renamed for netCDF4
variables = [
            'temperature',                      
            'salinity',                      
            'O2',                      
            'potential_density',                      
            'O2_sat',                      
            'chlorophyll_a',                      
            'phaeophytin',                      
            'PO4',                                            
            'SiO3',                      
            'NO2',                      
            'NO3',                      
            'NH3',                      
            'carbon_assimilation',
            'light_intensity',                      
            'DIC',                      
            'total_alk',                      
            'pH',                      
            'bottom_depth',
            'integrated_chlorophyll',
            'integrated_primary_prod',
            'wave_direction',
            'wave_height',
            'wave_period',
            'wind_dir',
            'wind_speed',
            'atmos_press',
            'dry_air_T',
            'wet_air_T',
            'weather',
            'cloud_typ',
            'cloud_amt',
            'visibility']

##########################
# TURN PANDAS DF INTO MATLAB
#############################

# create arrays of time, lat, lon, and cast variables
# to add to bottle_csv
time_bottle = np.empty(len(bottle_csv['Cst_Cnt']))
lat_bottle = np.empty(len(bottle_csv['Cst_Cnt']))
lon_bottle = np.empty(len(bottle_csv['Cst_Cnt']))
bottom_depth_bottle             = np.empty(len(bottle_csv['Cst_Cnt']))
integrated_chlorophyll_bottle    = np.empty(len(bottle_csv['Cst_Cnt']))
integrated_primary_prod_bottle  = np.empty(len(bottle_csv['Cst_Cnt']))
wave_direction_bottle           = np.empty(len(bottle_csv['Cst_Cnt']))
wave_height_bottle              = np.empty(len(bottle_csv['Cst_Cnt']))
wave_period_bottle              = np.empty(len(bottle_csv['Cst_Cnt']))
wind_dir_bottle                 = np.empty(len(bottle_csv['Cst_Cnt']))
wind_speed_bottle               = np.empty(len(bottle_csv['Cst_Cnt']))
atmos_press_bottle              = np.empty(len(bottle_csv['Cst_Cnt']))
dry_air_T_bottle                = np.empty(len(bottle_csv['Cst_Cnt']))
wet_air_T_bottle                = np.empty(len(bottle_csv['Cst_Cnt']))
weather_bottle                  = np.empty(len(bottle_csv['Cst_Cnt']))
cloud_typ_bottle                = np.empty(len(bottle_csv['Cst_Cnt']))
cloud_amt_bottle                = np.empty(len(bottle_csv['Cst_Cnt']))
visibility_bottle               = np.empty(len(bottle_csv['Cst_Cnt']))

# assign lat/lon columns to lat/lon of that station
for i in range(len(bottle_csv['Cst_Cnt'])):
    print(str(i)+' of '+str(len(bottle_csv['Cst_Cnt'])))
    ind_lat_lon = np.where(station_unique==bottle_csv['Sta_ID'][i])[0][0] 
    lat_bottle[i] = lat_unique[ind_lat_lon]
    lon_bottle[i] = lon_unique[ind_lat_lon]
    ind_datetime = np.where(cast_csv['Cst_Cnt']==bottle_csv['Cst_Cnt'][i])[0][0]
    time_bottle[i] = time_nc[ind_datetime]
    bottom_depth_bottle[i] = np.copy(cast_csv['Bottom_D'][ind_datetime])           
    integrated_chlorophyll_bottle[i] = np.copy(cast_csv['IntChl'][ind_datetime])    
    integrated_primary_prod_bottle[i] = np.copy(cast_csv['IntC14'][ind_datetime])    
    wave_direction_bottle[i]          = np.copy(cast_csv['Wave_Dir'][ind_datetime])    
    wave_height_bottle[i]             = np.copy(cast_csv['Wave_Ht'][ind_datetime])    
    wave_period_bottle[i]             = np.copy(cast_csv['Wave_Prd'][ind_datetime])    
    wind_dir_bottle[i]                = np.copy(cast_csv['Wind_Dir'][ind_datetime])    
    wind_speed_bottle[i]              = np.copy(cast_csv['Wind_Spd'][ind_datetime])    
    atmos_press_bottle[i]             = np.copy(cast_csv['Barometer'][ind_datetime])    
    dry_air_T_bottle[i]               = np.copy(cast_csv['Dry_T'][ind_datetime])    
    wet_air_T_bottle[i]               = np.copy(cast_csv['Wet_T'][ind_datetime])    
    weather_bottle[i]                 = np.copy(cast_csv['Wea'][ind_datetime])    
    cloud_typ_bottle[i]               = np.copy(cast_csv['Cloud_Typ'][ind_datetime])    
    cloud_amt_bottle[i]               = np.copy(cast_csv['Cloud_Amt'][ind_datetime])    
    visibility_bottle[i]              = np.copy(cast_csv['Visibility'][ind_datetime])    

# add columns time, latitude, and longitude to bottle_csv df
bottle_csv.insert(0,'datetime',time_bottle)
bottle_csv.insert(1,'latitude',lat_bottle)
bottle_csv.insert(2,'longitude',lon_bottle)

# add columns for variables in cast_csv
bottle_csv.insert(4,'bottom_depth',bottom_depth_bottle)
bottle_csv.insert(4,'integrated_chlorophyll',integrated_chlorophyll_bottle)
bottle_csv.insert(4,'integrated_primary_prod',integrated_primary_prod_bottle)
bottle_csv.insert(4,'wave_direction',wave_direction_bottle)
bottle_csv.insert(4,'wave_height',wave_height_bottle)
bottle_csv.insert(4,'wave_period',wave_period_bottle)
bottle_csv.insert(4,'wind_dir',wind_dir_bottle)
bottle_csv.insert(4,'wind_speed',wind_speed_bottle)
bottle_csv.insert(4,'atmos_press',atmos_press_bottle)
bottle_csv.insert(4,'dry_air_T',dry_air_T_bottle)
bottle_csv.insert(4,'wet_air_T',wet_air_T_bottle)
bottle_csv.insert(4,'weather',weather_bottle)
bottle_csv.insert(4,'cloud_typ',cloud_typ_bottle)
bottle_csv.insert(4,'cloud_amt',cloud_amt_bottle)
bottle_csv.insert(4,'visibility',visibility_bottle)

bottle_csv = bottle_csv.drop(['Cst_Cnt','Sta_ID'],axis=1)

# rename columns
bottle_csv.rename(index=str,columns={
'Depthm':'depth',   
'T_degC':'temperature',         
'Salnty':'salinity',           
'O2ml_L':'O2',                 
'STheta':'potential_density',   
'O2Sat':'O2_sat',             
'ChlorA':'chlorophyll_a',      
'Phaeop':'phaeophytin',        
'PO4uM':'PO4',                
'SiO3uM':'SiO3',               
'NO2uM':'NO2',                
'NO3uM':'NO3',                
'NH3uM':'NH3',                
'MeanAs':'carbon_assimilation',
'LightP':'light_intensity',    
'DIC1':'DIC',                
'TA1':'total_alk',          
'pH1':'pH'},inplace=True)                 

# add column with units in last column
units_list = [ 
'datetime = minutes since 1949-03-01 09:30:00',
'latitude = degrees north',
'longitude = degrees east',
'depths = m',
'temperature = degrees C',    
'salinity = psu', 
'O2 = mL/L', 
'potential_density = kg/m3', 
'O2_sat = %', 
'chlorophyll_a = ug/L', 
'phaeophytin = ug/L', 
'PO4 = umol/L', 
'SiO3 = umol/L', 
'NO2 = umol/L', 
'NO3 = umol/L', 
'NH3 = umol/L', 
'carbon_assimilation = mg C/m3', 
'light_intensity = %', 
'DIC = umol/kg', 
'total_alk = umol/kg', 
'bottom_depth = m', 
'integrated_chlorophyll = mg/m2', 
'integrated_primary_prod = mg C/m2',
'wave_direction = abbreviated 360 azimuth circle with 00 representing True North, 18 represents 180',
'wave_height = ft', 
'wave_period = seconds',
'wind_dir = abbreviated 360 azimuth circle with 00 representing True North, 18 represents 180', 
'wind_speed = knots', 
'atmos_press = mbar',
'dry_air_T = degrees C', 
'wet_air_T = degrees C', 
'weather = 1 Digit Code from The World Meteorological Organization.  Code source WMO 4501, see http://www.jodc.go.jp/data_format/weather-code.html', 
'cloud_typ = 1 Digit Code from The World Meteorological Organization.  Code source WMO 0500, see http://www.jodc.go.jp/data_format/weather-code.html', 
'cloud_amt = 1 Digit Code from The World Meteorological Organization.  Code source WMO 2700, see http://www.jodc.go.jp/data_format/weather-code.html', 
'visibility = 1 Digit Code from The World Meteorological Organization.  Code source WMO 4300, see http://www.jodc.go.jp/data_format/weather-code.html' 
]


bottle_csv.insert(0,'units',np.nan*len(bottle_csv['datetime']))
bottle_csv['units'][:len(units_list)] = units_list[:]

# multiindex pandas
bottle_csv_ind = bottle_csv.set_index(['datetime','longitude','latitude','depth'])

# dictionary structure
bottle_dict = {col_name : bottle_csv[col_name].values for col_name in bottle_csv.columns.values}
bottle_dict_ind = {col_name : bottle_csv_ind[col_name].values for col_name in bottle_csv_ind.columns.values}
'''
bottle_csv.to_csv('calcofi_database.csv',index=False)
bottle_csv_ind.to_csv('calcofi_database_ind.csv',index=False)
sio.savemat('test_calcofi.mat',{'struct':bottle_dict})
sio.savemat('test_calcofi_ind.mat',{'struct':bottle_dict_ind})
bottle_csv.to_csv('calcofi_database.dat',sep='|')
'''

'''
# get data from CalCOFI_Bottle.csv and put into 3D array (time,station,depth)

#create HDF5 file (numpy can't store data this huge)
h5_file = h5.File('calcofi_database.hdf5','w')

# skip key 'Cst_Cnt' and 'Sta_ID'
v_i = 0
for key in bottle_csv.keys()[2:]:
    print(variables[v_i])
    var_temp = h5_file.create_dataset(variables[v_i],(len(time_nc),len(station_unique),len(depth_unique)),dtype='float32')
    data = bottle_csv[key] 
    for d_i in range(len(data)):
        # find where station_unique equals bottle_csv['Sta_ID']
        station_ind = np.where(station_unique==bottle_csv['Sta_ID'][d_i])
        s = station_ind[0][0]
        # -1 because cast count starts at 1
        t = np.where(cast_csv['Cst_Cnt']==bottle_csv['Cst_Cnt'][d_i])[0][0]-1
        d = np.where(depth_unique==depth_all[d_i])[0][0]
        var_temp[t,s,d] = data[d_i]
    # put dictionary key as variable name for netCDF4
    v_i += 1

# get data from CalCofi_Cast.csv and put in 2D array (time,station)
for key_cast in cast_vars:
    print(variables[v_i])
    var_temp_cast = h5_file.create_dataset(variables[v_i],(len(time_nc),len(station_unique)),dtype='float32')
    data_cast = cast_csv[key_cast]
    for d_i_cast in range(len(data)):
        s_c = np.where(station_unique==cast_csv['Sta_ID'][d_i_cast])[0][0]
        # -1 because cast count starts at 1
        t_c = cast_csv['Cst_Cnt'][d_i_cast]-1
        var_temp_cast[t_c,s_c] = data_cast[d_i_cast]
    v_i += 1
'''
'''
#####################
# make netCDF file
####################
f = Dataset('calcofi_database.nc','w')

f.title = 'CalCOFI Sampling Cast and Bottle Database 1949-2017'

# dimensions
time = f.createDimension('time',len(time_nc))
position = f.createDimension('station',len(station_unique))
depth = f.createDimension('depth',len(depth_unique))

# variables
times = f.createVariable('time',np.float64,('time',))
positions = f.createVariable('position',np.float64,('position',))
depths = f.createVariable('depth',np.float32,('depth',))

lats = f.createVariable('latitude',np.float32,('lat',))
lons = f.createVariable('longitude',np.float32,('lon',))


v_i = 0
temperature             = f.createVariable(variables[v_i],np.float32,('time','position','depth'))
salinity                = f.createVariable(variables[v_i+1],np.float32,('time','position','depth'))
O2                      = f.createVariable(variables[v_i+2],np.float32,('time','position','depth'))
potential_density       = f.createVariable(variables[v_i+3],np.float32,('time','position','depth'))
O2_sat                  = f.createVariable(variables[v_i+4],np.float32,('time','position','depth'))
chlorophyll_a           = f.createVariable(variables[v_i+5],np.float32,('time','position','depth'))
phaeophytin             = f.createVariable(variables[v_i+6],np.float32,('time','position','depth'))
PO4                     = f.createVariable(variables[v_i+7],np.float32,('time','position','depth'))
SiO3                    = f.createVariable(variables[v_i+8],np.float32,('time','position','depth'))
NO2                     = f.createVariable(variables[v_i+9],np.float32,('time','position','depth'))
NO3                     = f.createVariable(variables[v_i+10],np.float32,('time','position','depth'))
NH3                     = f.createVariable(variables[v_i+11],np.float32,('time','position','depth'))
carbon_assimilation     = f.createVariable(variables[v_i+12],np.float32,('time','position','depth'))
light_intensity         = f.createVariable(variables[v_i+13],np.float32,('time','position','depth'))
DIC                     = f.createVariable(variables[v_i+14],np.float32,('time','position','depth'))
total_alk               = f.createVariable(variables[v_i+15],np.float32,('time','position','depth'))
pH                      = f.createVariable(variables[v_i+16],np.float32,('time','position','depth'))
bottom_depth            = f.createVariable(variables[v_i+17],np.float32,('time','position'))
integrated_chlorophyll  = f.createVariable(variables[v_i+18],np.float32,('time','position'))
integrated_primary_prod = f.createVariable(variables[v_i+19],np.float32,('time','position'))
wave_direction          = f.createVariable(variables[v_i+20],np.float32,('time','position'))
wave_height             = f.createVariable(variables[v_i+21],np.float32,('time','position'))
wave_period             = f.createVariable(variables[v_i+22],np.float32,('time','position'))
wind_dir                = f.createVariable(variables[v_i+23],np.float32,('time','position'))
wind_speed              = f.createVariable(variables[v_i+24],np.float32,('time','position'))
atmos_press             = f.createVariable(variables[v_i+25],np.float32,('time','position'))
dry_air_T               = f.createVariable(variables[v_i+26],np.float32,('time','position'))
wet_air_T               = f.createVariable(variables[v_i+27],np.float32,('time','position'))
weather                 = f.createVariable(variables[v_i+28],np.float32,('time','position'))
cloud_typ               = f.createVariable(variables[v_i+29],np.float32,('time','position'))
cloud_amt               = f.createVariable(variables[v_i+30],np.float32,('time','position'))
visibility              = f.createVariable(variables[v_i+31],np.float32,('time','position'))

# units
times.units = 'minutes since 1949-03-01 09:30:00'
positions.units = 'sampling site, each index matches to lat/lon index'
depths.units = 'm'

lats.units = 'degrees north'
lons.units = 'degrees east'

temperature.units           = 'degrees C'       
salinity.units              = 'psu' 
O2.units                    = 'mL/L' 
potential_density.units     = 'kg/m3' 
O2_sat.units                = '%' 
chlorophyll_a.units         = 'ug/L' 
phaeophytin.units           = 'ug/L' 
PO4.units                   = 'umol/L' 
SiO3.units                  = 'umol/L' 
NO2.units                   = 'umol/L' 
NO3.units                   = 'umol/L' 
NH3.units                   = 'umol/L' 
carbon_assimilation.units   = 'mg C/m3' 
light_intensity.units       = '%' 
DIC.units                   = 'umol/kg' 
total_alk.units             = 'umol/kg' 
bottom_depth.units          = 'm' 
integrated_chlorophyll.units  = 'mg/m2' 
integrated_primary_prod.units = 'mg C/m2'
wave_direction.units        = 'abbreviated 360 azimuth circle with 00 representing True North, 18 represents 180' 
wave_height.units           = 'ft' 
wave_period.units           = 'seconds'
wind_dir.units              = 'abbreviated 360 azimuth circle with 00 representing True North, 18 represents 180' 
wind_speed.units            = 'knots' 
atmos_press.units           = 'mbar'
dry_air_T.units             = 'degrees C' 
wet_air_T.units             = 'degrees C' 
weather.units               = '1 Digit Code from The World Meteorological Organization.  Code source WMO 4501, see http://www.jodc.go.jp/data_format/weather-code.html' 
cloud_typ.units             = '1 Digit Code from The World Meteorological Organization.  Code source WMO 0500, see http://www.jodc.go.jp/data_format/weather-code.html' 
cloud_amt.units             = '1 Digit Code from The World Meteorological Organization.  Code source WMO 2700, see http://www.jodc.go.jp/data_format/weather-code.html' 
visibility.units            = '1 Digit Code from The World Meteorological Organization.  Code source WMO 4300, see http://www.jodc.go.jp/data_format/weather-code.html' 

# assign values to variables
times[:] = time_nc
positions[:] = np.arange(len(station_unique))
depths[:] = depth_unique

lats[:] = lat_unique
lons[:] = lat_unique

v_ind = 0
temperature[:,:,:]            = nc_v[variables[v_ind]]
salinity[:,:,:]               = nc_v[variables[v_ind+1]]
O2[:,:,:]                     = nc_v[variables[v_ind+2]]
potential_density[:,:,:]      = nc_v[variables[v_ind+3]]
O2_sat[:,:,:]                 = nc_v[variables[v_ind+4]]
chlorophyll_a[:,:,:]          = nc_v[variables[v_ind+5]]
phaeophytin[:,:,:]            = nc_v[variables[v_ind+6]]
PO4[:,:,:]                    = nc_v[variables[v_ind+7]]
SiO3[:,:,:]                   = nc_v[variables[v_ind+8]]
NO2[:,:,:]                    = nc_v[variables[v_ind+9]]
NO3[:,:,:]                    = nc_v[variables[v_ind+10]]
NH3[:,:,:]                    = nc_v[variables[v_ind+11]]
carbon_assimilation[:,:,:]    = nc_v[variables[v_ind+12]]
light_intensity[:,:,:]        = nc_v[variables[v_ind+13]]
DIC[:,:,:]                    = nc_v[variables[v_ind+14]]
total_alk[:,:,:]              = nc_v[variables[v_ind+15]]
pH[:,:,:]                     = nc_v[variables[v_ind+16]]
bottom_depth[:,:]             = nc_v[variables[v_ind+17]]
integrated_chlorophyll[:,:]   = nc_v[variables[v_ind+18]]
integrated_primary_prod[:,:]  = nc_v[variables[v_ind+19]]
wave_direction[:,:]           = nc_v[variables[v_ind+20]]
wave_height[:,:]              = nc_v[variables[v_ind+21]]
wave_period[:,:]              = nc_v[variables[v_ind+22]]
wind_dir[:,:]                 = nc_v[variables[v_ind+23]]
wind_speed[:,:]               = nc_v[variables[v_ind+24]]
atmos_press[:,:]              = nc_v[variables[v_ind+25]]
dry_air_T[:,:]                = nc_v[variables[v_ind+26]]
wet_air_T[:,:]                = nc_v[variables[v_ind+27]] 
weather[:,:]                  = nc_v[variables[v_ind+28]] 
cloud_typ[:,:]                = nc_v[variables[v_ind+29]]
cloud_amt[:,:]                = nc_v[variables[v_ind+30]]
visibility[:,:]               = nc_v[variables[v_ind+31]]

f.close()
'''
