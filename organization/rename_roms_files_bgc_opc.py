##################################
# rename model files e.g., l2_scb_avg.01328.nc to 
# l2_scb_avg.Y????M??D??.nc
# Minna Ho, SCCWRP, Nov 2020
##################################
import subprocess
import glob as glob

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 1997
end_year = 1999

# between 1 and 12
start_month = 8
end_month = 10

######################
# PATHS
######################
# model name
model_name = 'l2_scb'

# model file types e.g. bgc_flux_avg
model_types = ['phys_flux','his','bgc_flux_avg']
#model_types = ['his']

model_sce = 'src_attr_loads1617'

# roms file path
roms_path = '/data/project6/ROMS/L2SCB_OPC/'+model_sce+'/'

# monthly/daily path
day_path  = '/data/project6/ROMS/L2SCB_OPC/'+model_sce+'/monthly/'



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
        for f in range(len(file_types)):
            print('month: '+str(m))
            year_month = 'Y'+str(y)+'M'+'%02d'%m
            # use glob to find number of avg files
            roms_fi = sorted(glob.glob(roms_path+'AVG_'+year_month+'/'+file_types[f]+'*'))
            subprocess.call('ln -fs '+roms_fi[0]+' '+day_path+file_types[f]+year_month+'.nc',shell=True)

