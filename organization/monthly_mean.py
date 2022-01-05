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

start_year = 1997
end_year = 1997

# between 1 and 12
start_month = 8
end_month = 12

######################
# PATHS
######################
# model name
model_name = 'l2_scb'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg','bdiags_avg']
model_types = ['avg']

# path with outputs
roms_path    = '/data/project6/ROMS/L2SCB_OPC/loads1617/daily/'
# path to save monthly averages
monthly_path = '/data/project6/ROMS/L2SCB_OPC/loads1617/monthly/'

# exclude varibles
#exclude = '-x -v zlev_u_rho,zlev_rho '
exclude = ''

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
            subprocess.call('ncra -O '+exclude+roms_path+f+year_month+'D*.nc '+monthly_path+f+year_month+'.nc',shell=True) 
