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

river_din = np.nansum((river_nh4,river_no3),axis=0)

river_flo[river_flo>1E20] = np.nan
river_tn[river_tn>1E20] = np.nan
river_tp[river_tp>1E20] = np.nan

r_river_flo = [[] for i in range(maskarr.shape[0])]
r_river_tn = [[] for i in range(maskarr.shape[0])] # TN flux
r_river_tp = [[] for i in range(maskarr.shape[0])] # TP flux
r_river_di = [[] for i in range(maskarr.shape[0])] # DIN flux
r_river_dp = [[] for i in range(maskarr.shape[0])] # DIP flux
for r_i in range(len(r_river_ind)):
    r_river_flo[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]).tolist())
    r_river_tn[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_tn[:,r_river_ind[r_i]]).tolist())
    r_river_tp[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_tp[:,r_river_ind[r_i]]).tolist())
    r_river_di[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_din[:,r_river_ind[r_i]]).tolist())
    r_river_dp[r_i].append(np.transpose(river_flo[:,r_river_ind[r_i]]*river_po4[:,r_river_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (10,12) because this data set is 10 years
# then average over each year to get yearly averages
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

r_din_ssd = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[0][0]),axis=0).reshape(ry0,12),axis=1))
r_din_nsd = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[1][0]),axis=0).reshape(ry0,12),axis=1))
r_din_occ = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[2][0]),axis=0).reshape(ry0,12),axis=1))
r_din_spp = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[3][0]),axis=0).reshape(ry0,12),axis=1))
r_din_smm = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[4][0]),axis=0).reshape(ry0,12),axis=1))
r_din_ven = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[5][0]),axis=0).reshape(ry0,12),axis=1))
r_din_sbb = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_di[6][0]),axis=0).reshape(ry0,12),axis=1))

r_dip_ssd = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[0][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_nsd = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[1][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_occ = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[2][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_spp = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[3][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_smm = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[4][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_ven = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[5][0]),axis=0).reshape(ry0,12),axis=1))
r_dip_sbb = np.nanmedian(np.nanmean(np.nansum(np.array(r_river_dp[6][0]),axis=0).reshape(ry0,12),axis=1))

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
potw_2013 = major_potw_time.shape[0] # 2017-01-01

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
major_din = major_nh4+major_no3+major_no2

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan

p_major_flo = [[] for i in range(maskarr.shape[0])]
p_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
p_major_tp = [[] for i in range(maskarr.shape[0])] # TP flux
p_major_di = [[] for i in range(maskarr.shape[0])] # DIN flux
p_major_dp = [[] for i in range(maskarr.shape[0])] # DIP flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    p_major_tp[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_tp[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    p_major_di[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_din[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())
    p_major_dp[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i]]*major_po4[potw_1997:potw_2013,p_major_ind[r_i]]).tolist())

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

# find DIN flux average monthly, for each year (mmol/s)
p_major_din_ssd = np.nanmean(np.nansum(np.array(p_major_di[0][0]),axis=0).reshape(ry0,12),axis=1) 
p_major_din_nsd = np.zeros((ry0))
p_major_din_occ = np.nanmean(np.nansum(np.array(p_major_di[2][0]),axis=0).reshape(ry0,12),axis=1)
p_major_din_spp = np.nanmean(np.nansum(np.array(p_major_di[3][0]),axis=0).reshape(ry0,12),axis=1)
p_major_din_smm = np.nanmean(np.nansum(np.array(p_major_di[4][0]),axis=0).reshape(ry0,12),axis=1)
p_major_din_ven = np.zeros((ry0))
p_major_din_sbb = np.zeros((ry0))

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
p_minor_di = [[] for i in range(maskarr.shape[0])]
p_minor_dp = [[] for i in range(maskarr.shape[0])]
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

p_minor_din_ssd = np.nanmean(np.nansum(np.array(p_minor_tn[0][0]),axis=0).reshape(ry0,12),axis=1)
p_minor_din_nsd = np.nanmean(np.nansum(np.array(p_minor_tn[1][0]),axis=0).reshape(ry0,12),axis=1)
p_minor_din_occ = np.nanmean(np.nansum(np.array(p_minor_tn[2][0]),axis=0).reshape(ry0,12),axis=1)
p_minor_din_spp = np.nanmean(np.nansum(np.array(p_minor_tn[3][0]),axis=0).reshape(ry0,12),axis=1)
#p_minor_tnn_smm = np.nanmean(np.nansum(np.array(p_minor_tn[4][0]),axis=0).reshape(ry0,12),axis=0)
p_minor_din_smm = np.zeros((ry0))
p_minor_din_ven = np.nanmean(np.nansum(np.array(p_minor_tn[5][0]),axis=0).reshape(ry0,12),axis=1)
p_minor_din_sbb = np.nanmean(np.nansum(np.array(p_minor_tn[6][0]),axis=0).reshape(ry0,12),axis=1)

