##################################
# add record dimension to 
# usw42 biogeochemical model 
# maximum and minimum files
# then concatenate to find min/max
# over one month
# Minna Ho, UCLA, March 2018 
##################################
import subprocess

#########################################
# CHANGE THESE INPUTS TO CHANGE YEARS 
# AND MONTHS TO DO CALUCULATION ON
#########################################

start_year = 2016
end_year = 2016

# between 1 and 12
start_month = 1
end_month = 12 

######################
# PATHS
######################
# path with outputs
outpath    = '/data/project6/minnaho/bio_interp/co2sys_output_L1_sm/'

# file types
file_types = ['ussw1_avg.']

##############################
# CALCULATE 
# DAYS IN EACH MONTH
# AND FIND MONTHLY AVERAGE
# FOR EACH VARIABLE
##############################

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

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
        # loop through each file type
        for f in file_types:
            ###################################
            # add record dimension (time) to min and max for each day
            ###################################
            # find out how many days to loop over for each month
            if m in months_w_31_days:
                ndays = 31
            if m not in months_w_31_days:
                ndays = 30
                if m == 2 and y in leap_years:
                    ndays = 29
                if m == 2 and y not in leap_years:
                    ndays = 28 
            for d in list(range(1,ndays+1)):
                datestr = year_month+'D'+'%02d'%d
                print(f+datestr)
                subprocess.call('ncks -A -v depth '+outpath+f+datestr+'_depth.nc '+outpath+f+datestr+'_co2sys_smdomain.nc',shell=True) 
