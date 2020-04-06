import xarray as xr
import subprocess
import glob

start_year = 1997
end_year = 2007

# between 1 and 12
start_month = 1
end_month = 12 

######################
# PATHS AND FILE NAMES
# change these for different
# model names and model file types
######################
'''
folders = []
for y_i in range(start_year,end_year+1):
    if y_i == start_year:
        s_m = start_month 
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y_i == end_year:
        e_m = end_month+1
    else: 
        e_m = 13
    for m_i in range(s_m,e_m): 
        folders.append('AVG_Y'+str(y_i)+'M'+'%02d'%m_i)
'''
        
# model name
model_name   = 'usw42'

# model file types e.g. bgc_flux_avg
model_types = ['phys_flux','avg']
bgc_name = 'uswc4_bgc_flux_avg'

# path with outputs
path_output = '/data/project4/kesf/ROMS/USW4NCF/'

# climatology path
clim_path    = '/data/project4/kesf/ROMS/USW4NCF/CLIM/'

#########################
# get list of model file names 
# e.g. 'usw42_phys_flux.'
#########################
file_types = []
for t_i in model_types:
    file_types.append(model_name+'_'+t_i+'.')

'''
############################
# find bgc climatology
############################
for m_i in range(start_month,end_month+1):
    print('month '+str(m_i))
    bgc_files_list = sorted(glob.glob(path_output+'AVG_Y****M'+'%02d'%m_i+'/'+bgc_name+'*'))
    # turn into one string with spaces between file names
    bgc_files_str = ' '.join(bgc_files_list) 
    #print('\nncra -O '+bgc_files_str+' uswc4_bgc_flux_avg.M'+'%02d'%m_i+'_1997_2007.nc')
    subprocess.call('ncra -O '+bgc_files_str+' '+clim_path+'uswc4_bgc_flux_avg.M'+'%02d'%m_i+'_1997_2007.nc',shell=True)
'''
# loop through months
for m_i in range(start_month,end_month+1):
    print('month '+str(m_i))
    # loop through file types
    for f_i in file_types:
        print(f_i)
        # get list of files from each year for one month to find average of
        f_list = sorted(glob.glob(path_output+'AVG_Y****M'+'%02d'%m_i+'/'+f_i+'*'))
        # turn into one string with spaces between file names
        f_str = ' '.join(f_list)
        #print('ncra -O '+f_str+' '+clim_path+f_i+'M'+'%02d'%m_i+'_1997_2007.nc')        
        subprocess.call('ncra -O '+f_str+' '+clim_path+f_i+'M'+'%02d'%m_i+'_1997_2007.nc',shell=True)
    



