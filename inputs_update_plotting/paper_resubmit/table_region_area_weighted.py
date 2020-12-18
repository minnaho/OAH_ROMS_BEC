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
river_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc'
potw_major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
log_set = True

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

################
# load atmos data
################
dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')
#m2_to_hectare = 10000
m2_resolution_grid = 330*330

oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_resolution_grid*mask_nc
redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_resolution_grid*mask_nc
alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_resolution_grid*mask_nc
fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_resolution_grid*mask_nc

oxn_yr  = np.nansum(oxn,axis=0)
redn_yr = np.nansum(redn,axis=0)
alk_yr  = np.nansum(alk,axis=0)
fe_yr   = np.nansum(fe,axis=0)

oxn_all = np.empty((maskarr.shape[0],maskarr.shape[1],maskarr.shape[2]))
redn_all = np.empty((maskarr.shape[0],maskarr.shape[1],maskarr.shape[2]))
alk_all = np.empty((maskarr.shape[0],maskarr.shape[1],maskarr.shape[2]))
fe_all = np.empty((maskarr.shape[0],maskarr.shape[1],maskarr.shape[2]))

# break into regions
for r_i in range(oxn_all.shape[0]):
    oxn_all[r_i,:,:] = maskarr[r_i,:,:]*oxn_yr[:,:]
    redn_all[r_i,:,:] = maskarr[r_i,:,:]*redn_yr[:,:]
    alk_all[r_i,:,:] = maskarr[r_i,:,:]*alk_yr[:,:]
    fe_all[r_i,:,:] = maskarr[r_i,:,:]*fe_yr[:,:]

atmos_plt = np.nansum(np.nansum((oxn_all+redn_all),axis=1),axis=1)

###############
# river major data (10 yrs) 1997-2007
###############
river_nc = Dataset(river_path,'r')

river_time = num2date(np.array(river_nc.variables['time']),river_nc.variables['time'].units)

# convert real_datetime to datetime
river_time_l = []
for d_i in range(len(river_time)):
    river_time_l.append(river_time[d_i]+datetime.timedelta(0,1))

river_time_dt = np.array(river_time_l)

#river_lat = np.array(river_nc.variables['latitude'][0,:])
#river_lon = np.array(river_nc.variables['longitude'][0,:])
river_lat = np.array(river_nc.variables['latitude'][:])
river_lon = np.array(river_nc.variables['longitude'][:])

r_coord_i = []
r_coord_j = []
for coord in range(len(river_lat)):
    lat_you_want = river_lat[coord]
    lon_you_want = river_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    r_coord_i.append(xi_coord)
    r_coord_j.append(eta_coord)

# make list of lists because each sublist will have different length
r_river_ind = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(river_lat)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,r_coord_j[r_i],r_coord_i[r_i]] == 1:
            r_river_ind[m_i].append(r_i)

# divide flows

river_flo = np.array(river_nc.variables['flow']) # m3/s
river_nh4 = np.array(river_nc.variables['NH4']) # mmol/m3
river_no3 = np.array(river_nc.variables['NO3']) # mmol/m3
river_po4 = np.array(river_nc.variables['PO4']) # mmol/m3
river_alk = np.array(river_nc.variables['alkalinity']) 
river_temp = np.array(river_nc.variables['temperature']) 
river_tn = np.array(river_nc.variables['total_N']) 
river_tp = np.array(river_nc.variables['total_P']) 

river_flo[river_flo>1E20] = np.nan
river_tn[river_tn>1E20] = np.nan
river_tp[river_tp>1E20] = np.nan

