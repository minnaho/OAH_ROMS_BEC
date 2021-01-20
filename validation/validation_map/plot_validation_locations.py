#####################################################
# plot where the samplings/moorings took place 
# for validation
##################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
plt.ion()

# get validation coordinates
v_data = pd.read_csv('validation_metadata.csv',header=None,skiprows=1)

lat_v = v_data[1]
lon_v = v_data[2]

# load L2 grid
grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc'
nc_grid = Dataset(grid_path,'r')
lon_nc  = nc_grid.variables['lon_rho'][:,:]
lat_nc  = nc_grid.variables['lat_rho'][:,:]

lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)

# indices where nan (changes source of data)
nan_ind = np.where(np.isnan(lat_v))[0]

data_sources = ['LACSD moorings','OCSD ADCP','San Diego ADCP','Central Bight Master Sampling (bgc)','CalCOFI (bgc)','POTW stations (profiles)']

# basemap boundaries
'''
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)
'''
# zoom
'''
lat_min = 32.25
lat_max = 34.4
lon_min = -119.5
lon_max = -117
'''
# SMB SPB
'''
lat_min = 33.25
lat_max = 34.1
lon_min = -119
lon_max = -117.6
'''

'''
# OC SD
lat_min = 32.35
lat_max = 32.8
lon_min = -117.5
lon_max = -117.0
'''

#OC
lat_min = 33.55
lat_max = 33.6
lon_min = -118.05
lon_max = -117.97


# make basemap
m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,epsg=4269)
# map lat/lon to coordinates
x_coords,y_coords = m(lon_v,lat_v)


####################
# plot
###############
fig_h = 18
fig_w = 15

fig = plt.figure(figsize=[fig_w,fig_h])

# latitudes to draw
parallels = np.arange(0,90,.05)
# longitudes to draw
meridians = np.arange(180,360,.05)

axis_tick_size = 16

m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
#m.arcgisimage(service='ESRI_Imagery_World_2D',xpixels=2000,verblose=True)

m_size = 100

m_size_small = 40

lacsd_c = 'blue'
ocsd_c = 'orange'
sdsd_c = 'green'
central_c = 'red'
calcofi_c = 'purple'
potw_c = 'gray'
 
lacsd = m.scatter(x_coords[1:nan_ind[1]],y_coords[1:nan_ind[1]],s=m_size,marker='o',color=lacsd_c,label=data_sources[0])

central = m.scatter(x_coords[nan_ind[6]+1:nan_ind[7]],y_coords[nan_ind[6]+1:nan_ind[7]],s=m_size_small,marker='o',color=central_c,label=data_sources[3])

calcofi = m.scatter(x_coords[nan_ind[8]+1:nan_ind[9]],y_coords[nan_ind[8]+1:nan_ind[9]],s=m_size_small,marker='o',color=calcofi_c,label=data_sources[4])

potw = m.scatter(x_coords[nan_ind[-1]+1:],y_coords[nan_ind[-1]+1:],s=m_size,marker='s',color=potw_c,label=data_sources[5])

ocsd = m.scatter(x_coords[nan_ind[2]+1:nan_ind[3]],y_coords[nan_ind[2]+1:nan_ind[3]],s=m_size,marker='^',color=ocsd_c,label=data_sources[1])

sdsd = m.scatter(x_coords[nan_ind[4]+1:nan_ind[5]],y_coords[nan_ind[4]+1:nan_ind[5]],s=m_size,marker='s',color=sdsd_c,label=data_sources[2])

plt.savefig('OC_profiles.png',bbox_inches='tight')

#plt.legend(loc='upper right',fontsize=18)
#plt.savefig('validation_basemap.png',bbox_inches='tight')
#plt.savefig('validation_basemap_zoom.png',bbox_inches='tight')
#plt.savefig('validation_basemap_SD.png',bbox_inches='tight')

