# 2017 loads in Aug 1997- Nov 1998
# US inputs only (exclude Tijuana River and South Bay International WTP)
from netCDF4 import Dataset,num2date
import numpy as np
import pandas as pd

# roms psource file to copy and remake
file_path = '/data/project1/minnaho/psource/run_fixjwpcp/roms_psource_102020_full.767.nc'
file_path_out = '/data/project1/minnaho/psource/source_attribution/roms_psource_USonly.nc'
file_nc = Dataset(file_path,'r')


Qbar_nc   = np.array(file_nc.variables['Qbar'][:,:])
# end psources before rivers to exclude rivers
#end_ind = 115 # end of all POTWs, start of rivers
end_ind = Qbar_nc.shape[0]

# LA river, San Gabriel, Calleguas, Malibu creek, San Diego Creek,
# San Diego River, Santa clara river, ventura river
# see /data/project1/minnaho/find_inputs_coords/river_points.py
rivst = 115
nsrc_list = [rivst+32,190,191,192,rivst+51,193,194,195, 196,rivst+12,rivst+34,rivst+48, rivst+49,rivst+61,rivst+72]

# psource time is actually days since 1994-01-01
psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
psrc_dt = num2date(psource_time_nc,'days since 1994-01-01',only_use_cftime_datetimes=False)

# psrc time starts at 1997-01-30
# only choose Aug 2016 - Jul 2017
p_st = -17
p_en = -5

Qbar_nc   = np.array(file_nc.variables['Qbar'][:,p_st:p_en])

Qshape_nc = np.array(file_nc.variables['Qshape'][:,:])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][:])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][:])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][:])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,:])

# read in input file 
temp_nc = np.array(file_nc.variables['temp'][:,p_st:p_en])
salt_nc = np.array(file_nc.variables['salt'][:,p_st:p_en])
PO4_nc = np.array(file_nc.variables['PO4'][:,p_st:p_en])
NO3_nc = np.array(file_nc.variables['NO3'][:,p_st:p_en])
NH4_nc = np.array(file_nc.variables['NH4'][:,p_st:p_en])
Fe_nc  = np.array(file_nc.variables['Fe'][:,p_st:p_en])
O2_nc  = np.array(file_nc.variables['O2'][:,p_st:p_en])
DIC_nc = np.array(file_nc.variables['DIC'][:,p_st:p_en])
Alk_nc = np.array(file_nc.variables['Alk'][:,p_st:p_en])
DOC_nc = np.array(file_nc.variables['DOC'][:,p_st:p_en])
DON_nc = np.array(file_nc.variables['DON'][:,p_st:p_en])
DOP_nc = np.array(file_nc.variables['DOP'][:,p_st:p_en])
NO2_nc = np.array(file_nc.variables['NO2'][:,p_st:p_en])
SiO3_nc = np.array(file_nc.variables['SiO3'][:,p_st:p_en])

# assign inland POTW values 
kgy_to_mmols = (1000*1000)/(365*86400*14)
mgL_to_mmolm3 = 1000./14

# LA river
# divide over number of cells spreading (4 cells)
#Qbar_nc[nsrc_list[0:4],:] = (1.05+0.39+0.19)/4 
#NO3_nc[nsrc_list[0:4],:]  = ((398.27*1.05)+(307.17*.39)+(467.7*.19))*(1/(1.05+.39+.19))
#NH4_nc[nsrc_list[0:4],:]  = ((96.84*1.05)+(101.43*.39)+(79.29*.19))*(1/(1.05+.39+.19))
#DON_nc[nsrc_list[0:4],:]  = ((106.53*1.05)+(84.97*.39)+(65.26*.19))*(1/(1.05+.39+.19))


# subtract inland POTW discharge
larminus = Qbar_nc[nsrc_list[0],:] - ((1.05+0.39+0.19)/4) 
# set all negative flow to POTW flow
Qbar_nc[nsrc_list[0],larminus<0] = (1.05+0.39+0.19)/4
Qbar_nc[nsrc_list[0:4]] = Qbar_nc[nsrc_list[0]]

