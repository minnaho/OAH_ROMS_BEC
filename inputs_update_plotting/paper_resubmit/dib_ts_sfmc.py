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
import PIL

fig_path = './figs/'
# data paths
river_path = '/data/project1/minnaho/potw_central_coast/River_data_full.xlsx'
potw_path = '/data/project1/minnaho/potw_central_coast/POTW_data_full.xlsx'

log_set = True

# convert to kg/month, then sum
s_to_d = 86400
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14
g_P = 30.97


###############
# river data (5 yrs) 2010-2015
###############
'''
rxl = pd.ExcelFile(river_path)
rsn = rxl.sheet_names

rs=pd.read_excel(river_path,sheet_name=rsn[1],skiprows=2,header=None)

rflo = np.empty((len(rsn[1:]),len(rs)))*np.nan
rnh4 = np.empty((len(rsn[1:]),len(rs)))*np.nan
rno3 = np.empty((len(rsn[1:]),len(rs)))*np.nan
rdon = np.empty((len(rsn[1:]),len(rs)))*np.nan
rn2  = np.empty((len(rsn[1:]),len(rs)))*np.nan
rno2 = np.empty((len(rsn[1:]),len(rs)))*np.nan
rn2o = np.empty((len(rsn[1:]),len(rs)))*np.nan
rpo4 = np.empty((len(rsn[1:]),len(rs)))*np.nan
rdop = np.empty((len(rsn[1:]),len(rs)))*np.nan

for s_i in range(1,len(rsn)):
    print('reading '+rsn[s_i])
    riv = pd.read_excel(river_path,sheet_name=rsn[s_i],skiprows=2,header=None)
    if s_i == 1:
        rtim = pd.to_datetime(riv[0])
    rflo[s_i-1,:] = riv[3]
    rnh4[s_i-1,:] = riv[9]
    rno3[s_i-1,:] = riv[7]
    rdon[s_i-1,:] = riv[27]
    rn2[s_i-1,:]  = riv[32]
    rno2[s_i-1,:] = riv[30]
    rn2o[s_i-1,:] = riv[31]
    rpo4[s_i-1,:] = riv[6]
    rdop[s_i-1,:] = riv[29]

river_no3 = rno3*(g_N/62)
river_nh4 = rnh4*(g_N/18)
river_no2 = rno2*(g_N/46)
river_n2o = rn2o*((g_N*2)/44)

river_po4 = rpo4*(g_P/(g_P+(16*4)))

river_tnn = river_no3+river_nh4+river_no2+river_n2o+rn2+rdon
river_tpp = river_po4+rdop

river_flo = rflo

river_time_dt = rtim

np.save('sfmc_riv_tnn.npy',river_tnn)
np.save('sfmc_riv_tpp.npy',river_tpp)
np.save('sfmc_riv_flo.npy',river_flo)
np.save('sfmc_riv_dt.npy',rtim)
'''
river_tnn = np.load('sfmc_riv_tnn.npy')
river_tpp = np.load('sfmc_riv_tpp.npy')
river_flo = np.load('sfmc_riv_flo.npy')
river_time_dt = np.load('sfmc_riv_dt.npy')

######################
# potw
######################
'''
pxl = pd.ExcelFile(potw_path)
psn = pxl.sheet_names

ps=pd.read_excel(potw_path,sheet_name=psn[1],skiprows=2,header=None)

pflo = np.empty((len(psn[1:]),len(ps)))*np.nan
pnh4 = np.empty((len(psn[1:]),len(ps)))*np.nan
pno3 = np.empty((len(psn[1:]),len(ps)))*np.nan
pdon = np.empty((len(psn[1:]),len(ps)))*np.nan
pn2  = np.empty((len(psn[1:]),len(ps)))*np.nan
pno2 = np.empty((len(psn[1:]),len(ps)))*np.nan
pn2o = np.empty((len(psn[1:]),len(ps)))*np.nan
ppo4 = np.empty((len(psn[1:]),len(ps)))*np.nan
pdop = np.empty((len(psn[1:]),len(ps)))*np.nan


for s_n in range(1,len(psn)):
    print('reading '+psn[s_n])
    potw = pd.read_excel(potw_path,sheet_name=psn[s_n],skiprows=2,header=None)
    if s_n == 1:
        ptim = pd.to_datetime(potw[0])
    pflo[s_n-1,:] = potw[3-2]
    pnh4[s_n-1,:] = potw[9-2]
    pno3[s_n-1,:] = potw[7-2]
    pdon[s_n-1,:] = potw[27-2]
    pn2[s_n-1,:]  = potw[32-2]
    pno2[s_n-1,:] = potw[30-2]
    pn2o[s_n-1,:] = potw[31-2]
    ppo4[s_n-1,:] = potw[6-2]
    pdop[s_n-1,:] = potw[29-2]

potw_no3 = pno3*(g_N/62)
potw_nh4 = pnh4*(g_N/18)
potw_no2 = pno2*(g_N/46)
potw_n2o = pn2o*((g_N*2)/44)

potw_po4 = ppo4*(g_P/(g_P+(16*4)))

major_tnn = potw_no3+potw_nh4+potw_no2+potw_n2o+pn2+pdon
major_tpp = potw_po4+pdop

major_flo = pflo

np.save('sfmc_potw_tnn.npy',major_tnn)
np.save('sfmc_potw_tpp.npy',major_tpp)
np.save('sfmc_potw_flo.npy',major_flo)
np.save('sfmc_potw_dt.npy',ptim)

potw_time_dt = ptim
'''

