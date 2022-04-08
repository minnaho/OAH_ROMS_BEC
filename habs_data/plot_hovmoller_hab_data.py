import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmocean

# read in data
df_raw = pd.read_csv('WW_data_Clearlake_trimmed_2020.csv')

# convert to datetime to plot
dt_plt = pd.to_datetime(df_raw['date_time'])

# get variables
dp_plt = df_raw['depth']
o2_plt = df_raw['DO_conc']
tm_plt = df_raw['temp']
ch_plt = df_raw['chla']

#plt.ion()

figw = 14
figh = 8

axfont = 16

# change colormap here
# see https://matplotlib.org/cmocean/ for selecting a colormap
# e.g., change this to cmocean.cm.thermal for the thermal colormap
c_map = cmocean.cm.balance

# plotting
fig,ax = plt.subplots(1,1,figsize=[figw,figh])

# change o2_plt to the other variables to plot them
p_plt = ax.scatter(dt_plt,dp_plt,s=20,c=o2_plt,marker='s',cmap=c_map)

# flip y axis to make depth make sense
ax.invert_yaxis()

# set date limits
ax.set_xlim([pd.to_datetime('2020-08-03'),pd.to_datetime('2020-08-19')])

# rotate dates in x axis so they don't run into each other
plt.xticks(rotation=45)

# colorbar settings
p0 = ax.get_position().get_points().flatten()
cb_ax = fig.add_axes([p0[2]+.015,p0[1],.01,p0[3]-p0[1]])
#cb = fig.colorbar(p_plt,cax=cb_ax,orientation='vertical',ticks=np.arange(v_min,v_max+cbstp,cbstp))
cb = fig.colorbar(p_plt,cax=cb_ax,orientation='vertical')

# change variable name for each variable
cb.set_label('O2 mg/L',fontsize=axfont)
cb.ax.tick_params(axis='both',which='major',labelsize=axfont)


ax.set_ylabel('Depth (m)',fontsize=axfont)
ax.set_xlabel('Time',fontsize=axfont)
ax.tick_params(axis='both',which='major',labelsize=axfont)
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')

# save figure, change name of variable here
plt.savefig('O2_hovmoller.png',bbox_inches='tight')

