###############################
# take 2007-2017 minor potw monthly data
# and turn to netcdf
# for psource model input
##############################
import numpy as np
from netCDF4 import Dataset,date2num
import pandas as pd
import glob
import datetime as datetime

# path to files
fol = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/'
fnames = sorted(glob.glob(fol+'*.csv'))

# get potw minor names
# order of potw minors in netcdf will be alphabetical
rnames = []
for f_i in fnames:
    rnames.append(f_i[75:f_i.index('_1971')])

# mg/L to mmol/m3
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855
mg_l_a = 1000/100.09 # mg/L CaCO3 to mmol/m3

example = pd.read_csv(fnames[0])
#example[0][0] = '01/01/2007' # set first time to 01/01/2007
example['date'] = pd.to_datetime(example['date']) # make dates index to resample to daily
example.set_index('date',inplace=True)
example.loc[pd.to_datetime('1971-01-01')] = np.nan
example.loc['1971-01-01'] = example.loc['1971-01-31']
#example.loc[pd.to_datetime('1971-01-01')] = example.loc['1971-01-31']
daily_ex = example.resample('D').bfill()

df = daily_ex.loc['1971':'2017']

# make arrays
tim_arr = np.arange(0,df.shape[0])

lat_arr = np.empty((len(fnames)))
lon_arr = np.empty((len(fnames)))
flo_arr = np.empty((df.shape[0],len(fnames)))
nh4_arr = np.empty((df.shape[0],len(fnames)))
no3_arr = np.empty((df.shape[0],len(fnames)))
no2_arr = np.empty((df.shape[0],len(fnames)))
doo_arr = np.empty((df.shape[0],len(fnames)))
tem_arr = np.empty((df.shape[0],len(fnames)))
bod_arr = np.empty((df.shape[0],len(fnames)))
phh_arr = np.empty((df.shape[0],len(fnames)))
tpp_arr = np.empty((df.shape[0],len(fnames)))
tnn_arr = np.empty((df.shape[0],len(fnames)))
po4_arr = np.empty((df.shape[0],len(fnames)))
opp_arr = np.empty((df.shape[0],len(fnames)))
toc_arr = np.empty((df.shape[0],len(fnames)))
onn_arr = np.empty((df.shape[0],len(fnames)))
tfe_arr = np.empty((df.shape[0],len(fnames)))
sil_arr = np.empty((df.shape[0],len(fnames)))
alk_arr = np.empty((df.shape[0],len(fnames)))
sal_arr = np.empty((df.shape[0],len(fnames)))
dfe_arr = np.empty((df.shape[0],len(fnames)))

# 1971-2017
tim_mon = np.arange(0,564)

lat_mon = np.empty((len(fnames)))
lon_mon = np.empty((len(fnames)))
flo_mon = np.empty((tim_mon.shape[0],len(fnames)))
nh4_mon = np.empty((tim_mon.shape[0],len(fnames)))
no3_mon = np.empty((tim_mon.shape[0],len(fnames)))
no2_mon = np.empty((tim_mon.shape[0],len(fnames)))
doo_mon = np.empty((tim_mon.shape[0],len(fnames)))
tem_mon = np.empty((tim_mon.shape[0],len(fnames)))
bod_mon = np.empty((tim_mon.shape[0],len(fnames)))
phh_mon = np.empty((tim_mon.shape[0],len(fnames)))
tpp_mon = np.empty((tim_mon.shape[0],len(fnames)))
tnn_mon = np.empty((tim_mon.shape[0],len(fnames)))
po4_mon = np.empty((tim_mon.shape[0],len(fnames)))
opp_mon = np.empty((tim_mon.shape[0],len(fnames)))
toc_mon = np.empty((tim_mon.shape[0],len(fnames)))
onn_mon = np.empty((tim_mon.shape[0],len(fnames)))
tfe_mon = np.empty((tim_mon.shape[0],len(fnames)))
sil_mon = np.empty((tim_mon.shape[0],len(fnames)))
alk_mon = np.empty((tim_mon.shape[0],len(fnames)))
sal_mon = np.empty((tim_mon.shape[0],len(fnames)))
dfe_mon = np.empty((tim_mon.shape[0],len(fnames)))

mgd_to_m3s = 0.043812645072430365


