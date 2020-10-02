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
fol = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/formatted/'
fnames = sorted(glob.glob(fol+'*'))

# get potw minor names
# order of potw minors in netcdf will be alphabetical
rnames = []
for f_i in fnames:
    rnames.append(f_i[85:f_i.index('.xl')])

example = pd.read_excel(fnames[0],sheet_name='reordered',header=None,skiprows=1)
#example[0][0] = '01/01/2007' # set first time to 01/01/2007
example[0] = pd.to_datetime(example[0]) # make dates index to resample to daily
example.set_index(0,inplace=True)
example.loc[pd.to_datetime('2007-01-01')] = example.loc['2007-01-31']
daily_ex = example.resample('D').bfill()

df = daily_ex.loc['2007-01-01':'2017-12-31']

# make arrays
tim_arr = np.arange(0,df.shape[0])

lat_arr = np.empty((len(fnames)))
lon_arr = np.empty((len(fnames)))
flo_arr = np.empty((df.shape[0],len(fnames)))
nh4_arr = np.empty((df.shape[0],len(fnames)))
no3_arr = np.empty((df.shape[0],len(fnames)))
doo_arr = np.empty((df.shape[0],len(fnames)))
tem_arr = np.empty((df.shape[0],len(fnames)))
bod_arr = np.empty((df.shape[0],len(fnames)))
phh_arr = np.empty((df.shape[0],len(fnames)))
tpp_arr = np.empty((df.shape[0],len(fnames)))
po4_arr = np.empty((df.shape[0],len(fnames)))
opp_arr = np.empty((df.shape[0],len(fnames)))
toc_arr = np.empty((df.shape[0],len(fnames)))
onn_arr = np.empty((df.shape[0],len(fnames)))
tfe_arr = np.empty((df.shape[0],len(fnames)))
sil_arr = np.empty((df.shape[0],len(fnames)))
alk_arr = np.empty((df.shape[0],len(fnames)))
sal_arr = np.empty((df.shape[0],len(fnames)))
dfe_arr = np.empty((df.shape[0],len(fnames)))

mgd_to_m3s = 0.043812645072430365

# mg/L to mmol/m3
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855

# loop through files
for f_i in range(len(fnames)):
    # read file
    dat_fi = pd.read_excel(fnames[f_i],sheet_name='reordered',header=None,skiprows=1)
    # make monthly into daily data
    dat_fi[0] = pd.to_datetime(dat_fi[0]) # make dates index to resample to daily
    dat_fi.set_index(0,inplace=True)
    try:
        dat_fi.loc[pd.to_datetime('2007-01-01')] = dat_fi.loc['2007-01-31']
    except:
        dat_fi.loc[pd.to_datetime('2007-01-01')] = np.nan
        dat_fi['2007-01-01'] = dat_fi.loc['2007-01-31']
    dat_fi = dat_fi.resample('D').bfill()
    # get only 2007-01-01 - 2017-12-31
    dat_fi = dat_fi['2007-01-01':'2017-12-31']
    # assign values
    lat_arr[f_i] = dat_fi[18][0]
    lon_arr[f_i] = dat_fi[19][0]
    flo_arr[:,f_i] = np.array(dat_fi[1]).astype(float)*mgd_to_m3s
    nh4_arr[:,f_i] = np.array(dat_fi[2].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_n
    no3_arr[:,f_i] = np.array(dat_fi[3]).astype(float)*mg_l_n
    doo_arr[:,f_i] = np.array(dat_fi[4]).astype(float)*mg_l_o
    tem_arr[:,f_i] = np.array(dat_fi[5]).astype(float)
    bod_arr[:,f_i] = np.array(dat_fi[6]).astype(float)*mg_l_o
    phh_arr[:,f_i] = np.array(dat_fi[7]).astype(float)
    tpp_arr[:,f_i] = np.array(dat_fi[8]).astype(float)*mg_l_p
    po4_arr[:,f_i] = np.array(dat_fi[9]).astype(float)*mg_l_p
    opp_arr[:,f_i] = np.array(dat_fi[10]).astype(float)*mg_l_p
    toc_arr[:,f_i] = np.array(dat_fi[11]).astype(float)*mg_l_p
    onn_arr[:,f_i] = np.array(dat_fi[12].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_c
    tfe_arr[:,f_i] = (np.array(dat_fi[13]).astype(float)*mg_l_f)/1000
    sil_arr[:,f_i] = np.array(dat_fi[14]).astype(float)*mg_l_s
    alk_arr[:,f_i] = np.array(dat_fi[15]).astype(float)*mg_l_c
    sal_arr[:,f_i] = np.array(dat_fi[16]).astype(float)
    dfe_arr[:,f_i] = (np.array(dat_fi[17]).astype(float)*mg_l_f)/1000

# time array
timeunit = 'days since 2007-01-01'
timenum = date2num(dat_fi.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('minor_potw_2007_2017.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 19 minor potws

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
bod_v = ncf.createVariable('BOD',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total P',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic P',np.float64,('time','location'))
toc_v = ncf.createVariable('total organic C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'mmol/m3'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'mmol/m3'
bod_v.units = 'mmol/m3'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
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
doo_v[:,:] = doo_arr
tem_v[:,:] = tem_arr
bod_v[:,:] = bod_arr
phh_v[:,:] = phh_arr
tpp_v[:,:] = tpp_arr
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

