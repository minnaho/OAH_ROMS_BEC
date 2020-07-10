# create vertical profile of duration, intensity, frequency
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import glob as glob
import datetime as datetime

save_path = 'decapod_figs/'


ij_pt = [[540,615],[1070,660]]
ij_nm = ['Channel Island','Offshore SF Bay']
#ij_pt = [540,615] #first point near channel islands, second in 
#ij_pt = [1070,660] #offshore SF
#ij_pt = [1060,690] #inshore SF
#ij_pt = [1060,670] #inshore SF
# read data

exp_variables = ['Duration',
                 #'Recovery',
                 'Frequency',
                 'Intensity']
                 #'Severity']
var_label = ['% time below threshold','Number of events','Mean value below threshold']

dt_st = datetime.datetime(1997,2,1)
dt_en = datetime.datetime(2007,11,30)
date_range = np.array([dt_st+datetime.timedelta(days=n) for n in range(int ((dt_en+datetime.timedelta(days=1)-dt_st).days))])
num_days_full = len(date_range)



# depth range
depth_rg = np.arange(30,160,10)
data_path = '../decapods_nc/'
files_nc = [
'decapods_juvenile_mort_30m_1997_2007.nc',
'decapods_juvenile_mort_40m_1997_2007.nc',
'decapods_juvenile_mort_50m_1997_2007.nc',
'decapods_juvenile_mort_60m_1997_2007.nc',
'decapods_juvenile_mort_70m_1997_2007.nc',
'decapods_juvenile_mort_80m_1997_2007.nc',
'decapods_juvenile_mort_90m_1997_2007.nc',
'decapods_juvenile_mort_100m_1997_2007.nc',
'decapods_juvenile_mort_110m_1997_2007.nc',
'decapods_juvenile_mort_120m_1997_2007.nc',
'decapods_juvenile_mort_130m_1997_2007.nc',
'decapods_juvenile_mort_140m_1997_2007.nc',
'decapods_juvenile_mort_150m_1997_2007.nc']

fig_w = 14
fig_h = 10
axis_tick_size = 14
subplot_title_font = 14

# get values and plot
plt.ion()
fig,axes = plt.subplots(1,3,figsize=[fig_w,fig_h],sharey=True)
for v_i in range(len(exp_variables)):
    print(exp_variables[v_i])
    axes.flat[v_i].set_title(exp_variables[v_i],fontsize=subplot_title_font)
    prof_values = np.empty((len(ij_pt),len(files_nc)))
    for f_i in range(len(files_nc)):
        print(files_nc[f_i])
        data_nc = Dataset(data_path+files_nc[f_i],'r')
        for p_i in range(len(ij_pt)):
            # convert to % time
            if exp_variables[v_i]=='Duration':
                pt_value = ((np.array(data_nc.variables[exp_variables[v_i]])[ij_pt[p_i][1],ij_pt[p_i][0]])/num_days_full)*100
            else:
                pt_value = np.array(data_nc.variables[exp_variables[v_i]])[ij_pt[p_i][1],ij_pt[p_i][0]]
            prof_values[p_i,f_i] = pt_value
    axes.flat[v_i].plot(prof_values[0],depth_rg,linestyle='--',marker='o',label=ij_nm[0])
    axes.flat[v_i].plot(prof_values[1],depth_rg,linestyle='--',marker='o',label=ij_nm[1])
    axes.flat[v_i].set_ylim(axes.flat[v_i].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    axes.flat[v_i].xaxis.set_label_position('top') # this moves the label to the top
    axes.flat[v_i].xaxis.set_ticks_position('top') # this moves the ticks to the top
    axes.flat[v_i].set_ylabel('Depth (m)',fontsize=axis_tick_size)
    axes.flat[v_i].set_xlabel(var_label[v_i],fontsize=axis_tick_size)
    axes.flat[v_i].tick_params(axis='both',which='major',labelsize=axis_tick_size)
    axes.flat[v_i].set_xlim(0)
    axes.flat[v_i].grid(True)

axes.flat[0].legend(fontsize='large',loc='best')
plt.savefig(save_path+'profile_decapods_juvenile_mort.png',bbox_inches='tight')
    
