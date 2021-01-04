import numpy as np
import scipy.io as sio
import pandas as pd
import glob as glob
import datetime as datetime

num = '6'

time_unit = 'minutes since 2000-10-31 00:15'

xl = pd.read_excel('A'+num+'_lacsd_palos_verdes_sampling.xlsx',sheet_name='5m')

lat_nc = xl['latitude'][1]
lon_nc = xl['longitude'][1]
u_final = np.array(xl['EW_velocity']/100)
v_final = np.array(xl['NS_velocity']/100)
u_final[u_final<-99] = np.nan
v_final[v_final<-99] = np.nan


num_arr = np.empty((u_final.shape[0]))
for d_i in range(len(u_final)):
    num_arr[d_i] = 15*d_i

savename = 'A'+num+'_lacsd_PV_sampling_surf.mat'

var_key = ['time','time_unit','u','v','latitude','longitude']
var_save = [num_arr,time_unit,u_final,v_final,lat_nc,lon_nc]

save_dict = {}
for k_i in range(len(var_key)):
    save_dict[var_key[k_i]] = var_save[k_i]

sio.savemat(savename, save_dict)


