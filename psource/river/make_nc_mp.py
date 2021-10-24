# 2017 loads in Aug 1997- Nov 1998
# file with corrected inland POTW
# add microplastic variables to test
# just OCSan, LA River, San Gabriel River, Santa Ana River
from netCDF4 import Dataset,num2date
import numpy as np
import pandas as pd

# roms psource file to copy and remake
file_path = '/data/project1/minnaho/psource/run_fixjwpcp/roms_psource_102020_full.767.nc'
file_path_out = '/data/project1/minnaho/psource/river/roms_psource_mp.nc'
file_nc = Dataset(file_path,'r')


Qbar_nc   = np.array(file_nc.variables['Qbar'][:,:])
# end psources before rivers to exclude rivers
#end_ind = 115 # end of all POTWs, start of rivers
end_ind = Qbar_nc.shape[0]

# LA river, San Gabriel, Calleguas, Malibu creek, San Diego Creek,
# San Diego River, Santa clara river, ventura river
# see /data/project1/minnaho/find_inputs_coords/river_points.py
rivst = 115
nsrc_list = list(range(56,70))+[rivst+32,190,191,192,rivst+51,193,194,195,196,rivst+60]

ocend = len(range(56,70))

rivlist = list(range(ocend,len(nsrc_list)))

# psource time is actually days since 1994-01-01
psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
psrc_dt = num2date(psource_time_nc,'days since 1994-01-01',only_use_cftime_datetimes=False)

# psrc time starts at 1997-01-30
# only choose Aug 2016 - Jul 2017
p_st = -17
p_en = -5

Qbar_nc   = np.array(file_nc.variables['Qbar'][nsrc_list,p_st:p_en])

Qshape_nc = np.array(file_nc.variables['Qshape'][:,nsrc_list])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][nsrc_list])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][nsrc_list])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][nsrc_list])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,nsrc_list])

# read in input file 
temp_nc = np.array(file_nc.variables['temp'][nsrc_list,p_st:p_en])
salt_nc = np.array(file_nc.variables['salt'][nsrc_list,p_st:p_en])
PO4_nc = np.array(file_nc.variables['PO4'][nsrc_list,p_st:p_en])
NO3_nc = np.array(file_nc.variables['NO3'][nsrc_list,p_st:p_en])
NH4_nc = np.array(file_nc.variables['NH4'][nsrc_list,p_st:p_en])
Fe_nc  = np.array(file_nc.variables['Fe'][nsrc_list,p_st:p_en])
O2_nc  = np.array(file_nc.variables['O2'][nsrc_list,p_st:p_en])
DIC_nc = np.array(file_nc.variables['DIC'][nsrc_list,p_st:p_en])
Alk_nc = np.array(file_nc.variables['Alk'][nsrc_list,p_st:p_en])
DOC_nc = np.array(file_nc.variables['DOC'][nsrc_list,p_st:p_en])
DON_nc = np.array(file_nc.variables['DON'][nsrc_list,p_st:p_en])
DOP_nc = np.array(file_nc.variables['DOP'][nsrc_list,p_st:p_en])
NO2_nc = np.array(file_nc.variables['NO2'][nsrc_list,p_st:p_en])
SiO3_nc = np.array(file_nc.variables['SiO3'][nsrc_list,p_st:p_en])

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
larminus = Qbar_nc[rivlist[0],:] - ((1.05+0.39+0.19)/4) 
# set all negative flow to POTW flow
Qbar_nc[rivlist[0],larminus<0] = (1.05+0.39+0.19)/4
Qbar_nc[rivlist[0:4]] = Qbar_nc[rivlist[0]]

