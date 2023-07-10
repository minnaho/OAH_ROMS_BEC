import numpy as np
from netCDF4 import Dataset,num2date

orig = Dataset('./run_2013_2017/roms_psource_1997_2017.nc','r')
fix =  Dataset('./run_fixjwpcp/roms_psource_102020_full.767.nc','r')

origflux_riv = np.squeeze(orig['Qbar'])[115:]
fixflux_riv = np.squeeze(fix['Qbar'])[115:]
fluxsum = np.nansum(origflux_riv-fixflux_riv)

orignh4_riv = np.squeeze(orig['NH4'])[115:]
fixnh4_riv = np.squeeze(fix['NH4'])[115:]
nh4sum = np.nansum(orignh4_riv-fixnh4_riv)

origno3_riv = np.squeeze(orig['NO3'])[115:]
fixno3_riv = np.squeeze(fix['NO3'])[115:]
no3sum = np.nansum(origno3_riv-fixno3_riv)

origo2_riv = np.squeeze(orig['O2'])[115:]
fixo2_riv = np.squeeze(fix['O2'])[115:]
o2sum = np.nansum(origo2_riv-fixo2_riv)
