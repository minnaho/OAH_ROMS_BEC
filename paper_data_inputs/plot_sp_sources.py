import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pickle as pickle

fig_path = './figs/'
# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc'

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

###############
# river major data (10 yrs) 1997-2007
###############
major_nc = Dataset(major_path,'r')

r_names_major = pickle.load(open('../river_data/river_names_10.pkl','rb'))

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

r_major_flo_ssd = np.array(r_major_flo[0][0])
r_major_flo_nsd = np.array(r_major_flo[1][0])
r_major_flo_occ = np.array(r_major_flo[2][0])
r_major_flo_spp = np.array(r_major_flo[3][0])
r_major_flo_smm = np.array(r_major_flo[4][0])
r_major_flo_ven = np.array(r_major_flo[5][0])
r_major_flo_sbb = np.array(r_major_flo[6][0])

r_major_tnn_ssd = np.array(r_major_tn[0][0])
r_major_tnn_nsd = np.array(r_major_tn[1][0])
r_major_tnn_occ = np.array(r_major_tn[2][0])
r_major_tnn_spp = np.array(r_major_tn[3][0])
r_major_tnn_smm = np.array(r_major_tn[4][0])
r_major_tnn_ven = np.array(r_major_tn[5][0])
r_major_tnn_sbb = np.array(r_major_tn[6][0])


##############
# river 24 yrs
##############
minor_nc = Dataset(minor_path,'r')

r_names_minor = pickle.load(open('../river_data/river_names_24.pkl','rb'))

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
r_minor_en_in = 287+1 # index for end of 2013
r_minor_flo = [[] for i in range(maskarr.shape[0])]
r_minor_tn = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    r_minor_flo[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())
    r_minor_tn[r_i].append(np.transpose(minor_flo[r_minor_st_in:r_minor_en_in,r_minor_ind[r_i],r_minor_ind[r_i]]*minor_tn[r_minor_st_in:r_minor_en_in,r_minor_ind[r_i],r_minor_ind[r_i]]).tolist())

# turn to array so can sum all rivers in region up
# then reshape to (17,12) because this data set is 17 years (1997-2013)
# then average over 17 years to get year average
ry1 = 17
#r_minor_flo_ssd = np.nanmean(np.nansum(np.array(r_minor_flo[0][0]),axis=0).reshape(ry1,12),axis=0)
#r_minor_flo_nsd = np.nanmean(np.nansum(np.array(r_minor_flo[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_flo_ssd = np.array(()) # no rivers fall into these regions
r_minor_flo_nsd = np.array(())
r_minor_flo_occ = np.array(r_minor_flo[2][0])
r_minor_flo_spp = np.array(r_minor_flo[3][0])
r_minor_flo_smm = np.array(r_minor_flo[4][0])
r_minor_flo_ven = np.array(r_minor_flo[5][0])
r_minor_flo_sbb = np.array(r_minor_flo[6][0])

#r_minor_tnn_ssd = np.nanmean(np.nansum(np.array(r_minor_tn[0][0])
#r_minor_tnn_nsd = np.nanmean(np.nansum(np.array(r_minor_tn[1][0]),axis=0).reshape(ry1,12),axis=0)
r_minor_tnn_ssd = np.array(()) # no rivers fall into these regions
r_minor_tnn_nsd = np.array(())
r_minor_tnn_occ = np.array(r_minor_tn[2][0])
r_minor_tnn_spp = np.array(r_minor_tn[3][0])
r_minor_tnn_smm = np.array(r_minor_tn[4][0])
r_minor_tnn_ven = np.array(r_minor_tn[5][0])
r_minor_tnn_sbb = np.array(r_minor_tn[6][0])


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
major_toc[major_toc>1E20] = np.nan

