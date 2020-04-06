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
plt.ion()

# cut off depth
d_e_cc = 100
d_e_r = 500

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
model_path_all = './extract_zslice/'

fig_path = './npp_nitrif_figs/'

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

# data variable
cc_data_var = np.array((text_file.iloc[:,cc_num][cc_loc_ind]))

cc_t_ind = np.where(~np.isnan(cc_data_var))[0]
cc_data_slice = cc_data_var[cc_t_ind]
cc_data_lat = cc_lat[cc_t_ind]
cc_data_lon = cc_lon[cc_t_ind]
cc_loc_u = np.unique(np.array((cc_data_lat,cc_data_lon)).transpose(),axis=0)

cc_data_depth = np.array((text_file.iloc[:,19][cc_loc_ind]))[cc_t_ind]


##########
# validationratedata
##########

r_lat = np.array(nitr_rate_df['Lat'])
r_lon = np.array(nitr_rate_df['Lon'])

r_lat_ind = np.where((r_lat>lat_min) & (r_lat<lat_max))[0]
r_lon_ind = np.where((r_lon>lon_min) & (r_lon<lon_max))[0]

r_loc_ind = np.asarray((list(set(r_lat_ind).intersection(r_lon_ind))))

r_depth = np.array(nitr_rate_df['Depth'])[r_loc_ind]
r_data  = np.array(nitr_rate_df['NitrRate'])[r_loc_ind]

r_lat_data = np.array(r_lat[r_loc_ind])
r_lon_data = np.array(r_lon[r_loc_ind])
r_date_data = pd.to_datetime(nitr_rate_df['Date'])[r_loc_ind]

r_loc_u = np.unique(np.array((r_lat_data,r_lon_data)).transpose(),axis=0)

#########################
# statistics and analyses
#########################
# nitrification rate data

# already filtered r_depth/cc_data_depth by location
r_ind = np.where(r_depth<d_e_r)[0]

cc_ind = np.where(cc_data_depth<d_e_cc)[0]

################
# model data and plotting
################
c_conv = 12
n_conv  = 14
sec_day = 86400
npp_conv_m = c_conv # mmol/m3/s to mg C/m2/s
npp_conv_o = (1./sec_day)
#nit_conv = (1./sec_day)*(1./1000) # nmol/L/day to mmol/m3/s
nit_conv_o = (1./sec_day)*(1./1000)*n_conv # nmol/L/day to mg N/m3/s
nit_conv_m = n_conv

h_plot = 9
w_plot = 16

intv0 = 5
intv1 = 95

keyword = 'domain'
fliers = 'no'
axistick = 14

######################
# nitrification 
#######################
m_files = glob.glob(model_path_all+'*Y*_0_'+str(d_e_r)+'.nc')

nit_obs = (r_data[r_ind])*nit_conv_o
season = 'year'

if fliers=='no':
    flier_str = '_nofliers'
elif fliers=='yes':
    flier_str = ''

savename = season+'_'+keyword+'_nitrif_'+str(d_e_r)+'_npp_'+str(d_e_cc)+'_step2'+flier_str

nit_list = []
for m_i in m_files:
    print(m_i)
#    if keyword=='domain':
    nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][::20,:,:])*nit_conv_m
#    nit_sum = np.nanmean(nit_nc,axis=0)
    nit_sum = nit_nc
    nit_list.append(nit_sum)
#    elif keyword=='loc':
#        for r_i in range(len(r_x_coord)):
#            nit_nc = np.array(Dataset(m_i,'r').variables['NITRIF'][:,r_y_coord[r_i],r_x_coord[r_i]])
#            nit_sum = np.nansum(nit_nc,axis=0)
#            nit_list.append(nit_sum)

nit_flat = np.array(nit_list).flatten()
nit_flat[nit_flat>1E30] = np.nan
nit_flat[nit_flat<1E-10] = np.nan
#nit_flat[nit_flat==0] = np.nan
nit_flat = nit_flat[~np.isnan(nit_flat)]

####################
# primary production
####################
#m_files = glob.glob(model_path_all+'*Y*_0_'+str(d_e_cc)+'.nc')
#npp_obs = (cc_data_slice[cc_ind])*npp_conv_o
#
#npp_list = []
#for m_i in m_files:
#    print(m_i)
##    if keyword=='domain':
#    npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][::2,:,:])*npp_conv_m
#    npp_sum = np.nansum(npp_nc,axis=0)
#    npp_list.append(npp_sum)
##    elif keyword=='loc':
##        for c_i in range(len(cc_x_coord)):
##            npp_nc = np.array(Dataset(m_i,'r').variables['TOT_PROD'][:,cc_y_coord[c_i],cc_x_coord[c_i]])*npp_conv_m
##            npp_sum = np.nansum(npp_nc,axis=0)
##            npp_list.append(npp_sum)
#
#npp_flat = np.array(npp_list).flatten()
#npp_flat[npp_flat>1E30] = np.nan
##npp_flat[npp_flat<1E-10] = np.nan
#npp_flat[npp_flat==0] = np.nan
#npp_flat = npp_flat[~np.isnan(npp_flat)]

# box and whisker
fig1,(ax1,ax2) = plt.subplots(1,2,figsize=[w_plot,h_plot])

ax1.set_xlabel('Nitrification',fontsize=axistick)
ax1.set_ylabel('mg N m$^{-3}$ s$^{-1}$',fontsize=axistick)
nit_plot = [nit_obs,nit_flat]
if fliers=='no':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
elif fliers=='yes':
    ax1.boxplot(nit_plot,labels=['observation','model'],whis=[intv0,intv1])

#ax2.set_xlabel('Integrated Primary Production',fontsize=axistick)
#ax2.set_ylabel('mg C m$^{-2}$ s$^{-1}$',fontsize=axistick)
#npp_plot = [npp_obs,npp_flat]
#if fliers=='no':
#    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1],showfliers=False)
#elif fliers=='yes':
#    ax2.boxplot(npp_plot,labels=['observation','model'],whis=[intv0,intv1])

ax1.tick_params(axis='both',which='major',labelsize=axistick)
ax2.tick_params(axis='both',which='major',labelsize=axistick)
ax1.grid(True)
ax2.grid(True)
#plt.savefig(fig_path+savename,bbox_inches='tight')
