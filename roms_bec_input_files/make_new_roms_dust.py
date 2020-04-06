import numpy as np
from netCDF4 import Dataset
import datetime

NO3_var_name = 'nitrate'
NH4_var_name = 'ammonium'
alk_var_name = 'alkalinity'

############################
# open original roms_dust.nc
############################
dust_or = Dataset('roms_dust.nc','r')

# get variables
dust_t = dust_or.variables['dust_time'][:]
iron_t = dust_or.variables['iron_time'][:]
dust_v = dust_or.variables['dust'][:,:,:]
iron_v = dust_or.variables['iron'][:,:,:]

############################
# open atmospheric deposition data
############################
atmos_path = '/data/project1/minnaho/atmos_deposition_data/'
atmos = Dataset(atmos_path+'L2_SCB_atmos_deposition.nc','r')

# get variables
NO3_a = atmos.variables['NO3'][:,:,:]
NH4_a = atmos.variables['NH4'][:,:,:]
alk_a = atmos.variables['alk'][:,:,:]

# convert variables from mmol m-2 s-1 to nmol cm-2 s-1
mmol_to_nmol = 1000000
m2_to_cm2 = 1./10000
NO3_c = NO3_a[:,:,:]*mmol_to_nmol*m2_to_cm2
NH4_c = NH4_a[:,:,:]*mmol_to_nmol*m2_to_cm2
alk_c = alk_a[:,:,:]*mmol_to_nmol*m2_to_cm2

eta_shape = NO3_a.shape[1]
xi_shape = NO3_a.shape[2]


############################
# make new netcdf
############################
dust_new = Dataset('roms_dust_new.nc','w')

# descriptors of file
dust_new.title = 'dust file produced from ROMS-USW4 and EPA CMAQ modeling system'

now = datetime.datetime.now()
dust_new.date = now.strftime('%d-%b-%Y')

dust_new.grd_file = '/data/project4/kesf/DUST/L2_SCB/roms_grd.nc'
dust_new.type = 'roms dust file'
dust_new.history = 'none'

# dimensions
time = dust_new.createDimension('dust_time',None)
eta_rho = dust_new.createDimension('eta_rho',eta_shape)
xi_rho = dust_new.createDimension('xi_rho',xi_shape)

dust_time = dust_new.createVariable('dust_time',np.float32,('dust_time',))
iron_time = dust_new.createVariable('iron_time',np.float32,('dust_time',))
NO3_time = dust_new.createVariable(NO3_var_name+'_time',np.float32,('dust_time',))
NH4_time = dust_new.createVariable(NH4_var_name+'_time',np.float32,('dust_time',))
alk_time = dust_new.createVariable(alk_var_name+'_time',np.float32,('dust_time',))

dust_n = dust_new.createVariable('dust',np.float32,('dust_time','eta_rho','xi_rho'))
iron_n = dust_new.createVariable('iron',np.float32,('dust_time','eta_rho','xi_rho'))
NO3_n = dust_new.createVariable(NO3_var_name,np.float32,('dust_time','eta_rho','xi_rho'))
NH4_n = dust_new.createVariable(NH4_var_name,np.float32,('dust_time','eta_rho','xi_rho'))
alk_n = dust_new.createVariable(alk_var_name,np.float32,('dust_time','eta_rho','xi_rho'))

# units and long names and other variable descriptors
dust_time.long_name = 'dust deposition time'
iron_time.long_name = 'iron deposition time'
NO3_time.long_name = NO3_var_name+' deposition time'
NH4_time.long_name = NH4_var_name+' deposition time'
alk_time.long_name = alk_var_name+' deposition time'

dust_n.long_name = 'dust deposition'
iron_n.long_name = 'iron deposition'
NO3_n.long_name = NO3_var_name+' deposition'
NH4_n.long_name = NH4_var_name+' deposition'
alk_tnlong_name = alk_var_name+' deposition'

dust_time.units = 'days'
iron_time.units = 'days'
NO3_time.units = 'days'
NH4_time.units = 'days'
alk_time.units = 'days'

dust_time.cycle_length = 365.25
iron_time.cycle_length = 365.25
NO3_time.cycle_length = 365.25
NH4_time.cycle_length = 365.25
alk_time.cycle_length = 365.25

dust_n.units = 'nmol/cm2/s'
iron_n.units = 'nmol/cm2/s'
NO3_n.units = 'nmol/cm2/s'
NH4_n.units = 'nmol/cm2/s'
alk_n.units = 'nmol/cm2/s'

# assign variable values
dust_time[:] = dust_t
iron_time[:] = dust_t
NO3_time[:] = dust_t
NH4_time[:] = dust_t
alk_time[:] = dust_t

dust_n[:,:,:] = dust_v
iron_n[:,:,:] = iron_v
NO3_n[:,:,:] = NO3_c
NH4_n[:,:,:] = NH4_c
alk_n[:,:,:] = alk_c

dust_new.close()
print('data written to roms_dust_new.nc')
