# turn hourly LA river flow to daily
import numpy as np
import pandas as pd

path = '/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/'
fi = '/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/hourly_flow_2002_2018_los_angeles_river.csv'

riv = pd.read_csv(fi,header=None,skiprows=2)
form = '%m/%d/%Y %H:%M:%S'
riv[0] = pd.to_datetime(riv[0]+' '+riv[1],format=form)
riv.set_index(riv[0],inplace=True)

del riv[1]
del riv[3]

daily = riv.resample('D').mean()

daily_2007_2018 = daily['2007':'2018']

df = pd.DataFrame({'flow cfs':daily_2007_2018[2]})
df.to_csv(path+'daily_flow_2007_2018_los_angeles_river.txt')

# supplemental flow data
fi = 'Supplemental Flow Data.xlsx'
xl = pd.ExcelFile(fi)
# gauged data

frank_hour = pd.read_excel(xl,sheet_name='FK00',header=None,skiprows=1,nrows=49264,usecols='D,F')
frank_hour.set_index(pd.to_datetime(frank_hour[3]),inplace=True)
frank_dail = frank_hour.resample('D').mean()
frank_dail[5][frank_dail[5]<0]=np.nan
frank_dail[5] = frank_dail[5]/1000 # L/s to m3/s
frank_dail['2007':].to_csv('franklin_creek_daily_2007_2008.csv')

gavio_hour = pd.read_excel(xl,sheet_name='GV01',header=None,skiprows=1,nrows=114632,usecols='C,D')
gavio_hour.set_index(pd.to_datetime(gavio_hour[2]),inplace=True)
gavio_dail = gavio_hour.resample('D').mean()
gavio_dail[3][gavio_dail[3]<0]=np.nan
gavio_dail[3] = gavio_dail[3]/1000 # L/s to m3/s
gavio_dail['2007':].to_csv('gaviota_creek_daily_2007_2016.csv')

burro_hour = pd.read_excel(xl,sheet_name='AB00',header=None,skiprows=1,nrows=139170,usecols='C:E')
burro_hour.set_index(pd.to_datetime(burro_hour[2]+' '+burro_hour[3]),inplace=True)
burro_dail = burro_hour.resample('D').mean()
burro_dail[4][burro_dail[4]<0]=np.nan
burro_dail[4] = burro_dail[4]/1000 # L/s to m3/s
burro_dail['2007':].to_csv('arroyo_burro_creek_daily_2007_2018.csv')

rinco_hour = pd.read_excel(xl,sheet_name='RN01',header=None,skiprows=1,usecols='B,D')
rinco_hour.set_index(pd.to_datetime(rinco_hour[1]),inplace=True)
rinco_dail = rinco_hour.resample('D').mean()
rinco_dail[3][rinco_dail[3]<0]=np.nan
rinco_dail[3] = rinco_dail[3]/1000 # L/s to m3/s
rinco_dail['2007':].to_csv('rincon_creek_daily_2007_2008.csv')

# new river Bell Canyon
bellc_hour = pd.read_excel(xl,sheet_name='BC02',header=None,skiprows=1,nrows=114342,usecols='C,E,F')
bellc_hour.set_index(pd.to_datetime(bellc_hour[2]),inplace=True)
bellc_dail = bellc_hour.resample('D').mean()
bellc_dail[4][bellc_dail[4]<0]=np.nan
bellc_dail[5][bellc_dail[5]<0]=np.nan
bellc_dail[4] = bellc_dail[4]/1000 # L/s to m3/s
bellc_dail['2001':'2017'].to_csv('bell_canyon_daily_2004_2018.csv')

# new river Arroyo Honda
honda_hour = pd.read_excel(xl,sheet_name='HO00',header=None,skiprows=1,nrows=122411,usecols='C,E,F')
honda_hour.set_index(pd.to_datetime(honda_hour[2]),inplace=True)
honda_dail = honda_hour.resample('D').mean()
honda_dail[4][honda_dail[4]<0]=np.nan
honda_dail[5][honda_dail[5]<0]=np.nan
honda_dail[4] = honda_dail[4]/1000 # L/s to m3/s
honda_dail['2001':'2017'].to_csv('arroyo_honda_creek_daily_2001_2018.csv')

# new river Refugio Creek
refug_hour = pd.read_excel(xl,sheet_name='RG01',header=None,skiprows=1,nrows=131169,usecols='C,E,F')
refug_hour.set_index(pd.to_datetime(refug_hour[2]),inplace=True)
refug_dail = refug_hour.resample('D').mean()
refug_dail[4][refug_dail[4]<0]=np.nan
refug_dail[5][refug_dail[5]<0]=np.nan
refug_dail[4] = refug_dail[4]/1000 # L/s to m3/s
refug_dail['2001':'2017'].to_csv('refugio_creek_daily_2001_2018.csv')
