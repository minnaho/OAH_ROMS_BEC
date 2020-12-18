# data in brief time series
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pandas as pd

fig_path = './figs/'
# data paths
river_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_daily.nc'
potw_major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017.nc'

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

river_time_dt = num2date(np.array(river_nc.variables['time']),river_nc.variables['time'].units,only_use_cftime_datetimes=False)

## convert real_datetime to datetime
#river_time_l = []
#for d_i in range(len(river_time)):
#    river_time_l.append(river_time[d_i]+datetime.timedelta(0,1))

#river_time_dt = np.array(river_time_l)
#river_time_dt = np.array(river_time_l)

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
river_tnn = np.array(river_nc.variables['total_N']) 
river_tpp = np.array(river_nc.variables['total_P']) 
river_toc = np.array(river_nc.variables['total_organic_C']) 

river_din = np.nansum((river_nh4,river_no3),axis=0)

######################
# potw
######################
potw_ma_nc = Dataset(potw_major_path,'r')

major_potw_time = num2date(np.array(potw_ma_nc.variables['time']),potw_ma_nc.variables['time'].units,only_use_cftime_datetimes=False)
# start and end indices of potw for 1997-2010
potw_1997 = 9497 # 1997-01-01
potw_2013 = major_potw_time.shape[0] # 2017-01-01

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_all = np.array(major_potw_time[:])

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

