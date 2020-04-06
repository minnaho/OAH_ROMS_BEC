# San Diego ADCP 
# make 3 separate netCDF files for each (100m, 60m, 36m)
import datetime
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num

xl = pd.ExcelFile('San_Diego_Moored_Data_100m.xlsx')
sheets = xl.sheet_names

time_units = 'minutes since 2006-08-31 08:39'

bin_2m = sheets[:3]+sheets[5:9]

# organize by velocities
max_depth = 25
east_start = 8
east_end = east_start+max_depth
north_start = east_end
north_end = north_start+max_depth
vert_start = north_end
vert_end = north_end+max_depth

# unique lat/lon (1 of them)
lat_unique = [32.66683333]
lon_unique = [-117.32687]
'''
df_east_2m = pd.DataFrame()
df_north_2m = pd.DataFrame()
df_vert_2m = pd.DataFrame()

df_east_4m = pd.DataFrame()
df_north_4m = pd.DataFrame()
df_vert_4m = pd.DataFrame()
'''

df_east = pd.DataFrame()
df_north = pd.DataFrame()
df_vert = pd.DataFrame()

df_time = pd.DataFrame()
df_all = pd.DataFrame()
'''
east_array = np.empty((5888,max_depth))
east_array.fill(np.nan)

north_array = np.empty((5888,max_depth))
north_array.fill(np.nan)

vert_array = np.empty((5888,max_depth))
vert_array.fill(np.nan)
'''
for ind,sh_i in enumerate(sheets):
    print(sh_i)
    df_load = xl.parse(sh_i,skiprows=range(0,12),header=None,ignore_index=True)
    df_load = df_load.convert_objects(convert_numeric=True)
    #df_all = df_all.append(df_load)
 
    # remove labeling rows
    df_load = df_load[6:]

    # get east, north, & vertical velocities only by column
    if sh_i in bin_2m:
        max_depth = 50
        east_end = east_start+max_depth
        north_start = east_end
        north_end = north_start+max_depth
        vert_start = north_end
        vert_end = north_end+max_depth

        df_east_temp = df_load.iloc[:,east_start:east_end]
        df_north_temp = df_load.iloc[:,north_start:north_end]
        df_vert_temp = df_load.iloc[:,vert_start:vert_end]
    
        print('df_vert_temp column length: '+str(len(df_vert_temp.columns)))

        df_east = df_east.append(df_east_temp)
        df_north = df_north.append(df_north_temp,ignore_index=True)
        df_vert = df_vert.append(df_vert_temp)

        #df_east_2m = df_east_2m.append(df_east_temp)
        #df_north_2m = df_north_2m.append(df_north_temp)
        #df_vert_2m = df_vert_2m.append(df_vert_temp)


    elif sh_i not in bin_2m:
        max_depth = 25
        east_end = east_start+max_depth
        north_start = east_end
        north_end = north_start+max_depth
        vert_start = north_end
        vert_end = north_end+max_depth

        if sh_i == '2014 0512-0914':
            max_depth = 24
            east_end = east_start+max_depth
            north_start = east_end
            north_end = north_start+max_depth
            vert_start = north_end
            vert_end = north_end+max_depth

        df_east_temp = df_load.iloc[:,east_start:east_end]
        df_north_temp = df_load.iloc[:,north_start:north_end]
        df_vert_temp = df_load.iloc[:,vert_start:vert_end]

        print('df_vert_temp column length: '+str(len(df_vert_temp.columns)))

        df_nan = np.empty((len(df_east_temp[10])))
        df_nan.fill(np.nan)
        idx_in = list(range(1,max_depth*2,2))
        for df_i in idx_in:
            df_east_temp.insert(df_i,'',df_nan,allow_duplicates=True)
            df_north_temp.insert(df_i,'',df_nan,allow_duplicates=True)
            df_vert_temp.insert(df_i,'',df_nan,allow_duplicates=True)
        
        # name columns for df_east_temp the same as df_east so it can append
        if sh_i == '2014 0512-0914':
            df_east_temp.columns = list(df_east.columns[:-2])
            df_north_temp.columns = list(df_north.columns[:-2])
            df_vert_temp.columns = list(df_vert.columns[:-2])

        elif sh_i != '2014 0512-0914':
            df_east_temp.columns = list(df_east.columns)
            df_north_temp.columns = list(df_north.columns)
            df_vert_temp.columns = list(df_vert.columns)


        df_east = df_east.append(df_east_temp,ignore_index=True)
        df_north = df_north.append(df_north_temp,ignore_index=True)
        df_vert = df_vert.append(df_vert_temp,ignore_index=True)
        #df_east_4m = df_east_4m.append(df_east_temp)
        #df_north_4m = df_north_4m.append(df_north_temp)
        #df_vert_4m = df_vert_4m.append(df_vert_temp)
  

    # append each dataset to previous to concatenate

    #east_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_east_temp 
    #north_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_north_temp
    #vert_array[ind*256:(ind+1)*256,loc_ind,:max_depth] = df_vert_temp

    # get date/time by column
    df_time_temp = df_load.iloc[:,1:6]

    # append each dataset to previous to concatenate
    df_time = df_time.append(df_time_temp)

# get each element of time and convert to datetime and then to num
year = np.copy(df_time[1]+2000).astype(int)
month = np.copy(df_time[2]).astype(int)
day = np.copy(df_time[3]).astype(int)
hour = np.copy(df_time[4]).astype(int)
minute = np.copy(df_time[5]).astype(int)

time_arr = np.empty(len(year))
for t_i in range(len(year)):
    d_t = datetime.datetime(year[t_i],month[t_i],day[t_i],hour[t_i],minute[t_i])
    time_num = date2num(d_t,time_units)
    time_arr[t_i] = time_num

# convert to arrays
east_m_array = np.array(df_east/1000.)
north_m_array = np.array(df_north/1000.)
vert_arr = np.array(df_vert/1000.)



####################
# make netCDF file
####################

adcp_data = Dataset('SD_ADCP_100m.nc','w')

adcp_data.title = 'San Diego 100 meter ADCP data from Wendy Enright from San Diego Public Utilities Department'

adcp_data.description = '2006-08-31 to 2017-12-31, 2-4 m bins, 3-5 min frequency'

# dimensions
time_dim = adcp_data.createDimension('time',len(year))
depth_dim = adcp_data.createDimension('depth',east_m_array.shape[1])
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
depth_var[:] = np.arange(2,102,2)
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






