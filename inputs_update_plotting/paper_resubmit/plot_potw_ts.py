import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import scipy.io
import cmocean as cmocean

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc'
fig_path = './figs/'

#convert to kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# conversions mg/L to mmol/m3
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855
mg_l_a = 1000/100.09 # mg/L CaCO3 to mmol/m3

###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time_dt = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False)
'''
# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)
'''


major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2']) # mmol/m3
major_on = np.array(major_nc.variables['organic_N']) # mmol/m3
major_bod = np.array(major_nc.variables['BOD']) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4']) # mmol/m3
major_op = np.array(major_nc.variables['organic_P']) # mmol/m3
major_fe  = np.array(major_nc.variables['dissolved_Fe'])  # mmol/m3
major_pH  = np.array(major_nc.variables['pH']) 
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_salt = np.array(major_nc.variables['salinity']) 
major_toc = np.array(major_nc.variables['total_organic_C']) 
major_tnn = np.array(major_nc.variables['total_N']) 


major_nh4[major_nh4>1E10] == np.nan
major_no3[major_no3>1E10] == np.nan
major_no2[major_no2>1E10] == np.nan
major_on[major_on>1E10] == np.nan

major_tn = major_nh4+major_no3+major_no2+major_on
major_din = major_nh4+major_no3+major_no2
major_tp = major_po4+major_op

