##################################
# add record dimension to 
# usw42 biogeochemical model 
# maximum and minimum files
# then concatenate to find min/max
# over one month
# Minna Ho, UCLA, March 2018 
##################################
import subprocess
import numpy as np
from netCDF4 import Dataset

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 1997
end_year = 1999

# between 1 and 12
start_month = 1
end_month = 12 

######################
# PATHS
######################
# path with outputs
roms_path    = '/data/project3/kesf/ROMS/USW4/ALL/'
monthly_path = '/data/project3/kesf/ROMS/USW4/M_ALL/'
# climatology path
clim_path    = '/data/project3/kesf/ROMS/USW4/CLIM/'
# min, max, and standard deviation paths
stats_path = '/data/project3/kesf/ROMS/USW4/STATS/'

# add bdiags
file_types = ['usw42_phys_flux.','usw42_avg.','usw42_bgc_flux_avg.','usw42_bdiags_avg.']

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
            ###################################
            # add record dimension (time) to min and max for each day
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
                print('adding record dimension to '+f+year_month+'D'+str('%02d'%d))
                subprocess.call('ncecat -u time -O '+stats_path+'min_'+f+year_month+'D'+'%02d'%d+'.nc '+stats_path+'t_min_'+f+year_month+'D'+'%02d'%d+'.nc',shell=True) 
                subprocess.call('ncecat -u time -O '+stats_path+'max_'+f+year_month+'D'+'%02d'%d+'.nc '+stats_path+'t_max_'+f+year_month+'D'+'%02d'%d+'.nc',shell=True) 

            # concatenate to find min/max
            print('concatenating t_min_'+f+year_month+'D*.nc')
            subprocess.call('ncrcat -x -v spherical,h,f,pm,pn,lon_rho,lat_rho,angle,mask_rho -O '+stats_path+'t_min_'+f+year_month+'D*.nc '+stats_path+'concat_min_'+f+year_month+'.nc',shell=True)
            subprocess.call('ncrcat -x -v spherical,h,f,pm,pn,lon_rho,lat_rho,angle,mask_rho -O '+stats_path+'t_max_'+f+year_month+'D*.nc '+stats_path+'concat_max_'+f+year_month+'.nc',shell=True) 

            # find min/max over each min/max data
            print('finding min/max of concat_min_'+f+year_month+'.nc')
            subprocess.call('ncwa -y min -O '+stats_path+'concat_min_'+f+year_month+'.nc '+stats_path+'min_'+f+year_month+'.nc',shell=True)
            subprocess.call('ncwa -y max -O '+stats_path+'concat_max_'+f+year_month+'.nc '+stats_path+'max_'+f+year_month+'.nc',shell=True)
            print('min for year month '+year_month+' in min_'+f+year_month+'.nc')
            print('max for year month '+year_month+' in max_'+f+year_month+'.nc')

