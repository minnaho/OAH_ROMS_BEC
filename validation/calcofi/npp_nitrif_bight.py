###################################################################
# read calcofi data and other data net primary production and nitrification
# compare to L2 model 1997-2000
# Nov 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
#plt.ion()

# cut off depth
d_e = 40

##########################
# load observation data
#########################
# calcofi
text_file = pd.read_csv('calcofi_database.csv',header=None,low_memory=False,skiprows=1)
time_unit = 'minutes since 1949-03-01 09:30:00'
# choose variable
variable_name = 'integrated_primary_prod'
cc_n_unit = 'mg C/m2'
cc_num = 16

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

# calcofi convert datetime numbers to dates
cc_time_num = np.array((text_file.iloc[:,1]))
cc_date_conv = num2date(cc_time_num,time_unit)


# get indexes of target years
print('getting indices of target years')
cc_yr_ind_l = []
for ind_d,d_i in enumerate(cc_date_conv):
    if d_i.year in list(range(yr_s,yr_e+1)):
        cc_yr_ind_l.append(ind_d) 

cc_yr_ind = np.array((cc_yr_ind_l))

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
# calcofi
##########
cc_lat = np.array((text_file.iloc[:,2]))
cc_lon = np.array((text_file.iloc[:,3]))

cc_lat_ind = np.where((cc_lat>lat_min) & (cc_lat<lat_max))[0]
cc_lon_ind = np.where((cc_lon>lon_min) & (cc_lon<lon_max))[0]

# find intersection of index values
cc_loc_ind = np.asarray((list(set(cc_lat_ind).intersection(cc_lon_ind))))
# find years and locations that we want
cc_data_ind = np.asarray(sorted((list(set(cc_loc_ind).intersection(cc_yr_ind)))))

# data variable
cc_data_var = np.array((text_file.iloc[:,cc_num][cc_data_ind]))

cc_t_ind = np.where(~np.isnan(cc_data_var))[0]
cc_data_slice = cc_data_var[cc_t_ind]
cc_data_lat = cc_lat[cc_data_ind][cc_t_ind]
cc_data_lon = cc_lon[cc_data_ind][cc_t_ind]
cc_loc_u = np.unique(np.array((cc_data_lat,cc_data_lon)).transpose(),axis=0)

cc_data_depth = np.array((text_file.iloc[:,19][cc_data_ind]))[cc_t_ind]

cc_data_date = cc_date_conv[cc_data_ind][cc_t_ind]

# find calcofi locations
cc_x_coord = np.empty((len(cc_loc_u)))
cc_y_coord = np.empty((len(cc_loc_u)))
for l_i in range(len(cc_loc_u)):
    min_l = np.abs( (lat_nc - cc_loc_u[l_i][0])**2 + (lon_nc - cc_loc_u[l_i][1])**2)
    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
    cc_x_coord[l_i] = x_site
    cc_y_coord[l_i] = y_site


#plt.figure()
#plt.imshow(mask_nc,origin='lower')
#plt.scatter(cc_x_coord,cc_y_coord)

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

# integrated primary productivity data calcofi
cc_spring_ind_l = []
cc_winter_ind_l = []
cc_summer_ind_l = []
cc_fall_ind_l = []

for d_i in range(len(cc_data_date)):
    m = cc_data_date[d_i].month
    if m == 12 or m == 1 or m == 2:
        cc_winter_ind_l.append(d_i)
    if m == 3 or m == 4 or m == 5:
        cc_spring_ind_l.append(d_i)
    if m == 6 or m == 7 or m == 8:
        cc_summer_ind_l.append(d_i)
    if m == 9 or m == 10 or m == 11:
        cc_fall_ind_l.append(d_i)

cc_spring_ind = np.array(cc_spring_ind_l)
cc_winter_ind = np.array(cc_winter_ind_l)
cc_summer_ind = np.array(cc_summer_ind_l)
cc_fall_ind   = np.array(cc_fall_ind_l)

cc_deep_ind = np.where(cc_data_depth>d_e)[0]
cc_surface_ind = np.where(cc_data_depth<=d_e)[0]

cc_spring_surf_ind = np.asarray((list(set(cc_surface_ind).intersection(cc_spring_ind))))
cc_winter_surf_ind = np.asarray((list(set(cc_surface_ind).intersection(cc_winter_ind))))
cc_summer_surf_ind = np.asarray((list(set(cc_surface_ind).intersection(cc_summer_ind))))
cc_fall_surf_ind   = np.asarray((list(set(cc_surface_ind).intersection(cc_fall_ind))))
cc_spring_deep_ind = np.asarray((list(set(cc_deep_ind).intersection(cc_spring_ind))))
cc_winter_deep_ind = np.asarray((list(set(cc_deep_ind).intersection(cc_winter_ind))))
cc_summer_deep_ind = np.asarray((list(set(cc_deep_ind).intersection(cc_summer_ind))))
cc_fall_deep_ind   = np.asarray((list(set(cc_deep_ind).intersection(cc_fall_ind))))

################
# model data and plotting
################
c_conv = 12
sec_day = 86400
npp_conv_m = c_conv
npp_conv_o = (1./sec_day)
nit_conv = (1./sec_day)*(1./1000) # nmol/L/day

