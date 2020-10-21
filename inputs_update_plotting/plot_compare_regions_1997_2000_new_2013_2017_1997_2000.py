import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pandas as pd

fig_path = './figs/'
# data paths

potw_major_path_old = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/major_potw_data.nc'
potw_major_path_new = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'

potw_minor_path_old = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/minor_potw_data_new.nc'
potw_minor_path_new = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

############
# load grid
############
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

# mask that is first 0-15km offshore
mask_mat = scipy.io.loadmat('../maskt.mat')['maskt'] 

# regions
# south sd, north sd, oc, sp, sm, v, sb
j_locs = np.array((164,264,500,610,740,948))
maskarr = np.zeros((len(j_locs)+1,mask_nc.shape[0],mask_nc.shape[1]))
maskarr[0,:j_locs[0],:] = 1
maskarr[1,j_locs[0]:j_locs[1],:] = 1
maskarr[2,j_locs[1]:j_locs[2],:] = 1
maskarr[3,j_locs[2]:j_locs[3],:] = 1
maskarr[4,j_locs[3]:j_locs[4],:] = 1
maskarr[5,j_locs[4]:j_locs[5],:] = 1
maskarr[6,j_locs[5]:,:] = 1

maskarr[maskarr==0] = np.nan

# uncomment to see masks plotted
#colors = ['spring','viridis_r','gray','rainbow','gnuplot_r','seismic','Greens_r']
#plt.ion()
#for i in range(len(maskarr)):
#    plt.imshow(maskarr[i]*mask_nc,cmap=colors[i],origin='lower')

'''
#maskscb = total domain
#maskt = total coast; 
#maskla: great los angeles ; 
#maskocd = oceanside-carlsbad, called north san diego ; 
#maskocs = south orange county ; 
#masksb= santa barbara ; 
#masksd = south sandiego ; 
#masksm= santa monica ; 
#masksp= san pedro shelf ; 
#maskv = ventura ; 
region_mask = h5py.File('/data/project3/minnaho/Nexport_paper/mask.mat','r')['mask']

# array of 7 regional masks
maskarr = np.empty((7,region_mask['maskla'].shape[1],region_mask['maskla'].shape[0]))
maskarr[0,:,:] = np.transpose(region_mask['masksb'])
maskarr[1,:,:] = np.transpose(region_mask['maskv'])
maskarr[2,:,:] = np.transpose(region_mask['masksm'])
maskarr[3,:,:] = np.transpose(region_mask['masksp'])
maskarr[4,:,:] = np.transpose(region_mask['maskocs'])
maskarr[5,:,:] = np.transpose(region_mask['maskocd'])
maskarr[6,:,:] = np.transpose(region_mask['masksd'])
'''


######################
# potw
######################
potw_ma_nc_old = Dataset(potw_major_path_old,'r')
potw_ma_nc_new = Dataset(potw_major_path_new,'r')

major_potw_time_old = num2date(np.array(potw_ma_nc_old.variables['time']),potw_ma_nc_old.variables['time'].units,only_use_cftime_datetimes=False)
# start and end indices of potw for 1997-2000
potw_1997 = 313 # 1997-01-31
potw_2013 = 361 # 2001-01-01

major_potw_time_new = num2date(np.array(potw_ma_nc_new.variables['time']),potw_ma_nc_new.variables['time'].units,only_use_cftime_datetimes=False)
# start and end indices of potw for 1997-2000
potn_2013 = 504 # 2013-01-31
potn_2017 = major_potw_time_new.shape[0] # 2017-12-31

potn_1997 = 312
potn_2000 = 360

major_potw_time_dt_old = np.array(major_potw_time_old[potw_1997:potw_2013])
major_potw_time_dt_new = np.array(major_potw_time_new[potn_2013:potn_2017])

major_potw_lat = np.array(potw_ma_nc_old.variables['latitude'])
major_potw_lon = np.array(potw_ma_nc_old.variables['longitude'])

p_coord_i = []
p_coord_j = []
for coord in range(len(major_potw_lat)):
    lat_you_want = major_potw_lat[coord]
    lon_you_want = major_potw_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    p_coord_i.append(xi_coord)
    p_coord_j.append(eta_coord)

# make list of lists because each sublist will have different length
p_major_ind = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(major_potw_lat)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,p_coord_j[r_i],p_coord_i[r_i]] == 1:
            p_major_ind[m_i].append(r_i)

# divide flows
major_flo_old = np.array(potw_ma_nc_old.variables['flow']) # m3/s
major_nh4_old = np.array(potw_ma_nc_old.variables['NH4']) # mmol/m3
major_no3_old = np.array(potw_ma_nc_old.variables['NO3']) # mmol/m3
major_no2_old = np.array(potw_ma_nc_old.variables['NO2']) # mmol/m3
major_onn_old = np.array(potw_ma_nc_old.variables['ON']) # mmol/m3

major_nh4_old[major_nh4_old>1E10] == np.nan
major_no3_old[major_no3_old>1E10] == np.nan
major_no2_old[major_no2_old>1E10] == np.nan

major_din_old = np.nansum((major_nh4_old,major_no3_old,major_no2_old),axis=0)
major_tn_old = np.nansum((major_nh4_old,major_no3_old,major_no2_old,major_onn_old),axis=0)

major_flo_old[major_flo_old>1E20] = np.nan
major_tn_old[major_tn_old>1E20] = np.nan
major_din_old[major_din_old>1E20] = np.nan

