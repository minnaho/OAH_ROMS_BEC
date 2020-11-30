# median annual load for each region
# find annual load for 1997-2010 then median 
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

# calculate area of each region from old table 2 in km^2
# mean of km2 from TN and TP column
# Southern California Bight 
#scb_area = np.mean((4.78E7/3517,2.83E6/210))
## Santa Barbara
#sbb_area = np.mean((3.67E4/44,1.53E4/19))
## ventura 
#ven_area = np.mean((6.04E5/100,1.6E5/27))
## santa monica bay 
#smm_area = np.mean((1.56E7/15988,1.01E6/1038))
## san pedro 
#spp_area = np.mean((2.32E7/2434,7.69E5/81))/2
## orange county 
#occ_area = np.mean((2.32E7/2434,7.69E5/81))/2
## north san diego
#nsd_area = np.mean((5.22E5/64,1.13E5/14))
## south san diego
#ssd_area = np.mean((7.81E6/2132,7.56E5/206))

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


############
# load grid
############
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])
pm_nc = np.array(grid_nc.variables['pm'])
pn_nc = np.array(grid_nc.variables['pn'])


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

maskarr[4,:,:] = np.transpose(np.array(h5py.File('masksm.mat','r')['masksm']))

maskarr[maskarr==0] = np.nan

# uncomment to see masks plotted
#colors = ['spring','viridis_r','gray','rainbow','gnuplot_r','seismic','Greens_r']
#plt.ion()
#for i in range(len(maskarr)):
#    plt.imshow(maskarr[i]*mask_nc,cmap=colors[i],origin='lower')

s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

################
# load atmos data
################
dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')
#m2_to_hectare = 10000
m2_resolution_grid = 330*330

oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_resolution_grid*mask_nc*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_resolution_grid*mask_nc*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_resolution_grid*mask_nc*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_resolution_grid*mask_nc*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

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

# annual load per region
atmos_plt = np.nansum(np.nansum((oxn_all+redn_all),axis=1),axis=1)
a_bight = np.nansum(atmos_plt)
a_yr = np.append(atmos_plt,a_bight)
atmos_plt = a_yr[:]

# calculate area of each region
# size of each grid cell 
pm_res = 1E-3/pm_nc
pn_res = 1E-3/pn_nc
grid_area = pm_res*pn_res # km^2

# km^2 of each region
grid_km = np.empty((maskarr.shape[0]+1))
grid_km[-1] = np.nan
for r_i in range(maskarr.shape[0]):
    grid_km[r_i] = np.nansum(grid_area*maskarr[r_i,:,:])

# full bight size
grid_km[-1] = np.nansum(grid_km)

atmos_plt_km = atmos_plt/grid_km

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

major_din = major_nh4+major_no3

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan
major_din[major_din>1E20] = np.nan

