import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import l2grid
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date
import pyroms
import glob
import datetime

roms_out = '/data/project6/ROMS/L2SCB_AP/daily/l2_scb_avg.Y'

# choose same location of profiles in observations as in model

# choose specific months
#list_jfm = find(month==2) ;
#list_amj = find(month==5) ;
#list_jas = find(month==8) ;
#list_ond = find(month==10) ;


# try taking same period of daily model output as observations

# run other years when this is done

# pick year
year = 2016

#######################
# observational data
#######################
obsnc = Dataset('/data/project1/minnaho/validation/central_bight/central_bight_master_database_1998_2019_1D_validation_2023.nc','r')
# date since info in netcdf file ncdump -h
obsdate = num2date(np.array(obsnc.variables['date']),'days since 1994-01-16',only_use_cftime_datetimes=False,only_use_python_datetimes=True)
obslat  = np.array(obsnc.variables['latitude'])
obslon  = np.array(obsnc.variables['longitude'])

# get all x and y of all obs points

indx_mat = h5py.File('./data/indx1.mat','r')
indy_mat = h5py.File('./data/indy1.mat','r')

indx_all = np.array(indx_mat['indx1'])
indy_all = np.array(indy_mat['indy1'])

# find x and y within one year

datestart = datetime.datetime(year,1,1)
dateend = datetime.datetime(year,12,31)

dateind = np.where((obsdate>datestart)&(obsdate<dateend))[0]

indx_dt = np.squeeze(indx_all[dateind])
indy_dt = np.squeeze(indy_all[dateind])

coords_dt = np.array((indy_dt,indx_dt)).T

# obsdata.keys()
# ['depth', 'max', 'mean', 'min', 'nb', 'pct05', 'pct10', 
# 'pct25', 'pct50', 'pct75', 'pct90', 'pct95', 'std', 'sterror']
obsdata = h5py.File('./data/bight_bin.mat','r')['bight_bin']
obs_depth = np.squeeze(obsdata['depth'])

# regions ['carlsbad', 'hyperion', 'jwpcp', 'ocsd', 'plwptp', 'ventura']
obs_regions = ['carlsbad','ocsd','plwptp','hyperion','jwpcp','ventura']


# variables ['CDOM', 'Chl', 'ammonia', 'dissolved_oxygen', 
# 'irradiance', 'pH', 'salinity', 'temperature']
#obs_var = list(obsdata['mean']['hyperion']['yy2017']['all'].keys())
#obs_var = ['ammonia','dissolved_oxygen','irradiance','salinity','temperature','Chl']
model_var = ['NH4','O2','PAR','salt','temp','Chl']
#obs_var = ['Chl']
#model_var = ['NH4']

obs_mean = obsdata['mean']
obs_pct95 = obsdata['pct95']
obs_pct05 = obsdata['pct05']

####################
# model data
####################
masknc = l2grid.mask_nc

# regions
mask_valid = Dataset('mask_valid.nc','r')
mask_keys = list(sorted(mask_valid.variables.keys()))
mask_all = []
for m_i in range(len(mask_keys)):
    masktemp = np.squeeze(mask_valid.variables[mask_keys[m_i]]) 
    masktemp[masktemp==0] = np.nan
    mask_all.append(masktemp)

# find x and y in region and time
locind = []
datelist = []
for m_i in range(len(obs_regions)):
    indy_mask = np.where(~np.isnan(mask_all[m_i])==True)[0]
    indx_mask = np.where(~np.isnan(mask_all[m_i])==True)[1]
    coords_mask = np.array((indy_mask,indx_mask)).T
    dtset = set([tuple(x) for x in coords_dt])
    maskset = set([tuple(x) for x in coords_mask])
    locind.append(np.array([x for x in dtset & maskset]))
    # find dates in obs data
    for l_i in range(len(locind[m_i])):
        # indices where locind matches in coords_dt
        tempind = np.where((locind[m_i].T[0][l_i]==coords_dt.T[0])&(locind[m_i].T[1][l_i]==coords_dt.T[1]))[0]
        # dates that match the time and location
        tempdates = np.unique(obsdate[dateind[tempind]])
        datelist.append(tempdates)

# a little lazy here by using all dates in a year
# instead of specific to each profile

locarr = np.array([item for sublist in locind for item in sublist])
dateuniq = np.unique([item for sublist in datelist for item in sublist])
# remove dates in december 2017 since no model output
dateuniq = dateuniq[dateuniq<datetime.datetime(2017,12,1,0,0)]

# loop through model output days 
# that fit the obs date and get profiles
# matching locations in each region
# save one region's profiles as a .npy with 
# dim 0 as depth and dim 1 as each profile in a region
for d_i in range(dateuniq.shape[0]):
    modely = dateuniq[d_i].year
    modelm = dateuniq[d_i].month
    modeld = dateuniq[d_i].day
    print(roms_out+str(modely)+'M%02d'%modelm+'D%02d'%modeld+'.nc')
    readnc = Dataset(roms_out+str(modely)+'M%02d'%modelm+'D%02d'%modeld+'.nc','r')
    for v_i in range(len(model_var)): 
        if model_var[v_i] == 'Chl':
            diatc = np.squeeze(readnc.variables['DIATC'])
            spcnc = np.squeeze(readnc.variables['SPC'])
            diazc = np.squeeze(readnc.variables['DIAZC'])
            diatc[diatc>1E10] = np.nan
            spcnc[spcnc>1E10] = np.nan
            diazc[diazc>1E10] = np.nan

            diatc[diatc<0] = 0
            spcnc[spcnc<0] = 0
            diazc[diazc<0] = 0

            varnc = diatc+spcnc+diazc
        else:
            varnc = np.squeeze(readnc.variables[model_var[v_i]])

        grdz = pyroms.grid.get_ROMS_grid('L2',zeta=np.squeeze(readnc.variables['zeta'])) 
        varnc[varnc>1E10] = np.nan
        datanc = np.ones((len(obs_depth),masknc.shape[0],masknc.shape[1]))*np.nan
        # get same depths as observations
        for d_i in range(len(obs_depth)):
            print(model_var[v_i],' depth '+str(obs_depth[d_i]))
            zslice_arr = np.array(pyroms.tools.zslice(varnc,-1*obs_depth[d_i],grdz)[0])
            zslice_arr[zslice_arr>1E10] = np.nan
            datanc[d_i,:,:] = zslice_arr
        # locind len is 6, 1 for each region
        # get profiles in each region
        for l_i in range(len(locind)):
            # try except because some locind are empty 
            # because no data in that region for that year
            try:
                print(model_var[v_i],' region '+str(obs_regions[l_i]))
                profs = datanc[:,locind[l_i].T[0].astype(int),locind[l_i].T[1].astype(int)]
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[l_i]+'_'+str(modely)+'M%02d'%modelm+'D%02d'%modeld+'.npy',profs)
            except IndexError:
                pass
        

    

# use unique dates as ROMS daily output list? and find all points?
# trying ^ this
# or try to be more precise with specific days for each profile?        

