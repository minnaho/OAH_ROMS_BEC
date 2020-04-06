#############################################
# interpolate pCO2 data to have hourly outputs for entire year
#####################################################
import numpy as np
import subprocess
import glob
import datetime as dt
from netCDF4 import Dataset

###################
# FOLDER PATHS
####################
rec_path = '/data/project1/minnaho/pCO2/rec_output/'
interp_path = '/data/project1/minnaho/pCO2/data_interp/'
save_path = '/data/project1/minnaho/pCO2/two_hourly/'
hourly_path = '/data/project1/minnaho/pCO2/'

model = 'wrfout_d01_2015'
interp_files = list(sorted(glob.glob(interp_path+'*')))

###########################################
# interpolate data over time to have data for every day
###########################################
# outputs right before and after a time skip in data

data1 = np.empty((24,228,228))
for hr_i in range(24):
    data1[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-04-29_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

data2 = np.empty((24,228,228))
for hr_i in range(24):
    if hr_i < 12:
        data2[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-07-04_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]
    if hr_i >= 12: 
        data2[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-07-03_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

data3 = np.empty((24,228,228))
for hr_i in range(24):
    if hr_i <= 12:
        data3[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-08-19_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]
    if hr_i > 12: 
        data3[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-08-18_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

data4 = np.empty((24,228,228))
for hr_i in range(24):
    if hr_i < 12:
        data4[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-10-07_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]
    if hr_i >= 12: 
        data4[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-10-06_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

data5 = np.empty((24,228,228))
for hr_i in range(24):
    if hr_i <= 12:
        data5[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-11-13_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]
    if hr_i > 12: 
        data5[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-11-12_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

data6 = np.empty((24,228,228))
for hr_i in range(24):
    data6[hr_i,:,:] = Dataset(rec_path+'wrfout_d01_2015-01-04_'+'%02d'%hr_i+'.nc','r').variables['co2ff'][0,0,:,:]

# gaps in time in data
date1 = dt.datetime(2015,4,29,23)
date2 = dt.datetime(2015,7,3,12)
date3 = dt.datetime(2015,8,19,12)
date4 = dt.datetime(2015,10,6,12)

date5 = dt.datetime(2015,11,13,12)
date6 = dt.datetime(2016,1,4,0)

hours1 = (date2-date1).total_seconds()/3600
hours2 = (date4-date3).total_seconds()/3600
hours3 = (date6-date5).total_seconds()/3600


add_hour = dt.timedelta(hours=1)
# concatenate to use np.average 
data_concat1 = np.array((data1,data2))

# loop over number of hours between 2 dates and create
# netcdf file of new data 

new_date = date1
for h_1 in range(1,int(hours1)):
    print(str(h_1)+' of '+str(hours1))
    new_date = new_date + add_hour
    name_str = model+'-'+'%02d'%new_date.month+'-'+'%02d'%new_date.day+'_'+'%02d'%new_date.hour+'.nc'
    data_interp = np.average(data_concat1[:,(h_1-1)%24,:,:],weights=[(hours1-h_1)/hours1,(h_1/hours1)],axis=0)
    new_data = Dataset(interp_path+name_str,'w')
    time_d = new_data.createDimension('time',None)
    s_n_d = new_data.createDimension('south_north',228) 
    w_e_d = new_data.createDimension('west_east',228) 
    b_t_d = new_data.createDimension('bottom_top',6) 
    pco2 = new_data.createVariable('co2ff',np.float32,('time','bottom_top','south_north','west_east'))
    pco2[0,0,:,:] = data_interp
    new_data.close()

   

data_concat2 = np.array((data3,data4))
new_date = date3
for h_2 in range(1,int(hours2)):
    print(str(h_2)+' of '+str(hours2))
    new_date = new_date + add_hour
    name_str = model+'-'+'%02d'%new_date.month+'-'+'%02d'%new_date.day+'_'+'%02d'%new_date.hour+'.nc'
    data_interp = np.average(data_concat2[:,(h_2+12)%24,:,:],weights=[(hours2-h_2)/hours2,(h_2/hours2)],axis=0)
    new_data = Dataset(interp_path+name_str,'w')
    time_d = new_data.createDimension('time',None)
    s_n_d = new_data.createDimension('south_north',228) 
    w_e_d = new_data.createDimension('west_east',228) 
    b_t_d = new_data.createDimension('bottom_top',6) 
    pco2 = new_data.createVariable('co2ff',np.float32,('time','bottom_top','south_north','west_east'))
    pco2[0,0,:,:] = data_interp
    new_data.close()


data_concat3 = np.array((data5,data6))
new_date = date5
for h_3 in range(1,int(hours3)):
    print(str(h_3)+' of '+str(hours3))
    new_date = new_date + add_hour
    name_str = model+'-'+'%02d'%new_date.month+'-'+'%02d'%new_date.day+'_'+'%02d'%new_date.hour+'.nc'
    data_interp = np.average(data_concat3[:,(h_3+12)%24,:,:],weights=[(hours3-h_3)/hours3,(h_3/hours3)],axis=0)
    new_data = Dataset(interp_path+name_str,'w')
    time_d = new_data.createDimension('time',None)
    s_n_d = new_data.createDimension('south_north',228) 
    w_e_d = new_data.createDimension('west_east',228) 
    b_t_d = new_data.createDimension('bottom_top',6) 
    pco2 = new_data.createVariable('co2ff',np.float32,('time','bottom_top','south_north','west_east'))
    pco2[0,0,:,:] = data_interp
    new_data.close()

'''
##################################
# take average of pCO2 data
##################################
for f_r in range(0,len(interp_files),2):
    print('averaging '+interp_files[f_r]+' and  '+interp_files[f_r+1])
    subprocess.call('ncra -O -v co2ff '+interp_files[f_r]+' '+interp_files[f_r+1]+' '+save_path+'avg_2hr_'+interp_files[f_r][51:],shell=True)

subprocess.call('ncrcat '+interp_path+'* '+hourly_path+'wrfout_pCO2_hourly_interp.nc',shell=True)
subprocess.call('ncrcat '+save_path+'avg_2hr* wrfout_d01_2015_avg_2hr.nc',shell=True)
'''

