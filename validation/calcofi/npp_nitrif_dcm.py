###################################################################
# read calcofi data and other data net primary production and nitrification
# compare to L2 model 1997-2000
# Nov 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
#plt.ion()

# cut off depth
d_e_30 = 30
d_e_40 = 40
d_e_50 = 50

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
cc_chl = 25

# rate data from Karen
rate_name = '/data/project1/minnaho/validation/ValidationRateData_mh.xlsx'
#nitr_rate_df = pd.read_excel(rate_name,sheet_name='Nitrification and nut uptake')
nitr_rate_nc = Dataset('/data/project1/minnaho/validation/bight13/bight13.nc','r')

# model data 2 1997- 9 2000
model_path = './extract_zslice/'

fig_path = './npp_nitrif_figs/'

#npp_dcm_file = '/data/project3/kesf/tools_matlab/applications/pollution/terrestrial/potw/state_of_art/prod_at_dcm.nc'
# integrated NPP at DCM
npp_dcm_file = '/data/project3/kesf/tools_matlab/applications/pollution/terrestrial/potw/bgc_rate/TOT_PROD_int_0_to_100.nc'
nit_dcm_file = '/data/project3/kesf/tools_matlab/applications/pollution/terrestrial/potw/state_of_art/nitrif_at_dcm.nc'

# choose years
yr_s = 1999
yr_e = 2000

# calcofi convert datetime numbers to dates
cc_time_num = np.array((text_file.iloc[:,1]))
cc_date_conv = num2date(cc_time_num,time_unit)


st_dt = num2date(0,'days since 1999-9-01')
en_dt = num2date(0,'days since 2000-9-30')
# get indexes of target years
print('getting indices of target years')
cc_yr_ind_l = []
for ind_d,d_i in enumerate(cc_date_conv):
    if d_i < en_dt and d_i > st_dt:
        cc_yr_ind_l.append(ind_d) 

# get all data instead
#cc_yr_ind = np.array((cc_yr_ind_l))
cc_yr_ind = np.arange(cc_date_conv.shape[0])

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
cc_data_chl = np.array((text_file.iloc[:,cc_chl][cc_data_ind]))

cc_t_ind = np.where(~np.isnan(cc_data_var))[0]
cc_data_slice_nondcm = cc_data_var[cc_t_ind]
cc_data_slice_chl = cc_data_chl[cc_t_ind]

cc_data_lat_nondcm = cc_lat[cc_data_ind][cc_t_ind]
cc_data_lon_nondcm = cc_lon[cc_data_ind][cc_t_ind]
cc_loc_u_nondcm = np.unique(np.array((cc_data_lat_nondcm,cc_data_lon_nondcm)).transpose(),axis=0)

cc_data_depth_nondcm = np.array((text_file.iloc[:,19][cc_data_ind]))[cc_t_ind]
cc_data_date_nondcm = cc_date_conv[cc_data_ind][cc_t_ind]

# find where depth = 0 to find dcm
cc_depth_0_ind = np.where(cc_data_depth_nondcm==0)[0]

# new data set of just npp dcm data
npp_depth_dcm_l = []
npp_dcm_l = []
npp_lat_dcm_l = []
npp_lon_dcm_l = []
npp_date_dcm_l = []
for chl_i in range(len(cc_depth_0_ind)-1):
    d_ind = np.where(cc_data_slice_chl[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]]==np.nanmax(cc_data_slice_chl[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]]))[0][0]
    npp_depth_dcm_l.append(cc_data_depth_nondcm[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]][d_ind])
    npp_dcm_l.append(cc_data_slice_nondcm[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]][d_ind])
    npp_lat_dcm_l.append(cc_data_lat_nondcm[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]][d_ind])
    npp_lon_dcm_l.append(cc_data_lon_nondcm[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]][d_ind])
    npp_date_dcm_l.append(cc_data_date_nondcm[cc_depth_0_ind[chl_i]:cc_depth_0_ind[chl_i+1]][d_ind])

# npp bight13 data
bight_nc = Dataset('/data/project1/minnaho/validation/bight13/bight13.nc','r')
bight_d = np.array(bight_nc.variables['depth'])
bight_npp_ind = np.where(~np.isnan(bight_nc.variables['NPP_rate']))[0]

