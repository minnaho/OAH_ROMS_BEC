import numpy as np
from netCDF4 import Dataset,num2date,date2num
import matplotlib
import matplotlib.pyplot as plt
import glob
plt.ion()

# data source
path_folder = '/data/project1/minnaho/validation/ocsd_george_robertson/SAIC_moored_data_1986_2008_veloc_temp_salt/'
# get temperature files only
mooring_folder = 'mooring_P/*t_*'

data_files = sorted(glob.glob(path_folder+mooring_folder))

temp_list = []
time_list = []
depth_list = []
for f_i in data_files:
    print(f_i[109:])
    dataset = Dataset(f_i,'r')
    temp_list.append(dataset.variables['T_var'][:,:])
    time_units = dataset.variables['time'].units
    time_list.append(num2date(dataset.variables['time'][:],time_units))
    d_temp = np.empty((len(num2date(dataset.variables['time'][:],time_units))))
    d_temp.fill(dataset.variables['depth'][:][0])
    depth_list.append(d_temp)

temp_flat = [item for sublist in temp_list for item in sublist]
temp_flat = [item for sublist in temp_flat for item in sublist]
depth_flat = [item for sublist in depth_list for item in sublist]
depth_unique = np.array(sorted((list(set(depth_flat)))))
time_flat = [item for sublist in time_list for item in sublist]
time_num = date2num(time_flat,time_units)

temp_2d = np.empty((depth_unique.shape[0],len(time_num)))
temp_2d.fill(np.nan)
for d_t in range(len(depth_flat)):
    print(d_t)
    for ind in range(len(depth_unique)):
        if (depth_flat[d_t] == depth_unique[ind]):
            temp_2d[ind,d_t] = temp_flat[d_t]
            

plt.figure(figsize=[13,8])
#plt.contourf(time_num,depth_unique,temp_2d,cmap='viridis')
#plt.pcolor(time_num,depth_unique,temp_2d,cmap='viridis')
plt.imshow(temp_2d,aspect='auto',cmap='viridis')
#plt.gca().invert_yaxis()
plt.colorbar()