# inland POTW
# see Inland POTW excel for inland potw data
inland_tnn = np.load('inland_potw_tnn_region.npy')
inland_tpp = np.load('inland_potw_tpp_region.npy')
inland_din = np.load('inland_potw_din_region.npy')
inland_dip = np.load('inland_potw_dip_region.npy')

# inland potw flow by region
#ssd,nsd,occ,spp,smb,ven,sbb,scb
#inland_flows = [2348848,17432137,2564159,1.75E8,4941331,53495704,np.nan,255900740]
inland_flo = [2348592.5,17430240.42,2563880.146,175099510.9,4940793.908,53489884.95,np.nan,255872902.9]

# Esondido (nsd) actually is a minor POTW
# remove inland flow for nsd and sbb because they don't have inland plants 
inland_flo[1] = 0
inland_flo[6] = 0

inland_tnn[1] = 0
inland_tnn[6] = 0

inland_tpp[1] = 0
inland_tpp[6] = 0

inland_din[1] = 0
inland_din[6] = 0

inland_dip[1] = 0
inland_dip[6] = 0

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

p_din_ssd = p_major_din_ssd+p_minor_din_ssd
p_din_nsd = p_major_din_nsd+p_minor_din_nsd
p_din_occ = p_major_din_occ+p_minor_din_occ
p_din_spp = p_major_din_spp+p_minor_din_spp
p_din_smm = p_major_din_smm+p_minor_din_smm
p_din_ven = p_major_din_ven+p_minor_din_ven
p_din_sbb = p_major_din_sbb+p_minor_din_sbb

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14
g_P = 30.97

p_yr_nobight_fl = np.array((np.nansum(s_to_d*d_to_mo*p_flo_ssd),np.nansum(s_to_d*d_to_mo*p_flo_nsd),np.nansum(s_to_d*d_to_mo*p_flo_occ),np.nansum(s_to_d*d_to_mo*p_flo_spp),np.nansum(s_to_d*d_to_mo*p_flo_smm),np.nansum(s_to_d*d_to_mo*p_flo_ven),np.nansum(s_to_d*d_to_mo*p_flo_sbb)))

p_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*p_tnn_sbb)))

p_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_nsd),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*p_tpp_sbb)))

r_yr_nobight_fl = np.array((np.nansum(s_to_d*d_to_mo*r_flo_ssd),np.nansum(s_to_d*d_to_mo*r_flo_nsd),np.nansum(s_to_d*d_to_mo*r_flo_occ),np.nansum(s_to_d*d_to_mo*r_flo_spp),np.nansum(s_to_d*d_to_mo*r_flo_smm),np.nansum(s_to_d*d_to_mo*r_flo_ven),np.nansum(s_to_d*d_to_mo*r_flo_sbb)))

r_yr_nobight_tn = np.array((np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ssd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_nsd),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_occ),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_spp),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_smm),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_ven),np.nansum(((s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol))*r_tnn_sbb)))

r_yr_nobight_tp = np.array((np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_ssd),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_nsd),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_occ),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_spp),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_smm),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_ven),np.nansum(((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol))*r_tpp_sbb)))

r_yr_nobight_din = np.array((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_ssd,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_nsd,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_occ,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_spp,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_smm,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_ven,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_din_sbb))

r_yr_nobight_dip = np.array((s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_ssd,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_nsd,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_occ,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_spp,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_smm,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_ven,s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol*r_dip_sbb))

# bightwide sum
p_bight_fl = np.nansum(p_yr_nobight_fl)
p_bight_tn = np.nansum(p_yr_nobight_tn)
r_bight_fl = np.nansum(r_yr_nobight_fl)
r_bight_tn = np.nansum(r_yr_nobight_tn)
p_bight_tp = np.nansum(p_yr_nobight_tp)
r_bight_tp = np.nansum(r_yr_nobight_tp)

r_bight_din = np.nansum(r_yr_nobight_din)
r_bight_dip = np.nansum(r_yr_nobight_dip)




p_yr_fl = np.append(p_yr_nobight_fl,p_bight_fl)
r_yr_fl = np.append(r_yr_nobight_fl,r_bight_fl)

p_yr_tn = np.append(p_yr_nobight_tn,p_bight_tn)
r_yr_tn = np.append(r_yr_nobight_tn,r_bight_tn)
p_yr_tp = np.append(p_yr_nobight_tp,p_bight_tp)
r_yr_tp = np.append(r_yr_nobight_tp,r_bight_tp)

r_yr_din = np.append(r_yr_nobight_din,r_bight_din)
r_yr_dip = np.append(r_yr_nobight_dip,r_bight_dip)

# natural current, NPS, PS, inland PS
# natural current riverine 
# ssd, nsd, occ, spp, smm, ven, sbb

