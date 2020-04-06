#######################
# run ncjoin on all files
# and run ncks on bgc files
# Minna Ho, UCLA, Mar 2018
######################## 
import os
import time
import subprocess
import glob

##############
# Inputs
##############
# file prefix here, e.g. 'usw1_bgc_flux_avg'
# make sure bgc file name is first!!!
file_prefix = ['uswc4_bgc_flux_avg','usw42_bdiags_avg','usw42.his','usw42_phys_flux','usw42_avg']

# only for usw4
bgc_out = 'usw42_bgc_flux_avg'

# change year and month of folder that files are in
start_year = 2000
end_year = 2007
# enter as 2 digit month e.g. 01,02,03,...,12
start_month = 01
end_month = 12


############################
# run ncks and ncjoin 
# for all years and months
############################
# number of grid files
g = 256

# change into directory of output files
for year in list(range(start_year,end_year+1)):
    for month in list(range(start_month,end_month+1)):
        out_path = '/data/project3/kesf/ROMS/USW4/AVG_Y'+str(year)+'M'+'%02d'%month+'/'
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
                # loop over 256 for ncks for bgc files
                if f == file_names[0]:
                    print(str(d)+' ncks begin at: '+time.ctime())
                    for j in range(g):
                        subprocess.call('ncks -d time,0 '+out_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc c'+out_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc',shell=True)
                    print(str(d)+' ncks ends at: '+time.ctime())    
                    print(str(d)+' nc join for '+out_file+' begins at '+time.ctime())
                    subprocess.call('ncjoin -d c'+out_file+'.'+'%05d'%d+'.'+'???.nc',shell=True)       
                    subprocess.call('mv c'+out_file+'.'+'%05d'%d+'.nc '+bgc_out+'.'+'%05d'%d+'.nc',shell=True)
                    print(str(d)+' ncjoin step ends at: '+time.ctime())
                    print(str(d)+' suppression of the original files NOW')
                    subprocess.call('rm '+out_file+'.'+'%05d'%d+'.???.nc',shell=True)

                if f != file_names[0]:
                    print(str(d)+' nc join for '+out_file+' begins at '+time.ctime())
                    subprocess.call('ncjoin -d '+out_file+'.'+'%05d'%d+'.'+'???.nc',shell=True)       
                    print(str(d)+' '+out_file+' ends at: '+time.ctime())
                    #print(str(d)+' suppression of the original files NOW')
                    #subprocess.call('rm '+out_file+'.'+'%05d'%d+'.???.nc',shell=True)

'''
###################################
# Run ncks and ncjoin over files
###################################
# number of grid files
g = 256

# loop over each file type
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
        # loop over 256 for ncks for bgc files
        if f == file_names[0]:
            print(str(d)+' ncks begin at: '+time.ctime())
            for j in range(g):
                subprocess.call('ncks -d time,0 '+out_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc c'+out_file+'.'+'%05d'%d+'.'+'%03d'%j+'.nc',shell=True)
            print(str(d)+' ncks ends at: '+time.ctime())    
            print(str(d)+' nc join for '+out_file+' begins at '+time.ctime())
            subprocess.call('ncjoin -d c'+out_file+'.'+'%05d'%d+'.'+'???.nc',shell=True)       
            subprocess.call('mv c'+out_file+'.'+'%05d'%d+'.nc '+bgc_out+'.'+'%05d'%d+'.nc',shell=True)
            print(str(d)+' ncjoin step ends at: '+time.ctime())
            print(str(d)+' suppression of the original files NOW')
            subprocess.call('rm '+out_file+'.'+'%05d'%d+'.???.nc',shell=True)

        if f != file_names[0]:
            print(str(d)+' nc join for '+out_file+' begins at '+time.ctime())
            subprocess.call('ncjoin -d '+out_file+'.'+'%05d'%d+'.'+'???.nc',shell=True)       
            print(str(d)+' '+out_file+' ends at: '+time.ctime())
            print(str(d)+' suppression of the original files NOW')
            subprocess.call('rm '+out_file+'.'+'%05d'%d+'.???.nc',shell=True)

'''
