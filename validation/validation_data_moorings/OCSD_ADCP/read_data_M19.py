# OCSD ADCP data
import datetime
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num

xl = pd.ExcelFile('OCSD_M19.xlsx')
sheets = xl.sheet_names

time_units = 'minutes since 2007-03-22 16:01'

max_size = 45

# sheets with 45 instead of 44
sh_45 = ['201312','201401','201405','201502']

# organize by velocities
max_depth = 44
east_start = 9
east_end = east_start+max_depth
north_start = east_end
north_end = north_start+max_depth
vert_start = north_end
vert_end = north_end+max_depth

# get lat/lon for each

lat_unique = [33.59000]
lon_unique = [-118.00640]

loc_unique_len = len(lat_unique)

df_east = pd.DataFrame()
df_north = pd.DataFrame()
df_vert = pd.DataFrame()
df_time = pd.DataFrame()


for ind,sh_i in enumerate(sheets):
    print(sh_i)

    # max depth changes from 44 to 45 in last 4 sheets
    if sh_i in sh_45:
        max_depth = 45
        east_start = 9
        east_end = east_start+max_depth
        north_start = east_end
        north_end = north_start+max_depth
        vert_start = north_end
        vert_end = north_end+max_depth

    df_load = xl.parse(sh_i,skiprows=range(13),header=None,ignore_index=True)
 
    # remove labeling rows
    df_load = df_load[4:]


    # get date/time by column
    df_time_temp = df_load.iloc[:,1:6]
    
    # get east, north, & vertical velocities only by column
    df_east_temp = df_load.iloc[:,east_start:east_end]
    df_north_temp = df_load.iloc[:,north_start:north_end]
    df_vert_temp = df_load.iloc[:,vert_start:vert_end]

    print('df_north_temp length: '+str(df_north_temp.shape[1]))
    print('df_vert_temp length: '+str(df_vert_temp.shape[1]))

    if sh_i in sh_45:
        df_north_temp.columns = list(range(53,53+max_depth))
        df_vert_temp.columns = list(range(97,97+max_depth))

    df_east = df_east.append(df_east_temp,ignore_index=True)
    df_north = df_north.append(df_north_temp,ignore_index=True)
    df_vert = df_vert.append(df_vert_temp,ignore_index=True)
    
    print('df_vert length: '+str(df_vert.shape[1]))

    # append each dataset to previous to conglomerate
    #east_array[ind*256:(ind+1)*256,:max_depth] = df_east_temp 
    #north_array[ind*256:(ind+1)*256,:max_depth] = df_north_temp
    #vert_array[ind*256:(ind+1)*256,:max_depth] = df_vert_temp

    # append each dataset to previous to conglomerate
    df_time = df_time.append(df_time_temp)


# convert units from mm/s to m/s
east_m_array = np.array(df_east.astype(float)/1000.)
north_m_array = np.array(df_north.astype(float)/1000.)
vert_m_array = np.array(df_vert.astype(float)/1000.)

# get each element of time and convert to datetime and then to num
year = np.copy(df_time[1]).astype(int)+2000
month = np.copy(df_time[2]).astype(int)
day = np.copy(df_time[3]).astype(int)
hour = np.copy(df_time[4]).astype(int)
minute = np.copy(df_time[5]).astype(int)

time_arr = np.empty(len(year))
for t_i in range(len(year)):
    d_t = datetime.datetime(year[t_i],month[t_i],day[t_i],hour[t_i],minute[t_i])
    time_num = date2num(d_t,time_units)
    time_arr[t_i] = time_num


####################
# make netCDF file
####################

adcp_data = Dataset('OCSD_M19.nc','w')

adcp_data.title = 'Orange County Sanitation District ADCP data for station M19'

adcp_data.description = '2007-03-22 to 2015-02-25, 1 m bins, 6 min frequency'

# dimensions
time_dim = adcp_data.createDimension('time',len(year))
depth_dim = adcp_data.createDimension('depth',max_size)
loc_dim = adcp_data.createDimension('location',1)


# variables
time_var = adcp_data.createVariable('time',np.float64,('time',))
depth_var = adcp_data.createVariable('depth',np.float32,('depth',))
lat_var = adcp_data.createVariable('latitude',np.float32,('location',))
lon_var = adcp_data.createVariable('longitude',np.float32,('location',))

east = adcp_data.createVariable('u',np.float32,('time','depth'))
north = adcp_data.createVariable('v',np.float32,('time','depth'))
vert = adcp_data.createVariable('w',np.float32,('time','depth'))

# assign values
time_var[:] = time_arr
depth_var[:] = np.arange(1,max_size+1)
lat_var[:] = lat_unique
lon_var[:] = lon_unique

east[:,:] = east_m_array
north[:,:] = north_m_array
vert[:,:] = vert_m_array

time_var.units = time_units
depth_var.units = 'm from bottom'
lat_var.units = 'degrees north'
lon_var.units = 'degrees east'

east.units = 'm/s'
north.units = 'm/s'
vert.units = 'm/s'

east.long_name = 'eastward_velocity'
north.long_name = 'northward_velocity'
vert.long_name = 'vertical_velocity'

adcp_data.close()






