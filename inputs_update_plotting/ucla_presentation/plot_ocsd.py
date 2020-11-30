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
major_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017.nc'
fig_path = './figs/'

#convert to kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# other constituents
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
major_pH  = np.array(major_nc.variables['pH']) 
major_alk = np.array(major_nc.variables['alkalinity']) 
major_toc = np.array(major_nc.variables['total_organic_C']) 
major_tpp = np.array(major_nc.variables['total_P']) # mmol/m3
major_fee  = np.array(major_nc.variables['total_Fe'])  # mmol/m3
major_bod  = np.array(major_nc.variables['BOD'])  # mmol/m3
major_sil  = np.array(major_nc.variables['SiO4'])  # mmol/m3
major_alk  = np.array(major_nc.variables['alkalinity'])  # mmol/m3


major_nh4[major_nh4>1E10] == np.nan
major_no3[major_no3>1E10] == np.nan
major_no2[major_no2>1E10] == np.nan
major_on[major_on>1E10] == np.nan

major_bod[major_bod>1E10] == np.nan
major_toc[major_toc>1E10] == np.nan
major_tpp[major_tpp>1E10] == np.nan
major_fee[major_fee>1E10] == np.nan
major_bod[major_bod>1E10] == np.nan
major_sil[major_sil>1E10] == np.nan
major_alk[major_alk>1E10] == np.nan

major_tn = major_nh4+major_no3+major_no2+major_on
major_din = major_nh4+major_no3+major_no2

major_tn[major_tn>1E20] = np.nan

# 2019-2020
dt_20 = pd.date_range(start='2018-01-31',end='2020-06-30',freq='M')
fl_20 = np.array((87.47, 84.64, 84.14, 94.9, 81.45, 85.07, 88.04, 113.47, 159.23, 92.59, 83.73, 87.42, 100.45, 123.67, 112.35, 98.26, 102.45, 94.08, 92.73, 92.31, 93.74, 90.8, 87.14, 102.68, 98.2, 100.32, 101.88, 130.63, 127.79, 89.64))
nh_20 = np.array((26.6, 25.6, 31.7, 28.4, 29.8, 21.2, 21.1, 18, 12, 21.1, 23.5, 25.6, 30.1, 32.2, 34.4, 34.1, 34.6, 31.3, 29.4, 26, 24.9, 27.9, 25.3, 26.5, 28.1, 33.1, 34.6, 26.3, 26.8, 31.7))
nn_20 = np.array((20.3, 20.3, 19.8, 27.4, 27.4, 35, 29.65, 29.65, 24.3, 19.65, 19.65, 15, 16.5, 16.5, 18, 14.35, 14.35, 10.7, 13.55, 13.55, 16.4, 17.4, 17.4, 18.4, 17.7, 17.7, 17, 15.65, 15.65, 14.3))
dn_20 = nh_20+nn_20
bd_20 = np.array(( 13.1, 14.2, 14.2, 14.2, 13.8, 10.9, 8.6, 6, 5.5, 9.7, 10.4, 10.5, 8.1, 8.8, 10.1, 11.4, 10.7, 12.5, 11.1, 7.8, 8.6, 11.3, 12.4, 11.6, 15.8, 12.6, 12.2, 10, 9.8, 13.8,))

tp_20 = np.array(( 4.0665, 4.1412, 4.1387, 3.8955, 4.2165, 4.1628, 4.1139, 3.5834, 3.0151, 3.9301, 4.1363, 4.0698, 3.8498, 3.6973, 3.7837, 3.8896, 3.7611, 3.9601, 3.9906, 3.9968, 3.9654, 3.9961, 4.1029, 3.8108, 3.8792, 3.8184, 3.8281, 3.3915, 3.3402, 4.0169))

tc_20 = np.array((16.3116, 16.7912, 16.7912, 16.7912, 16.6168, 15.3524, 14.3496, 13.216 , 12.998 , 14.8292, 15.1344, 15.178 , 14.1316, 14.4368, 15.0036, 15.5704, 15.2652, 16.05  , 15.4396, 14.0008, 14.3496, 15.5268, 16.0064, 15.6576, 17.4888, 16.0936, 15.9192, 14.96  , 14.8728, 16.6168))

