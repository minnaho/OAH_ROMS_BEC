##################################
# Take monthly averages
# of model outputs
# ROMS output file names must conform to
# model_name_file_type.Y????M??D??.nc
# Minna Ho, UCLA, March 2018 
# mexican source attribution
##################################
import subprocess

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 2016
end_year = 2017

# between 1 and 12
start_month = 12
end_month = 10

######################
# PATHS
######################
# model name
model_name = 'l2_scb'
scenario = 'mex'
#scenario = 'us'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg']
model_types = ['avg']

# path with outputs
roms_path    = '/data/project9/kesf/ROMS/L2SCB_AP/contribution/'+scenario+'/daily/'

# path to save monthly averages
monthly_path = '/data/project9/kesf/ROMS/L2SCB_AP/contribution/'+scenario+'/monthly/' 


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
        year_month = 'Y'+str(y)+'M'+'%02d'%m
        print(scenario+' '+year_month)
        # loop through each file type
        for f in file_types:
            #################################
            # find monthly average using ncra
            ################################
            subprocess.call('ncra -O '+roms_path+f+year_month+'D*.nc '+monthly_path+f+year_month+'.nc',shell=True) 