major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_toc[major_toc>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

##############
# minor data
##############
minor_nc = Dataset(minor_path,'r')
minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(minor_nc.variables['NO2']) # mmol/m3
minor_on = np.array(minor_nc.variables['organic_N']) # mmol/m3
minor_bod = np.array(minor_nc.variables['BOD']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['PO4']) # mmol/m3
minor_op = np.array(minor_nc.variables['organic_P']) # mmol/m3
minor_fe  = np.array(minor_nc.variables['dissolved_Fe'])  # mmol/m3
minor_pH  = np.array(minor_nc.variables['pH']) 
minor_alk = np.array(minor_nc.variables['alkalinity']) 
minor_temp = np.array(minor_nc.variables['temperature']) 
minor_salt = np.array(minor_nc.variables['salinity']) 
minor_toc = np.array(minor_nc.variables['total_organic_C']) 

minor_nh4[minor_nh4>1E10] == np.nan
minor_no3[minor_no3>1E10] == np.nan
minor_no2[minor_no2>1E10] == np.nan
minor_on[minor_on>1E10] == np.nan

minor_tn = minor_nh4+minor_no3+minor_no2+minor_on
minor_din = minor_nh4+minor_no3+minor_no2
minor_tp = minor_po4+minor_op

minor_tn[minor_tn>1E20] = np.nan
minor_tp[minor_tp>1E20] = np.nan
minor_toc[minor_toc>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

# plotting major
figw = 10
#figw = 12
figh = 12
axis_tick_font = 14
axis_font = 14
major_names = ['HTP','JWPCP','OC San','PLWTP']
major_linesty = ['-','--','-.',':']
lw = 2
plwtp_st = 170
iend_major = major_time_dt.shape[0]
savename_major = fig_path+'major_potw_ts.pdf'

plt.ion()

fig,axes = plt.subplots(7,1,sharex=True,figsize=[figw,figh+2])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt,(1./mg_l_n)*major_nh4[:,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt,(1./mg_l_n)*major_no3[:,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[2].plot(major_time_dt,(1./mg_l_n)*major_on[:,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[3].plot(major_time_dt,(1./mg_l_o)*major_bod[:,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[4].plot(major_time_dt,major_flo[:,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[5].plot(major_time_dt,major_flo[:,p_i]*major_din[:,p_i]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[6].plot(major_time_dt,major_flo[:,p_i]*major_on[:,p_i]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    #axes.flat[0].set_ybound(lower=0)
    axes.flat[0].set_ylabel('NH4\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[1].set_ylabel('NO3\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[2].set_ylabel('ON\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[3].set_ylabel('BOD\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[4].set_ylabel('Volume Flux\nm$^3$ s$^{-1}$',fontsize=axis_font)
    axes.flat[5].set_ylabel('DIN Flux\nkg d$^{-1}$',fontsize=axis_font)
    axes.flat[6].set_ylabel('ON Flux\nkg d$^{-1}$',fontsize=axis_font)
    for i in range(len(axes.flat)):
        axes.flat[i].tick_params(axis='both',which='major',labelsize=axis_tick_font)
        axes.flat[i].yaxis.set_ticks_position('both')
        axes.flat[i].xaxis.set_ticks_position('both')
        

axes.flat[0].yaxis.set_major_locator(mtick.MultipleLocator(10))
axes.flat[1].yaxis.set_major_locator(mtick.MultipleLocator(5))
axes.flat[2].yaxis.set_major_locator(mtick.MultipleLocator(5))
axes.flat[3].yaxis.set_major_locator(mtick.MultipleLocator(100))
#axes.flat[4].yaxis.set_major_locator(mtick.MultipleLocator(5))
axes.flat[5].yaxis.set_major_locator(mtick.MultipleLocator(15000))
axes.flat[6].yaxis.set_major_locator(mtick.MultipleLocator(10000))
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
#axes.flat[5].set_yscale('log')
#axes.flat[5].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
#axes.flat[5].set_ybound(lower=0,upper=1.7E5)
fig.savefig(savename_major,bbox_inches='tight')


###############
# minor data
###############
# split into regions for time series
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

# multiply masks by 0-15km mask to exclude island minor potws
for j_i in range(maskarr.shape[0]):
    maskarr[j_i] = maskarr[j_i]*mask_mat

minor_nc = Dataset(minor_path,'r')

minor_potw_lat = np.array(minor_nc.variables['latitude'])
minor_potw_lon = np.array(minor_nc.variables['longitude'])

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

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units,only_use_cftime_datetimes=False)

mi_st = 120 # 2007-01-31
mi_en = minor_time.shape[0] # 2007-01-31

minor_time_dt = minor_time[mi_st:mi_en]

minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(minor_nc.variables['NO2']) # mmol/m3
minor_bod = np.array(minor_nc.variables['BOD']) # mmol/m3
minor_onn = np.array(minor_nc.variables['organic_N']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['PO4']) # mmol/m3

minor_tn = minor_no3+minor_nh4+minor_no2+minor_onn
minor_din = minor_no3+minor_nh4+minor_no2

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_din[minor_din>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

p_minor_flo = [[] for i in range(maskarr.shape[0])]
p_minor_onn = [[] for i in range(maskarr.shape[0])]
p_minor_bod = [[] for i in range(maskarr.shape[0])]
p_minor_nh4 = [[] for i in range(maskarr.shape[0])]
p_minor_no3 = [[] for i in range(maskarr.shape[0])]
p_minor_din = [[] for i in range(maskarr.shape[0])]
for r_i in range(len(p_minor_ind)):
    p_minor_flo[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]).tolist())
    p_minor_onn[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]*minor_onn[mi_st:mi_en,p_minor_ind[r_i]]).tolist())
    p_minor_bod[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]*minor_bod[mi_st:mi_en,p_minor_ind[r_i]]).tolist())
    p_minor_nh4[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]*minor_nh4[mi_st:mi_en,p_minor_ind[r_i]]).tolist())
    p_minor_no3[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]*minor_no3[mi_st:mi_en,p_minor_ind[r_i]]).tolist())
    p_minor_din[r_i].append(np.transpose(minor_flo[mi_st:mi_en,p_minor_ind[r_i]]*minor_din[mi_st:mi_en,p_minor_ind[r_i]]).tolist())

p_minor_flo_ssd = np.nansum(np.array(p_minor_flo[0][0]),axis=0)
p_minor_flo_nsd = np.nansum(np.array(p_minor_flo[1][0]),axis=0)
p_minor_flo_occ = np.nansum(np.array(p_minor_flo[2][0]),axis=0)
p_minor_flo_spp = np.nansum(np.array(p_minor_flo[3][0]),axis=0)
p_minor_flo_smm = np.nansum(np.array(p_minor_flo[4][0]),axis=0)
#p_minor_flo_smm =np.zeros((12))
p_minor_flo_ven = np.nansum(np.array(p_minor_flo[5][0]),axis=0)
p_minor_flo_sbb = np.nansum(np.array(p_minor_flo[6][0]),axis=0)

p_minor_onn_ssd = np.nansum(np.array(p_minor_onn[0][0]),axis=0)
p_minor_onn_nsd = np.nansum(np.array(p_minor_onn[1][0]),axis=0)
p_minor_onn_occ = np.nansum(np.array(p_minor_onn[2][0]),axis=0)
p_minor_onn_spp = np.nansum(np.array(p_minor_onn[3][0]),axis=0)
p_minor_onn_smm = np.nansum(np.array(p_minor_onn[4][0]),axis=0)
#p_minor_onn_smm =np.zeros((12))
p_minor_onn_ven = np.nansum(np.array(p_minor_onn[5][0]),axis=0)
p_minor_onn_sbb = np.nansum(np.array(p_minor_onn[6][0]),axis=0)

p_minor_bod_ssd = np.nansum(np.array(p_minor_bod[0][0]),axis=0)
p_minor_bod_nsd = np.nansum(np.array(p_minor_bod[1][0]),axis=0)
p_minor_bod_occ = np.nansum(np.array(p_minor_bod[2][0]),axis=0)
p_minor_bod_spp = np.nansum(np.array(p_minor_bod[3][0]),axis=0)
p_minor_bod_smm = np.nansum(np.array(p_minor_bod[4][0]),axis=0)
#p_minor_bod_smm =np.zeros((12))
p_minor_bod_ven = np.nansum(np.array(p_minor_bod[5][0]),axis=0)
p_minor_bod_sbb = np.nansum(np.array(p_minor_bod[6][0]),axis=0)

p_minor_nh4_ssd = np.nansum(np.array(p_minor_nh4[0][0]),axis=0)
p_minor_nh4_nsd = np.nansum(np.array(p_minor_nh4[1][0]),axis=0)
p_minor_nh4_occ = np.nansum(np.array(p_minor_nh4[2][0]),axis=0)
p_minor_nh4_spp = np.nansum(np.array(p_minor_nh4[3][0]),axis=0)
p_minor_nh4_smm = np.nansum(np.array(p_minor_nh4[4][0]),axis=0)
#p_minor_nh4_smm =np.zeros((12))
p_minor_nh4_ven = np.nansum(np.array(p_minor_nh4[5][0]),axis=0)
p_minor_nh4_sbb = np.nansum(np.array(p_minor_nh4[6][0]),axis=0)

p_minor_no3_ssd = np.nansum(np.array(p_minor_no3[0][0]),axis=0)
p_minor_no3_nsd = np.nansum(np.array(p_minor_no3[1][0]),axis=0)
p_minor_no3_occ = np.nansum(np.array(p_minor_no3[2][0]),axis=0)
p_minor_no3_spp = np.nansum(np.array(p_minor_no3[3][0]),axis=0)
p_minor_no3_smm = np.nansum(np.array(p_minor_no3[4][0]),axis=0)
#p_minor_no3_smm =np.zeros((12))
p_minor_no3_ven = np.nansum(np.array(p_minor_no3[5][0]),axis=0)
p_minor_no3_sbb = np.nansum(np.array(p_minor_no3[6][0]),axis=0)

p_minor_din_ssd = np.nansum(np.array(p_minor_din[0][0]),axis=0)
p_minor_din_nsd = np.nansum(np.array(p_minor_din[1][0]),axis=0)
p_minor_din_occ = np.nansum(np.array(p_minor_din[2][0]),axis=0)
p_minor_din_spp = np.nansum(np.array(p_minor_din[3][0]),axis=0)
p_minor_din_smm = np.nansum(np.array(p_minor_din[4][0]),axis=0)
#p_minor_din_smm =np.zeros((12))
p_minor_din_ven = np.nansum(np.array(p_minor_din[5][0]),axis=0)
p_minor_din_sbb = np.nansum(np.array(p_minor_din[6][0]),axis=0)

# m3/s
p_minor_flo = np.array((p_minor_flo_ssd,p_minor_flo_nsd,p_minor_flo_occ,p_minor_flo_spp,np.ones((p_minor_flo_ssd.shape[0]))*np.nan,p_minor_flo_ven,p_minor_flo_sbb))[::-1]

# fluxes mmol/s
p_minor_onn = np.array((p_minor_onn_ssd,p_minor_onn_nsd,p_minor_onn_occ,p_minor_onn_spp,np.ones((p_minor_onn_ssd.shape[0]))*np.nan,p_minor_onn_ven,p_minor_onn_sbb))[::-1]

p_minor_bod = np.array((p_minor_bod_ssd,p_minor_bod_nsd,p_minor_bod_occ,p_minor_bod_spp,np.ones((p_minor_onn_ssd.shape[0]))*np.nan,p_minor_bod_ven,p_minor_bod_sbb))[::-1]

p_minor_nh4 = np.array((p_minor_nh4_ssd,p_minor_nh4_nsd,p_minor_nh4_occ,p_minor_nh4_spp,np.ones((p_minor_onn_ssd.shape[0]))*np.nan,p_minor_nh4_ven,p_minor_nh4_sbb))[::-1]

p_minor_no3 = np.array((p_minor_no3_ssd,p_minor_no3_nsd,p_minor_no3_occ,p_minor_no3_spp,np.ones((p_minor_onn_ssd.shape[0]))*np.nan,p_minor_no3_ven,p_minor_no3_sbb))[::-1]

p_minor_din = np.array((p_minor_din_ssd,p_minor_din_nsd,p_minor_din_occ,p_minor_din_spp,np.ones((p_minor_onn_ssd.shape[0]))*np.nan,p_minor_din_ven,p_minor_din_sbb))[::-1]

# get colors matching map for each region
cmcolors = cmocean.cm.thermal(np.linspace(0,1,maskarr.shape[0]))
cmcolors = list(cmcolors)[:-1]+['gold']
cmcolors = cmcolors[::-1]
minor_names = ['SSD','NSD','OC','SP','','V','SB'][::-1]


# no santa monica - no minor POTWs
# plot

savename_minor = fig_path+'minor_potw_ts.pdf'
minor_linesty = ['-','--','-','-.',':',(0, (3, 1, 1, 1, 1, 1)),'-']

fig,axes = plt.subplots(7,1,sharex=True,figsize=[figw,figh+2])
for p_i in range(p_minor_flo.shape[0]):
    if minor_names[p_i] != '' or minor_names[p_i] != 'SSD':
        axes.flat[0].plot(minor_time_dt,(1./mg_l_n)*(p_minor_nh4[p_i]/p_minor_flo[p_i]),linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[1].plot(minor_time_dt,(1./mg_l_n)*(p_minor_no3[p_i]/p_minor_flo[p_i]),linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[2].plot(minor_time_dt,(1./mg_l_n)*(p_minor_onn[p_i]/p_minor_flo[p_i]),linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[3].plot(minor_time_dt,(1./mg_l_o)*(p_minor_bod[p_i]/p_minor_flo[p_i]),linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[4].plot(minor_time_dt,p_minor_flo[p_i],linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[5].plot(minor_time_dt,p_minor_din[p_i]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)
        axes.flat[6].plot(minor_time_dt,p_minor_onn[p_i]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=minor_linesty[p_i],label=minor_names[p_i],color=cmcolors[p_i],linewidth=lw)

    axes.flat[0].set_ylabel('NH4\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[1].set_ylabel('NO3\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[2].set_ylabel('ON\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[3].set_ylabel('BOD\nmg L$^{-1}$',fontsize=axis_font)
    axes.flat[4].set_ylabel('Volume Flux\nm$^3$ s$^{-1}$',fontsize=axis_font)
    axes.flat[5].set_ylabel('DIN Flux\nkg d$^{-1}$',fontsize=axis_font)
    axes.flat[6].set_ylabel('ON Flux\nkg d$^{-1}$',fontsize=axis_font)
    for i in range(len(axes.flat)):
        axes.flat[i].tick_params(axis='both',which='major',labelsize=axis_tick_font)
        axes.flat[i].yaxis.set_ticks_position('both')
        axes.flat[i].xaxis.set_ticks_position('both')

axes.flat[0].yaxis.set_major_locator(mtick.MultipleLocator(10))
axes.flat[1].yaxis.set_major_locator(mtick.MultipleLocator(5))
axes.flat[2].yaxis.set_major_locator(mtick.MultipleLocator(2))
axes.flat[3].yaxis.set_major_locator(mtick.MultipleLocator(20))
axes.flat[4].yaxis.set_major_locator(mtick.MultipleLocator(.5))
axes.flat[5].yaxis.set_major_locator(mtick.MultipleLocator(2000))
axes.flat[6].yaxis.set_major_locator(mtick.MultipleLocator(200))
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=6,mode='expand',borderaxespad=0.,handlelength=3)
#axes.flat[5].set_yscale('log')
#axes.flat[5].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
#axes.flat[5].set_ybound(lower=0,upper=1.7E5)
fig.savefig(savename_minor,bbox_inches='tight')


#major stats
# % change in DIN 
din_flux = major_flo[:,:]*major_din[:,:]*s_to_d*mmol_to_mol*g_to_kg*g_N
# take first and last value
din_perc = (din_flux[0,:]-din_flux[-1,:])/din_flux[0,:]
print('reduction in DIN fluxes 1971, 2017',din_perc)

# average over first 5 years and last 5 years
din_perc = (np.nanmean(din_flux[:12*5,:],axis=0)-np.nanmean(din_flux[din_flux.shape[0]-(12*5):,:],axis=0))/np.nanmean(din_flux[:12*5,:],axis=0)
print('reduction in DIN fluxes 1971-1976, 2013-2017',din_perc)

din_kg_yr = major_flo[:,:]*major_din[:,:]*s_to_d*d_to_mo*mmol_to_mol*g_to_kg*g_N
old_kg_yr = np.nanmean(np.nansum(np.nansum(din_kg_yr[:12*5,:],axis=1).reshape(5,12),axis=1))
new_kg_yr = np.nanmean(np.nansum(np.nansum(din_kg_yr[din_flux.shape[0]-(12*5):,:],axis=1).reshape(5,12),axis=1))

# DIN fluxes 1971-1976 kg/day vs 2013-2017 kg/day
din_kg_d = major_flo[:,:]*major_din[:,:]*s_to_d*mmol_to_mol*g_to_kg*g_N
old_kg_d = np.nanmean((np.nansum(din_kg_d[:12*5,:],axis=1)))
new_kg_d = np.nanmean((np.nansum(din_kg_d[din_flux.shape[0]-(12*5):,:],axis=1)))


# average over 1996-2000 and 2013-2017
din_perc = (np.nanmean(din_flux[300:300+(12*5),:],axis=0)-np.nanmean(din_flux[din_flux.shape[0]-(12*5):,:],axis=0))/np.nanmean(din_flux[300:300+(12*5),:],axis=0)
print('reduction in DIN fluxes 1996-2000, 2013-2017',din_perc)

# % change in ON 1970-1990 and 2017
on_flux = major_flo[:,:]*major_on[:,:]*s_to_d*mmol_to_mol*g_to_kg*g_N
# take first and last value
on_perc = (np.nanmean(on_flux[:12*20,:])-np.nanmean(on_flux[on_flux.shape[0]-(12):,:]))/np.nanmean(on_flux[:12*20,:])
print('reduction in ON fluxes 1970-1990, 2017',on_perc)

# minor stats
# average over 2007-2008 and 2016-2017
minor_din_flux = p_minor_din*s_to_d*mmol_to_mol*g_to_kg*g_N
minor_din_perc = (np.nanmean(minor_din_flux[:,:12*2],axis=1)-np.nanmean(minor_din_flux[:,minor_din_flux.shape[1]-(12*2):],axis=1))/np.nanmean(minor_din_flux[:,:12*2],axis=1)


# major average over 1997-2000 and 2013-2017 kg/d
din_old = np.nanmean(din_flux[300+(12*1):300+(12*5),:],axis=0)
din_new = np.nanmean(din_flux[din_flux.shape[0]-(12*5):,:],axis=0)
din_perc = (din_new-din_old)/din_old
print('din_old',din_old)
print('din_new',din_new)
print('reduction in din fluxes 1997-2000, 2013-2017',din_perc*100)

onn_flux = major_flo[:,:]*major_on[:,:]*s_to_d*mmol_to_mol*g_to_kg*g_N
onn_old = np.nanmean(onn_flux[300+(12*1):300+(12*5),:],axis=0)
onn_new = np.nanmean(onn_flux[onn_flux.shape[0]-(12*5):,:],axis=0)
onn_perc = (onn_new-onn_old)/onn_old
print('onn_old',onn_old)
print('onn_new',onn_new)
print('reduction in onn fluxes 1997-2000, 2013-2017',onn_perc*100)

tnn_flux = major_flo[:,:]*major_tnn*s_to_d*mmol_to_mol*g_to_kg*g_N
tnn_old = np.nanmean(tnn_flux[300+(12*1):300+(12*5),:],axis=0)
tnn_new = np.nanmean(tnn_flux[tnn_flux.shape[0]-(12*5):,:],axis=0)
tnn_perc = (tnn_new-tnn_old)/tnn_old
print('tnn_old',tnn_old)
print('tnn_new',tnn_new)
print('reduction in tnn fluxes 1997-2000, 2013-2017',tnn_perc*100)