p_major_flo = [[] for i in range(maskarr.shape[0])]
p_major_tn = [[] for i in range(maskarr.shape[0])] # TN flux
p_major_toc = [[] for i in range(maskarr.shape[0])] # TN flux
for r_i in range(len(p_major_ind)):
    p_major_flo[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    # flux mmol/s
    p_major_tn[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_tn[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())
    p_major_toc[r_i].append(np.transpose(major_flo[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]*major_toc[potw_1997:potw_2013,p_major_ind[r_i],p_major_ind[r_i]]).tolist())

# turn to array so can sum all potw in region up
# then reshape to (17,12) because this data set is 17 years
# then average over 17 years to get year average
ry0 = 17

p_major_flo_ssd = np.squeeze(np.array(p_major_flo[0][0]))
p_major_flo_nsd = np.squeeze(np.zeros((12)))
p_major_flo_occ = np.squeeze(np.array(p_major_flo[2][0]))
p_major_flo_spp = np.squeeze(np.array(p_major_flo[3][0]))
p_major_flo_smm = np.squeeze(np.array(p_major_flo[4][0]))
p_major_flo_ven = np.squeeze(np.zeros((12)))
p_major_flo_sbb = np.squeeze(np.zeros((12)))

p_major_tnn_ssd = np.squeeze(np.array(p_major_tn[0][0]))
p_major_tnn_nsd = np.squeeze(np.zeros((12)))
p_major_tnn_occ = np.squeeze(np.array(p_major_tn[2][0]))
p_major_tnn_spp = np.squeeze(np.array(p_major_tn[3][0]))
p_major_tnn_smm = np.squeeze(np.array(p_major_tn[4][0]))
p_major_tnn_ven = np.squeeze(np.zeros((12)))
p_major_tnn_sbb = np.squeeze(np.zeros((12)))


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
minor_toc = np.array(potw_mi_nc.variables['TOC']) # mmol/m3

minor_tn = minor_no3+minor_nh4+minor_no2

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan
minor_toc[minor_toc>1E20] = np.nan

p_minor_flo = [[] for i in range(maskarr.shape[0])]
p_minor_tn = [[] for i in range(maskarr.shape[0])]
p_minor_toc = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(r_minor_ind)):
    p_minor_flo[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())
    p_minor_tn[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]*minor_tn[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())
    p_minor_toc[r_i].append(np.transpose(minor_flo[:12,p_minor_ind[r_i],p_minor_ind[r_i]]*minor_toc[:12,p_minor_ind[r_i],p_minor_ind[r_i]]).tolist())

# turn to array so can sum all minor potw in region up
p_minor_flo_ssd = np.array(p_minor_flo[0][0])
p_minor_flo_nsd = np.array(p_minor_flo[1][0])
p_minor_flo_occ = np.array(p_minor_flo[2][0])
p_minor_flo_spp = np.array(p_minor_flo[3][0])
p_minor_flo_smm = np.array(p_minor_flo[4][0])
p_minor_flo_ven = np.array(p_minor_flo[5][0])
p_minor_flo_sbb = np.array(p_minor_flo[6][0])

p_minor_tnn_ssd = np.array(p_minor_tn[0][0])
p_minor_tnn_nsd = np.array(p_minor_tn[1][0])
p_minor_tnn_occ = np.array(p_minor_tn[2][0])
p_minor_tnn_spp = np.array(p_minor_tn[3][0])
p_minor_tnn_smm = np.array(p_minor_tn[4][0])
p_minor_tnn_ven = np.array(p_minor_tn[5][0])
p_minor_tnn_sbb = np.array(p_minor_tn[6][0])

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

r_major_tnn_spp = (r_major_tnn_spp)*s_to_d*mmol_to_mol*g_N*g_to_kg
r_minor_tnn_spp = (r_minor_tnn_spp)*s_to_d*mmol_to_mol*g_N*g_to_kg
p_major_tnn_spp = (p_major_tnn_spp)*s_to_d*mmol_to_mol*g_N*g_to_kg
p_minor_tnn_spp = (p_minor_tnn_spp)*s_to_d*mmol_to_mol*g_N*g_to_kg
p_minor_tnn_spp = np.array(list(p_minor_tnn_spp)*ry1).reshape(ry1*p_minor_tnn_spp.shape[1])


p_minor_flo_spp = np.array(list(p_minor_flo_spp)*ry1).reshape(ry1*p_minor_flo_spp.shape[1])

# names
region_ind = 3
n_r_major = [r_names_major[i] for i in r_major_ind[region_ind]]
n_r_minor = [r_names_minor[i] for i in r_minor_ind[region_ind]]

n_r_minor[0] = 'Bolsa Chica\nWestminster Channel'
n_r_minor[3] = 'E Garden Grove\nWintersberg Channel'

n_p_major = 'JWPCP'
n_p_minor = 'Terminal Island WWTP'


#############
# plot
#############

figw = 12
figh = 8

axis_tick_font = 14

savename = fig_path+'sanpedro_ts.pdf'

r_col = 'blue'
p_col = 'orange'
l_sty = ['-','--',':','-.']
l_size0 = [1,1,1,1]
l_size1 = [3,3,3,3]

plt.ion()

fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
for i_ind in range(len(r_minor_ind[region_ind])):
    axes.flat[0].plot(minor_time_dt[r_minor_st_in:r_minor_en_in],r_minor_flo_spp[i_ind],label=n_r_minor[i_ind],linestyle=l_sty[i_ind],linewidth=l_size0[i_ind],color=r_col)

for i_ind in range(len(r_major_ind[region_ind])):
    axes.flat[0].plot(major_time_dt,r_major_flo_spp[i_ind],label=n_r_major[i_ind],linestyle=l_sty[i_ind],linewidth=l_size1[i_ind],color=r_col)

axes.flat[0].plot(major_potw_time_dt,p_major_flo_spp,label=n_p_major,linestyle=l_sty[0],linewidth=l_size1[0],color=p_col)
axes.flat[0].plot(major_potw_time_dt,p_minor_flo_spp,label=n_p_minor,linestyle=l_sty[1],linewidth=l_size0[0],color=p_col)

for i_ind in range(len(r_minor_ind[region_ind])):
    axes.flat[1].plot(minor_time_dt[r_minor_st_in:r_minor_en_in],r_minor_tnn_spp[i_ind],label=n_r_minor[i_ind],linestyle=l_sty[i_ind],linewidth=l_size0[i_ind],color=r_col)

for i_ind in range(len(r_major_ind[region_ind])):
    axes.flat[1].plot(major_time_dt,r_major_tnn_spp[i_ind],label=n_r_major[i_ind],linestyle=l_sty[i_ind],linewidth=l_size1[i_ind],color=r_col)

axes.flat[1].plot(major_potw_time_dt,p_major_tnn_spp,label=n_p_major,linestyle=l_sty[0],linewidth=l_size1[0],color=p_col)
axes.flat[1].plot(major_potw_time_dt,p_minor_tnn_spp,label=n_p_minor,linestyle=l_sty[1],linewidth=l_size0[0],color=p_col)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux\n kg d$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].legend(bbox_to_anchor=(1.01,1),loc='upper left',fontsize=axis_tick_font,columnspacing=.5,labelspacing=1)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font)
#axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
#loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename,bbox_inches='tight')

