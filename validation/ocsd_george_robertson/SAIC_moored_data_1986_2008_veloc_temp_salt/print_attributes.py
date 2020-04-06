import os
import glob
import subprocess

#folder_path = '/data/project1/minnaho/validation/ocsd_george_robertson/SAIC_moored_data_1986_2008_veloc_temp_salt/*/'
folder_path = '/data/project1/minnaho/validation/ocsd_george_robertson/SAIC_moored_data_1986_2008_veloc_temp_salt/mooring_P/'


# get folder names and remove the docs folder
#folders = sorted(glob.glob(folder_path))[1:]
folders = sorted(glob.glob(folder_path))[:]


for fol_i in folders:
    os.chdir(fol_i)
    file_names = sorted(glob.glob('*.nc')) 
    print(fol_i)
    for fil_i in file_names:
        print(fil_i)
        subprocess.call('ncdump -v depth '+fil_i+' | grep "depth = "',shell=True)
        #subprocess.call('ncdump -v time '+fil_i+' | grep "time = "',shell=True)
        subprocess.call('ncdump -h '+fil_i+' | grep "Start_Time"',shell=True)
        subprocess.call('ncdump -h '+fil_i+' | grep "Stop_Time"',shell=True)

