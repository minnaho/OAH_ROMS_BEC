import numpy as np
import h5py
import matplotlib.pyplot as plt
import glob

prof_dir = './model_profiles/'

obsdata = h5py.File('./data/bight_bin.mat','r')['bight_bin']
obs_depth = np.squeeze(obsdata['depth'])

# regions ['carlsbad', 'hyperion', 'jwpcp', 'ocsd', 'plwptp', 'ventura']
obs_regions = ['carlsbad','ocsd','plwptp','hyperion','jwpcp','ventura']

# variables
#obs_var = ['ammonia','dissolved_oxygen','salinity','temperature','irradiance','Chl']
#model_var = ['NH4','O2','PAR','salt','temp']
#model_var = ['NH4','O2','salt','temp','PAR','Chl']
model_var = ['Chl']
obs_var = ['Chl']

# years 'yy1998' - 'yy2017'
years = range(2013,2018)

# seasons ['all', 'amj', 'jas', 'jfm', 'ond']
#seasons = ['amj', 'jas', 'jfm', 'ond','all']
seasons = ['all','jfm','amj','jas','ond']
ax_titles = ['Year','Winter','Spring','Summer','Fall']

for y_i in years:
    for v_i in range(len(obs_var)):
        for r_i in range(len(obs_regions)):
            fig1,ax1 = plt.subplots(1,5,figsize=[16,6])
            for a_i in range(len(seasons)):
                # read in obs data
                if model_var[v_i] == 'Chl':
                    # convert ug/L to umol/L (which is equal to mmol/m3) *(1./12)
                    # or is it mg/L, then *(1000./12)
                    obsmean = np.squeeze(obsdata['mean'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])*(1000./12)
                    obspct95 = np.squeeze(obsdata['pct95'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])*(1000./12)
                    obspct05 = np.squeeze(obsdata['pct05'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])*(1000./12)
                else:
                    obsmean = np.squeeze(obsdata['mean'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])
                    obspct95 = np.squeeze(obsdata['pct95'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])
                    obspct05 = np.squeeze(obsdata['pct05'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])
            
                # read in model data
                if seasons[a_i] == 'all':
                    roms_list = list(sorted(glob.glob(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'M*.npy')))
                elif seasons[a_i] == 'jfm':
                    roms_list = list(sorted(glob.glob(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'M0[1-3]*.npy')))
                elif seasons[a_i] == 'amj':
                    roms_list = list(sorted(glob.glob(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'M0[4-6]*.npy')))
                elif seasons[a_i] == 'jas':
                    roms_list = list(sorted(glob.glob(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'M0[7-9]*.npy')))
                elif seasons[a_i] == 'ond':
                    roms_list = list(sorted(glob.glob(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'M1[0-2]*.npy')))
            
                # initialize a 12 x 1 array to append to
                # end up with a 12 x N array that contains profiles
                # of the chosen season and region
                roms_arr = np.ones((len(obs_depth),1))*np.nan
            
                for p_i in range(len(roms_list)):
                    p_arr = np.load(roms_list[p_i])
                    roms_arr = np.concatenate((roms_arr,p_arr),axis=1)
            
                modelmean  = np.nanmean(roms_arr,axis=1)
                modelpct95 = np.nanpercentile(roms_arr,95,axis=1)
                modelpct05 = np.nanpercentile(roms_arr,5,axis=1)
                
                # plot
                ax1.flat[a_i].plot(obsmean,obs_depth,color='navy')
                ax1.flat[a_i].plot(obspct95,obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(obspct05,obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(modelmean,obs_depth,color='red')
                ax1.flat[a_i].plot(modelpct95,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].plot(modelpct05,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].set_title(ax_titles[a_i])
                ax1.flat[a_i].invert_yaxis()
            ax1.flat[0].set_ylabel('Depth (m)',fontsize=14)
            if model_var[v_i] == 'NH4' or model_var[v_i] == 'O2':
                ax1.flat[2].set_xlabel(model_var[v_i]+' (mmol m$^{-3}$)',fontsize=14)
            if model_var[v_i] == 'salt':
                ax1.flat[2].set_xlabel('Salinity (PSU)',fontsize=14)
            if model_var[v_i] == 'temp':
                ax1.flat[2].set_xlabel('Temperature (C)',fontsize=14)
            if model_var[v_i] == 'PAR':
                ax1.flat[2].set_xlabel('Irradiance (W m$^{-2}$)',fontsize=14)
            if model_var[v_i] == 'Chl':
                ax1.flat[2].set_xlabel('Chl-a (mmol m$^{-3}$)',fontsize=14)
            fig1.suptitle(str(y_i),fontsize=16)
            fig1.savefig('./figs/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'.png',bbox_inches='tight')
            plt.close()



