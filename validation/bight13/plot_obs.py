###################################################################
# read and plot bight data  
# Oct 24 2018 Minna Ho minnaho@ucla.edu
################################################################
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset
import glob
import datetime
#import depths as depths
import calendar
#plt.ion()


##########################
# load observation data
#########################
text_file = pd.read_csv('ProcessStudiesFull_minna_edit.csv',header=None)

lats = [
33.6985, 
33.73, 
33.7573, 
33.6685, 
33.694, 
33.5756, 
33.5812, 
33.5848, 
33.546, 
33.2154, 
33.1838, 
33.6067, 
33.4194]  

lons = [
-118.336,
-118.402,
-118.441,
-118.297,
-118.191,
-118.005,
-118.052,
-117.945,
-117.836,
-117.481,
-117.523,
-118.409,
-117.912]

station_IDs = [
'2903',
'3053',
'3003',
'2803',
'2602',
'2205',
'2306',
'2103',
'1903',
'CP1',
'CP2',
'SPOTS',
'9030']

# station IDs
# 2903  LACSD ocean outfall (JWPC)
# 3053  LACSD Off-Outfall (northern current) 
# 3003  LACSD Off-Outfall (northern current) 
# 2803  LACSD Off-Outfall (southern current) 
# 2602  Long Beach Harbor Shelf (LA County) 
# 2205  OCSD Ocean Outfall 
# 2306  OCSD Off-Outfall (northern current) 
# 2103  OCSD Off-Outfall (southern current) 
# 1903  Orange County Southern Transect Line 
# CP1   Northern San Diego County- on shelf 
# CP2   Northern San Diego County- continental slope 
# SPOTS San Pedro Ocean Time Series (LA County Offshore)
# 9030  CALCOFI station 9030 (Orange County Offshore) 

# get data and variable
# 28 = AvgNH4
# 27 = SCCWRPChl
# 32 = Chlorophyll
# 33 = CDOM
# 9  = PO4
# 30 = Salinity
# 31 = oxygen
# 29 = temperature
variable_num = 29
variable_name = 'Temperature'
#variable_unit = 'mmol m$^{-3}$'
variable_unit = 'C'

ind_jwpcp = np.where((text_file[2]==station_IDs[0]))[0]
ind_ocsd = np.where((text_file[2]==station_IDs[5]))[0]
 
nh4_jwpcp = np.array(text_file.iloc[ind_jwpcp,variable_num]).astype(np.float)
nh4_ocsd = np.array(text_file.iloc[ind_ocsd,variable_num]).astype(np.float)

depth_jwpcp = np.array(text_file.iloc[ind_jwpcp,8]).astype(np.float)
depth_ocsd = np.array(text_file.iloc[ind_ocsd,8]).astype(np.float)

################
# plot
################
suptitle_size = 20
xy_labels = 16
tick_size = 14
legend_size = 14
fig1, (ax1, ax2) = plt.subplots(1,2,sharey=True,figsize=(14,9))
# plot observation
num_depths = 5
profiles = int(len(depth_jwpcp)/num_depths)
line_col = ['green','red']

for p_i in range(profiles):
    if p_i == 1 or p_i == 3:
        ax1.plot([nh4_jwpcp[p_i*num_depths],nh4_jwpcp[(p_i*num_depths)+2],nh4_jwpcp[(p_i*num_depths)+1],nh4_jwpcp[(p_i*num_depths)+3],nh4_jwpcp[(p_i)*num_depths+4]],[depth_jwpcp[p_i*num_depths],depth_jwpcp[(p_i*num_depths)+2],depth_jwpcp[(p_i*num_depths)+1],depth_jwpcp[(p_i*num_depths)+3],depth_jwpcp[(p_i)*num_depths+4]],'o-',label='Spring',color=line_col[0])
        ax2.plot(nh4_ocsd[p_i*num_depths:(p_i+1)*num_depths],depth_ocsd[p_i*num_depths:(p_i+1)*num_depths],'o-',label='Spring',color=line_col[0])
    else:
        ax1.plot(nh4_jwpcp[p_i*num_depths:(p_i+1)*num_depths],depth_jwpcp[p_i*num_depths:(p_i+1)*num_depths],'o-',label='Summer',color=line_col[1])
        ax2.plot(nh4_ocsd[p_i*num_depths:(p_i+1)*num_depths],depth_ocsd[p_i*num_depths:(p_i+1)*num_depths],'o-',label='Summer',color=line_col[1])

#    ax2.plot(nh4_ocsd[p_i*num_depths:(p_i+1)*num_depths],depth_ocsd[p_i*num_depths:(p_i+1)*num_depths],'o-',label='Observation',color=line_col[p_i])

ax1.set_ylabel('Depth (m)',fontsize=xy_labels)
ax1.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
ax1.set_xlabel('JWPCP '+variable_name+' '+variable_unit,fontsize=xy_labels)
ax1.xaxis.set_label_position('top') # this moves the label to the top
ax1.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax1.tick_params(axis='both',which='major',labelsize=tick_size)
#ax1.legend(loc='best',fontsize=legend_size)
ax1.grid(True)

# Salinity
ax2.legend(loc='upper right',fontsize=legend_size,bbox_to_anchor=(1.3,1))
ax2.set_xlabel('OCSD '+variable_name+' '+variable_unit,fontsize=xy_labels)
ax2.xaxis.set_label_position('top') # this moves the label to the top
ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax2.tick_params(axis='both',which='major',labelsize=tick_size)
#ax2.yaxis.set_visible(False) # This erases the y ticks
ax2.grid(True)
plt.suptitle('Bight Process Studies Observations 2014-09-02 to 2016-03-29',fontsize=suptitle_size)
plt.savefig('bight_obs_'+variable_name+'.png',bbox_inches='tight')
#plt.show()

