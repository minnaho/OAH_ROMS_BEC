from netCDF4 import Dataset,num2date
import numpy as np

file_path = '/data/project1/minnaho/psource/ocsd_psource/recyling_env_impacts/roms_psource_ocsd_realistic_1999_2008.nc'
file_path_out = 'roms_psource_ocsd_1999_avg.nc'
file_nc = Dataset(file_path,'r')

# psource data
ocsd_st = 0
ocsd_en = 14

psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
Qshape_nc = np.array(file_nc.variables['Qshape'][:,ocsd_st:ocsd_en])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][ocsd_st:ocsd_en])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][ocsd_st:ocsd_en])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][ocsd_st:ocsd_en])

# ocsd data
potw_nc = Dataset('/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017.nc')

potw_ti = num2date(np.array(potw_nc.variables['time']),potw_nc.variables['time'].units,only_use_cftime_datetimes=False)

# 1999 starts
stin = 10227
enin = stin+265

# number of time steps
# number of days between 1997-08-01 to 1999-12-31
tstep = 883

potw_fl = np.nanmean(np.array(potw_nc.variables['flow'])[stin:enin,2])
potw_tm = np.nanmean(np.array(potw_nc.variables['temperature'])[stin:enin,2])
potw_sl = np.nanmean(np.array(potw_nc.variables['salinity'])[stin:enin,2])
potw_po = np.nanmean(np.array(potw_nc.variables['PO4'])[stin:enin,2])
potw_no = np.nanmean(np.array(potw_nc.variables['NO3'])[stin:enin,2])
potw_si = np.nanmean(np.array(potw_nc.variables['SiO4'])[stin:enin,2])
potw_nh = np.nanmean(np.array(potw_nc.variables['NH4'])[stin:enin,2])
potw_fe = np.nanmean(np.array(potw_nc.variables['dissolved_Fe'])[stin:enin,2])
potw_o2 = np.nanmean(np.array(potw_nc.variables['dissolved_oxygen'])[stin:enin,2])
# DIC needs to be calculated, use matlab script
#potw_di = np.ones((tstep))*np.nanmean(np.array(potw_nc.variables[''])[stin:enin,2])
potw_di = 6343.7
potw_ak = np.nanmean(np.array(potw_nc.variables['alkalinity'])[stin:enin,2])
potw_do = np.nanmean(np.array(potw_nc.variables['total_organic_C'])[stin:enin,2])
potw_dn = np.nanmean(np.array(potw_nc.variables['organic_N'])[stin:enin,2])
potw_dp = np.nanmean(np.array(potw_nc.variables['organic_P'])[stin:enin,2])
potw_n2 = np.nanmean(np.array(potw_nc.variables['NO2'])[stin:enin,2])
potw_ph = np.nanmean(np.array(potw_nc.variables['pH'])[stin:enin,2])

# make new netcdf

file_out = Dataset(file_path_out,'w')
file_out.title = 'psource file of just OCSD inputs averaged 1999 loads run for Oct 1997- Jul 1999 simulation'
Nsrc_dim = file_out.createDimension('Nsrc',Qshape_nc.shape[1])
Npas_dim = file_out.createDimension('Npas',14)
s_rho_dim = file_out.createDimension('s_rho',Qshape_nc.shape[0])
psrc_time_dim = file_out.createDimension('psrc_time',tstep)

psrc_time_var = file_out.createVariable('psrc_time','float64',('psrc_time'))
psrc_time_var.units = 'days since 1997-08-01'
psrc_time_var.longname = 'point source time from 1999-08-01'
psrc_time_var[:] = np.arange(tstep)

Qbar_var = file_out.createVariable('Qbar','float32',('Nsrc','psrc_time'))
Qbar_var.units = 'meter3 second-1'
Qbar_var.longname = 'vertically integrated mass transport of point'

Qbar_var[0,:]  = potw_fl*(5/14) 
Qbar_var[6,:]  = potw_fl*(5/14) 
                              
