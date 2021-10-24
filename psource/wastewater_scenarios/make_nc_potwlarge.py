# 2017 loads in Aug 1997- Nov 1998
from netCDF4 import Dataset,num2date
import numpy as np
import pandas as pd

# roms psource file to copy and remake
file_path = '/data/project1/minnaho/psource/run_fixjwpcp/roms_psource_102020_full.767.nc'
file_path_out = '/data/project1/minnaho/psource/wastewater_scenarios/roms_psource_potwlarge.nc'
file_nc = Dataset(file_path,'r')


Qbar_nc   = np.array(file_nc.variables['Qbar'][:,:])
# end psources before rivers to exclude rivers
end_ind = 96
#end_ind = Qbar_nc.shape[0]

# psource time is actually days since 1994-01-01
psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
psrc_dt = num2date(psource_time_nc,'days since 1994-01-01',only_use_cftime_datetimes=False)

# psrc time starts at 1997-01-30
# only choose Aug 2016 - Jul 2017
p_st = -17
p_en = -5

Qbar_nc   = np.array(file_nc.variables['Qbar'][:end_ind,p_st:p_en])

Qshape_nc = np.array(file_nc.variables['Qshape'][:,:end_ind])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][:end_ind])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][:end_ind])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][:end_ind])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,:end_ind])

# read in input file 
temp_nc = np.array(file_nc.variables['temp'][:end_ind,p_st:p_en])
salt_nc = np.array(file_nc.variables['salt'][:end_ind,p_st:p_en])
PO4_nc = np.array(file_nc.variables['PO4'][:end_ind,p_st:p_en])
NO3_nc = np.array(file_nc.variables['NO3'][:end_ind,p_st:p_en])
NH4_nc = np.array(file_nc.variables['NH4'][:end_ind,p_st:p_en])
Fe_nc  = np.array(file_nc.variables['Fe'][:end_ind,p_st:p_en])
O2_nc  = np.array(file_nc.variables['O2'][:end_ind,p_st:p_en])
DIC_nc = np.array(file_nc.variables['DIC'][:end_ind,p_st:p_en])
Alk_nc = np.array(file_nc.variables['Alk'][:end_ind,p_st:p_en])
DOC_nc = np.array(file_nc.variables['DOC'][:end_ind,p_st:p_en])
DON_nc = np.array(file_nc.variables['DON'][:end_ind,p_st:p_en])
DOP_nc = np.array(file_nc.variables['DOP'][:end_ind,p_st:p_en])
NO2_nc = np.array(file_nc.variables['NO2'][:end_ind,p_st:p_en])
SiO3_nc = np.array(file_nc.variables['SiO3'][:end_ind,p_st:p_en])

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

file_out.close()
