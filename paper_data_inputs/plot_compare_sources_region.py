import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import scipy.io

fig_path = './figs/'
# data paths
major_path = '/data/project1/minnaho/river_data/south_coast_rivers_10_years_no_watershed_new.nc'
minor_path = '/data/project1/minnaho/river_data/south_coast_rivers_24_years_new.nc'

potw_major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
potw_minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc'

atmos_path = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
setting = 'bight'

# define boxes of each region 
#   SB =  above SM, SM = SMB, SP = bottom SMB to Huntington Beach
#   OC =  Huntington to Oceanside, SD = Oceanside to bottom
#      >SB    SM    SP    OC   SD
lat_sites = [34.05,33.77,33.65,33.2]
lon_sites = [-118.816,-118.39,-117.99,-117.39]

################
# load atmos data
################
if setting == 'bight':
    grid_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/roms_grd.nc'
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/L2_SCB_atmos_deposition.nc'
    atmos_data = Dataset(dataset_name,'r')
    mask_mat = scipy.io.loadmat('../maskt.mat')['maskt'] # mask that is first 0-15km offshore
    m2_to_hectare = 10000

    grid_nc = Dataset(grid_path,'r')
    lat_nc = np.array(grid_nc.variables['lat_rho'])
    lon_nc = np.array(grid_nc.variables['lon_rho'])
    mask_nc = np.array(grid_nc.variables['mask_rho'])

    oxn  = np.array(atmos_data.variables['NH4'])*mask_mat*m2_to_hectare
    redn = np.array(atmos_data.variables['NO3'])*mask_mat*m2_to_hectare
    alk  = np.array(atmos_data.variables['alk'])*mask_mat*m2_to_hectare
    fe   = np.array(atmos_data.variables['fe'])*mask_mat*m2_to_hectare

if setting == 'cal':
    dataset_name = '/data/project1/minnaho/atmos_deposition_data/atmos_deposition_CMAQ_2002_2012.nc'
    atmos_data = Dataset(dataset_name,'r')

    lat_nc = np.array(atmos_data.variables['latitude'])
    lon_nc = np.array(atmos_data.variables['longitude'])

    oxn  = atmos_data.variables['oxidized_nitrogen']
    redn = atmos_data.variables['reduced_nitrogen']
    alk  = atmos_data.variables['alkalinity']
    fe   = atmos_data.variables['iron']