#Summary Table_natural_historical_current.xlsx
# m3/s
nat_flo = [2.14E7,4.25E7,2.66E7,2.96E7,1.07E7,6.98E7,1.12E7,2.12E8]

# kg/y
nat_cur_tpp =[637,1463,2602,2901,95,1921,317,9937]
nat_cur_dip = [56,128,227,253,8,168,28,866]
nat_cur_tnn = [4584,10524,18710,20863,685,13817,2278,33289]
nat_cur_din = [863,1808,2900,3234,120,2122,359,5463]

# nonpoint source nps NPS

nps_flo = np.empty((8))
nps_flo[0] = r_yr_fl[0]-nat_flo[0]-inland_flo[0]
nps_flo[1] = r_yr_fl[1]-nat_flo[1]-inland_flo[1]
nps_flo[2] = r_yr_fl[2]-nat_flo[2]-inland_flo[2]
nps_flo[3] = r_yr_fl[3]-nat_flo[3]-inland_flo[3]
nps_flo[4] = r_yr_fl[4]-nat_flo[4]-inland_flo[4]
nps_flo[5] = r_yr_fl[5]-nat_flo[5]-inland_flo[5]
nps_flo[6] = r_yr_fl[6]-nat_flo[6]-inland_flo[6]
nps_flo[7] = np.nansum((nps_flo[0]+nps_flo[1]+nps_flo[2]+nps_flo[3]+nps_flo[4]+nps_flo[5]+nps_flo[6]))

nps_tnn = np.empty((8))
nps_tnn[0] = r_yr_tn[0]-nat_cur_tnn[0]-inland_tnn[0]
nps_tnn[1] = r_yr_tn[1]-nat_cur_tnn[1]-inland_tnn[1]
nps_tnn[2] = r_yr_tn[2]-nat_cur_tnn[2]-inland_tnn[2]
nps_tnn[3] = r_yr_tn[3]-nat_cur_tnn[3]-(r_yr_tn[3]*.95)
nps_tnn[4] = r_yr_tn[4]-nat_cur_tnn[4]-inland_tnn[4]
nps_tnn[5] = r_yr_tn[5]-nat_cur_tnn[5]-inland_tnn[5]
nps_tnn[6] = r_yr_tn[6]-nat_cur_tnn[6]-inland_tnn[6]
nps_tnn[7] = np.nansum((nps_tnn[0]+nps_tnn[1]+nps_tnn[2]+nps_tnn[3]+nps_tnn[4]+nps_tnn[5]+nps_tnn[6]))

nps_din = np.empty((8))
nps_din[0] = r_yr_din[0]-nat_cur_din[0]-inland_din[0]
nps_din[1] = r_yr_din[1]-nat_cur_din[1]-inland_din[1]
nps_din[2] = r_yr_din[2]-nat_cur_din[2]-inland_din[2]
nps_din[3] = r_yr_din[3]-nat_cur_din[3]-(r_yr_din[3]*.95)
nps_din[4] = r_yr_din[4]-nat_cur_din[4]-(r_yr_din[4]*.95)
nps_din[5] = r_yr_din[5]-nat_cur_din[5]-(r_yr_din[5]*.95)
nps_din[6] = r_yr_din[6]-nat_cur_din[6]-inland_din[6]
nps_din[7] = np.nansum((nps_din[0]+nps_din[1]+nps_din[2]+nps_din[3]+nps_din[4]+nps_din[5]+nps_din[6]))

nps_tpp = np.empty((8))
nps_tpp[7] = np.nansum((r_yr_tp[0]-nat_cur_tpp[0]-inland_tpp[0],r_yr_tp[1]-nat_cur_tpp[1]-inland_tpp[1],r_yr_tp[2]-nat_cur_tpp[2]-inland_tpp[2],r_yr_tp[3]-nat_cur_tpp[3]-inland_tpp[3],r_yr_tp[4]-nat_cur_tpp[4]-(r_yr_tp[4]*.95),r_yr_tp[5]-nat_cur_tpp[5]-(r_yr_tp[5]*.95),r_yr_tp[6]-nat_cur_tpp[6]-inland_tpp[6]))
nps_tpp[0] = r_yr_tp[0]-nat_cur_tpp[0]-inland_tpp[0]
nps_tpp[1] = r_yr_tp[1]-nat_cur_tpp[1]-inland_tpp[1]
nps_tpp[2] = r_yr_tp[2]-nat_cur_tpp[2]-inland_tpp[2]
nps_tpp[3] = r_yr_tp[3]-nat_cur_tpp[3]-inland_tpp[3]
nps_tpp[4] = r_yr_tp[4]-nat_cur_tpp[4]-inland_tpp[4]
nps_tpp[5] = r_yr_tp[5]-nat_cur_tpp[5]-inland_tpp[5]
nps_tpp[6] = r_yr_tp[6]-nat_cur_tpp[6]-inland_tpp[6]

