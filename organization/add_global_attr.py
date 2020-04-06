import subprocess
import glob

path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/clim/'
model_name0 = 'l2_scb_bgc_flux_avg.M'
model_name1 = '_1997_2000_bgc_limitation.nc'

for i in range(1,13):
    subprocess.call('ncatted -O -a theta_s,global,a,f,6 '+path+model_name0+'%02d'%i+model_name1,shell=True)
