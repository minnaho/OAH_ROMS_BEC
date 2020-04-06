#######################
# run ncjoin on all files
# for usw4
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
# file prefix here, e.g. 'usw1_bgc_flux_avg'
#file_prefix = ['ussw1_bdiags_avg','ussw1_his','ussw1_phys_flux','ussw1_avg'] save copy of all names
file_prefix = ['usw42_bdiags_avg','usw42_his','usw42_phys_flux']
#file_prefix = ['usw42_avg']

# path here
out_path1 = '/data/project4/kesf/ROMS/USW4_082018/'

# change year and month of folder that files are in
start_year = 2001
end_year = 2001
# enter as digit month e.g. 1,2,3,...,12
start_month = 5
end_month = 6


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
                #print(str(d)+' suppression of the original files NOW')
                #subprocess.call('rm '+out_file+'.'+'%05d'%d+'.???.nc',shell=True)