# set all constituents with -flow to POTW conc
NO3_nc[nsrc_list[0],larminus<0] = ((398.27*1.05)+(307.17*.39)+(467.7*.19))*(1/(1.05+.39+.19))
NH4_nc[nsrc_list[0],larminus<0] = ((96.84*1.05)+(101.43*.39)+(79.29*.19))*(1/(1.05+.39+.19)) 
DON_nc[nsrc_list[0],larminus<0] = ((106.53*1.05)+(84.97*.39)+(65.26*.19))*(1/(1.05+.39+.19)) 

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[0],larminus>0]  = ((NO3_nc[nsrc_list[0],larminus>0]*larminus[larminus>0]) +((398.27*1.05)+(307.17*.39)+(467.7*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

NO3_nc[nsrc_list[0:4]] = NO3_nc[nsrc_list[0]]

NH4_nc[nsrc_list[0],larminus>0]  = ((NH4_nc[nsrc_list[0],larminus>0]*larminus[larminus>0]) +((96.84*1.05)+(101.43*.39)+(79.29*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

NH4_nc[nsrc_list[0:4]] = NH4_nc[nsrc_list[0]]

DON_nc[nsrc_list[0],larminus>0]  = ((DON_nc[nsrc_list[0],larminus>0]*larminus[larminus>0]) +((106.53*1.05)+(84.97*.39)+(65.26*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

DON_nc[nsrc_list[0:4]] = DON_nc[nsrc_list[0]]

# SG river
# divide over number of cells spreading (5 cells)
# subtract inland POTW discharge
sgrminus = Qbar_nc[nsrc_list[4],:] - (0.74+0.25+0.18+0.12)/5
# set all negative flow to POTW flow
Qbar_nc[nsrc_list[4],sgrminus<0] = (0.74+0.25+0.18+0.12)/5
Qbar_nc[nsrc_list[4:9]] = Qbar_nc[nsrc_list[4]]

# add flow to just Jan-Mar for one of the plants that has 
# intermittent discharge
Qbar_nc[nsrc_list[4:9],6:9] = Qbar_nc[nsrc_list[4:9],6:9]+(0.35/5)

NO3_nc[nsrc_list[4],sgrminus<0]  = ((348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.74+0.25+0.18+0.12))
#NO3_nc[nsrc_list[4],6:9]  = ((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NH4_nc[nsrc_list[4],sgrminus<0]  = ((122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.74+0.25+0.18+0.12))
#NH4_nc[nsrc_list[4],6:9]  = ((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
DON_nc[nsrc_list[4],sgrminus<0]  = ((98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.74+0.25+0.18+0.12))
#DON_nc[nsrc_list[4],6:9]  = ((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.35+0.74+0.25+0.18+0.12))

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[4],sgrminus>0]  = ((NO3_nc[nsrc_list[4],sgrminus>0]*sgrminus[sgrminus>0]) +((348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
NO3_nc[nsrc_list[4],6]  = ((NO3_nc[nsrc_list[4],6]*sgrminus[6])+((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
NO3_nc[nsrc_list[4],7:9]  = ((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NO3_nc[nsrc_list[4:9]] = NO3_nc[nsrc_list[4]]


NH4_nc[nsrc_list[4],sgrminus>0]  = ((NH4_nc[nsrc_list[4],sgrminus>0]*sgrminus[sgrminus>0]) +((122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
NH4_nc[nsrc_list[4],6]  = ((NH4_nc[nsrc_list[4],6]*sgrminus[6])+((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
NH4_nc[nsrc_list[4],7:9]  = ((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NH4_nc[nsrc_list[4:9]] = NH4_nc[nsrc_list[4]]

DON_nc[nsrc_list[4],sgrminus>0]  = ((DON_nc[nsrc_list[4],sgrminus>0]*sgrminus[sgrminus>0]) +((98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
DON_nc[nsrc_list[4],6]  = ((DON_nc[nsrc_list[4],6]*sgrminus[6])+((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
DON_nc[nsrc_list[4],7:9]  = ((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
DON_nc[nsrc_list[4:9]] = DON_nc[nsrc_list[4]]


# Calleguas creek
calminus = Qbar_nc[nsrc_list[9],:] - (0.34+0.36+0.15)
Qbar_nc[nsrc_list[9],calminus<0] = 0.34+0.36+0.15
NO3_nc[nsrc_list[9],calminus<0]  = ((521.13*0.34)+(601.19*.36)+(447.11*.15))*(1/(0.34+0.36+0.15))
NH4_nc[nsrc_list[9],calminus<0]  = ((84.82*0.34)+(112.2*.36)+(72.14*.15))*(1/(0.34+0.36+0.15))
DON_nc[nsrc_list[9],calminus<0]  = ((94.05*0.34)+(45.8*.36)+(60.75*.15))*(1/(0.34+0.36+0.15))

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[9],calminus>0]  = ((NO3_nc[nsrc_list[9],calminus>0]*calminus[calminus>0])+((521.13*0.34)+(601.19*.36)+(447.11*.15)))*(1/((0.34+0.36+0.15)+calminus[calminus>0]))
NH4_nc[nsrc_list[9],calminus>0]  = ((NH4_nc[nsrc_list[9],calminus>0]*calminus[calminus>0])+((84.82*0.34)+(112.2*.36)+(72.14*.15)))*(1/((0.34+0.36+0.15)+calminus[calminus>0]))
DON_nc[nsrc_list[9],calminus>0]  = ((DON_nc[nsrc_list[9],calminus>0]*calminus[calminus>0])+((94.05*0.34)+(45.8*.36)+(60.75*.15)))*(1/((0.34+0.36+0.15)+calminus[calminus>0]))

# Malibu creek
# put values from reworked file with correct Malibu values
# /data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc
Qbar_nc[nsrc_list[10],:] = np.array([0.0349585178064516, 0.0529940352666667, 0.0730592920645162, 0.110288455633333, 0.496738697290323, 4.430423738, 9.01828875346428, 1.06463945796774, 0.392940615233333, 0.248019041806452, 0.0895765698666667, 0.0708578856451613])
NO3_nc[nsrc_list[10],:]  = np.array([ 28.7857142857143, 28.7857142857143, 28.7857142857143, 11.8982301743166, 96.2555972957793, 215.761867384518, 229.821428571428, 222.791647977973, 70.0110830802131, 28.7857142857143, 28.7857142857143, 28.7857142857143])
NH4_nc[nsrc_list[10],:]  = np.array([ 0.964285714285715, 0.964285714285715, 0.964285714285715, 2.1823834161324, 3.73482485873553, 5.93411690242329, 6.19285714285715, 6.06348702264022, 3.25184307659233, 0.964285714285715, 0.964285714285715, 0.964285714285715])
DON_nc[nsrc_list[10],:] = np.array([120,120,120,120,120,120,120,120,120,120,120,120])

malminus = Qbar_nc[nsrc_list[10],:] - .12 # subtract inland POTW discharge
Qbar_nc[nsrc_list[10],malminus<0] = .12 # set all negative flow to POTW flow
NO3_nc[nsrc_list[10],malminus<0] = 462.18 # set all constituents with -flow to POTW conc
NH4_nc[nsrc_list[10],malminus<0] = 76.05 # set all constituents with -flow to POTW conc
DON_nc[nsrc_list[10],malminus<0] = 74.79 # set all constituents with -flow to POTW conc

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[10],malminus>0]  = ((NO3_nc[nsrc_list[10],malminus>0]*malminus[malminus>0])+(.12*462.18))*(1/(.12+malminus[malminus>0]))
NH4_nc[nsrc_list[10],malminus>0]  = ((NH4_nc[nsrc_list[10],malminus>0]*malminus[malminus>0])+(.12*76.05))*(1/(.12+malminus[malminus>0]))
DON_nc[nsrc_list[10],malminus>0]  = ((DON_nc[nsrc_list[10],malminus>0]*malminus[malminus>0])+(.12*74.79))*(1/(.12+malminus[malminus>0]))

# San Diego Creek
#Qbar_nc[nsrc_list[11],:] = 0
# November to March only
#Qbar_nc[nsrc_list[11],4:9] = 0.07 # flow during this time is already higher
sdcminus = Qbar_nc[nsrc_list[11],:] - 0.07
Qbar_nc[nsrc_list[11],sdcminus<0] = .07 # set all negative flow to POTW flow
NO3_nc[nsrc_list[11],sdcminus<0] = 1097.07 
NH4_nc[nsrc_list[11],sdcminus<0] = 4.97  
DON_nc[nsrc_list[11],sdcminus<0] = 0

# do mass balance
NO3_nc[nsrc_list[11],4:9]  = ((NO3_nc[nsrc_list[11],4:9]*Qbar_nc[nsrc_list[11],4:9])+(0.07*1097.07))*(1./(Qbar_nc[nsrc_list[11],4:9]+0.07))
NH4_nc[nsrc_list[11],4:9]  = ((NH4_nc[nsrc_list[11],4:9]*Qbar_nc[nsrc_list[11],4:9])+(0.07*4.97))*(1./(Qbar_nc[nsrc_list[11],4:9]+0.07))
DON_nc[nsrc_list[11],4:9]  = ((DON_nc[nsrc_list[11],4:9]*Qbar_nc[nsrc_list[11],4:9])+(0.07*0))*(1./(Qbar_nc[nsrc_list[11],4:9]+0.07))

# San Diego River
#Qbar_nc[nsrc_list[12],:] = 0.63
sdrminus = Qbar_nc[nsrc_list[12],:] - 0.63
#NO3_nc[nsrc_list[12],:]  = 0
#NH4_nc[nsrc_list[12],:]  = 0
#DON_nc[nsrc_list[12],:]  = 118.06

Qbar_nc[nsrc_list[12],sdrminus<0] = .63 # set all negative flow to POTW flow
NO3_nc[nsrc_list[12],sdrminus<0] = 0 # set all constituents with -flow to POTW conc
NH4_nc[nsrc_list[12],sdrminus<0] = 0 # set all constituents with -flow to POTW conc
DON_nc[nsrc_list[12],sdrminus<0] = 118.06 # set all constituents with -flow to POTW conc

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[12],sdrminus>0]  = ((NO3_nc[nsrc_list[12],sdrminus>0]*sdrminus[sdrminus>0])+(.63*0))*(1/(.63+sdrminus[sdrminus>0]))
NH4_nc[nsrc_list[12],sdrminus>0]  = ((NH4_nc[nsrc_list[12],sdrminus>0]*sdrminus[sdrminus>0])+(.63*0))*(1/(.63+sdrminus[sdrminus>0]))
DON_nc[nsrc_list[12],sdrminus>0]  = ((DON_nc[nsrc_list[12],sdrminus>0]*sdrminus[sdrminus>0])+(.63*118.06))*(1/(.63+sdrminus[sdrminus>0]))

# Santa Clara River
#Qbar_nc[nsrc_list[13],:] = 0.22+0.56+0.32
scrminus = Qbar_nc[nsrc_list[13],:] - (0.22+0.56+0.32)
#NO3_nc[nsrc_list[13],:]  = ((345.54*.22)+(153.27*.56)+(584.82*.32))*(1/(0.22+0.56+0.32))
#NH4_nc[nsrc_list[13],:]  = ((63.88*.22)+(64.37*.56)+(39.8*.32))*(1/(0.22+0.56+0.32))
#DON_nc[nsrc_list[13],:]  = ((83.84*.22)+(93.02*.56)+(50.97*.32))*(1/(0.22+0.56+0.32))

# set all constituents with -flow to POTW conc
Qbar_nc[nsrc_list[13],scrminus<0] = 0.22+0.56+0.32 # set all negative flow to POTW flow
NO3_nc[nsrc_list[13],scrminus<0] = ((345.54*.22)+(153.27*.56)+(584.82*.32))*(1/(0.22+0.56+0.32)) 
NH4_nc[nsrc_list[13],scrminus<0] = ((63.88*.22)+(64.37*.56)+(39.8*.32))*(1/(0.22+0.56+0.32)) 
DON_nc[nsrc_list[13],scrminus<0] = ((83.84*.22)+(93.02*.56)+(50.97*.32))*(1/(0.22+0.56+0.32)) 
# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[13],scrminus>0]  = ((NO3_nc[nsrc_list[13],scrminus>0]*scrminus[scrminus>0])+((0.22+0.56+0.32)*((345.54*.22)+(153.27*.56)+(584.82*.32))))*(1/((0.22+0.56+0.32)+scrminus[scrminus>0]))
NH4_nc[nsrc_list[13],scrminus>0]  = ((NH4_nc[nsrc_list[13],scrminus>0]*scrminus[scrminus>0])+((0.22+0.56+0.32)*((63.88*.22)+(64.37*.56)+(39.8*.32))))*(1/((0.22+0.56+0.32)+scrminus[scrminus>0]))
DON_nc[nsrc_list[13],scrminus>0]  = ((DON_nc[nsrc_list[13],scrminus>0]*scrminus[scrminus>0])+((0.22+0.56+0.32)*((83.84*.22)+(93.02*.56)+(50.97*.32))))*(1/((0.22+0.56+0.32)+scrminus[scrminus>0]))

# Ventura River
#Qbar_nc[nsrc_list[14],:] = 0.07
verminus = Qbar_nc[nsrc_list[14],:] - 0.07
#NO3_nc[nsrc_list[14],:]  = 295.83
#NH4_nc[nsrc_list[14],:]  = 12.38
#DON_nc[nsrc_list[14],:]  = 117.79

Qbar_nc[nsrc_list[14],verminus<0] = .07 # set all negative flow to POTW flow
NO3_nc[nsrc_list[14],verminus<0] = 295.83 # set all constituents with -flow to POTW conc
NH4_nc[nsrc_list[14],verminus<0] = 12.38
DON_nc[nsrc_list[14],verminus<0] = 117.79

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[nsrc_list[14],verminus>0]  = ((NO3_nc[nsrc_list[14],verminus>0]*verminus[verminus>0])+(.07*295.83))*(1/(.07+verminus[verminus>0]))
NH4_nc[nsrc_list[14],verminus>0]  = ((NH4_nc[nsrc_list[14],verminus>0]*verminus[verminus>0])+(.07*12.38))*(1/(.07+verminus[verminus>0]))
DON_nc[nsrc_list[14],verminus>0]  = ((DON_nc[nsrc_list[14],verminus>0]*verminus[verminus>0])+(.07*117.79))*(1/(.07+verminus[verminus>0]))

# remove Tijuana river and SBIWTP
sbind = 111
tjind = 183


# make new netcdf

file_out = Dataset(file_path_out,'w')
# -2 for removed inputs
Nsrc_dim = file_out.createDimension('Nsrc',Qbar_nc.shape[0]-2)
Npas_dim = file_out.createDimension('Npas',Lsrc_nc.shape[0])
s_rho_dim = file_out.createDimension('s_rho',Qshape_nc.shape[0])

# loop over this time for Aug 1 1997 to Nov 31 1999 
# start Aug 1 2016, last time step is Nov 1 1999

# add 2 to time values because the times are at end of months 
# so simulation will start at beginning of month
# Jul 30 --> Aug 1
#psrc_final = psource_time_nc[6:27+7]+2 
# no need to change start time because ROMS interpolates

# 6 is Jul 30 1997 and ends in Nov 29 1999
psrc_final = psource_time_nc[6:27+8]

psrc_time_dim = file_out.createDimension('psrc_time',psrc_final.shape[0])

psrc_time_var = file_out.createVariable('psrc_time','float64',('psrc_time'))
psrc_time_var.units = 'days'
psrc_time_var.longname = 'point source time from 1994-1-1'
# psource loads for Aug 1 2016 to Jul 31 2017
#psrc_time_var[:] = psource_time_nc[p_st:p_en]
# loop over this time for Aug 1 1997 to Nov 31 1999 
# start Aug 1 2016, last time step is Nov 1 1999
#psrc_time_var[:] = psource_time_nc
psrc_time_var[:] = psrc_final

# time steps to add to loop the time
lp = 5

# put variables in new netcdf
# append same time series + last 5 (lp) times again to get 28 months
Qbar_var = file_out.createVariable('Qbar','float32',('Nsrc','psrc_time'))
Qbar_var.units = 'meter3 second-1'
Qbar_var.longname = 'vertically integrated mass transport of point'
#Qbar_var[:,:] = Qbar_nc
nclp = np.append(np.append(Qbar_nc,Qbar_nc,axis=1),Qbar_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
Qbar_var[:,:] = ncfi2

Qshape_var = file_out.createVariable('Qshape','float32',('s_rho','Nsrc'))
Qshape_var.units = 'no units'
Qshape_var.longname = 'Vertical weight of the flux for each psource cell'
nclp = Qshape_nc[:,:]
ncsl1 = np.append(nclp[:,:sbind],nclp[:,sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:,:sbind].shape[1] # 0 --> SBIWTP ind
ncshp2 = nclp[:,sbind+1:tjind].shape[1] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[0] # srho
ncshp3 = nclp[:,tjind+1:].shape[1] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshpt,ncshp1+ncshp2))
ncsl2 = np.append(ncsl1,nclp[:,tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshpt,ncshp1+ncshp2+ncshp3))
Qshape_var[:,:] = ncfi2

Isrc_var = file_out.createVariable('Isrc','float32',('Nsrc'))
Isrc_var.units = 'no units'
Isrc_var.longname = 'global xi-directional grid number of the point sources'
nclp = Isrc_nc[:]
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind])
ncsl2 = np.append(ncsl1,nclp[tjind+1:])
Isrc_var[:] = ncsl2

Jsrc_var = file_out.createVariable('Jsrc','float32',('Nsrc'))
Jsrc_var.units = 'no units'
Jsrc_var.longname = 'global xi-directional grid number of the point sources'
nclp = Jsrc_nc[:]
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind])
ncsl2 = np.append(ncsl1,nclp[tjind+1:])
Jsrc_var[:] = ncsl2

Dsrc_var = file_out.createVariable('Dsrc','float32',('Nsrc'))
Dsrc_var.units = 'no units'
Dsrc_var.longname = 'flag to determine direction of the mass point source'
nclp = Dsrc_nc[:]
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind])
ncsl2 = np.append(ncsl1,nclp[tjind+1:])
Dsrc_var[:] = ncsl2

Lsrc_var = file_out.createVariable('Lsrc','float32',('Npas','Nsrc'))
Lsrc_var.units = 'no units'
Lsrc_var.longname = 'logical switch for any tracers at every point source locations'
#Lsrc_var[:,:] = Lsrc_nc
Lsrc_var[:,:] = np.ones((Lsrc_var.shape[0],Lsrc_var.shape[1]))*np.nan

temp_var = file_out.createVariable('temp','float32',('Nsrc','psrc_time'))
temp_var.units = 'Degrees Celsius'
temp_var.longname = 'Temperature at point source'
#temp_var[:,:] = temp_nc
#temp_var[:,:] = np.append(np.append(temp_nc,temp_nc,axis=1),temp_nc[:,:lp],axis=1)
nclp = np.append(np.append(temp_nc,temp_nc,axis=1),temp_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
temp_var[:,:] = ncfi2


salt_var = file_out.createVariable('salt','float32',('Nsrc','psrc_time'))
salt_var.units = 'psu'
salt_var.longname = 'Salinity at point source'
#salt_var[:,:] = salt_nc
#salt_var[:,:] = np.append(np.append(salt_nc,salt_nc,axis=1),salt_nc[:,:lp],axis=1)
nclp = np.append(np.append(salt_nc,salt_nc,axis=1),salt_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
salt_var[:,:] = ncfi2

PO4_var = file_out.createVariable('PO4','float32',('Nsrc','psrc_time'))
PO4_var.units = 'mmol P m-3'
PO4_var.longname = 'averaged Phosphate'
#PO4_var[:,:] = PO4_nc
#PO4_var[:,:] = np.append(np.append(PO4_nc,PO4_nc,axis=1),PO4_nc[:,:lp],axis=1)
nclp = np.append(np.append(PO4_nc,PO4_nc,axis=1),PO4_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
PO4_var[:,:] = ncfi2

NO3_var = file_out.createVariable('NO3','float32',('Nsrc','psrc_time'))
NO3_var.units = 'mmol N m-3'
NO3_var.longname = 'averaged Nitrate'
#NO3_var[:,:] = NO3_nc
#NO3_var[:,:] = np.append(np.append(NO3_nc,NO3_nc,axis=1),NO3_nc[:,:lp],axis=1)
nclp = np.append(np.append(NO3_nc,NO3_nc,axis=1),NO3_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
NO3_var[:,:] = ncfi2

NH4_var = file_out.createVariable('NH4','float32',('Nsrc','psrc_time'))
NH4_var.units = 'mmol N m-3'
NH4_var.longname = 'averaged Ammonium'
#NH4_var[:,:] = NH4_nc
#NH4_var[:,:] = np.append(np.append(NH4_nc,NH4_nc,axis=1),NH4_nc[:,:lp],axis=1)
nclp = np.append(np.append(NH4_nc,NH4_nc,axis=1),NH4_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
NH4_var[:,:] = ncfi2

Fe_var = file_out.createVariable('Fe','float32',('Nsrc','psrc_time'))
Fe_var.units = 'mmol Fe m-3'
Fe_var.longname = 'averaged Iron'
#Fe_var[:,:] = Fe_nc
#Fe_var[:,:] = np.append(np.append(Fe_nc,Fe_nc,axis=1),Fe_nc[:,:lp],axis=1)
nclp = np.append(np.append(Fe_nc,Fe_nc,axis=1),Fe_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
Fe_var[:,:] = ncfi2

O2_var = file_out.createVariable('O2','float32',('Nsrc','psrc_time'))
O2_var.units = 'mmol O2 m-3'
O2_var.longname = 'averaged Oxygen'
#O2_var[:,:] = O2_nc
#O2_var[:,:] = np.append(np.append(O2_nc,O2_nc,axis=1),O2_nc[:,:lp],axis=1)
nclp = np.append(np.append(O2_nc,O2_nc,axis=1),O2_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
O2_var[:,:] = ncfi2

DIC_var = file_out.createVariable('DIC','float32',('Nsrc','psrc_time'))
DIC_var.units = 'mmol C m-3'
DIC_var.longname = 'averaged Dissolved inorganic carbon'
#DIC_var[:,:] = DIC_nc
#DIC_var[:,:] = np.append(np.append(DIC_nc,DIC_nc,axis=1),DIC_nc[:,:lp],axis=1)
nclp = np.append(np.append(DIC_nc,DIC_nc,axis=1),DIC_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
DIC_var[:,:] = ncfi2

Alk_var = file_out.createVariable('Alk','float32',('Nsrc','psrc_time'))
Alk_var.units = 'mmol m-3'
Alk_var.longname = 'averaged alkalinity'
#Alk_var[:,:] = Alk_nc
#Alk_var[:,:] = np.append(np.append(Alk_nc,Alk_nc,axis=1),Alk_nc[:,:lp],axis=1)
nclp = np.append(np.append(Alk_nc,Alk_nc,axis=1),Alk_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
Alk_var[:,:] = ncfi2

DOC_var = file_out.createVariable('DOC','float32',('Nsrc','psrc_time'))
DOC_var.units = 'mmol C m-3'
DOC_var.longname = 'averaged Dissolved organic carbon'
#DOC_var[:,:] = DOC_nc
#DOC_var[:,:] = np.append(np.append(DOC_nc,DOC_nc,axis=1),DOC_nc[:,:lp],axis=1)
nclp = np.append(np.append(DOC_nc,DOC_nc,axis=1),DOC_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
DOC_var[:,:] = ncfi2

DON_var = file_out.createVariable('DON','float32',('Nsrc','psrc_time'))
DON_var.units = 'mmol N m-3'
DON_var.longname = 'averaged Dissolved organic nitrogen'
#DON_var[:,:] = DON_nc
#DON_var[:,:] = np.append(np.append(DON_nc,DON_nc,axis=1),DON_nc[:,:lp],axis=1)
nclp = np.append(np.append(DON_nc,DON_nc,axis=1),DON_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
DON_var[:,:] = ncfi2

DOP_var = file_out.createVariable('DOP','float32',('Nsrc','psrc_time'))
DOP_var.units = 'mmol P m-3'
DOP_var.longname = 'averaged Dissolved organic phosphorus'
#DOP_var[:,:] = DOP_nc
#DOP_var[:,:] = np.append(np.append(DOP_nc,DOP_nc,axis=1),DOP_nc[:,:lp],axis=1)
nclp = np.append(np.append(DOP_nc,DOP_nc,axis=1),DOP_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
DOP_var[:,:] = ncfi2

NO2_var = file_out.createVariable('NO2','float32',('Nsrc','psrc_time'))
NO2_var.units = 'mmol N m-3'
NO2_var.longname = 'averaged Nitrite'
#NO2_var[:,:] = NO2_nc
#NO2_var[:,:] = np.append(np.append(NO2_nc,NO2_nc,axis=1),NO2_nc[:,:lp],axis=1)
nclp = np.append(np.append(NO2_nc,NO2_nc,axis=1),NO2_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
NO2_var[:,:] = ncfi2

SO3_var = file_out.createVariable('SiO3','float32',('Nsrc','psrc_time'))
SO3_var.units = 'mmol N m-3'
SO3_var.longname = 'averaged Silicate'
#SO3_var[:,:] = NO2_nc
#SO3_var[:,:] = np.append(np.append(SiO3_nc,SiO3_nc,axis=1),SiO3_nc[:,:lp],axis=1)
nclp = np.append(np.append(SiO3_nc,SiO3_nc,axis=1),SiO3_nc[:,:lp],axis=1)
ncsl1 = np.append(nclp[:sbind],nclp[sbind+1:tjind]) # skip SBIWTP
ncshp1 = nclp[:sbind].shape[0] # 0 --> SBIWTP ind
ncshp2 = nclp[sbind+1:tjind].shape[0] # SBIWTP+1(skip it) --> Tijuana
ncshpt = nclp[:sbind].shape[1] # time ind
ncshp3 = nclp[tjind+1:].shape[0] # Tijuana+1(skip it) --> end
ncfi1 = ncsl1.reshape((ncshp1+ncshp2,ncshpt))
ncsl2 = np.append(ncsl1,nclp[tjind+1:]) # skip Tijuana 
ncfi2 = ncsl2.reshape((ncshp1+ncshp2+ncshp3,ncshpt))
SO3_var[:,:] = ncfi2

file_out.close()
