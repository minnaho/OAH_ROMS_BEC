##################################################
# compare L2 SCB AP 300 m simulations
# hourly outputs vs daily average outputs
# time series of NH4 and salinity at HTP and OCSD
# and rivers
##################################################
import numpy as np
from netCDF4 import Dataset,num2date
import glob as glob
import matplotlib.pyplot as plt
import datetime as datetime

# variables to look at
var1 = 'NH4'
var2 = 'salt'

# sigma level (-1 = surface)
s_l = -1

# hourly outputs
h_path = '/data/project3/kesf/ROMS/L2_SCB_AP/hourly/AVG_Y2000M07/'
h_files = list(sorted(glob.glob(h_path+'l2_scb_his.*')))

# daily outputs
d_path = '/data/project5/kesf/ROMS/L2SCB_AP/V3/AVG_Y2000M07/'
d_files = list(sorted(glob.glob(d_path+'l2_scb_avg.*')))

# points to extract time series
places = ['HTP','OCSD','SB river','SM river','LA River','SG River','SD River']
o_hp_pt = np.array([557,650])
o_oc_pt = np.array([551,447])

r_sb_pt = np.array([534,961])
r_sm_pt = np.array([589,682])
r_la_pt = np.array([557,565])
r_sg_pt = np.array([577,533])
r_sd_pt = np.array([564,314])

eta_pts = np.array([o_hp_pt[1],o_oc_pt[1],r_sb_pt[1],r_sm_pt[1],r_la_pt[1],r_sg_pt[1],r_sd_pt[1]])
xi_pts  = np.array([o_hp_pt[0],o_oc_pt[0],r_sb_pt[0],r_sm_pt[0],r_la_pt[0],r_sg_pt[0],r_sd_pt[0]])

h_time = np.empty((len(h_files)))
d_time = np.empty((len(d_files)))

h_ts_v1 = np.empty((len(eta_pts),len(h_files)))
h_ts_v2 = np.empty((len(eta_pts),len(h_files)))
d_ts_v1 = np.empty((len(eta_pts),len(d_files)))
d_ts_v2 = np.empty((len(eta_pts),len(d_files)))


for h_i in range(len(h_files)):
    h_time[h_i] = Dataset(h_files[h_i],'r').variables['ocean_time'][0]
    print('file # '+str(h_i)+' of '+str(len(h_files)))
    for p_i in range(len(eta_pts)):
        h_nc_v1 = Dataset(h_files[h_i],'r').variables[var1][0,s_l,eta_pts[p_i],xi_pts[p_i]]
        h_nc_v2 = Dataset(h_files[h_i],'r').variables[var2][0,s_l,eta_pts[p_i],xi_pts[p_i]]
        h_ts_v1[p_i,h_i] = h_nc_v1
        h_ts_v2[p_i,h_i] = h_nc_v2


for d_i in range(len(d_files)):
    d_time[d_i] = Dataset(d_files[d_i],'r').variables['ocean_time'][0]
    print('file # '+str(d_i)+' of '+str(len(d_files)))
    for p_i in range(len(eta_pts)):
        d_nc_v1 = Dataset(d_files[d_i],'r').variables[var1][0,s_l,eta_pts[p_i],xi_pts[p_i]]
        d_nc_v2 = Dataset(d_files[d_i],'r').variables[var2][0,s_l,eta_pts[p_i],xi_pts[p_i]]
        d_ts_v1[p_i,d_i] = d_nc_v1
        d_ts_v2[p_i,d_i] = d_nc_v2

# datetime calculation
dateinit = datetime.datetime(1994,1,1,0,0,0)
h_dt = []
for t_i in range(len(h_time)):
    h_dt.append(datetime.timedelta(seconds=h_time[t_i])+dateinit)

d_dt = []
for t_i in range(len(d_time)):
    d_dt.append(datetime.timedelta(seconds=d_time[t_i])+dateinit)


hours = range(len(h_files))
plt.ion()
for p_i in range(len(places)):
    fig,(ax1,ax2) = plt.subplots(2,1,sharex=True)
    ax1.set_title(places[p_i]+' '+var1)
    ax1.plot(h_dt,h_ts_v1[p_i],label='hourly snapshot new Dsrc')
    ax1.plot(d_dt,d_ts_v1[p_i],label='daily avg Dsrc 2')
    ax2.set_title(places[p_i]+' '+var2)
    ax2.plot(h_dt,h_ts_v2[p_i],label='hourly snapshot new Dsrc')
    ax2.plot(d_dt,d_ts_v2[p_i],label='daily avg Dsrc 2')
    ax2.legend(loc='best')
    ax2.tick_params(labelrotation=45)
#    ax2.xticks(rotation=45)
    fig.savefig(places[p_i]+'_ts.png',bbox_inches='tight')
