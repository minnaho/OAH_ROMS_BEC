import sys
sys.path.append('/data/project1/minnaho/river_data/updated_2013_2017/hspfbin/PyHSPF/src/pyhspf/core')
from hbnreader import HBNReader
import pandas as pd
import numpy as np

fi = 'smr-rchDO_v23c.hbn'
df = HBNReader().read(fi)

# Santa margarita river at Ysidora is HSPF reach 105
# values in mg/L
# tuples to pandas df
doo = pd.DataFrame(df['RCHRES'][105]['OXRX']['DOXCONC'],columns=['date','do mg/L'])
bod = pd.DataFrame(df['RCHRES'][105]['OXRX']['BODCONC'],columns=['date','bod mg/L'])
tic = pd.DataFrame(df['RCHRES'][105]['PHCARB']['TIC-CONC'],columns=['date','TIC mg/L'])
phr = pd.DataFrame(df['RCHRES'][105]['PHCARB']['PH'],columns=['date','pH mg/L'])
alk = pd.DataFrame(df['RCHRES'][105]['CONS']['Alkalinity-CONC'],columns=['date','alk mg/L'])
nh4 = pd.DataFrame(df['RCHRES'][105]['NUTRX']['NH4-CONCDIS'],columns=['date','nh4 mg/L'])
no3 = pd.DataFrame(df['RCHRES'][105]['NUTRX']['NO3-CONCDIS'],columns=['date','no3 mg/L'])
no2 = pd.DataFrame(df['RCHRES'][105]['NUTRX']['NO2-CONCDIS'],columns=['date','no2 mg/L'])
po4 = pd.DataFrame(df['RCHRES'][105]['NUTRX']['PO4-CONCDIS'],columns=['date','po4 mg/L'])

# get daily mean
doo.set_index('date',inplace=True)
doo_d = doo.resample('D').mean()
doo_d[doo_d<-1E20] = np.nan

bod.set_index('date',inplace=True)
bod_d = bod.resample('D').mean()
bod_d[bod_d<-1E10] = np.nan

tic.set_index('date',inplace=True)
tic_d = tic.resample('D').mean()
tic_d[tic_d<-1E10] = np.nan

phr.set_index('date',inplace=True)
phr_d = phr.resample('D').mean()
phr_d[phr_d<-1E10] = np.nan

alk.set_index('date',inplace=True)
alk_d = alk.resample('D').mean()
alk_d[alk_d<-1E10] = np.nan

nh4.set_index('date',inplace=True)
nh4_d = nh4.resample('D').mean()
nh4_d[nh4_d<-1E10] = np.nan

no3.set_index('date',inplace=True)
no3_d = no3.resample('D').mean()
no3_d[no3_d<-1E10] = np.nan

no2.set_index('date',inplace=True)
no2_d = no2.resample('D').mean()
no2_d[no2_d<-1E10] = np.nan

po4.set_index('date',inplace=True)
po4_d = po4.resample('D').mean()
po4_d[po4_d<-1E10] = np.nan

# datetimes to put in csv
ai = doo_d.index.date.tolist()

# interpolate missing values
doo_i = np.array(doo_d['do mg/L'][1:].interpolate().values.ravel().tolist())
bod_i = np.array(bod_d['bod mg/L'][1:].interpolate().values.ravel().tolist())
tic_i = np.array(tic_d['TIC mg/L'][1:].interpolate().values.ravel().tolist())
phr_i = np.array(phr_d['pH mg/L'][1:].interpolate().values.ravel().tolist())
alk_i = np.array(alk_d['alk mg/L'].interpolate().values.ravel().tolist())
nh4_i = np.array(nh4_d['nh4 mg/L'].interpolate().values.ravel().tolist())
no3_i = np.array(no3_d['no3 mg/L'].interpolate().values.ravel().tolist())
no2_i = np.array(no2_d['no2 mg/L'].interpolate().values.ravel().tolist())
po4_i = np.array(po4_d['po4 mg/L'].interpolate().values.ravel().tolist())

new = pd.DataFrame({'date':a[1:],'DO mg/L':doo_i,'BOD mg/L':bod_i,'TIC mg/L':tic_i,'pH':phr_i,'alk mg/L':alk_i,'NH4 mg/L':nh4_i,'NO3 mg/L':no3_i,'NO2 mg/L':no2_i,'PO4 mg/L':po4_i},index=None)

new.to_csv('smr_data.csv')


