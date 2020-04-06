########################
# read adcp data
# from LACSD
#######################
import pandas as pd
import numpy as np
import glob
from netCDF4 import Dataset,num2date,date2num

start_time_netcdf = 'minutes since 2000-10-31 00:15'

xl_files = sorted(glob.glob('/data/project1/minnaho/validation/validation_data_moorings/PV_moored/A*'))

files_86 = ['/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AE_lacsd_palos_verdes_sampling.xlsx','/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AF_lacsd_palos_verdes_sampling.xlsx']

files_17 = ['/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AH_lacsd_palos_verdes_sampling.xlsx','/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AJ_lacsd_palos_verdes_sampling.xlsx','/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AK_lacsd_palos_verdes_sampling.xlsx','/data/project1/minnaho/validation/validation_data_moorings/PV_moored/AL_lacsd_palos_verdes_sampling.xlsx']

depths_86 = ['5m', '8m', '11m', '14m', '17m', '20m', '23m', '26m', '29m', '32m', '35m', '38m', '41m', '44m', '47m', '50m', '53m', '56m', '59m', '62m', '65m', '68m', '71m', '74m', '77m', '80m', '83m', '86m']

depths_17 = ['1.25m', '2.75m', '2m', '4.25m', '5.75m', '5m', '7.25m', '8.75m', '8m', '10.25m', '11.75m', '11m', '13.25m', '14.75m', '14m', '16.25m', '17.75m', '17']

depths_20 = ['1.25m', '2.75m', '2m', '4.25m', '5.75m', '5m', '7.25m', '8.75m', '8m', '10.25m', '11.75m', '11m', '13.25m', '14.75m', '14m', '16.25m', '17.75m', '17', '19.25m', '20.75m', '20m']


lats = []
lons = []
for f_i in xl_files:
    xl = pd.ExcelFile(f_i)
    sheets = xl.sheet_names 
    print('\n'+f_i)
    print(sheets)
    # get lat/lon
    df_load = xl.parse(sheets[0],header=None,ignore_index=True)
    print(df_load[0][1])
    lats.append(df_load[1][2])
    lons.append(df_load[2][2])


'''
# max length of time/depth array
time_length = []
depth_length = []

for f_i in csv_files:
    temp_file = pd.read_csv(f_i,skiprows=range(6),header=None)
    #temp_time = range(0,len(temp_file)*15,15) # sampling frequency of 15 min
    time_length.append(len(temp_file))
    depth_length.append(temp_file.shape[1])

max_time = np.max(time_length)
#max_depth = np.max(depth_length)
time_arr = np.arange(0,max_time*15,15)
#depth_arr = np.arange(2,((max_depth-1)*3)-1,3) # starts at 2 m depth to 65 m depth
depth_arr = np.arange(2,92,3) # tE has depths from 8 to 89 every 3 m


temp_arr = np.empty((len(lats),time_arr.shape[0],depth_arr.shape[0]))
temp_arr.fill(np.nan)

for ID,f_a in enumerate(csv_files):
    print('appended '+str(ID)+' of '+str(len(csv_files)))
    append_file = pd.read_csv(f_i,skiprows=range(6),header=None)
    # set -9999.0 values to np.nan
    append_file[append_file==-9999.0] = np.nan
    # make sure to put the values from depths 8 to 89 for tE
    if f_i == '/data/project1/minnaho/validation/validation_data_moorings/PV_moored/tEPVFSF.csv':
        # [:,1:] to cut out time column
        temp_arr[ID,:len(append_file),2:] = append_file.iloc[:,1:] 
    if f_i in files_13:
        temp_arr[ID,:len(append_file),:12] = append_file.iloc[:,1:]
    else:
        temp_arr[ID,:len(append_file),:22] = append_file.iloc[:,1:]
#############
# make netcdf
#############
temp_nc = Dataset('PV_temp.nc','w')

temp_nc.title = 'Los Angeles County Sanitation District Palos Verdes Flow Study - thermistor data'
temp_nc.description = '2000-10-31 00:15 PST to 2008-04-26, 3 m bins, 15 min frequency'

# dimensions
loc_dim = temp_nc.createDimension('location',len(lats))
time_dim = temp_nc.createDimension('time',len(time_arr))
depth_dim = temp_nc.createDimension('depth',len(depth_arr))

# variables
time_var = temp_nc.createVariable('time',np.float64,('time',))
depth_var = temp_nc.createVariable('depth',np.float32,('depth',))
lat_var = temp_nc.createVariable('latitude',np.float32,('location',))
lon_var = temp_nc.createVariable('longitude',np.float32,('location',))

temperature = temp_nc.createVariable('temperature',np.float32,('location','time','depth'))

# assign values
time_var[:] = time_arr
depth_var[:] = depth_arr
lat_var[:] = lats
lon_var[:] = lons

temperature[:,:,:] = temp_arr

time_var.units = start_time_netcdf
depth_var.units = 'm'
lat_var.units = 'degrees north'
lon_var.units = 'degrees east'

temperature.units = 'degrees C'

temp_nc.close()
'''
