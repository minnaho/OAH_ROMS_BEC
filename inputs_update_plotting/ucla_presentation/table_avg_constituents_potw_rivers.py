import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import h5py
import scipy.io
import pandas as pd

fig_path = './figs/'
# data paths

potw_path = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc'

river_path = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc'

# convert to kg/month, then sum
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# conversions mg/L to mmol/m3
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855
mg_l_a = 1000/100.09 # mg/L CaCO3 to mmol/m3

######################
# potw
######################
potw_nc = Dataset(potw_path,'r')

potw_time = num2date(np.array(potw_nc.variables['time']),potw_nc.variables['time'].units,only_use_cftime_datetimes=False)
# start and end indices of potw for 1997-2000
potwn_1997 = 312
potwn_2017 = potw_time.shape[0] # 2017-12-31

potw_time_dt = np.array(potw_time[potwn_1997:potwn_2017])

# divide flows
potw_flo = np.array(potw_nc.variables['flow']) # m3/s
potw_nh4 = np.array(potw_nc.variables['NH4']) # mmol/m3
potw_no3 = np.array(potw_nc.variables['NO3']) # mmol/m3
potw_no2 = np.array(potw_nc.variables['NO2']) # mmol/m3
potw_doo = np.array(potw_nc.variables['dissolved_oxygen']) # mmol/m3
potw_tem = np.array(potw_nc.variables['temperature']) # mmol/m3
potw_bod = np.array(potw_nc.variables['BOD']) # mmol/m3
potw_phh = np.array(potw_nc.variables['pH']) # mmol/m3
potw_tpp = np.array(potw_nc.variables['total_P']) # mmol/m3
potw_tnn = np.array(potw_nc.variables['total_N']) # mmol/m3
potw_po4 = np.array(potw_nc.variables['PO4']) # mmol/m3
potw_opp = np.array(potw_nc.variables['organic_P']) # mmol/m3
potw_onn = np.array(potw_nc.variables['organic_N']) # mmol/m3
potw_toc = np.array(potw_nc.variables['total_organic_C']) # mmol/m3
potw_tfe = np.array(potw_nc.variables['total_Fe']) # mmol/m3
potw_sil = np.array(potw_nc.variables['SiO4']) # mmol/m3
potw_alk = np.array(potw_nc.variables['alkalinity']) # mmol/m3
potw_sal = np.array(potw_nc.variables['salinity']) # mmol/m3
potw_dfe = np.array(potw_nc.variables['dissolved_Fe']) # mmol/m3

pavg_nh4 = np.nanmean(potw_nh4[potwn_1997:potwn_2017])
pavg_no3 = np.nanmean(potw_no3[potwn_1997:potwn_2017])
pavg_no2 = np.nanmean(potw_no2[potwn_1997:potwn_2017])
pavg_doo = np.nanmean(potw_doo[potwn_1997:potwn_2017])
pavg_tem = np.nanmean(potw_tem[potwn_1997:potwn_2017])
pavg_bod = np.nanmean(potw_bod[potwn_1997:potwn_2017])
pavg_phh = np.nanmean(potw_phh[potwn_1997:potwn_2017])
pavg_tpp = np.nanmean(potw_tpp[potwn_1997:potwn_2017])
pavg_tnn = np.nanmean(potw_tnn[potwn_1997:potwn_2017])
pavg_po4 = np.nanmean(potw_po4[potwn_1997:potwn_2017])
pavg_opp = np.nanmean(potw_opp[potwn_1997:potwn_2017])
pavg_onn = np.nanmean(potw_onn[potwn_1997:potwn_2017])
pavg_toc = np.nanmean(potw_toc[potwn_1997:potwn_2017])
pavg_tfe = np.nanmean(potw_tfe[potwn_1997:potwn_2017])
pavg_sil = np.nanmean(potw_sil[potwn_1997:potwn_2017])
pavg_alk = np.nanmean(potw_alk[potwn_1997:potwn_2017])
pavg_sal = np.nanmean(potw_sal[potwn_1997:potwn_2017])
pavg_dfe = np.nanmean(potw_dfe[potwn_1997:potwn_2017])

pavg_nnn = pavg_no3+pavg_no2

###########
# river
###########
river_nc = Dataset(river_path,'r')

