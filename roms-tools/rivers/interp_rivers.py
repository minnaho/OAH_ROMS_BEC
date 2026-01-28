# SEE /data/project9/minnaho/swel/rivers/make_rivers_grid.py
# interpolate rivers from parent to child grid
# only works on the river locations in the grid and fractionation

import numpy as np
from netCDF4 import Dataset
import numpy as np
from scipy.ndimage import distance_transform_edt
from collections import deque
import matplotlib.pyplot as plt
plt.ion()

par_grd_nm = '/data/project9/minnaho/swel/smode200_grd.nc'
old_ch_grd_nm = '/data/project9/minnaho/swel/mc60_grd.nc'
ch_grd_nm = '/data/project9/minnaho/swel/mc60_newlarge_grd.nc'

par_grd = Dataset(par_grd_nm,'r')
oc_grd = Dataset(old_ch_grd_nm,'r')
ch_grd = Dataset(ch_grd_nm,'r+')

plon = np.array(par_grd.variables['lon_rho'])
plat = np.array(par_grd.variables['lat_rho'])
pmask = np.array(par_grd.variables['mask_rho'])

oclon = np.array(oc_grd.variables['lon_rho'])
oclat = np.array(oc_grd.variables['lat_rho'])
ocmask = np.array(oc_grd.variables['mask_rho'])

clon = np.array(ch_grd.variables['lon_rho'])
clat = np.array(ch_grd.variables['lat_rho'])
cmask = np.array(ch_grd.variables['mask_rho'])

prf = np.array(par_grd.variables['river_flux'])
orf = np.array(oc_grd.variables['river_flux'])

priv_eta = np.where(prf>0)[0]
priv_xi = np.where(prf>0)[1]

oriv_eta = np.where(orf>0)[0]
oriv_xi = np.where(orf>0)[1]

# get river indices of 
# rivers for mc60 domain, rivers 1-8
prind = np.where(prf[priv_eta,priv_xi]<9)[0]

prind_eta = priv_eta[prind]
prind_xi = priv_xi[prind]

# get river lon/lat
priv_lon = plon[prind_eta,prind_xi]
priv_lat = plat[prind_eta,prind_xi]

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

ch_xi,ch_eta = calc_ij(ch_grd,priv_lat,priv_lon)

# move all river points on water to land
if 1 in cmask[ch_eta.astype(int),ch_xi.astype(int)]:
    plt.imshow(cmask,origin='lower')
    distance, indices = distance_transform_edt(cmask == 1, return_indices=True)
    for c_i in range(len(cmask[ch_eta.astype(int),ch_xi.astype(int)])):
        if cmask[ch_eta.astype(int),ch_xi.astype(int)][c_i] == 1:
            nearest_land = (indices[0][ch_eta[c_i].astype(int),ch_xi[c_i].astype(int)], indices[1][ch_eta[c_i].astype(int),ch_xi[c_i].astype(int)])
            print("Closest land to eta, xi:",ch_eta[c_i].astype(int),ch_xi[c_i].astype(int)," is at ",nearest_land)
            print('moving to that point now')
            ch_eta[c_i] = nearest_land[0]
            ch_xi[c_i] = nearest_land[1]

# check all land points are next to water
# and if not, move them to the next land point next to water that 
# doesn't already have a river flux
def find_nearest_zero_next_to_one_unique(mask, x_list, y_list, max_search_radius=10):

    rows, cols = mask.shape
    results = []
    used_coords = set()  # Track already-used coordinates

    def is_next_to_one(y, x):
        neighbors = [
            (y - 1, x),
            (y + 1, x),
            (y, x - 1),
            (y, x + 1)
        ]
        for ny, nx in neighbors:
            if 0 <= ny < rows and 0 <= nx < cols:
                if mask[ny, nx] == 1:
                    return True
        return False

    for x0, y0 in zip(x_list, y_list):
        if mask[y0, x0] != 0:
            results.append((False, None))  # not a 0 to begin with
            continue

        # Case 1: the original 0 is next to a 1 and not already used
        if is_next_to_one(y0, x0) and (x0, y0) not in used_coords:
            used_coords.add((x0, y0))
            results.append((True, (x0, y0)))
            continue

        # Case 2: BFS to find nearest unused 0 next to 1
        visited = set()
        queue = deque()
        queue.append((x0, y0, 0))
        visited.add((x0, y0))
        found = False
        nearest_coords = None

        while queue:
            x, y, dist = queue.popleft()
            if dist > max_search_radius:
                break
            if mask[y, x] == 0 and is_next_to_one(y, x) and (x, y) not in used_coords:
                found = True
                nearest_coords = (x, y)
                used_coords.add((x, y))
                break
            # Check 4 neighbors
            neighbors = [
                (y - 1, x),
                (y + 1, x),
                (y, x - 1),
                (y, x + 1)
            ]
            for ny, nx in neighbors:
                if 0 <= ny < rows and 0 <= nx < cols:
                    if (nx, ny) not in visited and mask[ny, nx] == 0:
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))
        if found:
            results.append((False, nearest_coords))
        else:
            results.append((False, None))
    return results



