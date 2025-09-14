import os
import sys
sys.path.append('/data/project3/minnaho/global')
import numpy as np
from netCDF4 import Dataset,num2date
import l2grid
import pyfuncs as pf
import pandas as pd
import glob
import ROMS_depths as rd
import cmocean
import matplotlib.pyplot as plt

plt.ion()

tempnc = np.squeeze(Dataset('PV_temp.nc','r')['temperature'])
depthnc = np.squeeze(Dataset('PV_temp.nc','r')['depth'])
timenc = np.squeeze(Dataset('PV_temp.nc','r')['time'])
latnc = np.squeeze(Dataset('PV_temp.nc','r')['latitude'])
lonnc = np.squeeze(Dataset('PV_temp.nc','r')['longitude'])

gridnc = l2grid.grid_nc

isites,jsites = pf.calc_ij(gridnc,latnc,lonnc)
isites = isites.astype('int')
jsites = jsites.astype('int')

timefreq = 'minutes since 2000-10-31 00:15'

timedt = num2date(timenc,timefreq,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

# use this just to get length of monthly data
df = pd.DataFrame(data=tempnc[0,:,0],index=timedt,columns=['temp'])
df_monthly = df.resample('M').mean()

monthly_mean_arr = np.ones((len(df_monthly),len(latnc),len(depthnc)))*np.nan

for l_i in range(len(latnc)):
    for d_i in range(len(depthnc)):
        df = pd.DataFrame(data=tempnc[l_i,:,d_i],index=timedt,columns=['temp'])
        df_monthly = df.resample('M').mean()
        monthly_mean_arr[:,l_i,d_i] = df_monthly['temp']

#roms_path = '/data/project6/ROMS/L2SCB_AP/daily/'
#roms_files = sorted(glob.glob(roms_path+'*Y200[0-8]*'))
#
#roms_arr = np.ones((len(roms_files),len(isites),60))*np.nan
#roms_depths = np.ones((len(roms_files),len(isites),60))*np.nan
#
#startyear = 2000
#endyear = 2008
#startmonth = 10
#endmonth = 4

#for y_i in range(startyear,endyear+1):
#    # if we are on the first year, starts at s_m
#    if y_i == startyear:
#        s_m = startmonth
#    else:
#        s_m = 1
#    # if we are on the last year, end at e_m
#    if y_i == endyear:
#        e_m = endmonth+1
#    else:
#        e_m = 13
#    for m_i in range(s_m,e_m):
#        roms_files = sorted(glob.glob(roms_path+'l2_scb_avg.Y'+str(y_i)+'M'+'%02d'%m_i+'D*.nc'))
#        for f_i in range(len(roms_files)):
#            print(roms_files[f_i])
#            romsnc = Dataset(roms_files[f_i],'r')
#            romstemp = np.squeeze(romsnc['temp'])
#            z_r = rd.get_zr_zeta(romsnc,gridnc)
#            z_r[z_r>1E10] = np.nan
#            for l_i in range(len(isites)):
#                roms_arr[f_i,l_i,:] = romstemp[:,jsites[l_i],isites[l_i]]
#                roms_depths[f_i,l_i,:] = z_r[:,jsites[l_i],isites[l_i]]
#
#np.save('roms_temp_2000_2008.npy',roms_arr)
#np.save('roms_depths_2000_2008.npy',roms_depths)
        
roms_temp = np.load('roms_temp_2000_2008.npy')
roms_depths = np.load('roms_depths_2000_2008.npy')

pltdt = num2date(np.arange(roms_temp.shape[0]),'days since 2000-10-01',only_use_cftime_datetimes=False,only_use_python_datetimes=True)


c_map = 'bwr'

pltdt = np.tile(pltdt,(roms_depths.shape[2],1)).T

fig,ax = plt.subplots(1,1,figsize=[15,7])
#ax.pcolor(pltdt,np.ma.masked_invalid(roms_depths[:,0,:]),np.ma.masked_invalid(roms_temp[:,0,:]),cmap=c_map,vmin=10,vmax=20)
ax.pcolor(pltdt,roms_depths[:,0,:],roms_temp[:,0,:],cmap=c_map,vmin=5,vmax=20)

