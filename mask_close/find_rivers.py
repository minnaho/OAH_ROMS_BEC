from netCDF4 import Dataset
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import spatial
plt.ion()

grid_path = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc'

data = Dataset(grid_path,'r')
mask = data.variables['mask_rho'][:,:]
lat_nc = data.variables['lat_rho'][:,:]
lon_nc = data.variables['lon_rho'][:,:]

# LA river, Ventura
#lat_data = [33.7408,34.2717] 
#lon_data = [-118.219,-119.315]

lon_data = np.array(
[-117.692,
-119.83,
-119.642,
-117.261,
-117.247,
-118.768,
-118.219,
-119.83,
-117.729,
-118.971,
-117.966,
-118.609,
-117.828,
-118.457,
-117.136,
-117.421,
-118.213,
-118.596,
-119.479,
-118.722,
-119.274,
-118.531,
-117.451,
-118.642,
-117.261,
-117.247,
-117.271,
-117.32,
-118.938,
-117.884,
-119.315,
-118.395,
-119.718,
-118.81,
-118.847,
-118.655,
-119.099,
-118.128,
-117.397,
-117.355,
-117.367,
-117.292,
-117.476,
-117.282,
-117.593,
-117.32,
-117.261,
-117.247,
-117.729,
-118.095,
-117.884,
-119.531,
-117.884,
-118.128,
-117.599,
-119.89,
-118.247424,
-118.041,
-119.83,
-117.79,
-118.682,
-117.641,
-119.099,
-117.599,
-119.83,
-117.884,
-117.641,
-118.596,
-118.829,
-119.7402756,
-120.2272929,
-119.5220235,
])

