import scipy.io
import numpy as np
from netCDF4 import Dataset

ncfile = scipy.io.loadmat('mask_gridL2.mat')

maskarr = np.ones((len(ncfile['mask_gridL2'][0][0]),ncfile['mask_gridL2'][0][0][0].shape[0],ncfile['mask_gridL2'][0][0][0].shape[1]))*np.nan

for m_i in range(len(ncfile['mask_gridL2'][0][0])):
    maskarr[m_i,:,:] = ncfile['mask_gridL2'][0][0][m_i]
    
outnc = Dataset('mask_gridL2.nc','w')
eta_coord = outnc.createDimension('eta_rho',maskarr.shape[1])
xi_coord = outnc.createDimension('xi_rho',maskarr.shape[2])

mask0 = outnc.createVariable('mask0',np.float32,('eta_rho','xi_rho'))
mask1 = outnc.createVariable('mask1',np.float32,('eta_rho','xi_rho'))
mask2 = outnc.createVariable('mask2',np.float32,('eta_rho','xi_rho'))
mask3 = outnc.createVariable('mask3',np.float32,('eta_rho','xi_rho'))
mask4 = outnc.createVariable('mask4',np.float32,('eta_rho','xi_rho'))
mask5 = outnc.createVariable('mask5',np.float32,('eta_rho','xi_rho'))
mask6 = outnc.createVariable('mask6',np.float32,('eta_rho','xi_rho'))
mask7 = outnc.createVariable('mask7',np.float32,('eta_rho','xi_rho'))
mask8 = outnc.createVariable('mask8',np.float32,('eta_rho','xi_rho'))
mask9 = outnc.createVariable('mask9',np.float32,('eta_rho','xi_rho'))

mask0[:,:] = maskarr[0]
mask1[:,:] = maskarr[1]
mask2[:,:] = maskarr[2]
mask3[:,:] = maskarr[3]
mask4[:,:] = maskarr[4]
mask5[:,:] = maskarr[5]
mask6[:,:] = maskarr[6]
mask7[:,:] = maskarr[7]
mask8[:,:] = maskarr[8]
mask9[:,:] = maskarr[9]

outnc.close()
