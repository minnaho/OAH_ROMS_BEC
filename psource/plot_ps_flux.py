# plot NH4 and total DIN flux timeseries
# of point sources
import numpy as np
from netCDF4 import Dataset,num2date

# indices 0-114 are point sources
end_ind = 115

datanc = Dataset('./run_fixjwpcp/roms_psource_102020_full.767.nc','r')

datatim = np.array(datanc['psrc_time'])
dt = num2date(datatim,'days since 1994-1-1',only_use_cftime_datetimes=False)

# mmol/m3
datanh4 = np.array(datanc['NH4'])[:end_ind,:]
datadin = np.array(datanc['NH4'])[:end_ind,:] + np.array(datanc['NO3'])[:end_ind,:] + np.array(datanc['NO2'])[:end_ind,:] 

# volume flux m3/s
dataflo = np.array(datanc['Qbar'])[:end_ind,:]

# total flux mmol/s
nh4flux = dataflo*datanh4
dinflux = dataflo*datadin

# convert to kg/day
s_to_d = 86400
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

nh4kgd = np.nansum(nh4flux*s_to_d*mmol_to_mol*g_to_kg*g_N,axis=0)
dinkgd = np.nansum(dinflux*s_to_d*mmol_to_mol*g_to_kg*g_N,axis=0)

fileout = Dataset('ps_flux.nc','w')
psrcdim = fileout.createDimension('psrc_time',datatim.shape[0])
psrcvar = fileout.createVariable('psrc_time','float64',('psrc_time'))
psrcvar[:] = datatim
psrcvar.units = 'days since 1994-1-1'

nh4var = fileout.createVariable('NH4flux','float64',('psrc_time'))
nh4var[:] = nh4kgd
nh4var.unit = 'kg/day'

dinvar = fileout.createVariable('DINflux','float64',('psrc_time'))
dinvar[:] = dinkgd
dinvar.unit = 'kg/day'

fileout.close()

