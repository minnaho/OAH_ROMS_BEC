###################################################################
# read calcofi data and other data net primary production and nitrification
# compare to L2 model 1997-2000
# Nov 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
plt.ion()

# cut off depth
d_e = 40

##########################
# load observation data
#########################
# rate data from Karen
rate_name = '/data/project1/minnaho/validation/ValidationRateData_mh.xlsx'
nitr_rate_df = pd.read_excel(rate_name,sheet_name='Nitrification and nut uptake')
#growth_df = pd.read_excel(rate_name,sheet_name='growth and grazing')

# model data 2 1997- 9 2000
model_path_deep = './extract_zslice/'
model_path_surf = './extract_zslice/'
model_path_all = './extract_zslice/slices/'

fig_path = './npp_nitrif_figs/'


# choose years
yr_s = 1997
yr_e = 2000

#####################################################
# load L2 grid and get grid locations of all sites within year range
#####################################################
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
nc_grid = Dataset(grid_path,'r')

lon_nc = nc_grid.variables['lon_rho'][:,:]
lat_nc = nc_grid.variables['lat_rho'][:,:]
mask_nc = nc_grid.variables['mask_rho'][:,:]

# choose between what lat/lon
# L2 domain 
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)


##########
# validationratedata
##########

r_lat = np.array(nitr_rate_df['Lat'])
r_lon = np.array(nitr_rate_df['Lon'])

r_lat_ind = np.where((r_lat>lat_min) & (r_lat<lat_max))[0]
r_lon_ind = np.where((r_lon>lon_min) & (r_lon<lon_max))[0]

r_loc_ind = np.asarray((list(set(r_lat_ind).intersection(r_lon_ind))))
#r_data_ind = np.asarray(sorted((list(set(r_loc_ind).intersection(rate_yr_ind)))))

r_depth = np.array(nitr_rate_df['Depth'])[r_loc_ind]
r_data  = np.array(nitr_rate_df['NitrRate'])[r_loc_ind]

r_lat_data = np.array(r_lat[r_loc_ind])
r_lon_data = np.array(r_lon[r_loc_ind])
r_date_data = pd.to_datetime(nitr_rate_df['Date'])[r_loc_ind]

r_loc_u = np.unique(np.array((r_lat_data,r_lon_data)).transpose(),axis=0)

# find rate data locations
r_x_coord = np.empty((len(r_loc_u)))
r_y_coord = np.empty((len(r_loc_u)))
for l_i in range(len(r_loc_u)):
    min_l = np.abs( (lat_nc - r_loc_u[l_i][0])**2 + (lon_nc - r_loc_u[l_i][1])**2)
    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
    r_x_coord[l_i] = x_site
    r_y_coord[l_i] = y_site

#########################
# statistics and analyses
#########################
# nitrification rate data
r_spring_ind_l = []
r_winter_ind_l = []
r_summer_ind_l = []
r_fall_ind_l = []

for d_i,pd_i in enumerate(r_date_data):
    m = pd_i.month
    if m == 12 or m == 1 or m == 2:
        r_winter_ind_l.append(d_i)
    if m == 3 or m == 4 or m == 5:
        r_spring_ind_l.append(d_i)
    if m == 6 or m == 7 or m == 8:
        r_summer_ind_l.append(d_i)
    if m == 9 or m == 10 or m == 11:
        r_fall_ind_l.append(d_i)

r_spring_ind = np.array(r_spring_ind_l)
r_winter_ind = np.array(r_winter_ind_l)
r_summer_ind = np.array(r_summer_ind_l)
r_fall_ind   = np.array(r_fall_ind_l)

r_deep_ind = np.where(r_depth>d_e)[0]
r_surface_ind = np.where(r_depth<=d_e)[0]

r_spring_surf_ind = np.asarray((list(set(r_surface_ind).intersection(r_spring_ind))))
r_winter_surf_ind = np.asarray((list(set(r_surface_ind).intersection(r_winter_ind))))
r_summer_surf_ind = np.asarray((list(set(r_surface_ind).intersection(r_summer_ind))))
r_fall_surf_ind   = np.asarray((list(set(r_surface_ind).intersection(r_fall_ind))))
r_spring_deep_ind = np.asarray((list(set(r_deep_ind).intersection(r_spring_ind))))
r_winter_deep_ind = np.asarray((list(set(r_deep_ind).intersection(r_winter_ind))))
r_summer_deep_ind = np.asarray((list(set(r_deep_ind).intersection(r_summer_ind))))
r_fall_deep_ind   = np.asarray((list(set(r_deep_ind).intersection(r_fall_ind))))

