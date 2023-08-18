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
seasons = ['amj', 'jas', 'jfm', 'ond','all']

# variables ['CDOM', 'Chl', 'ammonia', 'dissolved_oxygen', 
# 'irradiance', 'pH', 'salinity', 'temperature']
#obs_var = list(obsdata['mean']['hyperion']['yy2017']['all'].keys())
obs_var = ['ammonia','dissolved_oxygen','irradiance','salinity','temperature']
model_var = ['NH4','O2','PAR','salt','temp']

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


for y_i in years:
    for v_i in range(len(obs_var)): 
        fig1,ax1 = plt.subplots(1,5,figsize=[16,6])
        roms_list = list(sorted(glob.glob(roms_monthly+str(y_i)+'M*.nc')))
        snnc = np.ones((len(roms_list),len(obs_depth),masknc.shape[0],masknc.shape[1]))*np.nan
        for s_i in range(1,len(roms_list)+1):
            # 12 for each month
            datanc = Dataset(roms_monthly+str(y_i)+'M'+'%02d'%s_i+'.nc','r')
            grdz = pyroms.grid.get_ROMS_grid('L2',zeta=np.squeeze(datanc.variables['zeta'])) 
            varnc = np.squeeze(datanc.variables[model_var[v_i]])
            varnc[varnc>1E10] = np.nan
            # get same depths as observations
            for d_i in range(len(obs_depth)):
                print(str(y_i),obs_var[v_i],' month ',s_i,' depth '+str(obs_depth[d_i]))
                zslice_arr = np.array(pyroms.tools.zslice(varnc,-1*obs_depth[d_i],grdz)[0])
                zslice_arr[zslice_arr>1E10] = np.nan
                snnc[s_i-1,d_i,:,:] = zslice_arr
        for r_i in range(len(obs_regions)):
            for a_i in range(len(seasons)):
                # model seasonal average
                if seasons[a_i] == 'all': 
                    modelmean = np.nanmean(snnc*mask_all[r_i],axis=(0,2,3))
                    modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc*mask_all[r_i],axis=(2,3)),95,axis=0)
                    modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc*mask_all[r_i],95,axis=0),axis=(1,2))
                    modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc*mask_all[r_i],axis=(2,3)),5,axis=0)
                    modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc*mask_all[r_i],5,axis=0),axis=(1,2))
                elif seasons[a_i] == 'jfm': 
                    modelmean = np.nanmean(snnc[0:3]*mask_all[r_i],axis=(0,2,3))
                    modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc[0:3]*mask_all[r_i],axis=(2,3)),95,axis=0)
                    modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc[0:3]*mask_all[r_i],95,axis=0),axis=(1,2))
                    modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc[0:3]*mask_all[r_i],axis=(2,3)),5,axis=0)
                    modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc[0:3]*mask_all[r_i],5,axis=0),axis=(1,2))
                elif seasons[a_i] == 'amj': 
                    modelmean = np.nanmean(snnc[3:6]*mask_all[r_i],axis=(0,2,3))
                    modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc[3:6]*mask_all[r_i],axis=(2,3)),95,axis=0)
                    modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc[3:6]*mask_all[r_i],95,axis=0),axis=(1,2))
                    modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc[3:6]*mask_all[r_i],axis=(2,3)),5,axis=0)
                    modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc[3:6]*mask_all[r_i],5,axis=0),axis=(1,2))
                elif seasons[a_i] == 'jas': 
                    modelmean = np.nanmean(snnc[6:9]*mask_all[r_i],axis=(0,2,3))
                    modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc[6:9]*mask_all[r_i],axis=(2,3)),95,axis=0)
                    modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc[6:9]*mask_all[r_i],95,axis=0),axis=(1,2))
                    modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc[6:9]*mask_all[r_i],axis=(2,3)),5,axis=0)
                    modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc[6:9]*mask_all[r_i],5,axis=0),axis=(1,2))
                elif seasons[a_i] == 'ond': 
                    modelmean = np.nanmean(snnc[9:]*mask_all[r_i],axis=(0,2,3))
                    modelpct95_mean_pct = np.nanpercentile(np.nanmean(snnc[9:12]*mask_all[r_i],axis=(2,3)),95,axis=0)
                    modelpct95_pct_mean = np.nanmean(np.nanpercentile(snnc[9:12]*mask_all[r_i],95,axis=0),axis=(1,2))
                    modelpct05_mean_pct = np.nanpercentile(np.nanmean(snnc[9:12]*mask_all[r_i],axis=(2,3)),5,axis=0)
                    modelpct05_pct_mean = np.nanmean(np.nanpercentile(snnc[9:12]*mask_all[r_i],5,axis=0),axis=(1,2))
                    
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_mean.npy',modelmean)
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct95_mean_pct.npy',modelpct95_mean_pct)
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct05_mean_pct.npy',modelpct05_mean_pct)
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct95_pct_mean.npy',modelpct95_pct_mean)
                np.save('./model_profiles/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct05_pct_mean.npy',modelpct05_pct_mean)
                ax1.flat[a_i].plot(np.squeeze(obs_mean[obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]]),obs_depth,color='navy')
                ax1.flat[a_i].plot(np.squeeze(obs_pct95[obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]]),obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(np.squeeze(obs_pct05[obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]]),obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(modelmean,obs_depth,color='red')
                ax1.flat[a_i].plot(modelpct95_mean_pct,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].plot(modelpct05_mean_pct,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].invert_yaxis()
        fig1.savefig(model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'.png',bbox_inches='tight')


