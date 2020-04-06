#######################
# run ncjoin on all files
# except bgc files
# (bgc ncks and ncjoin in 
# bgc_ncks_ncjoin_roms.py)
# By Minna Ho, UCLA, Mar 2018
# contact: minnaho@ucla.edu
# Adapted for roms-bec 
# version CCS-2018, Comet/xsede
# contact: Faycal Kessouri
# kesf@ucla.edu
########################
import os
import time
import subprocess
import glob

##############
# Inputs
##############
# model name
model_name = 'l2_scb'

# model file types e.g. 'his','phys_flux','avg','bdiags_avg'
model_types = ['his','phys_flux','avg','bdiags_avg','bgc_flux_avg']

# path here
out_path1 = '/data/project5/kesf/ROMS/L2_SCB_AP/'

# change year and month of folder that files are in
start_year = 1997
end_year = 1997

# enter as digit month e.g. 1,2,3,...,12
start_month = 8
end_month = 8

##########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
##########################
file_prefix = []
for i in model_types:
    file_prefix.append(model_name+'_'+i)

############################
# run ncjoin 
# for all years and months
############################
# change into directory of output files
for year in list(range(start_year,end_year+1)):
    # if we are on the first year, starts at s_m
    if year == start_year:
        s_m = start_month
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if year == end_year:
        e_m = end_month+1
    else:
        e_m = 13
    for month in list(range(s_m,e_m)): 
        out_path = out_path1+'AVG_Y'+str(year)+'M'+'%02d'%month+'/'
        os.chdir(out_path)

        for f in file_prefix:
            out_file = f
            # call file names to get first and last day 
            file_names = sorted(glob.glob('./'+out_file+'.*.000.nc'))
            # get first day
            # +3 to length to include './' before and '.' after out_file
            ind_nc = file_names[0].index('.000.')
            first_day = int(file_names[0][len(out_file)+3:ind_nc])
            # get last day
            last_day = int(file_names[-1][len(out_file)+3:ind_nc])

            # loop over each day specific to each file type
            for d in list(range(first_day,last_day+1)): 
                print(str(d)+' nc join for '+out_file+' begins at '+time.ctime())
                subprocess.call('ncjoin -d '+out_file+'.'+'%05d'%d+'.'+'???.nc',shell=True)       
                print(str(d)+' '+out_file+' ends at: '+time.ctime())

