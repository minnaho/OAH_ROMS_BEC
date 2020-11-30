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
#major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc'
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_updated_14_years_1997_2010_monthly.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc'
ocsd_data = '/data/project1/minnaho/potw_outfall_data/OO10-OCSD _REvised 06052020.xlsx'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
setting = 'bight'
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
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

#major_lat = np.array(major_nc.variables['latitude'][0,:])
#major_lon = np.array(major_nc.variables['longitude'][0,:])
major_lat = np.array(major_nc.variables['latitude'][:])
major_lon = np.array(major_nc.variables['longitude'][:])

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
major_tp = np.array(major_nc.variables['total_phosphorus']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan

r_major_flo = [[] for i in range(maskarr.shape[0])]
r_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
r_major_tp = [[] for i in range(maskarr.shape[0])] # TN flux
for r_i in range(len(r_major_ind)):
    r_major_flo[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tn[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tn[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tp[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tp[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (10,12) because this data set is 10 years
# then average over 10 years to get year average
ry0 = 14

r_major_flo_ssd = np.nansum(np.nansum(np.array(r_major_flo[0][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_nsd = np.nansum(np.nansum(np.array(r_major_flo[1][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_occ = np.nansum(np.nansum(np.array(r_major_flo[2][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_spp = np.nansum(np.nansum(np.array(r_major_flo[3][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_smm = np.nansum(np.nansum(np.array(r_major_flo[4][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_ven = np.nansum(np.nansum(np.array(r_major_flo[5][0]),axis=0).reshape(ry0,12),axis=1)
r_major_flo_sbb = np.nansum(np.nansum(np.array(r_major_flo[6][0]),axis=0).reshape(ry0,12),axis=1)

r_major_tnn_ssd = np.nansum(np.nansum(np.array(r_major_tn[0][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_nsd = np.nansum(np.nansum(np.array(r_major_tn[1][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_occ = np.nansum(np.nansum(np.array(r_major_tn[2][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_spp = np.nansum(np.nansum(np.array(r_major_tn[3][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_smm = np.nansum(np.nansum(np.array(r_major_tn[4][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_ven = np.nansum(np.nansum(np.array(r_major_tn[5][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tnn_sbb = np.nansum(np.nansum(np.array(r_major_tn[6][0]),axis=0).reshape(ry0,12),axis=1)

r_major_tpp_ssd = np.nansum(np.nansum(np.array(r_major_tp[0][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_nsd = np.nansum(np.nansum(np.array(r_major_tp[1][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_occ = np.nansum(np.nansum(np.array(r_major_tp[2][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_spp = np.nansum(np.nansum(np.array(r_major_tp[3][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_smm = np.nansum(np.nansum(np.array(r_major_tp[4][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_ven = np.nansum(np.nansum(np.array(r_major_tp[5][0]),axis=0).reshape(ry0,12),axis=1)
r_major_tpp_sbb = np.nansum(np.nansum(np.array(r_major_tp[6][0]),axis=0).reshape(ry0,12),axis=1)

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
minor_tp = np.array(minor_nc.variables['total_phosphorus'])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_tp[minor_tp>1E20] = np.nan

r_minor_st_in = 84 # index for start of 1997
r_minor_en_in = 251 # index for end of 2010
r_minor_flo = [[] for i in range(maskarr.shape[0])]
r_minor_tn = [[] for i in range(maskarr.shape[0])]
r_minor_tp = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    r_minor_flo[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tn[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tn[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tp[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tp[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (14,12) because this data set is 14 years (1997-2010)
# then average over 14 years to get year average
ry1 = 14
#r_minor_flo_ssd = np.nanmean(np.nansum(np.array(r_minor_flo[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_flo_nsd = np.nanmean(np.nansum(np.array(r_minor_flo[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_ssd = np.array(()) # no rivers fall into these regions
r_minor_flo_nsd = np.array(())
r_minor_flo_occ = np.nansum(np.nansum(np.array(r_minor_flo[2][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_flo_spp = np.nansum(np.nansum(np.array(r_minor_flo[3][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_flo_smm = np.nansum(np.nansum(np.array(r_minor_flo[4][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_flo_ven = np.nansum(np.nansum(np.array(r_minor_flo[5][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_flo_sbb = np.nansum(np.nansum(np.array(r_minor_flo[6][0]),axis=0).reshape(ry1,12),axis=1)

#r_minor_tnn_ssd = np.nanmean(np.nansum(np.array(r_minor_tn[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_tnn_nsd = np.nanmean(np.nansum(np.array(r_minor_tn[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_ssd = np.array(()) # no rivers fall into these regions
r_minor_tnn_nsd = np.array(())
r_minor_tnn_occ = np.nansum(np.nansum(np.array(r_minor_tn[2][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_spp = np.nansum(np.nansum(np.array(r_minor_tn[3][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_smm = np.nansum(np.nansum(np.array(r_minor_tn[4][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_ven = np.nansum(np.nansum(np.array(r_minor_tn[5][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_sbb = np.nansum(np.nansum(np.array(r_minor_tn[6][0]),axis=0).reshape(ry1,12),axis=1)

#r_minor_tpp_ssd = np.nanmean(np.nansum(np.array(r_minor_tn[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_tpp_nsd = np.nanmean(np.nansum(np.array(r_minor_tn[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tpp_ssd = np.array(()) # no rivers fall into these regions
r_minor_tpp_nsd = np.array(())
r_minor_tpp_occ = np.nansum(np.nansum(np.array(r_minor_tn[2][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_spp = np.nansum(np.nansum(np.array(r_minor_tn[3][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_smm = np.nansum(np.nansum(np.array(r_minor_tn[4][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_ven = np.nansum(np.nansum(np.array(r_minor_tn[5][0]),axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_sbb = np.nansum(np.nansum(np.array(r_minor_tn[6][0]),axis=0).reshape(ry1,12),axis=1)

# sum different river datasets
r_flo_ssd = np.nanmean(r_major_flo_ssd)
r_flo_nsd = np.nanmean(r_major_flo_nsd)
r_flo_occ = np.nanmean(r_major_flo_occ+r_minor_flo_occ)
r_flo_spp = np.nanmean(r_major_flo_spp+r_minor_flo_spp)
r_flo_smm = np.nanmean(r_major_flo_smm+r_minor_flo_smm)
r_flo_ven = np.nanmean(r_major_flo_ven+r_minor_flo_ven)
r_flo_sbb = np.nanmean(r_major_flo_sbb+r_minor_flo_sbb)

r_tnn_ssd = np.nanmean(r_major_tnn_ssd)
r_tnn_nsd = np.nanmean(r_major_tnn_nsd)
r_tnn_occ = np.nanmean(r_major_tnn_occ+r_minor_tnn_occ)
r_tnn_spp = np.nanmean(r_major_tnn_spp+r_minor_tnn_spp)
r_tnn_smm = np.nanmean(r_major_tnn_smm+r_minor_tnn_smm)
r_tnn_ven = np.nanmean(r_major_tnn_ven+r_minor_tnn_ven)
r_tnn_sbb = np.nanmean(r_major_tnn_sbb+r_minor_tnn_sbb)

r_tpp_ssd = np.nanmean(r_major_tpp_ssd)
r_tpp_nsd = np.nanmean(r_major_tpp_nsd)
r_tpp_occ = np.nanmean(r_major_tpp_occ+r_minor_tpp_occ)
r_tpp_spp = np.nanmean(r_major_tpp_spp+r_minor_tpp_spp)
r_tpp_smm = np.nanmean(r_major_tpp_smm+r_minor_tpp_smm)
r_tpp_ven = np.nanmean(r_major_tpp_ven+r_minor_tpp_ven)
r_tpp_sbb = np.nanmean(r_major_tpp_sbb+r_minor_tpp_sbb)

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units)
# start and end indices of potw for 1997-2010
potw_1997 = 313 # 1997-01-31
potw_2013 = 481 # 2011-01-01

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

# replace NO3/NO2 OCSD data with Martha's new calculations of NO3 + NO2
ocsd_df = pd.read_excel(ocsd_data,header=None,sheet_name='Sheet1')
# new NO3+NO2
# is it actually mg/L, not kg/m3? makes more sense as mg/L
kg_to_g = 1000
g_to_mol = 1./14
mol_to_mmol = 1000
mgL_to_mmolm3 = 1000./14

# starts at 12-1970 instead of 1-1971 [potw_1997+1:potw_2013+1]
ocsd_nox_l = list(ocsd_df[3][1:])
for i in range(len(major_nh4[:,2,2])-len(ocsd_df[3][1:])):
    ocsd_nox_l.append(np.nan)

ocsd_nox = np.array(ocsd_nox_l).astype(float)*mgL_to_mmolm3

# replace ocsd major tn data with new calculations
major_tn[:,2,2] = major_nh4[:,2,2]+major_on[:,2,2]+ocsd_nox

p_major_flo = [[] for i in range(maskarr.shape[0])]
p_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
p_major_tp = [[] for i in range(maskarr.shape[0])] # TP flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_tp[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tp[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())



# turn to array so can sum all potw in region up
# then reshape to (14,12) because this data set is 14 years 1997-2010
# then average over 14 years to get year average
ry0 = 14

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
for r_i in range(len(r_minor_ind)):
    p_minor_flo[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())
    p_minor_tn[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]*minor_tn[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())
    p_minor_tp[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]*minor_po4[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())

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

p_minor_tpp_ssd = np.nansum(np.array(p_minor_tp[0][0]),axis=0)
p_minor_tpp_nsd = np.nansum(np.array(p_minor_tp[1][0]),axis=0)
p_minor_tpp_occ = np.nansum(np.array(p_minor_tp[2][0]),axis=0)
p_minor_tpp_spp = np.nansum(np.array(p_minor_tp[3][0]),axis=0)
p_minor_tpp_smm = np.nansum(np.array(p_minor_tp[4][0]),axis=0)
p_minor_tpp_ven = np.nansum(np.array(p_minor_tp[5][0]),axis=0)
p_minor_tpp_sbb = np.nansum(np.array(p_minor_tp[6][0]),axis=0)

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

# Esondido (nsd) actually is a minor POTW, add it to nsd


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

p_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_nsd)+inland_tnn[1],np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_sbb)))

r_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_sbb)))

p_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_nsd)+inland_tpp[1],np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tpp_sbb)))
r_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tpp_sbb)))

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