nps_dip = np.empty((8))
nps_dip[0] = r_yr_dip[0]-nat_cur_dip[0]-inland_dip[0]
nps_dip[1] = r_yr_dip[1]-nat_cur_dip[1]-inland_dip[1]
nps_dip[2] = r_yr_dip[2]-nat_cur_dip[2]-inland_dip[2]
nps_dip[3] = r_yr_dip[3]-nat_cur_dip[3]-(r_yr_dip[3]*.95)
nps_dip[4] = r_yr_dip[4]-nat_cur_dip[4]-(r_yr_dip[4]*.95)
nps_dip[5] = r_yr_dip[5]-nat_cur_dip[5]-(r_yr_dip[5]*.95)
nps_dip[6] = r_yr_dip[6]-nat_cur_dip[6]-inland_dip[6]
nps_dip[7] = nps_dip[0]+ nps_dip[1]+ nps_dip[2]+ nps_dip[3]+ nps_dip[4]+ nps_dip[5]+ nps_dip[6]



# natural flows without bight total
nnt_tnn = np.nansum(nat_cur_tnn[:7])

inl_flo = np.array(inland_flo[:])
inl_tnn = np.array(inland_tnn[:])
inl_din = np.array(inland_din[:])
inl_tpp = np.array(inland_tpp[:])
inl_dip = np.array(inland_dip[:])

#inl_tnn[3] = r_yr_nobight_tn[3]*.95
#inl_tnn[4] = r_yr_nobight_tn[4]*.95
#inl_tnn[5] = r_yr_nobight_tn[5]*.95

#inl_din[3] = r_yr_nobight_din[3]*.95
#inl_din[4] = r_yr_nobight_din[4]*.95
#inl_din[5] = r_yr_nobight_din[5]*.95

#inl_dip[3] = r_yr_nobight_dip[3]*.95
#inl_dip[4] = r_yr_nobight_dip[4]*.95
#inl_dip[5] = r_yr_nobight_dip[5]*.95

#######################
# table of  medians
#######################

