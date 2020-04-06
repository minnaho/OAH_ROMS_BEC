##################################
# Take monthly averages
# of biogeochemical model outputs
# and find min/max and standard deviation 
# ROMS output file names must conform to
# model_name_file_type.Y????M??D??.nc
# Minna Ho, UCLA, March 2018 
##################################
import subprocess
import numpy as np
from netCDF4 import Dataset

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 1998
end_year = 2006

# between 1 and 12
start_month = 3
end_month = 12

######################
# PATHS
######################
# model name
model_name = 'usw1'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg']
model_types = ['avg']

# path with outputs
roms_path    = '/data/project5/kesf/ROMS/USNW1/DAILY/'
# path to save monthly averages
monthly_path = '/data/project5/kesf/ROMS/USNW1/MONTHLY/'

# min, max, and standard deviation paths
#stats_path = '/data/project3/kesf/ROMS/USSW1/STATS/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

##############################
# CALCULATE 
# DAYS IN EACH MONTH
# AND FIND MONTHLY AVERAGE
# FOR EACH VARIABLE
##############################

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

for y in range(start_year,end_year+1):
    print('year: '+str(y))
    # if we are on the first year, starts at s_m
    if y == start_year:
        s_m = start_month 
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y == end_year:
        e_m = end_month+1
    else: 
        e_m = 13
    for m in range(s_m,e_m): 
        print('month: '+str(m))
        year_month = 'Y'+str(y)+'M'+'%02d'%m
        # loop through each file type
        for f in file_types:
            #################################
            # find monthly average using ncra
            ################################
            print('starting ncra on '+str(f))
            subprocess.call('ncra -O '+roms_path+f+year_month+'D*.nc '+monthly_path+f+year_month+'.nc',shell=True) 

'''
            ###################################
            # find min and max for each day
            # ncra preserves dimensions when finding min/max
            ###################################
            # find out how many days to loop over for each month
            if m in months_w_31_days:
                ndays = 31
            if m not in months_w_31_days:
                ndays = 30
                if m == 2 and y in leap_years:
                    ndays = 29
                if m == 2 and y not in leap_years:
                    ndays = 28 
            for d in list(range(1,ndays+1)):
                print('finding min and max of '+f+year_month+'D'+str('%02d'%d))
                subprocess.call('ncra -y min -O '+roms_path+f+year_month+'D'+'%02d'%d+'.nc '+stats_path+'min_'+f+year_month+'D'+'%02d'%d+'.nc',shell=True) 
                subprocess.call('ncra -y max -O '+roms_path+f+year_month+'D'+'%02d'%d+'.nc '+stats_path+'max_'+f+year_month+'D'+'%02d'%d+'.nc',shell=True)

            # concatenate to find min/max
            print('concatenating min_'+f+year_month+'D*.nc')
            subprocess.call('ncrcat -x -v spherical,h,f,pm,pn,lon_rho,lat_rho,angle,mask_rho -O '+stats_path+'min_'+f+year_month+'D*.nc '+stats_path+'concat_min_'+f+year_month+'.nc',shell=True)
            print('concatenating max_'+f+year_month+'D*.nc')
            subprocess.call('ncrcat -x -v spherical,h,f,pm,pn,lon_rho,lat_rho,angle,mask_rho -O '+stats_path+'max_'+f+year_month+'D*.nc '+stats_path+'concat_max_'+f+year_month+'.nc',shell=True) 

            # find min/max over each concatenated min/max month data
            print('finding min/max of concat_min_'+f+year_month+'.nc')
            subprocess.call('ncra -y min -O '+stats_path+'concat_min_'+f+year_month+'.nc '+stats_path+'min_'+f+year_month+'.nc',shell=True)
            subprocess.call('ncra -y max -O '+stats_path+'concat_max_'+f+year_month+'.nc '+stats_path+'max_'+f+year_month+'.nc',shell=True)
            print('min for year month '+year_month+' in min_'+f+year_month+'.nc')
            print('max for year month '+year_month+' in max_'+f+year_month+'.nc')
'''
'''
            ################################################        
            # find standard deviation through multiple steps
            ################################################
            print('finding standard deviation')
            # first step: concatenate all days into one file 
            subprocess.call('ncrcat -O '+roms_path+f+year_month+'D*.nc '+stats_path+'concat_'+f+year_month+'.nc',shell=True)
            # second step: find temporal mean of all variables
            subprocess.call('ncwa -O -a time '+stats_path+'concat_'+f+year_month+'.nc '+stats_path+'temp_mean_'+f+year_month+'.nc',shell=True)
            # third step: find anomaly (deviation from the mean)
            subprocess.call('ncbo -O '+stats_path+'concat_'+f+year_month+'.nc '+stats_path+'temp_mean_'+f+year_month+'.nc '+stats_path+'anom_'+f+year_month+'.nc',shell=True)
            # last step: find root mean square of anomaly
            subprocess.call('ncra -O -y rmssdn '+stats_path+'anom_'+f+year_month+'.nc '+stats_path+'std_'+f+year_month+'.nc',shell=True)

'''

'''
variable = []
f = file_types[0]
for y in range(start_year,end_year+1):
    print('year: '+str(y))
    # if we are on the first year, starts at s_m
    if y == start_year:
        s_m = start_month 
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y == end_year:
        e_m = end_month+1
    else: 
        e_m = 13
    for m in range(s_m,e_m): 
        print('month: '+str(m))
        if m in months_with_31_days:
            ndays = 31
        if m not in months_with_31_days:
            ndays = 30
            if m == 2 and y in leap_years:
                ndays = 29
            if m == 2 and y not in leap_years: 
                ndays = 28
        for d in range(1,ndays+1):
            year_month_day = 'Y'+str(y)+'M'+'%02d'%m+'D'+'%02d'%d
            print('assigning data for day: '+str(d)+' in month '+str(m))
#            for f in file_types:
            roms_file = roms_path+f+year_month_day+'.nc'
            data_set = Dataset(roms_file,'r')
            variable_list = data_set.variables 
            # make dictionary with each variable as a key
            variable_dict = dict((k,[]) for k in variable_list) 
            variable_dict_avg = dict((k,[]) for k in variable_list) 
            for v in variable_list:
                variable_dict[v].append(np.array(data_set.variables[v]))
#        for v in variable_list:
#            np.nanmean(variable_dict[v],axis=0)
'''
