from netCDF4 import Dataset
import numpy as np

file_path = '/data/project1/minnaho/psource/roms_psource_newocsd.nc'
file_path_out = 'roms_psource_ocsd_realistic1999.nc'
file_nc = Dataset(file_path,'r')

ocsd_in = range(56,69+1) # ocsd indices are 56-69
ocsd_st = 56
ocsd_en = 69+1

psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
Qbar_nc   = np.array(file_nc.variables['Qbar'][ocsd_st:ocsd_en,:])
Qshape_nc = np.array(file_nc.variables['Qshape'][:,ocsd_st:ocsd_en])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][ocsd_st:ocsd_en])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][ocsd_st:ocsd_en])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][ocsd_st:ocsd_en])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,ocsd_st:ocsd_en])

temp_nc   = np.array(file_nc.variables['temp'][ocsd_st:ocsd_en,:])
salt_nc   = np.array(file_nc.variables['salt'][ocsd_st:ocsd_en,:])
PO4_nc   = np.array(file_nc.variables['PO4'][ocsd_st:ocsd_en,:])
NO3_nc   = np.array(file_nc.variables['NO3'][ocsd_st:ocsd_en,:])
NH4_nc   = np.array(file_nc.variables['NH4'][ocsd_st:ocsd_en,:])
Fe_nc   = np.array(file_nc.variables['Fe'][ocsd_st:ocsd_en,:])
O2_nc   = np.array(file_nc.variables['O2'][ocsd_st:ocsd_en,:])
DIC_nc   = np.array(file_nc.variables['DIC'][ocsd_st:ocsd_en,:])
Alk_nc   = np.array(file_nc.variables['Alk'][ocsd_st:ocsd_en,:])
DOC_nc   = np.array(file_nc.variables['DOC'][ocsd_st:ocsd_en,:])
DON_nc   = np.array(file_nc.variables['DON'][ocsd_st:ocsd_en,:])
DOP_nc   = np.array(file_nc.variables['DOP'][ocsd_st:ocsd_en,:])
NO2_nc   = np.array(file_nc.variables['NO2'][ocsd_st:ocsd_en,:])

# make new netcdf

file_out = Dataset(file_path_out,'w')
file_out.title = 'psource file of just OCSD inputs for realistic 1999 run'
Nsrc_dim = file_out.createDimension('Nsrc',Qbar_nc.shape[0])
Npas_dim = file_out.createDimension('Npas',Lsrc_nc.shape[0])
s_rho_dim = file_out.createDimension('s_rho',Qshape_nc.shape[0])
psrc_time_dim = file_out.createDimension('psrc_time',psource_time_nc.shape[0])

psrc_time_var = file_out.createVariable('psrc_time','float64',('psrc_time'))
psrc_time_var.units = 'days since 1994-01-01'
psrc_time_var.longname = 'point source time from 1994-1-1'
psrc_time_var[:] = psource_time_nc

Qbar_var = file_out.createVariable('Qbar','float32',('Nsrc','psrc_time'))
Qbar_var.units = 'meter3 second-1'
Qbar_var.longname = 'vertically integrated mass transport of point'
Qbar_var[:,:] = Qbar_nc

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
temp_var[:,:] = temp_nc

salt_var = file_out.createVariable('salt','float32',('Nsrc','psrc_time'))
salt_var.units = 'psu'
salt_var.longname = 'Salinity at point source'
salt_var[:,:] = salt_nc

PO4_var = file_out.createVariable('PO4','float32',('Nsrc','psrc_time'))
PO4_var.units = 'mmol P m-3'
PO4_var.longname = 'averaged Phosphate'
PO4_var[:,:] = PO4_nc

NO3_var = file_out.createVariable('NO3','float32',('Nsrc','psrc_time'))
NO3_var.units = 'mmol N m-3'
NO3_var.longname = 'averaged Nitrate'
NO3_var[:,:] = NO3_nc

NH4_var = file_out.createVariable('NH4','float32',('Nsrc','psrc_time'))
NH4_var.units = 'mmol N m-3'
NH4_var.longname = 'averaged Ammonium'
NH4_var[:,:] = NH4_nc

Fe_var = file_out.createVariable('Fe','float32',('Nsrc','psrc_time'))
Fe_var.units = 'mmol Fe m-3'
Fe_var.longname = 'averaged Iron'
Fe_var[:,:] = Fe_nc

O2_var = file_out.createVariable('O2','float32',('Nsrc','psrc_time'))
O2_var.units = 'mmol O2 m-3'
O2_var.longname = 'averaged Oxygen'
O2_var[:,:] = O2_nc

DIC_var = file_out.createVariable('DIC','float32',('Nsrc','psrc_time'))
DIC_var.units = 'mmol C m-3'
DIC_var.longname = 'averaged Dissolved inorganic carbon'
DIC_var[:,:] = DIC_nc

Alk_var = file_out.createVariable('Alk','float32',('Nsrc','psrc_time'))
Alk_var.units = 'mmol m-3'
Alk_var.longname = 'averaged alkalinity'
Alk_var[:,:] = Alk_nc

DOC_var = file_out.createVariable('DOC','float32',('Nsrc','psrc_time'))
DOC_var.units = 'mmol C m-3'
DOC_var.longname = 'averaged Dissolved organic carbon'
DOC_var[:,:] = DOC_nc

DON_var = file_out.createVariable('DON','float32',('Nsrc','psrc_time'))
DON_var.units = 'mmol N m-3'
DON_var.longname = 'averaged Dissolved organic nitrogen'
DON_var[:,:] = DON_nc

DOP_var = file_out.createVariable('DOP','float32',('Nsrc','psrc_time'))
DOP_var.units = 'mmol P m-3'
DOP_var.longname = 'averaged Dissolved organic phosphorus'
DOP_var[:,:] = DOP_nc

NO2_var = file_out.createVariable('NO2','float32',('Nsrc','psrc_time'))
NO2_var.units = 'mmol N m-3'
NO2_var.longname = 'averaged Nitrite'
NO2_var[:,:] = NO2_nc

file_out.close()
