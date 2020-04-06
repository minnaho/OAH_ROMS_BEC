# San Diego ADCP 
# make 3 separate netCDF files for each (100m, 60m, 36m)
import datetime
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num

xl = pd.ExcelFile('San_Diego_Moored_Data_36m.xlsx')
sheets = xl.sheet_names

# organize by velocities
max_depth = 9
east_start = 8
east_end = east_start+max_depth
north_start = east_end
north_end = north_start+max_depth
vert_start = north_end
vert_end = north_end+max_depth

# get lat/lon for each
lat_lon = []
# unique lat/lon (7 of them)
lat_unique = []
lon_unique = []

loc_unique_len = len(lat_unique)

df_east = pd.DataFrame(columns=range(max_depth))
df_north = pd.DataFrame(columns=range(max_depth))
df_vert = pd.DataFrame(columns=range(max_depth))
df_time = pd.DataFrame()
df_all = pd.DataFrame()
'''
east_array = np.empty((5888,loc_unique_len,max_depth))
east_array.fill(np.nan)

north_array = np.empty((5888,loc_unique_len,max_depth))
north_array.fill(np.nan)

vert_array = np.empty((5888,loc_unique_len,max_depth))
vert_array.fill(np.nan)
'''
east_array = np.empty((5888,max_depth))
east_array.fill(np.nan)

north_array = np.empty((5888,max_depth))
north_array.fill(np.nan)

vert_array = np.empty((5888,max_depth))
vert_array.fill(np.nan)

for ind,sh_i in enumerate(sheets):
    print(sh_i)
    df_load = xl.parse(sh_i,skiprows=range(2,13),header=None,ignore_index=True)
    df_all = df_all.append(df_load)
    # get lat/lon
    #lat_lon.append([df_load[0][0],df_load[1][0]]) 

    # find the lat/lon in the unique list for netCDF indexing 
    #loc_ind = lat_unique.index(df_load[0][0])    
    
    # remove labeling rows
    #df_load = df_load[6:]


    # get date/time by column
    #df_time_temp = df_load.iloc[:,1:6]
    
    # get east, north, & vertical velocities only by column
    #df_east_temp = df_load.iloc[:,east_start:east_end]
    #df_north_temp = df_load.iloc[:,north_start:north_end]
    #df_vert_temp = df_load.iloc[:,vert_start:vert_end]
    

    # append each dataset to previous to conglomerate
    #east_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_east_temp 
    #north_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_north_temp
    #vert_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_vert_temp

    # append each dataset to previous to conglomerate
    #df_time = df_time.append(df_time_temp)
'''
# convert units from mm/s to m/s
east_m_array = east_array/1000.
north_m_array = north_array/1000.
vert_m_array = vert_array/1000.

# get each element of time and convert to datetime and then to num
year = np.copy(df_time[1]+2000)
month = np.copy(df_time[2])
day = np.copy(df_time[3])
hour = np.copy(df_time[4])
minute = np.copy(df_time[5])

time_arr = np.empty(len(year))
for t_i in range(len(year)):
    d_t = datetime.datetime(year[t_i],month[t_i],day[t_i],hour[t_i],minute[t_i])
    time_num = date2num(d_t,'minutes since 2007-12-12-16-43')
    time_arr[t_i] = time_num

'''
'''
####################
# make netCDF file
####################

adcp_data = Dataset('LACSD_ADCP.nc','w')

adcp_data.title = 'Los Angeles County Sanitation District ADCP data for mooring M18'

adcp_data.description = 'eastward, northward, and vertical velocities'
adcp_data.comment = 'location dimension matches with latitude and longitude indexes'

# dimensions
time_dim = adcp_data.createDimension('time',None)
depth_dim = adcp_data.createDimension('depth',76)
loc_dim = adcp_data.createDimension('location',7)


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
depth_var[:] = np.arange(1,77)
lat_var[:] = lat_unique
lon_var[:] = lon_unique

east[:,:] = east_m_array
north[:,:] = north_m_array
vert[:,:] = vert_m_array

time_var.units = 'minutes since 2007-12-12-16-43'
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
'''





