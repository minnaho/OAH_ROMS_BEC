##################################
# Extract monthly averages over some depth
# of biogeochemical model outputs
# z slice then NCO operators to average over depth
# ROMS output file names must conform to
# model_name_file_type.Y????M??.nc
# Minna Ho, UCLA, Oct 2019 
##################################
import subprocess
import numpy as np
#import depths as depths
from netCDF4 import Dataset
#from pyroms import tools

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO FIND CLIMATOLOGY 
#########################################

start_year = 1997
end_year = 2000

# between 1 and 12
start_month = 2
end_month = 9

# Sed_Flux_POC,Sed_Flux_CaCO3 omitted for zslice because 2D
bgc_vars = 'TOT_PROD,NITRIF'

######################
# PATHS AND FILE NAMES
# change these for different
# model names and model file types
######################
# model name
model_name   = 'l2_scb'

# path with outputs
monthly_path    = '/data/project5/kesf/ROMS/L2SCB_AP/V3/monthly/'
zslice_path = './slices/'

grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'

##############################
# 40 - 1000 m averaged
##############################

# bgc
model_types = ['bgc_flux_avg']

file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

bot = -1000
top = -40
a = [-45,-50,-60,-70,-80,-90,-100,-150,-200,-250,-300,-400,-500,-600,-700,-800,-900,-1000]
#a = list(range(bot,top+1))
b = ' '.join(str(x) for x in a)
print('bgc '+str(top)+' - '+str(bot))
'''
for y in range(start_year,end_year+1):
    print('year = '+str(y))
    if y != start_year:
        sm = 1
    else:
        sm = start_month
    if y == end_year:
        em = end_month
    else:
        em = 12
    for m in range(sm,em+1): 
        print('month: '+str(m))
        date_str = 'Y'+str(y)+'M'+'%02d'%m+'.nc'
        subprocess.call('ln -fs '+monthly_path+file_types[0]+date_str+' '+zslice_path+model_name+'_'+model_types[0]+'_'+date_str,shell=True)
'''
#zslice
# make sure to rename these before doing the next one
#subprocess.call('zslice '+b+' --vars='+bgc_vars+' '+grid_path+' '+zslice_path+model_name+'_'+model_types[0]+'_Y*.nc',shell=True)

bot = -40
top = 0
a = list(range(bot,top+1,5))
b = ' '.join(str(x) for x in a)
subprocess.call('zslice '+b+' --vars='+bgc_vars+' '+grid_path+' '+zslice_path+model_name+'_'+model_types[0]+'_Y*.nc',shell=True)
