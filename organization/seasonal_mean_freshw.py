##################################
# Take monthly averages
# of biogeochemical model outputs
# and find min/max and standard deviation 
# ROMS output file names must conform to
# model_name_file_type.Y????M??D??.nc
# Minna Ho, UCLA, March 2018 
##################################
import subprocess

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################
# season
season = 'summer'

######################
# PATHS
######################
# model name
model_name = 'l2_scb'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg']
model_types = ['avg']

# path with outputs
#roms_path    = '/data/project5/kesf/ROMS/L2SCB_AP/freshw/monthly/'
roms_path    = '/data/project3/minnaho/freshwater/control_1999_2000/'
# path to save monthly averages
#monthly_path = '/data/project3/minnaho/freshwater/seasonal_avg/freshw/'
monthly_path = '/data/project3/minnaho/freshwater/seasonal_avg/control/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

##############################
# find seasonal average
##############################
if season == 'summer':
    print('summer')
    for f in file_types:
        subprocess.call('ncra -O '+roms_path+f+'Y*M0[6-8].nc '+monthly_path+f+'summer.nc',shell=True) 
if season == 'winter':
    print('winter')
    for f in file_types:
        subprocess.call('ncra -O '+roms_path+f+'Y*M12.nc '+roms_path+f+'Y*M01.nc '+roms_path+f+'Y*M02.nc '+monthly_path+f+'winter.nc',shell=True) 
if season == 'spring':
    print('spring')
    for f in file_types:
        subprocess.call('ncra -O '+roms_path+f+'Y*M03.nc '+roms_path+f+'Y*M04.nc '+roms_path+f+'Y*M05.nc '+monthly_path+f+'spring.nc',shell=True) 
if season == 'fall':
    print('fall')
    for f in file_types:
        subprocess.call('ncra -O '+roms_path+f+'Y*M09.nc '+roms_path+f+'Y*M10.nc '+roms_path+f+'Y*M11.nc '+monthly_path+f+'autumn.nc',shell=True) 
