########################
# ncks and ncjoin on bgc files
# By Minna Ho, UCLA, Mar 2018
# contact: minnaho@ucla.edu
# Adapted for roms-bec 
# version CCS-2018, Comet/xsede
# contact Faycal Kessouri
# kesf@ucla.edu
######################## 
import os
import time
import subprocess
import glob

##############
# Inputs
##############

# change year and month of folder that files are in
start_year = 2000
end_year = 2000
# enter as 2 digit month e.g. 01,02,03,...,12
start_month = 02
end_month = 02

# path here
# out_path = '/home/kesf/PROJECTS/USW4/Run/SCRATCH/'
out_path = '/home/kesf/PROJECTS/USSW1/Run/SCRATCH/'

# file prefix here, e.g. 'usw1_bgc_flux_avg'
bgc_file = 'ussw1_bgc_flux_avg'
bgc_out = 'ussw1_bgc_flux_avg'


#####################
# Run ncks over files
#####################
# loop over days
g = 256
for year in list(range(start_year,end_year+1)):
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
        # call file names to get first and last day 
        out_folder = 'AVG_Y'+str(year)+'M'+'%02d'%month+'/'  
        os.chdir(out_path+out_folder)
        file_names = sorted(glob.glob('./'+bgc_file+'.*.000.nc'))
        # get first day
        # +3 to length to include './' before and '.' after out_file
        ind_nc = file_names[0].index('.000.')
        first_day = int(file_names[0][len(bgc_file)+3:ind_nc])
        # get last day
        last_day = int(file_names[-1][len(bgc_file)+3:ind_nc])

        for d in list(range(first_day,last_day+1)):
            print(str(d)+' begin at: '+time.ctime())
            # loop over 256
            for j in range(g):
                subprocess.call('ncks -d time,0 '+bgc_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc c'+bgc_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc',shell=True)
            print(str(d)+' step1 ends at: '+time.ctime())    
            # start ncjoin
            subprocess.call('ncjoin -d c'+bgc_file+'.'+'%05d'%d+'.'+'???.nc',shell=True) 
            subprocess.call('mv c'+bgc_file+'.'+'%05d'%d+'.nc '+bgc_out+'.'+'%05d'%d+'.nc',shell=True)
            print(str(d)+' final step ends at: '+time.ctime())
            print(str(d)+' suppression of the original files NOW')
            subprocess.call('rm '+bgc_file+'.'+'%05d'%d+'.???.nc',shell=True)
