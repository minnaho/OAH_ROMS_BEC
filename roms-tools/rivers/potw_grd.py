# add POTW to ROMS grid file
# adding pipe_flux variable to grid file
import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import numpy as np
from scipy.io import loadmat
from netCDF4 import num2date,Dataset
#import pyfuncs as pf

grd = '/data/project9/minnaho/swel/mc60_newlarge_grd.nc'


data0 = loadmat('ROMS_CC_new.mat')

data = data0['ROMS']

print(data.dtype.names)

dt = num2date(data['time'][0,0].flatten(),'days since 1994-01-01')

target_year = 2019
target_month = 4

# Find matching index for time
idx = np.where([(d.year == target_year and d.month == target_month) for d in dt])[0][0]

# get correct POTWs for region manually by looking at data
# Carmel Area     data['name'][0,0][7]
# Monterey Area   data['name'][0,0][6]
# Watsonville     data['name'][0,0][5]
# Santa Cruz      data['name'][0,0][4]

# POTW indices
pind = [4,5,6,7]
# target time range +-2
tind = range(idx-2,idx+2)

# 1D attributes
attr = ['lon', 'lat', 'depth', 'name']
attrnc = []

# order of tracers in ROMS
ntracers = ['temp','salt','PO4','NO3','SIO3','NH4','FE','O2','DIC','ALK','DOC','Don','Dofe','Dop','Dopr','Donr','ZOOC','SPCHL','SPC','SPFE','SPCACO3','DIATCHL','DIATC','DIATFE','DIATSI','Diazchl','Diazc','Diazfe','NO2','N2','N2O']

# Prepare a lowercase version of ntracers for comparison
ntracers_lower = [item.lower() for item in ntracers]


# create pipe_tracer variable
pipt = np.ones((len(tind),len(ntracers),len(pind)))*np.nan

# loop through pipes to get attributes
for p_i in range(len(pind)):
    # manually find the attributes range
    # lon, lat, depth, name
    for v_i in range(3,5):
        attrnc.append(data[list(data.dtype.names)[v_i]][0,0][pind[p_i]][0])

lats = np.array(attrnc[1::2])
lons = np.array(attrnc[::2])+360

grdnc = Dataset(grd,'a')

# had to add this because tethys down...
def calc_ij(nc_grd,lat_sites,lon_sites):

    lon_nc = nc_grd.variables['lon_rho'][:,:]
    lat_nc = nc_grd.variables['lat_rho'][:,:]

    nsites = len(lat_sites)
    isites = np.ones(nsites)*np.nan
    jsites = np.ones(nsites)*np.nan

    for s in range(nsites):
        ##################################
        # FIND SITE IN GRIDPOINTS
        ####################################
        min_1D = np.abs( (lat_nc - lat_sites[s])**2 + (lon_nc - lon_sites[s])**2)
        y_site, x_site = np.unravel_index(min_1D.argmin(), min_1D.shape)
        isites[s] = x_site
        jsites[s] = y_site

    return isites, jsites


ipip,jpip = calc_ij(grdnc,lats,lons)

if 'pipe_flux' not in grdnc.variables:
    pipe_flux = grdnc.createVariable('pipe_flux','f4',('eta_rho','xi_rho'))
else:
    pipe_flux = grdnc.variables['pipe_flux']

pipe_flux[:,:] = 0
pipe_flux[jpip[0].astype(int),ipip[0].astype(int)] = 1
pipe_flux[jpip[1].astype(int),ipip[1].astype(int)] = 2
pipe_flux[jpip[2].astype(int),ipip[2].astype(int)] = 3
pipe_flux[jpip[3].astype(int),ipip[3].astype(int)] = 4

pipe_flux.longname = "Pipe volume flux partition"

grdnc.close()
