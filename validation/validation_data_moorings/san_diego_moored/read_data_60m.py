# San Diego ADCP 
# make 3 separate netCDF files for each (100m, 60m, 36m)
import datetime
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num

xl = pd.ExcelFile('San_Diego_Moored_Data_60m.xlsx')
sheets = xl.sheet_names

# find index where lat/lon changes
new_ind = sheets.index('2010 0326-0819')
new_sheets = sheets[new_ind:]

time_units = 'minutes since 2007-08-29 11:51'

# organize by velocities
max_depth = 15
east_start = 8
east_end = east_start+max_depth
north_start = east_end
north_end = north_start+max_depth
vert_start = north_end
vert_end = north_end+max_depth

# unique lat/lon (2 of them)
lat_unique = [32.669655,32.6286666666666]
lon_unique = [-117.281731666666,-117.273583333333]

loc_unique_len = len(lat_unique)

df_east = pd.DataFrame()
df_north = pd.DataFrame()
df_vert = pd.DataFrame()

df_new_east = pd.DataFrame()
df_new_north = pd.DataFrame()
df_new_vert = pd.DataFrame()

df_time = pd.DataFrame()
df_all = pd.DataFrame()
for ind,sh_i in enumerate(sheets):
    print(sh_i)
    df_load = xl.parse(sh_i,skiprows=range(0,12),header=None,ignore_index=True)
    df_all = df_all.append(df_load)
 
    # remove labeling rows
    df_load = df_load[4:]


    # get date/time by column
    df_time_temp = df_load.iloc[:,1:6]
    
    # get east, north, & vertical velocities only by column
    df_east_temp = df_load.iloc[:,east_start:east_end]
    df_north_temp = df_load.iloc[:,north_start:north_end]
    df_vert_temp = df_load.iloc[:,vert_start:vert_end]
    

    # append each dataset to previous to concatenate
    if sh_i in new_sheets:
        df_new_east = df_new_east.append(df_east_temp)
        df_new_north = df_new_north.append(df_north_temp)
        df_new_vert = df_new_vert.append(df_vert_temp)
    elif sh_i not in new_sheets: 
        df_east = df_east.append(df_east_temp)
        df_north = df_north.append(df_north_temp)
        df_vert = df_vert.append(df_vert_temp)
    #east_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_east_temp 
    #north_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_north_temp
    #vert_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_vert_temp

    # append each dataset to previous to concatenate
    df_time = df_time.append(df_time_temp)

# get each element of time and convert to datetime and then to num
year = np.copy(df_time[1]+2000)
month = np.copy(df_time[2])
day = np.copy(df_time[3])
hour = np.copy(df_time[4])
minute = np.copy(df_time[5])

time_arr = np.empty(len(year))
for t_i in range(len(year)):
    d_t = datetime.datetime(year[t_i],month[t_i],day[t_i],hour[t_i],minute[t_i])
    time_num = date2num(d_t,time_units)
    time_arr[t_i] = time_num

# convert to arrays
east_array = np.empty((len(year),len(lat_unique),max_depth))
east_array.fill(np.nan)

north_array = np.empty((len(year),len(lat_unique),max_depth))
north_array.fill(np.nan)

vert_array = np.empty((len(year),len(lat_unique),max_depth))
vert_array.fill(np.nan)

east_array[:len(df_east),0,:] = df_east
east_array[len(df_east):,1,:] = df_new_east

north_array[:len(df_north),0,:] = df_north
north_array[len(df_north):,1,:] = df_new_north

vert_array[:len(df_vert),0,:] = df_vert
vert_array[len(df_vert):,1,:] = df_new_vert

east_m_array = east_array/1000.
north_m_array = north_array/1000.
vert_m_array = vert_array/1000.


####################
# make netCDF file
####################
adcp_data = Dataset('SD_ADCP_60m.nc','w')

adcp_data.title = 'San Diego 60 meter ADCP data from Wendy Enright from San Diego Public Utilities Department'

adcp_data.comment = 'location dimension matches with latitude and longitude indexes'
adcp_data.description = '2007-08-29 to 2013-11-25, 4 m bins, 3-5 min frequency'

# dimensions
time_dim = adcp_data.createDimension('time',len(year))
depth_dim = adcp_data.createDimension('depth',max_depth)
loc_dim = adcp_data.createDimension('location',len(lat_unique))

# variables
time_var = adcp_data.createVariable('time',np.float64,('time',))
depth_var = adcp_data.createVariable('depth',np.float32,('depth',))
lat_var = adcp_data.createVariable('latitude',np.float32,('location',))
lon_var = adcp_data.createVariable('longitude',np.float32,('location',))

east = adcp_data.createVariable('u',np.float32,('time','location','depth'))
north = adcp_data.createVariable('v',np.float32,('time','location','depth'))
vert = adcp_data.createVariable('w',np.float32,('time','location','depth'))

# assign values
time_var[:] = time_arr
depth_var[:] = np.arange(4,(max_depth*4)+4,4)
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






