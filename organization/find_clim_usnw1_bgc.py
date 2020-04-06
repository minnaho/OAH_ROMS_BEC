##################################
# Find climatology from monthly averages
# of biogeochemical model outputs
# ROMS output file names must conform to
# model_name_file_type.Y????M??.nc
# Minna Ho, UCLA, March 2018 
##################################
import subprocess
import numpy as np
from netCDF4 import Dataset

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO FIND CLIMATOLOGY 
#########################################

start_year = 1997
end_year = 2007

# between 1 and 12
start_month = 1
end_month = 12

######################
# PATHS AND FILE NAMES
# change these for different
# model names and model file types
######################
# model name
model_name   = 'usw1'

# model file types e.g. bgc_flux_avg
model_types = ['bgc_flux_avg']
#model_types = ['avg']


# path with outputs
monthly_path    = '/data/project5/kesf/ROMS/USNW1/MONTHLY/'

# climatology path
clim_path    = '/data/project5/kesf/ROMS/USNW1/CLIM/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

##################
# find climatology
##################        
print('calculating climatology')
for m in range(start_month,end_month+1): 
    print('month: '+str(m))
    for f in file_types:
        subprocess.call('ncra '+monthly_path+f+'Y????M'+'%02d'%m+'.nc -o '+clim_path+f+'M'+'%02d'%m+'_'+str(start_year)+'_'+str(end_year)+'.nc',shell=True)
  