h_plot = 8
w_plot = 12

intv0 = 5
intv1 = 95

keyword = 'loc'
fliers = 'no'

##################
# spring surface
##################
npp_obs = (cc_data_slice[cc_spring_surf_ind])*npp_conv_o
nit_obs = (r_data[r_spring_surf_ind])*nit_conv
m_files = glob.glob(model_path_surf+'*Y*M0[3-5]_0_40.nc')
season = 'spring'

npp_list = []
nit_list = []

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_surf_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_surf_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# winter surface
##################
m_files0 = glob.glob(model_path_surf+'*Y*M[0-1]2_0_40.nc')
m_files1 = glob.glob(model_path_surf+'*Y*M01_0_40.nc')
m_files = m_files0+m_files1

npp_obs = (cc_data_slice[cc_winter_surf_ind])*npp_conv_o
#nit_obs = (r_data[r_winter_surf_ind])*nit_conv
season = 'winter'

npp_list = []
nit_list = []

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_surf_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_surf_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
#nit_plot = [list(nit_obs),list(nit_flat)]
nit_plot = [list(),list(nit_flat)]
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

##################
# summer surface
##################
m_files = glob.glob(model_path_surf+'*Y*M0[6-8]_0_40.nc')
npp_obs = (cc_data_slice[cc_summer_surf_ind])*npp_conv_o
nit_obs = (r_data[r_summer_surf_ind])*nit_conv
season = 'summer'

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_surf_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_surf_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# fall surface
##################
m_files0 = glob.glob(model_path_surf+'*Y*M09_0_40.nc')
m_files1 = glob.glob(model_path_surf+'*Y*M1[0-1]_0_40.nc')
m_files = m_files0+m_files1

npp_obs = (cc_data_slice[cc_fall_surf_ind])*npp_conv_o
nit_obs = (r_data[r_fall_surf_ind])*nit_conv
season = 'fall'

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_surf_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_surf_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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
# all seasons surface
##################
m_files = glob.glob(model_path_surf+'*Y*_0_40.nc')

npp_obs = list((cc_data_slice[cc_winter_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_spring_surf_ind])*npp_conv_o)+ list((cc_data_slice[cc_summer_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_fall_surf_ind])*npp_conv_o)
#nit_obs = list((r_data[r_winter_surf_ind])*nit_conv)+list((r_data[r_spring_surf_ind])*nit_conv)+ list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_surf_ind])*nit_conv)
nit_obs = list((r_data[r_spring_surf_ind])*nit_conv)+ list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_surf_ind])*nit_conv)
season = 'year'

season = 'year'

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_surf_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_surf_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# spring deep 
##################
m_files = glob.glob(model_path_deep+'*Y*M0[3-5]_40_1000.nc')
npp_obs = (cc_data_slice[cc_spring_deep_ind])*npp_conv_o
nit_obs = (r_data[r_spring_deep_ind])*nit_conv
season = 'spring'

npp_list = []
nit_list = []
for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_deep_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_deep_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)


npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# winter deep 
##################
m_files0 = glob.glob(model_path_deep+'Y*M[0-1]2_40_1000.nc')
m_files1 = glob.glob(model_path_deep+'Y*M01_40_1000.nc')
m_files = m_files0+m_files1
npp_obs = (cc_data_slice[cc_winter_deep_ind])*npp_conv_o
#nit_obs = (r_data[r_winter_deep_ind])*nit_conv
season = 'spring'

npp_list = []
nit_list = []
for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_deep_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_deep_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)


npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
#nit_plot = [list(nit_obs),list(nit_flat)]
nit_plot = [list(),list(nit_flat)]

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

##################
# summer deep 
##################
m_files = glob.glob(model_path_deep+'*Y*M0[6-8]_40_1000.nc')
npp_obs = (cc_data_slice[cc_summer_deep_ind])*npp_conv_o
nit_obs = (r_data[r_summer_deep_ind])*nit_conv
season = 'summer'

npp_list = []
nit_list = []
for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_deep_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_deep_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)


npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# fall deep
##################
m_files0 = glob.glob(model_path_deep+'Y*M09_40_1000.nc')
m_files1 = glob.glob(model_path_deep+'Y*M1[0-1]_40_1000.nc')
m_files = m_files0+m_files1

npp_obs = (cc_data_slice[cc_fall_deep_ind])*npp_conv_o
nit_obs = (r_data[r_fall_deep_ind])*nit_conv
season = 'fall'

npp_list = []
nit_list = []
for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_deep_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_deep_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)


npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

for m_i in m_files:
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    if keyword=='domain':
        savename = season+'_deep_domain'+flier_str
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_deep_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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
##################
# spring all depths
##################
m_files = glob.glob(model_path_all+'*Y*M0[3-5]*.nc')
npp_obs = list((cc_data_slice[cc_spring_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_spring_surf_ind])*npp_conv_o)
nit_obs = list((r_data[r_spring_deep_ind])*nit_conv) + list((r_data[r_spring_surf_ind])*nit_conv)
season = 'spring'

