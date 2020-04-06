##################################
# Find climatology from monthly averages
# of biogeochemical model outputs
# ROMS output file names must conform to
# model_name_file_type.Y????M??.nc
# Minna Ho, UCLA, March 2018 
##################################
import subprocess

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
model_name   = 'ussw1'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg']
model_types = ['avg']

# path with outputs
monthly_path    = '/data/project3/kesf/ROMS/USSW1/MONTHLY/'

# climatology path
clim_path    = '/data/project3/kesf/ROMS/USSW1/CLIM/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

###########################
# variables to extract for budget
##########################
phys_vars = 'HorXAdvFlux_O2,HorXAdvFlux_DIC,HorXAdvFlux_Alk,HorYAdvFlux_O2,HorYAdvFlux_DIC,HorYAdvFlux_Alk,VertAdvFlux_O2,VertAdvFlux_DIC,VertAdvFlux_Alk,VertDiffFlux_O2,VertDiffFlux_DIC,VertDiffFlux_Alk'

avg_vars = 'DIC,Alk,O2,u,v,w'

bgc_vars = 'J_O2,FG_O2'

##################
# find climatology
##################        
'''
print('calculating climatology')
for m in range(start_month,end_month+1): 
    print('month: '+str(m))
    for f in file_types:
        subprocess.call('ncra -x -v GRAZE_SP '+monthly_path+f+'Y????M'+'%02d'%m+'.nc -O '+clim_path+f+'M'+'%02d'%m+'_'+str(start_year)+'_'+str(end_year)+'.nc',shell=True)
'''  
for m in range(start_month,end_month+1):
    print('month: '+str(m))
    for f in file_types:
        if f == 'ussw1_phys_flux.':
            subprocess.call('ncra -v '+phys_vars+' '+monthly_path+f+'Y200[0-5]M'+'%02d'%m+'.nc -O '+clim_path+f+'M'+'%02d'%m+'_2000_2005.nc',shell=True)
        if f == 'ussw1_bgc_flux_avg.':
            subprocess.call('ncra -v '+bgc_vars+' '+monthly_path+f+'Y200[0-5]M'+'%02d'%m+'.nc -O '+clim_path+f+'M'+'%02d'%m+'_2000_2005.nc',shell=True)
        if f == 'ussw1_avg.':
            subprocess.call('ncra -v '+avg_vars+' '+monthly_path+f+'Y200[0-5]M'+'%02d'%m+'.nc -O '+clim_path+f+'M'+'%02d'%m+'_2000_2005.nc',shell=True)