# divide flows
major_flo = np.array(potw_ma_nc.variables['flow']) # m3/s
major_nh4 = np.array(potw_ma_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(potw_ma_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(potw_ma_nc.variables['NO2']) # mmol/m3
major_onn  = np.array(potw_ma_nc.variables['organic_N']) # mmol/m3
major_tnn  = np.array(potw_ma_nc.variables['total_N']) # mmol/m3
major_tpp  = np.array(potw_ma_nc.variables['total_P']) # mmol/m3
major_po4 = np.array(potw_ma_nc.variables['PO4']) # mmol/m3
major_opp  = np.array(potw_ma_nc.variables['organic_P']) # mmol/m3
major_fee  = np.array(potw_ma_nc.variables['total_Fe'])  # mmol/m3
major_phh  = np.array(potw_ma_nc.variables['pH'])
major_alk = np.array(potw_ma_nc.variables['alkalinity'])
major_tem = np.array(potw_ma_nc.variables['temperature'])
major_sal = np.array(potw_ma_nc.variables['salinity'])
major_toc  = np.array(potw_ma_nc.variables['total_organic_C'])

major_flo = major_flo[potw_1997:potw_2013]
major_tnn = major_tnn[potw_1997:potw_2013]
major_tpp = major_tpp[potw_1997:potw_2013]
major_toc = major_toc[potw_1997:potw_2013]

major_din = major_nh4[potw_1997:potw_2013]+major_no3[potw_1997:potw_2013]+major_no2[potw_1997:potw_2013]

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
minor_tnn = np.array(potw_mi_nc.variables['total_N']) # mmol/m3
minor_tpp = np.array(potw_mi_nc.variables['total_P']) # mmol/m3
minor_toc = np.array(potw_mi_nc.variables['total_organic_C']) # mmol/m3

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

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14
g_P = 30.97

river_fflux = np.nansum(river_flo,axis=1)
river_nflux = np.nansum(river_flo*river_tnn*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
river_pflux = np.nansum(river_flo*river_tpp*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
river_cflux = np.nansum(river_flo*river_toc*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)

major_fflux = np.nansum(major_flo,axis=1)
major_nflux = np.nansum(major_flo*major_tnn*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
major_pflux = np.nansum(major_flo*major_tpp*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
major_cflux = np.nansum(major_flo*major_toc*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)

minor_fflux = np.nansum(minor_flo,axis=1)
minor_nflux = np.nansum(minor_flo*minor_tnn*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
minor_pflux = np.nansum(minor_flo*minor_tpp*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
minor_cflux = np.nansum(minor_flo*minor_toc*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)

# plot
figw = 12
figh = 14
axis_font = 16

rcol = 'lightblue'
pcol = 'orange'
mcol = 'black'

rsty = '-'
psty = '--'
msty = ':'

plt.ion()
'''
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(river_time_dt,river_fflux,color=rcol,linestyle=rsty,label='River')
axes.flat[0].plot(river_time_dt,major_fflux,color=pcol,linestyle=psty,label='Major POTW')
axes.flat[0].plot(river_time_dt,minor_fflux,color=mcol,linestyle=msty,label='Minor POTW')

axes.flat[1].plot(river_time_dt,river_nflux,color=rcol,linestyle=rsty,label='River')
axes.flat[1].plot(river_time_dt,major_nflux,color=pcol,linestyle=psty,label='Major POTW')
axes.flat[1].plot(river_time_dt,minor_nflux,color=mcol,linestyle=msty,label='Minor POTW')

axes.flat[2].plot(river_time_dt,river_pflux,color=rcol,linestyle=rsty,label='River')
axes.flat[2].plot(river_time_dt,major_pflux,color=pcol,linestyle=psty,label='Major POTW')
axes.flat[2].plot(river_time_dt,minor_pflux,color=mcol,linestyle=msty,label='Minor POTW')

axes.flat[0].yaxis.set_ticks_position('both')
axes.flat[1].yaxis.set_ticks_position('both')
axes.flat[2].yaxis.set_ticks_position('both')

axes.flat[0].xaxis.set_ticks_position('both')
axes.flat[1].xaxis.set_ticks_position('both')
axes.flat[2].xaxis.set_ticks_position('both')

axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_font)

axes.flat[0].legend(loc='best')
'''

fig = plt.figure(figsize=[figw,figh])
gs = GridSpec(9,1) 

ax1 = fig.add_subplot(gs[0:2,:])
ax2 = fig.add_subplot(gs[2,:])
ax3 = fig.add_subplot(gs[3:5,:])
ax4 = fig.add_subplot(gs[5,:])
ax5 = fig.add_subplot(gs[6:8,:])
ax6 = fig.add_subplot(gs[8,:])

ax1.plot(river_time_dt,river_fflux,color=rcol,linestyle=rsty,label='River')
ax1.plot(river_time_dt,major_fflux,color=pcol,linestyle=psty,label='Major POTW')
ax1.plot(river_time_dt,minor_fflux,color=mcol,linestyle=msty,label='Minor POTW')

ax2.plot(river_time_dt,major_fflux,color=pcol,linestyle=psty,label='Major POTW',zorder=2)
ax2.plot(river_time_dt,minor_fflux,color=mcol,linestyle=msty,label='Minor POTW',zorder=3)
#ylim0_2 = ax2.get_ylim()[0]
ylim0_2 = 0
ylim1_2 = ax2.get_ylim()[1]
ax2.plot(river_time_dt,river_fflux,color=rcol,linestyle=rsty,label='River',zorder=1)
ax2.set_ylim([ylim0_2,ylim1_2])

ax3.plot(river_time_dt,river_nflux,color=rcol,linestyle=rsty,label='River')
ax3.plot(river_time_dt,major_nflux,color=pcol,linestyle=psty,label='Major POTW')
ax3.plot(river_time_dt,minor_nflux,color=mcol,linestyle=msty,label='Minor POTW')

ax4.plot(river_time_dt,major_nflux,color=pcol,linestyle=psty,label='Major POTW',zorder=2)
ax4.plot(river_time_dt,minor_nflux,color=mcol,linestyle=msty,label='Minor POTW',zorder=3)
#ylim0_4 = ax4.get_ylim()[0]
ylim0_4 = 0
ylim1_4 = ax4.get_ylim()[1]
ax4.plot(river_time_dt,river_nflux,color=rcol,linestyle=rsty,label='River',zorder=1)
ax4.set_ylim([ylim0_4,ylim1_4])

ax5.plot(river_time_dt,river_pflux,color=rcol,linestyle=rsty,label='River')
ax5.plot(river_time_dt,major_pflux,color=pcol,linestyle=psty,label='Major POTW')
ax5.plot(river_time_dt,minor_pflux,color=mcol,linestyle=msty,label='Minor POTW')

ax6.plot(river_time_dt,major_pflux,color=pcol,linestyle=psty,label='Major POTW',zorder=2)
ax6.plot(river_time_dt,minor_pflux,color=mcol,linestyle=msty,label='Minor POTW',zorder=3)
#ylim0_6 = ax6.get_ylim()[0]
ylim0_6 = 0
ylim1_6 = ax6.get_ylim()[1]
ax6.plot(river_time_dt,river_pflux,color=rcol,linestyle=rsty,label='River',zorder=1)
ax6.set_ylim([ylim0_6,ylim1_6])

ax1.axes.xaxis.set_ticklabels([])
ax2.axes.xaxis.set_ticklabels([])
ax3.axes.xaxis.set_ticklabels([])
ax4.axes.xaxis.set_ticklabels([])
ax5.axes.xaxis.set_ticklabels([])

ax1.xaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
ax3.xaxis.set_ticks_position('both')
ax4.xaxis.set_ticks_position('both')
ax5.xaxis.set_ticks_position('both')
ax6.xaxis.set_ticks_position('both')

ax1.yaxis.set_ticks_position('both')
ax2.yaxis.set_ticks_position('both')
ax3.yaxis.set_ticks_position('both')
ax4.yaxis.set_ticks_position('both')
ax5.yaxis.set_ticks_position('both')
ax6.yaxis.set_ticks_position('both')

ax1.tick_params(axis='both',which='major',labelsize=axis_font)
ax2.tick_params(axis='both',which='major',labelsize=axis_font)
ax3.tick_params(axis='both',which='major',labelsize=axis_font)
ax4.tick_params(axis='both',which='major',labelsize=axis_font)
ax5.tick_params(axis='both',which='major',labelsize=axis_font)
ax6.tick_params(axis='both',which='major',labelsize=axis_font)

#ax1.text(datetime.datetime(1992,4,1),np.nanmax(river_fflux),'Volume Flux\n    m$^3$ s$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')
#ax2.text(datetime.datetime(1992,7,1),np.nanmin(minor_fflux),'Volume Flux m$^3$ s$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='bottom')
ax1.text(datetime.datetime(1992,7,1),np.nanmax(river_fflux),'Volume Flux m$^3$ s$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')
ax3.text(datetime.datetime(1992,7,1),np.nanmax(river_nflux),'TN Flux kg d$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')
ax5.text(datetime.datetime(1992,7,1),np.nanmax(river_pflux),'TP Flux kg d$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')

ax1.yaxis.set_major_locator(mtick.MultipleLocator(.5E3))
ax2.yaxis.set_major_locator(mtick.MultipleLocator(2.5E1))
ax3.yaxis.set_major_locator(mtick.MultipleLocator(1.25E5))
ax4.yaxis.set_major_locator(mtick.MultipleLocator(.75E5))
ax5.yaxis.set_major_locator(mtick.MultipleLocator(2E4))
ax6.yaxis.set_major_locator(mtick.MultipleLocator(4E3))

class MathTextSciFormatter(mtick.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt
    def __call__(self, x, pos=None):
        s = self.fmt % x
        decimal_point = '.'
        positive_sign = '+'
        tup = s.split('e')
        significand = tup[0].rstrip(decimal_point)
        sign = tup[1][0].replace(positive_sign, '')
        exponent = tup[1][1:].lstrip('0')
        if exponent:
            exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s =  r'%s{\times}%s' % (significand, exponent)
        else:
            s =  r'%s%s' % (significand, exponent)
        return "${}$".format(s)

# Format with 2 decimal places
ax1.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax2.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax3.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax4.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax5.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))
ax6.yaxis.set_major_formatter(MathTextSciFormatter("%1.1e"))

ax1.text(datetime.datetime(1996,2,1),2.8E3,'a)',fontsize=axis_font)
ax2.text(datetime.datetime(1996,2,1),63,'b)',fontsize=axis_font)
ax3.text(datetime.datetime(1996,2,1),6.8E5,'c)',fontsize=axis_font)
ax4.text(datetime.datetime(1996,2,1),2.07E5,'d)',fontsize=axis_font)
ax5.text(datetime.datetime(1996,2,1),7.9E4,'e)',fontsize=axis_font)
ax6.text(datetime.datetime(1996,2,1),1.04E4,'f)',fontsize=axis_font)


fig.subplots_adjust(hspace=0.3)

ax1.legend(loc='best',fontsize=axis_font-1)
fig.savefig('figs/dib_ts.pdf',bbox_inches='tight')


# TN of just major POTWs
major_flo_all = np.array(potw_ma_nc.variables['flow']) # m3/s
major_tnn_all  = np.array(potw_ma_nc.variables['total_N']) # mmol/m3
major_nflux_all = np.nansum(major_flo_all*major_tnn_all*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)
major_nflux_each = major_flo_all*major_tnn_all*s_to_d*g_N*g_to_kg*mmol_to_mol

plt.figure()
plt.plot(major_potw_time_all,major_nflux_all)


plt.figure()
plt.plot(major_potw_time_all,major_nflux_each[:,0],label='HTP')
plt.plot(major_potw_time_all,major_nflux_each[:,1],label='JWPCP')
plt.plot(major_potw_time_all,major_nflux_each[:,2],label='OCSD')
plt.plot(major_potw_time_all,major_nflux_each[:,3],label='PLWTP')

# N all sources Jan 1997-Dec 1999
dec1999 = 1095
din_90s = np.nanmean(np.nansum(major_din[:dec1999]*major_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)+np.nansum(river_din[:dec1999]*river_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)+np.nansum(minor_tnn[:dec1999]*minor_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1))
tnn_90s = np.nanmean(np.nansum(major_tnn[:dec1999]*major_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)+np.nansum(river_tnn[:dec1999]*river_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1)+np.nansum(minor_tnn[:dec1999]*minor_flo[:dec1999]*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=1))

# DIN early 1970s
