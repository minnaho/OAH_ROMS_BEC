#############################################
# plot_inputs_map.py
# plot rivers and potw inputs on map
#####################################################
import numpy as np
import pickle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
import matplotlib.patheffects as path_effects
from netCDF4 import Dataset, date2num, num2date
from PIL import Image
#from PIL import Image
plt.ion()

###################
# FOLDER PATHS
####################
grid_path = '/data/project3/kesf/ROMS/USSW1/grid/usw1_grd.nc'
save_figs_path = './maps/'


###################
# INPUT FILES
##################
# axis 0 is lats, axis 1 is lons
major_potw = np.load('major_potw_lat_lon.npy')
minor_potw = np.load('minor_potw_lat_lon.npy')
river = np.load('river_lat_lon.npy')

# names of locations
minor_potw_names_long = pickle.load(open('minor_potw_names.pkl','rb'))
# make names without number and hyphen ('OO1-South Bay' to 'South Bay')
# (names are sometimes 'OO12-...' so hyphen not always in the same place...)
minor_potw_names = []
# remove 'WWTP' or 'WWTF' at end of name
remove_WWT = [1,5,8,9,10,11,12,13]
# remove 'Ocean Outfall' at end of name
remove_Oc = [2,3,4,7]
for j,m in enumerate(minor_potw_names_long):
    i = m.index('-')+1 
    if j in remove_WWT:
        end_ind = m.index('W')-1
        name = m[i:end_ind] 
        minor_potw_names.append(name) 
    if j in remove_Oc:
        end_ind = m.index('Ocean ')-1
        name = m[i:end_ind]
        minor_potw_names.append(name) 
    if j==6: # San Juan Creek Outfall (just get rid of 'Outfall')
        end_ind = m.index('Ou')-1
        name = m[i:end_ind]
        minor_potw_names.append(name) 
    if j not in remove_WWT and j not in remove_Oc and j!=6:
        name = m[i:]
        minor_potw_names.append(name) 
major_potw_names = ['HTP','JWPCP','OCSD','PLWTP']

'''
# concatenate so all lats are on axis 0 and lon coords axis 1
coords = np.concatenate((major_potw,minor_potw,river),axis=1)
lats_input = coords[0]
lons_input = coords[1]
'''
# separate by input type for color coding on map
lats_major_potw = major_potw[0]
lons_major_potw = major_potw[1]

lats_minor_potw = minor_potw[0]
lons_minor_potw = minor_potw[1]

lats_river = river[0]
lons_river = river[1]

################################
# CALL GRID
################################
# load grid
grid_nc = Dataset(grid_path,'r')
mask_nc = grid_nc.variables['mask_rho']
mask = np.copy(mask_nc)
#mask[mask==0.0] = np.nan

lat_nc = grid_nc.variables['lat_rho']
lon_nc = grid_nc.variables['lon_rho']
lat_plt = np.copy(lat_nc)
lon_plt = np.copy(lon_nc)

Ly = mask.shape[0] # shape 1410
Lx = mask.shape[1] # shape 770
#pm = grid_nc.variables['pm'][:,:]
#pn = grid_nc.variables['pn'][:,:]
#h = grid_nc.variables['h'][:,:]

#mean_pm = np.mean(pm)
#mean_pn = np.mean(pn)

# region
'''
r_y0 = 0
r_yE = Ly
r_x0 = 0
r_xE = Lx
'''

r_y0 = 50
r_yE = 650
r_x0 = 400
r_xE = Lx


lat_mean = np.mean(lat_plt)
lon_mean = np.mean(lon_plt)

#pn_mult = (1E-3/mean_pn)
#pm_mult = (1E-3/mean_pm)

#r_y0_km = r_y0 * pn_mult 
#r_yE_km = r_yE * pn_mult
#r_x0_km = r_x0 * pm_mult
#r_xE_km = r_xE * pm_mult

#im_ext_km = [r_x0_km,r_xE_km,r_y0_km,r_yE_km]

################
# MAKE BASEMAP
################
'''
# all of california
lat_min = 31.5
lat_max = 42.5
lon_min = -125
lon_max = -115
'''
# so cal
lat_min = 32
lat_max = 35
lon_min = -120.5
lon_max = -117

# use epsg for high resolution map instead of etopo, epsg number is for America
# see https://stackoverflow.com/questions/20768777/how-to-draw-a-high-resolution-etopo-background-in-matplotlib-basemap
#m = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,epsg=4269)
m = Basemap(projection='stere',resolution='h',llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,epsg=4269)

# compute map projection coords

x_major_potw,y_major_potw = m(lons_major_potw,lats_major_potw)

x_minor_potw,y_minor_potw = m(lons_minor_potw,lats_minor_potw)

