##################################
# rename model files 
# e.g., l2_scb_avg.Y????M??D??.nc to 
# l2_scb_avg_Y????M??D??.nc
# Minna Ho, SCCWRP, Nov 2020
##################################
import subprocess
import glob as glob

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 1999
end_year = 2000

# between 1 and 12
start_month = 7
end_month = 9

######################
# PATHS
######################
# model name
model_name = 'l2_scb'

# model file types e.g. bgc_flux_avg
#model_types = ['phys_flux','avg','bgc_flux_avg']
model_types = ['avg']
#model_types = ['bgc_flux_avg']
#model_types = ['his']

# roms file path
roms_path = '/data/project6/kesf/ROMS/L2SCB_AP/'
#roms_path = '/data/project5/kesf/ROMS/L2_SCB/'
#roms_path = '/data/project6/ROMS/L2SCB_AP/fresh/'
#roms_path = '/data/project6/ROMS/L2SCB_AP/nutrients/'
#roms_path = '/data/project6/ROMS/L2SCB_P_1999_2000/'
#roms_path = '/data/project6/ROMS/L2SCB_1997_2000/'

# daily path
#day_path    = '/data/project1/minnaho/validation/hydrodynamics/roms_slices/roms_output_his/'
#day_path    = '/data/project3/minnaho/freshwater/postprocessing/roms_files_extract/freshw/'
#day_path    = '/data/project3/minnaho/freshwater/postprocessing/roms_files_extract/nutri/'
#day_path    = '/data/project3/minnaho/freshwater/postprocessing/roms_files_extract/pipes/'
#day_path    = '/data/project3/minnaho/freshwater/postprocessing/roms_files_extract/control/'
day_path = '/data/project3/minnaho/freshwater/postprocessing/roms_files_extract/fulll/'


#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for i in model_types:
    file_types.append(model_name+'_'+i+'.')

##############################
# make symbolic link from roms folders
# with numeric file name
# to daily folder with Y????M??D??
# naming convention
##############################
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
        # use glob to find number of avg files
        roms_fi = sorted(glob.glob(roms_path+'AVG_'+year_month+'/'+file_types[0]+'*'))
        for r_i in range(len(roms_fi)):
            if model_types[0] == 'avg':
                subprocess.call('ln -fs '+roms_fi[r_i]+' '+day_path+model_name+'_'+model_types[0]+'_'+year_month+'D'+'%02d'%(r_i+1)+'.nc',shell=True)
            if model_types[0] == 'bgc_flux_avg':
                subprocess.call('ln -fs '+roms_fi[r_i]+' '+day_path+model_name+'_'+model_types[0]+'_'+year_month+'.nc',shell=True)
            if model_types[0] == 'his':
                subprocess.call('ln -fs '+roms_fi[r_i]+' '+day_path+model_name+'_'+model_types[0]+'_'+year_month+'.nc',shell=True)
