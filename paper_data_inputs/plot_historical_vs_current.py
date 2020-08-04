import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt

# excel data
df = pd.read_excel('Historical versus present day composition of terrestrial inputs.xlsx')

h_nh4 = df['NH4'][0]
c_nh4 = df['NH4'][1]

h_don = df['PN+DON'][0]
c_don = df['PN+DON'][1]

h_nox = df['NOX'][0]
c_nox = df['NOX'][1]

h_po4 = df['PO4'][0]
c_po4 = df['PO4'][1]

h_dop = df['PP+DOP'][0]
c_dop = df['PP+DOP'][1]

# minor POTW
minor = Dataset('/data/project1/minnaho/potw_outfall_data/minor_potw_data_new.nc','r')

minor_flo = np.array(minor.variables['flow'][:12,:,:]) # m3/s
minor_nh4 = np.array(minor.variables['NH4'][:12,:,:]) # mmol/m3
minor_no3 = np.array(minor.variables['NO3'][:12,:,:]) # mmol/m3
minor_no2 = np.array(minor.variables['NO2'][:12,:,:]) # mmol/m3
minor_po4 = np.array(minor.variables['PO4'][:12,:,:]) 

minor_flo[minor_flo>1E20] = np.nan
minor_nh4[minor_nh4>1E20] = np.nan
minor_no3[minor_no3>1E20] = np.nan
minor_no2[minor_no2>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

nh4_flux = np.nansum(np.nansum(np.nansum(minor_flo*minor_nh4*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=1),axis=1))
no3_flux = np.nansum(np.nansum(np.nansum(minor_flo*minor_no3*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=1),axis=1))
no2_flux = np.nansum(np.nansum(np.nansum(minor_flo*minor_no2*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=1),axis=1))
po4_flux = np.nansum(np.nansum(np.nansum(minor_flo*minor_po4*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol,axis=1),axis=1))

c_nh4_p = c_nh4+nh4_flux
c_nox_p = c_nox+no3_flux+no2_flux
c_po4_p = c_po4+po4_flux

# plot
plt.ion()
figw = 10
figh = 8
hc_labels = ['Historical','Current']
width = .5
axis_font=16
hlen = 2.5

fig,axes = plt.subplots(1,2,figsize=[figw,figh])
x_ind = np.arange(len(hc_labels))
axes.flat[0].bar(x_ind[0]+width,h_nh4,width=width,color='black',label='NH4')
axes.flat[0].bar(x_ind[0]+width,h_don,width=width,bottom=h_nh4,color='lightgray',label='PN+DON',hatch='/')
axes.flat[0].bar(x_ind[0]+width,h_nox,width=width,bottom=h_nh4+h_don,color='gray',label='NOX')
axes.flat[0].bar(x_ind[1]+width,c_nh4,width=width,color='black')
axes.flat[0].bar(x_ind[1]+width,c_don,width=width,bottom=c_nh4,color='lightgray',hatch='/')
axes.flat[0].bar(x_ind[1]+width,c_nox,width=width,bottom=c_nh4+c_don,color='gray')
axes.flat[0].set_yscale('log')
axes.flat[0].set_xticks([width,1+width])
axes.flat[0].set_xticklabels(hc_labels)
axes.flat[0].set_ybound(lower=10E2,upper=10E7)
axes.flat[0].set_xbound(lower=0,upper=2)
axes.flat[0].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[0].set_ylabel('TN (kg)',fontsize=axis_font)
axes.flat[0].legend(loc='upper left',fontsize=axis_font,handlelength=hlen)



axes.flat[1].bar(x_ind[0]+width,h_po4,width=width,color='black',label='PO4')
axes.flat[1].bar(x_ind[0]+width,h_dop,width=width,bottom=h_po4,color='lightgray',label='PP+DOP',hatch='/')
axes.flat[1].bar(x_ind[1]+width,c_po4,width=width,color='black')
axes.flat[1].bar(x_ind[1]+width,c_dop,width=width,bottom=c_po4,color='lightgray',hatch='/')
axes.flat[1].set_yscale('log')
axes.flat[1].legend(loc='best')
axes.flat[1].set_xticks([width,1+width])
axes.flat[1].set_xticklabels(hc_labels)
axes.flat[1].set_ybound(lower=10E2,upper=10E7)
axes.flat[1].set_xbound(lower=0,upper=2)
axes.flat[1].tick_params(axis='both',which='major',labelsize=axis_font)
axes.flat[1].yaxis.set_label_position("right")
axes.flat[1].yaxis.tick_right()
axes.flat[1].set_ylabel('TP (kg)',fontsize=axis_font)
axes.flat[1].legend(loc='best',fontsize=axis_font,handlelength=hlen)

fig.savefig('./figs/hist_vs_current.pdf',bbox_inches='tight')