river_flo = np.array(river_nc.variables['flow']) # m3/s
river_nh4 = np.array(river_nc.variables['NH4']) # mmol/m3
river_no3 = np.array(river_nc.variables['NO3']) # mmol/m3
river_doo = np.array(river_nc.variables['dissolved_oxygen']) # mmol/m3
river_tem = np.array(river_nc.variables['temperature']) # mmol/m3
river_phh = np.array(river_nc.variables['pH']) # mmol/m3
river_tpp = np.array(river_nc.variables['total_P']) # mmol/m3
river_tnn = np.array(river_nc.variables['total_N']) # mmol/m3
river_po4 = np.array(river_nc.variables['PO4']) # mmol/m3
river_opp = np.array(river_nc.variables['organic_P']) # mmol/m3
river_onn = np.array(river_nc.variables['organic_N']) # mmol/m3
river_toc = np.array(river_nc.variables['total_organic_C']) # mmol/m3
river_tfe = np.array(river_nc.variables['total_Fe']) # mmol/m3
river_sil = np.array(river_nc.variables['SiO4']) # mmol/m3
river_alk = np.array(river_nc.variables['alkalinity']) # mmol/m3
river_sal = np.array(river_nc.variables['salinity']) # mmol/m3
river_dfe = np.array(river_nc.variables['dissolved_Fe']) # mmol/m3

ravg_nh4 = np.nanmean(river_nh4)
ravg_no3 = np.nanmean(river_no3)
ravg_doo = np.nanmean(river_doo)
ravg_tem = np.nanmean(river_tem)
ravg_phh = np.nanmean(river_phh)
ravg_tpp = np.nanmean(river_tpp)
ravg_tnn = np.nanmean(river_tnn)
ravg_po4 = np.nanmean(river_po4)
ravg_opp = np.nanmean(river_opp)
ravg_onn = np.nanmean(river_onn)
ravg_toc = np.nanmean(river_toc)
ravg_tfe = np.nanmean(river_tfe)
ravg_sil = np.nanmean(river_sil)
ravg_alk = np.nanmean(river_alk)
ravg_sal = np.nanmean(river_sal)
ravg_dfe = np.nanmean(river_dfe)

print('potw avg tnn: ',pavg_tnn*1./mg_l_n)
print('potw avg nnn: ',pavg_nnn*1./mg_l_n)
print('potw avg nh4: ',pavg_nh4*1./mg_l_n)
print('potw avg onn: ',pavg_onn*1./mg_l_n)
print('potw avg tpp: ',pavg_tpp*1./mg_l_p)
print('potw avg po4: ',pavg_po4*1./mg_l_p)
print('potw avg opp: ',pavg_opp*1./mg_l_p)
print('potw avg doo: ',pavg_doo*1./mg_l_o)
print('potw avg toc: ',pavg_toc*1./mg_l_c)
print('potw avg tfe: ',pavg_tfe*1./mg_l_f)
print('potw avg sil: ',pavg_sil*1./mg_l_s)
print('potw avg alk: ',pavg_alk*1./mg_l_a)
print('potw avg phh: ',pavg_phh)
print('potw avg tem: ',pavg_tem)
print('potw avg sal: ',pavg_sal)
#print('potw avg dfe: ',pavg_dfe*mg_l_n)

print('river avg tnn: ',ravg_tnn*1./mg_l_n)
print('river avg nnn: ',ravg_no3*1./mg_l_n)
print('river avg nh4: ',ravg_nh4*1./mg_l_n)
print('river avg onn: ',ravg_onn*1./mg_l_n)
print('river avg tpp: ',ravg_tpp*1./mg_l_p)
print('river avg po4: ',ravg_po4*1./mg_l_p)
print('river avg opp: ',ravg_opp*1./mg_l_p)
print('river avg doo: ',ravg_doo*1./mg_l_o)
print('river avg toc: ',ravg_toc*1./mg_l_c)
print('river avg tfe: ',ravg_tfe*1./mg_l_f)
print('river avg sil: ',ravg_sil*1./mg_l_s)
print('river avg alk: ',ravg_alk*1./mg_l_a)
print('river avg phh: ',ravg_phh)
print('river avg tem: ',ravg_tem)
print('river avg sal: ',ravg_sal)
