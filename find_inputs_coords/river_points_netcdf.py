import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import l2grid as l2grid
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

ncfile = '/data/project1/minnaho/psource/river/roms_psource_inlandpotw.nc'

datanc = Dataset(ncfile,'r')

isrc = np.array(datanc.variables['Isrc']).astype(int)
jsrc = np.array(datanc.variables['Jsrc']).astype(int)
qbar = np.array(datanc.variables['Qbar'])

mask_nc = l2grid.mask_nc

rst = 115 # river start

plt.ion()
plt.imshow(mask_nc,origin='lower')

for ind in range(isrc.shape[0]-rst):
    plt.scatter(isrc[rst+ind],jsrc[rst+ind],c='blue')

## LA river
#plt.scatter(isrc[32+rst],jsrc[32+rst],c='blue') 
#plt.scatter(isrc[190:193],jsrc[190:193],c='blue') 
## 190, 191, 192
#
## San Gabriel River
#plt.scatter(isrc[51+rst],jsrc[51+rst],c='blue')
#plt.scatter(isrc[193:197],jsrc[193:197],c='blue')
## 193, 194, 195, 196
#
## Calleguas
#plt.scatter(isrc[12+rst],jsrc[12+rst],c='orange')
#
## Malibu Creek
#plt.scatter(isrc[34+rst],jsrc[34+rst],marker='^',c='orange')
#
##San Diego Creek
#plt.scatter(isrc[48+rst],jsrc[48+rst],marker='^',c='orange')
#
#
##San Diego River
#plt.scatter(isrc[49+rst],jsrc[49+rst],marker='^',c='blue')
#
## Santa clara
#plt.scatter(isrc[61+rst],jsrc[61+rst],marker='s',c='blue')
#
## Ventura River
#plt.scatter(isrc[72+rst],jsrc[72+rst],marker='s',c='orange')

