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
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
setting = 'bight'

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

################
# load atmos data
################

grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
atmos_data = Dataset(dataset_name,'r')
mask_mat = scipy.io.loadmat('../maskt.mat')['maskt'] # mask that is first 0-15km offshore
m2_to_hectare = 10000

grid_nc = Dataset(grid_path,'r')
lat_nc = np.array(grid_nc.variables['lat_rho'])
lon_nc = np.array(grid_nc.variables['lon_rho'])
mask_nc = np.array(grid_nc.variables['mask_rho'])

oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_to_hectare
redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_to_hectare
alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_to_hectare
fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_to_hectare

oxn_yr = np.sum(oxn,axis=0)
redn_yr = np.sum(redn,axis=0)
alk_yr = np.sum(alk,axis=0)
fe_yr = np.sum(fe,axis=0)

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

atmos_plt = np.sum(np.sum((oxn_all+redn_all),axis=1),axis=1)

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
r_major_tn = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_major_ind)):
    r_major_flo[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())
    r_major_tn[r_i].append(np.transpose(major_flo[:,r_major_ind[r_i],r_major_ind[r_i]]*major_tn[:,r_major_ind[r_i],r_major_ind[r_i]]).tolist())


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

r_minor_flo = [[] for i in range(maskarr.shape[0])]
r_minor_tn = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    r_minor_flo[r_i].append(np.transpose(minor_flo[:,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tn[r_i].append(np.transpose(minor_flo[:,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tn[:,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())

'''
# combine rivers 10 yrs and 24 yrs
# find days at beginning and end  
num_st = major_time_dt[0]-minor_time_dt[0]
num_en = minor_time_dt[-1]-major_time_dt[-1]

a = []
b = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_tn[num_st.days:-num_en.days,m_i,m_i])
    b.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_po4[num_st.days:-num_en.days,m_i,m_i])


# a,b shape (24,3650)
# sum up all rivers
minor_fluxn = np.nansum(np.array(a),axis=0)
minor_fluxp = np.nansum(np.array(b),axis=0)
minor_flo_short = np.nansum(np.nansum(minor_flo[num_st.days:-num_en.days,:,:],axis=1),axis=1)

minor_fluxn_sb = np.sum(np.array(a)[r_ind_24[0]],axis=0)
minor_fluxn_sm = np.sum(np.array(a)[r_ind_24[1]],axis=0)
minor_fluxn_sp = np.sum(np.array(a)[r_ind_24[2]],axis=0)
minor_fluxn_oc = np.sum(np.array(a)[r_ind_24[3]],axis=0)
minor_fluxn_sd = np.sum(np.array(a)[r_ind_24[4]],axis=0)
                                                
minor_fluxp_sb = np.sum(np.array(b)[r_ind_24[0]],axis=0)
minor_fluxp_sm = np.sum(np.array(b)[r_ind_24[1]],axis=0)
minor_fluxp_sp = np.sum(np.array(b)[r_ind_24[2]],axis=0)
minor_fluxp_oc = np.sum(np.array(b)[r_ind_24[3]],axis=0)
minor_fluxp_sd = np.sum(np.array(b)[r_ind_24[4]],axis=0)

a = []
b = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])
    b.append(major_flo[:,m_i,m_i]*major_po4[:,m_i,m_i])

# sum up all rivers
major_fluxn = np.nansum(np.array(a),axis=0)
major_fluxp = np.nansum(np.array(b),axis=0)
major_flo_sum = np.nansum(np.nansum(major_flo[:,:,:],axis=1),axis=1)

major_fluxn_sb = np.sum(np.array(a)[r_ind_10[0]],axis=0)
major_fluxn_sm = np.sum(np.array(a)[r_ind_10[1]],axis=0)
major_fluxn_sp = np.sum(np.array(a)[r_ind_10[2]],axis=0)
major_fluxn_oc = np.sum(np.array(a)[r_ind_10[3]],axis=0)
major_fluxn_sd = np.sum(np.array(a)[r_ind_10[4]],axis=0)
                                         
major_fluxp_sb = np.sum(np.array(b)[r_ind_10[0]],axis=0)
major_fluxp_sm = np.sum(np.array(b)[r_ind_10[1]],axis=0)
major_fluxp_sp = np.sum(np.array(b)[r_ind_10[2]],axis=0)
major_fluxp_oc = np.sum(np.array(b)[r_ind_10[3]],axis=0)
major_fluxp_sd = np.sum(np.array(b)[r_ind_10[4]],axis=0)

r_fluxn_sb = major_fluxn_sb+minor_fluxn_sb
r_fluxn_sm = major_fluxn_sm+minor_fluxn_sm
r_fluxn_sp = major_fluxn_sp+minor_fluxn_sp
r_fluxn_sd = major_fluxn_sd+minor_fluxn_sd
r_fluxn_oc = major_fluxn_oc+minor_fluxn_oc

r_flo = major_flo_sum+minor_flo_short
r_fluxn = major_fluxn+minor_fluxn
r_fluxp = major_fluxp+minor_fluxp # mmol/s

# find indices for each season
r_1 = []
r_2 = []
r_3 = []
r_4 = []
r_5 = []
r_6 = []
r_7 = []
r_8 = []
r_9 = []
r_10 = []
r_11 = []
r_12 = []
for d_i in range(len(major_time_dt)):
    if major_time_dt[d_i].month == 1:  
        r_1.append(d_i)
    if major_time_dt[d_i].month == 2:  
        r_2.append(d_i)
    if major_time_dt[d_i].month == 3:  
        r_3.append(d_i)
    if major_time_dt[d_i].month == 4:  
        r_4.append(d_i)
    if major_time_dt[d_i].month == 5:  
        r_5.append(d_i)
    if major_time_dt[d_i].month == 6:  
        r_6.append(d_i)
    if major_time_dt[d_i].month == 7:  
        r_7.append(d_i)
    if major_time_dt[d_i].month == 8:  
        r_8.append(d_i)
    if major_time_dt[d_i].month == 9:  
        r_9.append(d_i)
    if major_time_dt[d_i].month == 10:  
        r_10.append(d_i)
    if major_time_dt[d_i].month == 11:  
        r_11.append(d_i)
    if major_time_dt[d_i].month == 12:  
        r_12.append(d_i)

r_months_ind = [r_1,r_2,r_3,r_4,r_5,r_6,r_7,r_8,r_9,r_10,r_11,r_12]

# monthly climatology
r_flo_mon = np.empty((12))
r_n_mon = np.empty((12))
r_p_mon = np.empty((12))
# monthly climatology by region
r_n_mon_sb = np.empty((12))
r_n_mon_sm = np.empty((12))
r_n_mon_sp = np.empty((12))
r_n_mon_oc = np.empty((12))
r_n_mon_sd = np.empty((12))
for r_i in range(len(r_months_ind)):
    r_n_mon[r_i] = np.nanmean(r_fluxn[r_i])
    r_p_mon[r_i] = np.nanmean(r_fluxp[r_i])
    r_flo_mon[r_i] = np.nanmean(r_flo[r_i])
    r_n_mon_sb[r_i] = np.nanmean(r_fluxn_sb[r_i])
    r_n_mon_sm[r_i] = np.nanmean(r_fluxn_sm[r_i])
    r_n_mon_sp[r_i] = np.nanmean(r_fluxn_sp[r_i])
    r_n_mon_sd[r_i] = np.nanmean(r_fluxn_sd[r_i])
    r_n_mon_oc[r_i] = np.nanmean(r_fluxn_oc[r_i])

np.save('river_monthly_flo_all.npy',r_flo_mon)
np.save('river_monthly_nflux_all.npy',r_n_mon)
np.save('river_monthly_pflux_all.npy',r_p_mon)
    
r_season_n = np.array([(r_n_mon[11])+(r_n_mon[1])+(r_n_mon[0]),(r_n_mon[2])+(r_n_mon[3])+(r_n_mon[4]),(r_n_mon[5])+(r_n_mon[6])+(r_n_mon[7]),(r_n_mon[8])+(r_n_mon[9])+(r_n_mon[10])])

r_season_p = np.array([(r_p_mon[11])+(r_p_mon[1])+(r_p_mon[0]),(r_p_mon[2])+(r_p_mon[3])+(r_p_mon[4]),(r_p_mon[5])+(r_p_mon[6])+(r_p_mon[7]),(r_p_mon[8])+(r_p_mon[9])+(r_p_mon[10])])

# yearly flux of n per region
r_sb_yr = np.nansum(r_n_mon_sb)
r_sm_yr = np.nansum(r_n_mon_sm)
r_sp_yr = np.nansum(r_n_mon_sp)
r_sd_yr = np.nansum(r_n_mon_sd)
r_oc_yr = np.nansum(r_n_mon_oc)
   
##################
# potws
##################
potw_ma_nc = Dataset(potw_major_path,'r')
potw_mi_nc = Dataset(potw_minor_path,'r')

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
minor_potw_lat = np.array(potw_mi_nc.variables['latitude'])

p_ind_ma_sb = np.where(major_potw_lat>lat_sites[0])[0]
p_ind_ma_sm = np.where((major_potw_lat<lat_sites[0])&(major_potw_lat>lat_sites[1]))[0]
p_ind_ma_sp = np.where((major_potw_lat<lat_sites[1])&(major_potw_lat>lat_sites[2]))[0]
p_ind_ma_oc = np.where((major_potw_lat<lat_sites[2])&(major_potw_lat>lat_sites[3]))[0]
p_ind_ma_sd = np.where(major_potw_lat<lat_sites[3])[0]
p_ind_ma = np.array((p_ind_ma_sb,p_ind_ma_sm,p_ind_ma_sp,p_ind_ma_oc,p_ind_ma_sd))

p_ind_mi_sb = np.where(minor_potw_lat>lat_sites[0])[0]
p_ind_mi_sm = np.where((minor_potw_lat<lat_sites[0])&(minor_potw_lat>lat_sites[1]))[0]
p_ind_mi_sp = np.where((minor_potw_lat<lat_sites[1])&(minor_potw_lat>lat_sites[2]))[0]
p_ind_mi_oc = np.where((minor_potw_lat<lat_sites[2])&(minor_potw_lat>lat_sites[3]))[0]
p_ind_mi_sd = np.where(minor_potw_lat<lat_sites[3])[0]
p_ind_mi = np.array((p_ind_mi_sb,p_ind_mi_sm,p_ind_mi_sp,p_ind_mi_oc,p_ind_mi_sd))

major_potw_flo = np.array(potw_ma_nc.variables['flow'][potw_1997:potw_2013]) # m3/s
major_potw_nh4 = np.array(potw_ma_nc.variables['NH4'][potw_1997:potw_2013]) # mmol/m3
major_potw_no3 = np.array(potw_ma_nc.variables['NO3'][potw_1997:potw_2013]) # mmol/m3
major_potw_no2 = np.array(potw_ma_nc.variables['NO2'][potw_1997:potw_2013]) # mmol/m3
major_potw_po4 = np.array(potw_ma_nc.variables['PO4'][potw_1997:potw_2013]) # mmol/m3

minor_potw_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_potw_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_potw_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_potw_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_potw_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

major_potw_tn = major_potw_no3+major_potw_nh4+major_potw_no2

major_potw_flo[major_potw_flo>1E20] = np.nan
major_potw_tn[major_potw_tn>1E20] = np.nan
major_potw_po4[major_potw_po4>1E20] = np.nan

minor_potw_tn = minor_potw_no3+minor_potw_nh4+minor_potw_no2

minor_potw_flo[minor_potw_flo>1E20] = np.nan
minor_potw_tn[minor_potw_tn>1E20] = np.nan
minor_potw_po4[minor_potw_po4>1E20] = np.nan

# loads of all potws
a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_tn[:,m_i,m_i])

major_potw_fluxalln = np.nansum(np.array(a),axis=0)

major_potw_fluxn_sb = np.sum(np.array(a)[p_ind_ma[0]],axis=0)
major_potw_fluxn_sm = np.sum(np.array(a)[p_ind_ma[1]],axis=0)
major_potw_fluxn_sp = np.sum(np.array(a)[p_ind_ma[2]],axis=0)
major_potw_fluxn_oc = np.sum(np.array(a)[p_ind_ma[3]],axis=0)
major_potw_fluxn_sd = np.sum(np.array(a)[p_ind_ma[4]],axis=0)

a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_po4[:,m_i,m_i])
major_potw_fluxallp = np.nansum(np.array(a),axis=0)

# already in monthly clim
iend_minor = 12
a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_tn[:iend_minor,m_i,m_i])

minor_potw_fluxalln = np.nansum(np.array(a),axis=0)

minor_potw_fluxn_sb = np.sum(np.array(a)[p_ind_mi[0]],axis=0)
minor_potw_fluxn_sm = np.sum(np.array(a)[p_ind_mi[1]],axis=0)
minor_potw_fluxn_sp = np.sum(np.array(a)[p_ind_mi[2]],axis=0)
minor_potw_fluxn_oc = np.sum(np.array(a)[p_ind_mi[3]],axis=0)
minor_potw_fluxn_sd = np.sum(np.array(a)[p_ind_mi[4]],axis=0)

a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_po4[:iend_minor,m_i,m_i])
minor_potw_fluxallp = np.nansum(np.array(a),axis=0)


# find indices for each season
r_potw_1 = []
r_potw_2 = []
r_potw_3 = []
r_potw_4 = []
r_potw_5 = []
r_potw_6 = []
r_potw_7 = []
r_potw_8 = []
r_potw_9 = []
r_potw_10 = []
r_potw_11 = []
r_potw_12 = []
for d_i in range(len(major_potw_time_dt)):
    if major_potw_time_dt[d_i].month == 1:  
        r_potw_1.append(d_i)
    if major_potw_time_dt[d_i].month == 2:  
        r_potw_2.append(d_i)
    if major_potw_time_dt[d_i].month == 3:  
        r_potw_3.append(d_i)
    if major_potw_time_dt[d_i].month == 4:  
        r_potw_4.append(d_i)
    if major_potw_time_dt[d_i].month == 5:  
        r_potw_5.append(d_i)
    if major_potw_time_dt[d_i].month == 6:  
        r_potw_6.append(d_i)
    if major_potw_time_dt[d_i].month == 7:  
        r_potw_7.append(d_i)
    if major_potw_time_dt[d_i].month == 8:  
        r_potw_8.append(d_i)
    if major_potw_time_dt[d_i].month == 9:  
        r_potw_9.append(d_i)
    if major_potw_time_dt[d_i].month == 10:  
        r_potw_10.append(d_i)
    if major_potw_time_dt[d_i].month == 11:  
        r_potw_11.append(d_i)
    if major_potw_time_dt[d_i].month == 12:  
        r_potw_12.append(d_i)


potw_months_ind = [r_potw_1,r_potw_2,r_potw_3,r_potw_4,r_potw_5,r_potw_6,r_potw_7,r_potw_8,r_potw_9,r_potw_10,r_potw_11,r_potw_12]

potw_flo_mon = np.empty((12))
potw_n_mon = np.empty((12))
potw_p_mon = np.empty((12))
# monthly climatology by region
potw_n_mon_sb = np.empty((12))
potw_n_mon_sm = np.empty((12))
potw_n_mon_sp = np.empty((12))
potw_n_mon_oc = np.empty((12))
potw_n_mon_sd = np.empty((12))
for r_i in range(len(potw_months_ind)):
    potw_n_mon[r_i] = np.nanmean(major_potw_fluxalln[r_i])
    potw_p_mon[r_i] = np.nanmean(major_potw_fluxallp[r_i])
    potw_n_mon_sb[r_i] = np.nanmean(major_potw_fluxn_sb[r_i])
    potw_n_mon_sm[r_i] = np.nanmean(major_potw_fluxn_sm[r_i])
    potw_n_mon_sp[r_i] = np.nanmean(major_potw_fluxn_sp[r_i])
    potw_n_mon_sd[r_i] = np.nanmean(major_potw_fluxn_sd[r_i])
    potw_n_mon_oc[r_i] = np.nanmean(major_potw_fluxn_oc[r_i])
    
major_potw_season_n = np.array([(potw_n_mon[11])+(potw_n_mon[1])+(potw_n_mon[0]),(potw_n_mon[2])+(potw_n_mon[3])+(potw_n_mon[4]),(potw_n_mon[5])+(potw_n_mon[6])+(potw_n_mon[7]),(potw_n_mon[8])+(potw_n_mon[9])+(potw_n_mon[10])])

major_potw_season_p = np.array([(potw_p_mon[11])+(potw_p_mon[1])+(potw_p_mon[0]),(potw_p_mon[2])+(potw_p_mon[3])+(potw_p_mon[4]),(potw_p_mon[5])+(potw_p_mon[6])+(potw_p_mon[7]),(potw_p_mon[8])+(potw_p_mon[9])+(potw_p_mon[10])])

all_potw_n_mon = potw_n_mon+minor_potw_fluxalln
all_potw_p_mon = potw_p_mon+minor_potw_fluxallp

all_potw_season_n = np.array([(all_potw_n_mon[11])+(all_potw_n_mon[1])+(all_potw_n_mon[0]),(all_potw_n_mon[2])+(all_potw_n_mon[3])+(all_potw_n_mon[4]),(all_potw_n_mon[5])+(all_potw_n_mon[6])+(all_potw_n_mon[7]),(all_potw_n_mon[8])+(all_potw_n_mon[9])+(all_potw_n_mon[10])])

all_potw_season_p = np.array([(all_potw_p_mon[11])+(all_potw_p_mon[1])+(all_potw_p_mon[0]),(all_potw_p_mon[2])+(all_potw_p_mon[3])+(all_potw_p_mon[4]),(all_potw_p_mon[5])+(all_potw_p_mon[6])+(all_potw_p_mon[7]),(all_potw_p_mon[8])+(all_potw_p_mon[9])+(all_potw_p_mon[10])])

p_fluxn_sb = potw_n_mon_sb+minor_potw_fluxn_sb
p_fluxn_sm = potw_n_mon_sm+minor_potw_fluxn_sm
p_fluxn_sp = potw_n_mon_sp+minor_potw_fluxn_sp
p_fluxn_sd = potw_n_mon_sd+minor_potw_fluxn_sd
p_fluxn_oc = potw_n_mon_oc+minor_potw_fluxn_oc


# yearly flux of n per region
p_sb_yr = np.nansum(p_fluxn_sb)
p_sm_yr = np.nansum(p_fluxn_sm)
p_sp_yr = np.nansum(p_fluxn_sp)
p_sd_yr = np.nansum(p_fluxn_sd)
p_oc_yr = np.nansum(p_fluxn_oc)

#############
# plot
#############
a_yr = np.array((atmos_sb,atmos_sm,atmos_sp,atmos_oc,atmos_sd))
p_yr = np.array((p_sb_yr,p_sm_yr,p_sp_yr,p_oc_yr,p_sd_yr))
r_yr = np.array((r_sb_yr,r_sm_yr,r_sp_yr,r_oc_yr,r_sd_yr))

figw = 12
figh = 8
seasons = ['Winter','Spring','Summer','Fall']
regions = ['Santa Barbara','Santa Monica','San Pedro','Orange County','San Diego']
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
ax.set_xticks([width,1+width,2+width,3+width,4+width])
ax.set_xticklabels(['Santa Barbara','Santa Monica','San Pedro','Orange County','San Diego'])
#ax.set_yscale('log')
#ax.set_ybound(lower=10E-1,upper=25E5)
ax.set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
#ax.tick_params(axis='both',which='minor',labelsize=axis_font)
ax.legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)

plt.savefig(savename,bbox_inches='tight')

'''