lat_data = np.array(
[33.4521,
34.4105,
34.4089,
32.7529,
32.6596,
34.0182,
33.7408,
34.4105,
33.4757,
34.0468,
33.6292,
34.0305,
33.5567,
33.9561,
32.5464,
33.2221,
33.735,
34.0297,
34.3705,
34.0209,
34.2196,
34.015,
33.2614,
34.027,
32.7529,
32.6596,
32.9221,
33.0818,
34.0394,
33.5868,
34.2717,
33.8379,
34.3864,
33.9987,
34.0229,
34.0278,
34.0986,
33.7358,
33.1993,
33.1377,
33.1599,
33.01,
33.2843,
32.9661,
33.3713,
33.0818,
32.7529,
32.6596,
33.4757,
33.7286,
33.5868,
34.3849,
33.5868,
33.7358,
33.377,
34.409,
33.708504,
33.6767,
34.4105,
33.5331,
34.0294,
33.4279,
34.0986,
33.377,
34.4105,
33.5868,
33.4279,
34.0297,
34.0054,
34.40479931,
34.47279229,
34.40129042,
])
coord_i = []
coord_j = []
for coord in range(len(lat_data)):
    lat_you_want = lat_data[coord]
    lon_you_want = lon_data[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    coord_i.append(xi_coord)
    coord_j.append(eta_coord)

'''
Jsrc = Dataset('/data/project3/kesf/tools_roms/psource/psource_L2_scbV6.nc','r').variables['Jsrc'][:]
Isrc = Dataset('/data/project3/kesf/tools_roms/psource/psource_L2_scbV6.nc','r').variables['Isrc'][:]
'''
'''

fig = plt.figure(figsize=[9,15])
ax = fig.add_subplot(111)
ax.imshow(mask,origin='lower')
plt.plot(coord_i,coord_j,'o',color='white')
for i in range(len(coord_i)):
    ax.annotate(str(i+86),(coord_i[i+86],coord_j[i+86]))
'''

# i,j places where mask == 1 (water)
mask_i = np.where(mask==1)[1]
mask_j = np.where(mask==1)[0]
# pairs of i,j arrays (([i,j],[i,j],...))
mask_1 = np.column_stack((mask_i,mask_j))
# i,j places where mask == 0 (land)

# i,j places where mask == 0 (land) (want rivers 1 grid point onto land)
# pairs of i,j arrays (([i,j],[i,j],...))
mask_0 = np.column_stack((np.where(mask==0)[1],np.where(mask==0)[0]))

'''
# find grid points RIGHT OFF land (coastal water, 1 grid point off land)
# TAKES VERY LONG
mask_0 = np.column_stack((np.where(mask==0)[1],np.where(mask==0)[0]))
coast_i = []
coast_j = []
for pt_0 in range(len(mask_0)):
    print('coast: '+str(pt_0)+' of '+str(len(mask_0)))
    index_0 = spatial.KDTree(mask_1).query(mask_0[pt_0])[1]
    coast_i.append(mask_1[index_0][0])
    coast_j.append(mask_1[index_0][1])    
'''
# find closest land point to river
coord_i_land_l = []
coord_j_land_l = []
for pt in range(len(coord_i)): 
    print('land: '+str(pt)+' of '+str(len(coord_i)))
    index = spatial.KDTree(mask_0).query([coord_i[pt],coord_j[pt]])[1]
    coord_i_land_l.append(mask_0[index][0])
    coord_j_land_l.append(mask_0[index][1])

coord_i_land_arr = np.array(coord_i_land_l)
coord_j_land_arr = np.array(coord_j_land_l)

# automatically find coastal water (water one grid point off land) 
# closest to river i,j found from lat,lon
coord_i_new = []
coord_j_new = []
for pt in range(len(coord_i)):
    print('rivers: '+str(pt)+' of '+str(len(coord_i)))
    #mask_pt = mask_1[spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))[1]]
    #distance,index = spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))
    index = spatial.KDTree(mask_1).query(np.array((coord_i_land_arr[pt],coord_j_land_arr[pt])))[1]
    coord_i_new.append(mask_1[index][0])
    coord_j_new.append(mask_1[index][1])
'''
# automatically find mask point == 1 (water) closest to river i,j found from lat,lon
coord_i_new = []
coord_j_new = []
for pt in range(len(coord_i)):
    print('rivers: '+str(pt)+' of '+str(len(coord_i)))
    #mask_pt = mask_1[spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))[1]]
    #distance,index = spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))
    index = spatial.KDTree(mask_1).query(np.array((coord_i[pt],coord_j[pt])))[1]
    coord_i_new.append(mask_1[index][0])
    coord_j_new.append(mask_1[index][1])
'''



coord_i_arr = np.array(coord_i)
coord_i_arr_new = np.array(coord_i_new)
coord_j_arr = np.array(coord_j)
coord_j_arr_new = np.array(coord_j_new)
'''
# manually move LA harbor
#la_harb_i = np.where(coord_i_arr_new==547)[0]
la_harb_j = np.where(coord_j_arr_new==559)[0]

coord_j_arr_new[la_harb_j] = 566
'''

'''
# compare movement of points
coord_i_diff = coord_i_arr_new - coord_i_arr
print(coord_i_diff)

coord_j_diff = coord_j_arr_new - coord_j_arr
print(coord_j_diff)
'''

'''
# now find first land point from water because need rivers flowing out from land
coord_i_land_l = []
coord_j_land_l = []
for pt in range(len(coord_i)): 
    print('land: '+str(pt)+' of '+str(len(coord_i)))
    index = spatial.KDTree(mask_0).query([coord_i_arr_new[pt],coord_j_arr_new[pt]])[1]
    coord_i_land_l.append(mask_0[index][0])
    coord_j_land_l.append(mask_0[index][1])

coord_i_land_arr = np.array(coord_i_land_l)
coord_j_land_arr = np.array(coord_j_land_l)

fig = plt.figure(figsize=[9,15])
ax = fig.add_subplot(111)
ax.imshow(mask,origin='lower')
plt.plot(coord_i_land_arr,coord_j_land_arr,'o',color='white')
'''

'''
psource file --> rivers start at index 85 (0 base indexing)
index 91,113,135,136 same i,j in psource file
index 91,113,135 == index 6,28,50 in lat/lon files and lats/lons match each other
index 136 == index 51 in lat_data,lon_data but lat/lon doesn't match 
possibly duplicate being made at 136 that should not be there

Franklin Creek is not in psource code but present in lat/lon data
(last river in lat/lon files and should be last index in psource file)
'''
