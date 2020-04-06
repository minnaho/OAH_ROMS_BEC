import numpy as np
from netCDF4 import Dataset

test = open('vgpm.2002182.all.xyz','r')
lon_l = []
lat_l = []
val_l = []
for l_i in test:
    lon_raw,lat_raw,val_raw = l_i.split()
    lon_l.append(float(lon_raw))
    lat_l.append(float(lat_raw))
    val_l.append(float(val_raw))
test.close()

lon_arr = np.array(lon_l)
lat_arr = np.array(lat_l)
val_arr = np.array(val_l)

lat_re = lat_arr.reshape(2160,4320)
lon_re = lon_arr.reshape(2160,4320) 
val_re = val_arr.reshape(2160,4320) 

nc_file = Dataset('lat_lon_vgpm.nc','w')
dim0 = nc_file.createDimension('dim0',lat_re.shape[0])
dim1 = nc_file.createDimension('dim1',lat_re.shape[1])

lat_nc = nc_file.createVariable('Lat',np.float64,('dim0','dim1'))
lon_nc = nc_file.createVariable('Lon',np.float64,('dim0','dim1'))
val_nc = nc_file.createVariable('val',np.float64,('dim0','dim1'))

lat_nc[:,:] = lat_re
lon_nc[:,:] = lon_re
val_nc[:,:] = val_re

nc_file.close()