bight_t = num2date(np.array(bight_nc.variables['time']),bight_nc.variables['time'].units)[bight_npp_ind]
bight_dcm_depth = bight_d[bight_npp_ind]
bight_data_npp  = np.array(bight_nc.variables['NPP_rate'])[bight_npp_ind]
bight_lat = np.array(bight_nc.variables['latitude'])[bight_npp_ind]
bight_lon = np.array(bight_nc.variables['longitude'])[bight_npp_ind]

bight_loc_u = np.unique(np.array((bight_lat,bight_lon)).transpose(),axis=0)

# incorporate with calcofi data
cc_data_depth = np.concatenate((np.array(npp_depth_dcm_l),bight_dcm_depth))
cc_data_slice = np.concatenate((np.array(npp_dcm_l),bight_data_npp))
cc_data_lat = np.concatenate((np.array(npp_lat_dcm_l),bight_lat))
cc_data_lon = np.concatenate((np.array(npp_lon_dcm_l),bight_lon))
cc_data_date = np.concatenate((np.array(npp_date_dcm_l),bight_t))

cc_loc_u = np.concatenate((np.unique(np.array((cc_data_lat,cc_data_lon)).transpose(),axis=0),bight_loc_u),axis=0)
 
# find calcofi locations
#cc_x_coord = np.empty((len(cc_loc_u)))
#cc_y_coord = np.empty((len(cc_loc_u)))
#for l_i in range(len(cc_loc_u)):
#    min_l = np.abs( (lat_nc - cc_loc_u[l_i][0])**2 + (lon_nc - cc_loc_u[l_i][1])**2)
#    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
#    cc_x_coord[l_i] = x_site
#    cc_y_coord[l_i] = y_site


#plt.figure()
#plt.imshow(mask_nc,origin='lower')
#plt.scatter(cc_x_coord,cc_y_coord)


##########
# validationratedata and bight13
##########

r_lat = np.array(nitr_rate_nc.variables['latitude'])
r_lon = np.array(nitr_rate_nc.variables['longitude'])

r_lat_ind = np.where((r_lat>lat_min) & (r_lat<lat_max))[0]
r_lon_ind = np.where((r_lon>lon_min) & (r_lon<lon_max))[0]

r_loc_ind = np.asarray((list(set(r_lat_ind).intersection(r_lon_ind))))
#r_data_ind = np.asarray(sorted((list(set(r_loc_ind).intersection(rate_yr_ind)))))

r_depth = np.array(nitr_rate_nc.variables['depth'])[r_loc_ind]
# r npp rate data only at deep chlorophyll maximum
r_npp_ind = np.where(~np.isnan(nitr_rate_nc.variables['NPP_rate'][r_loc_ind]))[0]
r_dcm_depth = r_depth[r_npp_ind]
r_data_npp  = np.array(nitr_rate_nc.variables['NPP_rate'])[r_npp_ind]
r_data_nit  = np.array(nitr_rate_nc.variables['nitr_rate'])[r_npp_ind]

r_lat_data = np.array(r_lat[r_npp_ind])
r_lon_data = np.array(r_lon[r_npp_ind])
r_date_data = num2date(np.array(nitr_rate_nc.variables['time']),nitr_rate_nc.variables['time'].units)[r_npp_ind]
#r_date_data = pd.to_datetime(nitr_rate_df['Date'])[r_loc_ind]

r_loc_u = np.unique(np.array((r_lat_data,r_lon_data)).transpose(),axis=0)

# find rate data locations
r_x_coord = np.empty((len(r_loc_u)))
r_y_coord = np.empty((len(r_loc_u)))
for l_i in range(len(r_loc_u)):
    min_l = np.abs( (lat_nc - r_loc_u[l_i][0])**2 + (lon_nc - r_loc_u[l_i][1])**2)
    y_site, x_site = np.unravel_index(min_l.argmin(), min_l.shape)
    r_x_coord[l_i] = x_site
    r_y_coord[l_i] = y_site

# check if any latitudes from r data set matches with cc data set
# check_lat = 0 if no latitudes match
check_lat = np.sum(r_lat_data[:min(len(r_lat_data), len(cc_data_lat))] == cc_data_lat[:min(len(r_lat_data), len(cc_data_lat))])

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
axistick = 14

