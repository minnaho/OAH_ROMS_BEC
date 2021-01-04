import numpy as np
from netCDF4 import Dataset,num2date

ncfile = Dataset('central_bight_master_database_1998_2017_1D.nc','r')
time_nc = np.array(ncfile.variables['date'])
lat_nc = np.array(ncfile.variables['latitude'])
lon_nc = np.array(ncfile.variables['longitude'])
nh4_nc = np.array(ncfile.variables['ammonia-N'])

lats = lat_nc[np.where((lat_nc<32.8)&(lat_nc>32.35))[0]]
lons = lon_nc[np.where((lon_nc<-117)&(lon_nc>-117.5))[0]]

# check if indices are the same (they are)
check = np.where((np.where((lat_nc<32.8)&(lat_nc>32.35))[0] == np.where((lon_nc<-117)&(lon_nc>-117.5))[0])==False)

inds = np.where((lat_nc<32.8)&(lat_nc>32.35))[0]

times = num2date(time_nc,'days since 1998-07-07')