fe_20 = np.array((382.6232, 386.3772, 386.2536, 374.0338, 390.1598, 387.4641, 385.0059, 358.3523, 329.8041, 375.7721, 386.1328, 382.7902, 371.7392, 364.0745, 368.4183, 373.7387, 367.2808, 377.2784, 378.8112, 379.1223, 377.5474, 379.0886, 384.4531, 369.7777, 373.2167, 370.1598, 370.6471, 348.7131, 346.1334, 380.1347))*(1./1000)
ak_20 = np.array((717.7382, 723.2974, 723.1144, 705.0182, 728.8990, 724.9071, 721.2666, 681.7957, 639.5188, 707.5924, 722.9355, 717.9855, 701.6201, 690.2696, 696.7023, 704.5812, 695.0177, 709.8232, 712.0930, 712.5537, 710.2214, 712.5038, 720.4480, 698.7154, 703.8081, 699.2812, 700.0028, 667.5210, 663.7007, 714.0530))
si_20 = np.array((55.9578, 56.8544, 56.8249, 53.9062, 57.7579, 57.1140, 56.5269, 50.1606, 43.3417, 54.3214, 56.7960, 55.9977, 53.3581, 51.5274, 52.5649, 53.8357, 52.2932, 54.6812, 55.0473, 55.1216, 54.7454, 55.1135, 56.3948, 52.8896, 53.7110, 52.9808, 53.0972, 47.8582, 47.2420, 55.3634))


# plotting major
figw = 10
#figw = 12
figh = 8
axis_tick_font = 14
axis_font = 14
major_names = ['HTP','JWPCP','OCSD','PLWTP']
major_linesty = ['-','--','-.',':']
lw = 2
iend_major = major_time_dt.shape[0]

# start 1998
stin = 9826
p_i = 2
plt.ion()
m3s_to_mgd = 22.824465227271
gwrs_dt = datetime.datetime(2023,1,1)
gwrs_fl = 50.3
# (mgd to m3/s) * (mg/L to mmol/m3) = mmol/s to kg/d
gwrs_nh_c = 28.88
gwrs_nn1_c = 40.863537
gwrs_nn2_c = 51.19
gwrs_dn1_c = 74.768152
gwrs_dn2_c = gwrs_nn2_c+gwrs_nh_c

gwrs_nh_l = (50.3*(1./m3s_to_mgd))*gwrs_nh_c*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N
gwrs_nn1_l = (50.3*(1./m3s_to_mgd))*40.863537*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N
gwrs_nn2_l = (50.3*(1./m3s_to_mgd))*gwrs_nn2_c*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N
gwrs_dn1_l = (50.3*(1./m3s_to_mgd))*74.768152*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N
gwrs_dn2_l = (50.3*(1./m3s_to_mgd))*gwrs_dn2_c*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N

fig,axes = plt.subplots(3,2,sharex=True,figsize=[figw+5,figh])
#axes.flat[0].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*m3s_to_mgd,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color='C0')
#axes.flat[0].set_ybound(lower=0)
#axes.flat[0].scatter(gwrs_dt,gwrs_fl)
#axes.flat[0].set_ylabel('Flow MGD',fontsize=axis_font)

axes.flat[0].plot(major_time_dt[stin:iend_major],major_nh4[stin:iend_major,2]*(14./1000),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].plot(dt_20,nh_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].set_ybound(lower=0)
axes.flat[0].scatter(gwrs_dt,gwrs_nh_c,color='C0')
axes.flat[0].set_ylabel('NH4 mg/L',fontsize=axis_font)

axes.flat[1].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_nh4[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].plot(dt_20,nh_20*fl_20*(1./m3s_to_mgd)*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].set_ybound(lower=0)
axes.flat[1].scatter(gwrs_dt,gwrs_nh_l,color='C0')
axes.flat[1].set_ylabel('NH4 kg/day',fontsize=axis_font)

axes.flat[2].plot(major_time_dt[stin:iend_major],(major_no3[stin:iend_major,2]+major_no2[stin:iend_major,2])*(14./1000),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].plot(dt_20,nn_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].set_ybound(lower=0)
#axes.flat[2].scatter(gwrs_dt,gwrs_nn1_c,color='C1')
axes.flat[2].scatter(gwrs_dt,gwrs_nn2_c,color='C1')
axes.flat[2].set_ylabel('NO3+NO2 mg/L',fontsize=axis_font)

