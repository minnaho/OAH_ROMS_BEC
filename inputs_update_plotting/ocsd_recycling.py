import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

figp = './figs/'

fi = pd.read_csv('ocsd_recycling_overtime.csv')
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

infflo = np.nansum((fi['influent1'],fi['influent2']),axis=0)*mgd_to_m3s
infflo[infflo==0] = np.nan
totflo = np.array(fi['total effluent'])*mgd_to_m3s
rooflo = np.array(fi['RO reject'])*mgd_to_m3s

dinmg = np.nansum((fi['no3'],fi['nh4'],fi['no2']),axis=0)
dinmg[dinmg==0] = np.nan
dinfl = totflo*(np.nansum((fi['no3'],fi['nh4'],fi['no2']),axis=0)*mg_l_n)*s_to_d*mmol_to_mol*g_to_kg*g_N

siomg = fi['sio4']
siofl = totflo*(siomg*mg_l_s)*s_to_d*mmol_to_mol*g_to_kg*g_N

figw = 12
figh = 7

axis_font = 16
lw = 2

plt.ion()
fig,axes = plt.subplots(1,1,sharex=True,figsize=[figw,figh])
axes.plot(fi['date'],infflo,linestyle='-',linewidth=lw,color='blue',label='Influent')
axes.plot(fi['date'],totflo,linestyle='--',linewidth=lw,color='black',label='Total Effluent')
axes.plot(fi['date'],rooflo,linewidth=lw,linestyle=':',color='red',label='RO Reject')
axes.set_ylabel('Volume Flux m$^3$ s$^{-1}$',fontsize=axis_font)
axes.tick_params(axis='both',which='major',labelsize=axis_font)
axes.legend(loc='best',fontsize=axis_font)
fig.savefig(figp+'ocsd_flow.png',bbox_inches='tight')


fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(fi['date'],dinmg,linewidth=lw,linestyle='-',color='C2')
axes.flat[1].plot(fi['date'],dinfl,linewidth=lw,linestyle='-',color='C2')
axes.flat[0].set_ylabel('DIN mg L$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('DIN Flux \nkg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_font)
fig.savefig(figp+'ocsd_din.png',bbox_inches='tight')

fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh])
axes.flat[0].plot(fi['date'],siomg,linewidth=lw,linestyle='-',color='C3')
axes.flat[1].plot(fi['date'],siofl,linewidth=lw,linestyle='-',color='C3')
axes.flat[0].set_ylabel('SiO4 mg L$^{-1}$',fontsize=axis_font)
axes.flat[1].set_ylabel('SiO4 Flux \nkg d$^{-1}$',fontsize=axis_font)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_font)
fig.savefig(figp+'ocsd_sio.png',bbox_inches='tight')
