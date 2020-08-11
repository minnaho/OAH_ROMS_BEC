# extend south_coast_rivers_10_years_monthly_new.nc
# to have 1997-2010 data (14 years)
import numpy as np
from netCDF4 import Dataset,date2num
import pandas as pd
import datetime as datetime
import time

# read in 2007-2010 river data
order_files = ['monthly_flow_2007_2010_san_juan_creek.txt','monthly_flow_2007_2010_san_jose_creek.txt','monthly_flow_2007_2010_san_diego_river.txt','monthly_flow_2007_2010_atascadero_creek.txt','monthly_flow_2007_2010_santa_margarita.txt','monthly_flow_2007_2010_santa_clara.txt','monthly_flow_2007_2010_los_penasquitos_lagoon.txt','monthly_flow_2007_2010_ventura_river.txt','monthly_flow_2007_2010_calleguas_creek.txt']

# 48 for 4 years of data 
ft3_to_m3 = 0.02831685
usgs_rivs = np.empty((len(order_files),48))
for f_i in range(len(order_files)):
    usgs_rivs[f_i] = pd.read_csv(order_files[f_i],header=None,sep='\t',comment='#')[6][2:].astype(float)*ft3_to_m3

# timeperiod
date_months_pd = pd.date_range(start='1997-01-01',end='2010-12-01',freq='MS')
date_months_l = []

for i in range(len(date_months_pd)):
    date_months_l.append(datetime.datetime(date_months_pd[i].year,date_months_pd[i].month,date_months_pd[i].day))

date_months = np.array(date_months_l)
t_unit = 'days since 1997-01-01'
time_nc = date2num(date_months,t_unit)

nc10 = Dataset('south_coast_rivers_10_years_monthly_new.nc','r')
lat10 = np.array(nc10.variables['latitude'][0])
lon10 = np.array(nc10.variables['longitude'][0])
flo10 = np.array(nc10.variables['flow'])
nh410 = np.array(nc10.variables['ammonium'])
no310 = np.array(nc10.variables['nitrate'])
po410 = np.array(nc10.variables['phosphate'])
tnn10 = np.array(nc10.variables['total_nitrogen'])
tpp10 = np.array(nc10.variables['total_phosphorus'])
alk10 = np.array(nc10.variables['alkalinity'])
tem10 = np.array(nc10.variables['temperature'])

# order
# san juan creek, san jose creek,san diego river,Atascadero Creek,santa margarita,
# santa clara,los penasquitos,ventura,calleguas
ind_usgs = [0,1,3,7,15,20,26,30,36]

f0 = Dataset('south_coast_rivers_updated_14_years_1997_2010_monthly.nc','w')

# details about bight/usgs data
f0.title = 'Southern California Bight Coastal River Data, 10 years of data'
f0.source = 'Southern California Bight \'08 Data, USGS Gauge data'
f0.history = 'Created '+time.ctime(time.time())
f0.description = 'Rivers in this data set: 154-San_Juan_Crk, 345-Goleta_SanJose, 350-Montecito, 237-SanDiegoR, 257-Sweetwater, 109-Solstice Canyon, 32-LARiver, 345-Goleta_Atascadero, 189-Salt Creek, 98-little Sycamore, 34-StaAnaRiver, 119-Pena Canyon, 177-Moro Canyon, 85-Ballona_Crk, 262-Tijuana, Santa Margarita River, 143-LAHarbor, 116-Tuna Canyon, 351-Rincon, 317-Marie Canyon, 45-Santa_Clara, 91-Santa Monica Canyon, 210-Aliso Canyon, 108-Las Flores Canyon, 267-MissionBay, 288-Otay, 256-LPL(Los Penasquitos), 331-Encinas, 95- Arroyo Sequit, 141-SanDiegoCrk, 7-VenturaRiv, 130-RedondoBchKingHarbor, 354-Mission Creek, 112-Walnut Canyon, 101-Trancas canyon, 111-Carbon Canyon, 37-Calleguas, 36-SanGabrielR, 201-SanLuisReyR, 227-AguaHedionda, 221-BuenaVista, 224-EscondidoCrk, 206-LasFlores, 217-SanDieguito, 199-SanOnofreCrk, 225-SanMarcosCrk, 279-TecoloteCrk, 287-Chollas-Crk, USGS data for: Santa Margarita River, San Diego River, Calleguas Creek, Santa Clara River, Los Penasquitos Lagoon, San Jose Creek, Ventura River, San Juan Creek, Atascadero Creek' 

time_c = f0.createDimension('time',None)
lat_c = f0.createDimension('lat',flo10.shape[1])
lon_c = f0.createDimension('lon',flo10.shape[1])

times_c = f0.createVariable('time',np.float64,('time',))
lats_c = f0.createVariable('latitude',np.float32,('lat',))
lons_c = f0.createVariable('longitude',np.float32,('lon',))

flow_c = f0.createVariable('flow',np.float32,('time','lat','lon'))
NH4_c = f0.createVariable('ammonium',np.float32,('time','lat','lon'))
NO3_c = f0.createVariable('nitrate',np.float32,('time','lat','lon'))
PO4_c = f0.createVariable('phosphate',np.float32,('time','lat','lon'))
TN_c = f0.createVariable('total_nitrogen',np.float32,('time','lat','lon'))
TP_c = f0.createVariable('total_phosphorus',np.float32,('time','lat','lon'))
alk_c = f0.createVariable('alkalinity',np.float32,('time','lat','lon'))
temp_c = f0.createVariable('temperature',np.float32,('time','lat','lon'))

times_c.units = 'days since 1997-1-1'
lats_c.units = 'degrees north'
lons_c.units = 'degrees east'
flow_c.units = 'm3/s'
NH4_c.units = 'mmol/m3'
PO4_c.units = 'mmol/m3'
NO3_c.units = 'mmol/m3'
TN_c.units = 'mmol/m3'
TP_c.units = 'mmol/m3'
alk_c.units = 'mmol/m3'
temp_c.units = 'degrees Celsius'

times_c[:] = time_nc
lons_c[:] = lon10
lats_c[:] = lat10

u_i = 0
for r_i in range(flo10.shape[1]):
    if r_i in ind_usgs:
        flow_c[:,r_i,r_i] = np.array(list(flo10[:,r_i,r_i])+list(usgs_rivs[u_i]))
        u_i += 1
    else:
        flow_c[:,r_i,r_i] = np.array(list(flo10[:12,r_i,r_i])*14)
    NH4_c[:,r_i,r_i] = np.array(list(flo10[:12,r_i,r_i])*14)
    NO3_c[:,r_i,r_i] = np.array(list(no310[:12,r_i,r_i])*14)
    PO4_c[:,r_i,r_i] = np.array(list(po410[:12,r_i,r_i])*14)
    TN_c[:,r_i,r_i]  = np.array(list(tnn10[:12,r_i,r_i])*14)
    TP_c[:,r_i,r_i]  = np.array(list(tpp10[:12,r_i,r_i])*14)
    alk_c[:,r_i,r_i] = np.array(list(alk10[:12,r_i,r_i])*14)
    temp_c[:,r_i,r_i] = np.array(list(tem10[:12,r_i,r_i])*14)

f0.close()
