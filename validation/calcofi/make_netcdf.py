import numpy as np
from netCDF4 import Dataset
import pandas as pd

time_units = 'minutes since 1949-03-01 09:30:00'

data_df = pd.read_csv('calcofi_database.csv',header=None)

data_points = len(data_df[1][1:])

data_nc = Dataset('calcofi_database.nc','w')
data_nc.title = 'CalCOFI Sampling Cast and Bottle Database 1949-2017'
data_nc.description = '1-D data, each variable index matches with each other'

# 1D netCDF
index = data_nc.createDimension('index',data_points)

# variables
time_nc         = data_nc.createVariable('time',np.float64,('index'))
lat_nc          = data_nc.createVariable(data_df.iloc[0][2],np.float32,('index'))
lon_nc          = data_nc.createVariable(data_df.iloc[0][3],np.float32,('index'))
vis_nc          = data_nc.createVariable(data_df.iloc[0][4],np.float32,('index'))
cloud_amt_nc    = data_nc.createVariable(data_df.iloc[0][5],np.float32,('index'))
cloud_typ_nc    = data_nc.createVariable(data_df.iloc[0][6],np.float32,('index'))
weather_nc      = data_nc.createVariable(data_df.iloc[0][7],np.float32,('index'))
wet_air_T_nc    = data_nc.createVariable(data_df.iloc[0][8],np.float32,('index'))
dry_air_T_nc    = data_nc.createVariable(data_df.iloc[0][9],np.float32,('index'))
atmo_press_nc   = data_nc.createVariable(data_df.iloc[0][10],np.float32,('index'))
wind_sp_nc      = data_nc.createVariable(data_df.iloc[0][11],np.float32,('index'))
wind_dir_nc     = data_nc.createVariable(data_df.iloc[0][12],np.float32,('index'))
wave_per_nc     = data_nc.createVariable(data_df.iloc[0][13],np.float32,('index'))
wave_ht_nc      = data_nc.createVariable(data_df.iloc[0][14],np.float32,('index'))
wave_dir_nc     = data_nc.createVariable(data_df.iloc[0][15],np.float32,('index'))
int_prod_nc     = data_nc.createVariable(data_df.iloc[0][16],np.float32,('index'))
int_chl_nc      = data_nc.createVariable(data_df.iloc[0][17],np.float32,('index'))
bot_depth_nc    = data_nc.createVariable(data_df.iloc[0][18],np.float32,('index'))
depth_nc        = data_nc.createVariable(data_df.iloc[0][19],np.float32,('index'))
temp_nc         = data_nc.createVariable(data_df.iloc[0][20],np.float32,('index'))
salt_nc         = data_nc.createVariable(data_df.iloc[0][21],np.float32,('index'))
O2_nc           = data_nc.createVariable(data_df.iloc[0][22],np.float32,('index'))
pot_dens_nc     = data_nc.createVariable(data_df.iloc[0][23],np.float32,('index'))
O2_sat_nc       = data_nc.createVariable(data_df.iloc[0][24],np.float32,('index'))
chla_nc         = data_nc.createVariable(data_df.iloc[0][25],np.float32,('index'))
phaeophytin_nc  = data_nc.createVariable(data_df.iloc[0][26],np.float32,('index'))
PO4_nc          = data_nc.createVariable(data_df.iloc[0][27],np.float32,('index'))
SiO3_nc         = data_nc.createVariable(data_df.iloc[0][28],np.float32,('index'))
NO2_nc          = data_nc.createVariable(data_df.iloc[0][29],np.float32,('index'))
NO3_nc          = data_nc.createVariable(data_df.iloc[0][30],np.float32,('index'))
NH3_nc          = data_nc.createVariable(data_df.iloc[0][31],np.float32,('index'))
carb_nc         = data_nc.createVariable(data_df.iloc[0][32],np.float32,('index'))
light_nc        = data_nc.createVariable(data_df.iloc[0][33],np.float32,('index'))
DIC_nc          = data_nc.createVariable(data_df.iloc[0][34],np.float32,('index'))
alk_nc          = data_nc.createVariable(data_df.iloc[0][35],np.float32,('index'))
pH_nc           = data_nc.createVariable(data_df.iloc[0][36],np.float32,('index'))

