import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import pandas as pd

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/major_potw_data_newocsd.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/minor_potw_data.nc'
maj_newp = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data_2013_2017.nc'
fig_path = './figs/'



###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')
major_nc_2013 = Dataset(maj_newp,'r')

major_time_dt = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

major_time_dt_2013 = num2date(np.array(major_nc_2013.variables['time']),major_nc_2013.variables['time'].units,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

ind_1997 = 313
ind_2010 = 481

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
major_toc = np.array(major_nc.variables['TOC']) 


major_nh4[major_nh4>1E20] = np.nan 
major_no3[major_no3>1E20] = np.nan 
major_no2[major_no2>1E20] = np.nan 
major_on[major_on>1E20] = np.nan 
major_op[major_op>1E20] = np.nan 

major_tn = np.nansum((major_nh4,major_no3,major_no2,major_on),axis=0)
major_tp = major_po4+major_op

major_tn[major_tn>1E20] = np.nan
major_tp[major_tp>1E20] = np.nan
major_toc[major_toc>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

major_din = np.nansum((major_nh4,major_no3,major_no2),axis=0)


new_major_flo = np.array(major_nc_2013.variables['flow']) # m3/s
new_major_nh4 = np.array(major_nc_2013.variables['NH4']) # mmol/m3
new_major_no3 = np.array(major_nc_2013.variables['NO3']) # mmol/m3
new_major_no2 = np.array(major_nc_2013.variables['NO2']) # mmol/m3
new_major_ton = np.array(major_nc_2013.variables['TON']) # mmol/m3
new_major_tp = np.array(major_nc_2013.variables['total_phosphorus']) # mmol/m3
new_major_pH  = np.array(major_nc_2013.variables['pH']) 
new_major_toc = np.array(major_nc_2013.variables['TOC']) 

new_major_nh4[new_major_nh4>1E20] = np.nan 
new_major_no3[new_major_no3>1E20] = np.nan 
new_major_no2[new_major_no2>1E20] = np.nan 
new_major_ton[new_major_ton>1E20] = np.nan 

new_major_tp[new_major_tp>1E20] = np.nan
new_major_toc[new_major_toc>1E20] = np.nan

new_major_tn = np.nansum((new_major_nh4,new_major_no3,new_major_no2,new_major_ton),axis=0)
new_major_din = np.nansum((new_major_nh4,new_major_no3,new_major_no2),axis=0)

new_major_tn[new_major_tn>1E20] = np.nan

kg_to_g = 1000
g_to_mol = 1./14
mol_to_mmol = 1000
mgL_to_mmolm3 = 1000./14

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
savename_major = fig_path+'major_potw_ts_19972010_20132017.png'
col_p = ['blue','orange','green','red']

# conversion
convn = 14./1000 # mmol/m3 to mg/L
convp = 30.97/1000 # mmol/m3 to kg/L
convnf = (14.*86400)/1E6 # mmol/s to kg/d
convpf = (30.97*86400)/1E6 # mmol/s to kg/d
convv = 1./0.043812645072430365 # m3/s to mgd

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_tn[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_tp[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt_2013,new_major_tn[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt_2013,new_major_tp[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N mmol m$^{-3}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P mmol m$^{-3}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

# include major fluxes
savename_major_flux = fig_path+'major_potw_ts_flux_19972010_20132017.png'

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_tn[ind_1997:ind_2010,p_i,p_i]*major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_tp[ind_1997:ind_2010,p_i,p_i]*major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt_2013,new_major_tn[:,p_i,p_i]*new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt_2013,new_major_tp[:,p_i,p_i]*new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\nmmol s$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\nmmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major_flux,bbox_inches='tight')

# ocsd only
savename_major = fig_path+'ocsd_ts_19972010_20132017.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_tn[ind_1997:ind_2010,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_tp[ind_1997:ind_2010,2,2]*convp,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,2,2]*convv,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt_2013,new_major_tn[:,2,2]*convn,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt_2013,new_major_tp[:,2,2]*convp,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N mg L$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P mg L$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

# include major fluxes
savename_major_flux = fig_path+'ocsd_ts_flux_19972010_20132017.png'

fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_tn[ind_1997:ind_2010,2,2]*major_flo[ind_1997:ind_2010,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_tp[ind_1997:ind_2010,2,2]*major_flo[ind_1997:ind_2010,2,2]*convpf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,2,2]*convv,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt_2013,new_major_tn[:,2,2]*new_major_flo[:,2,2]*convnf,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt_2013,new_major_tp[:,2,2]*new_major_flo[:,2,2]*convpf,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('Total N Flux\nkg d$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('Total P Flux\nkg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major_flux,bbox_inches='tight')

###########
# ammonium only
##############
# all potw concentrations
savename_major = fig_path+'major_potw_ts_nh4_19972010_20132017.png'

fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_nh4[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt_2013,new_major_nh4[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('NH4 mmol m$^{-3}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

# include major fluxes
savename_major_flux = fig_path+'major_potw_ts_nh4_flux_19972010_20132017.png'

fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_nh4[ind_1997:ind_2010,p_i,p_i]*major_flo[ind_1997:ind_2010,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt_2013,new_major_nh4[:,p_i,p_i]*new_major_flo[:,p_i,p_i],linestyle=major_linesty[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('NH4 Flux\nmmol s$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major_flux,bbox_inches='tight')

# ocsd only
savename_major = fig_path+'ocsd_ts_nh4_19972010_20132017.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_nh4[ind_1997:ind_2010,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_nh4[ind_1997:ind_2010,2,2]*major_flo[ind_1997:ind_2010,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,2,2]*convv,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt_2013,new_major_nh4[:,2,2]*convn,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt_2013,new_major_nh4[:,2,2]*new_major_flo[:,2,2]*convnf,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('NH4 mg L$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('NH4 Flux kg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

#########
# DIN only 
########
# ocsd only
savename_major = fig_path+'ocsd_ts_din_19972010_20132017.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[ind_1997:ind_2010],major_flo[ind_1997:ind_2010,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2010],major_din[ind_1997:ind_2010,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2010],major_din[ind_1997:ind_2010,2,2]*major_flo[ind_1997:ind_2010,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(major_time_dt_2013,new_major_flo[:,2,2]*convv,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt_2013,new_major_din[:,2,2]*convn,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt_2013,new_major_din[:,2,2]*new_major_flo[:,2,2]*convnf,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('DIN mg L$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('DIN Flux kg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