output = find_nearest_zero_next_to_one_unique(cmask,ch_xi.astype(int),ch_eta.astype(int))
for original, result in zip(zip(ch_xi.astype(int), ch_eta.astype(int)), output):
    status, coords = result
    print(f"Original: {original}, Next to 1: {status}, Nearest Zero Next to 1: {coords}")

# Move invalid river points to the nearest valid '0' next to '1'
for i, ((orig_x, orig_y), (status, new_coords)) in enumerate(zip(zip(ch_xi.astype(int), ch_eta.astype(int)), output)):
    if not status and new_coords is not None:
        print(f"Moving river point from ({orig_x}, {orig_y}) to nearest valid point {new_coords}")
        ch_xi[i] = new_coords[0]
        ch_eta[i] = new_coords[1]
    elif not status and new_coords is None:
        print(f"Warning: No valid neighbor found within search radius for point ({orig_x}, {orig_y})")

# Optionally plot moved points for verification
plt.figure()
plt.imshow(cmask, origin='lower', cmap='gray')
plt.scatter(ch_xi, ch_eta, color='red', label='Adjusted River Points')
plt.legend()
plt.title("Adjusted River Points on Mask")
plt.show()

# assign fractionation of river flux
crf = np.copy(prf[priv_eta,priv_xi][prind])

# add river_flux to child grid
# Get dimensions
eta_dim = ch_grd.dimensions['eta_rho']
xi_dim = ch_grd.dimensions['xi_rho']

# Create the variable: float32, with dimensions (eta_rho, xi_rho)
if 'river_flux' not in ch_grd.variables:
    river_flux_var = ch_grd.createVariable('river_flux', 'f4', ('eta_rho', 'xi_rho'))
else:
    river_flux_var = ch_grd.variables['river_flux']

# initialize with zeros 
river_flux_var[:, :] = 0.0  

# fix river 2nd from the top
ch_xi[18] = 276
ch_eta[18] = 1142
ch_xi[19:21] = 277
ch_eta[19] = 1144
ch_eta[20] = 1145

# fix Elkhorn Slough location (looked at it manually)
#ch_xi[6:9] = 698
#ch_eta[6] = 482
#ch_eta[7] = 483
#ch_eta[8] = 486


# fix Pajarjo river (looked at it manually)
#ch_eta[9] = 555
#ch_eta[10] = 556
#ch_eta[11] = 557
#

# Ensure your ch_eta and ch_xi are integers
ch_eta_int = ch_eta.astype(int)
ch_xi_int = ch_xi.astype(int)

# assign fractination values at river locations
for r_i in range(len(ch_eta_int)):
    river_flux_var[ch_eta_int[r_i], ch_xi_int[r_i]] = crf[r_i]

# Add metadata (optional)
river_flux_var.long_name = "River volume flux partition"
print("river_flux variable created and initialized.")

# Close the file after writing
ch_grd.close()

# check locations
ch_grd = Dataset(ch_grd_nm,'r')
crf2 = np.array(ch_grd.variables['river_flux'])

criv_eta = np.where(crf2>0)[0]
criv_xi = np.where(crf2>0)[1]

plt.figure()
plt.imshow(cmask, origin='lower', cmap='gray')
plt.scatter(criv_xi, criv_eta, color='red')
plt.legend()
plt.title("child grid rivers")

plt.figure()
plt.imshow(pmask, origin='lower', cmap='gray')
plt.scatter(priv_xi, priv_eta, color='red')
plt.legend()
plt.title("parent grid rivers")
plt.show()


plt.figure()
plt.imshow(ocmask, origin='lower', cmap='gray')
plt.scatter(oriv_xi, oriv_eta, color='red')
plt.legend()
plt.title("old mc grid rivers")
plt.show()
