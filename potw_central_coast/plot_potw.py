import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cpf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

ncdata = Dataset('minor_potw_central_coast.nc','r')
latnc = np.squeeze(ncdata['latitude'])
lonnc = np.squeeze(ncdata['longitude'])
lonnc[5] = -121.325

lat_max = np.nanmax(latnc)
lat_min = np.nanmin(latnc)
lon_max = np.nanmax(lonnc)
lon_min = np.nanmin(lonnc)

axfont = 14

plt.ion()

extent = [lon_min-0.1,lon_max+0.1,lat_min-0.1,lat_max+0.1]
coast_10m = cpf.NaturalEarthFeature('physical','coastline','10m')

fig,ax = plt.subplots(1,1,subplot_kw=dict(projection=ccrs.PlateCarree()))
ax.set_extent(extent)
ax.add_feature(coast_10m,facecolor='None',edgecolor='k')
ax.add_feature(cpf.BORDERS,facecolor='None',edgecolor='k')
for l_i in range(len(lonnc)):
    ax.scatter(lonnc[l_i],latnc[l_i],marker='o',facecolors='none',edgecolors='blue',s=100)

ax.gridlines(draw_labels={'bottom':'x','left':'y'})


