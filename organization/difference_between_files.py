##################################
# find difference 
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
end_year = 2001

# between 1 and 12
start_month = 1
end_month = 12 

######################
# PATHS AND FILE NAMES
# change these for different
# model names and model file types
######################
# model name
model_name   = 'usw42'

# model file types e.g. bgc_flux_avg
model_types = ['phys_flux','avg','bgc_flux_avg']

# path with outputs
roms_path1    = '/data/project3/kesf/ROMS/USW4/M_ALL/'
roms_path2    = '/data/project3/kesf/ROMS/USW4/MONTHLY/'

# path to put difference
diff_path    = '/data/project3/kesf/ROMS/USW4/difference_MONTHLY_M_ALL/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

##################
# find difference
# MONTHLY - M_ALL
##################        
print('calculating difference')
for y in range(start_year,end_year+1):
    print('year: '+str(y))
    for m in range(start_month,end_month+1): 
        print('month: '+str(m))
        year_month = 'Y'+str(y)+'M'+'%02d'%m
        for f in file_types:
            subprocess.call('ncdiff -O '+roms_path2+f+year_month+'.nc '+roms_path1+f+year_month+'.nc '+diff_path+'diff_'+f+year_month+'.nc',shell=True)
  