major_tnn = np.load('sfmc_potw_tnn.npy')
major_tpp = np.load('sfmc_potw_tpp.npy')
major_flo = np.load('sfmc_potw_flo.npy')
potw_time_dt = np.load('sfmc_potw_dt.npy')

#############
# sum flows
#############

river_fflux = np.nansum(river_flo,axis=0)
river_nflux = np.nansum(river_flo*river_tnn*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=0)
river_pflux = np.nansum(river_flo*river_tpp*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=0)

major_fflux = np.nansum(major_flo,axis=0)
major_nflux = np.nansum(major_flo*major_tnn*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=0)
major_pflux = np.nansum(major_flo*major_tpp*s_to_d*g_N*g_to_kg*mmol_to_mol,axis=0)

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

#plt.ion()
fig = plt.figure(figsize=[figw,figh])
gs = GridSpec(9,1) 

ax1 = fig.add_subplot(gs[0:2,:])
ax2 = fig.add_subplot(gs[2,:])
ax3 = fig.add_subplot(gs[3:5,:])
ax4 = fig.add_subplot(gs[5,:])
ax5 = fig.add_subplot(gs[6:8,:])
ax6 = fig.add_subplot(gs[8,:])

ax1.plot(river_time_dt,river_fflux,color=rcol,linestyle=rsty,label='River')
ax1.plot(potw_time_dt,major_fflux,color=pcol,linestyle=psty,label='POTW')

ax2.plot(potw_time_dt,major_fflux,color=pcol,linestyle=psty,label='POTW',zorder=2)
ylim0_2 = 0
ylim1_2 = ax2.get_ylim()[1]
ax2.plot(river_time_dt,river_fflux,color=rcol,linestyle=rsty,label='River',zorder=1)
ax2.set_ylim([ylim0_2,ylim1_2])

ax3.plot(river_time_dt,river_nflux,color=rcol,linestyle=rsty,label='River')
ax3.plot(potw_time_dt,major_nflux,color=pcol,linestyle=psty,label='POTW')

ax4.plot(potw_time_dt,major_nflux,color=pcol,linestyle=psty,label='POTW',zorder=2)
#ylim0_4 = ax4.get_ylim()[0]
ylim0_4 = 0
ylim1_4 = ax4.get_ylim()[1]
ax4.plot(river_time_dt,river_nflux,color=rcol,linestyle=rsty,label='River',zorder=1)
ax4.set_ylim([ylim0_4,ylim1_4])

ax5.plot(river_time_dt,river_pflux,color=rcol,linestyle=rsty,label='River')
ax5.plot(potw_time_dt,major_pflux,color=pcol,linestyle=psty,label='POTW')

ax6.plot(potw_time_dt,major_pflux,color=pcol,linestyle=psty,label='POTW',zorder=2)
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

ax1.text(datetime.datetime(2008,11,1),np.nanmax(river_fflux),'Volume Flux m$^3$ s$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')
ax3.text(datetime.datetime(2008,11,1),np.nanmax(river_nflux),'TN Flux kg d$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')
ax5.text(datetime.datetime(2008,11,1),np.nanmax(river_pflux),'TP Flux kg d$^{-1}$',rotation=90,fontsize=axis_font,verticalalignment='top')

ax1.text(datetime.datetime(2009,9,10),np.nanmax(river_fflux)+130,'a)',fontsize=axis_font)
ax2.text(datetime.datetime(2009,9,10),3.1,'b)',fontsize=axis_font)
ax3.text(datetime.datetime(2009,9,10),np.nanmax(river_nflux)+15000,'c)',fontsize=axis_font)
ax4.text(datetime.datetime(2009,9,10),9300,'d)',fontsize=axis_font)
ax5.text(datetime.datetime(2009,9,10),5050,'e)',fontsize=axis_font)
ax6.text(datetime.datetime(2009,9,10),207,'f)',fontsize=axis_font)


fig.subplots_adjust(hspace=0.3)

ax1.legend(loc='best',fontsize=axis_font-1)
fig.savefig('figs/dib_ts_sfmc.pdf',bbox_inches='tight')