# set all constituents with -flow to POTW conc
NO3_nc[rivlist[0],larminus<0] = ((398.27*1.05)+(307.17*.39)+(467.7*.19))*(1/(1.05+.39+.19))
NH4_nc[rivlist[0],larminus<0] = ((96.84*1.05)+(101.43*.39)+(79.29*.19))*(1/(1.05+.39+.19)) 
DON_nc[rivlist[0],larminus<0] = ((106.53*1.05)+(84.97*.39)+(65.26*.19))*(1/(1.05+.39+.19)) 

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[rivlist[0],larminus>0]  = ((NO3_nc[rivlist[0],larminus>0]*larminus[larminus>0]) +((398.27*1.05)+(307.17*.39)+(467.7*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

NO3_nc[rivlist[0:4]] = NO3_nc[rivlist[0]]

NH4_nc[rivlist[0],larminus>0]  = ((NH4_nc[rivlist[0],larminus>0]*larminus[larminus>0]) +((96.84*1.05)+(101.43*.39)+(79.29*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

NH4_nc[rivlist[0:4]] = NH4_nc[rivlist[0]]

DON_nc[rivlist[0],larminus>0]  = ((DON_nc[rivlist[0],larminus>0]*larminus[larminus>0]) +((106.53*1.05)+(84.97*.39)+(65.26*.19)))*(1/((1.05+0.39+0.19)+larminus[larminus>0]))

DON_nc[rivlist[0:4]] = DON_nc[rivlist[0]]

# SG river
# divide over number of cells spreading (5 cells)
# subtract inland POTW discharge
sgrminus = Qbar_nc[rivlist[4],:] - (0.74+0.25+0.18+0.12)/5
# set all negative flow to POTW flow
Qbar_nc[rivlist[4],sgrminus<0] = (0.74+0.25+0.18+0.12)/5
Qbar_nc[rivlist[4:9]] = Qbar_nc[rivlist[4]]

# add flow to just Jan-Mar for one of the plants that has 
# intermittent discharge
Qbar_nc[rivlist[4:9],6:9] = Qbar_nc[rivlist[4:9],6:9]+(0.35/5)

NO3_nc[rivlist[4],sgrminus<0]  = ((348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.74+0.25+0.18+0.12))
#NO3_nc[rivlist[4],6:9]  = ((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NH4_nc[rivlist[4],sgrminus<0]  = ((122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.74+0.25+0.18+0.12))
#NH4_nc[rivlist[4],6:9]  = ((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
DON_nc[rivlist[4],sgrminus<0]  = ((98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.74+0.25+0.18+0.12))
#DON_nc[rivlist[4],6:9]  = ((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.35+0.74+0.25+0.18+0.12))

# do mass balance on non-inlandPOTW and inlandPOTW flow
NO3_nc[rivlist[4],sgrminus>0]  = ((NO3_nc[rivlist[4],sgrminus>0]*sgrminus[sgrminus>0]) +((348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
NO3_nc[rivlist[4],6]  = ((NO3_nc[rivlist[4],6]*sgrminus[6])+((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
NO3_nc[rivlist[4],7:9]  = ((474.43*0.35)+(348.48*0.74)+(469.40*0.25)+(489.80*0.18)+(478.04*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NO3_nc[rivlist[4:9]] = NO3_nc[rivlist[4]]


NH4_nc[rivlist[4],sgrminus>0]  = ((NH4_nc[rivlist[4],sgrminus>0]*sgrminus[sgrminus>0]) +((122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
NH4_nc[rivlist[4],6]  = ((NH4_nc[rivlist[4],6]*sgrminus[6])+((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
NH4_nc[rivlist[4],7:9]  = ((98.57*0.35)+(122.20*0.74)+(90.95*0.25)+(31.68*0.18)+(115.95*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
NH4_nc[rivlist[4:9]] = NH4_nc[rivlist[4]]

DON_nc[rivlist[4],sgrminus>0]  = ((DON_nc[rivlist[4],sgrminus>0]*sgrminus[sgrminus>0]) +((98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12)))*(1/((0.74+0.25+0.18+0.12)+sgrminus[sgrminus>0]))
# of intermittent discharge period, only index 6 lines up with when sgrminus>0
DON_nc[rivlist[4],6]  = ((DON_nc[rivlist[4],6]*sgrminus[6])+((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12)))*(1/((0.35+0.74+0.25+0.18+0.12)+sgrminus[6]))
# change indices 7 and 8 to the 5 discharges
DON_nc[rivlist[4],7:9]  = ((90.77*0.35)+(98.63*0.74)+(139.38*0.25)+(47.52*0.18)+(98.25*.12))*(1/(0.35+0.74+0.25+0.18+0.12))
DON_nc[rivlist[4:9]] = DON_nc[rivlist[4]]


# make new netcdf

file_out = Dataset(file_path_out,'w')
Nsrc_dim = file_out.createDimension('Nsrc',Qbar_nc.shape[0])
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
Qbar_var[:,:] = np.append(np.append(Qbar_nc,Qbar_nc,axis=1),Qbar_nc[:,:lp],axis=1)

Qshape_var = file_out.createVariable('Qshape','float32',('s_rho','Nsrc'))
Qshape_var.units = 'no units'
Qshape_var.longname = 'Vertical weight of the flux for each psource cell'
Qshape_var[:,:] = Qshape_nc

Isrc_var = file_out.createVariable('Isrc','float32',('Nsrc'))
Isrc_var.units = 'no units'
Isrc_var.longname = 'global xi-directional grid number of the point sources'
Isrc_var[:] = Isrc_nc

Jsrc_var = file_out.createVariable('Jsrc','float32',('Nsrc'))
Jsrc_var.units = 'no units'
Jsrc_var.longname = 'global xi-directional grid number of the point sources'
Jsrc_var[:] = Jsrc_nc

Dsrc_var = file_out.createVariable('Dsrc','float32',('Nsrc'))
Dsrc_var.units = 'no units'
Dsrc_var.longname = 'flag to determine direction of the mass point source'
Dsrc_var[:] = Dsrc_nc

Lsrc_var = file_out.createVariable('Lsrc','float32',('Npas','Nsrc'))
Lsrc_var.units = 'no units'
Lsrc_var.longname = 'logical switch for any tracers at every point source locations'
Lsrc_var[:,:] = Lsrc_nc

temp_var = file_out.createVariable('temp','float32',('Nsrc','psrc_time'))
temp_var.units = 'Degrees Celsius'
temp_var.longname = 'Temperature at point source'
#temp_var[:,:] = temp_nc
temp_var[:,:] = np.append(np.append(temp_nc,temp_nc,axis=1),temp_nc[:,:lp],axis=1)

salt_var = file_out.createVariable('salt','float32',('Nsrc','psrc_time'))
salt_var.units = 'psu'
salt_var.longname = 'Salinity at point source'
#salt_var[:,:] = salt_nc
salt_var[:,:] = np.append(np.append(salt_nc,salt_nc,axis=1),salt_nc[:,:lp],axis=1)

PO4_var = file_out.createVariable('PO4','float32',('Nsrc','psrc_time'))
PO4_var.units = 'mmol P m-3'
PO4_var.longname = 'averaged Phosphate'
#PO4_var[:,:] = PO4_nc
PO4_var[:,:] = np.append(np.append(PO4_nc,PO4_nc,axis=1),PO4_nc[:,:lp],axis=1)

NO3_var = file_out.createVariable('NO3','float32',('Nsrc','psrc_time'))
NO3_var.units = 'mmol N m-3'
NO3_var.longname = 'averaged Nitrate'
#NO3_var[:,:] = NO3_nc
NO3_var[:,:] = np.append(np.append(NO3_nc,NO3_nc,axis=1),NO3_nc[:,:lp],axis=1)

NH4_var = file_out.createVariable('NH4','float32',('Nsrc','psrc_time'))
NH4_var.units = 'mmol N m-3'
NH4_var.longname = 'averaged Ammonium'
#NH4_var[:,:] = NH4_nc
NH4_var[:,:] = np.append(np.append(NH4_nc,NH4_nc,axis=1),NH4_nc[:,:lp],axis=1)

Fe_var = file_out.createVariable('Fe','float32',('Nsrc','psrc_time'))
Fe_var.units = 'mmol Fe m-3'
Fe_var.longname = 'averaged Iron'
#Fe_var[:,:] = Fe_nc
Fe_var[:,:] = np.append(np.append(Fe_nc,Fe_nc,axis=1),Fe_nc[:,:lp],axis=1)

O2_var = file_out.createVariable('O2','float32',('Nsrc','psrc_time'))
O2_var.units = 'mmol O2 m-3'
O2_var.longname = 'averaged Oxygen'
#O2_var[:,:] = O2_nc
O2_var[:,:] = np.append(np.append(O2_nc,O2_nc,axis=1),O2_nc[:,:lp],axis=1)

DIC_var = file_out.createVariable('DIC','float32',('Nsrc','psrc_time'))
DIC_var.units = 'mmol C m-3'
DIC_var.longname = 'averaged Dissolved inorganic carbon'
#DIC_var[:,:] = DIC_nc
DIC_var[:,:] = np.append(np.append(DIC_nc,DIC_nc,axis=1),DIC_nc[:,:lp],axis=1)

Alk_var = file_out.createVariable('Alk','float32',('Nsrc','psrc_time'))
Alk_var.units = 'mmol m-3'
Alk_var.longname = 'averaged alkalinity'
#Alk_var[:,:] = Alk_nc
Alk_var[:,:] = np.append(np.append(Alk_nc,Alk_nc,axis=1),Alk_nc[:,:lp],axis=1)

DOC_var = file_out.createVariable('DOC','float32',('Nsrc','psrc_time'))
DOC_var.units = 'mmol C m-3'
DOC_var.longname = 'averaged Dissolved organic carbon'
#DOC_var[:,:] = DOC_nc
DOC_var[:,:] = np.append(np.append(DOC_nc,DOC_nc,axis=1),DOC_nc[:,:lp],axis=1)

DON_var = file_out.createVariable('DON','float32',('Nsrc','psrc_time'))
DON_var.units = 'mmol N m-3'
DON_var.longname = 'averaged Dissolved organic nitrogen'
#DON_var[:,:] = DON_nc
DON_var[:,:] = np.append(np.append(DON_nc,DON_nc,axis=1),DON_nc[:,:lp],axis=1)

DOP_var = file_out.createVariable('DOP','float32',('Nsrc','psrc_time'))
DOP_var.units = 'mmol P m-3'
DOP_var.longname = 'averaged Dissolved organic phosphorus'
#DOP_var[:,:] = DOP_nc
DOP_var[:,:] = np.append(np.append(DOP_nc,DOP_nc,axis=1),DOP_nc[:,:lp],axis=1)

NO2_var = file_out.createVariable('NO2','float32',('Nsrc','psrc_time'))
NO2_var.units = 'mmol N m-3'
NO2_var.longname = 'averaged Nitrite'
#NO2_var[:,:] = NO2_nc
NO2_var[:,:] = np.append(np.append(NO2_nc,NO2_nc,axis=1),NO2_nc[:,:lp],axis=1)

SO3_var = file_out.createVariable('SiO3','float32',('Nsrc','psrc_time'))
SO3_var.units = 'mmol N m-3'
SO3_var.longname = 'averaged Silicate'
#SO3_var[:,:] = NO2_nc
SO3_var[:,:] = np.append(np.append(SiO3_nc,SiO3_nc,axis=1),SiO3_nc[:,:lp],axis=1)

# microplastic variables
# nonbuoyant, buoyant, and settling
mp_nb_var = file_out.createVariable('mp_nb','float32',('Nsrc','psrc_time'))
mp_nb_var.units = 'mmol N m-3'
mp_nb_var.longname = 'microplastics neutrally buoyant'
mp_nb_var[:,:] = np.repeat(np.nanmean(NH4_nc,axis=1)[:,np.newaxis],psrc_final.shape[0],axis=1)

mp_b_var = file_out.createVariable('mp_b','float32',('Nsrc','psrc_time'))
mp_b_var.units = 'mmol N m-3'
mp_b_var.longname = 'microplastics buoyant'
mp_b_var[:,:] = np.repeat(np.nanmean(NH4_nc,axis=1)[:,np.newaxis],psrc_final.shape[0],axis=1)

mp_s_var = file_out.createVariable('mp_s','float32',('Nsrc','psrc_time'))
mp_s_var.units = 'mmol N m-3'
mp_s_var.longname = 'microplastics negatively buoyant - settling'
mp_s_var[:,:] = np.repeat(np.nanmean(NH4_nc,axis=1)[:,np.newaxis],psrc_final.shape[0],axis=1)


file_out.close()
