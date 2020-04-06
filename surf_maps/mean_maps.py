import subprocess
import glob

path_output = '/data/project3/kesf/tools_matlab/applications/xyt/outputs/'
path_mean = '/data/project1/minnaho/surf_maps/'
file_name = 'L1S*'

files = glob.glob1(path_output,file_name)
ind = files[0].index('_')+1
files[0][ind:].index('_')

for f_i in files:
    print(f_i)
    mean_name = f_i[ind:]
    ind_end = mean_name.index('_')
    subprocess.call('ncra -O '+path_output+f_i+' '+path_mean+mean_name[:ind_end]+'_surf_mean_1997_2007.nc',shell=True)
