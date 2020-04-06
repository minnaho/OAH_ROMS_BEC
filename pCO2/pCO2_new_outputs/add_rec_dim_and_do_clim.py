import subprocess
import glob

files = list(sorted(glob.glob('*.nc')))
'''
# add record dimension
for f_i in files:
    subprocess.call('ncecat -u time '+f_i+' '+f_i[:30]+'_rec.nc',shell=True)

# hourly climatology
for t_i in range(24):
    subprocess.call('ncra wrfout_d01_2010-??-??_'+'%02d'%t_i+':00:00_rec.nc '+'new_pCO2_clim_'+'%02d'%t_i+'.nc',shell=True)
'''
'''
# monthly avg old outputs
old_outputs_path = '/data/project1/minnaho/pCO2/rec_output/'
destination = '/data/project1/minnaho/pCO2/avg_monthly/'
for t_i in range(1,5):
    subprocess.call('ncra '+old_outputs_path+'wrfout_d01_2015-'+'%02d'%t_i+'*'+' '+destination+'pCO2_avg_monthly_'+'%02d'%t_i+'.nc',shell=True)
for t_i in range(7,9):
    subprocess.call('ncra '+old_outputs_path+'wrfout_d01_2015-'+'%02d'%t_i+'*'+' '+destination+'pCO2_avg_monthly_'+'%02d'%t_i+'.nc',shell=True)
for t_i in range(10,12):
    subprocess.call('ncra '+old_outputs_path+'wrfout_d01_2015-'+'%02d'%t_i+'*'+' '+destination+'pCO2_avg_monthly_'+'%02d'%t_i+'.nc',shell=True)
'''

# monthly avg new outputs
new_outputs_path = '/data/project1/minnaho/pCO2/pCO2_new_outputs/'
destination = '/data/project1/minnaho/pCO2/avg_monthly/'
for t_i in range(5,7):
    subprocess.call('ncra -O -v lat,lon,hestia '+new_outputs_path+'wrfout_d01_2010-'+'%02d'%t_i+'*_rec.nc'+' '+destination+'pCO2_avg_monthly_'+'%02d'%t_i+'.nc',shell=True)
