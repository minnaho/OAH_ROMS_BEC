###################################################################
# read bight 13 and literature  data net primary production and nitrification
# Jun 2020
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
nit_df = pd.read_excel(rate_name,sheet_name='Nitrification and nut uptake')
gro_df = pd.read_excel(rate_name,sheet_name='growth and grazing')
npp_df = pd.read_excel(rate_name,sheet_name='Primary Production')

# grid data
grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
nc_grid = Dataset(grid_path,'r')

lon_nc = nc_grid.variables['lon_rho'][:,:]
lat_nc = nc_grid.variables['lat_rho'][:,:]
mask_nc = nc_grid.variables['mask_rho'][:,:]

# choose between what lat/lon
# L2 domain 
lat_min = np.min(lat_nc)
lat_max = np.max(lat_nc)
lon_min = np.min(lon_nc)
lon_max = np.max(lon_nc)


#################
# primary production: mg/m2/day
####################
# conv mg C/m2/day to g C/m2/y
npp_conv = 365./1000
bight_npp = np.array(npp_df['IntegratedPrimaryProduction'])
print('mean bight npp g C/m2/y: ',np.nanmean(bight_npp)*npp_conv)
print('max bight npp  g C/m2/y: ',np.nanmax(bight_npp)*npp_conv)
print('min bight npp  g C/m2/y: ',np.nanmin(bight_npp)*npp_conv)

#####################
# nitrification: units nmol/L day
#####################
# convert nmol/L/day to mmol/m3/s
nit_conv = (1./86400)*(1./1000)

r_lat = np.array(nit_df['Lat'])
r_lon = np.array(nit_df['Lon'])

# bight data ends at 127
b_en = 127

# find values within Bight
nit_lat_ind_bight = np.where((r_lat[:b_en+1]>lat_min) & (r_lat[:b_en+1]<lat_max))[0]
nit_lon_ind_bight = np.where((r_lon[:b_en+1]>lon_min) & (r_lon[:b_en+1]<lon_max))[0]

nit_lat_ind_lit   = np.where((r_lat[b_en+1:]>lat_min) & (r_lat[b_en+1:]<lat_max))[0]
nit_lon_ind_lit   = np.where((r_lon[b_en+1:]>lon_min) & (r_lon[b_en+1:]<lon_max))[0]

nit_loc_ind_bight = np.asarray((list(set(nit_lat_ind_bight).intersection(nit_lon_ind_bight))))
nit_loc_ind_lit = np.array(sorted(np.asarray((list(set(nit_lat_ind_lit).intersection(nit_lon_ind_lit))))))

nit_bight = np.array(nit_df['NitrRate'][:b_en+1][nit_loc_ind_bight])
nit_lit   = np.array(nit_df['NitrRate'][b_en+1:][nit_loc_ind_lit])

print('mean nitrification bight mmol/m3/s: ',np.nanmean(nit_bight)*nit_conv)
print('max  nitrification bight mmol/m3/s: ',np.nanmax(nit_bight)*nit_conv)
print('min  nitrification bight mmol/m3/s: ',np.nanmin(nit_bight[np.where(nit_bight>0)[0]])*nit_conv)

print('mean nitrification literature mmol/m3/s: ',np.nanmean(nit_lit)*nit_conv)
print('max  nitrification literature mmol/m3/s: ',np.nanmax(nit_lit)*nit_conv)
print('min  nitrification literature mmol/m3/s: ',np.nanmin(nit_lit[np.where(nit_lit>0)[0]])*nit_conv)

################
# uptake values only in bight 13
###############
# times 24 to get units in day
# uM N/ug Chl/h = mmol N/mg Chl/h
up_no3 = np.array(nit_df['CHl normalized Max Nitrate Uptake-- Vmax (uM N ug Chl -1 h-1)'][~np.isnan(nit_df['CHl normalized Max Nitrate Uptake-- Vmax (uM N ug Chl -1 h-1)'])])*24

up_nh4 = np.array(nit_df['CHl normalized Max Ammonium Uptake-- Vmax (uM N ug Chl -1 h-1)'][~np.isnan(nit_df['CHl normalized Max Ammonium Uptake-- Vmax (uM N ug Chl -1 h-1)'])])*24

up_N = up_no3+up_nh4

print('mean no3 uptake bight mmol N/mg Chl/day: ',np.nanmean(up_no3))
print('max  no3 uptake bight mmol N/mg Chl/day: ',np.nanmax(up_no3))
print('min  no3 uptake bight mmol N/mg Chl/day: ',np.nanmin(up_no3[np.nonzero(up_no3)[0]]))

print('mean nh4 uptake bight mmol N/mg Chl/day: ',np.nanmean(up_nh4))
print('max  nh4 uptake bight mmol N/mg Chl/day: ',np.nanmax(up_nh4))
print('min  nh4 uptake bight mmol N/mg Chl/day: ',np.nanmin(up_nh4[np.nonzero(up_nh4)[0]]))

####################
# growth: 1/day
###################
phyto_grw0 = np.array(gro_df['phytoplankton growth'][9:][~np.isnan(gro_df['phytoplankton growth'][9:])])
phyto_grw1 = np.array(gro_df['meanphytogrowth'][~np.isnan(gro_df['meanphytogrowth'])])
tot_grw = np.array(list(phyto_grw0)+list(phyto_grw1))

print('mean total phytoplankton growth lit $\mu$ 1/day: ',np.nanmean(tot_grw))
print('max  total phytoplankton growth lit $\mu$ 1/day: ',np.nanmax(tot_grw))
print('min  total phytoplankton growth lit $\mu$ 1/day: ',np.nanmin(tot_grw[np.nonzero(tot_grw)[0]]))

micro_grz0 = np.array(gro_df['depthintegratedmicrozooplanktongrazing'][~np.isnan(gro_df['depthintegratedmicrozooplanktongrazing'])])
micro_grz1 = np.array(gro_df['mircozooplanktongrazing'][~np.isnan(gro_df['mircozooplanktongrazing'])])
meso_grz = np.array(gro_df['depthintegratedmesozooplanktongrazing'][~np.isnan(gro_df['depthintegratedmesozooplanktongrazing'])])
tot_grz = np.array(list(micro_grz0)+list(micro_grz1)+list(meso_grz))

print('mean literature graze 1/day: ',np.nanmean(tot_grz))
print('max  literature graze 1/day: ',np.nanmax(tot_grz))
print('min  literature graze 1/day: ',np.nanmin(tot_grz[np.nonzero(tot_grz)[0]]))