r_major_flo = [[] for i in range(maskarr.shape[0])]
r_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
r_major_tp = [[] for i in range(maskarr.shape[0])] # TN flux
r_major_din = [[] for i in range(maskarr.shape[0])] # DIN flux
r_major_dip = [[] for i in range(maskarr.shape[0])] # DIN flux
for r_i in range(len(r_major_ind)):
    r_major_flo[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tn[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tn[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tp[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tp[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_din[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_din[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_dip[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_po4[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (10,12) because this data set is 10 years
# then average over 10 years to get year average
ry0 = 14

# m3/month flow 
r_major_flo_ssd = np.nansum(np.nansum(np.array(r_major_flo[0][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1) 
r_major_flo_nsd = np.nansum(np.nansum(np.array(r_major_flo[1][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1) 
r_major_flo_occ = np.nansum(np.nansum(np.array(r_major_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1) 
r_major_flo_spp = np.nansum(np.nansum(np.array(r_major_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)
r_major_flo_smm = np.nansum(np.nansum(np.array(r_major_flo[4][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)
r_major_flo_ven = np.nansum(np.nansum(np.array(r_major_flo[5][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)
r_major_flo_sbb = np.nansum(np.nansum(np.array(r_major_flo[6][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)

# annual loads
r_major_tnn_ssd = np.nansum(np.nansum(np.array(r_major_tn[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tnn_nsd = np.nansum(np.nansum(np.array(r_major_tn[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tnn_occ = np.nansum(np.nansum(np.array(r_major_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tnn_spp = np.nansum(np.nansum(np.array(r_major_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tnn_smm = np.nansum(np.nansum(np.array(r_major_tn[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tnn_ven = np.nansum(np.nansum(np.array(r_major_tn[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tnn_sbb = np.nansum(np.nansum(np.array(r_major_tn[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
                                                                                                       
r_major_tpp_ssd = np.nansum(np.nansum(np.array(r_major_tp[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tpp_nsd = np.nansum(np.nansum(np.array(r_major_tp[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tpp_occ = np.nansum(np.nansum(np.array(r_major_tp[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_tpp_spp = np.nansum(np.nansum(np.array(r_major_tp[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tpp_smm = np.nansum(np.nansum(np.array(r_major_tp[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tpp_ven = np.nansum(np.nansum(np.array(r_major_tp[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_tpp_sbb = np.nansum(np.nansum(np.array(r_major_tp[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)

r_major_din_ssd = np.nansum(np.nansum(np.array(r_major_din[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_din_nsd = np.nansum(np.nansum(np.array(r_major_din[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_din_occ = np.nansum(np.nansum(np.array(r_major_din[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_din_spp = np.nansum(np.nansum(np.array(r_major_din[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_din_smm = np.nansum(np.nansum(np.array(r_major_din[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_din_ven = np.nansum(np.nansum(np.array(r_major_din[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_din_sbb = np.nansum(np.nansum(np.array(r_major_din[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)

r_major_dip_ssd = np.nansum(np.nansum(np.array(r_major_dip[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_dip_nsd = np.nansum(np.nansum(np.array(r_major_dip[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_dip_occ = np.nansum(np.nansum(np.array(r_major_dip[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_major_dip_spp = np.nansum(np.nansum(np.array(r_major_dip[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_dip_smm = np.nansum(np.nansum(np.array(r_major_dip[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_dip_ven = np.nansum(np.nansum(np.array(r_major_dip[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_major_dip_sbb = np.nansum(np.nansum(np.array(r_major_dip[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)

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

minor_din = minor_nh4+minor_no3
minor_dip = minor_po4

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_tp[minor_tp>1E20] = np.nan
minor_din[minor_din>1E20] = np.nan
minor_dip[minor_dip>1E20] = np.nan

r_minor_st_in = 84 # index for start of 1997
r_minor_en_in = 251 # index for end of 2010
r_minor_flo = [[] for i in range(maskarr.shape[0])]
r_minor_tn = [[] for i in range(maskarr.shape[0])]
r_minor_tp = [[] for i in range(maskarr.shape[0])]
r_minor_din = [[] for i in range(maskarr.shape[0])]
r_minor_dip = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    r_minor_flo[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tn[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tn[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tp[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tp[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_din[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_din[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_dip[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_dip[r_minor_st_in:r_minor_en_in+1,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (14,12) because this data set is 14 years (1997-2010)
# then average over 14 years to get year average
ry1 = 14


r_minor_flo_ssd = np.array(()) # no rivers fall into these regions
r_minor_flo_nsd = np.array(())
r_minor_flo_occ = np.nansum(np.nansum(np.array(r_minor_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry1,12),axis=1) 
r_minor_flo_spp = np.nansum(np.nansum(np.array(r_minor_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry1,12),axis=1)
r_minor_flo_smm = np.nansum(np.nansum(np.array(r_minor_flo[4][0])*s_to_d*d_to_mo,axis=0).reshape(ry1,12),axis=1)
r_minor_flo_ven = np.nansum(np.nansum(np.array(r_minor_flo[5][0])*s_to_d*d_to_mo,axis=0).reshape(ry1,12),axis=1)
r_minor_flo_sbb = np.nansum(np.nansum(np.array(r_minor_flo[6][0])*s_to_d*d_to_mo,axis=0).reshape(ry1,12),axis=1)

r_minor_tnn_ssd = np.array(()) # no rivers fall into these regions
r_minor_tnn_nsd = np.array(())
r_minor_tnn_occ = np.nansum(np.nansum(np.array(r_minor_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1) 
r_minor_tnn_spp = np.nansum(np.nansum(np.array(r_minor_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_smm = np.nansum(np.nansum(np.array(r_minor_tn[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_ven = np.nansum(np.nansum(np.array(r_minor_tn[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tnn_sbb = np.nansum(np.nansum(np.array(r_minor_tn[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
                                                                                                       
r_minor_tpp_ssd = np.array(()) # no rivers fall into these regions
r_minor_tpp_nsd = np.array(())
r_minor_tpp_occ = np.nansum(np.nansum(np.array(r_minor_tp[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1) 
r_minor_tpp_spp = np.nansum(np.nansum(np.array(r_minor_tp[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_smm = np.nansum(np.nansum(np.array(r_minor_tp[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_ven = np.nansum(np.nansum(np.array(r_minor_tp[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)
r_minor_tpp_sbb = np.nansum(np.nansum(np.array(r_minor_tp[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry1,12),axis=1)

r_minor_din_ssd = np.array(())
r_minor_din_nsd = np.array(())
r_minor_din_occ = np.nansum(np.nansum(np.array(r_minor_din[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_minor_din_spp = np.nansum(np.nansum(np.array(r_minor_din[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_din_smm = np.nansum(np.nansum(np.array(r_minor_din[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_din_ven = np.nansum(np.nansum(np.array(r_minor_din[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_din_sbb = np.nansum(np.nansum(np.array(r_minor_din[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)

r_minor_dip_ssd = np.array(())
r_minor_dip_nsd = np.array(())
r_minor_dip_occ = np.nansum(np.nansum(np.array(r_minor_dip[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
r_minor_dip_spp = np.nansum(np.nansum(np.array(r_minor_dip[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_dip_smm = np.nansum(np.nansum(np.array(r_minor_dip[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_dip_ven = np.nansum(np.nansum(np.array(r_minor_dip[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
r_minor_dip_sbb = np.nansum(np.nansum(np.array(r_minor_dip[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)


# sum different river datasets
# and get median for each region
r_flo_ssd = np.median(r_major_flo_ssd)
r_flo_nsd = np.median(r_major_flo_nsd)
r_flo_occ = np.median(r_major_flo_occ+r_minor_flo_occ)
r_flo_spp = np.median(r_major_flo_spp+r_minor_flo_spp)
r_flo_smm = np.median(r_major_flo_smm+r_minor_flo_smm)
r_flo_ven = np.median(r_major_flo_ven+r_minor_flo_ven)
r_flo_sbb = np.median(r_major_flo_sbb+r_minor_flo_sbb)
r_flo_scb = np.median(r_major_flo_ssd+r_major_flo_nsd+r_major_flo_occ+r_major_flo_spp+r_major_flo_smm+r_major_flo_ven+r_major_flo_sbb)

r_tnn_ssd = np.median(r_major_tnn_ssd)
r_tnn_nsd = np.median(r_major_tnn_nsd)
r_tnn_occ = np.median(r_major_tnn_occ+r_minor_tnn_occ)
r_tnn_spp = np.median(r_major_tnn_spp+r_minor_tnn_spp)
r_tnn_smm = np.median(r_major_tnn_smm+r_minor_tnn_smm)
r_tnn_ven = np.median(r_major_tnn_ven+r_minor_tnn_ven)
r_tnn_sbb = np.median(r_major_tnn_sbb+r_minor_tnn_sbb)
r_tnn_scb = np.median(r_major_tnn_ssd+r_major_tnn_nsd+r_major_tnn_occ+r_major_tnn_spp+r_major_tnn_smm+r_major_tnn_ven+r_major_tnn_sbb)

r_tpp_ssd = np.median(r_major_tpp_ssd)
r_tpp_nsd = np.median(r_major_tpp_nsd)
r_tpp_occ = np.median(r_major_tpp_occ+r_minor_tpp_occ)
r_tpp_spp = np.median(r_major_tpp_spp+r_minor_tpp_spp)
r_tpp_smm = np.median(r_major_tpp_smm+r_minor_tpp_smm)
r_tpp_ven = np.median(r_major_tpp_ven+r_minor_tpp_ven)
r_tpp_sbb = np.median(r_major_tpp_sbb+r_minor_tpp_sbb)
r_tpp_scb = np.median(r_major_tpp_ssd+r_major_tpp_nsd+r_major_tpp_occ+r_major_tpp_spp+r_major_tpp_smm+r_major_tpp_ven+r_major_tpp_sbb)

r_din_ssd = np.median(r_major_din_ssd)
r_din_nsd = np.median(r_major_din_nsd)
r_din_occ = np.median(r_major_din_occ+r_minor_din_occ)
r_din_spp = np.median(r_major_din_spp+r_minor_din_spp)
r_din_smm = np.median(r_major_din_smm+r_minor_din_smm)
r_din_ven = np.median(r_major_din_ven+r_minor_din_ven)
r_din_sbb = np.median(r_major_din_sbb+r_minor_din_sbb)
r_din_scb = np.median(r_major_din_ssd+r_major_din_nsd+r_major_din_occ+r_major_din_spp+r_major_din_smm+r_major_din_ven+r_major_din_sbb)

r_dip_ssd = np.median(r_major_dip_ssd)
r_dip_nsd = np.median(r_major_dip_nsd)
r_dip_occ = np.median(r_major_dip_occ+r_minor_dip_occ)
r_dip_spp = np.median(r_major_dip_spp+r_minor_dip_spp)
r_dip_smm = np.median(r_major_dip_smm+r_minor_dip_smm)
r_dip_ven = np.median(r_major_dip_ven+r_minor_dip_ven)
r_dip_sbb = np.median(r_major_dip_sbb+r_minor_dip_sbb)
r_dip_scb = np.median(r_major_dip_ssd+r_major_dip_nsd+r_major_dip_occ+r_major_dip_spp+r_major_dip_smm+r_major_dip_ven+r_major_dip_sbb)

# mean river
r_mean_flo_ssd = np.nanmean(r_major_flo_ssd)
r_mean_flo_nsd = np.nanmean(r_major_flo_nsd)
r_mean_flo_occ = np.nanmean(r_major_flo_occ+r_minor_flo_occ)
r_mean_flo_spp = np.nanmean(r_major_flo_spp+r_minor_flo_spp)
r_mean_flo_smm = np.nanmean(r_major_flo_smm+r_minor_flo_smm)
r_mean_flo_ven = np.nanmean(r_major_flo_ven+r_minor_flo_ven)
r_mean_flo_sbb = np.nanmean(r_major_flo_sbb+r_minor_flo_sbb)
r_mean_flo_scb = r_flo_ssd+r_flo_nsd+r_flo_occ+r_flo_spp+r_flo_smm+r_flo_ven+r_flo_sbb

r_mean_tnn_ssd = np.nanmean(r_major_tnn_ssd)
r_mean_tnn_nsd = np.nanmean(r_major_tnn_nsd)
r_mean_tnn_occ = np.nanmean(r_major_tnn_occ+r_minor_tnn_occ)
r_mean_tnn_spp = np.nanmean(r_major_tnn_spp+r_minor_tnn_spp)
r_mean_tnn_smm = np.nanmean(r_major_tnn_smm+r_minor_tnn_smm)
r_mean_tnn_ven = np.nanmean(r_major_tnn_ven+r_minor_tnn_ven)
r_mean_tnn_sbb = np.nanmean(r_major_tnn_sbb+r_minor_tnn_sbb)
r_mean_tnn_scb = r_tnn_ssd+r_tnn_nsd+r_tnn_occ+r_tnn_spp+r_tnn_smm+r_tnn_ven+r_tnn_sbb

r_mean_tpp_ssd = np.nanmean(r_major_tpp_ssd)
r_mean_tpp_nsd = np.nanmean(r_major_tpp_nsd)
r_mean_tpp_occ = np.nanmean(r_major_tpp_occ+r_minor_tpp_occ)
r_mean_tpp_spp = np.nanmean(r_major_tpp_spp+r_minor_tpp_spp)
r_mean_tpp_smm = np.nanmean(r_major_tpp_smm+r_minor_tpp_smm)
r_mean_tpp_ven = np.nanmean(r_major_tpp_ven+r_minor_tpp_ven)
r_mean_tpp_sbb = np.nanmean(r_major_tpp_sbb+r_minor_tpp_sbb)
r_mean_tpp_scb = r_tpp_ssd+r_tpp_nsd+r_tpp_occ+r_tpp_spp+r_tpp_smm+r_tpp_ven+r_tpp_sbb

r_mean_din_ssd = np.nanmean(r_major_din_ssd)
r_mean_din_nsd = np.nanmean(r_major_din_nsd)
r_mean_din_occ = np.nanmean(r_major_din_occ+r_minor_din_occ)
r_mean_din_spp = np.nanmean(r_major_din_spp+r_minor_din_spp)
r_mean_din_smm = np.nanmean(r_major_din_smm+r_minor_din_smm)
r_mean_din_ven = np.nanmean(r_major_din_ven+r_minor_din_ven)
r_mean_din_sbb = np.nanmean(r_major_din_sbb+r_minor_din_sbb)
r_mean_din_scb = r_din_ssd+r_din_nsd+r_din_occ+r_din_spp+r_din_smm+r_din_ven+r_din_sbb

r_mean_dip_ssd = np.nanmean(r_major_dip_ssd)
r_mean_dip_nsd = np.nanmean(r_major_dip_nsd)
r_mean_dip_occ = np.nanmean(r_major_dip_occ+r_minor_dip_occ)
r_mean_dip_spp = np.nanmean(r_major_dip_spp+r_minor_dip_spp)
r_mean_dip_smm = np.nanmean(r_major_dip_smm+r_minor_dip_smm)
r_mean_dip_ven = np.nanmean(r_major_dip_ven+r_minor_dip_ven)
r_mean_dip_sbb = np.nanmean(r_major_dip_sbb+r_minor_dip_sbb)
r_mean_dip_scb = r_dip_ssd+r_dip_nsd+r_dip_occ+r_dip_spp+r_dip_smm+r_dip_ven+r_dip_sbb

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
major_din = major_nh4+major_no3+major_no2
major_dip = major_po4

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_din[major_din>1E20]=np.nan
major_dip[major_dip>1E20]=np.nan

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
p_major_din = [[] for i in range(maskarr.shape[0])] # TP flux
p_major_dip = [[] for i in range(maskarr.shape[0])] # TP flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_tp[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tp[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_din[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_din[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_dip[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_dip[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())



# turn to array so can sum all potw in region up
# then reshape to (14,12) because this data set is 14 years 1997-2010
# then average over 14 years to get year average
ry0 = 14

p_major_flo_ssd = np.nansum(np.nansum(np.array(p_major_flo[0][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1) 
p_major_flo_nsd = np.zeros((ry0))
p_major_flo_occ = np.nansum(np.nansum(np.array(p_major_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1) 
p_major_flo_spp = np.nansum(np.nansum(np.array(p_major_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)
p_major_flo_smm = np.nansum(np.nansum(np.array(p_major_flo[4][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1)
p_major_flo_ven = np.zeros((ry0))
p_major_flo_sbb = np.zeros((ry0))

p_major_tnn_ssd = np.nansum(np.nansum(np.array(p_major_tn[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_tnn_nsd = np.zeros((ry0))
p_major_tnn_occ = np.nansum(np.nansum(np.array(p_major_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_tnn_spp = np.nansum(np.nansum(np.array(p_major_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_tnn_smm = np.nansum(np.nansum(np.array(p_major_tn[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_tnn_ven = np.zeros((ry0))
p_major_tnn_sbb = np.zeros((ry0))                                                                                                       
p_major_tpp_ssd = np.nansum(np.nansum(np.array(p_major_tp[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_tpp_nsd = np.zeros((ry0))
p_major_tpp_occ = np.nansum(np.nansum(np.array(p_major_tp[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_tpp_spp = np.nansum(np.nansum(np.array(p_major_tp[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_tpp_smm = np.nansum(np.nansum(np.array(p_major_tp[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_tpp_ven = np.zeros((ry0))
p_major_tpp_sbb = np.zeros((ry0))

p_major_din_ssd = np.nansum(np.nansum(np.array(p_major_din[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_din_nsd = np.zeros((ry0))
p_major_din_occ = np.nansum(np.nansum(np.array(p_major_din[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_din_spp = np.nansum(np.nansum(np.array(p_major_din[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_din_smm = np.nansum(np.nansum(np.array(p_major_din[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_din_ven = np.zeros((ry0))
p_major_din_sbb = np.zeros((ry0))

p_major_dip_ssd = np.nansum(np.nansum(np.array(p_major_dip[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_dip_nsd = np.zeros((ry0))
p_major_dip_occ = np.nansum(np.nansum(np.array(p_major_dip[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1) 
p_major_dip_spp = np.nansum(np.nansum(np.array(p_major_dip[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_dip_smm = np.nansum(np.nansum(np.array(p_major_dip[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1)
p_major_dip_ven = np.zeros((ry0))
p_major_dip_sbb = np.zeros((ry0))

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

# inland POTW
# see Inland POTW excel for inland potw data
inland_tnn = np.load('inland_potw_tnn_region.npy')
inland_tpp = np.load('inland_potw_tpp_region.npy')
inland_din = np.load('inland_potw_din_region.npy')
inland_dip = np.load('inland_potw_dip_region.npy')

# inland potw flow by region m3/yr from excel
#ssd,nsd,occ,spp,smb,ven,sbb,scb
#inland_flows = [2348848,17432137,2564159,1.75E8,4941331,53495704,np.nan,255900740]
#inland_flows = [2348592.5,17430240.42,2563880.146,175099510.9,4940793.908,53489884.95,np.nan,255872902.9]
inland_flows = [2.35E+06,17430240.42,2.56E+06,1.75E+08,4.94E+06,5.35E+06,np.nan,2.56E+08]


# Esondido (nsd) actually is a minor POTW, add it to nsd

# turn to array so can sum all minor potw in region up
# annual flow m3/s
p_minor_flo_ssd = np.nansum(np.nansum(np.array(p_minor_flo[0][0])*s_to_d*d_to_mo,axis=0))
p_minor_flo_nsd = np.nansum(np.nansum(np.array(p_minor_flo[1][0])*s_to_d*d_to_mo,axis=0))+inland_flows[1]
p_minor_flo_occ = np.nansum(np.nansum(np.array(p_minor_flo[2][0])*s_to_d*d_to_mo,axis=0))
p_minor_flo_spp = np.nansum(np.nansum(np.array(p_minor_flo[3][0])*s_to_d*d_to_mo,axis=0))
p_minor_flo_smm = np.nansum(np.nansum(np.array(p_minor_flo[4][0])*s_to_d*d_to_mo,axis=0))
p_minor_flo_ven = np.nansum(np.nansum(np.array(p_minor_flo[5][0])*s_to_d*d_to_mo,axis=0))
p_minor_flo_sbb = np.nansum(np.nansum(np.array(p_minor_flo[6][0])*s_to_d*d_to_mo,axis=0))

p_minor_tnn_ssd = np.nansum(np.nansum(np.array(p_minor_tn[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tnn_nsd = np.nansum(np.nansum(np.array(p_minor_tn[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))+inland_tnn[1]
p_minor_tnn_occ = np.nansum(np.nansum(np.array(p_minor_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tnn_spp = np.nansum(np.nansum(np.array(p_minor_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tnn_smm = np.nansum(np.nansum(np.array(p_minor_tn[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tnn_ven = np.nansum(np.nansum(np.array(p_minor_tn[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tnn_sbb = np.nansum(np.nansum(np.array(p_minor_tn[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))

p_minor_tpp_ssd = np.nansum(np.nansum(np.array(p_minor_tp[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tpp_nsd = np.nansum(np.nansum(np.array(p_minor_tp[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))+inland_tpp[1]
p_minor_tpp_occ = np.nansum(np.nansum(np.array(p_minor_tp[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tpp_spp = np.nansum(np.nansum(np.array(p_minor_tp[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tpp_smm = np.nansum(np.nansum(np.array(p_minor_tp[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tpp_ven = np.nansum(np.nansum(np.array(p_minor_tp[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))
p_minor_tpp_sbb = np.nansum(np.nansum(np.array(p_minor_tp[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0))

p_minor_flo_scb = p_minor_flo_ssd+p_minor_flo_nsd+p_minor_flo_occ+p_minor_flo_spp+p_minor_flo_smm+p_minor_flo_ven+p_minor_flo_sbb
p_minor_tnn_scb = p_minor_tnn_ssd+p_minor_tnn_nsd+p_minor_tnn_occ+p_minor_tnn_spp+p_minor_tnn_smm+p_minor_tnn_ven+p_minor_tnn_sbb
p_minor_tpp_scb = p_minor_tpp_ssd+p_minor_tpp_nsd+p_minor_tpp_occ+p_minor_tpp_spp+p_minor_tpp_smm+p_minor_tpp_ven+p_minor_tpp_sbb

# major and minor potw separately
pma_flo_ssd = np.median(p_major_flo_ssd)
pma_flo_nsd = np.median(p_major_flo_nsd)
pma_flo_occ = np.median(p_major_flo_occ)
pma_flo_spp = np.median(p_major_flo_spp)
pma_flo_smm = np.median(p_major_flo_smm)
pma_flo_ven = np.median(p_major_flo_ven)
pma_flo_sbb = np.median(p_major_flo_sbb)
pma_flo_scb = np.median(p_major_flo_ssd+p_major_flo_nsd+p_major_flo_occ+p_major_flo_spp+p_major_flo_smm+p_major_flo_ven+p_major_flo_sbb)

pma_din_ssd = np.median(p_major_din_ssd)
pma_din_nsd = np.median(p_major_din_nsd)
pma_din_occ = np.median(p_major_din_occ)
pma_din_spp = np.median(p_major_din_spp)
pma_din_smm = np.median(p_major_din_smm)
pma_din_ven = np.median(p_major_din_ven)
pma_din_sbb = np.median(p_major_din_sbb)
pma_din_scb = np.median(p_major_din_ssd+p_major_din_nsd+p_major_din_occ+p_major_din_spp+p_major_din_smm+p_major_din_ven+p_major_din_sbb)

pma_tnn_ssd = np.median(p_major_tnn_ssd)
pma_tnn_nsd = np.median(p_major_tnn_nsd)
pma_tnn_occ = np.median(p_major_tnn_occ)
pma_tnn_spp = np.median(p_major_tnn_spp)
pma_tnn_smm = np.median(p_major_tnn_smm)
pma_tnn_ven = np.median(p_major_tnn_ven)
pma_tnn_sbb = np.median(p_major_tnn_sbb)
pma_tnn_scb = np.median(p_major_tnn_ssd+p_major_tnn_nsd+p_major_tnn_occ+p_major_tnn_spp+p_major_tnn_smm+p_major_tnn_ven+p_major_tnn_sbb)

pma_dip_ssd = np.median(p_major_dip_ssd)
pma_dip_nsd = np.median(p_major_dip_nsd)
pma_dip_occ = np.median(p_major_dip_occ)
pma_dip_spp = np.median(p_major_dip_spp)
pma_dip_smm = np.median(p_major_dip_smm)
pma_dip_ven = np.median(p_major_dip_ven)
pma_dip_sbb = np.median(p_major_dip_sbb)
pma_dip_scb = np.median(p_major_dip_ssd+p_major_dip_nsd+p_major_dip_occ+p_major_dip_spp+p_major_dip_smm+p_major_dip_ven+p_major_dip_sbb)

pma_tpp_ssd = np.median(p_major_tpp_ssd)
pma_tpp_nsd = np.median(p_major_tpp_nsd)
pma_tpp_occ = np.median(p_major_tpp_occ)
pma_tpp_spp = np.median(p_major_tpp_spp)
pma_tpp_smm = np.median(p_major_tpp_smm)
pma_tpp_ven = np.median(p_major_tpp_ven)
pma_tpp_sbb = np.median(p_major_tpp_sbb)
pma_tpp_scb = np.median(p_major_tpp_ssd+p_major_tpp_nsd+p_major_tpp_occ+p_major_tpp_spp+p_major_tpp_smm+p_major_tpp_ven+p_major_tpp_sbb)


# sum major and minor potw datasets
p_flo_ssd = np.median(p_major_flo_ssd)+p_minor_flo_ssd
p_flo_nsd = np.median(p_major_flo_nsd)+p_minor_flo_nsd
p_flo_occ = np.median(p_major_flo_occ)+p_minor_flo_occ
p_flo_spp = np.median(p_major_flo_spp)+p_minor_flo_spp
p_flo_smm = np.median(p_major_flo_smm)+p_minor_flo_smm
p_flo_ven = np.median(p_major_flo_ven)+p_minor_flo_ven
p_flo_sbb = np.median(p_major_flo_sbb)+p_minor_flo_sbb
p_flo_scb = p_flo_ssd+p_flo_nsd+p_flo_occ+p_flo_spp+p_flo_smm+p_flo_ven+p_flo_sbb

p_tnn_ssd = np.median(p_major_tnn_ssd)+p_minor_tnn_ssd
p_tnn_nsd = np.median(p_major_tnn_nsd)+p_minor_tnn_nsd
p_tnn_occ = np.median(p_major_tnn_occ)+p_minor_tnn_occ
p_tnn_spp = np.median(p_major_tnn_spp)+p_minor_tnn_spp
p_tnn_smm = np.median(p_major_tnn_smm)+p_minor_tnn_smm
p_tnn_ven = np.median(p_major_tnn_ven)+p_minor_tnn_ven
p_tnn_sbb = np.median(p_major_tnn_sbb)+p_minor_tnn_sbb
p_tnn_scb = p_tnn_ssd+p_tnn_nsd+p_tnn_occ+p_tnn_spp+p_tnn_smm+p_tnn_ven+p_tnn_sbb

p_tpp_ssd = np.median(p_major_tpp_ssd)+p_minor_tpp_ssd
p_tpp_nsd = np.median(p_major_tpp_nsd)+p_minor_tpp_nsd
p_tpp_occ = np.median(p_major_tpp_occ)+p_minor_tpp_occ
p_tpp_spp = np.median(p_major_tpp_spp)+p_minor_tpp_spp
p_tpp_smm = np.median(p_major_tpp_smm)+p_minor_tpp_smm
p_tpp_ven = np.median(p_major_tpp_ven)+p_minor_tpp_ven
p_tpp_sbb = np.median(p_major_tpp_sbb)+p_minor_tpp_sbb
p_tpp_scb = p_tpp_ssd+p_tpp_nsd+p_tpp_occ+p_tpp_spp+p_tpp_smm+p_tpp_ven+p_tpp_sbb

# mean
# major and minor outfalls
p_mean_flo_ssd = np.nanmean(p_major_flo_ssd)+p_minor_flo_ssd
p_mean_flo_nsd = np.nanmean(p_major_flo_nsd)+p_minor_flo_nsd
p_mean_flo_occ = np.nanmean(p_major_flo_occ)+p_minor_flo_occ
p_mean_flo_spp = np.nanmean(p_major_flo_spp)+p_minor_flo_spp
p_mean_flo_smm = np.nanmean(p_major_flo_smm)+p_minor_flo_smm
p_mean_flo_ven = np.nanmean(p_major_flo_ven)+p_minor_flo_ven
p_mean_flo_sbb = np.nanmean(p_major_flo_sbb)+p_minor_flo_sbb
p_mean_flo_scb = p_mean_flo_ssd+p_mean_flo_nsd+p_mean_flo_occ+p_mean_flo_spp+p_mean_flo_smm+p_mean_flo_ven+p_mean_flo_sbb

p_mean_tnn_ssd = np.nanmean(p_major_tnn_ssd)+p_minor_tnn_ssd
p_mean_tnn_nsd = np.nanmean(p_major_tnn_nsd)+p_minor_tnn_nsd
p_mean_tnn_occ = np.nanmean(p_major_tnn_occ)+p_minor_tnn_occ
p_mean_tnn_spp = np.nanmean(p_major_tnn_spp)+p_minor_tnn_spp
p_mean_tnn_smm = np.nanmean(p_major_tnn_smm)+p_minor_tnn_smm
p_mean_tnn_ven = np.nanmean(p_major_tnn_ven)+p_minor_tnn_ven
p_mean_tnn_sbb = np.nanmean(p_major_tnn_sbb)+p_minor_tnn_sbb
p_mean_tnn_scb = p_mean_tnn_ssd+p_mean_tnn_nsd+p_mean_tnn_occ+p_mean_tnn_spp+p_mean_tnn_smm+p_mean_tnn_ven+p_mean_tnn_sbb

p_mean_tpp_ssd = np.nanmean(p_major_tpp_ssd)+p_minor_tpp_ssd
p_mean_tpp_nsd = np.nanmean(p_major_tpp_nsd)+p_minor_tpp_nsd
p_mean_tpp_occ = np.nanmean(p_major_tpp_occ)+p_minor_tpp_occ
p_mean_tpp_spp = np.nanmean(p_major_tpp_spp)+p_minor_tpp_spp
p_mean_tpp_smm = np.nanmean(p_major_tpp_smm)+p_minor_tpp_smm
p_mean_tpp_ven = np.nanmean(p_major_tpp_ven)+p_minor_tpp_ven
p_mean_tpp_sbb = np.nanmean(p_major_tpp_sbb)+p_minor_tpp_sbb
p_mean_tpp_scb = p_mean_tpp_ssd+p_mean_tpp_nsd+p_mean_tpp_occ+p_mean_tpp_spp+p_mean_tpp_smm+p_mean_tpp_ven+p_mean_tpp_sbb

# major outfalls only means
pma_mean_tnn_ssd = np.nanmean(p_major_tnn_ssd)
pma_mean_tnn_nsd = np.nanmean(p_major_tnn_nsd)
pma_mean_tnn_occ = np.nanmean(p_major_tnn_occ)
pma_mean_tnn_spp = np.nanmean(p_major_tnn_spp)
pma_mean_tnn_smm = np.nanmean(p_major_tnn_smm)
pma_mean_tnn_ven = np.nanmean(p_major_tnn_ven)
pma_mean_tnn_sbb = np.nanmean(p_major_tnn_sbb)
pma_mean_tnn_scb = pma_mean_tnn_ssd+pma_mean_tnn_nsd+pma_mean_tnn_occ+pma_mean_tnn_spp+pma_mean_tnn_smm+pma_mean_tnn_ven+pma_mean_tnn_sbb

pma_mean_tpp_ssd = np.nanmean(p_major_tpp_ssd)
pma_mean_tpp_nsd = np.nanmean(p_major_tpp_nsd)
pma_mean_tpp_occ = np.nanmean(p_major_tpp_occ)
pma_mean_tpp_spp = np.nanmean(p_major_tpp_spp)
pma_mean_tpp_smm = np.nanmean(p_major_tpp_smm)
pma_mean_tpp_ven = np.nanmean(p_major_tpp_ven)
pma_mean_tpp_sbb = np.nanmean(p_major_tpp_sbb)
pma_mean_tpp_scb = pma_mean_tpp_ssd+pma_mean_tpp_nsd+pma_mean_tpp_occ+pma_mean_tpp_spp+pma_mean_tpp_smm+pma_mean_tpp_ven+pma_mean_tpp_sbb

pma_mean_din_ssd = np.nanmean(p_major_din_ssd)
pma_mean_din_nsd = np.nanmean(p_major_din_nsd)
pma_mean_din_occ = np.nanmean(p_major_din_occ)
pma_mean_din_spp = np.nanmean(p_major_din_spp)
pma_mean_din_smm = np.nanmean(p_major_din_smm)
pma_mean_din_ven = np.nanmean(p_major_din_ven)
pma_mean_din_sbb = np.nanmean(p_major_din_sbb)
pma_mean_din_scb = pma_mean_din_ssd+pma_mean_din_nsd+pma_mean_din_occ+pma_mean_din_spp+pma_mean_din_smm+pma_mean_din_ven+pma_mean_din_sbb

pma_mean_dip_ssd = np.nanmean(p_major_dip_ssd)
pma_mean_dip_nsd = np.nanmean(p_major_dip_nsd)
pma_mean_dip_occ = np.nanmean(p_major_dip_occ)
pma_mean_dip_spp = np.nanmean(p_major_dip_spp)
pma_mean_dip_smm = np.nanmean(p_major_dip_smm)
pma_mean_dip_ven = np.nanmean(p_major_dip_ven)
pma_mean_dip_sbb = np.nanmean(p_major_dip_sbb)
pma_mean_dip_scb = pma_mean_dip_ssd+pma_mean_dip_nsd+pma_mean_dip_occ+pma_mean_dip_spp+pma_mean_dip_smm+pma_mean_dip_ven+pma_mean_dip_sbb

########################################
# natural current riverine flows
# subtract from total to get non point source
####################################
#Summary Table_natural_historical_current.xlsx
# m3/s
nat_flo = [2.14E7,4.25E7,2.66E7,2.96E7,1.07E7,6.98E7,1.12E7,2.12E8]

# kg/y
nat_tpp =[637,1463,2602,2901,95,1921,317,9937]    
nat_dip = [56,128,227,253,8,168,28,866]
nat_tnn = [4584,10524,18710,20863,685,13817,2278,33289]          
nat_din = [863,1808,2900,3234,120,2122,359,5463]

################
# values in text
################

print('major outfalls percent DIN of TN',(pma_mean_din_scb/pma_mean_tnn_scb))
print('major outfalls percent DIP of TP',(pma_mean_dip_scb/pma_mean_tpp_scb))

print('median of terrestrial flows m3',(r_flo_scb+p_flo_scb))
print('median of terrestrial TN m3',(r_tnn_scb+p_tnn_scb))
print('median of terrestrial TP m3',(r_tpp_scb+p_tpp_scb))


###########################################
# table 2 - median TP and TP per region in kg
###########################################
'''
ssd_tn = r_tnn_ssd+p_tnn_ssd+atmos_plt[0]
nsd_tn = r_tnn_nsd+p_tnn_nsd+atmos_plt[1]
occ_tn = r_tnn_occ+p_tnn_occ+atmos_plt[2]
spp_tn = r_tnn_spp+p_tnn_spp+atmos_plt[3]
smm_tn = r_tnn_smm+p_tnn_smm+atmos_plt[4]
ven_tn = r_tnn_ven+p_tnn_ven+atmos_plt[5]
sbb_tn = r_tnn_sbb+p_tnn_sbb+atmos_plt[6]
scb_tn = r_tnn_scb+p_tnn_scb+atmos_plt[7]

ssd_tp = r_tpp_ssd+p_tpp_ssd
nsd_tp = r_tpp_nsd+p_tpp_nsd
occ_tp = r_tpp_occ+p_tpp_occ
spp_tp = r_tpp_spp+p_tpp_spp
smm_tp = r_tpp_smm+p_tpp_smm
ven_tp = r_tpp_ven+p_tpp_ven
sbb_tp = r_tpp_sbb+p_tpp_sbb
scb_tp = r_tpp_scb+p_tpp_scb

# divide by area of region
ssd_tn_km = ssd_tn/ssd_area
nsd_tn_km = nsd_tn/nsd_area
occ_tn_km = occ_tn/occ_area
spp_tn_km = spp_tn/spp_area
smm_tn_km = smm_tn/smm_area
ven_tn_km = ven_tn/ven_area
sbb_tn_km = sbb_tn/sbb_area
scb_tn_km = scb_tn/scb_area

ssd_tp_km = ssd_tp/ssd_area
nsd_tp_km = nsd_tp/nsd_area
occ_tp_km = occ_tp/occ_area
spp_tp_km = spp_tp/spp_area
smm_tp_km = smm_tp/smm_area
ven_tp_km = ven_tp/ven_area
sbb_tp_km = sbb_tp/sbb_area
scb_tp_km = scb_tp/scb_area
'''
# table 5 is only terrestrial fluxes
ssd_tn = r_mean_tnn_ssd+p_mean_tnn_ssd
nsd_tn = r_mean_tnn_nsd+p_mean_tnn_nsd
occ_tn = r_mean_tnn_occ+p_mean_tnn_occ
spp_tn = r_mean_tnn_spp+p_mean_tnn_spp
smm_tn = r_mean_tnn_smm+p_mean_tnn_smm
ven_tn = r_mean_tnn_ven+p_mean_tnn_ven
sbb_tn = r_mean_tnn_sbb+p_mean_tnn_sbb
scb_tn = r_mean_tnn_scb+p_mean_tnn_scb

ssd_tp = r_mean_tpp_ssd+p_mean_tpp_ssd
nsd_tp = r_mean_tpp_nsd+p_mean_tpp_nsd
occ_tp = r_mean_tpp_occ+p_mean_tpp_occ
spp_tp = r_mean_tpp_spp+p_mean_tpp_spp
smm_tp = r_mean_tpp_smm+p_mean_tpp_smm
ven_tp = r_mean_tpp_ven+p_mean_tpp_ven
sbb_tp = r_mean_tpp_sbb+p_mean_tpp_sbb
scb_tp = r_mean_tpp_scb+p_mean_tpp_scb

ssd_tn_km = ssd_tn/ssd_area
nsd_tn_km = nsd_tn/nsd_area
occ_tn_km = occ_tn/occ_area
spp_tn_km = spp_tn/spp_area
smm_tn_km = smm_tn/smm_area
ven_tn_km = ven_tn/ven_area
sbb_tn_km = sbb_tn/sbb_area
scb_tn_km = scb_tn/scb_area

ssd_tp_km = ssd_tp/ssd_area
nsd_tp_km = nsd_tp/nsd_area
occ_tp_km = occ_tp/occ_area
spp_tp_km = spp_tp/spp_area
smm_tp_km = smm_tp/smm_area
ven_tp_km = ven_tp/ven_area
sbb_tp_km = sbb_tp/sbb_area
scb_tp_km = scb_tp/scb_area
print('smm,spp,occ tn km-2',((occ_tn+spp_tn+smm_tn)/(occ_area+spp_area+smm_area)))
print('smm,spp,occ tp km-2',((occ_tp+spp_tp+smm_tp)/(occ_area+spp_area+smm_area)))

print('table 5 with info from old(removed) table 2')
#print('scb tn ','{:0.2e}'.format(scb_tn))
#print('ssd tn ','{:0.2e}'.format(ssd_tn))
#print('nsd tn ','{:0.2e}'.format(ssd_tn))
#print('occ tn ','{:0.2e}'.format(occ_tn))
#print('spp tn ','{:0.2e}'.format(spp_tn))
#print('smm tn ','{:0.2e}'.format(smm_tn))
#print('ven tn ','{:0.2e}'.format(ven_tn))
#print('sbb tn ','{:0.2e}'.format(sbb_tn))

print('mean scb tn_km ',scb_tn_km)
print('mean ssd tn_km ',ssd_tn_km)
print('mean nsd tn_km ',nsd_tn_km)
print('mean occ tn_km ',occ_tn_km)
print('mean spp tn_km ',spp_tn_km)
print('mean smm tn_km ',smm_tn_km)
print('mean ven tn_km ',ven_tn_km)
print('mean sbb tn_km ',sbb_tn_km)

#print('scb tp ','{:0.2e}'.format(scb_tp))
#print('ssd tp ','{:0.2e}'.format(ssd_tp))
#print('nsd tp ','{:0.2e}'.format(nsd_tp))
#print('occ tp ','{:0.2e}'.format(occ_tp))
#print('spp tp ','{:0.2e}'.format(spp_tp))
#print('smm tp ','{:0.2e}'.format(smm_tp))
#print('ven tp ','{:0.2e}'.format(ven_tp))
#print('sbb tp ','{:0.2e}'.format(sbb_tp))

print('mean scb tp_km ',scb_tp_km)
print('mean ssd tp_km ',ssd_tp_km)
print('mean nsd tp_km ',nsd_tp_km)
print('mean occ tp_km ',occ_tp_km)
print('mean spp tp_km ',spp_tp_km)
print('mean smm tp_km ',smm_tp_km)
print('mean ven tp_km ',ven_tp_km)
print('mean sbb tp_km ',sbb_tp_km)

print('mean scb atmos tn km',atmos_plt_km[-1])
print('mean ssd atmos tn km',atmos_plt_km[0])
print('mean nsd atmos tn km',atmos_plt_km[1])
print('mean occ atmos tn km',atmos_plt_km[2])
print('mean spp atmos tn km',atmos_plt_km[3])
print('mean smm atmos tn km',atmos_plt_km[4])
print('mean ven atmos tn km',atmos_plt_km[5])
print('mean sbb atmos tn km',atmos_plt_km[6])

print('supplemental table 7')
print('scb major potw discharge','{:0.2e}'.format(pma_flo_scb))
print('ssd major potw discharge','{:0.2e}'.format(pma_flo_ssd))
print('nsd major potw discharge','{:0.2e}'.format(pma_flo_nsd))
print('occ major potw discharge','{:0.2e}'.format(pma_flo_occ))
print('spp major potw discharge','{:0.2e}'.format(pma_flo_spp))
print('smm major potw discharge','{:0.2e}'.format(pma_flo_smm))
print('ven major potw discharge','{:0.2e}'.format(pma_flo_ven))
print('sbb major potw discharge','{:0.2e}'.format(pma_flo_sbb))

print('scb major potw din','{:0.2e}'.format(pma_din_scb))
print('ssd major potw din','{:0.2e}'.format(pma_din_ssd))
print('nsd major potw din','{:0.2e}'.format(pma_din_nsd))
print('occ major potw din','{:0.2e}'.format(pma_din_occ))
print('spp major potw din','{:0.2e}'.format(pma_din_spp))
print('smm major potw din','{:0.2e}'.format(pma_din_smm))
print('ven major potw din','{:0.2e}'.format(pma_din_ven))
print('sbb major potw din','{:0.2e}'.format(pma_din_sbb))

print('scb major potw tnn','{:0.2e}'.format(pma_tnn_scb))
print('ssd major potw tnn','{:0.2e}'.format(pma_tnn_ssd))
print('nsd major potw tnn','{:0.2e}'.format(pma_tnn_nsd))
print('occ major potw tnn','{:0.2e}'.format(pma_tnn_occ))
print('spp major potw tnn','{:0.2e}'.format(pma_tnn_spp))
print('smm major potw tnn','{:0.2e}'.format(pma_tnn_smm))
print('ven major potw tnn','{:0.2e}'.format(pma_tnn_ven))
print('sbb major potw tnn','{:0.2e}'.format(pma_tnn_sbb))

print('scb major potw dip','{:0.2e}'.format(pma_dip_scb))
print('ssd major potw dip','{:0.2e}'.format(pma_dip_ssd))
print('nsd major potw dip','{:0.2e}'.format(pma_dip_nsd))
print('occ major potw dip','{:0.2e}'.format(pma_dip_occ))
print('spp major potw dip','{:0.2e}'.format(pma_dip_spp))
print('smm major potw dip','{:0.2e}'.format(pma_dip_smm))
print('ven major potw dip','{:0.2e}'.format(pma_dip_ven))
print('sbb major potw dip','{:0.2e}'.format(pma_dip_sbb))

print('scb major potw tpp','{:0.2e}'.format(pma_tpp_scb))
print('ssd major potw tpp','{:0.2e}'.format(pma_tpp_ssd))
print('nsd major potw tpp','{:0.2e}'.format(pma_tpp_nsd))
print('occ major potw tpp','{:0.2e}'.format(pma_tpp_occ))
print('spp major potw tpp','{:0.2e}'.format(pma_tpp_spp))
print('smm major potw tpp','{:0.2e}'.format(pma_tpp_smm))
print('ven major potw tpp','{:0.2e}'.format(pma_tpp_ven))
print('sbb major potw tpp','{:0.2e}'.format(pma_tpp_sbb))

print('scb minor potw discharge','{:0.2e}'.format(p_minor_flo_scb))
print('ssd minor potw discharge','{:0.2e}'.format(p_minor_flo_ssd))
print('nsd minor potw discharge','{:0.2e}'.format(p_minor_flo_nsd))
print('occ minor potw discharge','{:0.2e}'.format(p_minor_flo_occ))
print('spp minor potw discharge','{:0.2e}'.format(p_minor_flo_spp))
print('smm minor potw discharge','{:0.2e}'.format(p_minor_flo_smm))
print('ven minor potw discharge','{:0.2e}'.format(p_minor_flo_ven))
print('sbb minor potw discharge','{:0.2e}'.format(p_minor_flo_sbb))

print('scb minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_scb))
print('ssd minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_ssd))
print('nsd minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_nsd))
print('occ minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_occ))
print('spp minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_spp))
print('smm minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_smm))
print('ven minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_ven))
print('sbb minor potw tnn/din','{:0.2e}'.format(p_minor_tnn_sbb))

print('scb minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_scb))
print('ssd minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_ssd))
print('nsd minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_nsd))
print('occ minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_occ))
print('spp minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_spp))
print('smm minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_smm))
print('ven minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_ven))
print('sbb minor potw tpp/dip','{:0.2e}'.format(p_minor_tpp_sbb))

# inland nsd is wrong, Hale Ave/Escondido not inland POTW
inland_flows[-1] = inland_flows[-1]-inland_flows[1]
inland_tnn[-1] = inland_tnn[-1]-inland_tnn[1]
inland_tpp[-1] = inland_tpp[-1]-inland_tpp[1]
inland_din[-1] = inland_din[-1]-inland_din[1]
inland_dip[-1] = inland_dip[-1]-inland_dip[1]

inland_flows[1] = 0
inland_tnn[1] =0 
inland_tpp[1] =0 
inland_din[1] =0 
inland_dip[1] =0 

inland_tnn[6] =0 
inland_tpp[6] =0 
inland_din[6] =0 
inland_dip[6] =0 


print('scb inland POTW discharge','{:0.2e}'.format(inland_flows[-1]))
print('ssd inland POTW discharge','{:0.2e}'.format(inland_flows[0]))
print('nsd inland POTW discharge','{:0.2e}'.format(inland_flows[1]))
print('occ inland POTW discharge','{:0.2e}'.format(inland_flows[2]))
print('spp inland POTW discharge','{:0.2e}'.format(inland_flows[3]))
print('smm inland POTW discharge','{:0.2e}'.format(inland_flows[4]))
print('ven inland POTW discharge','{:0.2e}'.format(inland_flows[5]))
print('sbb inland POTW discharge','{:0.2e}'.format(inland_flows[6]))

print('scb inland POTW din','{:0.2e}'.format(inland_din[-1]))
print('ssd inland POTW din','{:0.2e}'.format(inland_din[0]))
print('nsd inland POTW din','{:0.2e}'.format(inland_din[1]))
print('occ inland POTW din','{:0.2e}'.format(inland_din[2]))
print('spp inland POTW din','{:0.2e}'.format(inland_din[3]))
print('smm inland POTW din','{:0.2e}'.format(inland_din[4]))
print('ven inland POTW din','{:0.2e}'.format(inland_din[5]))

print('scb inland POTW tnn','{:0.2e}'.format(inland_tnn[-1]))
print('ssd inland POTW tnn','{:0.2e}'.format(inland_tnn[0]))
print('nsd inland POTW tnn','{:0.2e}'.format(inland_tnn[1]))
print('occ inland POTW tnn','{:0.2e}'.format(inland_tnn[2]))
print('spp inland POTW tnn','{:0.2e}'.format(inland_tnn[3]))
print('smm inland POTW tnn','{:0.2e}'.format(inland_tnn[4]))
print('ven inland POTW tnn','{:0.2e}'.format(inland_tnn[5]))
print('sbb inland POTW tnn','{:0.2e}'.format(inland_tnn[6]))
print('sbb inland POTW din','{:0.2e}'.format(inland_din[6]))

print('scb inland POTW dip','{:0.2e}'.format(inland_dip[-1]))
print('ssd inland POTW dip','{:0.2e}'.format(inland_dip[0]))
print('nsd inland POTW dip','{:0.2e}'.format(inland_dip[1]))
print('occ inland POTW dip','{:0.2e}'.format(inland_dip[2]))
print('spp inland POTW dip','{:0.2e}'.format(inland_dip[3]))
print('smm inland POTW dip','{:0.2e}'.format(inland_dip[4]))
print('ven inland POTW dip','{:0.2e}'.format(inland_dip[5]))
print('sbb inland POTW dip','{:0.2e}'.format(inland_dip[6]))

print('scb inland POTW tpp','{:0.2e}'.format(inland_tpp[-1]))
print('ssd inland POTW tpp','{:0.2e}'.format(inland_tpp[0]))
print('nsd inland POTW tpp','{:0.2e}'.format(inland_tpp[1]))
print('occ inland POTW tpp','{:0.2e}'.format(inland_tpp[2]))
print('spp inland POTW tpp','{:0.2e}'.format(inland_tpp[3]))
print('smm inland POTW tpp','{:0.2e}'.format(inland_tpp[4]))
print('ven inland POTW tpp','{:0.2e}'.format(inland_tpp[5]))
print('sbb inland POTW tpp','{:0.2e}'.format(inland_tpp[6]))

print('\n')
print('scb NPS din','{:0.2e}'.format(r_din_scb-nat_din[7]-inland_din[7]))
print('ssd NPS din','{:0.2e}'.format(r_din_ssd-nat_din[0]-inland_din[0]))
print('nsd NPS din','{:0.2e}'.format(r_din_nsd-nat_din[1]-inland_din[1]))
print('occ NPS din','{:0.2e}'.format(r_din_occ-nat_din[2]-inland_din[2]))
#print('spp NPS din','{:0.2e}'.format(r_din_spp-nat_din[3]-inland_din[3]))
# inland_din > total river din
print('spp NPS din','{:0.2e}'.format(r_din_spp-nat_din[3]-(r_din_spp*.95)))
print('smm NPS din','{:0.2e}'.format(r_din_smm-nat_din[4]-inland_din[4]))
print('ven NPS din','{:0.2e}'.format(r_din_ven-nat_din[5]-inland_din[5]))
print('sbb NPS din','{:0.2e}'.format(r_din_sbb-nat_din[6]-inland_din[6]))

print('\n')
#print('scb NPS tnn','{:0.2e}'.format(r_tnn_scb-nat_tnn[7]-inland_tnn[7]))
print('scb NPS tnn','{:0.2e}'.format(np.nansum((r_tnn_ssd-nat_tnn[0]-inland_tnn[0],r_tnn_nsd-nat_tnn[1]-inland_tnn[1],r_tnn_occ-nat_tnn[2]-inland_tnn[2],r_tnn_spp-nat_tnn[3]-(r_tnn_spp*.95),r_tnn_smm-nat_tnn[4]-(r_tnn_smm*.95),r_tnn_ven-nat_tnn[5]-(r_tnn_ven*.95)+(r_din_ven-nat_din[5]-inland_din[5]),r_tnn_sbb-nat_tnn[6]-inland_tnn[6]))))
print('ssd NPS tnn','{:0.2e}'.format(r_tnn_ssd-nat_tnn[0]-inland_tnn[0]))
print('nsd NPS tnn','{:0.2e}'.format(r_tnn_nsd-nat_tnn[1]-inland_tnn[1]))
print('occ NPS tnn','{:0.2e}'.format(r_tnn_occ-nat_tnn[2]-inland_tnn[2]))
print('spp NPS tnn','{:0.2e}'.format(r_tnn_spp-nat_tnn[3]-(r_tnn_spp*.95)))
print('smm NPS tnn','{:0.2e}'.format(r_tnn_smm-nat_tnn[4]-(r_tnn_smm*.95)))
print('ven NPS tnn','{:0.2e}'.format(r_tnn_ven-nat_tnn[5]-(r_tnn_ven*.95)+(r_din_ven-nat_din[5]-inland_din[5])))
print('sbb NPS tnn','{:0.2e}'.format(r_tnn_sbb-nat_tnn[6]-inland_tnn[6]))
#print('spp NPS tnn','{:0.2e}'.format(r_tnn_spp-nat_tnn[3]-inland_tnn[3]))
#print('smm NPS tnn','{:0.2e}'.format(r_tnn_smm-nat_tnn[4]-inland_tnn[4]))
#print('ven NPS tnn','{:0.2e}'.format(r_tnn_ven-nat_tnn[5]-inland_tnn[5]))

print('\n')
print('scb NPS dip','{:0.2e}'.format(np.nansum((r_dip_ssd-nat_dip[0]-inland_dip[0],r_dip_nsd-nat_dip[1]-inland_dip[1],r_dip_occ-nat_dip[2]-inland_dip[2],r_dip_spp-nat_dip[3]-inland_dip[3],r_dip_smm-nat_dip[4]-(r_dip_smm*.95),r_dip_ven-nat_dip[5]-(r_dip_ven*.95),r_dip_sbb-nat_dip[6]-inland_dip[6]))))
#print('scb NPS dip','{:0.2e}'.format(r_dip_scb-nat_dip[7]-inland_dip[7]))
print('ssd NPS dip','{:0.2e}'.format(r_dip_ssd-nat_dip[0]-inland_dip[0]))
print('nsd NPS dip','{:0.2e}'.format(r_dip_nsd-nat_dip[1]-inland_dip[1]))
print('occ NPS dip','{:0.2e}'.format(r_dip_occ-nat_dip[2]-inland_dip[2]))
print('spp NPS dip','{:0.2e}'.format(r_dip_spp-nat_dip[3]-inland_dip[3]))
print('smm NPS dip','{:0.2e}'.format(r_dip_smm-nat_dip[4]-(r_dip_smm*.95)))
print('ven NPS dip','{:0.2e}'.format(r_dip_ven-nat_dip[5]-(r_dip_ven*.95)))
#print('smm NPS dip','{:0.2e}'.format(r_dip_smm-nat_dip[4]-inland_dip[4]))
#print('ven NPS dip','{:0.2e}'.format(r_dip_ven-nat_dip[5]-inland_dip[5]))
print('sbb NPS dip','{:0.2e}'.format(r_dip_sbb-nat_dip[6]-inland_dip[6]))

print('\n')
#print('scb NPS tpp','{:0.2e}'.format(r_tpp_scb-nat_tpp[7]-inland_tpp[7]))
print('scb NPS tpp','{:0.2e}'.format(np.nansum((r_tpp_ssd-nat_tpp[0]-inland_tpp[0],r_tpp_nsd-nat_tpp[1]-inland_tpp[1],r_tpp_occ-nat_tpp[2]-inland_tpp[2],r_tpp_spp-nat_tpp[3]-inland_tpp[3],r_tpp_smm-nat_tpp[4]-(r_tpp_smm*.95),r_tpp_ven-nat_tpp[5]-(r_tpp_ven*.95),r_tpp_sbb-nat_tpp[6]-inland_tpp[6]))))
print('ssd NPS tpp','{:0.2e}'.format(r_tpp_ssd-nat_tpp[0]-inland_tpp[0]))
print('nsd NPS tpp','{:0.2e}'.format(r_tpp_nsd-nat_tpp[1]-inland_tpp[1]))
print('occ NPS tpp','{:0.2e}'.format(r_tpp_occ-nat_tpp[2]-inland_tpp[2]))
print('spp NPS tpp','{:0.2e}'.format(r_tpp_spp-nat_tpp[3]-inland_tpp[3]))
#print('smm NPS tpp','{:0.2e}'.format(r_tpp_smm-nat_tpp[4]-inland_tpp[4]))
#print('ven NPS tpp','{:0.2e}'.format(r_tpp_ven-nat_tpp[5]-inland_tpp[5]))
print('smm NPS tpp','{:0.2e}'.format(r_tpp_smm-nat_tpp[4]-(r_tpp_smm*.95)))
print('ven NPS tpp','{:0.2e}'.format(r_tpp_ven-nat_tpp[5]-(r_tpp_ven*.95)))
print('sbb NPS tpp','{:0.2e}'.format(r_tpp_sbb-nat_tpp[6]-inland_tpp[6]))

                                     