# load per season (add up each 3 months in season) then sum over entire region 
if setting == 'bight':
    nsites = len(lon_sites)
    x_sites = []
    y_sites = []
    for s in range(nsites):
        min_1D = np.abs( (lat_nc - lat_sites[s])**2 + (lon_nc - lon_sites[s])**2)
        y_site, x_site = np.unravel_index(min_1D.argmin(), min_1D.shape)
        x_sites.append(x_site)
        y_sites.append(y_site)

    oxn_win0_sb = np.array(oxn[11,y_sites[0]:mask_nc.shape[0],:]+oxn[0,y_sites[0]:mask_nc.shape[0],:]+oxn[1,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    oxn_win0_sm = np.array(oxn[11,y_sites[1]:y_sites[0],:]+oxn[0,y_sites[1]:y_sites[0],:]+oxn[1,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    oxn_win0_sp = np.array(oxn[11,y_sites[2]:y_sites[1],:]+oxn[0,y_sites[2]:y_sites[1],:]+oxn[1,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    oxn_win0_oc = np.array(oxn[11,y_sites[3]:y_sites[2],:]+oxn[0,y_sites[3]:y_sites[2],:]+oxn[1,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    oxn_win0_sd = np.array(oxn[11,0:y_sites[3],:]+oxn[0,0:y_sites[3],:]+oxn[1,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    oxn_win0_sb[oxn_win0_sb==0] = np.nan
    oxn_win0_sm[oxn_win0_sm==0] = np.nan
    oxn_win0_sp[oxn_win0_sp==0] = np.nan
    oxn_win0_oc[oxn_win0_oc==0] = np.nan
    oxn_win0_sd[oxn_win0_sd==0] = np.nan
    oxn_winter_sb = np.nansum(oxn_win0_sb)
    oxn_winter_sm = np.nansum(oxn_win0_sm)
    oxn_winter_sp = np.nansum(oxn_win0_sp)
    oxn_winter_oc = np.nansum(oxn_win0_oc)
    oxn_winter_sd = np.nansum(oxn_win0_sd)

    oxn_spr0_sb = np.array(oxn[2,y_sites[0]:mask_nc.shape[0],:]+oxn[3,y_sites[0]:mask_nc.shape[0],:]+oxn[4,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    oxn_spr0_sm = np.array(oxn[2,y_sites[1]:y_sites[0],:]+oxn[3,y_sites[1]:y_sites[0],:]+oxn[4,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    oxn_spr0_sp = np.array(oxn[2,y_sites[2]:y_sites[1],:]+oxn[3,y_sites[2]:y_sites[1],:]+oxn[4,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    oxn_spr0_oc = np.array(oxn[2,y_sites[3]:y_sites[2],:]+oxn[3,y_sites[3]:y_sites[2],:]+oxn[4,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    oxn_spr0_sd = np.array(oxn[2,0:y_sites[3],:]+oxn[3,0:y_sites[3],:]+oxn[4,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    oxn_spr0_sb[oxn_spr0_sb==0] = np.nan
    oxn_spr0_sm[oxn_spr0_sm==0] = np.nan
    oxn_spr0_sp[oxn_spr0_sp==0] = np.nan
    oxn_spr0_oc[oxn_spr0_oc==0] = np.nan
    oxn_spr0_sd[oxn_spr0_sd==0] = np.nan
    oxn_spring_sb = np.nansum(oxn_spr0_sb)
    oxn_spring_sm = np.nansum(oxn_spr0_sm)
    oxn_spring_sp = np.nansum(oxn_spr0_sp)
    oxn_spring_oc = np.nansum(oxn_spr0_oc)
    oxn_spring_sd = np.nansum(oxn_spr0_sd)

    oxn_sum0_sb = np.array(oxn[5,y_sites[0]:mask_nc.shape[0],:]+oxn[6,y_sites[0]:mask_nc.shape[0],:]+oxn[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    oxn_sum0_sm = np.array(oxn[5,y_sites[1]:y_sites[0],:]+oxn[6,y_sites[1]:y_sites[0],:]+oxn[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    oxn_sum0_sp = np.array(oxn[5,y_sites[2]:y_sites[1],:]+oxn[6,y_sites[2]:y_sites[1],:]+oxn[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    oxn_sum0_oc = np.array(oxn[5,y_sites[3]:y_sites[2],:]+oxn[6,y_sites[3]:y_sites[2],:]+oxn[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    oxn_sum0_sd = np.array(oxn[5,0:y_sites[3],:]+oxn[6,0:y_sites[3],:]+oxn[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    oxn_sum0_sb[oxn_sum0_sb==0] = np.nan
    oxn_sum0_sm[oxn_sum0_sm==0] = np.nan
    oxn_sum0_sp[oxn_sum0_sp==0] = np.nan
    oxn_sum0_oc[oxn_sum0_oc==0] = np.nan
    oxn_sum0_sd[oxn_sum0_sd==0] = np.nan
    oxn_summer_sb = np.nansum(oxn_sum0_sb)
    oxn_summer_sm = np.nansum(oxn_sum0_sm)
    oxn_summer_sp = np.nansum(oxn_sum0_sp)
    oxn_summer_oc = np.nansum(oxn_sum0_oc)
    oxn_summer_sd = np.nansum(oxn_sum0_sd)

    oxn_aut0_sb = np.array(oxn[5,y_sites[0]:mask_nc.shape[0],:]+oxn[6,y_sites[0]:mask_nc.shape[0],:]+oxn[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    oxn_aut0_sm = np.array(oxn[5,y_sites[1]:y_sites[0],:]+oxn[6,y_sites[1]:y_sites[0],:]+oxn[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    oxn_aut0_sp = np.array(oxn[5,y_sites[2]:y_sites[1],:]+oxn[6,y_sites[2]:y_sites[1],:]+oxn[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    oxn_aut0_oc = np.array(oxn[5,y_sites[3]:y_sites[2],:]+oxn[6,y_sites[3]:y_sites[2],:]+oxn[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    oxn_aut0_sd = np.array(oxn[5,0:y_sites[3],:]+oxn[6,0:y_sites[3],:]+oxn[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    oxn_aut0_sb[oxn_aut0_sb==0] = np.nan
    oxn_aut0_sm[oxn_aut0_sm==0] = np.nan
    oxn_aut0_sp[oxn_aut0_sp==0] = np.nan
    oxn_aut0_oc[oxn_aut0_oc==0] = np.nan
    oxn_aut0_sd[oxn_aut0_sd==0] = np.nan
    oxn_autumn_sb = np.nansum(oxn_aut0_sb)
    oxn_autumn_sm = np.nansum(oxn_aut0_sm)
    oxn_autumn_sp = np.nansum(oxn_aut0_sp)
    oxn_autumn_oc = np.nansum(oxn_aut0_oc)
    oxn_autumn_sd = np.nansum(oxn_aut0_sd)

    redn_win0_sb = np.array(redn[11,y_sites[0]:mask_nc.shape[0],:]+redn[0,y_sites[0]:mask_nc.shape[0],:]+redn[1,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    redn_win0_sm = np.array(redn[11,y_sites[1]:y_sites[0],:]+redn[0,y_sites[1]:y_sites[0],:]+redn[1,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    redn_win0_sp = np.array(redn[11,y_sites[2]:y_sites[1],:]+redn[0,y_sites[2]:y_sites[1],:]+redn[1,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    redn_win0_oc = np.array(redn[11,y_sites[3]:y_sites[2],:]+redn[0,y_sites[3]:y_sites[2],:]+redn[1,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    redn_win0_sd = np.array(redn[11,0:y_sites[3],:]+redn[0,0:y_sites[3],:]+redn[1,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    redn_win0_sb[redn_win0_sb==0] = np.nan
    redn_win0_sm[redn_win0_sm==0] = np.nan
    redn_win0_sp[redn_win0_sp==0] = np.nan
    redn_win0_oc[redn_win0_oc==0] = np.nan
    redn_win0_sd[redn_win0_sd==0] = np.nan
    redn_winter_sb = np.nansum(redn_win0_sb)
    redn_winter_sm = np.nansum(redn_win0_sm)
    redn_winter_sp = np.nansum(redn_win0_sp)
    redn_winter_oc = np.nansum(redn_win0_oc)
    redn_winter_sd = np.nansum(redn_win0_sd)

    redn_spr0_sb = np.array(redn[2,y_sites[0]:mask_nc.shape[0],:]+redn[3,y_sites[0]:mask_nc.shape[0],:]+redn[4,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    redn_spr0_sm = np.array(redn[2,y_sites[1]:y_sites[0],:]+redn[3,y_sites[1]:y_sites[0],:]+redn[4,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    redn_spr0_sp = np.array(redn[2,y_sites[2]:y_sites[1],:]+redn[3,y_sites[2]:y_sites[1],:]+redn[4,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    redn_spr0_oc = np.array(redn[2,y_sites[3]:y_sites[2],:]+redn[3,y_sites[3]:y_sites[2],:]+redn[4,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    redn_spr0_sd = np.array(redn[2,0:y_sites[3],:]+redn[3,0:y_sites[3],:]+redn[4,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    redn_spr0_sb[redn_spr0_sb==0] = np.nan
    redn_spr0_sm[redn_spr0_sm==0] = np.nan
    redn_spr0_sp[redn_spr0_sp==0] = np.nan
    redn_spr0_oc[redn_spr0_oc==0] = np.nan
    redn_spr0_sd[redn_spr0_sd==0] = np.nan
    redn_spring_sb = np.nansum(redn_spr0_sb)
    redn_spring_sm = np.nansum(redn_spr0_sm)
    redn_spring_sp = np.nansum(redn_spr0_sp)
    redn_spring_oc = np.nansum(redn_spr0_oc)
    redn_spring_sd = np.nansum(redn_spr0_sd)

    redn_sum0_sb = np.array(redn[5,y_sites[0]:mask_nc.shape[0],:]+redn[6,y_sites[0]:mask_nc.shape[0],:]+redn[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    redn_sum0_sm = np.array(redn[5,y_sites[1]:y_sites[0],:]+redn[6,y_sites[1]:y_sites[0],:]+redn[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    redn_sum0_sp = np.array(redn[5,y_sites[2]:y_sites[1],:]+redn[6,y_sites[2]:y_sites[1],:]+redn[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    redn_sum0_oc = np.array(redn[5,y_sites[3]:y_sites[2],:]+redn[6,y_sites[3]:y_sites[2],:]+redn[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    redn_sum0_sd = np.array(redn[5,0:y_sites[3],:]+redn[6,0:y_sites[3],:]+redn[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    redn_sum0_sb[redn_sum0_sb==0] = np.nan
    redn_sum0_sm[redn_sum0_sm==0] = np.nan
    redn_sum0_sp[redn_sum0_sp==0] = np.nan
    redn_sum0_oc[redn_sum0_oc==0] = np.nan
    redn_sum0_sd[redn_sum0_sd==0] = np.nan
    redn_summer_sb = np.nansum(redn_sum0_sb)
    redn_summer_sm = np.nansum(redn_sum0_sm)
    redn_summer_sp = np.nansum(redn_sum0_sp)
    redn_summer_oc = np.nansum(redn_sum0_oc)
    redn_summer_sd = np.nansum(redn_sum0_sd)

    redn_aut0_sb = np.array(redn[5,y_sites[0]:mask_nc.shape[0],:]+redn[6,y_sites[0]:mask_nc.shape[0],:]+redn[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    redn_aut0_sm = np.array(redn[5,y_sites[1]:y_sites[0],:]+redn[6,y_sites[1]:y_sites[0],:]+redn[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    redn_aut0_sp = np.array(redn[5,y_sites[2]:y_sites[1],:]+redn[6,y_sites[2]:y_sites[1],:]+redn[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    redn_aut0_oc = np.array(redn[5,y_sites[3]:y_sites[2],:]+redn[6,y_sites[3]:y_sites[2],:]+redn[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    redn_aut0_sd = np.array(redn[5,0:y_sites[3],:]+redn[6,0:y_sites[3],:]+redn[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    redn_aut0_sb[redn_aut0_sb==0] = np.nan
    redn_aut0_sm[redn_aut0_sm==0] = np.nan
    redn_aut0_sp[redn_aut0_sp==0] = np.nan
    redn_aut0_oc[redn_aut0_oc==0] = np.nan
    redn_aut0_sd[redn_aut0_sd==0] = np.nan
    redn_autumn_sb = np.nansum(redn_aut0_sb)
    redn_autumn_sm = np.nansum(redn_aut0_sm)
    redn_autumn_sp = np.nansum(redn_aut0_sp)
    redn_autumn_oc = np.nansum(redn_aut0_oc)
    redn_autumn_sd = np.nansum(redn_aut0_sd)

    alk_win0_sb = np.array(alk[11,y_sites[0]:mask_nc.shape[0],:]+alk[0,y_sites[0]:mask_nc.shape[0],:]+alk[1,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    alk_win0_sm = np.array(alk[11,y_sites[1]:y_sites[0],:]+alk[0,y_sites[1]:y_sites[0],:]+alk[1,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    alk_win0_sp = np.array(alk[11,y_sites[2]:y_sites[1],:]+alk[0,y_sites[2]:y_sites[1],:]+alk[1,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    alk_win0_oc = np.array(alk[11,y_sites[3]:y_sites[2],:]+alk[0,y_sites[3]:y_sites[2],:]+alk[1,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    alk_win0_sd = np.array(alk[11,0:y_sites[3],:]+alk[0,0:y_sites[3],:]+alk[1,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    alk_win0_sb[alk_win0_sb==0] = np.nan
    alk_win0_sm[alk_win0_sm==0] = np.nan
    alk_win0_sp[alk_win0_sp==0] = np.nan
    alk_win0_oc[alk_win0_oc==0] = np.nan
    alk_win0_sd[alk_win0_sd==0] = np.nan
    alk_winter_sb = np.nansum(alk_win0_sb)
    alk_winter_sm = np.nansum(alk_win0_sm)
    alk_winter_sp = np.nansum(alk_win0_sp)
    alk_winter_oc = np.nansum(alk_win0_oc)
    alk_winter_sd = np.nansum(alk_win0_sd)

    alk_spr0_sb = np.array(alk[2,y_sites[0]:mask_nc.shape[0],:]+alk[3,y_sites[0]:mask_nc.shape[0],:]+alk[4,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    alk_spr0_sm = np.array(alk[2,y_sites[1]:y_sites[0],:]+alk[3,y_sites[1]:y_sites[0],:]+alk[4,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    alk_spr0_sp = np.array(alk[2,y_sites[2]:y_sites[1],:]+alk[3,y_sites[2]:y_sites[1],:]+alk[4,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    alk_spr0_oc = np.array(alk[2,y_sites[3]:y_sites[2],:]+alk[3,y_sites[3]:y_sites[2],:]+alk[4,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    alk_spr0_sd = np.array(alk[2,0:y_sites[3],:]+alk[3,0:y_sites[3],:]+alk[4,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    alk_spr0_sb[alk_spr0_sb==0] = np.nan
    alk_spr0_sm[alk_spr0_sm==0] = np.nan
    alk_spr0_sp[alk_spr0_sp==0] = np.nan
    alk_spr0_oc[alk_spr0_oc==0] = np.nan
    alk_spr0_sd[alk_spr0_sd==0] = np.nan
    alk_spring_sb = np.nansum(alk_spr0_sb)
    alk_spring_sm = np.nansum(alk_spr0_sm)
    alk_spring_sp = np.nansum(alk_spr0_sp)
    alk_spring_oc = np.nansum(alk_spr0_oc)
    alk_spring_sd = np.nansum(alk_spr0_sd)

    alk_sum0_sb = np.array(alk[5,y_sites[0]:mask_nc.shape[0],:]+alk[6,y_sites[0]:mask_nc.shape[0],:]+alk[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    alk_sum0_sm = np.array(alk[5,y_sites[1]:y_sites[0],:]+alk[6,y_sites[1]:y_sites[0],:]+alk[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    alk_sum0_sp = np.array(alk[5,y_sites[2]:y_sites[1],:]+alk[6,y_sites[2]:y_sites[1],:]+alk[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    alk_sum0_oc = np.array(alk[5,y_sites[3]:y_sites[2],:]+alk[6,y_sites[3]:y_sites[2],:]+alk[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    alk_sum0_sd = np.array(alk[5,0:y_sites[3],:]+alk[6,0:y_sites[3],:]+alk[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    alk_sum0_sb[alk_sum0_sb==0] = np.nan
    alk_sum0_sm[alk_sum0_sm==0] = np.nan
    alk_sum0_sp[alk_sum0_sp==0] = np.nan
    alk_sum0_oc[alk_sum0_oc==0] = np.nan
    alk_sum0_sd[alk_sum0_sd==0] = np.nan
    alk_summer_sb = np.nansum(alk_sum0_sb)
    alk_summer_sm = np.nansum(alk_sum0_sm)
    alk_summer_sp = np.nansum(alk_sum0_sp)
    alk_summer_oc = np.nansum(alk_sum0_oc)
    alk_summer_sd = np.nansum(alk_sum0_sd)

    alk_aut0_sb = np.array(alk[5,y_sites[0]:mask_nc.shape[0],:]+alk[6,y_sites[0]:mask_nc.shape[0],:]+alk[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    alk_aut0_sm = np.array(alk[5,y_sites[1]:y_sites[0],:]+alk[6,y_sites[1]:y_sites[0],:]+alk[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    alk_aut0_sp = np.array(alk[5,y_sites[2]:y_sites[1],:]+alk[6,y_sites[2]:y_sites[1],:]+alk[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    alk_aut0_oc = np.array(alk[5,y_sites[3]:y_sites[2],:]+alk[6,y_sites[3]:y_sites[2],:]+alk[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    alk_aut0_sd = np.array(alk[5,0:y_sites[3],:]+alk[6,0:y_sites[3],:]+alk[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    alk_aut0_sb[alk_aut0_sb==0] = np.nan
    alk_aut0_sm[alk_aut0_sm==0] = np.nan
    alk_aut0_sp[alk_aut0_sp==0] = np.nan
    alk_aut0_oc[alk_aut0_oc==0] = np.nan
    alk_aut0_sd[alk_aut0_sd==0] = np.nan
    alk_autumn_sb = np.nansum(alk_aut0_sb)
    alk_autumn_sm = np.nansum(alk_aut0_sm)
    alk_autumn_sp = np.nansum(alk_aut0_sp)
    alk_autumn_oc = np.nansum(alk_aut0_oc)
    alk_autumn_sd = np.nansum(alk_aut0_sd)

    fe_win0_sb = np.array(fe[11,y_sites[0]:mask_nc.shape[0],:]+fe[0,y_sites[0]:mask_nc.shape[0],:]+fe[1,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    fe_win0_sm = np.array(fe[11,y_sites[1]:y_sites[0],:]+fe[0,y_sites[1]:y_sites[0],:]+fe[1,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    fe_win0_sp = np.array(fe[11,y_sites[2]:y_sites[1],:]+fe[0,y_sites[2]:y_sites[1],:]+fe[1,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    fe_win0_oc = np.array(fe[11,y_sites[3]:y_sites[2],:]+fe[0,y_sites[3]:y_sites[2],:]+fe[1,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    fe_win0_sd = np.array(fe[11,0:y_sites[3],:]+fe[0,0:y_sites[3],:]+fe[1,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    fe_win0_sb[fe_win0_sb==0] = np.nan
    fe_win0_sm[fe_win0_sm==0] = np.nan
    fe_win0_sp[fe_win0_sp==0] = np.nan
    fe_win0_oc[fe_win0_oc==0] = np.nan
    fe_win0_sd[fe_win0_sd==0] = np.nan
    fe_winter_sb = np.nansum(fe_win0_sb)
    fe_winter_sm = np.nansum(fe_win0_sm)
    fe_winter_sp = np.nansum(fe_win0_sp)
    fe_winter_oc = np.nansum(fe_win0_oc)
    fe_winter_sd = np.nansum(fe_win0_sd)

    fe_spr0_sb = np.array(fe[2,y_sites[0]:mask_nc.shape[0],:]+fe[3,y_sites[0]:mask_nc.shape[0],:]+fe[4,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    fe_spr0_sm = np.array(fe[2,y_sites[1]:y_sites[0],:]+fe[3,y_sites[1]:y_sites[0],:]+fe[4,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    fe_spr0_sp = np.array(fe[2,y_sites[2]:y_sites[1],:]+fe[3,y_sites[2]:y_sites[1],:]+fe[4,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    fe_spr0_oc = np.array(fe[2,y_sites[3]:y_sites[2],:]+fe[3,y_sites[3]:y_sites[2],:]+fe[4,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    fe_spr0_sd = np.array(fe[2,0:y_sites[3],:]+fe[3,0:y_sites[3],:]+fe[4,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    fe_spr0_sb[fe_spr0_sb==0] = np.nan
    fe_spr0_sm[fe_spr0_sm==0] = np.nan
    fe_spr0_sp[fe_spr0_sp==0] = np.nan
    fe_spr0_oc[fe_spr0_oc==0] = np.nan
    fe_spr0_sd[fe_spr0_sd==0] = np.nan
    fe_spring_sb = np.nansum(fe_spr0_sb)
    fe_spring_sm = np.nansum(fe_spr0_sm)
    fe_spring_sp = np.nansum(fe_spr0_sp)
    fe_spring_oc = np.nansum(fe_spr0_oc)
    fe_spring_sd = np.nansum(fe_spr0_sd)

    fe_sum0_sb = np.array(fe[5,y_sites[0]:mask_nc.shape[0],:]+fe[6,y_sites[0]:mask_nc.shape[0],:]+fe[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    fe_sum0_sm = np.array(fe[5,y_sites[1]:y_sites[0],:]+fe[6,y_sites[1]:y_sites[0],:]+fe[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    fe_sum0_sp = np.array(fe[5,y_sites[2]:y_sites[1],:]+fe[6,y_sites[2]:y_sites[1],:]+fe[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    fe_sum0_oc = np.array(fe[5,y_sites[3]:y_sites[2],:]+fe[6,y_sites[3]:y_sites[2],:]+fe[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    fe_sum0_sd = np.array(fe[5,0:y_sites[3],:]+fe[6,0:y_sites[3],:]+fe[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    fe_sum0_sb[fe_sum0_sb==0] = np.nan
    fe_sum0_sm[fe_sum0_sm==0] = np.nan
    fe_sum0_sp[fe_sum0_sp==0] = np.nan
    fe_sum0_oc[fe_sum0_oc==0] = np.nan
    fe_sum0_sd[fe_sum0_sd==0] = np.nan
    fe_summer_sb = np.nansum(fe_sum0_sb)
    fe_summer_sm = np.nansum(fe_sum0_sm)
    fe_summer_sp = np.nansum(fe_sum0_sp)
    fe_summer_oc = np.nansum(fe_sum0_oc)
    fe_summer_sd = np.nansum(fe_sum0_sd)

    fe_aut0_sb = np.array(fe[5,y_sites[0]:mask_nc.shape[0],:]+fe[6,y_sites[0]:mask_nc.shape[0],:]+fe[7,y_sites[0]:mask_nc.shape[0],:])*mask_nc[y_sites[0]:mask_nc.shape[0],:]
    fe_aut0_sm = np.array(fe[5,y_sites[1]:y_sites[0],:]+fe[6,y_sites[1]:y_sites[0],:]+fe[8,y_sites[1]:y_sites[0],:])*mask_nc[y_sites[1]:y_sites[0],:]
    fe_aut0_sp = np.array(fe[5,y_sites[2]:y_sites[1],:]+fe[6,y_sites[2]:y_sites[1],:]+fe[8,y_sites[2]:y_sites[1],:])*mask_nc[y_sites[2]:y_sites[1],:]
    fe_aut0_oc = np.array(fe[5,y_sites[3]:y_sites[2],:]+fe[6,y_sites[3]:y_sites[2],:]+fe[8,y_sites[3]:y_sites[2],:])*mask_nc[y_sites[3]:y_sites[2],:]
    fe_aut0_sd = np.array(fe[5,0:y_sites[3],:]+fe[6,0:y_sites[3],:]+fe[7,0:y_sites[3],:])*mask_nc[0:y_sites[3],:]
    fe_aut0_sb[fe_aut0_sb==0] = np.nan
    fe_aut0_sm[fe_aut0_sm==0] = np.nan
    fe_aut0_sp[fe_aut0_sp==0] = np.nan
    fe_aut0_oc[fe_aut0_oc==0] = np.nan
    fe_aut0_sd[fe_aut0_sd==0] = np.nan
    fe_autumn_sb = np.nansum(fe_aut0_sb)
    fe_autumn_sm = np.nansum(fe_aut0_sm)
    fe_autumn_sp = np.nansum(fe_aut0_sp)
    fe_autumn_oc = np.nansum(fe_aut0_oc)
    fe_autumn_sd = np.nansum(fe_aut0_sd)

    oxn_season_sb  = np.array([oxn_winter_sb,oxn_spring_sb,oxn_summer_sb,oxn_autumn_sb])
    oxn_season_sm  = np.array([oxn_winter_sm,oxn_spring_sm,oxn_summer_sm,oxn_autumn_sm])
    oxn_season_sp  = np.array([oxn_winter_sp,oxn_spring_sp,oxn_summer_sp,oxn_autumn_sp])
    oxn_season_oc  = np.array([oxn_winter_oc,oxn_spring_oc,oxn_summer_oc,oxn_autumn_oc])
    oxn_season_sd  = np.array([oxn_winter_sd,oxn_spring_sd,oxn_summer_sd,oxn_autumn_sd])

    redn_season_sb  = np.array([redn_winter_sb,redn_spring_sb,redn_summer_sb,redn_autumn_sb])
    redn_season_sm  = np.array([redn_winter_sm,redn_spring_sm,redn_summer_sm,redn_autumn_sm])
    redn_season_sp  = np.array([redn_winter_sp,redn_spring_sp,redn_summer_sp,redn_autumn_sp])
    redn_season_oc  = np.array([redn_winter_oc,redn_spring_oc,redn_summer_oc,redn_autumn_oc])
    redn_season_sd  = np.array([redn_winter_sd,redn_spring_sd,redn_summer_sd,redn_autumn_sd])

    alk_season_sb  = np.array([alk_winter_sb,alk_spring_sb,alk_summer_sb,alk_autumn_sb])
    alk_season_sm  = np.array([alk_winter_sm,alk_spring_sm,alk_summer_sm,alk_autumn_sm])
    alk_season_sp  = np.array([alk_winter_sp,alk_spring_sp,alk_summer_sp,alk_autumn_sp])
    alk_season_oc  = np.array([alk_winter_oc,alk_spring_oc,alk_summer_oc,alk_autumn_oc])
    alk_season_sd  = np.array([alk_winter_sd,alk_spring_sd,alk_summer_sd,alk_autumn_sd])

    fe_season_sb  = np.array([fe_winter_sb,fe_spring_sb,fe_summer_sb,fe_autumn_sb])
    fe_season_sm  = np.array([fe_winter_sm,fe_spring_sm,fe_summer_sm,fe_autumn_sm])
    fe_season_sp  = np.array([fe_winter_sp,fe_spring_sp,fe_summer_sp,fe_autumn_sp])
    fe_season_oc  = np.array([fe_winter_oc,fe_spring_oc,fe_summer_oc,fe_autumn_oc])
    fe_season_sd  = np.array([fe_winter_sd,fe_spring_sd,fe_summer_sd,fe_autumn_sd])
    
    # yearly input
    atmos_sb = np.sum(oxn_season_sb) + np.sum(redn_season_sb)
    atmos_sm = np.sum(oxn_season_sm) + np.sum(redn_season_sm)
    atmos_sp = np.sum(oxn_season_sp) + np.sum(redn_season_sp)
    atmos_oc = np.sum(oxn_season_oc) + np.sum(redn_season_oc)
    atmos_sd = np.sum(oxn_season_sd) + np.sum(redn_season_sd)

if setting == 'cal': 
    oxn_monthly = np.empty((12,oxn.shape[1],oxn.shape[2]))
    for m_i in range(12):
        oxn_monthly[m_i] = np.nanmean(oxn[m_i::12,:,:])
        
        

###############
# river major data (10 yrs)
###############
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

major_lat = np.array(major_nc.variables['latitude'])

# find indices per region
r_ind_10_sb = np.where(major_lat>lat_sites[0])[0]
r_ind_10_sm = np.where((major_lat<lat_sites[0])&(major_lat>lat_sites[1]))[0]
r_ind_10_sp = np.where((major_lat<lat_sites[1])&(major_lat>lat_sites[2]))[0]
r_ind_10_oc = np.where((major_lat<lat_sites[2])&(major_lat>lat_sites[3]))[0]
r_ind_10_sd = np.where(major_lat<lat_sites[3])[0]
r_ind_10 = np.array((r_ind_10_sb,r_ind_10_sm,r_ind_10_sp,r_ind_10_oc,r_ind_10_sd))

major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['ammonium']) # mmol/m3
major_no3 = np.array(major_nc.variables['nitrate']) # mmol/m3
major_po4 = np.array(major_nc.variables['phosphate']) # mmol/m3
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 

major_tn = np.array(major_nc.variables['total_nitrogen']) 

major_flo[major_flo>1E20] = np.nan
major_tn[major_tn>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

##############
# river 24 yrs
##############
minor_nc = Dataset(minor_path,'r')

minor_time = num2date(np.array(minor_nc.variables['time']),minor_nc.variables['time'].units)
minor_lat = np.array(minor_nc.variables['latitude'])
# find indices per region
r_ind_24_sb = np.where(minor_lat>lat_sites[0])[0]
r_ind_24_sm = np.where((minor_lat<lat_sites[0])&(minor_lat>lat_sites[1]))[0]
r_ind_24_sp = np.where((minor_lat<lat_sites[1])&(minor_lat>lat_sites[2]))[0]
r_ind_24_oc = np.where((minor_lat<lat_sites[2])&(minor_lat>lat_sites[3]))[0]
r_ind_24_sd = np.where(minor_lat<lat_sites[3])[0]
r_ind_24 = np.array((r_ind_24_sb,r_ind_24_sm,r_ind_24_sp,r_ind_24_oc,r_ind_24_sd))

# convert real_datetime to datetime
minor_time_l = []
for d_i in range(len(minor_time)):
    minor_time_l.append(minor_time[d_i]+datetime.timedelta(0,1))

minor_time_dt = np.array(minor_time_l)

minor_flo = np.array(minor_nc.variables['flow']) # m3/s
minor_nh4 = np.array(minor_nc.variables['ammonium']) # mmol/m3
minor_no3 = np.array(minor_nc.variables['nitrate']) # mmol/m3
minor_po4 = np.array(minor_nc.variables['phosphate']) # mmol/m3
minor_tn = np.array(minor_nc.variables['total_nitrogen'])

minor_flo[minor_flo>1E20] = np.nan
minor_tn[minor_tn>1E20] = np.nan
minor_po4[minor_po4>1E20] = np.nan

# combine rivers 10 yrs and 24 yrs
# find days at beginning and end  
num_st = major_time_dt[0]-minor_time_dt[0]
num_en = minor_time_dt[-1]-major_time_dt[-1]

a = []
b = []
for m_i in range(minor_flo.shape[1]):
    a.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_tn[num_st.days:-num_en.days,m_i,m_i])
    b.append(minor_flo[num_st.days:-num_en.days,m_i,m_i]*minor_po4[num_st.days:-num_en.days,m_i,m_i])


# a,b shape (24,3650)
# sum up all rivers
minor_fluxn = np.nansum(np.array(a),axis=0)
minor_fluxp = np.nansum(np.array(b),axis=0)
minor_flo_short = np.nansum(np.nansum(minor_flo[num_st.days:-num_en.days,:,:],axis=1),axis=1)

minor_fluxn_sb = np.sum(np.array(a)[r_ind_24[0]],axis=0)
minor_fluxn_sm = np.sum(np.array(a)[r_ind_24[1]],axis=0)
minor_fluxn_sp = np.sum(np.array(a)[r_ind_24[2]],axis=0)
minor_fluxn_oc = np.sum(np.array(a)[r_ind_24[3]],axis=0)
minor_fluxn_sd = np.sum(np.array(a)[r_ind_24[4]],axis=0)
                                                
minor_fluxp_sb = np.sum(np.array(b)[r_ind_24[0]],axis=0)
minor_fluxp_sm = np.sum(np.array(b)[r_ind_24[1]],axis=0)
minor_fluxp_sp = np.sum(np.array(b)[r_ind_24[2]],axis=0)
minor_fluxp_oc = np.sum(np.array(b)[r_ind_24[3]],axis=0)
minor_fluxp_sd = np.sum(np.array(b)[r_ind_24[4]],axis=0)

a = []
b = []
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])
    b.append(major_flo[:,m_i,m_i]*major_po4[:,m_i,m_i])

# sum up all rivers
major_fluxn = np.nansum(np.array(a),axis=0)
major_fluxp = np.nansum(np.array(b),axis=0)
major_flo_sum = np.nansum(np.nansum(major_flo[:,:,:],axis=1),axis=1)

major_fluxn_sb = np.sum(np.array(a)[r_ind_10[0]],axis=0)
major_fluxn_sm = np.sum(np.array(a)[r_ind_10[1]],axis=0)
major_fluxn_sp = np.sum(np.array(a)[r_ind_10[2]],axis=0)
major_fluxn_oc = np.sum(np.array(a)[r_ind_10[3]],axis=0)
major_fluxn_sd = np.sum(np.array(a)[r_ind_10[4]],axis=0)
                                         
major_fluxp_sb = np.sum(np.array(b)[r_ind_10[0]],axis=0)
major_fluxp_sm = np.sum(np.array(b)[r_ind_10[1]],axis=0)
major_fluxp_sp = np.sum(np.array(b)[r_ind_10[2]],axis=0)
major_fluxp_oc = np.sum(np.array(b)[r_ind_10[3]],axis=0)
major_fluxp_sd = np.sum(np.array(b)[r_ind_10[4]],axis=0)

r_fluxn_sb = major_fluxn_sb+minor_fluxn_sb
r_fluxn_sm = major_fluxn_sm+minor_fluxn_sm
r_fluxn_sp = major_fluxn_sp+minor_fluxn_sp
r_fluxn_sd = major_fluxn_sd+minor_fluxn_sd
r_fluxn_oc = major_fluxn_oc+minor_fluxn_oc

r_flo = major_flo_sum+minor_flo_short
r_fluxn = major_fluxn+minor_fluxn
r_fluxp = major_fluxp+minor_fluxp # mmol/s

# find indices for each season
r_1 = []
r_2 = []
r_3 = []
r_4 = []
r_5 = []
r_6 = []
r_7 = []
r_8 = []
r_9 = []
r_10 = []
r_11 = []
r_12 = []
for d_i in range(len(major_time_dt)):
    if major_time_dt[d_i].month == 1:  
        r_1.append(d_i)
    if major_time_dt[d_i].month == 2:  
        r_2.append(d_i)
    if major_time_dt[d_i].month == 3:  
        r_3.append(d_i)
    if major_time_dt[d_i].month == 4:  
        r_4.append(d_i)
    if major_time_dt[d_i].month == 5:  
        r_5.append(d_i)
    if major_time_dt[d_i].month == 6:  
        r_6.append(d_i)
    if major_time_dt[d_i].month == 7:  
        r_7.append(d_i)
    if major_time_dt[d_i].month == 8:  
        r_8.append(d_i)
    if major_time_dt[d_i].month == 9:  
        r_9.append(d_i)
    if major_time_dt[d_i].month == 10:  
        r_10.append(d_i)
    if major_time_dt[d_i].month == 11:  
        r_11.append(d_i)
    if major_time_dt[d_i].month == 12:  
        r_12.append(d_i)

r_months_ind = [r_1,r_2,r_3,r_4,r_5,r_6,r_7,r_8,r_9,r_10,r_11,r_12]

# monthly climatology
r_flo_mon = np.empty((12))
r_n_mon = np.empty((12))
r_p_mon = np.empty((12))
# monthly climatology by region
r_n_mon_sb = np.empty((12))
r_n_mon_sm = np.empty((12))
r_n_mon_sp = np.empty((12))
r_n_mon_oc = np.empty((12))
r_n_mon_sd = np.empty((12))
for r_i in range(len(r_months_ind)):
    r_n_mon[r_i] = np.nanmean(r_fluxn[r_i])
    r_p_mon[r_i] = np.nanmean(r_fluxp[r_i])
    r_flo_mon[r_i] = np.nanmean(r_flo[r_i])
    r_n_mon_sb[r_i] = np.nanmean(r_fluxn_sb[r_i])
    r_n_mon_sm[r_i] = np.nanmean(r_fluxn_sm[r_i])
    r_n_mon_sp[r_i] = np.nanmean(r_fluxn_sp[r_i])
    r_n_mon_sd[r_i] = np.nanmean(r_fluxn_sd[r_i])
    r_n_mon_oc[r_i] = np.nanmean(r_fluxn_oc[r_i])

np.save('river_monthly_flo_all.npy',r_flo_mon)
np.save('river_monthly_nflux_all.npy',r_n_mon)
np.save('river_monthly_pflux_all.npy',r_p_mon)
    
r_season_n = np.array([(r_n_mon[11])+(r_n_mon[1])+(r_n_mon[0]),(r_n_mon[2])+(r_n_mon[3])+(r_n_mon[4]),(r_n_mon[5])+(r_n_mon[6])+(r_n_mon[7]),(r_n_mon[8])+(r_n_mon[9])+(r_n_mon[10])])

r_season_p = np.array([(r_p_mon[11])+(r_p_mon[1])+(r_p_mon[0]),(r_p_mon[2])+(r_p_mon[3])+(r_p_mon[4]),(r_p_mon[5])+(r_p_mon[6])+(r_p_mon[7]),(r_p_mon[8])+(r_p_mon[9])+(r_p_mon[10])])

# yearly flux of n per region
r_sb_yr = np.nansum(r_n_mon_sb)
r_sm_yr = np.nansum(r_n_mon_sm)
r_sp_yr = np.nansum(r_n_mon_sp)
r_sd_yr = np.nansum(r_n_mon_sd)
r_oc_yr = np.nansum(r_n_mon_oc)
   
##################
# potws
##################
potw_ma_nc = Dataset(potw_major_path,'r')
potw_mi_nc = Dataset(potw_minor_path,'r')

major_potw_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_potw_time_l = []
for d_i in range(len(major_potw_time)):
    major_potw_time_l.append(major_potw_time[d_i]+datetime.timedelta(0,1))

major_potw_time_dt = np.array(major_potw_time_l)

major_potw_lat = np.array(potw_ma_nc.variables['latitude'])
minor_potw_lat = np.array(potw_mi_nc.variables['latitude'])

p_ind_ma_sb = np.where(major_potw_lat>lat_sites[0])[0]
p_ind_ma_sm = np.where((major_potw_lat<lat_sites[0])&(major_potw_lat>lat_sites[1]))[0]
p_ind_ma_sp = np.where((major_potw_lat<lat_sites[1])&(major_potw_lat>lat_sites[2]))[0]
p_ind_ma_oc = np.where((major_potw_lat<lat_sites[2])&(major_potw_lat>lat_sites[3]))[0]
p_ind_ma_sd = np.where(major_potw_lat<lat_sites[3])[0]
p_ind_ma = np.array((p_ind_ma_sb,p_ind_ma_sm,p_ind_ma_sp,p_ind_ma_oc,p_ind_ma_sd))

p_ind_mi_sb = np.where(minor_potw_lat>lat_sites[0])[0]
p_ind_mi_sm = np.where((minor_potw_lat<lat_sites[0])&(minor_potw_lat>lat_sites[1]))[0]
p_ind_mi_sp = np.where((minor_potw_lat<lat_sites[1])&(minor_potw_lat>lat_sites[2]))[0]
p_ind_mi_oc = np.where((minor_potw_lat<lat_sites[2])&(minor_potw_lat>lat_sites[3]))[0]
p_ind_mi_sd = np.where(minor_potw_lat<lat_sites[3])[0]
p_ind_mi = np.array((p_ind_mi_sb,p_ind_mi_sm,p_ind_mi_sp,p_ind_mi_oc,p_ind_mi_sd))

major_potw_flo = np.array(potw_ma_nc.variables['flow']) # m3/s
major_potw_nh4 = np.array(potw_ma_nc.variables['NH4']) # mmol/m3
major_potw_no3 = np.array(potw_ma_nc.variables['NO3']) # mmol/m3
major_potw_no2 = np.array(potw_ma_nc.variables['NO2']) # mmol/m3
major_potw_po4 = np.array(potw_ma_nc.variables['PO4']) # mmol/m3

minor_potw_flo = np.array(potw_mi_nc.variables['flow']) # m3/s
minor_potw_nh4 = np.array(potw_mi_nc.variables['NH4']) # mmol/m3
minor_potw_no3 = np.array(potw_mi_nc.variables['NO3']) # mmol/m3
minor_potw_no2 = np.array(potw_mi_nc.variables['NO2']) # mmol/m3
minor_potw_po4 = np.array(potw_mi_nc.variables['PO4']) # mmol/m3

major_potw_tn = major_potw_no3+major_potw_nh4+major_potw_no2

major_potw_flo[major_potw_flo>1E20] = np.nan
major_potw_tn[major_potw_tn>1E20] = np.nan
major_potw_po4[major_potw_po4>1E20] = np.nan

minor_potw_tn = minor_potw_no3+minor_potw_nh4+minor_potw_no2

minor_potw_flo[minor_potw_flo>1E20] = np.nan
minor_potw_tn[minor_potw_tn>1E20] = np.nan
minor_potw_po4[minor_potw_po4>1E20] = np.nan

# loads of all potws
a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_tn[:,m_i,m_i])

major_potw_fluxalln = np.nansum(np.array(a),axis=0)

major_potw_fluxn_sb = np.sum(np.array(a)[p_ind_ma[0]],axis=0)
major_potw_fluxn_sm = np.sum(np.array(a)[p_ind_ma[1]],axis=0)
major_potw_fluxn_sp = np.sum(np.array(a)[p_ind_ma[2]],axis=0)
major_potw_fluxn_oc = np.sum(np.array(a)[p_ind_ma[3]],axis=0)
major_potw_fluxn_sd = np.sum(np.array(a)[p_ind_ma[4]],axis=0)

a = []
for m_i in range(major_potw_flo.shape[1]):
    a.append(major_potw_flo[:,m_i,m_i]*major_potw_po4[:,m_i,m_i])
major_potw_fluxallp = np.nansum(np.array(a),axis=0)

# already in monthly clim
iend_minor = 12
a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_tn[:iend_minor,m_i,m_i])

minor_potw_fluxalln = np.nansum(np.array(a),axis=0)

minor_potw_fluxn_sb = np.sum(np.array(a)[p_ind_mi[0]],axis=0)
minor_potw_fluxn_sm = np.sum(np.array(a)[p_ind_mi[1]],axis=0)
minor_potw_fluxn_sp = np.sum(np.array(a)[p_ind_mi[2]],axis=0)
minor_potw_fluxn_oc = np.sum(np.array(a)[p_ind_mi[3]],axis=0)
minor_potw_fluxn_sd = np.sum(np.array(a)[p_ind_mi[4]],axis=0)

a = []
for m_i in range(minor_potw_flo.shape[1]):
    a.append(minor_potw_flo[:iend_minor,m_i,m_i]*minor_potw_po4[:iend_minor,m_i,m_i])
minor_potw_fluxallp = np.nansum(np.array(a),axis=0)


# find indices for each season
r_potw_1 = []
r_potw_2 = []
r_potw_3 = []
r_potw_4 = []
r_potw_5 = []
r_potw_6 = []
r_potw_7 = []
r_potw_8 = []
r_potw_9 = []
r_potw_10 = []
r_potw_11 = []
r_potw_12 = []
for d_i in range(len(major_potw_time_dt)):
    if major_potw_time_dt[d_i].month == 1:  
        r_potw_1.append(d_i)
    if major_potw_time_dt[d_i].month == 2:  
        r_potw_2.append(d_i)
    if major_potw_time_dt[d_i].month == 3:  
        r_potw_3.append(d_i)
    if major_potw_time_dt[d_i].month == 4:  
        r_potw_4.append(d_i)
    if major_potw_time_dt[d_i].month == 5:  
        r_potw_5.append(d_i)
    if major_potw_time_dt[d_i].month == 6:  
        r_potw_6.append(d_i)
    if major_potw_time_dt[d_i].month == 7:  
        r_potw_7.append(d_i)
    if major_potw_time_dt[d_i].month == 8:  
        r_potw_8.append(d_i)
    if major_potw_time_dt[d_i].month == 9:  
        r_potw_9.append(d_i)
    if major_potw_time_dt[d_i].month == 10:  
        r_potw_10.append(d_i)
    if major_potw_time_dt[d_i].month == 11:  
        r_potw_11.append(d_i)
    if major_potw_time_dt[d_i].month == 12:  
        r_potw_12.append(d_i)


potw_months_ind = [r_potw_1,r_potw_2,r_potw_3,r_potw_4,r_potw_5,r_potw_6,r_potw_7,r_potw_8,r_potw_9,r_potw_10,r_potw_11,r_potw_12]

potw_flo_mon = np.empty((12))
potw_n_mon = np.empty((12))
potw_p_mon = np.empty((12))
# monthly climatology by region
potw_n_mon_sb = np.empty((12))
potw_n_mon_sm = np.empty((12))
potw_n_mon_sp = np.empty((12))
potw_n_mon_oc = np.empty((12))
potw_n_mon_sd = np.empty((12))
for r_i in range(len(potw_months_ind)):
    potw_n_mon[r_i] = np.nanmean(major_potw_fluxalln[r_i])
    potw_p_mon[r_i] = np.nanmean(major_potw_fluxallp[r_i])
    potw_n_mon_sb[r_i] = np.nanmean(major_potw_fluxn_sb[r_i])
    potw_n_mon_sm[r_i] = np.nanmean(major_potw_fluxn_sm[r_i])
    potw_n_mon_sp[r_i] = np.nanmean(major_potw_fluxn_sp[r_i])
    potw_n_mon_sd[r_i] = np.nanmean(major_potw_fluxn_sd[r_i])
    potw_n_mon_oc[r_i] = np.nanmean(major_potw_fluxn_oc[r_i])
    
major_potw_season_n = np.array([(potw_n_mon[11])+(potw_n_mon[1])+(potw_n_mon[0]),(potw_n_mon[2])+(potw_n_mon[3])+(potw_n_mon[4]),(potw_n_mon[5])+(potw_n_mon[6])+(potw_n_mon[7]),(potw_n_mon[8])+(potw_n_mon[9])+(potw_n_mon[10])])

major_potw_season_p = np.array([(potw_p_mon[11])+(potw_p_mon[1])+(potw_p_mon[0]),(potw_p_mon[2])+(potw_p_mon[3])+(potw_p_mon[4]),(potw_p_mon[5])+(potw_p_mon[6])+(potw_p_mon[7]),(potw_p_mon[8])+(potw_p_mon[9])+(potw_p_mon[10])])

all_potw_n_mon = potw_n_mon+minor_potw_fluxalln
all_potw_p_mon = potw_p_mon+minor_potw_fluxallp

all_potw_season_n = np.array([(all_potw_n_mon[11])+(all_potw_n_mon[1])+(all_potw_n_mon[0]),(all_potw_n_mon[2])+(all_potw_n_mon[3])+(all_potw_n_mon[4]),(all_potw_n_mon[5])+(all_potw_n_mon[6])+(all_potw_n_mon[7]),(all_potw_n_mon[8])+(all_potw_n_mon[9])+(all_potw_n_mon[10])])

all_potw_season_p = np.array([(all_potw_p_mon[11])+(all_potw_p_mon[1])+(all_potw_p_mon[0]),(all_potw_p_mon[2])+(all_potw_p_mon[3])+(all_potw_p_mon[4]),(all_potw_p_mon[5])+(all_potw_p_mon[6])+(all_potw_p_mon[7]),(all_potw_p_mon[8])+(all_potw_p_mon[9])+(all_potw_p_mon[10])])

p_fluxn_sb = potw_n_mon_sb+minor_potw_fluxn_sb
p_fluxn_sm = potw_n_mon_sm+minor_potw_fluxn_sm
p_fluxn_sp = potw_n_mon_sp+minor_potw_fluxn_sp
p_fluxn_sd = potw_n_mon_sd+minor_potw_fluxn_sd
p_fluxn_oc = potw_n_mon_oc+minor_potw_fluxn_oc


# yearly flux of n per region
p_sb_yr = np.nansum(p_fluxn_sb)
p_sm_yr = np.nansum(p_fluxn_sm)
p_sp_yr = np.nansum(p_fluxn_sp)
p_sd_yr = np.nansum(p_fluxn_sd)
p_oc_yr = np.nansum(p_fluxn_oc)

#############
# plot
#############
a_yr = np.array((atmos_sb,atmos_sm,atmos_sp,atmos_oc,atmos_sd))
p_yr = np.array((p_sb_yr,p_sm_yr,p_sp_yr,p_oc_yr,p_sd_yr))
r_yr = np.array((r_sb_yr,r_sm_yr,r_sp_yr,r_oc_yr,r_sd_yr))

figw = 12
figh = 8
seasons = ['Winter','Spring','Summer','Fall']
regions = ['Santa Barbara','Santa Monica','San Pedro','Orange County','San Diego']
width = 0.1
axis_font = 18
#savename = './figs/inputs_compare_region.pdf'
savename = './figs/inputs_compare_region_nolog.pdf'

plt.ion()
fig,ax = plt.subplots(1,1,figsize=[figw,figh])
x_ind = np.arange(len(regions))
ax.bar(x_ind,a_yr,color='gray',width=width,hatch='//',label='Atmospheric Deposition')
ax.bar(x_ind+width,p_yr,color='orange',width=width,label='All POTWs')
ax.bar(x_ind+(2*width),r_yr,color='cornflowerblue',width=width,hatch='\\',label='Rivers')
ax.set_xticks([width,1+width,2+width,3+width,4+width])
ax.set_xticklabels(['Santa Barbara','Santa Monica','San Pedro','Orange County','San Diego'])
#ax.set_yscale('log')
#ax.set_ybound(lower=10E-1,upper=25E5)
ax.set_ylabel('Total N Flux mmol s$^{-1}$',fontsize=axis_font)
ax.tick_params(axis='both',which='major',labelsize=axis_font)
#ax.tick_params(axis='both',which='minor',labelsize=axis_font)
ax.legend(loc='lower left',fontsize=20,bbox_to_anchor=(0,1.02,1.,.102),mode='expand',borderaxespad=0.,ncol=3,handlelength=2.5,handleheight=1.5)

plt.savefig(savename,bbox_inches='tight')