nit_cmap = 'gnuplot'
npp_cmap = 'viridis'

axis_tick_size = 14
axis_font = 16
m_size = 200

min_c = 0
max_c = 0.004

min_r = 0
max_r = 10E-6

# basemap
lat_mean = np.mean(lat_nc)
lon_mean = np.mean(lon_nc)

parallels = np.arange(0,90,1)
meridians = np.arange(180,360,1)

################
# plotting
################
# observation data
num_vars_c = [
cc_spring_ind,
cc_summer_ind,
cc_winter_ind,
cc_fall_ind]

num_vars_r = [
r_spring_ind,
r_summer_ind,
r_winter_ind,
r_fall_ind]

npp_list = []
nit_list = []

for n_i in range(len(num_vars_c)):
    fig1,axes1 = plt.subplots(1,2,figsize=[w_plot,h_plot])
    fig2,axes2 = plt.subplots(1,2,figsize=[w_plot,h_plot])
    # observation data
    if num_vars_c[n_i].shape[0]==0:
        npp_obs = []
        lat_c = []
        lon_c = []
    else:
        npp_obs = []
        lat_c = []
        lon_c = []
        lat_temp = cc_data_lat[num_vars_c[n_i]]
        lon_temp = cc_data_lon[num_vars_c[n_i]]
        # get average value at each location and depth range
        for l_c in range(len(cc_loc_u)):
            loc_c = np.where((lat_temp==cc_loc_u[l_c][0])&(lon_temp==cc_loc_u[l_c][1]))[0]
            npp_app = np.nanmean(cc_data_slice[num_vars_c[n_i]][loc_c]*npp_conv_o)
            npp_obs.append(npp_app)
            lat_c.append(cc_loc_u[l_c][0])
            lon_c.append(cc_loc_u[l_c][1])
        #npp_obs = (cc_data_slice[num_vars_c[n_i]])*npp_conv_o 
    map_ax1 = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes1[0]) 
    x,y = map_ax1(lon_c,lat_c)
    npp_plot_o = map_ax1.scatter(x,y,c=npp_obs,cmap=npp_cmap,marker='o',s=m_size)
    map_ax1.drawcoastlines()
    map_ax1.drawstates()
    map_ax1.drawcountries()
    map_ax1.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    map_ax1.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)

    if num_vars_r[n_i].shape[0]==0:
        nit_obs = []
        lat_r = []
        lon_r = []
    else:
        nit_obs = []
        lat_r = []
        lon_r = []
        lat_temp = r_lat_data[num_vars_r[n_i]]
        lon_temp = r_lon_data[num_vars_r[n_i]]
        # get average value at each location and depth range
        for l_r in range(len(r_loc_u)):
            loc_r = np.where((lat_temp==r_loc_u[l_r][0])&(lon_temp==r_loc_u[l_r][1]))[0]
            nit_app = np.nanmean(r_data_nit[num_vars_r[n_i]][loc_r]*nit_conv_o)
            nit_obs.append(nit_app)
            lat_r.append(r_loc_u[l_r][0])
            lon_r.append(r_loc_u[l_r][1])

    map_ax2 = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes2[0]) 
    x,y = map_ax2(lon_r,lat_r)
    nit_plot_o = map_ax2.scatter(x,y,c=nit_obs,cmap=nit_cmap,marker='o',s=m_size)
    map_ax2.drawcoastlines()
    map_ax2.drawstates()
    map_ax2.drawcountries()
    map_ax2.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    map_ax2.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    
    # model data
    # spring
    if n_i==0:     
        season = 'spring'
        month_ind = [37,38,39]
    # summer
    if n_i==1:     
        season = 'summer'
        month_ind = [40,41,42]
    # winter
    if n_i==2:     
        season = 'winter'
        month_ind = [34,35,36]
    # fall
    if n_i==3:     
        season = 'fall'
        month_ind = [31,32,33,43]

    print(season)
    npp_nc = np.nanmean(np.array(Dataset(npp_dcm_file,'r').variables['TOT_PROD'][month_ind,:,:]),axis=0)*npp_conv_m
    nit_nc = np.nanmean(np.array(Dataset(nit_dcm_file,'r').variables['nitrif_at_dcm'][month_ind,:,:]),axis=0)*nit_conv_m
    
    npp_flat = npp_nc
    npp_flat[npp_flat>1E30] = np.nan
    #npp_flat[npp_flat<1E-7] = np.nan
    npp_flat[npp_flat==0] = np.nan
    #npp_flat = npp_flat[~np.isnan(npp_flat)]
    map_ax3 = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes1[1]) 
    x,y = map_ax3(lon_nc,lat_nc)
    if npp_plot_o.get_clim()[0]!=None:
        vmin_npp_o = npp_plot_o.get_clim()[0]
        vmax_npp_o = npp_plot_o.get_clim()[1]
        npp_plot_m = map_ax3.pcolor(x,y,npp_flat,cmap=npp_cmap,vmin=vmin_npp_o,vmax=vmax_npp_o)
    else: 
        npp_plot_m = map_ax3.pcolor(x,y,npp_flat,cmap=npp_cmap)
    
    nit_flat = nit_nc
    nit_flat[nit_flat>1E30] = np.nan
    #nit_flat[nit_flat<1E-7] = np.nan
    nit_flat[nit_flat==0] = np.nan
    #nit_flat = nit_flat[~np.isnan(nit_flat)]
    map_ax4 = Basemap(projection='stere',resolution='h',lat_0=lat_mean,lon_0=lon_mean,llcrnrlat=lat_min,urcrnrlat=lat_max,llcrnrlon=lon_min,urcrnrlon=lon_max,ax=axes2[1]) 
    x,y = map_ax4(lon_nc,lat_nc)
    if nit_plot_o.get_clim()[0]!=None:
        vmin_nit_o = nit_plot_o.get_clim()[0]
        vmax_nit_o = nit_plot_o.get_clim()[1]
        nit_plot_m = map_ax4.pcolor(x,y,nit_flat,cmap=nit_cmap,vmin=vmin_nit_o,vmax=vmax_nit_o)
    else: 
        nit_plot_m = map_ax4.pcolor(x,y,nit_flat,cmap=nit_cmap)

    map_ax3.drawcoastlines()
    map_ax3.drawstates()
    map_ax3.drawcountries()
    map_ax3.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    map_ax3.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    map_ax4.drawcoastlines()
    map_ax4.drawstates()
    map_ax4.drawcountries()
    map_ax4.drawparallels(parallels,labels=[1,0,0,0],fontsize=axis_tick_size)
    map_ax4.drawmeridians(meridians,labels=[0,0,0,1],fontsize=axis_tick_size)
    # colorbar
    p1 = axes1[0].get_position().get_points().flatten()
    p2 = axes1[1].get_position().get_points().flatten()
    cb_ax1 = fig1.add_axes([p2[2]+0.02,p1[1],0.01,p1[3]-p1[1]])
    cb1 = fig1.colorbar(npp_plot_m,cax=cb_ax1,orientation='vertical')
    cb1.set_label('mg C m$^{-2}$ s$^{-1}$',fontsize=axis_font)
    cb1.ax.tick_params(labelsize=axis_tick_size)
    cb1.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    cb1.ax.tick_params(axis='both',which='minor',labelsize=axis_tick_size)

    p3 = axes2[0].get_position().get_points().flatten()
    p4 = axes2[1].get_position().get_points().flatten()
    cb_ax2 = fig2.add_axes([p4[2]+0.02,p3[1],0.01,p3[3]-p3[1]])
    cb2 = fig2.colorbar(nit_plot_m,cax=cb_ax2,orientation='vertical')
    cb2.set_label('mg N m$^{-3}$ s$^{-1}$',fontsize=axis_font)
    cb2.ax.tick_params(labelsize=axis_tick_size)
    cb2.ax.tick_params(axis='both',which='major',labelsize=axis_tick_size)
    cb2.ax.tick_params(axis='both',which='minor',labelsize=axis_tick_size)
    
    savename1 = fig_path+'npp_'+season+'_dcm_alltime'
    savename2 = fig_path+'nit_'+season+'_dcm_alltime'
    
    fig1.savefig(savename1,bbox_inches='tight')
    fig2.savefig(savename2,bbox_inches='tight')
    plt.close('all')