npp_list = []
nit_list = []
for m_i in m_files:
    print(m_i)
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    savename = season+'_all_domain'+flier_str
    if keyword=='domain':
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,:,:])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,:,:])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_all_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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

##################
# summer all depths
####################
m_files = glob.glob(model_path_all+'*Y*M0[6-8]*.nc')
npp_obs = list((cc_data_slice[cc_summer_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_summer_surf_ind])*npp_conv_o)
nit_obs = list((r_data[r_summer_deep_ind])*nit_conv) + list((r_data[r_summer_surf_ind])*nit_conv)
season = 'spring'

npp_list = []
nit_list = []
for m_i in m_files:
    print(m_i)
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    savename = season+'_all_domain'+flier_str
    if keyword=='domain':
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,:,:])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,:,:])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_all_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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
# fall all depths
################
m_files0 = glob.glob(model_path_all+'*Y*M09*.nc')
m_files1 = glob.glob(model_path_all+'*Y*M1[0-1].nc')
m_files = m_files0+m_files1

npp_obs = list((cc_data_slice[cc_fall_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_fall_surf_ind])*npp_conv_o)
nit_obs = list((r_data[r_fall_deep_ind])*nit_conv) + list((r_data[r_fall_surf_ind])*nit_conv)
season = 'fall'

npp_list = []
nit_list = []
for m_i in m_files:
    print(m_i)
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    savename = season+'_all_domain'+flier_str
    if keyword=='domain':
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,:,:])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,:,:])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_all_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

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
# winter all depths
################
m_files0 = glob.glob(model_path_all+'Y*M12*.nc')
m_files1 = glob.glob(model_path_all+'Y*M0[1-2].nc')
m_files = m_files0+m_files1

npp_obs = list((cc_data_slice[cc_winter_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_winter_surf_ind])*npp_conv_o)
#nit_obs = list((r_data[r_winter_deep_ind])*nit_conv) + list((r_data[r_winter_surf_ind])*nit_conv)
season = 'winter'

npp_list = []
nit_list = []
for m_i in m_files:
    print(m_i)
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    savename = season+'_all_domain'+flier_str
    if keyword=='domain':
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,:,:])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,:,:])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_all_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
#nit_plot = [list(nit_obs),list(nit_flat)]
nit_plot = [list(),list(nit_flat)]
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

######################
# all seasons all depths
#######################
m_files = glob.glob(model_path_all+'*Y*.nc')

npp_obs = list((cc_data_slice[cc_winter_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_winter_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_spring_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_spring_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_summer_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_summer_surf_ind])*npp_conv_o)+list((cc_data_slice[cc_fall_deep_ind])*npp_conv_o) + list((cc_data_slice[cc_fall_surf_ind])*npp_conv_o)
#nit_obs = list((r_data[r_winter_deep_ind])*nit_conv) + list((r_data[r_winter_surf_ind])*nit_conv)+list((r_data[r_spring_deep_ind])*nit_conv) + list((r_data[r_spring_surf_ind])*nit_conv)+list((r_data[r_summer_deep_ind])*nit_conv) + list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_deep_ind])*nit_conv) + list((r_data[r_fall_surf_ind])*nit_conv)
nit_obs = list((r_data[r_spring_deep_ind])*nit_conv) + list((r_data[r_spring_surf_ind])*nit_conv)+list((r_data[r_summer_deep_ind])*nit_conv) + list((r_data[r_summer_surf_ind])*nit_conv)+list((r_data[r_fall_deep_ind])*nit_conv) + list((r_data[r_fall_surf_ind])*nit_conv)
season = 'year'

npp_list = []
nit_list = []
for m_i in m_files:
    print(m_i)
    if fliers=='no':
        flier_str = '_nofliers'
    elif fliers=='yes':
        flier_str = ''
    savename = season+'_all_domain'+flier_str
    if keyword=='domain':
        npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,:,:])*npp_conv_m
        npp_sum = np.nansum(npp_nc,axis=0)
        npp_list.append(npp_sum)
        nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,:,:])
        nit_sum = np.nansum(nit_nc,axis=0)
        nit_list.append(nit_sum)
    elif keyword=='loc':
        savename = season+'_all_loc'+flier_str
        for c_i in range(len(cc_x_coord)):
            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][0,:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
            npp_sum = np.nansum(npp_nc,axis=0)
            npp_list.append(npp_sum)
        for r_i in range(len(r_x_coord)):
            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][0,:,r_y_coord[r_i],r_x_coord[r_i]])
            nit_sum = np.nansum(nit_nc,axis=0)
            nit_list.append(nit_sum)

npp_flat = np.array(npp_list).flatten()
npp_flat[npp_flat>1E30] = np.nan
npp_flat[npp_flat<1E-7] = np.nan
npp_flat[npp_flat==0] = np.nan
npp_flat = npp_flat[~np.isnan(npp_flat)]

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-7] = np.nan
nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification')
ax1.set_ylabel('mmol m$^{-3}$ s$^{-1}$')
nit_plot = [list(nit_obs),list(nit_flat)]
#nit_plot = [list(),list(nit_flat)]
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

# uptake rates