axes.flat[3].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*(major_no3[stin:iend_major,2]+major_no2[stin:iend_major,2])*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].plot(dt_20,nn_20*fl_20*(1./m3s_to_mgd)*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].set_ybound(lower=0)
#axes.flat[3].scatter(gwrs_dt,gwrs_nn1_l)
axes.flat[3].scatter(gwrs_dt,gwrs_nn2_l,color='C1')
axes.flat[3].set_ylabel('NO3+NO2 kg/day',fontsize=axis_font)

axes.flat[4].plot(major_time_dt[stin:iend_major],major_din[stin:iend_major,2]*(14./1000),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[4].plot(dt_20,dn_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[4].set_ybound(lower=0)
#axes.flat[4].scatter(gwrs_dt,gwrs_dn1_c)
axes.flat[4].scatter(gwrs_dt,gwrs_dn2_c,color='C2')
axes.flat[4].set_ylabel('DIN mg/L',fontsize=axis_font)

axes.flat[5].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_din[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[5].plot(dt_20,dn_20*fl_20*(1./m3s_to_mgd)*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[5].set_ybound(lower=0)
#axes.flat[5].scatter(gwrs_dt,gwrs_dn1_l)
axes.flat[5].scatter(gwrs_dt,gwrs_dn2_l,color='C2')
axes.flat[5].set_ylabel('DIN kg/day',fontsize=axis_font)

for ax_i in range(6):
    axes.flat[ax_i].tick_params(axis='both',which='major',labelsize=axis_tick_font)

savename_major_flux = fig_path+'ocsd_N_loads.png'
fig.savefig(savename_major_flux,bbox_inches='tight')

# other constituents
gwrs_bd_c = 5.256160336
gwrs_tp_c = 4.2909
gwrs_tc_c = 31.8000
gwrs_fe_c = 491.2393*(1./1000)

gwrs_bd_l = (50.3*(1./m3s_to_mgd))*gwrs_bd_c*mg_l_c*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000))
gwrs_tp_l = (50.3*(1./m3s_to_mgd))*gwrs_tp_c*mg_l_p*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_p/1000))
gwrs_tc_l = (50.3*(1./m3s_to_mgd))*gwrs_tc_c*mg_l_c*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000))
gwrs_fe_l = (50.3*(1./m3s_to_mgd))*gwrs_fe_c*mg_l_f*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_f/1000))

fig,axes = plt.subplots(4,2,sharex=True,figsize=[figw+4,figh])
#axes.flat[0].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*m3s_to_mgd,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color='C0')
#axes.flat[0].set_ybound(lower=0)
#axes.flat[0].scatter(gwrs_dt,gwrs_fl)
#axes.flat[0].set_ylabel('Flow MGD',fontsize=axis_font)

axes.flat[0].plot(major_time_dt[stin:iend_major],major_bod[stin:iend_major,2]*(1./mg_l_c),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].plot(dt_20,bd_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].set_ybound(lower=0)
axes.flat[0].scatter(gwrs_dt,gwrs_bd_c,color='C0')
axes.flat[0].set_ylabel('BOD mg/L',fontsize=axis_font)

axes.flat[1].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_bod[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].plot(dt_20,bd_20*fl_20*(1./m3s_to_mgd)*(mg_l_c)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].set_ybound(lower=0)
axes.flat[1].scatter(gwrs_dt,gwrs_bd_l,color='C0')
axes.flat[1].set_ylabel('BOD kg/day',fontsize=axis_font)

axes.flat[2].plot(major_time_dt[stin:iend_major],major_tpp[stin:iend_major,2]*(1./mg_l_p),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].plot(dt_20,tp_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].set_ybound(lower=0)
axes.flat[2].scatter(gwrs_dt,gwrs_tp_c,color='C1')
axes.flat[2].set_ylabel('TP mg/L',fontsize=axis_font)

axes.flat[3].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_tpp[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_p/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].plot(dt_20,tp_20*fl_20*(1./m3s_to_mgd)*(mg_l_p)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_p/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].set_ybound(lower=0)
axes.flat[3].scatter(gwrs_dt,gwrs_tp_l,color='C1')
axes.flat[3].set_ylabel('TP kg/day',fontsize=axis_font)

