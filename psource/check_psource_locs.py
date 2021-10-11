import os
import sys
sys.path.append(os.path.abspath('/data/project3/minnaho/global/'))
import l2grid
import cartopy.crs as ccrs
import cartopy.feature as cpf
import matplotlib.pyplot as plt
import numpy as np

psrc = './run_2013_2017/roms_psource_1997_2017.nc'

psrc_nc = l2grid.Dataset(psrc,'r')

i_nc = np.array(psrc_nc.variables['Isrc']).astype(int)
j_nc = np.array(psrc_nc.variables['Jsrc']).astype(int)

lat_nc = l2grid.lat_nc 
lon_nc = l2grid.lon_nc 

lat_min = 32.4
lat_max = 34.6
lon_min = -120.5
lon_max = -117

latplt = np.ones(i_nc.shape[0])*np.nan
lonplt = np.ones(i_nc.shape[0])*np.nan

for l_i in range(len(latplt)):
    latplt[l_i] = lat_nc[j_nc[l_i],i_nc[l_i]]
    lonplt[l_i] = lon_nc[j_nc[l_i],i_nc[l_i]]

plt.ion()

figw = 12
figh = 12

fig,ax = plt.subplots(1,1,figsize=[figw,figh],subplot_kw=dict(projection=ccrs.PlateCarree()))
ax.scatter(lonplt[:96],latplt[:96],marker='o',facecolors='none',edgecolor='gold',lw=3)
ax.scatter(lonplt[96:115],latplt[96:115],marker='s',facecolors='none',edgecolor='k',lw=2)
ax.scatter(lonplt[115:],latplt[115:],marker='^',facecolors='lightgreen',edgecolor='green',lw=1)
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')