Qbar_var[4,:]  = potw_fl*((1/2)/14)
Qbar_var[9,:]  = potw_fl*((1/2)/14)
Qbar_var[7,:]  = potw_fl*((1/2)/14)
Qbar_var[10,:] = potw_fl*((1/2)/14)
Qbar_var[5,:]  = potw_fl*((1/2)/14)
Qbar_var[2,:]  = potw_fl*((1/2)/14)
                        
Qbar_var[3,:]  = potw_fl*((1/6)/14)
Qbar_var[8,:]  = potw_fl*((1/6)/14)
Qbar_var[1,:]  = potw_fl*((1/6)/14)
Qbar_var[13,:] = potw_fl*((1/6)/14)
Qbar_var[12,:] = potw_fl*((1/6)/14)
Qbar_var[11,:] = potw_fl*((1/6)/14)

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
Lsrc_var[:,:] = np.ones((Lsrc_var.shape[0],Lsrc_var.shape[1]))

temp_var = file_out.createVariable('temp','float32',('Nsrc','psrc_time'))
temp_var.units = 'Degrees Celsius'
temp_var.longname = 'Temperature at point source'
temp_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_tm

salt_var = file_out.createVariable('salt','float32',('Nsrc','psrc_time'))
salt_var.units = 'psu'
salt_var.longname = 'Salinity at point source'
salt_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_sl

PO4_var = file_out.createVariable('PO4','float32',('Nsrc','psrc_time'))
PO4_var.units = 'mmol P m-3'
PO4_var.longname = 'averaged Phosphate'
PO4_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_po

NO3_var = file_out.createVariable('NO3','float32',('Nsrc','psrc_time'))
NO3_var.units = 'mmol N m-3'
NO3_var.longname = 'averaged Nitrate'
NO3_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_no

SiO3_var = file_out.createVariable('SiO3','float32',('Nsrc','psrc_time'))
SiO3_var.units = 'mmol N m-3'
SiO3_var.longname = 'averaged Nitrite'
SiO3_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_si

NH4_var = file_out.createVariable('NH4','float32',('Nsrc','psrc_time'))
NH4_var.units = 'mmol N m-3'
NH4_var.longname = 'averaged Ammonium'
NH4_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_nh

Fe_var = file_out.createVariable('Fe','float32',('Nsrc','psrc_time'))
Fe_var.units = 'mmol Fe m-3'
Fe_var.longname = 'averaged Iron'
Fe_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_fe

O2_var = file_out.createVariable('O2','float32',('Nsrc','psrc_time'))
O2_var.units = 'mmol O2 m-3'
O2_var.longname = 'averaged Oxygen'
O2_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_o2

DIC_var = file_out.createVariable('DIC','float32',('Nsrc','psrc_time'))
DIC_var.units = 'mmol C m-3'
DIC_var.longname = 'averaged Dissolved inorganic carbon'
DIC_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_di

Alk_var = file_out.createVariable('Alk','float32',('Nsrc','psrc_time'))
Alk_var.units = 'mmol m-3'
Alk_var.longname = 'averaged alkalinity'
Alk_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_ak

DOC_var = file_out.createVariable('DOC','float32',('Nsrc','psrc_time'))
DOC_var.units = 'mmol C m-3'
DOC_var.longname = 'averaged Dissolved organic carbon'
DOC_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_do

DON_var = file_out.createVariable('DON','float32',('Nsrc','psrc_time'))
DON_var.units = 'mmol N m-3'
DON_var.longname = 'averaged Dissolved organic nitrogen'
DON_var[:,:] = np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_dn

DOP_var = file_out.createVariable('DOP','float32',('Nsrc','psrc_time'))
DOP_var.units = 'mmol P m-3'
DOP_var.longname = 'averaged Dissolved organic phosphorus'
DOP_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_dp

NO2_var = file_out.createVariable('NO2','float32',('Nsrc','psrc_time'))
NO2_var.units = 'mmol N m-3'
NO2_var.longname = 'averaged Nitrite'
NO2_var[:,:] =np.ones((Qbar_var.shape[0],psrc_time_var.shape[0]))*potw_n2

file_out.close()
