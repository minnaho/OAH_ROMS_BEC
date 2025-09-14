import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import l2grid
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import pyroms
import glob

roms_monthly = '/data/project6/ROMS/L2SCB_AP/monthly/l2_scb_avg.Y'

# choose specific months
#list_jfm = find(month==2) ;
#list_amj = find(month==5) ;
#list_jas = find(month==8) ;
#list_ond = find(month==10) ;

# choose same location of profiles in observations as in model

# try taking same period of daily model output as observations

# run other years when this is done

#######################
# observational data
#######################
# obsdata.keys()
# ['depth', 'max', 'mean', 'min', 'nb', 'pct05', 'pct10', 
# 'pct25', 'pct50', 'pct75', 'pct90', 'pct95', 'std', 'sterror']
obsdata = h5py.File('./data/bight_bin.mat','r')['bight_bin']
obs_depth = np.squeeze(obsdata['depth'])

# regions ['carlsbad', 'hyperion', 'jwpcp', 'ocsd', 'plwptp', 'ventura']
obs_regions = ['carlsbad','ocsd','plwptp','hyperion','jwpcp','ventura']

# years 'yy1998' - 'yy2017'
#years = range(1998,2018) 
years = range(2017,2018) 

# seasons ['all', 'amj', 'jas', 'jfm', 'ond']
#seasons = ['amj', 'jas', 'jfm', 'ond','all']
seasons = ['all']
#seasons = ['jfm']
#seasons = ['amj']
#seasons = ['jas']
#seasons = ['ond']

# variables ['CDOM', 'Chl', 'ammonia', 'dissolved_oxygen', 
# 'irradiance', 'pH', 'salinity', 'temperature']
#obs_var = list(obsdata['mean']['hyperion']['yy2017']['all'].keys())
#obs_var = ['ammonia','dissolved_oxygen','irradiance','salinity','temperature','Chl']
#model_var = ['NH4','O2','PAR','salt','temp','Chl']
#obs_var = ['Chl']
#model_var = ['Chl']

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


#for y_i in years:
for v_i in range(len(obs_var)): 
    for r_i in range(len(obs_regions)):
        for a_i in range(len(seasons)):
            if seasons[a_i] == 'all': 
                roms_list = list(sorted(glob.glob(roms_monthly+'201[3-7]'+'M*.nc')))
            elif seasons[a_i] == 'jfm': 
                roms_list = list(sorted(glob.glob(roms_monthly+'201[3-7]'+'M0[1-3].nc')))
            elif seasons[a_i] == 'amj': 
                roms_list = list(sorted(glob.glob(roms_monthly+'201[3-7]'+'M0[4-6].nc')))
            elif seasons[a_i] == 'jas': 
                roms_list = list(sorted(glob.glob(roms_monthly+'201[3-7]'+'M0[7-9].nc')))
            elif seasons[a_i] == 'ond': 
                roms_list = list(sorted(glob.glob(roms_monthly+'201[3-7]'+'M1[0-2].nc')))
            snnc = np.ones((len(roms_list),len(obs_depth),masknc.shape[0],masknc.shape[1]))*np.nan
            for s_i in range(len(roms_list)):
                if model_var[v_i] == 'Chl':
                    readnc = Dataset(roms_list[s_i],'r')
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
                    readnc = Dataset(roms_list[s_i],'r')
                    varnc = np.squeeze(readnc.variables[model_var[v_i]])

                grdz = pyroms.grid.get_ROMS_grid('L2',zeta=np.squeeze(readnc.variables['zeta'])) 
                varnc[varnc>1E10] = np.nan
                # get same depths as observations
                for d_i in range(len(obs_depth)):
                    print(seasons[a_i],' ',obs_var[v_i],' file ',roms_list[s_i],' depth '+str(obs_depth[d_i]))
                    zslice_arr = np.array(pyroms.tools.zslice(varnc,-1*obs_depth[d_i],grdz)[0])
                    zslice_arr[zslice_arr>1E10] = np.nan
                    snnc[s_i,d_i,:,:] = zslice_arr
            modelmean = np.nanmean(snnc*mask_all[r_i],axis=(0,2,3))
            modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc*mask_all[r_i],axis=(2,3)),95,axis=0)
            modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc*mask_all[r_i],95,axis=0),axis=(1,2))
            modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc*mask_all[r_i],axis=(2,3)),5,axis=0)
            modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc*mask_all[r_i],5,axis=0),axis=(1,2))
                
            np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_2013_2017_'+seasons[a_i]+'_mean.npy',modelmean)
            np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_2013_2017_'+seasons[a_i]+'_pct95_mean_pct.npy',modelpct95_mean_pct)
            np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_2013_2017_'+seasons[a_i]+'_pct05_mean_pct.npy',modelpct05_mean_pct)
            np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_2013_2017_'+seasons[a_i]+'_pct95_pct_mean.npy',modelpct95_pct_mean)
            np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_2013_2017_'+seasons[a_i]+'_pct05_pct_mean.npy',modelpct05_pct_mean)


