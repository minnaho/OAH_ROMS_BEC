##################################
# reduce size of 
# usw42 bgc files
# keep only variables: 
# TOT_PROD, NITRIF, Denitrif, Sed_denitr
# J_O2, FG_O2, O2SAT, ocean_time
# add nitrate phytoplankton uptake together: 
# no3_v_diat + no3_v_sp = no3_v_p
# add ammonium phytoplankton uptake together:
# nh4_v_diat + nh4_v_sp = nh4_v_p
# Minna Ho, UCLA, June 2018 
##################################
import subprocess
import numpy as np
from netCDF4 import Dataset

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################
# 1997 and 1998 ussw1 do not have zeta, so use variable list with zeta for 1999 onward
# 1999 does not have any oxygen variables, but does have zeta until october
# 2006 and 2007 do not have oxygen variables or zeta
start_year = 2006
end_year = 2007

# between 1 and 12
start_month = 1
end_month = 12

######################
# PATHS
######################
# model name
model_name = 'ussw1'

# model file types e.g. bgc_flux_avg
model_types = ['bgc_flux_avg']

# path with outputs
roms_path    = '/data/project3/kesf/ROMS/USSW1/DAILY/'

# path to save files with just these variables
bgc_daily_path = '/data/project4/kesf/ROMS/USSW1/BGC_DAILY/'

# variable list in string format
#variables = 'TOT_PROD,NITRIF,Denitrif,Sed_denitr,J_O2,FG_O2,O2SAT,ocean_time,no3_v_diat,no3_v_sp,nh4_v_diat,nh4_v_sp,zeta'
variables = 'TOT_PROD,NITRIF,Denitrif,Sed_denitr,ocean_time,no3_v_diat,no3_v_sp,nh4_v_diat,nh4_v_sp'

# variables after adding no3/nh4 uptake
#variables_new = 'TOT_PROD,NITRIF,Denitrif,Sed_denitr,J_O2,FG_O2,O2SAT,ocean_time,no3_v_p,nh4_v_p,zeta'
variables_new = 'TOT_PROD,NITRIF,Denitrif,Sed_denitr,ocean_time,no3_v_p,nh4_v_p'


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
                day_str = 'D'+str('%02d'%d)

                # extracting variables
                print('extracting variables to '+model_name+'_bgc.'+year_month+day_str+'.nc')
                subprocess.call('ncks -O -v '+variables+' '+roms_path+f+year_month+day_str+'.nc '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 

                # add up phytoplankton variables
                subprocess.call('ncap2 -O -s \'no3_v_p=(no3_v_diat+no3_v_sp)\' '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 
                subprocess.call('ncap2 -O -s \'nh4_v_p=(nh4_v_diat+nh4_v_sp)\' '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 

                # cut out the diat and sp variables
                subprocess.call('ncks -O -v '+variables_new+' '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 
                # change description of no3_v_p and nh4_v_p to match what it actually is
                subprocess.call('ncatted -a long_name,no3_v_p,o,c,\'NO3 uptake by diatoms and small plankton\' '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 
                subprocess.call('ncatted -a long_name,nh4_v_p,o,c,\'NH4 uptake by diatoms and small plankton\' '+bgc_daily_path+model_name+'_bgc.'+year_month+day_str+'.nc',shell=True) 


