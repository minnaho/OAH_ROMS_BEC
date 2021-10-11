import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

reg_nc = Dataset('/data/project3/minnaho/roms_psource_102020_R4.nc','r')
nut_nc = Dataset('/data/project1/minnaho/psource/freshwater_nutrients/roms_psource_nutr_corr.nc','r')

# end psources before rivers to exclude rivers
end_ind = 96

# time of runs
st = 29
en = 29+15

Qbar_reg = np.array(reg_nc.variables['Qbar'][:end_ind,:])

PO4_nc_reg = np.array(reg_nc.variables['PO4'][:end_ind,:])
NO3_nc_reg = np.array(reg_nc.variables['NO3'][:end_ind,:])
NH4_nc_reg = np.array(reg_nc.variables['NH4'][:end_ind,:])
Fe_nc_reg = np.array(reg_nc.variables['Fe'][:end_ind,:])
O2_nc_reg = np.array(reg_nc.variables['O2'][:end_ind,:])
DIC_nc_reg = np.array(reg_nc.variables['DIC'][:end_ind,:])
Alk_nc_reg = np.array(reg_nc.variables['Alk'][:end_ind,:])
DOC_nc_reg = np.array(reg_nc.variables['DOC'][:end_ind,:])
DON_nc_reg = np.array(reg_nc.variables['DON'][:end_ind,:])
DOP_nc_reg = np.array(reg_nc.variables['DOP'][:end_ind,:])
NO2_nc_reg = np.array(reg_nc.variables['NO2'][:end_ind,:])

nh4_ld_reg = Qbar_reg*NH4_nc_reg
no3_ld_reg = Qbar_reg*NO3_nc_reg



Qbar_nut = np.array(nut_nc.variables['Qbar'][:,:])

PO4_nc_nut = np.array(nut_nc.variables['PO4'][:,:])
NO3_nc_nut = np.array(nut_nc.variables['NO3'][:,:])
NH4_nc_nut = np.array(nut_nc.variables['NH4'][:,:])
Fe_nc_nut = np.array(nut_nc.variables['Fe'][:,:])
O2_nc_nut = np.array(nut_nc.variables['O2'][:,:])
DIC_nc_nut = np.array(nut_nc.variables['DIC'][:,:])
Alk_nc_nut = np.array(nut_nc.variables['Alk'][:,:])
DOC_nc_nut = np.array(nut_nc.variables['DOC'][:,:])
DON_nc_nut = np.array(nut_nc.variables['DON'][:,:])
DOP_nc_nut = np.array(nut_nc.variables['DOP'][:,:])
NO2_nc_nut = np.array(nut_nc.variables['NO2'][:,:])

nh4_ld_nut = Qbar_nut*NH4_nc_nut
no3_ld_nut = Qbar_nut*NO3_nc_nut

plt.ion()
#plt.plot(nh4_ld_reg[90],label='Regular')
#plt.plot(nh4_ld_nut[90],linestyle='--',label='Nutr only')

plt.figure()
plt.plot(np.nansum(nh4_ld_reg,axis=0),label='Regular')
plt.plot(np.nansum(nh4_ld_nut,axis=0),linestyle='--',label='Nutr only')
plt.xlabel('time')
plt.ylabel('NH4 mmol/s')
plt.legend(loc='best')
plt.savefig('nh4_load.png',bbox_inches='tight')

plt.figure()
plt.plot(np.nansum(no3_ld_reg,axis=0),label='Regular')
plt.plot(np.nansum(no3_ld_nut,axis=0),linestyle='--',label='Nutr only')
plt.xlabel('time')
plt.ylabel('NO3 mmol/s')
plt.legend(loc='best')
plt.savefig('no3_load.png',bbox_inches='tight')