r_river_flo = [[] for i in range(maskarr.shape[0])]
r_river_tn = [[] for i in range(maskarr.shape[0])] # TN flux
r_river_tp = [[] for i in range(maskarr.shape[0])] # TN flux
for r_i in range(len(r_river_ind)):
    r_river_flo[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]).tolist())
    r_river_tn[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_tn[:,r_river_ind[r_i]]).tolist())
    r_river_tp[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_tp[:,r_river_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (10,12) because this data set is 10 years
# then average over 10 years to get year average
ry0 = 21

r_river_flo_ssd = np.nansum(np.nansum(np.array(r_river_flo[0][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_nsd = np.nansum(np.nansum(np.array(r_river_flo[1][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_occ = np.nansum(np.nansum(np.array(r_river_flo[2][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_spp = np.nansum(np.nansum(np.array(r_river_flo[3][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_smm = np.nansum(np.nansum(np.array(r_river_flo[4][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_ven = np.nansum(np.nansum(np.array(r_river_flo[5][0]),axis=0).reshape(ry0,12),axis=1)
r_river_flo_sbb = np.nansum(np.nansum(np.array(r_river_flo[6][0]),axis=0).reshape(ry0,12),axis=1)

r_river_tnn_ssd = np.nansum(np.nansum(np.array(r_river_tn[0][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_nsd = np.nansum(np.nansum(np.array(r_river_tn[1][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_occ = np.nansum(np.nansum(np.array(r_river_tn[2][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_spp = np.nansum(np.nansum(np.array(r_river_tn[3][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_smm = np.nansum(np.nansum(np.array(r_river_tn[4][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_ven = np.nansum(np.nansum(np.array(r_river_tn[5][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tnn_sbb = np.nansum(np.nansum(np.array(r_river_tn[6][0]),axis=0).reshape(ry0,12),axis=1)

r_river_tpp_ssd = np.nansum(np.nansum(np.array(r_river_tp[0][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_nsd = np.nansum(np.nansum(np.array(r_river_tp[1][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_occ = np.nansum(np.nansum(np.array(r_river_tp[2][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_spp = np.nansum(np.nansum(np.array(r_river_tp[3][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_smm = np.nansum(np.nansum(np.array(r_river_tp[4][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_ven = np.nansum(np.nansum(np.array(r_river_tp[5][0]),axis=0).reshape(ry0,12),axis=1)
r_river_tpp_sbb = np.nansum(np.nansum(np.array(r_river_tp[6][0]),axis=0).reshape(ry0,12),axis=1)

# sum different river datasets
r_flo_ssd = np.nanmean(r_river_flo_ssd)
r_flo_nsd = np.nanmean(r_river_flo_nsd)
r_flo_occ = np.nanmean(r_river_flo_occ)
r_flo_spp = np.nanmean(r_river_flo_spp)
r_flo_smm = np.nanmean(r_river_flo_smm)
r_flo_ven = np.nanmean(r_river_flo_ven)
r_flo_sbb = np.nanmean(r_river_flo_sbb)

r_tnn_ssd = np.nanmean(r_river_tnn_ssd)
r_tnn_nsd = np.nanmean(r_river_tnn_nsd)
r_tnn_occ = np.nanmean(r_river_tnn_occ)
r_tnn_spp = np.nanmean(r_river_tnn_spp)
r_tnn_smm = np.nanmean(r_river_tnn_smm)
r_tnn_ven = np.nanmean(r_river_tnn_ven)
r_tnn_sbb = np.nanmean(r_river_tnn_sbb)

r_tpp_ssd = np.nanmean(r_river_tpp_ssd)
r_tpp_nsd = np.nanmean(r_river_tpp_nsd)
r_tpp_occ = np.nanmean(r_river_tpp_occ)
r_tpp_spp = np.nanmean(r_river_tpp_spp)
r_tpp_smm = np.nanmean(r_river_tpp_smm)
r_tpp_ven = np.nanmean(r_river_tpp_ven)
r_tpp_sbb = np.nanmean(r_river_tpp_sbb)

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2010
potw_1997 = 312 # 1997-01-31
potw_2013 = 564 # 2011-01-01

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l[potw_1997:potw_2013])

major_potw_lat = np.array(potw_ma_nc.variables['latitude'])
major_potw_lon = np.array(potw_ma_nc.variables['longitude'])

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
major_flo = np.array(potw_ma_nc.variables['flow']) # m3/s
major_nh4 = np.array(potw_ma_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(potw_ma_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(potw_ma_nc.variables['NO2']) # mmol/m3
major_on  = np.array(potw_ma_nc.variables['organic_N']) # mmol/m3
major_po4 = np.array(potw_ma_nc.variables['PO4']) # mmol/m3
major_op  = np.array(potw_ma_nc.variables['organic_P']) # mmol/m3
major_fe  = np.array(potw_ma_nc.variables['total_Fe'])  # mmol/m3
major_pH  = np.array(potw_ma_nc.variables['pH'])
major_alk = np.array(potw_ma_nc.variables['alkalinity'])
major_temp = np.array(potw_ma_nc.variables['temperature'])
major_salt = np.array(potw_ma_nc.variables['salinity'])
major_toc  = np.array(potw_ma_nc.variables['total_organic_C'])

major_tn = major_nh4+major_no3+major_no2+major_on
major_tp = major_po4+major_op

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan

p_major_flo = [[] for i in range(maskarr.shape[0])]
p_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
p_major_tp = [[] for i in range(maskarr.shape[0])] # TP flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    p_major_tp[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_tp[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())



# turn to array so can sum all potw in region up
# then reshape to (21,12) because this data set is 14 years 1997-2010
# then average over 14 years to get year average
ry0 = 21

#p_major_flo_nsd = np.nanmean(np.nansum(np.array(p_major_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ssd = np.nanmean(np.nansum(np.array(p_major_flo[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_nsd = np.zeros((12))
p_major_flo_occ = np.nanmean(np.nansum(np.array(p_major_flo[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_spp = np.nanmean(np.nansum(np.array(p_major_flo[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_smm = np.nanmean(np.nansum(np.array(p_major_flo[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_flo_ven = np.zeros((12))
p_major_flo_sbb = np.zeros((12))
#p_major_flo_ven = np.nanmean(np.nansum(np.array(p_major_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_flo_sbb = np.nanmean(np.nansum(np.array(p_major_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

#p_major_tnn_nsd = np.nanmean(np.nansum(np.array(p_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ssd = np.nanmean(np.nansum(np.array(p_major_tn[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_nsd = np.zeros((12))
p_major_tnn_occ = np.nanmean(np.nansum(np.array(p_major_tn[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_spp = np.nanmean(np.nansum(np.array(p_major_tn[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_smm = np.nanmean(np.nansum(np.array(p_major_tn[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tnn_ven = np.zeros((12))
p_major_tnn_sbb = np.zeros((12))
#p_major_tnn_ven = np.nanmean(np.nansum(np.array(p_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_tnn_sbb = np.nanmean(np.nansum(np.array(p_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)


#p_major_tpp_nsd = np.nanmean(np.nansum(np.array(p_major_tp[1][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tpp_ssd = np.nanmean(np.nansum(np.array(p_major_tp[0][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tpp_nsd = np.zeros((12))
p_major_tpp_occ = np.nanmean(np.nansum(np.array(p_major_tp[2][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tpp_spp = np.nanmean(np.nansum(np.array(p_major_tp[3][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tpp_smm = np.nanmean(np.nansum(np.array(p_major_tp[4][0]),axis=0).reshape(ry0,12),axis=0)
p_major_tpp_ven = np.zeros((12))
p_major_tpp_sbb = np.zeros((12))
#p_major_tpp_ven = np.nanmean(np.nansum(np.array(p_major_tp[5][0]),axis=0).reshape(ry0,12),axis=0)
#p_major_tpp_sbb = np.nanmean(np.nansum(np.array(p_major_tp[6][0]),axis=0).reshape(ry0,12),axis=0)

##############
# minor potw
##############
# multiply masks by 0-15km mask to exclude island minor potws
for j_i in range(maskarr.shape[0]):
    maskarr[j_i] = maskarr[j_i]*mask_mat

potw_mi_nc = Dataset(potw_minor_path,'r')


minor_potw_lat = np.array(potw_mi_nc.variables['latitude'])
minor_potw_lon = np.array(potw_mi_nc.variables['longitude'])

p_coord_i = []
p_coord_j = []
for coord in range(len(minor_potw_lat)):
    lat_you_want = minor_potw_lat[coord]
    lon_you_want = minor_potw_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    p_coord_i.append(xi_coord)
    p_coord_j.append(eta_coord)


# make list of lists because each sublist will have different length
p_minor_ind = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(minor_potw_lat)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,p_coord_j[r_i],p_coord_i[r_i]] == 1:
            p_minor_ind[m_i].append(r_i)

minor_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

minor_tn = minor_no3+minor_nh4+minor_no2

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

p_minor_flo = [[] for i in range(maskarr.shape[0])]
p_minor_tn = [[] for i in range(maskarr.shape[0])]
p_minor_tp = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(p_minor_ind)):
    p_minor_flo[r_i].append(np.transpose(minor_flo[:,p_minor_ind[r_i]]).tolist())
    p_minor_tn[r_i].append(np.transpose(minor_flo[:,p_minor_ind[r_i]]*minor_tn[:,p_minor_ind[r_i]]).tolist())
    p_minor_tp[r_i].append(np.transpose(minor_flo[:,p_minor_ind[r_i]]*minor_po4[:,p_minor_ind[r_i]]).tolist())

# turn to array so can sum all minor potw in region up
ry0 = 21

p_minor_flo_ssd = np.nanmean(np.nansum(np.array(p_minor_flo[0][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_flo_nsd = np.nanmean(np.nansum(np.array(p_minor_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_flo_occ = np.nanmean(np.nansum(np.array(p_minor_flo[2][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_flo_spp = np.nanmean(np.nansum(np.array(p_minor_flo[3][0]),axis=0).reshape(ry0,12),axis=0)
#p_minor_flo_smm = np.nanmean(np.nansum(np.array(p_minor_flo[4][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_flo_smm = np.zeros((12))
p_minor_flo_ven = np.nanmean(np.nansum(np.array(p_minor_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_flo_sbb = np.nanmean(np.nansum(np.array(p_minor_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

p_minor_tnn_ssd = np.nanmean(np.nansum(np.array(p_minor_tn[0][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tnn_nsd = np.nanmean(np.nansum(np.array(p_minor_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tnn_occ = np.nanmean(np.nansum(np.array(p_minor_tn[2][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tnn_spp = np.nanmean(np.nansum(np.array(p_minor_tn[3][0]),axis=0).reshape(ry0,12),axis=0)
#p_minor_tnn_smm = np.nanmean(np.nansum(np.array(p_minor_tn[4][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tnn_smm = np.zeros((12))
p_minor_tnn_ven = np.nanmean(np.nansum(np.array(p_minor_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tnn_sbb = np.nanmean(np.nansum(np.array(p_minor_tn[6][0]),axis=0).reshape(ry0,12),axis=0)

p_minor_tpp_ssd = np.nanmean(np.nansum(np.array(p_minor_tp[0][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_nsd = np.nanmean(np.nansum(np.array(p_minor_tp[1][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_occ = np.nanmean(np.nansum(np.array(p_minor_tp[2][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_spp = np.nanmean(np.nansum(np.array(p_minor_tp[3][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_smm = np.zeros((12))
#p_minor_tpp_smm = np.nanmean(np.nansum(np.array(p_minor_tp[4][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_ven = np.nanmean(np.nansum(np.array(p_minor_tp[5][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_tpp_sbb = np.nanmean(np.nansum(np.array(p_minor_tp[6][0]),axis=0).reshape(ry0,12),axis=0)

# inland POTW
# see Inland POTW excel for inland potw data
inland_tnn = np.load('inland_potw_tnn_region.npy')
inland_tpp = np.load('inland_potw_tpp_region.npy')
inland_din = np.load('inland_potw_din_region.npy')
inland_dip = np.load('inland_potw_dip_region.npy')

# inland potw flow by region
#ssd,nsd,occ,spp,smb,ven,sbb,scb
#inland_flows = [2348848,17432137,2564159,1.75E8,4941331,53495704,np.nan,255900740]
inland_flows = [2348592.5,17430240.42,2563880.146,175099510.9,4940793.908,53489884.95,np.nan,255872902.9]

# Esondido (nsd) actually is a minor POTW
# remove inland flow for nsd and sbb because they don't have inland plants 
inland_flows[1] = 0
inland_flows[6] = 0
inland_tnn[1] = 0
inland_tnn[6] = 0


# sum major and minor potw datasets
p_flo_ssd = p_major_flo_ssd+p_minor_flo_ssd
p_flo_nsd = p_major_flo_nsd+p_minor_flo_nsd
p_flo_occ = p_major_flo_occ+p_minor_flo_occ
p_flo_spp = p_major_flo_spp+p_minor_flo_spp
p_flo_smm = p_major_flo_smm+p_minor_flo_smm
p_flo_ven = p_major_flo_ven+p_minor_flo_ven
p_flo_sbb = p_major_flo_sbb+p_minor_flo_sbb

p_tnn_ssd = p_major_tnn_ssd+p_minor_tnn_ssd
p_tnn_nsd = p_major_tnn_nsd+p_minor_tnn_nsd
p_tnn_occ = p_major_tnn_occ+p_minor_tnn_occ
p_tnn_spp = p_major_tnn_spp+p_minor_tnn_spp
p_tnn_smm = p_major_tnn_smm+p_minor_tnn_smm
p_tnn_ven = p_major_tnn_ven+p_minor_tnn_ven
p_tnn_sbb = p_major_tnn_sbb+p_minor_tnn_sbb

p_tpp_ssd = p_major_tpp_ssd+p_minor_tpp_ssd
p_tpp_nsd = p_major_tpp_nsd+p_minor_tpp_nsd
p_tpp_occ = p_major_tpp_occ+p_minor_tpp_occ
p_tpp_spp = p_major_tpp_spp+p_minor_tpp_spp
p_tpp_smm = p_major_tpp_smm+p_minor_tpp_smm
p_tpp_ven = p_major_tpp_ven+p_minor_tpp_ven
p_tpp_sbb = p_major_tpp_sbb+p_minor_tpp_sbb

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

p_yr_nobight_fl = np.array((np.nansum(s_to_d*d_to_mo*p_flo_ssd),np.nansum(s_to_d*d_to_mo*p_flo_nsd),np.nansum(s_to_d*d_to_mo*p_flo_occ),np.nansum(s_to_d*d_to_mo*p_flo_spp),np.nansum(s_to_d*d_to_mo*p_flo_smm),np.nansum(s_to_d*d_to_mo*p_flo_ven),np.nansum(s_to_d*d_to_mo*p_flo_sbb)))

p_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_sbb)))

p_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_sbb)))

r_yr_nobight_fl = np.array((np.nansum(s_to_d*d_to_mo*r_flo_ssd),np.nansum(s_to_d*d_to_mo*r_flo_nsd),np.nansum(s_to_d*d_to_mo*r_flo_occ),np.nansum(s_to_d*d_to_mo*r_flo_spp),np.nansum(s_to_d*d_to_mo*r_flo_smm),np.nansum(s_to_d*d_to_mo*r_flo_ven),np.nansum(s_to_d*d_to_mo*r_flo_sbb)))

r_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_sbb)))

r_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_sbb)))

# bightwide sum
p_bight_fl = np.nansum(p_yr_nobight_fl)
p_bight_tn = np.nansum(p_yr_nobight_tn)
r_bight_fl = np.nansum(r_yr_nobight_fl)
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

p_yr_fl = np.append(p_yr_nobight_fl,p_bight_fl)
r_yr_fl = np.append(r_yr_nobight_fl,r_bight_fl)

p_yr_tn = np.append(p_yr_nobight_tn,p_bight_tn)
r_yr_tn = np.append(r_yr_nobight_tn,r_bight_tn)
p_yr_tp = np.append(p_yr_nobight_tp,p_bight_tp)
r_yr_tp = np.append(r_yr_nobight_tp,r_bight_tp)

p_yr_kg_tn = p_yr_tn
r_yr_kg_tn = r_yr_tn
p_yr_kg_tp = p_yr_tp
r_yr_kg_tp = r_yr_tp

# new numbers given by Martha
# Santa Barbara
sbb_area = 823
# ventura 
ven_area = 5122
# santa monica
smm_area = 788
# san pedro
spp_area = 2175
# orange coounty
occ_area = 1950
# north san diego
nsd_area = 3121
# south san diego
ssd_area = 1573
# Southern California Bight 
scb_area = sbb_area+ven_area+smm_area+spp_area+occ_area+nsd_area+ssd_area

ssd_tn = (p_yr_tn[0]+r_yr_tn[0])/ssd_area
nsd_tn = (p_yr_tn[1]+r_yr_tn[1])/nsd_area
occ_tn = (p_yr_tn[2]+r_yr_tn[2])/occ_area
spp_tn = (p_yr_tn[3]+r_yr_tn[3])/spp_area
smm_tn = (p_yr_tn[4]+r_yr_tn[4])/smm_area
ven_tn = (p_yr_tn[5]+r_yr_tn[5])/ven_area
sbb_tn = (p_yr_tn[6]+r_yr_tn[6])/sbb_area
scb_tn = (p_yr_tn[7]+r_yr_tn[7])/scb_area

print('scb tn km',scb_tn)
print('ssd tn km',ssd_tn)
print('nsd tn km',nsd_tn)
print('occ tn km',occ_tn)
print('spp tn km',spp_tn)
print('smm tn km',smm_tn)
print('ven tn km',ven_tn)
print('sbb tn km',sbb_tn)

# river: inland PS vs NPS vs natural
#Summary Table_natural_historical_current.xlsx
# m3/s
nat_flo = [2.14E7,4.25E7,2.66E7,2.96E7,1.07E7,6.98E7,1.12E7,2.12E8]
nnt_flo = np.nansum(nat_flo[:7])

# kg/y
nat_cur_tpp =[637,1463,2602,2901,95,1921,317,9937]
nat_cur_dip = [56,128,227,253,8,168,28,866]
nat_cur_tnn = [4584,10524,18710,20863,685,13817,2278,33289]
nat_cur_din = [863,1808,2900,3234,120,2122,359,5463]

nnt_tnn = np.nansum(nat_cur_tnn[:7])

nat_tnn = np.nansum(nat_cur_tnn)
inland_tnn[3] = r_yr_nobight_tn[3]*.95
inland_tnn[4] = r_yr_nobight_tn[4]*.95
inland_tnn[5] = r_yr_nobight_tn[5]*.95

inl_flo = np.nansum(inland_flows[:7])
inl_tnn = np.nansum(inland_tnn[:7])

# ps vs nps flows
ps_fl = inl_flo+np.nansum(p_yr_nobight_fl)
nps_fl = np.nansum(r_yr_nobight_fl)-inl_flo-nnt_flo
perc_fl = ps_fl/(ps_fl+nps_fl+nnt_flo)
print('% PS flow vs all other freshwater flows',perc_fl)

ps_tn = np.nansum(p_yr_nobight_tn)+inl_tnn
nps_tn = np.nansum(r_yr_nobight_tn)-inl_tnn-nnt_tnn
perc_tn = ps_tn/(ps_tn+nps_tn+nnt_tnn)
print('% PS TN vs all other TN',perc_tn)

# major vs minor flow
major_flow = np.nansum(p_major_flo_ssd+p_major_flo_nsd+p_major_flo_occ+p_major_flo_spp+p_major_flo_smm+p_major_flo_ven+p_major_flo_sbb)
minor_flow = np.nansum(p_minor_flo_ssd+p_minor_flo_nsd+p_minor_flo_occ+p_minor_flo_spp+p_minor_flo_smm+p_minor_flo_ven+p_minor_flo_sbb)
print('major potw flow percentage vs minor flow',major_flow/(major_flow+minor_flow))

# major vs minor TN
minor_tnn = np.nansum(p_minor_tnn_ssd+p_minor_tnn_nsd+p_minor_tnn_occ+p_minor_tnn_spp+p_minor_tnn_smm+p_minor_tnn_ven+p_minor_tnn_sbb)
major_tnn = np.nansum(p_major_tnn_ssd+p_major_tnn_nsd+p_major_tnn_occ+p_major_tnn_spp+p_major_tnn_smm+p_major_tnn_ven+p_major_tnn_sbb)

print('minor potw tnn percentage vs major',minor_tnn/(major_tnn+minor_tnn))


print('river: inland PS vs all river',inl_tnn/(inl_tnn+nnt_tnn+nps_tn))
print('river: NPS vs all river',nps_tn/(inl_tnn+nnt_tnn+nps_tn))
