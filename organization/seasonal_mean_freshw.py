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

# freshw or control
run_type = 'freshw'

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
roms_path    = '/data/project3/minnaho/freshwater/postprocessing/depth_avg/'+run_type+'/'
# path to save monthly averages
monthly_path = '/data/project3/minnaho/freshwater/seasonal_avg/'+run_type+'/'

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
    for f in range(len(file_types)):
        if model_types[f] == 'avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M0[6-8]D*.nc '+monthly_path+model_types[f]+'summer.nc',shell=True) 
        if model_types[f] == 'bgc_flux_avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M0[6-8].nc '+monthly_path+model_types[f]+'summer.nc',shell=True) 
if season == 'winter':
    print('winter')
    for f in range(len(file_types)):
        if model_types[f] == 'avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M12D*.nc '+roms_path+model_types[f]+'Y*M01D*.nc '+roms_path+model_types[f]+'Y*M02D*.nc '+monthly_path+model_types[f]+'winter.nc',shell=True) 
        if model_types[f] == 'bgc_flux_avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M12.nc '+roms_path+model_types[f]+'Y*M01.nc '+roms_path+model_types[f]+'Y*M02.nc '+monthly_path+model_types[f]+'winter.nc',shell=True) 
if season == 'spring':
    print('spring')
    for f in range(len(file_types)):
        if model_types[f] == 'avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M03D*.nc '+roms_path+model_types[f]+'Y*M04D*.nc '+roms_path+model_types[f]+'Y*M05D*.nc '+monthly_path+model_types[f]+'spring.nc',shell=True) 
        if model_types[f] == 'bgc_flux_avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M03.nc '+roms_path+model_types[f]+'Y*M04.nc '+roms_path+model_types[f]+'Y*M05.nc '+monthly_path+model_types[f]+'spring.nc',shell=True) 
if season == 'fall':
    print('fall')
    for f in range(len(file_types)):
        if model_types[f] == 'avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M09D*.nc '+roms_path+model_types[f]+'Y*M10D*.nc '+roms_path+model_types[f]+'Y*M11D*.nc '+monthly_path+model_types[f]+'autumn.nc',shell=True) 
        if model_types[f] == 'bgc_flux_avg':
            subprocess.call('ncra -O '+roms_path+model_types[f]+'Y*M09.nc '+roms_path+model_types[f]+'Y*M10.nc '+roms_path+model_types[f]+'Y*M11.nc '+monthly_path+model_types[f]+'autumn.nc',shell=True) 
