# uses corrected loads
from netCDF4 import Dataset,num2date
import numpy as np

file_path = '/data/project3/minnaho/roms_psource_102020_R4.nc'
file_path_out = '/data/project1/minnaho/psource/freshwater_nutrients/roms_psource_nutr_corr.nc'
file_nc = Dataset(file_path,'r')

temp_salt_ext = '/data/project1/minnaho/psource/freshwater_nutrients/temp_salt_extractions/'
htp_fi = 'l2_scb_avg.Y1999M06_Y2000M08_htp.nc'
jwp_fi = 'l2_scb_avg.Y1999M06_Y2000M08_jwp.nc'
ocs_fi = 'l2_scb_avg.Y1999M06_Y2000M08_ocs.nc'
plw_fi = 'l2_scb_avg.Y1999M06_Y2000M08_plw.nc'

# end psources before rivers to exclude rivers
end_ind = 96

# factor to divide flow by and multiply constituents by
fact = 100

# psource time is actually days since 1994-01-01
psource_time_nc   = np.array(file_nc.variables['psrc_time'][:])
psrc_dt = num2date(psource_time_nc,'days since 1994-01-01',only_use_cftime_datetimes=False)

# psrc time starts at 1997-01-30
# psrc_dt[30] is 1999-06-02 June
# psrc_dt[45] is 2000-09-01 Sept
p_st = 29
p_en = 29+15

# divide flow by factor
Qbar_nc   = np.array(file_nc.variables['Qbar'][:end_ind,:])/fact

Qshape_nc = np.array(file_nc.variables['Qshape'][:,:end_ind])
                                                   
Isrc_nc   = np.array(file_nc.variables['Isrc'][:end_ind])
Jsrc_nc   = np.array(file_nc.variables['Jsrc'][:end_ind])
Dsrc_nc   = np.array(file_nc.variables['Dsrc'][:end_ind])
Lsrc_nc   = np.array(file_nc.variables['Lsrc'][:,:end_ind])

################################
# use temp and salt extractions
################################
htp_temp = np.squeeze(np.array(Dataset(temp_salt_ext+htp_fi,'r').variables['temp']))
jwp_temp = np.squeeze(np.array(Dataset(temp_salt_ext+jwp_fi,'r').variables['temp']))
ocs_temp = np.squeeze(np.array(Dataset(temp_salt_ext+ocs_fi,'r').variables['temp']))
plw_temp = np.squeeze(np.array(Dataset(temp_salt_ext+plw_fi,'r').variables['temp']))

htp_salt = np.squeeze(np.array(Dataset(temp_salt_ext+htp_fi,'r').variables['salt']))
jwp_salt = np.squeeze(np.array(Dataset(temp_salt_ext+jwp_fi,'r').variables['salt']))
ocs_salt = np.squeeze(np.array(Dataset(temp_salt_ext+ocs_fi,'r').variables['salt']))
plw_salt = np.squeeze(np.array(Dataset(temp_salt_ext+plw_fi,'r').variables['salt']))

temp_nc = np.array(file_nc.variables['temp'][:end_ind,:])
salt_nc = np.array(file_nc.variables['salt'][:end_ind,:])

temp_nc[:28,p_st:p_en]  = htp_temp
salt_nc[:28,p_st:p_en]  = htp_salt
          
temp_nc[28:56,p_st:p_en]  = jwp_temp
salt_nc[28:56,p_st:p_en]  = jwp_salt
          
temp_nc[56:70,p_st:p_en]  = ocs_temp
salt_nc[56:70,p_st:p_en]  = ocs_salt
          
temp_nc[70:96,p_st:p_en]  = plw_temp
salt_nc[70:96,p_st:p_en]  = plw_salt

# multiply constituents by factor
PO4_nc = np.array(file_nc.variables['PO4'][:end_ind,:])*fact
NO3_nc = np.array(file_nc.variables['NO3'][:end_ind,:])*fact
NH4_nc = np.array(file_nc.variables['NH4'][:end_ind,:])*fact
Fe_nc  = np.array(file_nc.variables['Fe'][:end_ind,:])*fact
O2_nc  = np.array(file_nc.variables['O2'][:end_ind,:])*fact
DIC_nc = np.array(file_nc.variables['DIC'][:end_ind,:])*fact
Alk_nc = np.array(file_nc.variables['Alk'][:end_ind,:])*fact
DOC_nc = np.array(file_nc.variables['DOC'][:end_ind,:])*fact
DON_nc = np.array(file_nc.variables['DON'][:end_ind,:])*fact
DOP_nc = np.array(file_nc.variables['DOP'][:end_ind,:])*fact
NO2_nc = np.array(file_nc.variables['NO2'][:end_ind,:])*fact


# make new netcdf

file_out = Dataset(file_path_out,'w')
Nsrc_dim = file_out.createDimension('Nsrc',Qbar_nc.shape[0])
Npas_dim = file_out.createDimension('Npas',Lsrc_nc.shape[0])
s_rho_dim = file_out.createDimension('s_rho',Qshape_nc.shape[0])
psrc_time_dim = file_out.createDimension('psrc_time',psource_time_nc.shape[0])

psrc_time_var = file_out.createVariable('psrc_time','float64',('psrc_time'))
psrc_time_var.units = 's'
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
