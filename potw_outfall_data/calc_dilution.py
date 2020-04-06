import numpy as np
from netCDF4 import Dataset,num2date

data_file = 'major_potw_data.nc'
data_nc = Dataset(data_file,'r')

time_all = data_nc.variables['time']
time_dt = num2date(np.array(time_all),time_all.units)

#h_w = 4./9 # horizontal weight
#h_w = 1./9 # horizontal weight
h_w = .25/9 # horizontal weight
v_w = 0.23 # vertical weight
split = 0.5 # how is flow split into diffusers
vol = 108900
dt = 30

n_conv = 14./1000

yr_s = 1997
yr_e = 2000
yr_ind_l = []
for ind_d,d_i in enumerate(time_dt):
    if d_i.year in list(range(yr_s,yr_e+1)):
        yr_ind_l.append(ind_d)

yr_ind = np.array((yr_ind_l))

# 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
potw = 0
no3_one = np.array(data_nc.variables['NO3'])[yr_ind,potw,potw]
nh4_one = data_nc.variables['NH4'][yr_ind,potw,potw]
don_one = data_nc.variables['ON'][yr_ind,potw,potw]
flow_one = data_nc.variables['flow'][yr_ind,potw,potw]
    
no3_mean = np.nanmean(no3_one)
nh4_mean = np.nanmean(nh4_one)
don_mean = np.nanmean(don_one)
flow_mean = np.nanmean(flow_one)

no3_after = ((no3_mean)*(v_w*h_w*split*flow_mean)*dt)/vol
nh4_after = ((nh4_mean)*(v_w*h_w*split*flow_mean)*dt)/vol
don_after = ((don_mean)*(v_w*h_w*split*flow_mean)*dt)/vol

no3_dil = no3_mean/no3_after
nh4_dil = nh4_mean/nh4_after
don_dil = don_mean/don_after

print('no3 mean before ',no3_mean*n_conv)
print('nh4 mean before ',nh4_mean*n_conv)
print('don mean before ',don_mean*n_conv)
print('flow mean',flow_mean)

print('no3 mean after ',no3_after*n_conv)
print('nh4 mean after ',nh4_after*n_conv)
print('don mean after ',don_after*n_conv)

print('no3 dil ',no3_dil)
print('nh4 dil ',nh4_dil)
print('don dil ',don_dil)

# example
# mg/L to mmol/m3 *(1000./14)
g_conv = 1000000./(86400*264) # million gallon/day to m3/s
m_conv = (1000./14) # mg/L to mmol/m3

c_i = 20 # mg/L
v_i = 200
c_e = n_conv*((c_i*m_conv*(h_w*v_w*v_i*g_conv)*dt)/vol) # conc in mg/L
dil_i = c_i/c_e
print('example c_i ',c_i)
print('example c_e ',c_e)
print('example dil ',dil_i)