# major potw
p_major_med_flo_ssd = np.median(np.nansum(np.nansum(np.array(p_major_flo[0][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_major_med_flo_nsd = 0
p_major_med_flo_occ = np.median(np.nansum(np.nansum(np.array(p_major_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_major_med_flo_spp = np.median(np.nansum(np.nansum(np.array(p_major_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_major_med_flo_smm = np.median(np.nansum(np.nansum(np.array(p_major_flo[4][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_major_med_flo_ven = 0
p_major_med_flo_sbb = 0
p_major_med_flo_scb = p_major_med_flo_ssd +p_major_med_flo_nsd +p_major_med_flo_occ +p_major_med_flo_spp +p_major_med_flo_smm +p_major_med_flo_ven +p_major_med_flo_sbb

p_major_med_din_ssd = np.median(np.nansum(np.nansum(np.array(p_major_di[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_din_nsd = 0
p_major_med_din_occ = np.median(np.nansum(np.nansum(np.array(p_major_di[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_din_spp = np.median(np.nansum(np.nansum(np.array(p_major_di[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_din_smm = np.median(np.nansum(np.nansum(np.array(p_major_di[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_din_ven = 0
p_major_med_din_sbb = 0
p_major_med_din_scb = p_major_med_din_ssd +p_major_med_din_nsd +p_major_med_din_occ +p_major_med_din_spp +p_major_med_din_smm +p_major_med_din_ven +p_major_med_din_sbb

p_major_med_tnn_ssd = np.median(np.nansum(np.nansum(np.array(p_major_tn[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tnn_nsd = 0
p_major_med_tnn_occ = np.median(np.nansum(np.nansum(np.array(p_major_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tnn_spp = np.median(np.nansum(np.nansum(np.array(p_major_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tnn_smm = np.median(np.nansum(np.nansum(np.array(p_major_tn[4][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tnn_ven = 0
p_major_med_tnn_sbb = 0
p_major_med_tnn_scb = p_major_med_tnn_ssd +p_major_med_tnn_nsd +p_major_med_tnn_occ +p_major_med_tnn_spp +p_major_med_tnn_smm +p_major_med_tnn_ven +p_major_med_tnn_sbb

p_major_med_dip_ssd = np.median(np.nansum(np.nansum(np.array(p_major_dp[0][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_dip_nsd = 0
p_major_med_dip_occ = np.median(np.nansum(np.nansum(np.array(p_major_dp[2][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_dip_spp = np.median(np.nansum(np.nansum(np.array(p_major_dp[3][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_dip_smm = np.median(np.nansum(np.nansum(np.array(p_major_dp[4][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_dip_ven = 0
p_major_med_dip_sbb = 0
p_major_med_dip_scb = p_major_med_dip_ssd +p_major_med_dip_nsd +p_major_med_dip_occ +p_major_med_dip_spp +p_major_med_dip_smm +p_major_med_dip_ven +p_major_med_dip_sbb

p_major_med_tpp_ssd = np.median(np.nansum(np.nansum(np.array(p_major_tp[0][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tpp_nsd = 0                                                                                 
p_major_med_tpp_occ = np.median(np.nansum(np.nansum(np.array(p_major_tp[2][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tpp_spp = np.median(np.nansum(np.nansum(np.array(p_major_tp[3][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tpp_smm = np.median(np.nansum(np.nansum(np.array(p_major_tp[4][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_major_med_tpp_ven = 0
p_major_med_tpp_sbb = 0
p_major_med_tpp_scb = p_major_med_tpp_ssd +p_major_med_tpp_nsd +p_major_med_tpp_occ +p_major_med_tpp_spp +p_major_med_tpp_smm +p_major_med_tpp_ven +p_major_med_tpp_sbb

# minor potw
p_minor_med_flo_ssd = np.median(np.nansum(np.nansum(np.array(p_minor_flo[0][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_nsd = np.median(np.nansum(np.nansum(np.array(p_minor_flo[1][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_occ = np.median(np.nansum(np.nansum(np.array(p_minor_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_spp = np.median(np.nansum(np.nansum(np.array(p_minor_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_smm = 0
p_minor_med_flo_ven = np.median(np.nansum(np.nansum(np.array(p_minor_flo[5][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_sbb = np.median(np.nansum(np.nansum(np.array(p_minor_flo[6][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
p_minor_med_flo_scb = p_minor_med_flo_ssd +p_minor_med_flo_nsd +p_minor_med_flo_occ +p_minor_med_flo_spp +p_minor_med_flo_smm +p_minor_med_flo_ven +p_minor_med_flo_sbb

p_minor_med_tnn_ssd = np.median(np.nansum(np.nansum(np.array(p_minor_tn[0][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_nsd = np.median(np.nansum(np.nansum(np.array(p_minor_tn[1][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_occ = np.median(np.nansum(np.nansum(np.array(p_minor_tn[2][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_spp = np.median(np.nansum(np.nansum(np.array(p_minor_tn[3][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_smm = 0
p_minor_med_tnn_ven = np.median(np.nansum(np.nansum(np.array(p_minor_tn[5][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_sbb = np.median(np.nansum(np.nansum(np.array(p_minor_tn[6][0])*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tnn_scb = p_minor_med_tnn_ssd +p_minor_med_tnn_nsd +p_minor_med_tnn_occ +p_minor_med_tnn_spp +p_minor_med_tnn_smm +p_minor_med_tnn_ven +p_minor_med_tnn_sbb

p_minor_med_tpp_ssd = np.median(np.nansum(np.nansum(np.array(p_minor_tp[0][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_nsd = np.median(np.nansum(np.nansum(np.array(p_minor_tp[1][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_occ = np.median(np.nansum(np.nansum(np.array(p_minor_tp[2][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_spp = np.median(np.nansum(np.nansum(np.array(p_minor_tp[3][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_smm = 0
p_minor_med_tpp_ven = np.median(np.nansum(np.nansum(np.array(p_minor_tp[5][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_sbb = np.median(np.nansum(np.nansum(np.array(p_minor_tp[6][0])*s_to_d*d_to_mo*g_P*g_to_kg*mmol_to_mol,axis=0).reshape(ry0,12),axis=1))
p_minor_med_tpp_scb = p_minor_med_tpp_ssd +p_minor_med_tpp_nsd +p_minor_med_tpp_occ +p_minor_med_tpp_spp +p_minor_med_tpp_smm +p_minor_med_tpp_ven +p_minor_med_tpp_sbb

r_med_flo_ssd = np.median(np.nansum(np.nansum(np.array(r_river_flo[0][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_nsd = np.median(np.nansum(np.nansum(np.array(r_river_flo[1][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_occ = np.median(np.nansum(np.nansum(np.array(r_river_flo[2][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_spp = np.median(np.nansum(np.nansum(np.array(r_river_flo[3][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_smm = np.median(np.nansum(np.nansum(np.array(r_river_flo[4][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_ven = np.median(np.nansum(np.nansum(np.array(r_river_flo[5][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_sbb = np.median(np.nansum(np.nansum(np.array(r_river_flo[6][0])*s_to_d*d_to_mo,axis=0).reshape(ry0,12),axis=1))
r_med_flo_scb = r_med_flo_ssd + r_med_flo_nsd + r_med_flo_occ + r_med_flo_spp + r_med_flo_smm + r_med_flo_ven + r_med_flo_sbb

# major POTW
print('scb major POTW ','{:0.2E}'.format(p_major_med_flo_scb)+' & '+'{:0.2E}'.format(p_major_med_din_scb)+' & '+'{:0.2E}'.format(p_major_med_tnn_scb)+' & '+'{:0.2E}'.format(p_major_med_dip_scb)+' & '+'{:0.2E}'.format(p_major_med_tpp_scb))
print('ssd major POTW ','{:0.2E}'.format(p_major_med_flo_ssd)+' & '+'{:0.2E}'.format(p_major_med_din_ssd)+' & '+'{:0.2E}'.format(p_major_med_tnn_ssd)+' & '+'{:0.2E}'.format(p_major_med_dip_ssd)+' & '+'{:0.2E}'.format(p_major_med_tpp_ssd))
print('nsd major POTW ','{:0.2E}'.format(p_major_med_flo_nsd)+' & '+'{:0.2E}'.format(p_major_med_din_nsd)+' & '+'{:0.2E}'.format(p_major_med_tnn_nsd)+' & '+'{:0.2E}'.format(p_major_med_dip_nsd)+' & '+'{:0.2E}'.format(p_major_med_tpp_nsd))
print('occ major POTW ','{:0.2E}'.format(p_major_med_flo_occ)+' & '+'{:0.2E}'.format(p_major_med_din_occ)+' & '+'{:0.2E}'.format(p_major_med_tnn_occ)+' & '+'{:0.2E}'.format(p_major_med_dip_occ)+' & '+'{:0.2E}'.format(p_major_med_tpp_occ))
print('spp major POTW ','{:0.2E}'.format(p_major_med_flo_spp)+' & '+'{:0.2E}'.format(p_major_med_din_spp)+' & '+'{:0.2E}'.format(p_major_med_tnn_spp)+' & '+'{:0.2E}'.format(p_major_med_dip_spp)+' & '+'{:0.2E}'.format(p_major_med_tpp_spp))
print('smm major POTW ','{:0.2E}'.format(p_major_med_flo_smm)+' & '+'{:0.2E}'.format(p_major_med_din_smm)+' & '+'{:0.2E}'.format(p_major_med_tnn_smm)+' & '+'{:0.2E}'.format(p_major_med_dip_smm)+' & '+'{:0.2E}'.format(p_major_med_tpp_smm))
print('ven major POTW ','{:0.2E}'.format(p_major_med_flo_ven)+' & '+'{:0.2E}'.format(p_major_med_din_ven)+' & '+'{:0.2E}'.format(p_major_med_tnn_ven)+' & '+'{:0.2E}'.format(p_major_med_dip_ven)+' & '+'{:0.2E}'.format(p_major_med_tpp_ven))
print('sbb major POTW ','{:0.2E}'.format(p_major_med_flo_sbb)+' & '+'{:0.2E}'.format(p_major_med_din_sbb)+' & '+'{:0.2E}'.format(p_major_med_tnn_sbb)+' & '+'{:0.2E}'.format(p_major_med_dip_sbb)+' & '+'{:0.2E}'.format(p_major_med_tpp_sbb))
print('\n')

# minor POTW
print('scb minor POTW ','{:0.2E}'.format(p_minor_med_flo_scb)+' & '+'{:0.2E}'.format(p_minor_med_tnn_scb)+' & '+'{:0.2E}'.format(p_minor_med_tnn_scb)+' & '+'{:0.2E}'.format(p_minor_med_tpp_scb)+' & '+'{:0.2E}'.format(p_minor_med_tpp_scb))
print('ssd minor POTW ','{:0.2E}'.format(p_minor_med_flo_ssd)+' & '+'{:0.2E}'.format(p_minor_med_tnn_ssd)+' & '+'{:0.2E}'.format(p_minor_med_tnn_ssd)+' & '+'{:0.2E}'.format(p_minor_med_tpp_ssd)+' & '+'{:0.2E}'.format(p_minor_med_tpp_ssd))
print('nsd minor POTW ','{:0.2E}'.format(p_minor_med_flo_nsd)+' & '+'{:0.2E}'.format(p_minor_med_tnn_nsd)+' & '+'{:0.2E}'.format(p_minor_med_tnn_nsd)+' & '+'{:0.2E}'.format(p_minor_med_tpp_nsd)+' & '+'{:0.2E}'.format(p_minor_med_tpp_nsd))
print('occ minor POTW ','{:0.2E}'.format(p_minor_med_flo_occ)+' & '+'{:0.2E}'.format(p_minor_med_tnn_occ)+' & '+'{:0.2E}'.format(p_minor_med_tnn_occ)+' & '+'{:0.2E}'.format(p_minor_med_tpp_occ)+' & '+'{:0.2E}'.format(p_minor_med_tpp_occ))
print('spp minor POTW ','{:0.2E}'.format(p_minor_med_flo_spp)+' & '+'{:0.2E}'.format(p_minor_med_tnn_spp)+' & '+'{:0.2E}'.format(p_minor_med_tnn_spp)+' & '+'{:0.2E}'.format(p_minor_med_tpp_spp)+' & '+'{:0.2E}'.format(p_minor_med_tpp_spp))
print('smm minor POTW ','{:0.2E}'.format(p_minor_med_flo_smm)+' & '+'{:0.2E}'.format(p_minor_med_tnn_smm)+' & '+'{:0.2E}'.format(p_minor_med_tnn_smm)+' & '+'{:0.2E}'.format(p_minor_med_tpp_smm)+' & '+'{:0.2E}'.format(p_minor_med_tpp_smm))
print('ven minor POTW ','{:0.2E}'.format(p_minor_med_flo_ven)+' & '+'{:0.2E}'.format(p_minor_med_tnn_ven)+' & '+'{:0.2E}'.format(p_minor_med_tnn_ven)+' & '+'{:0.2E}'.format(p_minor_med_tpp_ven)+' & '+'{:0.2E}'.format(p_minor_med_tpp_ven))
print('sbb minor POTW ','{:0.2E}'.format(p_minor_med_flo_sbb)+' & '+'{:0.2E}'.format(p_minor_med_tnn_sbb)+' & '+'{:0.2E}'.format(p_minor_med_tnn_sbb)+' & '+'{:0.2E}'.format(p_minor_med_tpp_sbb)+' & '+'{:0.2E}'.format(p_minor_med_tpp_sbb))
print('\n')


# inland POTW, DIN, TNN, DIP, TPP
print('scb inl POTW ','{:0.2E}'.format(inl_flo[7])+' & '+'{:0.2E}'.format(inl_din[7])+' & '+'{:0.2E}'.format(inl_tnn[7])+' & '+'{:0.2E}'.format(inl_dip[7])+' & '+'{:0.2E}'.format(inl_tpp[7]))
print('ssd inl POTW ','{:0.2E}'.format(inl_flo[0])+' & '+'{:0.2E}'.format(inl_din[0])+' & '+'{:0.2E}'.format(inl_tnn[0])+' & '+'{:0.2E}'.format(inl_dip[0])+' & '+'{:0.2E}'.format(inl_tpp[0]))
print('nsd inl POTW ','{:0.2E}'.format(inl_flo[1])+' & '+'{:0.2E}'.format(inl_din[1])+' & '+'{:0.2E}'.format(inl_tnn[1])+' & '+'{:0.2E}'.format(inl_dip[1])+' & '+'{:0.2E}'.format(inl_tpp[1]))
print('occ inl POTW ','{:0.2E}'.format(inl_flo[2])+' & '+'{:0.2E}'.format(inl_din[2])+' & '+'{:0.2E}'.format(inl_tnn[2])+' & '+'{:0.2E}'.format(inl_dip[2])+' & '+'{:0.2E}'.format(inl_tpp[2]))
print('spp inl POTW ','{:0.2E}'.format(inl_flo[3])+' & '+'{:0.2E}'.format(inl_din[3])+' & '+'{:0.2E}'.format(inl_tnn[3])+' & '+'{:0.2E}'.format(inl_dip[3])+' & '+'{:0.2E}'.format(inl_tpp[3]))
print('smm inl POTW ','{:0.2E}'.format(inl_flo[4])+' & '+'{:0.2E}'.format(inl_din[4])+' & '+'{:0.2E}'.format(inl_tnn[4])+' & '+'{:0.2E}'.format(inl_dip[4])+' & '+'{:0.2E}'.format(inl_tpp[4]))
print('ven inl POTW ','{:0.2E}'.format(inl_flo[5])+' & '+'{:0.2E}'.format(inl_din[5])+' & '+'{:0.2E}'.format(inl_tnn[5])+' & '+'{:0.2E}'.format(inl_dip[5])+' & '+'{:0.2E}'.format(inl_tpp[5]))
print('sbb inl POTW ','{:0.2E}'.format(inl_flo[6])+' & '+'{:0.2E}'.format(inl_din[6])+' & '+'{:0.2E}'.format(inl_tnn[6])+' & '+'{:0.2E}'.format(inl_dip[6])+' & '+'{:0.2E}'.format(inl_tpp[6]))
print('\n')

# river NPS print
print('scb NPS ','{:0.2E}'.format(nps_flo[7])+' & '+'{:0.2E}'.format(nps_din[7])+' & '+'{:0.2E}'.format(nps_tnn[7])+' & '+'{:0.2E}'.format(nps_dip[7])+' & '+'{:0.2E}'.format(nps_tpp[7]))
print('ssd NPS ','{:0.2E}'.format(nps_flo[0])+' & '+'{:0.2E}'.format(nps_din[0])+' & '+'{:0.2E}'.format(nps_tnn[0])+' & '+'{:0.2E}'.format(nps_dip[0])+' & '+'{:0.2E}'.format(nps_tpp[0]))
print('nsd NPS ','{:0.2E}'.format(nps_flo[1])+' & '+'{:0.2E}'.format(nps_din[1])+' & '+'{:0.2E}'.format(nps_tnn[1])+' & '+'{:0.2E}'.format(nps_dip[1])+' & '+'{:0.2E}'.format(nps_tpp[1]))
print('occ NPS ','{:0.2E}'.format(nps_flo[2])+' & '+'{:0.2E}'.format(nps_din[2])+' & '+'{:0.2E}'.format(nps_tnn[2])+' & '+'{:0.2E}'.format(nps_dip[2])+' & '+'{:0.2E}'.format(nps_tpp[2]))
print('spp NPS ','{:0.2E}'.format(nps_flo[3])+' & '+'{:0.2E}'.format(nps_din[3])+' & '+'{:0.2E}'.format(nps_tnn[3])+' & '+'{:0.2E}'.format(nps_dip[3])+' & '+'{:0.2E}'.format(nps_tpp[3]))
print('smm NPS ','{:0.2E}'.format(nps_flo[4])+' & '+'{:0.2E}'.format(nps_din[4])+' & '+'{:0.2E}'.format(nps_tnn[4])+' & '+'{:0.2E}'.format(nps_dip[4])+' & '+'{:0.2E}'.format(nps_tpp[4]))
print('ven NPS ','{:0.2E}'.format(nps_flo[5])+' & '+'{:0.2E}'.format(nps_din[5])+' & '+'{:0.2E}'.format(nps_tnn[5])+' & '+'{:0.2E}'.format(nps_dip[5])+' & '+'{:0.2E}'.format(nps_tpp[5]))
print('sbb NPS ','{:0.2E}'.format(nps_flo[6])+' & '+'{:0.2E}'.format(nps_din[6])+' & '+'{:0.2E}'.format(nps_tnn[6])+' & '+'{:0.2E}'.format(nps_dip[6])+' & '+'{:0.2E}'.format(nps_tpp[6]))
print('\n')

# river natural
print('scb nat ','{:0.2E}'.format(nat_flo[7])+' & '+'{:0.2E}'.format(nat_cur_din[7])+' & '+'{:0.2E}'.format(nat_cur_tnn[7])+' & '+'{:0.2E}'.format(nat_cur_dip[7])+' & '+'{:0.2E}'.format(nat_cur_tpp[7]))
print('ssd nat ','{:0.2E}'.format(nat_flo[0])+' & '+'{:0.2E}'.format(nat_cur_din[0])+' & '+'{:0.2E}'.format(nat_cur_tnn[0])+' & '+'{:0.2E}'.format(nat_cur_dip[0])+' & '+'{:0.2E}'.format(nat_cur_tpp[0]))
print('nsd nat ','{:0.2E}'.format(nat_flo[1])+' & '+'{:0.2E}'.format(nat_cur_din[1])+' & '+'{:0.2E}'.format(nat_cur_tnn[1])+' & '+'{:0.2E}'.format(nat_cur_dip[1])+' & '+'{:0.2E}'.format(nat_cur_tpp[1]))
print('occ nat ','{:0.2E}'.format(nat_flo[2])+' & '+'{:0.2E}'.format(nat_cur_din[2])+' & '+'{:0.2E}'.format(nat_cur_tnn[2])+' & '+'{:0.2E}'.format(nat_cur_dip[2])+' & '+'{:0.2E}'.format(nat_cur_tpp[2]))
print('spp nat ','{:0.2E}'.format(nat_flo[3])+' & '+'{:0.2E}'.format(nat_cur_din[3])+' & '+'{:0.2E}'.format(nat_cur_tnn[3])+' & '+'{:0.2E}'.format(nat_cur_dip[3])+' & '+'{:0.2E}'.format(nat_cur_tpp[3]))
print('smm nat ','{:0.2E}'.format(nat_flo[4])+' & '+'{:0.2E}'.format(nat_cur_din[4])+' & '+'{:0.2E}'.format(nat_cur_tnn[4])+' & '+'{:0.2E}'.format(nat_cur_dip[4])+' & '+'{:0.2E}'.format(nat_cur_tpp[4]))
print('ven nat ','{:0.2E}'.format(nat_flo[5])+' & '+'{:0.2E}'.format(nat_cur_din[5])+' & '+'{:0.2E}'.format(nat_cur_tnn[5])+' & '+'{:0.2E}'.format(nat_cur_dip[5])+' & '+'{:0.2E}'.format(nat_cur_tpp[5]))
print('sbb nat ','{:0.2E}'.format(nat_flo[6])+' & '+'{:0.2E}'.format(nat_cur_din[6])+' & '+'{:0.2E}'.format(nat_cur_tnn[6])+' & '+'{:0.2E}'.format(nat_cur_dip[6])+' & '+'{:0.2E}'.format(nat_cur_tpp[6]))
print('\n')