p_major_flo_old = [[] for i in range(maskarr.shape[0])]
p_major_din_old = [[] for i in range(maskarr.shape[0])] # DIN flux
p_major_tn_old = [[] for i in range(maskarr.shape[0])] 
for r_i in range(len(p_major_ind)):
    p_major_flo_old[r_i].append(np.transpose(major_flo_old[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn_old[r_i].append(np.transpose(major_flo_old[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tn_old[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_din_old[r_i].append(np.transpose(major_flo_old[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_din_old[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())

# divide flows
major_flo_new = np.array(potw_ma_nc_new.variables['flow']) # m3/s
major_nh4_new = np.array(potw_ma_nc_new.variables['NH4']) # mmol/m3
major_no3_new = np.array(potw_ma_nc_new.variables['NO3']) # mmol/m3
major_no2_new = np.array(potw_ma_nc_new.variables['NO2']) # mmol/m3
major_onn_new = np.array(potw_ma_nc_new.variables['organic_N']) # mmol/m3

major_nh4_new[major_nh4_new>1E10] == np.nan
major_no3_new[major_no3_new>1E10] == np.nan
major_no2_new[major_no2_new>1E10] == np.nan

major_din_new = np.nansum((major_nh4_new,major_no3_new,major_no2_new),axis=0)
major_tn_new = np.nansum((major_nh4_new,major_no3_new,major_no2_new,major_onn_new),axis=0)

major_flo_new[major_flo_new>1E20] = np.nan
major_tn_new[major_tn_new>1E20] = np.nan
major_din_new[major_din_new>1E20] = np.nan

p_major_flo_new = [[] for i in range(maskarr.shape[0])]
p_major_flo_new19 = [[] for i in range(maskarr.shape[0])]
p_major_din_new = [[] for i in range(maskarr.shape[0])] # DIN flux
p_major_din_new19 = [[] for i in range(maskarr.shape[0])] # DIN flux
p_major_tn_new = [[] for i in range(maskarr.shape[0])] 
for r_i in range(len(p_major_ind)):
    p_major_flo_new[r_i].append(np.transpose(major_flo_new[potn_2013:potn_2017,p_major_ind[r_i]]).tolist())
    p_major_flo_new19[r_i].append(np.transpose(major_flo_new[potn_1997:potn_2000,p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn_new[r_i].append(np.transpose(major_flo_new[potn_2013:potn_2017,p_major_ind[r_i]]*major_tn_new[potn_2013:potn_2017,p_major_ind[r_i]]).tolist())
    p_major_din_new[r_i].append(np.transpose(major_flo_new[potn_2013:potn_2017,p_major_ind[r_i]]*major_din_new[potn_2013:potn_2017,p_major_ind[r_i]]).tolist())
    p_major_din_new19[r_i].append(np.transpose(major_flo_new[potn_1997:potn_2000,p_major_ind[r_i]]*major_din_new[potn_1997:potn_2000,p_major_ind[r_i]]).tolist())

# turn to array so can sum all potw in region up
# then reshape to (4,12) because this data set is 4 years 1997-2000
# then average over 4 years to get year average
ry0 = 4

#p_major_flo_nsd = np.nanmean(np.nansum(np.array(p_major_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ssd_old = np.nanmean(np.nansum(np.array(p_major_flo_old[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_nsd_old = np.zeros((12))
p_major_flo_occ_old = np.nanmean(np.nansum(np.array(p_major_flo_old[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_spp_old = np.nanmean(np.nansum(np.array(p_major_flo_old[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_smm_old = np.nanmean(np.nansum(np.array(p_major_flo_old[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ven_old = np.zeros((12))
p_major_flo_sbb_old = np.zeros((12))
#p_major_flo_ven = np.nanmean(np.nansum(np.array(p_major_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_flo_sbb = np.nanmean(np.nansum(np.array(p_major_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_tnn_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ssd_old = np.nanmean(np.nansum(np.array(p_major_tn_old[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_nsd_old = np.zeros((12))
p_major_tnn_occ_old = np.nanmean(np.nansum(np.array(p_major_tn_old[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_spp_old = np.nanmean(np.nansum(np.array(p_major_tn_old[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_smm_old = np.nanmean(np.nansum(np.array(p_major_tn_old[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ven_old = np.zeros((12))
p_major_tnn_sbb_old = np.zeros((12))
#p_major_tnn_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_tnn_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_din_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ssd_old = np.nanmean(np.nansum(np.array(p_major_din_old[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_nsd_old = np.zeros((12))
p_major_din_occ_old = np.nanmean(np.nansum(np.array(p_major_din_old[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_spp_old = np.nanmean(np.nansum(np.array(p_major_din_old[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_smm_old = np.nanmean(np.nansum(np.array(p_major_din_old[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ven_old = np.zeros((12))
p_major_din_sbb_old = np.zeros((12))
#p_major_din_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_din_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)


# turn to array so can sum all potw in region up
# then reshape to (5,12) because this data set is 5 years 2013-2017
# then average over 5 years to get year average
ry0 = 5

#p_major_flo_nsd = np.nanmean(np.nansum(np.array(p_major_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ssd_new = np.nanmean(np.nansum(np.array(p_major_flo_new[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_nsd_new = np.zeros((12))
p_major_flo_occ_new = np.nanmean(np.nansum(np.array(p_major_flo_new[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_spp_new = np.nanmean(np.nansum(np.array(p_major_flo_new[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_smm_new = np.nanmean(np.nansum(np.array(p_major_flo_new[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ven_new = np.zeros((12))
p_major_flo_sbb_new = np.zeros((12))
#p_major_flo_ven = np.nanmean(np.nansum(np.array(p_major_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_flo_sbb = np.nanmean(np.nansum(np.array(p_major_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_tnn_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ssd_new = np.nanmean(np.nansum(np.array(p_major_tn_new[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_nsd_new = np.zeros((12))
p_major_tnn_occ_new = np.nanmean(np.nansum(np.array(p_major_tn_new[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_spp_new = np.nanmean(np.nansum(np.array(p_major_tn_new[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_smm_new = np.nanmean(np.nansum(np.array(p_major_tn_new[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ven_new = np.zeros((12))
p_major_tnn_sbb_new = np.zeros((12))
#p_major_tnn_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_tnn_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_din_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ssd_new = np.nanmean(np.nansum(np.array(p_major_din_new[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_nsd_new = np.zeros((12))
p_major_din_occ_new = np.nanmean(np.nansum(np.array(p_major_din_new[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_spp_new = np.nanmean(np.nansum(np.array(p_major_din_new[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_smm_new = np.nanmean(np.nansum(np.array(p_major_din_new[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ven_new = np.zeros((12))
p_major_din_sbb_new = np.zeros((12))
#p_major_din_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_din_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)

# turn to array so can sum all potw in region up
# then reshape to (5,12) because this data set is 5 years 2013-2017
# then average over 5 years to get year average
ry0 = 4

#p_major_flo_nsd = np.nanmean(np.nansum(np.array(p_major_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ssd_new19 = np.nanmean(np.nansum(np.array(p_major_flo_new19[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_nsd_new19 = np.zeros((12))
p_major_flo_occ_new19 = np.nanmean(np.nansum(np.array(p_major_flo_new19[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_spp_new19 = np.nanmean(np.nansum(np.array(p_major_flo_new19[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_smm_new19 = np.nanmean(np.nansum(np.array(p_major_flo_new19[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ven_new19 = np.zeros((12))
p_major_flo_sbb_new19 = np.zeros((12))
#p_major_flo_ven = np.nanmean(np.nansum(np.array(p_major_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_flo_sbb = np.nanmean(np.nansum(np.array(p_major_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_din_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ssd_new19 = np.nanmean(np.nansum(np.array(p_major_din_new19[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_nsd_new19 = np.zeros((12))
p_major_din_occ_new19 = np.nanmean(np.nansum(np.array(p_major_din_new19[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_spp_new19 = np.nanmean(np.nansum(np.array(p_major_din_new19[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_smm_new19 = np.nanmean(np.nansum(np.array(p_major_din_new19[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_din_ven_new19 = np.zeros((12))
p_major_din_sbb_new19 = np.zeros((12))
#p_major_din_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_din_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)


##############
# minor potw
##############
# multiply masks by 0-15km mask to exclude island minor potws
for j_i in range(maskarr.shape[0]):
    maskarr[j_i] = maskarr[j_i]*mask_mat

potw_mi_nc_old = Dataset(potw_minor_path_old,'r')
potw_mi_nc_new = Dataset(potw_minor_path_new,'r')

minor_potw_time_new = num2date(np.array(potw_mi_nc_new.variables['time']),potw_mi_nc_new.variables['time'].units,only_use_cftime_datetimes=False)

minor_potw_lat_old = np.array(potw_mi_nc_old.variables['latitude'])
minor_potw_lon_old = np.array(potw_mi_nc_old.variables['longitude'])

minor_potw_lat_new = np.array(potw_mi_nc_new.variables['latitude'])
minor_potw_lon_new = np.array(potw_mi_nc_new.variables['longitude'])

p_coord_i_old = []
p_coord_j_old = []
for coord in range(len(minor_potw_lat_old)):
    lat_you_want = minor_potw_lat_old[coord]
    lon_you_want = minor_potw_lon_old[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    p_coord_i_old.append(xi_coord)
    p_coord_j_old.append(eta_coord)

p_coord_i_new = []
p_coord_j_new = []
for coord in range(len(minor_potw_lat_new)):
    lat_you_want = minor_potw_lat_new[coord]
    lon_you_want = minor_potw_lon_new[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    p_coord_i_new.append(xi_coord)
    p_coord_j_new.append(eta_coord)


# make list of lists because each sublist will have different length
p_minor_ind_old = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(minor_potw_lat_old)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,p_coord_j_old[r_i],p_coord_i_old[r_i]] == 1:
            p_minor_ind_old[m_i].append(r_i)

p_minor_ind_isl_old = [1,5]

# make list of lists because each sublist will have different length
p_minor_ind_new = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(minor_potw_lat_new)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,p_coord_j_new[r_i],p_coord_i_new[r_i]] == 1:
            p_minor_ind_new[m_i].append(r_i)

p_minor_ind_isl_new = [1,12]

minor_flo_old = np.array(potw_mi_nc_old.variables['flow']) # m3/s
minor_nh4_old = np.array(potw_mi_nc_old.variables['NH4']) # mmol/m3
minor_no3_old = np.array(potw_mi_nc_old.variables['NO3']) # mmol/m3
minor_no2_old = np.array(potw_mi_nc_old.variables['NO2']) # mmol/m3

minor_nh4_old[minor_nh4_old>1E10] = np.nan
minor_no3_old[minor_no3_old>1E10] = np.nan
minor_no2_old[minor_no2_old>1E10] = np.nan

# minor TN same as DIN
minor_tn_old = np.nansum((minor_no3_old,minor_nh4_old,minor_no2_old),axis=0)

minor_flo_old[minor_flo_old>1E20] = np.nan
minor_tn_old[minor_tn_old>1E20] = np.nan

minor_flo_new = np.array(potw_mi_nc_new.variables['flow']) # m3/s
minor_nh4_new = np.array(potw_mi_nc_new.variables['NH4']) # mmol/m3
minor_no3_new = np.array(potw_mi_nc_new.variables['NO3']) # mmol/m3
minor_no2_new = np.array(potw_mi_nc_new.variables['NO2']) # mmol/m3

minor_nh4_new[minor_nh4_new>1E10] = np.nan
minor_no3_new[minor_no3_new>1E10] = np.nan
minor_no2_new[minor_no2_new>1E10] = np.nan

# minor TN same as DIN
minor_tn_new = np.nansum((minor_no3_new,minor_nh4_new,minor_no2_new),axis=0)

minor_flo_new[minor_flo_new>1E20] = np.nan
minor_tn_new[minor_tn_new>1E20] = np.nan

p_minor_flo_old = [[] for i in range(maskarr.shape[0])]
p_minor_tn_old = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(p_minor_ind_old)):
    p_minor_flo_old[r_i].append(np.transpose(minor_flo_old[:12,p_minor_ind_old[r_i],p_minor_ind_old[r_i]]).tolist())
    p_minor_tn_old[r_i].append(np.transpose(minor_flo_old[:12,p_minor_ind_old[r_i],p_minor_ind_old[r_i]]*minor_tn_old[:12,p_minor_ind_old[r_i],p_minor_ind_old[r_i]]).tolist())

p_minor_tn_isl_old = np.nanmean(np.nansum(np.transpose(minor_flo_old[:12,p_minor_ind_isl_old,p_minor_ind_isl_old]*minor_tn_old[:12,p_minor_ind_isl_old,p_minor_ind_isl_old]),axis=0))*s_to_d*g_N*g_to_kg*mmol_to_mol

p_minor_flo_new = [[] for i in range(maskarr.shape[0])]
p_minor_tn_new = [[] for i in range(maskarr.shape[0])]
p_minor_flo_new19 = [[] for i in range(maskarr.shape[0])]
p_minor_tn_new19 = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(p_minor_ind_new)):
    p_minor_flo_new[r_i].append(np.transpose(minor_flo_new[-60:,p_minor_ind_new[r_i]]).tolist())
    p_minor_tn_new[r_i].append(np.transpose(minor_flo_new[-60:,p_minor_ind_new[r_i]]*minor_tn_new[-60:,p_minor_ind_new[r_i]]).tolist())
    p_minor_flo_new19[r_i].append(np.transpose(minor_flo_new[0:48,p_minor_ind_new[r_i]]).tolist())
    p_minor_tn_new19[r_i].append(np.transpose(minor_flo_new[0:48,p_minor_ind_new[r_i]]*minor_tn_new[0:48,p_minor_ind_new[r_i]]).tolist())

p_minor_tn_isl_new = np.nanmean(np.nansum(np.transpose(minor_flo_new[-60:,p_minor_ind_isl_new]*minor_tn_new[-60:,p_minor_ind_isl_new]),axis=0))*s_to_d*g_N*g_to_kg*mmol_to_mol
p_minor_tn_isl_new19 = np.nanmean(np.nansum(np.transpose(minor_flo_new[:48,p_minor_ind_isl_new]*minor_tn_new[:48,p_minor_ind_isl_new]),axis=0))*s_to_d*g_N*g_to_kg*mmol_to_mol

# turn to array so can sum all minor potw in region up
p_minor_flo_ssd_old = np.nansum(np.array(p_minor_flo_old[0][0]),axis=0)
p_minor_flo_nsd_old = np.nansum(np.array(p_minor_flo_old[1][0]),axis=0)
p_minor_flo_occ_old = np.nansum(np.array(p_minor_flo_old[2][0]),axis=0)
p_minor_flo_spp_old = np.nansum(np.array(p_minor_flo_old[3][0]),axis=0)
p_minor_flo_smm_old = np.nansum(np.array(p_minor_flo_old[4][0]),axis=0)
p_minor_flo_ven_old = np.nansum(np.array(p_minor_flo_old[5][0]),axis=0)
p_minor_flo_sbb_old = np.nansum(np.array(p_minor_flo_old[6][0]),axis=0)

p_minor_tnn_ssd_old = np.nansum(np.array(p_minor_tn_old[0][0]),axis=0)
p_minor_tnn_nsd_old = np.nansum(np.array(p_minor_tn_old[1][0]),axis=0)
p_minor_tnn_occ_old = np.nansum(np.array(p_minor_tn_old[2][0]),axis=0)
p_minor_tnn_spp_old = np.nansum(np.array(p_minor_tn_old[3][0]),axis=0)
p_minor_tnn_smm_old = np.nansum(np.array(p_minor_tn_old[4][0]),axis=0)
p_minor_tnn_ven_old = np.nansum(np.array(p_minor_tn_old[5][0]),axis=0)
p_minor_tnn_sbb_old = np.nansum(np.array(p_minor_tn_old[6][0]),axis=0)

ryi = 5
p_minor_flo_ssd_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[0][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_nsd_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[1][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_occ_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[2][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_spp_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[3][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_smm_new = np.zeros((12))
#p_minor_flo_smm_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[4][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_ven_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[5][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_sbb_new = np.nanmean(np.nansum(np.array(p_minor_flo_new[6][0]),axis=0).reshape(ryi,12),axis=0)

p_minor_tnn_ssd_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[0][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_nsd_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[1][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_occ_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[2][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_spp_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[3][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_smm_new = np.zeros((12))
#p_minor_tnn_smm_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[4][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_ven_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[5][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_sbb_new = np.nanmean(np.nansum(np.array(p_minor_tn_new[6][0]),axis=0).reshape(ryi,12),axis=0)

ryi = 4
p_minor_flo_ssd_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[0][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_nsd_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[1][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_occ_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[2][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_spp_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[3][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_smm_new19 = np.zeros((12))
#p_minor_flo_smm_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[4][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_ven_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[5][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_flo_sbb_new19 = np.nanmean(np.nansum(np.array(p_minor_flo_new19[6][0]),axis=0).reshape(ryi,12),axis=0)

p_minor_tnn_ssd_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[0][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_nsd_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[1][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_occ_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[2][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_spp_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[3][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_smm_new19 = np.zeros((12))
#p_minor_tnn_smm_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[4][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_ven_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[5][0]),axis=0).reshape(ryi,12),axis=0)
p_minor_tnn_sbb_new19 = np.nanmean(np.nansum(np.array(p_minor_tn_new19[6][0]),axis=0).reshape(ryi,12),axis=0)


# sum major and minor potw datasets
p_flo_ssd_old = p_major_flo_ssd_old+p_minor_flo_ssd_old
p_flo_nsd_old = p_major_flo_nsd_old+p_minor_flo_nsd_old
p_flo_occ_old = p_major_flo_occ_old+p_minor_flo_occ_old
p_flo_spp_old = p_major_flo_spp_old+p_minor_flo_spp_old
p_flo_smm_old = p_major_flo_smm_old+p_minor_flo_smm_old
p_flo_ven_old = p_major_flo_ven_old+p_minor_flo_ven_old
p_flo_sbb_old = p_major_flo_sbb_old+p_minor_flo_sbb_old

p_tnn_ssd_old = (p_major_tnn_ssd_old+p_minor_tnn_ssd_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_nsd_old = (p_major_tnn_nsd_old+p_minor_tnn_nsd_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_occ_old = (p_major_tnn_occ_old+p_minor_tnn_occ_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_spp_old = (p_major_tnn_spp_old+p_minor_tnn_spp_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_smm_old = (p_major_tnn_smm_old+p_minor_tnn_smm_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_ven_old = (p_major_tnn_ven_old+p_minor_tnn_ven_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_sbb_old = (p_major_tnn_sbb_old+p_minor_tnn_sbb_old)*s_to_d*g_N*g_to_kg*mmol_to_mol

p_din_ssd_old = (p_major_din_ssd_old+p_minor_tnn_ssd_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_nsd_old = (p_major_din_nsd_old+p_minor_tnn_nsd_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_occ_old = (p_major_din_occ_old+p_minor_tnn_occ_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_spp_old = (p_major_din_spp_old+p_minor_tnn_spp_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_smm_old = (p_major_din_smm_old+p_minor_tnn_smm_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_ven_old = (p_major_din_ven_old+p_minor_tnn_ven_old)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_sbb_old = (p_major_din_sbb_old+p_minor_tnn_sbb_old)*s_to_d*g_N*g_to_kg*mmol_to_mol

p_flo_ssd_new = p_major_flo_ssd_new+p_minor_flo_ssd_new
p_flo_nsd_new = p_major_flo_nsd_new+p_minor_flo_nsd_new
p_flo_occ_new = p_major_flo_occ_new+p_minor_flo_occ_new
p_flo_spp_new = p_major_flo_spp_new+p_minor_flo_spp_new
p_flo_smm_new = p_major_flo_smm_new+p_minor_flo_smm_new
p_flo_ven_new = p_major_flo_ven_new+p_minor_flo_ven_new
p_flo_sbb_new = p_major_flo_sbb_new+p_minor_flo_sbb_new

p_tnn_ssd_new = (p_major_tnn_ssd_new+p_minor_tnn_ssd_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_nsd_new = (p_major_tnn_nsd_new+p_minor_tnn_nsd_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_occ_new = (p_major_tnn_occ_new+p_minor_tnn_occ_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_spp_new = (p_major_tnn_spp_new+p_minor_tnn_spp_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_smm_new = (p_major_tnn_smm_new+p_minor_tnn_smm_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_ven_new = (p_major_tnn_ven_new+p_minor_tnn_ven_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_tnn_sbb_new = (p_major_tnn_sbb_new+p_minor_tnn_sbb_new)*s_to_d*g_N*g_to_kg*mmol_to_mol

p_din_ssd_new = (p_major_din_ssd_new+p_minor_tnn_ssd_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_nsd_new = (p_major_din_nsd_new+p_minor_tnn_nsd_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_occ_new = (p_major_din_occ_new+p_minor_tnn_occ_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_spp_new = (p_major_din_spp_new+p_minor_tnn_spp_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_smm_new = (p_major_din_smm_new+p_minor_tnn_smm_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_ven_new = (p_major_din_ven_new+p_minor_tnn_ven_new)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_sbb_new = (p_major_din_sbb_new+p_minor_tnn_sbb_new)*s_to_d*g_N*g_to_kg*mmol_to_mol


p_din_ssd_new19 = (p_major_din_ssd_new19+p_minor_tnn_ssd_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_nsd_new19 = (p_major_din_nsd_new19+p_minor_tnn_nsd_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_occ_new19 = (p_major_din_occ_new19+p_minor_tnn_occ_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_spp_new19 = (p_major_din_spp_new19+p_minor_tnn_spp_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_smm_new19 = (p_major_din_smm_new19+p_minor_tnn_smm_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_ven_new19 = (p_major_din_ven_new19+p_minor_tnn_ven_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol
p_din_sbb_new19 = (p_major_din_sbb_new19+p_minor_tnn_sbb_new19)*s_to_d*g_N*g_to_kg*mmol_to_mol

# yearly average
print('DIN ssd 1997-2000: ',np.nanmean(p_din_ssd_old))
print('DIN nsd 1997-2000: ',np.nanmean(p_din_nsd_old))
print('DIN occ 1997-2000: ',np.nanmean(p_din_occ_old))
print('DIN spp 1997-2000: ',np.nanmean(p_din_spp_old))
print('DIN smm 1997-2000: ',np.nanmean(p_din_smm_old))
print('DIN ven 1997-2000: ',np.nanmean(p_din_ven_old))
print('DIN sbb 1997-2000: ',np.nanmean(p_din_sbb_old))
print('DIN isl 1997-2000: ',p_minor_tn_isl_old)

print('DIN ssd 2013-2017: ',np.nanmean(p_din_ssd_new))
print('DIN nsd 2013-2017: ',np.nanmean(p_din_nsd_new))
print('DIN occ 2013-2017: ',np.nanmean(p_din_occ_new))
print('DIN spp 2013-2017: ',np.nanmean(p_din_spp_new))
print('DIN smm 2013-2017: ',np.nanmean(p_din_smm_new))
print('DIN ven 2013-2017: ',np.nanmean(p_din_ven_new))
print('DIN sbb 2013-2017: ',np.nanmean(p_din_sbb_new))
print('DIN isl 2013-2017: ',p_minor_tn_isl_new)

print('DIN ssd new 1997-2000: ',np.nanmean(p_din_ssd_new19))
print('DIN nsd new 1997-2000: ',np.nanmean(p_din_nsd_new19))
print('DIN occ new 1997-2000: ',np.nanmean(p_din_occ_new19))
print('DIN spp new 1997-2000: ',np.nanmean(p_din_spp_new19))
print('DIN smm new 1997-2000: ',np.nanmean(p_din_smm_new19))
print('DIN ven new 1997-2000: ',np.nanmean(p_din_ven_new19))
print('DIN sbb new 1997-2000: ',np.nanmean(p_din_sbb_new19))
print('DIN isl new 1997-2000: ',p_minor_tn_isl_new19)


# bightwide sum
p_bight_tn = np.nansum(p_yr_nobight_tn)
r_bight_tn = np.nansum(r_yr_nobight_tn)
p_bight_tp = np.nansum(p_yr_nobight_tp)
r_bight_tp = np.nansum(r_yr_nobight_tp)
a_bight = np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*atmos_plt)
atmos_plt = atmos_plt*((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))

#############
# plot
#############
#plt.ion()

a_yr = np.append(atmos_plt,a_bight)
p_yr_tn = np.append(p_yr_nobight_tn,p_bight_tn)
r_yr_tn = np.append(r_yr_nobight_tn,r_bight_tn)
p_yr_tp = np.append(p_yr_nobight_tp,p_bight_tp)
r_yr_tp = np.append(r_yr_nobight_tp,r_bight_tp)

p_yr_kg_tn = p_yr_tn
r_yr_kg_tn = r_yr_tn
p_yr_kg_tp = p_yr_tp
r_yr_kg_tp = r_yr_tp

figw = 14
figh = 8
regions = ['S SD','N SD','OC','SP','SM','Ventura','SB','Bightwide']
width = 0.2
axis_font = 18
if log_set == True:
    savename = './figs/inputs_compare_region_1997_2010_tptn.pdf'
else:
    savename = './figs/inputs_compare_region_1997_2010_nolog_tptn.pdf'

x_ind = np.arange(len(regions))

'''
r_col = 'lightskyblue'
p_col = 'gray'

y1 = 1E3
y2 = 1E9

fig,ax = plt.subplots(1,1,sharex=True,figsize=[figw,figh])
ax.bar(x_ind,p_yr_kg_tn,color=p_col,width=width,hatch='\\')
ax.bar(x_ind+width,r_yr_kg_tn,color=r_col,width=width,hatch='\\')
ax.bar(x_ind+(2.4*width),p_yr_kg_tp,color=p_col,width=width,hatch='.')
ax.bar(x_ind+(3.4*width),r_yr_kg_tp,color=r_col,width=width,hatch='.')
ax.bar(np.nan,np.nan,color=p_col,width=width,label='Ocean Outfalls')
ax.bar(np.nan,np.nan,color=r_col,width=width,label='Rivers')
ax.bar(np.nan,np.nan,color='white',hatch='\\',width=width,label='TN')
ax.bar(np.nan,np.nan,color='white',hatch='.',width=width,label='TP')
ax.set_xticks([width+.15,1+width+.15,2+width+.15,3+width+.15,4+width+.15,5+width+.15,6+width+.15,7+width+.15])
ax.set_xticklabels(regions)

ax.legend().set_visible(False)

ax.legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=4,handlelength=2.5,handleheight=1.5)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
ax.set_ylabel('Total Flux kg y$^{-1}$',fontsize=axis_font)
ax.set_xlabel('Region',fontsize=axis_font)
# set to log scale
if log_set == True:
    ax.set_yscale('log')
    ax.set_ybound(lower=y1,upper=y2)

ax.text(x_ind[0],p_yr_kg_tn[0]+3E6,format(np.floor(p_yr_kg_tn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[1],p_yr_kg_tn[1]+3E5,format(np.floor(p_yr_kg_tn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[2],p_yr_kg_tn[2]+3E6,format(np.floor(p_yr_kg_tn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[3],p_yr_kg_tn[3]+3E6,format(np.floor(p_yr_kg_tn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[4],p_yr_kg_tn[4]+3E6,format(np.floor(p_yr_kg_tn[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[5],p_yr_kg_tn[5]+2E5,format(np.floor(p_yr_kg_tn[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[6],p_yr_kg_tn[6]+5E4,format(np.floor(p_yr_kg_tn[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[7],p_yr_kg_tn[7]+1E7,format(np.floor(p_yr_kg_tn[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax.text(x_ind[0]+width,r_yr_kg_tn[0]+2E5,format(np.floor(r_yr_kg_tn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[1]+width,r_yr_kg_tn[1]+5E4,format(np.floor(r_yr_kg_tn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[2]+width,r_yr_kg_tn[2]+2E5,format(np.floor(r_yr_kg_tn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[3]+width,r_yr_kg_tn[3]+2E5,format(np.floor(r_yr_kg_tn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[4]+width,r_yr_kg_tn[4]+2E5,format(np.floor(r_yr_kg_tn[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[5]+width,r_yr_kg_tn[5]+2E5,format(np.floor(r_yr_kg_tn[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[6]+width,r_yr_kg_tn[6]+2E5,format(np.floor(r_yr_kg_tn[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[7]+width,r_yr_kg_tn[7]+1E6,format(np.floor(r_yr_kg_tn[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax.text(x_ind[0]+(2.4*width),p_yr_kg_tp[0]+5E4,format(np.floor(p_yr_kg_tp[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[1]+(2.4*width),p_yr_kg_tp[1]+5E4,format(np.floor(p_yr_kg_tp[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[2]+(2.4*width),p_yr_kg_tp[2]+2E5,format(np.floor(p_yr_kg_tp[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[3]+(2.4*width),p_yr_kg_tp[3]+2E5,format(np.floor(p_yr_kg_tp[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[4]+(2.4*width),p_yr_kg_tp[4]+2E5,format(np.floor(p_yr_kg_tp[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[5]+(2.4*width),p_yr_kg_tp[5]+4E4,format(np.floor(p_yr_kg_tp[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[6]+(2.4*width),p_yr_kg_tp[6]+4E2,format(np.floor(p_yr_kg_tp[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[7]+(2.4*width),p_yr_kg_tp[7]+1E6,format(np.floor(p_yr_kg_tp[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax.text(x_ind[0]+(3.4*width),r_yr_kg_tp[0]+3E4,format(np.floor(r_yr_kg_tp[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[1]+(3.4*width),r_yr_kg_tp[1]+8E3,format(np.floor(r_yr_kg_tp[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[2]+(3.4*width),r_yr_kg_tp[2]+3E4,format(np.floor(r_yr_kg_tp[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[3]+(3.4*width),r_yr_kg_tp[3]+3E4,format(np.floor(r_yr_kg_tp[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[4]+(3.4*width),r_yr_kg_tp[4]+3E4,format(np.floor(r_yr_kg_tp[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[5]+(3.4*width),r_yr_kg_tp[5]+3E4,format(np.floor(r_yr_kg_tp[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[6]+(3.4*width),r_yr_kg_tp[6]+3E4,format(np.floor(r_yr_kg_tp[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax.text(x_ind[7]+(3.4*width),r_yr_kg_tp[7]+2E5,format(np.floor(r_yr_kg_tp[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

plt.savefig(savename,bbox_inches='tight')
'''

###################################
# make it two panel with TN and TP
###################################
figw = 12
figh = 14
regions = ['S SD','N SD','OC','SP','SM','Ventura','SB','Bightwide']
width = 0.2
axis_font = 18
if log_set == True:
    savename = './figs/inputs_compare_region_1997_2010_tptn_2panel.pdf'
else:
    savename = './figs/inputs_compare_region_1997_2010_nolog_tptn_2panel.pdf'

x_ind = np.arange(len(regions))

#plt.ion()

r_col = 'lightskyblue'
p_col = 'orange'
a_col = 'gray'

y1 = 1E3
y2 = 1E9

fig,ax = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
ax[0].bar(x_ind,p_yr_kg_tn,color=p_col,width=width,label='Ocean Outfalls')
ax[0].bar(x_ind+width,r_yr_kg_tn,color=r_col,width=width,hatch='\\',label='Rivers')
ax[0].bar(x_ind+(2*width),a_yr,color=a_col,width=width,hatch='.',label='Atmospheric Deposition')
ax[1].bar(x_ind,p_yr_kg_tp,color=p_col,width=width)
ax[1].bar(x_ind+width,r_yr_kg_tp,color=r_col,width=width,hatch='\\')
ax[1].set_xticks([width,1+width,2+width,3+width,4+width,5+width,6+width,7+width])
ax[1].set_xticklabels(regions)

#ax.legend().set_visible(False)

ax[0].legend(loc='lower left',fontsize=axis_font,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=4,handlelength=2.5,handleheight=1.5)
ax[0].tick_params(axis='both',which='major',labelsize=axis_font)
ax[1].tick_params(axis='both',which='major',labelsize=axis_font)
ax[0].set_ylabel('Total Flux TN kg y$^{-1}$',fontsize=axis_font)
ax[1].set_ylabel('Total Flux TP kg y$^{-1}$',fontsize=axis_font)
ax[1].set_xlabel('Region',fontsize=axis_font)
# set to log scale
#if log_set == True:
ax[0].set_yscale('log')
ax[0].set_ybound(lower=1E4,upper=1E8)
ax[1].set_yscale('log')
ax[1].set_ybound(lower=y1,upper=1E7)

ax[0].text(x_ind[0],p_yr_kg_tn[0]+1E6,format(np.floor(p_yr_kg_tn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[1],p_yr_kg_tn[1]+1.5E5,format(np.floor(p_yr_kg_tn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[2],p_yr_kg_tn[2]-1.25E7,format(np.floor(p_yr_kg_tn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[3],p_yr_kg_tn[3]-1.65E7,format(np.floor(p_yr_kg_tn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[4],p_yr_kg_tn[4]-1.6E7,format(np.floor(p_yr_kg_tn[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[5],p_yr_kg_tn[5]+1E5,format(np.floor(p_yr_kg_tn[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[6],p_yr_kg_tn[6]+4E4,format(np.floor(p_yr_kg_tn[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[7],p_yr_kg_tn[7]-5.4E7,format(np.floor(p_yr_kg_tn[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax[0].text(x_ind[0]+width,r_yr_kg_tn[0]+1E5,format(np.floor(r_yr_kg_tn[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[1]+width,r_yr_kg_tn[1]+4E4,format(np.floor(r_yr_kg_tn[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[2]+width,r_yr_kg_tn[2]+1E5,format(np.floor(r_yr_kg_tn[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[3]+width,r_yr_kg_tn[3]+5E5,format(np.floor(r_yr_kg_tn[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[4]+width,r_yr_kg_tn[4]+2E4,format(np.floor(r_yr_kg_tn[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[5]+width,r_yr_kg_tn[5]+1E5,format(np.floor(r_yr_kg_tn[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[6]+width,r_yr_kg_tn[6]+2E4,format(np.floor(r_yr_kg_tn[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[7]+width,r_yr_kg_tn[7]+8.4E5,format(np.floor(r_yr_kg_tn[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax[0].text(x_ind[0]+(2*width),a_yr[0]+4E4,format(np.floor(a_yr[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[1]+(2*width),a_yr[1]+4E4,format(np.floor(a_yr[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[2]+(2*width),a_yr[2]+8E4,format(np.floor(a_yr[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[3]+(2*width),a_yr[3]+8E4,format(np.floor(a_yr[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[4]+(2*width),a_yr[4]+8E4,format(np.floor(a_yr[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[5]+(2*width),a_yr[5]+8E4,format(np.floor(a_yr[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[6]+(2*width),a_yr[6]+7E4,format(np.floor(a_yr[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[0].text(x_ind[7]+(2*width),a_yr[7]+4E5,format(np.floor(a_yr[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax[1].text(x_ind[0],p_yr_kg_tp[0]+4E4,format(np.floor(p_yr_kg_tp[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[1],p_yr_kg_tp[1]+4E4,format(np.floor(p_yr_kg_tp[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[2],p_yr_kg_tp[2]+1E5,format(np.floor(p_yr_kg_tp[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[3],p_yr_kg_tp[3]+1E5,format(np.floor(p_yr_kg_tp[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[4],p_yr_kg_tp[4]+1E5,format(np.floor(p_yr_kg_tp[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[5],p_yr_kg_tp[5]+2E4,format(np.floor(p_yr_kg_tp[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[6],p_yr_kg_tp[6]+4E2,format(np.floor(p_yr_kg_tp[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[7],p_yr_kg_tp[7]-1.9E6,format(np.floor(p_yr_kg_tp[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax[1].text(x_ind[0]+width,r_yr_kg_tp[0]+2E4,format(np.floor(r_yr_kg_tp[0]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[1]+width,r_yr_kg_tp[1]+7E3,format(np.floor(r_yr_kg_tp[1]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[2]+width,r_yr_kg_tp[2]+2E4,format(np.floor(r_yr_kg_tp[2]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[3]+width,r_yr_kg_tp[3]+6E4,format(np.floor(r_yr_kg_tp[3]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[4]+width,r_yr_kg_tp[4]+2E3,format(np.floor(r_yr_kg_tp[4]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[5]+width,r_yr_kg_tp[5]+2E4,format(np.floor(r_yr_kg_tp[5]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[6]+width,r_yr_kg_tp[6]+1E4,format(np.floor(r_yr_kg_tp[6]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')
ax[1].text(x_ind[7]+width,r_yr_kg_tp[7]+2E5,format(np.floor(r_yr_kg_tp[7]).astype(int),',d'),fontsize=12,rotation=90,horizontalalignment='center')

ax[0].text(-.4,60000000,'a)',fontsize=20)
ax[1].text(-.4,5000000,'b)',fontsize=20)
#ax[0].text(x_ind[7]+(2*width),60000000,'a)',fontsize=18)
#ax[1].text(x_ind[7]+(2*width),5000000,'b)',fontsize=18)
fig.subplots_adjust(hspace=0.1)
plt.savefig(savename,bbox_inches='tight')