axes.flat[4].plot(major_time_dt[stin:iend_major],major_toc[stin:iend_major,2]*(1./mg_l_c),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[4].plot(dt_20,tc_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[4].set_ybound(lower=0)
axes.flat[4].scatter(gwrs_dt,gwrs_tc_c,color='C2')
axes.flat[4].set_ylabel('TOC mg/L',fontsize=axis_font)

axes.flat[5].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_toc[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[5].plot(dt_20,tc_20*fl_20*(1./m3s_to_mgd)*(mg_l_c)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_c/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C2')
axes.flat[5].set_ybound(lower=0)
axes.flat[5].scatter(gwrs_dt,gwrs_tc_l,color='C2')
axes.flat[5].set_ylabel('TOC kg/day',fontsize=axis_font)

axes.flat[6].plot(major_time_dt[stin:iend_major],major_fee[stin:iend_major,2]*(1./mg_l_f),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C3')
axes.flat[6].plot(dt_20,fe_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C3')
axes.flat[6].set_ybound(lower=0)
axes.flat[6].scatter(gwrs_dt,gwrs_fe_c,color='C3')
axes.flat[6].set_ylabel('Fe mg/L',fontsize=axis_font)

axes.flat[7].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_fee[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_f/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C3')
axes.flat[7].plot(dt_20,fe_20*fl_20*(1./m3s_to_mgd)*(mg_l_f)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_f/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C3')
axes.flat[7].set_ybound(lower=0)
axes.flat[7].scatter(gwrs_dt,gwrs_fe_l,color='C3')
axes.flat[7].set_ylabel('Fe kg/day',fontsize=axis_font)

for ax_i in range(8):
    axes.flat[ax_i].tick_params(axis='both',which='major',labelsize=axis_tick_font)

savename_major_flux = fig_path+'ocsd_other_loads.png'
fig.savefig(savename_major_flux,bbox_inches='tight')

# alk and sil
gwrs_ak_c = 853.3188
gwrs_si_c = 76.7381

gwrs_ak_l = (50.3*(1./m3s_to_mgd))*gwrs_ak_c*mg_l_a*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_a/1000))
gwrs_si_l = (50.3*(1./m3s_to_mgd))*gwrs_si_c*mg_l_s*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_s/1000))

fig,axes = plt.subplots(2,2,sharex=True,figsize=[figw+6,figh])
#axes.flat[0].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*m3s_to_mgd,linestyle=major_linesty[2],label=major_names[2],linewidth=lw,color='C0')
#axes.flat[0].set_ybound(lower=0)
#axes.flat[0].scatter(gwrs_dt,gwrs_fl)
#axes.flat[0].set_ylabel('Flow MGD',fontsize=axis_font)

axes.flat[0].plot(major_time_dt[stin:iend_major],major_alk[stin:iend_major,2]*(1./mg_l_a),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].plot(dt_20,ak_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[0].set_ybound(lower=0)
axes.flat[0].scatter(gwrs_dt,gwrs_ak_c,color='C0')
axes.flat[0].set_ylabel('Alk mg/L',fontsize=axis_font)

axes.flat[1].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_alk[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_a/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].plot(dt_20,ak_20*fl_20*(1./m3s_to_mgd)*(mg_l_a)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_a/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C0')
axes.flat[1].set_ybound(lower=0)
axes.flat[1].scatter(gwrs_dt,gwrs_ak_l,color='C0')
axes.flat[1].set_ylabel('Alk kg/day',fontsize=axis_font)

axes.flat[2].plot(major_time_dt[stin:iend_major],major_sil[stin:iend_major,2]*(1./mg_l_s),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].plot(dt_20,si_20,linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[2].set_ybound(lower=0)
axes.flat[2].scatter(gwrs_dt,gwrs_si_c,color='C1')
axes.flat[2].set_ylabel('SiO4 mg/L',fontsize=axis_font)

axes.flat[3].plot(major_time_dt[stin:iend_major],major_flo[stin:iend_major,2]*major_sil[stin:iend_major,2]*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_s/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].plot(dt_20,si_20*fl_20*(1./m3s_to_mgd)*(mg_l_s)*s_to_d*mmol_to_mol*g_to_kg*(1./(mg_l_s/1000)),linestyle=major_linesty[0],label=major_names[2],linewidth=lw,color='C1')
axes.flat[3].set_ybound(lower=0)
axes.flat[3].scatter(gwrs_dt,gwrs_si_l,color='C1')
axes.flat[3].set_ylabel('SiO4 kg/day',fontsize=axis_font)

for ax_i in range(4):
    axes.flat[ax_i].tick_params(axis='both',which='major',labelsize=axis_tick_font)

savename_major_flux = fig_path+'ocsd_alk_si_loads.png'
fig.savefig(savename_major_flux,bbox_inches='tight')
