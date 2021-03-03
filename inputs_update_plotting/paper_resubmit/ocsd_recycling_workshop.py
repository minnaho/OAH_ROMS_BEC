import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime

figp = './figs/'

fi = pd.read_csv('../ocsd_recycling_overtime.csv')
#fi = fi.dropna()

fi['date'] = pd.to_datetime(fi['date'])

mgd_to_m3s = 0.043812645072430365
mg_l_n = 1000./14
mg_l_s = 1000./28.0855

#convert to kg/day or kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14
m3s_to_mgd = 22.824465227271


dt_20 = pd.date_range(start='2018-01-31',end='2020-06-30',freq='M')
fl_20 = np.array((87.47, 84.64, 84.14, 94.9, 81.45, 85.07, 88.04, 113.47, 159.23, 92.59, 83.73, 87.42, 100.45, 123.67, 112.35, 98.26, 102.45, 94.08, 92.73, 92.31, 93.74, 90.8, 87.14, 102.68, 98.2, 100.32, 101.88, 130.63, 127.79, 89.64))
in1_20 = np.array((120.17, 121.18, 120.78, 121.59, 120.97, 122.32, 123.09, 123.38, 114.49, 119.11, 117.74, 118.32, 117.67, 131.57, 126.79, 114.48, 111.44, 116.61, 116.88, 117.24, 117.07, 115.39, 121.25, 123.61, 123.42, 123.18, 118.26, 119.47, 116.97, 114.49))
in2_20 = np.array(( 62.81, 61.42, 60.56, 62.72, 60.12, 62.82, 64.74, 65.97, 71.96, 63.52, 62.54, 64.81, 73.4, 87.14, 80.41, 75.85, 75.47, 71.43, 70.94, 70.23, 70.73, 68.96, 63.82, 68.19, 65.9, 64.88, 73.59, 76.56, 69.05, 69.14))
ro_20 = np.array(( 17.4, 17.9, 17.8, 16.3, 18.2, 18.3, 18.2, 13.9, 5.0, 16.4, 17.6, 17.5, 16.6, 17.4, 17.3, 16.8, 15.4, 17.2, 17.4, 17.4, 17.2, 17.1, 17.9, 16.3, 16.6, 16.0, 16.4, 11.9, 10.6, 17.2,))

nh_20 = np.array((26.6, 25.6, 31.7, 28.4, 29.8, 21.2, 21.1, 18, 12, 21.1, 23.5, 25.6, 30.1, 32.2, 34.4, 34.1, 34.6, 31.3, 29.4, 26, 24.9, 27.9, 25.3, 26.5, 28.1, 33.1, 34.6, 26.3, 26.8, 31.7))
nn_20 = np.array((20.3, 20.3, 19.8, 27.4, 27.4, 35, 29.65, 29.65, 24.3, 19.65, 19.65, 15, 16.5, 16.5, 18, 14.35, 14.35, 10.7, 13.55, 13.55, 16.4, 17.4, 17.4, 18.4, 17.7, 17.7, 17, 15.65, 15.65, 14.3))

dn_20 = nh_20+nn_20

#infflo = np.nansum((fi['influent1'],fi['influent2']),axis=0)*mgd_to_m3s
#infflo[infflo==0] = np.nan
#totflo = np.array(fi['total effluent'])*mgd_to_m3s
#rooflo = np.array(fi['RO reject'])*mgd_to_m3s
infflo = np.nansum((fi['influent1'],fi['influent2']),axis=0)
infflo[infflo==0] = np.nan
totflo = np.array(fi['total effluent'])
rooflo = np.array(fi['RO reject'])

dinmg = np.nansum((fi['no3'],fi['nh4'],fi['no2']),axis=0)
dinmg[dinmg==0] = np.nan
dinfl = totflo*mgd_to_m3s*(np.nansum((fi['no3'],fi['nh4'],fi['no2']),axis=0)*mg_l_n)*s_to_d*mmol_to_mol*g_to_kg*g_N

siomg = fi['sio4']
siofl = totflo*(siomg*mg_l_s)*s_to_d*mmol_to_mol*g_to_kg*g_N

figw = 12
figh = 14

axis_font = 16
lw = 2

plt.ion()
fig,axes = plt.subplots(3,1,sharex=True,figsize=[figw,figh])
#axes.plot(fi['date'],infflo,linestyle='-',linewidth=lw,color='blue',label='Influent')
#axes.plot(dt_20,in1_20+in2_20,linestyle='-',linewidth=lw,color='blue')
axes.flat[0].plot(fi['date'],totflo,linestyle='--',linewidth=lw,color='black',label='Total Effluent')
axes.flat[0].plot(dt_20,fl_20,linestyle='--',linewidth=lw,color='black')
axes.flat[0].plot(fi['date'],rooflo,linewidth=lw,linestyle=':',color='red',label='RO Reject')
axes.flat[0].plot(dt_20,ro_20,linewidth=lw,linestyle=':',color='red')
axes.flat[0].scatter(datetime.datetime(2023,1,1),50.3,color='black')
axes.flat[0].scatter(datetime.datetime(2023,1,1),23.0,color='red')
axes.flat[0].set_ylabel('Volume Flux MGD',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[0].legend(loc='best',fontsize=axis_font)

axes.flat[1].plot(fi['date'],fi['nh4'],linewidth=lw,linestyle='-',label='NH4')
axes.flat[1].plot(dt_20,nn_20,linewidth=lw,linestyle='-',color='C1')
axes.flat[1].plot(fi['date'],fi['no3'],linewidth=lw,linestyle='-',label='NO3+NO2')
axes.flat[1].plot(dt_20,nh_20,linewidth=lw,linestyle='-',color='C0')
axes.flat[1].scatter(datetime.datetime(2023,1,1),51,color='C0')
axes.flat[1].scatter(datetime.datetime(2023,1,1),29,color='C1')
axes.flat[1].legend(loc='best',fontsize=axis_font)
axes.flat[1].set_ylabel('N mg/L',fontsize=axis_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_font)

axes.flat[2].plot(fi['date'],dinfl,linewidth=lw,linestyle='-',color='C2')
axes.flat[2].plot(dt_20,dn_20*fl_20*(1./m3s_to_mgd)*(1000./14)*s_to_d*mmol_to_mol*g_to_kg*g_N,linewidth=lw,linestyle='-',color='C2')
axes.flat[2].scatter(datetime.datetime(2023,1,1),15245,color='C2')
axes.flat[2].set_ylabel('DIN kg/day',fontsize=axis_font)
axes.flat[2].tick_params(axis='both',which='major',labelsize=axis_font)


fig.savefig(figp+'ocsd_flow_Nload.png',bbox_inches='tight')

