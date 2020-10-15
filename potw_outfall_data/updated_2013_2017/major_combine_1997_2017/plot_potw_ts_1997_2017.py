import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import pandas as pd
import glob as glob

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/major_potw_data_newocsd.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/minor_potw_data.nc'
maj_newp = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_combine_1997_2017/'
fig_path = './figs/'

majfi = sorted(glob.glob(maj_newp+'*xlsx'))

htp_up = pd.read_excel(majfi[0],sheet_name='formatted',header=None)
jwp_up = pd.read_excel(majfi[1],sheet_name='formatted',header=None)
ocs_up = pd.read_excel(majfi[2],sheet_name='formatted',header=None,skiprows=2)
plw_up = pd.read_excel(majfi[3],sheet_name='formatted',header=None)

htp_dt = np.array(pd.to_datetime(htp_up[0][1:]))
jwp_dt = np.array(pd.to_datetime(jwp_up[0][1:]))
ocs_dt = np.array(pd.to_datetime(ocs_up[0][1:]))
plw_dt = np.array(pd.to_datetime(plw_up[0][1:]))

htp_flo = np.array(htp_up[15][1:].astype(float))
jwp_flo = np.array(jwp_up[1][1:].astype(float))
ocs_flo = np.array(ocs_up[1][1:].astype(float))
plw_flo = np.array(plw_up[10][1:].astype(float))

htp_nh4 = np.array(htp_up[9][1:].astype(float))
jwp_nh4 = np.array(jwp_up[2][1:].astype(float))
ocs_nh4 = np.array(ocs_up[17][1:].astype(float))
plw_nh4 = np.array(plw_up[3][1:].astype(float))

htp_no3 = np.array(htp_up[6][1:].astype(float))
jwp_no3 = np.array(jwp_up[19][1:].astype(float))
ocs_no3 = np.array(ocs_up[18][1:].astype(float))
plw_no3 = np.array(plw_up[5][1:].astype(float))

htp_no2 = np.array(htp_up[5][1:].astype(float))
jwp_no2 = np.array(jwp_up[6][1:].astype(float))

htp_din = np.nansum((htp_nh4,htp_no3,htp_no2),axis=0)
jwp_din = np.nansum((jwp_nh4,jwp_no3,jwp_no2),axis=0)
ocs_din = np.nansum((ocs_nh4,ocs_no3),axis=0)
plw_din = np.nansum((plw_nh4,plw_no3),axis=0)

htp_din[htp_din==0] = np.nan
jwp_din[jwp_din==0] = np.nan
ocs_din[ocs_din==0] = np.nan
plw_din[plw_din==0] = np.nan

plt.ion()

###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time_dt = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

ind_1997 = 313
ind_2007 = 433

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
col_p = ['blue','orange','green','red']

# conversion
convn = 14./1000 # mmol/m3 to mg/L
convp = 30.97/1000 # mmol/m3 to kg/L
convnf = (14.*86400)/1E6 # mmol/s to kg/d
convpf = (30.97*86400)/1E6 # mmol/s to kg/d
convv = 1./0.043812645072430365 # m3/s to mgd
conva = 3.78541178 # million gal/day * mg/L to kg/d

# din
savename_major = 'major_potw_ts_1997_2017_din.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,p_i,p_i]*convv,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_din[ind_1997:ind_2007,p_i,p_i]*convn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_din[ind_1997:ind_2007,p_i,p_i]*major_flo[ind_1997:ind_2007,p_i,p_i]*convnf,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].plot(htp_dt,htp_flo,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[0].plot(jwp_dt,jwp_flo,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[0].plot(ocs_dt,ocs_flo,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(plw_dt,plw_flo,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])
axes.flat[1].plot(htp_dt,htp_din,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[1].plot(jwp_dt,jwp_din,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[1].plot(ocs_dt,ocs_din,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].scatter(plw_dt,plw_din,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])
axes.flat[2].plot(htp_dt,htp_din*htp_flo*conva,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[2].plot(jwp_dt,jwp_din*jwp_flo*conva,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[2].plot(ocs_dt,ocs_din*ocs_flo*conva,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(plw_dt,plw_din*plw_flo*conva,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('DIN mg L$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('DIN flux kg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

# nh4
savename_major = 'major_potw_ts_1997_2017_nh4.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
for p_i in range(len(major_names)):
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,p_i,p_i]*convv,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,p_i,p_i]*convn,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,p_i,p_i]*major_flo[ind_1997:ind_2007,p_i,p_i]*convnf,linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])

axes.flat[0].plot(htp_dt,htp_flo,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[0].plot(jwp_dt,jwp_flo,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[0].plot(ocs_dt,ocs_flo,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[0].plot(plw_dt,plw_flo,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])
axes.flat[1].plot(htp_dt,htp_nh4,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[1].plot(jwp_dt,jwp_nh4,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[1].plot(ocs_dt,ocs_nh4,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(plw_dt,plw_nh4,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])
axes.flat[2].plot(htp_dt,htp_nh4*htp_flo*conva,linestyle=major_linesty[0],linewidth=lw,color=col_p[0])
axes.flat[2].plot(jwp_dt,jwp_nh4*jwp_flo*conva,linestyle=major_linesty[1],linewidth=lw,color=col_p[1])
axes.flat[2].plot(ocs_dt,ocs_nh4*ocs_flo*conva,linestyle=major_linesty[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(plw_dt,plw_nh4*plw_flo*conva,linestyle=major_linesty[3],linewidth=lw,color=col_p[3])

axes.flat[0].set_ybound(lower=0)
axes.flat[1].set_ybound(lower=0)
axes.flat[2].set_ybound(lower=0)
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[1].set_ylabel('NH4 mg L$^{-1}$',fontsize=axis_font)
axes.flat[2].set_ylabel('NH4 flux kg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_tick_font)
axes.flat[0].grid(True)
axes.flat[1].grid(True)
axes.flat[2].grid(True)
axes.flat[0].legend(loc='lower left',fontsize=axis_tick_font,bbox_to_anchor=[0,1.02,1,.102],ncol=4,mode='expand',borderaxespad=0.,handlelength=3)
fig.savefig(savename_major,bbox_inches='tight')

'''
# ocsd only
savename_major = fig_path+'ocsd_ts_19972010_20132017.png'
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_tn[ind_1997:ind_2007,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_tp[ind_1997:ind_2007,2,2]*convp,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
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
axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_tn[ind_1997:ind_2007,2,2]*major_flo[ind_1997:ind_2007,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_tp[ind_1997:ind_2007,2,2]*major_flo[ind_1997:ind_2007,2,2]*convpf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
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
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
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
    axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
    axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,p_i,p_i]*major_flo[ind_1997:ind_2007,p_i,p_i],linestyle=major_linesty[p_i],label=major_names[p_i],linewidth=lw,color=col_p[p_i])
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
axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_nh4[ind_1997:ind_2007,2,2]*major_flo[ind_1997:ind_2007,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
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
axes.flat[0].plot(major_time_dt[ind_1997:ind_2007],major_flo[ind_1997:ind_2007,2,2]*convv,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[1].plot(major_time_dt[ind_1997:ind_2007],major_din[ind_1997:ind_2007,2,2]*convn,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
axes.flat[2].plot(major_time_dt[ind_1997:ind_2007],major_din[ind_1997:ind_2007,2,2]*major_flo[ind_1997:ind_2007,2,2]*convnf,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color=col_p[2])
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

'''