# loop through files
for f_i in range(len(fnames)):
    # read file
    dat_fi = pd.read_csv(fnames[f_i])
    # make monthly into daily data
    dat_fi['date'] = pd.to_datetime(dat_fi['date']) # make dates index to resample to daily
    dat_fi.set_index('date',inplace=True)
    dat_fi.loc[pd.to_datetime('1971-01-01')] = np.nan

    dat_fi.loc['1971-01-01'] = dat_fi.loc['1971-01-31']
        
    dat_fi = dat_fi.resample('D').interpolate()
    dat_fi = dat_fi.resample('D').bfill()
    dat_fi = dat_fi.resample('D').ffill()
    dat_fi = dat_fi.interpolate()
    dat_fi = dat_fi.bfill()

    # get only 1997-01-01 - 2017-12-31
    dat_fi = dat_fi['1971-01-01':'2017-12-31']
    #dat_fi[2] = dat_fi[2].replace(to_replace=' ',value=np.nan).astype(float)
    #dat_fi[12] = dat_fi[12].replace(to_replace=' ',value=np.nan).astype(float)
    # assign values
    lat_arr[f_i] = dat_fi['lat'][0]
    lon_arr[f_i] = dat_fi['lon'][0]
    flo_arr[:,f_i] = np.array(dat_fi['flow mgd']).astype(float)*mgd_to_m3s
    nh4_arr[:,f_i] = np.array(dat_fi['NH4 mg/L']).astype(float)*mg_l_n
    no3_arr[:,f_i] = np.array(dat_fi['NO3 mg/L']).astype(float)*mg_l_n
    no2_arr[:,f_i] = np.array(dat_fi['NO2 mg/L']).astype(float)*mg_l_n
    doo_arr[:,f_i] = np.array(dat_fi['dissolved oxygen mg/L']).astype(float)*mg_l_o
    tem_arr[:,f_i] = np.array(dat_fi['temperature C']).astype(float)
    bod_arr[:,f_i] = np.array(dat_fi['BOD mg/L']).astype(float)*mg_l_o
    phh_arr[:,f_i] = np.array(dat_fi['pH']).astype(float)
    tpp_arr[:,f_i] = np.array(dat_fi['TP mg/L']).astype(float)*mg_l_p
    po4_arr[:,f_i] = np.array(dat_fi['PO4 mg/L']).astype(float)*mg_l_p
    opp_arr[:,f_i] = np.array(dat_fi['OP mg/L']).astype(float)*mg_l_p
    toc_arr[:,f_i] = np.array(dat_fi['TOC mg/L']).astype(float)*mg_l_c
    onn_arr[:,f_i] = np.array(dat_fi['ON mg/L'].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_n
    tnn_arr[:,f_i] = np.nansum((nh4_arr[:,f_i],no3_arr[:,f_i],no2_arr[:,f_i],onn_arr[:,f_i]),axis=0)
    tfe_arr[:,f_i] = (np.array(dat_fi['total iron ug/L']).astype(float)*mg_l_f)/1000
    sil_arr[:,f_i] = np.array(dat_fi['SiO4 mg/L']).astype(float)*mg_l_s
    alk_arr[:,f_i] = np.array(dat_fi['Alk mg/L']).astype(float)*mg_l_a
    sal_arr[:,f_i] = np.array(dat_fi['Salinity PSU']).astype(float)
    # 20% of total
    dfe_arr[:,f_i] = (np.array(dat_fi['total iron ug/L']).astype(float)*mg_l_f*.2)/1000

    # assign monthly values
    dat_mon = dat_fi.resample('M').mean()
    lat_mon[f_i] = dat_mon['lat'][0]
    lon_mon[f_i] = dat_mon['lon'][0]
    flo_mon[:,f_i] = np.array(dat_mon['flow mgd']).astype(float)*mgd_to_m3s
    nh4_mon[:,f_i] = np.array(dat_mon['NH4 mg/L']).astype(float)*mg_l_n
    no3_mon[:,f_i] = np.array(dat_mon['NO3 mg/L']).astype(float)*mg_l_n
    no2_mon[:,f_i] = np.array(dat_mon['NO2 mg/L']).astype(float)*mg_l_n
    doo_mon[:,f_i] = np.array(dat_mon['dissolved oxygen mg/L']).astype(float)*mg_l_o
    tem_mon[:,f_i] = np.array(dat_mon['temperature C']).astype(float)
    bod_mon[:,f_i] = np.array(dat_mon['BOD mg/L']).astype(float)*mg_l_o
    phh_mon[:,f_i] = np.array(dat_mon['pH']).astype(float)
    tpp_mon[:,f_i] = np.array(dat_mon['TP mg/L']).astype(float)*mg_l_p
    po4_mon[:,f_i] = np.array(dat_mon['PO4 mg/L']).astype(float)*mg_l_p
    opp_mon[:,f_i] = np.array(dat_mon['OP mg/L']).astype(float)*mg_l_p
    toc_mon[:,f_i] = np.array(dat_mon['TOC mg/L']).astype(float)*mg_l_c
    onn_mon[:,f_i] = np.array(dat_mon['ON mg/L'].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_n
    tnn_mon[:,f_i] = np.nansum((nh4_mon[:,f_i],no3_mon[:,f_i],no2_mon[:,f_i],onn_mon[:,f_i]),axis=0)
    tfe_mon[:,f_i] = (np.array(dat_mon['total iron ug/L']).astype(float)*mg_l_f)/1000
    sil_mon[:,f_i] = np.array(dat_mon['SiO4 mg/L']).astype(float)*mg_l_s
    alk_mon[:,f_i] = np.array(dat_mon['Alk mg/L']).astype(float)*mg_l_a
    sal_mon[:,f_i] = np.array(dat_mon['Salinity PSU']).astype(float)
    # 20% of total
    dfe_mon[:,f_i] = (np.array(dat_mon['total iron ug/L']).astype(float)*mg_l_f*.2)/1000

# time array
timeunit = 'days since 1971-01-01'
timenum = date2num(dat_fi.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('../major_potw_data/major_potw_1971_2017.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 4 major potws

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
no2_v = ncf.createVariable('NO2',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
bod_v = ncf.createVariable('BOD',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
no2_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'mmol/m3'
bod_v.units = 'mmol/m3'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'mmol/m3'
dfe_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_arr
lon_v[:] = lon_arr
flo_v[:,:] = flo_arr
nh4_v[:,:] = nh4_arr
no3_v[:,:] = no3_arr
no2_v[:,:] = no2_arr
doo_v[:,:] = doo_arr
tem_v[:,:] = tem_arr
bod_v[:,:] = bod_arr
phh_v[:,:] = phh_arr
tpp_v[:,:] = tpp_arr
tnn_v[:,:] = tnn_arr
po4_v[:,:] = po4_arr
opp_v[:,:] = opp_arr
toc_v[:,:] = toc_arr
onn_v[:,:] = onn_arr
tfe_v[:,:] = tfe_arr
sil_v[:,:] = sil_arr
alk_v[:,:] = alk_arr
sal_v[:,:] = sal_arr
dfe_v[:,:] = dfe_arr

ncf.close()

writer = pd.ExcelWriter('../major_potw_data/major_potw_1971_2017.xlsx')

# print to excel file
for p_i in range(flo_arr.shape[1]):
    df = pd.DataFrame({'date':dat_fi.index.date,
    'flow m3/s':flo_arr[:,p_i],
    'NH4 mmol/m3':nh4_arr[:,p_i],
    'NO3 mmol/m3':no3_arr[:,p_i],
    'NO2 mmol/m3':no2_arr[:,p_i],
    'DO mmol/m3':doo_arr[:,p_i],
    'temperature C':tem_arr[:,p_i],
    'BOD mmol/m3':bod_arr[:,p_i],
    'pH':phh_arr[:,p_i],
    'TP mmol/m3':tpp_arr[:,p_i],
    'PO4 mmol/m3':po4_arr[:,p_i],
    'OP mmol/m3':opp_arr[:,p_i],
    'TOC mmol/m3':toc_arr[:,p_i],
    'ON mmol/m3':onn_arr[:,p_i],
    'TN mmol/m3':tnn_arr[:,p_i],
    'total Fe mmol/m3':tfe_arr[:,p_i],
    'SiO4 mmol/m3':sil_arr[:,p_i],
    'Alk mmol/m3':alk_arr[:,p_i],
    'salinity PSU':sal_arr[:,p_i],
    'dissolved Fe mmol/m3':dfe_arr[:,p_i],
    'latitude':lat_arr[p_i],
    'longitude':lon_arr[p_i]},index=None,columns=None)
    df.to_excel(writer,sheet_name=rnames[p_i])

writer.save()

# monthly
timenum = date2num(dat_mon.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('../major_potw_data/major_potw_1971_2017_monthly.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_mon.shape[0]) # 19 minor potws

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
no2_v = ncf.createVariable('NO2',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
bod_v = ncf.createVariable('BOD',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'mmol/m3'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
no2_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'mmol/m3'
bod_v.units = 'mmol/m3'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'mmol/m3'
dfe_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_mon
lon_v[:] = lon_mon
flo_v[:,:] = flo_mon
nh4_v[:,:] = nh4_mon
no3_v[:,:] = no3_mon
no2_v[:,:] = no2_mon
doo_v[:,:] = doo_mon
tem_v[:,:] = tem_mon
bod_v[:,:] = bod_mon
phh_v[:,:] = phh_mon
tpp_v[:,:] = tpp_mon
tnn_v[:,:] = tnn_mon
po4_v[:,:] = po4_mon
opp_v[:,:] = opp_mon
toc_v[:,:] = toc_mon
onn_v[:,:] = onn_mon
tfe_v[:,:] = tfe_mon
sil_v[:,:] = sil_mon
alk_v[:,:] = alk_mon
sal_v[:,:] = sal_mon
dfe_v[:,:] = dfe_mon

ncf.close()

writer = pd.ExcelWriter('../major_potw_data/major_potw_1971_2017_monthly.xlsx')

# print to excel file
for p_i in range(flo_mon.shape[1]):
    df = pd.DataFrame({'date':dat_mon.index.date,
    'flow m3/s':flo_mon[:,p_i],
    'NH4 mmol/m3':nh4_mon[:,p_i],
    'NO3 mmol/m3':no3_mon[:,p_i],
    'NO2 mmol/m3':no2_mon[:,p_i],
    'DO mmol/m3':doo_mon[:,p_i],
    'temperature C':tem_mon[:,p_i],
    'BOD mmol/m3':bod_mon[:,p_i],
    'pH':phh_mon[:,p_i],
    'TP mmol/m3':tpp_mon[:,p_i],
    'PO4 mmol/m3':po4_mon[:,p_i],
    'OP mmol/m3':opp_mon[:,p_i],
    'TOC mmol/m3':toc_mon[:,p_i],
    'ON mmol/m3':onn_mon[:,p_i],
    'TN mmol/m3':tnn_mon[:,p_i],
    'total Fe mmol/m3':tfe_mon[:,p_i],
    'SiO4 mmol/m3':sil_mon[:,p_i],
    'Alk mmol/m3':alk_mon[:,p_i],
    'salinity PSU':sal_mon[:,p_i],
    'dissolved Fe mmol/m3':dfe_mon[:,p_i],
    'latitude':lat_arr[p_i],
    'longitude':lon_arr[p_i]},index=None,columns=None)
    df.to_excel(writer,sheet_name=rnames[p_i])

writer.save()

np.where(np.isnan(flo_arr))
np.where(np.isnan(nh4_arr))
np.where(np.isnan(no3_arr))
np.where(np.isnan(no2_arr))
np.where(np.isnan(doo_arr))
np.where(np.isnan(tem_arr))
np.where(np.isnan(bod_arr))
np.where(np.isnan(phh_arr))
np.where(np.isnan(tpp_arr))
np.where(np.isnan(tnn_arr))
np.where(np.isnan(po4_arr))
np.where(np.isnan(opp_arr))
np.where(np.isnan(toc_arr))
np.where(np.isnan(onn_arr))
np.where(np.isnan(tfe_arr))
np.where(np.isnan(sil_arr))
np.where(np.isnan(alk_arr))
np.where(np.isnan(sal_arr))
np.where(np.isnan(dfe_arr))

np.where(np.isnan(flo_mon))
np.where(np.isnan(nh4_mon))
np.where(np.isnan(no3_mon))
np.where(np.isnan(no2_mon))
np.where(np.isnan(doo_mon))
np.where(np.isnan(tem_mon))
np.where(np.isnan(bod_mon))
np.where(np.isnan(phh_mon))
np.where(np.isnan(tpp_mon))
np.where(np.isnan(tnn_mon))
np.where(np.isnan(po4_mon))
np.where(np.isnan(opp_mon))
np.where(np.isnan(toc_mon))
np.where(np.isnan(onn_mon))
np.where(np.isnan(tfe_mon))
np.where(np.isnan(sil_mon))
np.where(np.isnan(alk_mon))
np.where(np.isnan(sal_mon))
np.where(np.isnan(dfe_mon))
