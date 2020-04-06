#############################################
# hourly_climatology.py
# take hourly average over all months for
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
save_path = '/data/project1/minnaho/pCO2/hourly_climatology/'

##################################
# take average of pCO2 data
##################################
dataset = 'wrfout_d01_2015-08'
#dataset = 'wrfout_d01_2015'
output_files = glob.glob(data_path+'*')

'''
# add record dimension to all files (needed to do ncra)
for f_i in output_files:
    subprocess.call('ncecat -u time '+f_i+' '+rec_path+f_i[41:65]+'.nc',shell=True)
'''


for hr in range(24):
    h0_str = '%02d'%hr+'*'
    h_str = '%02d'%hr
    print('averaging for hour '+h_str)
    print (rec_path+dataset)
    subprocess.call('ncra -O '+rec_path+dataset+'-??_'+h0_str+' '+save_path+'avg_08'+dataset+h_str+'.nc',shell=True)
    #subprocess.call('ncra -O '+rec_path+dataset+'??-??_'+h0_str+' '+save_path+'avg_'+dataset+h_str+'.nc',shell=True)


subprocess.call('ncrcat '+save_path+'avg_08* wrfout_d01_2015_hourly_climatology_08.nc',shell=True)

