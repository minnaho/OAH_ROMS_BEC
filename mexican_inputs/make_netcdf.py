import numpy as np
import pandas as pd
from netCDF4 import Dataset,date2num

fi = pd.read_csv('mexican_ww_inputs.csv')
date = pd.date_range(start='1997-01-01',end='2017-12-31',freq='D')

# tijuana river temp
tj = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/tijuana/tijuana_river_full_dataset.csv')

tj_temp = tj['temperature C']

mgd_to_m3s = 0.043812645072430365
mg_l_n = 1000./14
mg_l_c = 1000./12
mg_l_o = 1000./16
mg_l_p = 1000./30.97
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855

#convert to kg/day or kg/month
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

# change lat/lon so point is on land mask
fi['lat'][3] = 32.37003932265783
fi['lon'][3] = -117.07331941187711 

writer = pd.ExcelWriter('mexican_potw_estimates_1997_2017.xlsx')

# print to excel file
for r_i in range(fi['Plant Name'].shape[0]):
    lat_tem = np.ones(date.shape)*fi['lat'][r_i]    
    lon_tem = np.ones(date.shape)*fi['lon'][r_i]    
    save_df = pd.DataFrame({'date':date,
    'flow m3/s':np.ones(date.shape)*fi['flow m3/s'][r_i],
    fi.keys()[4][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[4]][r_i]*mg_l_n,
    fi.keys()[5][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[5]][r_i]*mg_l_n,
    fi.keys()[6][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[6]][r_i]*mg_l_n,
    fi.keys()[7][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[7]][r_i]*mg_l_c,
    fi.keys()[8][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[8]][r_i]*mg_l_n,
    fi.keys()[9][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[9]][r_i]*mg_l_p,
    fi.keys()[10][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[10]][r_i]*mg_l_p,
    fi.keys()[11][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[11]][r_i]*mg_l_c,
    fi.keys()[12]:np.ones(date.shape)*fi[fi.keys()[12]][r_i],
    fi.keys()[13][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[13]][r_i]*(1./1000)*mg_l_f,
    'Dissolved Iron mmol/m3':np.ones(date.shape)*fi[fi.keys()[13]][r_i]*(1./1000)*mg_l_f*.2,
    fi.keys()[14]:np.ones(date.shape)*fi[fi.keys()[14]][r_i],
    fi.keys()[15][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[15]][r_i]*mg_l_c,
    fi.keys()[16][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[16]][r_i]*mg_l_o,
    fi.keys()[17][:-6]+'mmol/m3':np.ones(date.shape)*fi[fi.keys()[17]][r_i]*mg_l_s,
    fi.keys()[18]:tj_temp[:-365],
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df.to_excel(writer,sheet_name=fi['Plant Name'][r_i])

writer.save()

# netcdf
# time array
timeunit = 'days since 1997-01-01'
timenum = date2num(date.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('mexican_potw_estimates_1997_2017.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',fi['Plant Name'].shape[0]) # 75 rivers

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
no2_v = ncf.createVariable('NO2',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'C'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'PSU'
dfe_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = fi['lat']
lon_v[:] = fi['lon']

for i_i in range(fi['flow m3/s'].shape[0]):
    flo_v[:,i_i] = np.ones(date.shape)*fi['flow m3/s'][i_i]
    nh4_v[:,i_i] = np.ones(date.shape)*fi['NH4 (mg/L)'][i_i]*mg_l_n
    no3_v[:,i_i] = np.ones(date.shape)*fi['NO3 (mg/L)'][i_i]*mg_l_n
    no2_v[:,i_i] = np.ones(date.shape)*fi['NO2 (mg/L)'][i_i]*mg_l_n
    doo_v[:,i_i] = np.ones(date.shape)*fi['DO (mg/L)'][i_i]*mg_l_o
    tem_v[:,i_i] = np.ones(date.shape)*tj_temp[:-365]
    phh_v[:,i_i] = np.ones(date.shape)*fi['pH'][i_i]
    tpp_v[:,i_i] = np.ones(date.shape)*(fi['PO4 (mg/L)'][i_i]+fi['OP (mg/L)'][i_i])*mg_l_p
    tnn_v[:,i_i] = np.ones(date.shape)*(fi['NO3 (mg/L)'][i_i]+fi['NH4 (mg/L)'][i_i]+fi['NO2 (mg/L)'][i_i])*mg_l_n
    po4_v[:,i_i] = np.ones(date.shape)*fi['PO4 (mg/L)'][i_i]*mg_l_p
    opp_v[:,i_i] = np.ones(date.shape)*fi['OP (mg/L)'][i_i]*mg_l_p
    toc_v[:,i_i] = np.ones(date.shape)*fi['TOC (mg/L)'][i_i]*mg_l_c
    onn_v[:,i_i] = np.ones(date.shape)*fi['ON (mg/L)'][i_i]*mg_l_n
    tfe_v[:,i_i] = np.ones(date.shape)*fi['Total Iron (ug/L)'][i_i]*mg_l_f*(1./1000)
    alk_v[:,i_i] = np.ones(date.shape)*fi['Total Alkalinity (mg/L)'][i_i]*mg_l_c
    sal_v[:,i_i] = np.ones(date.shape)*fi['Salinity (ppt)'][i_i]
    dfe_v[:,i_i] = np.ones(date.shape)*fi['Total Iron (ug/L)'][i_i]*(1./1000)*mg_l_f*.2

ncf.close()

# make monthly
date_mon = pd.date_range(start='1997-01-01',end='2017-12-31',freq='M')

# time array
timeunit = 'days since 1997-01-01'
timenum = date2num(date_mon.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('mexican_potw_estimates_1997_2017_monthly.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',fi['Plant Name'].shape[0]) # 75 rivers

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
no2_v = ncf.createVariable('NO2',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'C'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'PSU'
dfe_v.units = 'mmol/m3'

tj['date'] = pd.to_datetime(tj['date'])
tj.set_index(tj['date'],inplace=True)
tj_temp_mon = tj['temperature C'].resample('M').mean()

tim_v[:] = timenum
lat_v[:] = fi['lat']
lon_v[:] = fi['lon']

for i_i in range(fi['flow m3/s'].shape[0]):
    flo_v[:,i_i] = np.ones(date_mon.shape)*fi['flow m3/s'][i_i]
    nh4_v[:,i_i] = np.ones(date_mon.shape)*fi['NH4 (mg/L)'][i_i]*mg_l_n
    no3_v[:,i_i] = np.ones(date_mon.shape)*fi['NO3 (mg/L)'][i_i]*mg_l_n
    no2_v[:,i_i] = np.ones(date_mon.shape)*fi['NO2 (mg/L)'][i_i]*mg_l_n
    doo_v[:,i_i] = np.ones(date_mon.shape)*fi['DO (mg/L)'][i_i]*mg_l_o
    tem_v[:,i_i] = np.ones(date_mon.shape)*tj_temp_mon[:-12]
    phh_v[:,i_i] = np.ones(date_mon.shape)*fi['pH'][i_i]
    tpp_v[:,i_i] = np.ones(date_mon.shape)*(fi['PO4 (mg/L)'][i_i]+fi['OP (mg/L)'][i_i])*mg_l_p
    tnn_v[:,i_i] = np.ones(date_mon.shape)*(fi['NO3 (mg/L)'][i_i]+fi['NH4 (mg/L)'][i_i]+fi['NO2 (mg/L)'][i_i])*mg_l_n
    po4_v[:,i_i] = np.ones(date_mon.shape)*fi['PO4 (mg/L)'][i_i]*mg_l_p
    opp_v[:,i_i] = np.ones(date_mon.shape)*fi['OP (mg/L)'][i_i]*mg_l_p
    toc_v[:,i_i] = np.ones(date_mon.shape)*fi['TOC (mg/L)'][i_i]*mg_l_c
    onn_v[:,i_i] = np.ones(date_mon.shape)*fi['ON (mg/L)'][i_i]*mg_l_n
    tfe_v[:,i_i] = np.ones(date_mon.shape)*fi['Total Iron (ug/L)'][i_i]*mg_l_f*(1./1000)
    alk_v[:,i_i] = np.ones(date_mon.shape)*fi['Total Alkalinity (mg/L)'][i_i]*mg_l_c
    sal_v[:,i_i] = np.ones(date_mon.shape)*fi['Salinity (ppt)'][i_i]
    dfe_v[:,i_i] = np.ones(date_mon.shape)*fi['Total Iron (ug/L)'][i_i]*(1./1000)*mg_l_f*.2

ncf.close()
