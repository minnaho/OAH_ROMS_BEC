import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io

fig_path = './figs/'
# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
setting = 'bight'

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
colors = ['spring','viridis_r','gray','rainbow','gnuplot_r','seismic','Greens_r']
plt.ion()
for i in range(len(maskarr)):
    plt.imshow(maskarr[i]*mask_nc,cmap=colors[i],origin='lower')

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
m2_to_hectare = 10000

oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_to_hectare
redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_to_hectare
alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_to_hectare
fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_to_hectare

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
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

major_lat = np.array(major_nc.variables['latitude'][0,:])
major_lon = np.array(major_nc.variables['longitude'][0,:])

r_coord_i = []
r_coord_j = []
for coord in range(len(major_lat)):
    lat_you_want = major_lat[coord]
    lon_you_want = major_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    r_coord_i.append(xi_coord)
    r_coord_j.append(eta_coord)

# make list of lists because each sublist will have different length
r_major_ind = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(major_lat)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,r_coord_j[r_i],r_coord_i[r_i]] == 1:
            r_major_ind[m_i].append(r_i)

# divide flows

major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['ammonium']) # mmol/m3
major_no3 = np.array(major_nc.variables['nitrate']) # mmol/m3
major_po4 = np.array(major_nc.variables['phosphate']) # mmol/m3
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_tn = np.array(major_nc.variables['total_nitrogen']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

r_major_flo = [[] for i in range(maskarr.shape[0])]
r_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
for r_i in range(len(r_major_ind)):
    r_major_flo[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tn[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tn[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (10,12) because this data set is 10 years
# then average over 10 years to get year average
ry0 = 10

r_major_flo_ssd = np.nanmean(np.nansum(np.array(r_major_flo[0][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_nsd = np.nanmean(np.nansum(np.array(r_major_flo[1][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_occ = np.nanmean(np.nansum(np.array(r_major_flo[2][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_spp = np.nanmean(np.nansum(np.array(r_major_flo[3][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_smm = np.nanmean(np.nansum(np.array(r_major_flo[4][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_ven = np.nanmean(np.nansum(np.array(r_major_flo[5][0]),axis=0).reshape(ry0,12),axis=0)
r_major_flo_sbb = np.nanmean(np.nansum(np.array(r_major_flo[6][0]),axis=0).reshape(ry0,12),axis=0)

r_major_tnn_ssd = np.nanmean(np.nansum(np.array(r_major_tn[0][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_nsd = np.nanmean(np.nansum(np.array(r_major_tn[1][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_occ = np.nanmean(np.nansum(np.array(r_major_tn[2][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_spp = np.nanmean(np.nansum(np.array(r_major_tn[3][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_smm = np.nanmean(np.nansum(np.array(r_major_tn[4][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_ven = np.nanmean(np.nansum(np.array(r_major_tn[5][0]),axis=0).reshape(ry0,12),axis=0)
r_major_tnn_sbb = np.nanmean(np.nansum(np.array(r_major_tn[6][0]),axis=0).reshape(ry0,12),axis=0)


##############
# river 24 yrs
##############
minor_nc = Dataset(minor_path,'r')

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)

minor_lat = np.array(minor_nc.variables['latitude'][0,:])
minor_lon = np.array(minor_nc.variables['longitude'][0,:])

r_coord_i = []
r_coord_j = []
for coord in range(len(minor_lat)):
    lat_you_want = minor_lat[coord]
    lon_you_want = minor_lon[coord]
    temp = np.abs( (lat_nc - lat_you_want)**2 + (lon_nc - lon_you_want)**2)
    eta_coord,xi_coord = np.unravel_index(temp.argmin(),temp.shape)
    r_coord_i.append(xi_coord)
    r_coord_j.append(eta_coord)

# make list of lists because each sublist will have different length
r_minor_ind = [[] for i in range(maskarr.shape[0])]
# find indices per region
for r_i in range(len(minor_lat)):
    for m_i in range(maskarr.shape[0]):
        if maskarr[m_i,r_coord_j[r_i],r_coord_i[r_i]] == 1:
            r_minor_ind[m_i].append(r_i)

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time_dt = np.array(minor_time_l)

minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['ammonium']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['nitrate']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['phosphate']) # mmol/m3
minor_tn = np.array(minor_nc.variables['total_nitrogen'])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

r_minor_st_in = 84 # index for start of 1997
r_minor_en_in = 287 # index for end of 2013
r_minor_flo = [[] for i in range(maskarr.shape[0])]
r_minor_tn = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    r_minor_flo[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tn[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tn[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (17,12) because this data set is 17 years (1997-2013)
# then average over 17 years to get year average
ry1 = 17
#r_minor_flo_ssd = np.nanmean(np.nansum(np.array(r_minor_flo[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_flo_nsd = np.nanmean(np.nansum(np.array(r_minor_flo[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_ssd = np.array(()) # no rivers fall into these regions
r_minor_flo_nsd = np.array(())
r_minor_flo_occ = np.nanmean(np.nansum(np.array(r_minor_flo[2][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_spp = np.nanmean(np.nansum(np.array(r_minor_flo[3][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_smm = np.nanmean(np.nansum(np.array(r_minor_flo[4][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_ven = np.nanmean(np.nansum(np.array(r_minor_flo[5][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_sbb = np.nanmean(np.nansum(np.array(r_minor_flo[6][0]),axis=0).reshape(ry1,12),axis=0)

#r_minor_tnn_ssd = np.nanmean(np.nansum(np.array(r_minor_tn[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_tnn_nsd = np.nanmean(np.nansum(np.array(r_minor_tn[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_ssd = np.array(()) # no rivers fall into these regions
r_minor_tnn_nsd = np.array(())
r_minor_tnn_occ = np.nanmean(np.nansum(np.array(r_minor_tn[2][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_spp = np.nanmean(np.nansum(np.array(r_minor_tn[3][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_smm = np.nanmean(np.nansum(np.array(r_minor_tn[4][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_ven = np.nanmean(np.nansum(np.array(r_minor_tn[5][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_sbb = np.nanmean(np.nansum(np.array(r_minor_tn[6][0]),axis=0).reshape(ry1,12),axis=0)

# sum different river datasets
r_flo_ssd = r_major_flo_ssd
r_flo_nsd = r_major_flo_nsd
r_flo_occ = r_major_flo_occ+r_minor_flo_occ
r_flo_spp = r_major_flo_occ+r_minor_flo_spp
r_flo_smm = r_major_flo_occ+r_minor_flo_smm
r_flo_ven = r_major_flo_occ+r_minor_flo_ven
r_flo_sbb = r_major_flo_occ+r_minor_flo_sbb

r_tnn_ssd = r_major_tnn_ssd
r_tnn_nsd = r_major_tnn_nsd
r_tnn_occ = r_major_tnn_occ+r_minor_tnn_occ
r_tnn_spp = r_major_tnn_occ+r_minor_tnn_spp
r_tnn_smm = r_major_tnn_occ+r_minor_tnn_smm
r_tnn_ven = r_major_tnn_occ+r_minor_tnn_ven
r_tnn_sbb = r_major_tnn_occ+r_minor_tnn_sbb

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2013
potw_1997 = 313 # 1997-01-31
potw_2013 = 517 # 2014-01-13

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
major_on  = np.array(potw_ma_nc.variables['ON']) # mmol/m3
major_po4 = np.array(potw_ma_nc.variables['PO4']) # mmol/m3
major_op  = np.array(potw_ma_nc.variables['OP']) # mmol/m3
major_fe  = np.array(potw_ma_nc.variables['Fe'])  # mmol/m3
major_pH  = np.array(potw_ma_nc.variables['pH'])
major_alk = np.array(potw_ma_nc.variables['alkalinity'])
major_temp = np.array(potw_ma_nc.variables['temperature'])
major_salt = np.array(potw_ma_nc.variables['salinity'])
major_toc  = np.array(potw_ma_nc.variables['TOC'])

major_tn = major_nh4+major_no3+major_no2+major_on
major_tp = major_po4+major_op

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan

p_major_flo = [[] for i in range(maskarr.shape[0])]
p_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())

# turn to array so can sum all potw in region up
# then reshape to (17,12) because this data set is 17 years
# then average over 17 years to get year average
ry0 = 17

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
for r_i in range(len(r_minor_ind)):
    p_minor_flo[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())
    p_minor_tn[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]*minor_tn[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())

# turn to array so can sum all minor potw in region up
p_minor_flo_ssd = np.nansum(np.array(p_minor_flo[0][0]),axis=0)
p_minor_flo_nsd = np.nansum(np.array(p_minor_flo[1][0]),axis=0)
p_minor_flo_occ = np.nansum(np.array(p_minor_flo[2][0]),axis=0)
p_minor_flo_spp = np.nansum(np.array(p_minor_flo[3][0]),axis=0)
p_minor_flo_smm = np.nansum(np.array(p_minor_flo[4][0]),axis=0)
p_minor_flo_ven = np.nansum(np.array(p_minor_flo[5][0]),axis=0)
p_minor_flo_sbb = np.nansum(np.array(p_minor_flo[6][0]),axis=0)

p_minor_tnn_ssd = np.nansum(np.array(p_minor_tn[0][0]),axis=0)
p_minor_tnn_nsd = np.nansum(np.array(p_minor_tn[1][0]),axis=0)
p_minor_tnn_occ = np.nansum(np.array(p_minor_tn[2][0]),axis=0)
p_minor_tnn_spp = np.nansum(np.array(p_minor_tn[3][0]),axis=0)
p_minor_tnn_smm = np.nansum(np.array(p_minor_tn[4][0]),axis=0)
p_minor_tnn_ven = np.nansum(np.array(p_minor_tn[5][0]),axis=0)
p_minor_tnn_sbb = np.nansum(np.array(p_minor_tn[6][0]),axis=0)

# sum major and minor potw datasets
p_flo_ssd = p_major_flo_ssd+p_minor_flo_ssd
p_flo_nsd = p_major_flo_nsd+p_minor_flo_nsd
p_flo_occ = p_major_flo_occ+p_minor_flo_occ
p_flo_spp = p_major_flo_occ+p_minor_flo_spp
p_flo_smm = p_major_flo_occ+p_minor_flo_smm
p_flo_ven = p_major_flo_occ+p_minor_flo_ven
p_flo_sbb = p_major_flo_occ+p_minor_flo_sbb

p_tnn_ssd = p_major_tnn_ssd+p_minor_tnn_ssd
p_tnn_nsd = p_major_tnn_nsd+p_minor_tnn_nsd
p_tnn_occ = p_major_tnn_occ+p_minor_tnn_occ
p_tnn_spp = p_major_tnn_occ+p_minor_tnn_spp
p_tnn_smm = p_major_tnn_occ+p_minor_tnn_smm
p_tnn_ven = p_major_tnn_occ+p_minor_tnn_ven
p_tnn_sbb = p_major_tnn_occ+p_minor_tnn_sbb

#############
# plot
#############
a_yr = atmos_plt
p_yr = np.array((np.nanmean(p_tnn_ssd),np.nanmean(p_tnn_nsd),np.nanmean(p_tnn_occ),np.nanmean(p_tnn_spp),np.nanmean(p_tnn_smm),np.nanmean(p_tnn_ven),np.nanmean(p_tnn_sbb)))
r_yr = np.array((np.nanmean(r_tnn_ssd),np.nanmean(r_tnn_nsd),np.nanmean(r_tnn_occ),np.nanmean(r_tnn_spp),np.nanmean(r_tnn_smm),np.nanmean(r_tnn_ven),np.nanmean(r_tnn_sbb)))

figw = 14
figh = 8
regions = ['S SD','N SD','OC','San Pedro','Santa Monica','Ventura','Santa Barbara']
width = 0.1
axis_font = 18
#savename = './figs/inputs_compare_region.pdf'
savename = './figs/inputs_compare_region_1997_2013_nolog.pdf'

plt.ion()
fig,ax = plt.subplots(1,1,figsize=[figw,figh])
x_ind = np.arange(len(regions))
ax.bar(x_ind,a_yr,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
ax.bar(x_ind+width,p_yr,color='orange',width=width,label='All POTWs')
ax.bar(x_ind+(2*width),r_yr,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
ax.set_xticks([width,1+width,2+width,3+width,4+width,5+width,6+width])
ax.set_xticklabels(regions)
#ax.set_yscale('log')
#ax.set_ybound(lower=10E-1,upper=25E5)
ax.set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
#ax.tick_params(axis='both',which='minor',labelsize=axis_font)
ax.legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)

plt.savefig(savename,bbox_inches='tight')