# units
time_nc.units         = data_df[0][1][data_df[0][1].index('=')+2:]
lat_nc.units          = data_df[0][2][data_df[0][2].index('=')+2:]
lon_nc.units          = data_df[0][3][data_df[0][1].index('=')+2:]
vis_nc.units          = '1 Digit Code from The World Meteorological Organization.  Code source WMO 4300, see http://www.jodc.go.jp/data_format/weather-code.html'
cloud_amt_nc.units    = '1 Digit Code from The World Meteorological Organization.  Code source WMO 2700, see http://www.jodc.go.jp/data_format/weather-code.html'
cloud_typ_nc.units    = '1 Digit Code from The World Meteorological Organization.  Code source WMO 0500, see http://www.jodc.go.jp/data_format/weather-code.html'
weather_nc.units      = '1 Digit Code from The World Meteorological Organization.  Code source WMO 4501, see http://www.jodc.go.jp/data_format/weather-code.html'
wet_air_T_nc.units    = data_df[0][31][data_df[0][31].index('=')+2:]
dry_air_T_nc.units    = data_df[0][30][data_df[0][30].index('=')+2:]
atmo_press_nc.units   = data_df[0][29][data_df[0][29].index('=')+2:]
wind_sp_nc.units      = data_df[0][28][data_df[0][28].index('=')+2:]
wind_dir_nc.units     = data_df[0][27][data_df[0][27].index('=')+2:]
wave_per_nc.units     = data_df[0][26][data_df[0][26].index('=')+2:]
wave_ht_nc.units      = data_df[0][25][data_df[0][25].index('=')+2:]
wave_dir_nc.units     = data_df[0][24][data_df[0][24].index('=')+2:]
int_prod_nc.units     = data_df[0][23][data_df[0][23].index('=')+2:]
int_chl_nc.units      = data_df[0][22][data_df[0][22].index('=')+2:]
bot_depth_nc.units    = data_df[0][21][data_df[0][21].index('=')+2:]
depth_nc.units        = data_df[0][4][data_df[0][4].index('=')+2:]
temp_nc.units         = data_df[0][5][data_df[0][5].index('=')+2:]
salt_nc.units         = data_df[0][6][data_df[0][6].index('=')+2:]
O2_nc.units           = data_df[0][7][data_df[0][7].index('=')+2:]
pot_dens_nc.units     = data_df[0][8][data_df[0][8].index('=')+2:]
O2_sat_nc.units       = data_df[0][9][data_df[0][9].index('=')+2:]
chla_nc.units         = data_df[0][10][data_df[0][10].index('=')+2:]
phaeophytin_nc.units  = data_df[0][11][data_df[0][11].index('=')+2:]
PO4_nc.units          = data_df[0][12][data_df[0][12].index('=')+2:]
SiO3_nc.units         = data_df[0][13][data_df[0][13].index('=')+2:]
NO2_nc.units          = data_df[0][14][data_df[0][14].index('=')+2:]
NO3_nc.units          = data_df[0][15][data_df[0][15].index('=')+2:]
NH3_nc.units          = data_df[0][16][data_df[0][16].index('=')+2:]
carb_nc.units         = data_df[0][17][data_df[0][17].index('=')+2:]
light_nc.units        = data_df[0][18][data_df[0][18].index('=')+2:]
DIC_nc.units          = data_df[0][19][data_df[0][19].index('=')+2:]
alk_nc.units          = data_df[0][20][data_df[0][20].index('=')+2:]

# assign values
time_nc[:]         = np.array(data_df[1][1:]).astype('float')
lat_nc[:]          = np.array(data_df[2][1:]).astype('float')
lon_nc[:]          = np.array(data_df[3][1:]).astype('float')
vis_nc[:]          = np.array(data_df[4][1:]).astype('float')
cloud_amt_nc[:]    = np.array(data_df[5][1:]).astype('float')
cloud_typ_nc[:]    = np.array(data_df[6][1:]).astype('float')
weather_nc[:]      = np.array(data_df[7][1:]).astype('float')
wet_air_T_nc[:]    = np.array(data_df[8][1:]).astype('float')
dry_air_T_nc[:]    = np.array(data_df[9][1:]).astype('float')
atmo_press_nc[:]   = np.array(data_df[10][1:]).astype('float')
wind_sp_nc[:]      = np.array(data_df[11][1:]).astype('float')
wind_dir_nc[:]     = np.array(data_df[12][1:]).astype('float')
wave_per_nc[:]     = np.array(data_df[13][1:]).astype('float')
wave_ht_nc[:]      = np.array(data_df[14][1:]).astype('float')
wave_dir_nc[:]     = np.array(data_df[15][1:]).astype('float')
int_prod_nc[:]     = np.array(data_df[16][1:]).astype('float')
int_chl_nc[:]      = np.array(data_df[17][1:]).astype('float')
bot_depth_nc[:]    = np.array(data_df[18][1:]).astype('float')
depth_nc[:]        = np.array(data_df[19][1:]).astype('float')
temp_nc[:]         = np.array(data_df[20][1:]).astype('float')
salt_nc[:]         = np.array(data_df[21][1:]).astype('float')
O2_nc[:]           = np.array(data_df[22][1:]).astype('float')
pot_dens_nc[:]     = np.array(data_df[23][1:]).astype('float')
O2_sat_nc[:]       = np.array(data_df[24][1:]).astype('float')
chla_nc[:]         = np.array(data_df[25][1:]).astype('float')
phaeophytin_nc[:]  = np.array(data_df[26][1:]).astype('float')
PO4_nc[:]          = np.array(data_df[27][1:]).astype('float')
SiO3_nc[:]         = np.array(data_df[28][1:]).astype('float')
NO2_nc[:]          = np.array(data_df[29][1:]).astype('float')
NO3_nc[:]          = np.array(data_df[30][1:]).astype('float')
NH3_nc[:]          = np.array(data_df[31][1:]).astype('float')
carb_nc[:]         = np.array(data_df[32][1:]).astype('float')
light_nc[:]        = np.array(data_df[33][1:]).astype('float')
DIC_nc[:]          = np.array(data_df[34][1:]).astype('float')
alk_nc[:]          = np.array(data_df[35][1:]).astype('float')
pH_nc[:]           = np.array(data_df[36][1:]).astype('float')

data_nc.close()
