###################################################################
# read calcofi data and other data net primary production and nitrification
# compare to L2 model 1997-2000
# Nov 2019
################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset,num2date,date2num
import glob
import datetime
import calendar
import pandas as pd
#plt.ion()

##########################
# load observation data
#########################

# rate data from Karen (bight 18 and from literature)
rate_name = '/data/project1/minnaho/validation/ValidationRateData_mh.xlsx'
nitr_rate_df = pd.read_excel(rate_name,sheet_name='Nitrification and nut uptake')
growth_df = pd.read_excel(rate_name,sheet_name='growth and grazing')
npp_df = pd.read_excel(rate_name,sheet_name='Primary Production')

phyto_grw = np.array(growth_df['phytoplankton growth'][9:][~np.isnan(growth_df['phytoplankton growth'][9:])])

microzoo_grz = np.array(growth_df['depthintegratedmicrozooplanktongrazing'][~np.isnan(growth_df['depthintegratedmicrozooplanktongrazing'])])
meso_grz = np.array(growth_df['depthintegratedmesozooplanktongrazing'][~np.isnan(growth_df['depthintegratedmesozooplanktongrazing'])])
tot_grz = microzoo_grz+meso_grz

# onshore vs offshore
grw_onshore = np.array(list(phyto_grw[:7])+list(phyto_grw[15:29])+list(phyto_grw[37:45])+list(phyto_grw[53:]))
grw_ofshore = np.array(list(phyto_grw[7:15])+list(phyto_grw[29:37])+list(phyto_grw[45:53]))

grz_micro_only = np.array(growth_df['mircozooplanktongrazing'][~np.isnan(growth_df['mircozooplanktongrazing'])])
grz_on = np.array(list(grz_micro_only[:7])+list(grz_micro_only[15:29])+list(grz_micro_only[37:45])+list(grz_micro_only[53:]))
grz_of = np.array(list(grz_micro_only[7:15])+list(grz_micro_only[29:37])+list(grz_micro_only[45:53]))


nitr_up = np.array(nitr_rate_df['CHl normalized Max Nitrate Uptake-- Vmax (uM N ug Chl -1 h-1)'][~np.isnan(nitr_rate_df['CHl normalized Max Nitrate Uptake-- Vmax (uM N ug Chl -1 h-1)'])])*24

ammo_up = np.array(nitr_rate_df['CHl normalized Max Ammonium Uptake-- Vmax (uM N ug Chl -1 h-1)'][~np.isnan(nitr_rate_df['CHl normalized Max Ammonium Uptake-- Vmax (uM N ug Chl -1 h-1)'])])*24

# separate into regions
oc_nl = []
la_nl = []
sd_nl = []
oc_al = []
la_al = []
sd_al = []
stations = 5
for i in range(len(nitr_up)):
    if i%stations == 0 or i%stations == 2:
        oc_nl.append(nitr_up[i])
        oc_al.append(ammo_up[i])
    if i%stations == 1 or i%stations == 4:
        la_nl.append(nitr_up[i])
        la_al.append(ammo_up[i])
    if i%stations == 3:
        sd_nl.append(nitr_up[i])
        sd_al.append(ammo_up[i])

oc_nitr_up = np.array(oc_nl)
oc_ammo_up = np.array(oc_al)
la_nitr_up = np.array(la_nl)
la_ammo_up = np.array(la_al)
sd_nitr_up = np.array(sd_nl)
sd_ammo_up = np.array(sd_al)

