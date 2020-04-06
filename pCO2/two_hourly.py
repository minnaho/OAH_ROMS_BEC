#############################################
# two_hourly.py
# take 2 hour average over all months for
# hourly pCO2 data 
#####################################################
import numpy as np
import subprocess
import glob

###################
# FOLDER PATHS
####################
data_path = '/data/project1/minnaho/pCO2/output_links/'
rec_path = '/data/project1/minnaho/pCO2/rec_output/'
save_path = '/data/project1/minnaho/pCO2/two_hourly/'

##################################
# take average of pCO2 data
##################################
#dataset = 'wrfout_d01_2015-08'
dataset = 'wrfout_d01'
output_files = glob.glob(data_path+'*')
rec_files = list(sorted(glob.glob(rec_path+'*')))

'''
# add record dimension to all files (needed to do ncra)
for f_i in output_files:
    subprocess.call('ncecat -u time '+f_i+' '+rec_path+f_i[41:65]+'.nc',shell=True)
'''

for f_r in range(0,len(rec_files),2):
    print('averaging '+rec_files[f_r]+' and  '+rec_files[f_r+1])
    #subprocess.call('ncra -O '+rec_path+dataset+'-??_'+h0_str+' '+save_path+'avg_08'+dataset+h_str+'.nc',shell=True)
    subprocess.call('ncra -O '+rec_files[f_r]+' '+rec_files[f_r+1]+' '+save_path+'avg_2hr_'+dataset+'_'+rec_files[f_r][50:],shell=True)


subprocess.call('ncrcat '+save_path+'avg_2hr* wrfout_d01_2015_avg_2hr.nc',shell=True)

