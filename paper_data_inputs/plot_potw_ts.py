import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc'
fig_path = './figs/'

###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)


major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2']) # mmol/m3
major_on = np.array(major_nc.variables['ON']) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4']) # mmol/m3
major_op = np.array(major_nc.variables['OP']) # mmol/m3
major_fe  = np.array(major_nc.variables['Fe'])  # mmol/m3
major_pH  = np.array(major_nc.variables['pH']) 
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_salt = np.array(major_nc.variables['salinity']) 
major_toc = np.array(major_nc.variables['TOC']) 

major_tn = major_nh4+major_no3+major_no2+major_on
major_tp = major_po4+major_op

major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_toc[major_toc>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

# plotting major
figw = 10
#figw = 12
figh = 8
axis_tick_font = 14
axis_font = 14
major_names = ['HTP','JWPCP','OCSD','PLWTP']
major_linesty = ['-','--','-.',':']
lw = 3
plwtp_st = 170
iend_major = 506
savename_major = fig_path+'major_potw_ts.pdf'

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt[:iend_major],major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    if p_i == 3:   
        axes.flat[2].plot(major_time_dt[plwtp_st:iend_major],major_po4[plwtp_st:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    else:
        axes.flat[2].plot(major_time_dt[:iend_major],major_po4[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[0].set_ybound(lower=0)
    axes.flat[1].set_ybound(lower=0)
    axes.flat[2].set_ybound(lower=0)
    axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
    axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_font)
    axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_font)
    axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
    axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
    axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
    axes.flat[0].grid(True)
    axes.flat[1].grid(True)
    axes.flat[2].grid(True)
axes.flat[1].legend(loc='best')
fig.savefig(savename_major,bbox_inches='tight')

# include major fluxes
savename_major_flux = fig_path+'major_potw_ts_flux.pdf'
y_fmt = mtick.FormatStrFormatter('%1.E')

fig,axes = plt.subplots(5,1,sharex=True,figsize=[figw,figh+7])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt[:iend_major],major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    if p_i == 3:   
        axes.flat[2].plot(major_time_dt[plwtp_st:iend_major],major_po4[plwtp_st:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    else:
        axes.flat[2].plot(major_time_dt[:iend_major],major_po4[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[3].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[4].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_po4[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[3].set_ybound(lower=0)
axes.flat[4].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[2].set_ylabel('PO4\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[3].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[4].set_ylabel('PO4 Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[4].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')


# include TP flux with concentrations
savename_major_flux = fig_path+'major_potw_ts_flux_tp.pdf'
y_fmt = mtick.FormatStrFormatter('%1.E')

fig,axes = plt.subplots(5,1,sharex=True,figsize=[figw,figh+7])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt[:iend_major],major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    if p_i == 3:   
        axes.flat[2].plot(major_time_dt[plwtp_st:iend_major],major_tp[plwtp_st:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    else:
        axes.flat[2].plot(major_time_dt[:iend_major],major_tp[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[3].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[4].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_tp[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[3].set_ybound(lower=0)
axes.flat[4].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[3].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[4].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[4].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')

# fluxes only, including TOC
savename_major_flux = fig_path+'major_potw_ts_flux_only.pdf'

fig,axes = plt.subplots(4,1,sharex=True,figsize=[figw,figh+7])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_tn[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[2].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_tp[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[3].plot(major_time_dt[:iend_major],major_flo[:iend_major,p_i,p_i]*major_toc[:iend_major,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[3].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[3].set_ylabel('Total C Flux\n (organic) mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
#loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')

# major fluxes + all majors added up
savename_major_flux = fig_path+'major_potw_ts_sum_flux.pdf'

major_flo[major_flo>1E36]=np.nan
a = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])

major_potw_fluxalln = np.nansum(np.array(a),axis=0)

b = []
for m_i in range(major_flo.shape[1]):
    b.append(major_flo[:,m_i,m_i]*major_tp[:,m_i,m_i])

c = []
for m_i in range(major_flo.shape[1]):
    c.append(major_flo[:,m_i,m_i]*major_toc[:,m_i,m_i])

major_fluxalln = np.nansum(np.array(a),axis=0)
major_fluxallp = np.nansum(np.array(b),axis=0)
major_fluxallc = np.nansum(np.array(c),axis=0)

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[:iend_major-1],np.nansum(np.nansum(major_flo[:iend_major-1],axis=1),axis=1),linewidth=lw)
axes.flat[1].plot(major_time_dt[:iend_major-1],major_fluxalln[:iend_major-1],color='orange',linewidth=lw)
axes.flat[2].plot(major_time_dt[:iend_major-1],major_fluxallp[:iend_major-1],color='gray',linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
#axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')

savename_major_flux = fig_path+'major_potw_ts_sum_flux_toc.pdf'
fig,axes = plt.subplots(4,1,sharex=True,figsize=[figw,figh+7])
axes.flat[0].plot(major_time_dt[:iend_major-1],np.nansum(np.nansum(major_flo[:iend_major-1],axis=1),axis=1),linewidth=lw)
axes.flat[1].plot(major_time_dt[:iend_major-1],major_fluxalln[:iend_major-1],color='orange',linewidth=lw)
axes.flat[2].plot(major_time_dt[:iend_major-1],major_fluxallp[:iend_major-1],color='gray',linewidth=lw)
axes.flat[3].plot(major_time_dt[:iend_major-1],major_fluxallc[:iend_major-1],color='purple',linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[3].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[3].set_ylabel('Total C Flux\n (organic) mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
#axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')

savename_major_flux = fig_path+'major_potw_ts_sum_flux_nobound.pdf'
y_fmt = mtick.FormatStrFormatter('%1.E')

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw+1,figh])
axes.flat[0].plot(major_time_dt[:iend_major-1],np.nansum(np.nansum(major_flo[:iend_major-1],axis=1),axis=1),linewidth=lw)
axes.flat[1].plot(major_time_dt[:iend_major-1],major_fluxalln[:iend_major-1],color='orange',linewidth=lw)
axes.flat[2].plot(major_time_dt[:iend_major-1],major_fluxallp[:iend_major-1],color='gray',linewidth=lw)
#axes.flat[0].set_ybound(lower=0)
#axes.flat[1].set_ybound(lower=0)
#axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
#axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')


#start in 1980s
st_in = 200
savename_major_flux = fig_path+'major_potw_ts_sum_flux_shorter.pdf'
y_fmt = mtick.FormatStrFormatter('%1.E')

major_flo[major_flo>1E36]=np.nan
a = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])

major_potw_fluxalln = np.nansum(np.array(a),axis=0)

b = []
for m_i in range(major_flo.shape[1]):
    b.append(major_flo[:,m_i,m_i]*major_tp[:,m_i,m_i])

major_fluxalln = np.nansum(np.array(a),axis=0)
major_fluxallp = np.nansum(np.array(b),axis=0)

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[st_in:iend_major-1],np.nansum(np.nansum(major_flo[st_in:iend_major-1],axis=1),axis=1),linewidth=lw)
axes.flat[1].plot(major_time_dt[st_in:iend_major-1],major_fluxalln[st_in:iend_major-1],color='orange',linewidth=lw)
axes.flat[2].plot(major_time_dt[st_in:iend_major-1],major_fluxallp[st_in:iend_major-1],color='gray',linewidth=lw)
#axes.flat[0].set_ybound(lower=0)
#axes.flat[1].set_ybound(lower=0)
#axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=[1.,1],handlelength=3)
#axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
loc = mtick.MultipleLocator(base=50000) 
#axes.flat[3].yaxis.set_major_locator(loc)
fig.savefig(savename_major_flux,bbox_inches='tight')
'''

###############
# minor data
###############
minor_nc = Dataset(minor_path,'r')

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time_dt = np.array(minor_time_l)


minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['NH4']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['NO3']) # mmol/m3
minor_no2 = np.array(minor_nc.variables['NO2']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['PO4']) # mmol/m3

minor_tn = minor_no3+minor_nh4+minor_no2

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan
minor_allf = np.nansum(np.nansum(minor_flo,axis=1),axis=1)
minor_alln = np.nansum(np.nansum(minor_tn,axis=1),axis=1)
minor_allp = np.nansum(np.nansum(minor_po4,axis=1),axis=1)

iend_minor = 12 # monthly climatology
mon_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']

# cumulative minors
savename_minor_sum = fig_path+'minor_potw_ts_sum.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(mon_name,minor_allf[:iend_minor],linewidth=lw)
axes.flat[1].plot(mon_name,minor_alln[:iend_minor],linewidth=lw)
axes.flat[2].plot(mon_name,minor_allp[:iend_minor],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_minor_sum,bbox_inches='tight')

# individual minors
savename_minor_sum = fig_path+'minor_potw_ts_ind.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for m_i in range(minor_flo.shape[1]):
    axes.flat[0].plot(mon_name,minor_flo[:iend_minor,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(mon_name,minor_tn[:iend_minor,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(mon_name,minor_po4[:iend_minor,m_i,m_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('PO4 mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_minor_sum,bbox_inches='tight')

# individual minors flux
savename_minor_fluxsum = fig_path+'minor_potw_ts_fluxind.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for m_i in range(minor_flo.shape[1]):
    axes.flat[0].plot(mon_name,minor_flo[:iend_minor,m_i,m_i],linewidth=lw)
    axes.flat[1].plot(mon_name,minor_tn[:iend_minor,m_i,m_i],linewidth=lw)
    axes.flat[2].plot(mon_name,minor_flo[:iend_minor,m_i,m_i]*minor_tn[:iend_minor,m_i,m_i],linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
#axes.flat[2].legend(loc='best')
fig.savefig(savename_minor_fluxsum,bbox_inches='tight')

# major vs minor monthly clim
minor_lsty = (0, (3, 1, 1, 1, 1, 1))
months = 12
mon_l = range(1,13)

savename_both = fig_path+'potw_flux_compare.pdf'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    major_clim_flo_l = []
    major_clim_tn_l = []
    for m_i in range(1,months+1): # skip first value start at Jan
        major_clim_flo_l.append(np.nanmean(major_flo[m_i::months,p_i,p_i]))
        major_clim_tn_l.append(np.nanmean(major_tn[m_i::months,p_i,p_i]))
    major_clim_flo = np.array(major_clim_flo_l)
    major_clim_tn = np.array(major_clim_tn_l)
    axes.flat[0].plot(mon_name,major_clim_flo,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(mon_name,major_clim_tn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[2].plot(mon_name,major_clim_flo*major_clim_tn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)

axes.flat[0].plot(mon_name,minor_allf[:iend_minor],linestyle=minor_lsty,label='Minor POTW',linewidth=lw)
axes.flat[1].plot(mon_name,minor_alln[:iend_minor],linestyle=minor_lsty,label='Minor POTW',linewidth=lw)
a = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[:iend_minor,m_i,m_i]*minor_tn[:iend_minor,m_i,m_i])
minor_fluxalln = np.nansum(np.array(a),axis=0)
axes.flat[2].plot(mon_name,minor_fluxalln,linestyle=minor_lsty,linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_tick_font)
axes.flat[2].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='minor',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[1].legend(loc='best')
fig.savefig(savename_both,bbox_inches='tight')

# compare without N concentration
savename_both = fig_path+'potw_flux_compare_noconc.pdf'
fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    major_clim_flo_l = []
    major_clim_tn_l = []
    for m_i in range(1,months+1): # skip first value start at Jan
        major_clim_flo_l.append(np.nanmean(major_flo[m_i::months,p_i,p_i]))
        major_clim_tn_l.append(np.nanmean(major_tn[m_i::months,p_i,p_i]))
    major_clim_flo = np.array(major_clim_flo_l)
    major_clim_tn = np.array(major_clim_tn_l)
    axes.flat[0].plot(mon_name,major_clim_flo,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(mon_name,major_clim_flo*major_clim_tn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)

axes.flat[0].plot(mon_name,minor_allf[:iend_minor],linestyle=minor_lsty,label='14 Minor POTWs',linewidth=lw)
a = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[:iend_minor,m_i,m_i]*minor_tn[:iend_minor,m_i,m_i])

minor_fluxalln = np.nansum(np.array(a),axis=0)
axes.flat[1].plot(mon_name,minor_fluxalln,linestyle=minor_lsty,linewidth=lw)
axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_tick_font)
axes.flat[1].set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_tick_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=5,mode='expand',borderaxespad=0.,handlelength=2.2)
#axes.flat[0].legend(loc='best',fontsize=axis_tick_font,bbox_to_anchor=(1,.8),handlelength=3.5)
fig.savefig(savename_both,bbox_inches='tight')


# major POTW monthly clim conc and fluxes
savename_major_clim = fig_path+'major_potw_clim.pdf'
fig,axes = plt.subplots(5,1,sharex=True,figsize=[figw,figh+7])
for p_i in range(len(major_names)):
    major_clim_flo_l = []
    major_clim_tn_l = []
    major_clim_p_l = []
    major_clim_test = []
    for m_i in range(1,months+1): # skip first value start at Jan
        major_clim_flo_l.append(np.nanmean(major_flo[m_i::months,p_i,p_i]))
        major_clim_tn_l.append(np.nanmean(major_tn[m_i::months,p_i,p_i]))
        major_clim_p_l.append(np.nanmean(major_po4[m_i::months,p_i,p_i]))
#        major_clim_test.append(np.nanmean(major_flo[m_i::months,p_i,p_i]*major_tn[m_i::months,p_i,p_i]))
    major_clim_flo = np.array(major_clim_flo_l)
    major_clim_tn = np.array(major_clim_tn_l)
    major_clim_p = np.array(major_clim_p_l)
    axes.flat[0].plot(mon_name,major_clim_flo,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[1].plot(mon_name,major_clim_tn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[2].plot(mon_name,major_clim_p,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[3].plot(mon_name,major_clim_flo*major_clim_tn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
    axes.flat[4].plot(mon_name,major_clim_flo*major_clim_p,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw)
#    axes.flat[3].plot(mon_name,major_clim_test,linestyle=':',label='flux then clim',linewidth=0.5)

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[3].set_ybound(lower=0)
axes.flat[4].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux\n m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[2].set_ylabel('PO4\n mmol m$^{-3}$',fontsize=axis_font)
axes.flat[3].set_ylabel('Total N Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[4].set_ylabel('PO4 Flux\n mmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[3].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[4].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major_clim,bbox_inches='tight')
'''
