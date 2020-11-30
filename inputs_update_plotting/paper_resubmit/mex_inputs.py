import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

figp = './figs/'

fi = pd.read_csv('sbiwtp_tijuana.csv')
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

sbflo = np.array(fi['sb flow m3/s'])
trflo = np.array(fi['tr flow m3/s'])
mxflo = np.array(fi['mx mgd'])*mgd_to_m3s

sb_dinmm = np.nansum((fi['sb no3 mmol/m3'],fi['sb nh4 mmol/m3'],fi['sb no2 mmol/m3']),axis=0)
sb_dinfl = sbflo*sb_dinmm*s_to_d*mmol_to_mol*g_to_kg*g_N

tr_dinmm = np.nansum((fi['tr no3 mg/L'],fi['tr nh4 mg/L'],fi['tr no2 mg/L']),axis=0)
tr_dinfl = trflo*tr_dinmm*mg_l_n*s_to_d*mmol_to_mol*g_to_kg*g_N

mx_dinmm = np.array(fi['mx din mg/L'])
mx_dinfl = mxflo*mx_dinmm*mg_l_n*s_to_d*mmol_to_mol*g_to_kg*g_N

figw = 14
figh = 8

axis_font = 16
lw = 2

plt.ion()
fig,axes = plt.subplots(2,1,sharex=True,figsize=[figw,figh],gridspec_kw={'height_ratios':[3,1]})
axes[0].plot(fi['date'],sb_dinfl,linestyle='-',linewidth=lw,color='black',label='SBIWTP')
axes[0].plot(fi['date'],tr_dinfl,linestyle='--',linewidth=lw,color='blue',label='Tijuana River')
axes[0].plot(fi['date'],mx_dinfl,linewidth=lw,linestyle=':',color='red',label='Mexican WW Inputs')
axes[0].set_ylabel('DIN Flux kg d$^{-1}$',fontsize=axis_font)
axes[0].set_ybound(lower=0)
axes[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes[0].legend(loc='best',fontsize=axis_font)

axes[1].plot(fi['date'],sb_dinfl,linestyle='-',linewidth=lw,color='black',label='SBIWTP')
axes[1].plot(fi['date'],mx_dinfl,linewidth=lw,linestyle=':',color='red',label='Mexican WW Inputs')
axes[1].set_ylabel('DIN Flux kg d$^{-1}$',fontsize=axis_font)
axes[1].set_ybound(lower=0)
axes[1].tick_params(axis='both',which='major',labelsize=axis_font)
fig.savefig(figp+'mx_din.png',bbox_inches='tight')
