import numpy as np
import h5py
import matplotlib.pyplot as plt

prof_dir = './model_profiles/'

obsdata = h5py.File('./data/bight_bin.mat','r')['bight_bin']
obs_depth = np.squeeze(obsdata['depth'])

# regions ['carlsbad', 'hyperion', 'jwpcp', 'ocsd', 'plwptp', 'ventura']
obs_regions = ['carlsbad','ocsd','plwptp','hyperion','jwpcp','ventura']

# variables
obs_var = ['ammonia','dissolved_oxygen','irradiance','salinity','temperature']
model_var = ['NH4','O2','PAR','salt','temp']

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
                obsmean = np.squeeze(obsdata['mean'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])
                obspct95 = np.squeeze(obsdata['pct95'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])
                obspct05 = np.squeeze(obsdata['pct05'][obs_regions[r_i]]['yy'+str(y_i)][seasons[a_i]][obs_var[v_i]])

                # read in model data
                modelmean = np.load(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_mean.npy')
                modelpct95 = np.load(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct95_pct_mean.npy')
                modelpct05 = np.load(prof_dir+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'_'+seasons[a_i]+'_pct05_pct_mean.npy')
                
                # plot
                ax1.flat[a_i].plot(obsmean,obs_depth,color='navy')
                ax1.flat[a_i].plot(obspct95,obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(obspct05,obs_depth,color='lightblue',linestyle='--')
                ax1.flat[a_i].plot(modelmean,obs_depth,color='red')
                ax1.flat[a_i].plot(modelpct95,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].plot(modelpct05,obs_depth,color='pink',linestyle='--')
                ax1.flat[a_i].set_title(ax_titles[a_i])
                ax1.flat[a_i].invert_yaxis()
            fig1.savefig('./figs/'+model_var[v_i]+'_'+obs_regions[r_i]+'_'+str(y_i)+'.png',bbox_inches='tight')
            plt.close()