plt.ion()
axis_size = 14
'''
fig1,axes1 = plt.subplots(1,2,figsize=[15,9])
#axes[0].boxplot(phyto_grw,whis=[5,95],showfliers=False)
#axes[1].boxplot(microzoo_grz,whis=[5,95],showfliers=False)
axes1[0].boxplot(phyto_grw,labels=['Phytoplankton Growth'],showfliers=False)
axes1[0].set_ylabel('d$^{-1}$',fontsize=axis_size)
axes1[1].boxplot(tot_grz,labels=['Depth Integrated Zooplankton Grazing'],showfliers=False)
axes1[1].set_ylabel('d$^{-1}$',fontsize=axis_size)
axes1[0].grid(True)
axes1[1].grid(True)
axes1[0].tick_params(axis='both',labelsize=axis_size)
axes1[1].tick_params(axis='both',labelsize=axis_size)
plt.savefig('growth_graze.png',bbox_inches='tight')
'''
grw_all = [grw_onshore,grw_ofshore]
grz_all = [grz_on,grz_of]
fig1,axes1 = plt.subplots(1,2,figsize=[15,9])
#axes[0].boxplot(phyto_grw,whis=[5,95],showfliers=False)
#axes[1].boxplot(microzoo_grz,whis=[5,95],showfliers=False)
axes1[0].boxplot(grw_all,labels=['Onshore','Offshore'],showfliers=False)
axes1[0].set_xlabel('Phytoplankton Growth',fontsize=axis_size)
axes1[0].set_ylabel('d$^{-1}$',fontsize=axis_size)
axes1[1].boxplot(grz_all,labels=['Onshore','Offshore'],showfliers=False)
axes1[1].set_xlabel('Microzooplankton Grazing',fontsize=axis_size)
axes1[1].set_ylabel('d$^{-1}$',fontsize=axis_size)
axes1[0].grid(True)
axes1[1].grid(True)
axes1[0].tick_params(axis='both',labelsize=axis_size)
axes1[1].tick_params(axis='both',labelsize=axis_size)
plt.savefig('growth_graze.png',bbox_inches='tight')

fig2,axes2 = plt.subplots(1,2,figsize=[15,9])
nitr_plot = [oc_nitr_up,la_nitr_up,sd_nitr_up]
ammo_plot = [oc_ammo_up,la_ammo_up,sd_ammo_up]
axes2[0].boxplot(nitr_plot,labels=['OC','LA','SD'],showfliers=False)
axes2[0].set_ylabel('mmol N mg Chl$^{-1}$ d$^{-1}$',fontsize=axis_size)
axes2[0].set_xlabel('NO3 uptake',fontsize=axis_size)
axes2[1].boxplot(ammo_plot,labels=['OC','LA','SD'],showfliers=False)
axes2[1].set_ylabel('mmol N mg Chl$^{-1}$ d$^{-1}$',fontsize=axis_size)
axes2[1].set_xlabel('NH4 uptake',fontsize=axis_size)
axes2[0].grid(True)
axes2[1].grid(True)
axes2[0].tick_params(axis='both',labelsize=axis_size)
axes2[1].tick_params(axis='both',labelsize=axis_size)
plt.savefig('uptake_bight18.png',bbox_inches='tight')

fig2,axes2 = plt.subplots(1,1,figsize=[7,9])
nitr_plot = [la_nitr_up,la_ammo_up]
axes2.boxplot(nitr_plot,labels=['NO3 uptake','NH4 uptake'],showfliers=True)
axes2.set_ylabel('mmol N mg Chl$^{-1}$ d$^{-1}$',fontsize=axis_size)
axes2.grid(True)
axes2.tick_params(axis='both',labelsize=axis_size)
axes2.set_title('LA/Palos Verdes',fontsize=axis_size)
plt.savefig('uptake_bight18_la_fliers.png',bbox_inches='tight')


fig2,axes2 = plt.subplots(1,1,figsize=[7,9])
nitr_plot = [list(oc_nitr_up)+list(la_nitr_up)+list(sd_nitr_up),list(oc_ammo_up)+list(la_ammo_up)+list(sd_ammo_up)]
axes2.boxplot(nitr_plot,labels=['NO3 uptake','NH4 uptake'],showfliers=True)
axes2.set_ylabel('mmol N mg Chl$^{-1}$ d$^{-1}$',fontsize=axis_size)
axes2.grid(True)
axes2.tick_params(axis='both',labelsize=axis_size)
axes2.set_title('All Available Regions - LA, OC, Oceanside',fontsize=axis_size)
plt.savefig('uptake_bight18_all_fliers.png',bbox_inches='tight')
