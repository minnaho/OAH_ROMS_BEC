# make masks for each region for validation in SCB
# finds where the two 2d arrays intersects
import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import numpy as np
import l2grid
from netCDF4 import Dataset

# roms grid data
latnc = l2grid.lat_nc
lonnc = l2grid.lon_nc
masknc = l2grid.mask_nc
masknc[np.isnan(masknc)] = 0

# ventura
ventura_lat = np.array(np.where((latnc>33.9) & (latnc<34.3))).T
ventura_lon = np.array(np.where((lonnc>-118.9) & (lonnc<-118.45))).T

latset = set([tuple(x) for x in ventura_lat])
lonset = set([tuple(x) for x in ventura_lon])
ventura_loc = np.array([x for x in latset & lonset])

ventura_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
ventura_mask[ventura_loc.T[0],ventura_loc.T[1]] = 1
ventura_mask = ventura_mask*masknc

# santa monica
sm_lat = np.array(np.where((latnc>33.78) & (latnc<34.05))).T
sm_lon = np.array(np.where((lonnc>-118.85) & (lonnc<-118.4))).T

latset = set([tuple(x) for x in sm_lat])
lonset = set([tuple(x) for x in sm_lon])
sm_loc = np.array([x for x in latset & lonset])

sm_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
sm_mask[sm_loc.T[0],sm_loc.T[1]] = 1
sm_mask = sm_mask*masknc

# san pedro
sp_lat = np.array(np.where((latnc>33.6) & (latnc<33.78))).T
sp_lon = np.array(np.where((lonnc>-118.5) & (lonnc<-118.25))).T

latset = set([tuple(x) for x in sp_lat])
lonset = set([tuple(x) for x in sp_lon])
sp_loc = np.array([x for x in latset & lonset])

sp_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
sp_mask[sp_loc.T[0],sp_loc.T[1]] = 1
sp_mask = sp_mask*masknc


# orange county
oc_lat = np.array(np.where((latnc>33.45) & (latnc<33.69))).T
oc_lon = np.array(np.where((lonnc>-118.12) & (lonnc<-117.7))).T

latset = set([tuple(x) for x in oc_lat])
lonset = set([tuple(x) for x in oc_lon])
oc_loc = np.array([x for x in latset & lonset])

oc_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
oc_mask[oc_loc.T[0],oc_loc.T[1]] = 1
oc_mask = oc_mask*masknc

# san diego
sd_lat = np.array(np.where((latnc>32.4) & (latnc<32.8))).T
sd_lon = np.array(np.where((lonnc>-117.5) & (lonnc<-117.1))).T

latset = set([tuple(x) for x in sd_lat])
lonset = set([tuple(x) for x in sd_lon])
sd_loc = np.array([x for x in latset & lonset])

sd_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
sd_mask[sd_loc.T[0],sd_loc.T[1]] = 1
sd_mask = sd_mask*masknc

# carlsbad
cb_lat = np.array(np.where((latnc>33.1) & (latnc<33.23))).T
cb_lon = np.array(np.where((lonnc>-117.47) & (lonnc<-117.33))).T

latset = set([tuple(x) for x in cb_lat])
lonset = set([tuple(x) for x in cb_lon])
cb_loc = np.array([x for x in latset & lonset])

cb_mask = np.zeros((masknc.shape[0],masknc.shape[1]))
cb_mask[cb_loc.T[0],cb_loc.T[1]] = 1
cb_mask = cb_mask*masknc

mask_valid = Dataset('mask_valid.nc','w')
mask_valid.description = 'L2SCB masks for validation of each region'

# create dimensions
eta_coord = mask_valid.createDimension('eta_rho',masknc.shape[0])
xi_coord = mask_valid.createDimension('xi_rho',masknc.shape[1])

# create variables
mask_cb = mask_valid.createVariable('mask_cb',np.float32,('eta_rho','xi_rho'))
mask_sd = mask_valid.createVariable('mask_sd',np.float32,('eta_rho','xi_rho'))
mask_oc = mask_valid.createVariable('mask_oc',np.float32,('eta_rho','xi_rho'))
mask_sp = mask_valid.createVariable('mask_sp',np.float32,('eta_rho','xi_rho'))
mask_sm = mask_valid.createVariable('mask_sm',np.float32,('eta_rho','xi_rho'))
mask_v = mask_valid.createVariable('mask_v',np.float32,('eta_rho','xi_rho'))

mask_sd.longname = 'San Diego'
mask_oc.longname = 'Orange County'
mask_sp.longname = 'San Pedro'
mask_sm.longname = 'Santa Monica'
mask_v.longname = 'Ventura'
mask_cb.longname = 'Carlsbad region'

mask_cb[:,:] = cb_mask
mask_sd[:,:] = sd_mask
mask_oc[:,:] = oc_mask
mask_sp[:,:] = sp_mask
mask_sm[:,:]  = sm_mask
mask_v[:,:] = ventura_mask

mask_valid.close()


