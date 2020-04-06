############################
# Copy and run python script
# for all years and months
# Minna Ho, UCLA, Mar 2018
############################ 
import os
import time
import subprocess

##############
# Inputs
##############
# change year and month of folder that files are in
start_year = 2000
end_year = 2007
# enter as 2 digit month e.g. 01,02,03,...,12
start_month = 01
end_month = 12

py_script = 'bgc_ncks_ussw1.py'

############################
# Copy and run python script
# for all years and months
############################
for year in list(range(start_year,end_year+1)):
    for month in list(range(start_month,end_month+1)):
        bgc_path = '/data/project3/kesf/ROMS/USSW1/AVG_Y'+str(year)+'M'+'%02d'%month+'/'
        subprocess.call('cp /data/project3/kesf/tools_roms/Model_outputs/+'py_script+' '+bgc_path+'/.',shell=True)
        os.chdir(bgc_path)
        subprocess.call('python '+py_script,shell=True)