x_river,y_river = m(lons_river,lats_river)

############################
# PLOT RIVER LAT/LON ON GRID
############################
def plot_inputs(x_coords, y_coords, msize):
    [plt.plot(x_coords[n], y_coords[n],'o',markeredgecolor='orange',mfc='orange',markersize=msize) for n in range(len(x_coords))] 

def m_plot_inputs(x, y, msize, c, l):
    [m.plot(x[n], y[n],'o',markeredgecolor=c,mfc=c,markersize=msize,label=l) for n in range(len(x))] 


# latitudes to draw
parallels = np.arange(0,90,1)
# longitudes to draw
meridians = np.arange(180,360,1)

axis_tick_size = 16


fig_w = 15
fig_h = 12

major_c = 'red'
minor_c = 'magenta'
river_c = 'yellow'
edge_color = 'darkgray'
m_size = 150
line_width = .7

fig = plt.figure(figsize=[fig_w,fig_h])
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
# use high resolution topography map
#m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS',service='ESRI_Imagery_World_2D',xpixels=2000,ypixels=None,dpi=100,verbose=True)
m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS',service='ESRI_Imagery_World_2D',xpixels=2000)
#m.bluemarble()
'''
# plot separate inputs in different colors
m_plot_inputs(x_major_potw,y_major_potw,3,'red',l='Major POTW')
m_plot_inputs(x_minor_potw,y_minor_potw,3,'teal',l='Major POTW')
m_plot_inputs(x_river,y_river,3,'yellow',l='Rivers')
plt.legend(loc='best')
'''
# plot using scatter separate inputs in different colors
maj_potw_plt = m.scatter(x_major_potw,y_major_potw,s=m_size,marker='o',color=major_c,edgecolor=edge_color,lw=line_width,label='Major POTW',zorder=12)

min_potw_plt = m.scatter(x_minor_potw,y_minor_potw,s=m_size,marker='^',color=minor_c,edgecolor=edge_color,lw=line_width,label='Minor POTW',zorder=11)

river_plt = m.scatter(x_river,y_river,s=m_size,marker='s',color=river_c,edgecolor=edge_color,lw=line_width,label='Rivers',zorder=10)
plt.legend(loc='lower left',fontsize=25)
'''
# plot labels
label_font = 13

major_xoffset = .1
major_yoffset = .1

minor_xoffset = -.03
minor_yoffset = .01

for label,xpt,ypt in zip(major_potw_names,x_major_potw,y_major_potw):
    plt.text(xpt-major_xoffset,ypt-major_yoffset,label,fontsize=label_font,color='white')

# these indexes are fine to be plotted like this
# San Clemente to Carpinteria
lw = .2
s_ind = 1
e_ind = 10+1
for label,xpt,ypt in zip(minor_potw_names[s_ind:e_ind],x_minor_potw[s_ind:e_ind],y_minor_potw[s_ind:e_ind]):
    plt.text(xpt-minor_xoffset,ypt-minor_yoffset,label,fontsize=label_font+1,color='white',path_effects=[path_effects.Stroke(linewidth=lw,foreground='black')],zorder=20)

# South Bay (offset down and left)
plt.text(x_minor_potw[0]-(major_xoffset+.03),y_minor_potw[0]-major_yoffset,minor_potw_names[0],fontsize=label_font+1,color='white',path_effects=[path_effects.Stroke(linewidth=lw,foreground='black')],zorder=20)

# El Estero, Montecito, Summerland (rotate/move text so not on top of each other)
# El Estero
rot_e = 30
xoff_e = -.08
yoff_e = -.15
plt.text(x_minor_potw[-3]-xoff_e,y_minor_potw[-3]-yoff_e,minor_potw_names[-3],fontsize=label_font+1,color='white',rotation=rot_e,path_effects=[path_effects.Stroke(linewidth=lw,foreground='black')],zorder=20)

# Montecito
rot_m = 50
xoff_e = -.008
yoff_e = -.25
plt.text(x_minor_potw[-2]-xoff_e,y_minor_potw[-2]-yoff_e,minor_potw_names[-2],fontsize=label_font+1,color='white',rotation=rot_m,path_effects=[path_effects.Stroke(linewidth=lw,foreground='black')],zorder=20)

# Summerland
xoff_s = .4
yoff_s = .1
plt.text(x_minor_potw[-1]-xoff_s,y_minor_potw[-1]-yoff_s,minor_potw_names[-1],fontsize=label_font+1,color='white',path_effects=[path_effects.Stroke(linewidth=lw,foreground='black')],zorder=20)
'''
plt.savefig(save_figs_path+'inputs_basemap_nolabels.png',bbox_inches='tight')

