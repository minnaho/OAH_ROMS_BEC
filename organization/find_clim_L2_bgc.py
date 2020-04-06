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
end_year = 2000

# between 1 and 12
start_month = 1
end_month = 12 

######################
# PATHS AND FILE NAMES
# change these for different
# model names and model file types
######################
# model name
model_name   = 'l2_scb'

# model file types e.g. bgc_flux_avg
model_types = ['bgc_flux_avg']

# path with outputs
monthly_path    = '/data/project5/kesf/ROMS/L2SCB_AP/V3/monthly/'

# climatology path
clim_path    = '/data/project5/kesf/ROMS/L2SCB_AP/V3/clim/'

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
        subprocess.call('ncra -O '+monthly_path+f+'Y????M'+'%02d'%m+'.nc -v SP_N_LIM,DIAT_N_LIM,SP_LIGHT_LIM,DIAT_LIGHT_LIM,zeta -o '+clim_path+f+'M'+'%02d'%m+'_'+str(start_year)+'_'+str(end_year)+'_bgc_limitation.nc',shell=True)
  