################
# model data and plotting
################
c_conv = 12
sec_day = 86400
npp_conv_m = c_conv
npp_conv_o = (1./sec_day)
nit_conv = (1./sec_day)*(1./1000) # convert nmol/L/day to mmol/m3/s

h_plot = 9
w_plot = 6

intv0 = 5
intv1 = 95

keyword = 'loc'
fliers = 'yes'
'''
################
# all seasons surface
##################
m_files = glob.glob(model_path_surf+'*Y*_0_40.nc')

npp_obs = list((cc_data_slice[cc_winter_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_spring_surf_ind])*npp_conv_o)+ list((cc_data_slice[cc_summer_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_fall_surf_ind])*npp_conv_o)
#nit_obs = list((r_data[r_winter_surf_ind])*nit_conv)+list((r_data[r_spring_surf_ind])*nit_conv)+ list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_surf_ind])*nit_conv)
nit_obs = list((r_data[r_spring_surf_ind])*nit_conv)+ list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_surf_ind])*nit_conv)
season = 'year'

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
nit_plot = [list(nit_obs),list(nit_flat)]
if fliers=='no':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1])

ax2.set_xlabel('Integrated Primary Production')
ax2.set_ylabel('mg C m$^{-2}$ s$^{-1}$')
npp_plot = [npp_obs,npp_flat]
if fliers=='no':
    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1])
ax1.grid(True)
ax2.grid(True)
plt.savefig(fig_path+savename,bbox_inches='tight')
plt.close()

################
# all seasons deep
##################
m_files = glob.glob(model_path_deep+'*Y*_40_1000.nc')

npp_obs = list((cc_data_slice[cc_winter_deep_ind])*npp_conv_o)+list((cc_data_slice[cc_spring_deep_ind])*npp_conv_o)+ list((cc_data_slice[cc_summer_deep_ind])*npp_conv_o)+list((cc_data_slice[cc_fall_deep_ind])*npp_conv_o)
#nit_obs = list((r_data[r_winter_deep_ind])*nit_conv)+list((r_data[r_spring_deep_ind])*nit_conv)+ list((r_data[r_summer_deep_ind])*nit_conv)+list((r_data[r_fall_deep_ind])*nit_conv)
nit_obs = list((r_data[r_spring_deep_ind])*nit_conv)+ list((r_data[r_summer_deep_ind])*nit_conv)+list((r_data[r_fall_deep_ind])*nit_conv)
season = 'year'

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
nit_plot = [list(nit_obs),list(nit_flat)]
if fliers=='no':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1])

ax2.set_xlabel('Integrated Primary Production')
ax2.set_ylabel('mg C m$^{-2}$ s$^{-1}$')
npp_plot = [npp_obs,npp_flat]
if fliers=='no':
    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1])
ax1.grid(True)
ax2.grid(True)
plt.savefig(fig_path+savename,bbox_inches='tight')
plt.close()
'''
######################
# all seasons all depths
#######################
nit_obs = list((r_data[r_spring_deep_ind])*nit_conv) + list((r_data[r_spring_surf_ind])*nit_conv)+list((r_data[r_summer_deep_ind])*nit_conv) + list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_deep_ind])*nit_conv) + list((r_data[r_fall_surf_ind])*nit_conv)
season = 'year'

# box and whisker
f_size = 16
savename = 'nitrif_bight_obs_only_fliers.png'
fig1,ax1 = plt.subplots(1,1,figsize=[w_plot,h_plot])

ax1.set_title('Nitrification',fontsize=f_size)
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$',fontsize=f_size)
ax1.set_xlabel('LA/OC San Pedro region',fontsize=f_size)
nit_plot = list(nit_obs)
if fliers=='no':
    ax1.boxplot(nit_plot,whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax1.boxplot(nit_plot,whis=[intv0,intv1])
ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
ax1.tick_params(labelsize=14)
ax1.set_xticks([])
ax1.grid(True)
plt.savefig(fig_path+savename,bbox_inches='tight')

# uptake rates

