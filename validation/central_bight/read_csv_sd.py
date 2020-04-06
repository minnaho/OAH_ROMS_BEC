############################
# get agency survey csv data
# and organize into netCDF
##########################
import glob 
import pandas as pd
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import xarray as xr

# get csv files from folder
#csv_files_long = sorted(glob.glob('/mnt/d/Minna/Documents/BGC_model_work/validation/C*.csv'))
#csv_files_long = sorted(glob.glob('/data/project1/minnaho/validation/central_bight/C*.csv'))
csv_files = sorted(glob.glob('/data/project1/minnaho/validation/central_bight/Cen*.csv'))

# get lat/lon csv file
lat_lon_csv = pd.read_csv('Stn_coords.csv',sep=',')

# load in first file to append data to (1998 file)
#df = pd.read_csv(csv_files[0],sep=',',parse_dates=True,encoding='ISO-8859-1')
df = pd.DataFrame()
# append rest of data to first file
for data in csv_files:    
    # load in new data
    print('loading '+data)
    df_new = pd.read_csv(data,sep=',',parse_dates=True,encoding='ISO-8859-1',low_memory=False)

    ##########################################################
    # RENAME ALL DIFFERENT VARIABLE NAMES TO BE ONE VARIABLE 
    # (and change units if necessary)
    ##########################################################    
    # AMMONIA (mg/L)
    if 'Ammonia-N (ug/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Ammonia-N (ug/L)':'ammonia-N'},inplace=True)
        # divide by 1000 to turn ug/L to mg/L
        df_new['ammonia-N'] = df_new['ammonia-N'].apply(lambda x: x*(1./1000))
    if 'Ammonia-N(mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Ammonia-N(mg/L)':'ammonia-N'},inplace=True)
    if 'Ammonia-N(ug/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Ammonia-N(ug/L)':'ammonia-N'},inplace=True)
        # divide by 1000 to turn ug/L to mg/L
        df_new['ammonia-N'] = df_new['ammonia-N'].apply(lambda x: x*(1./1000))
    if 'Ammonia-N (mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Ammonia-N (mg/L)':'ammonia-N'},inplace=True)

    # Beam C (1/m)
    if 'Beam C (1/m)' in df_new.keys():
        df_new.rename(index=str,columns={'Beam C (1/m)':'beam_C'},inplace=True)
    if 'SBE Beam C' in df_new.keys():
        df_new.rename(index=str,columns={'SBE Beam C':'beam_C'},inplace=True)

    # CDOM (ug/L)
    if 'CDOM (ug/L) ' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L) ':'CDOM'},inplace=True)
    if 'CDOM (ug/L)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L)':'CDOM'},inplace=True)
    if 'CDOM(ug/L)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM(ug/L)':'CDOM'},inplace=True)

    if 'CDOM (ug/L) WET ' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L) WET ':'CDOM_WET'},inplace=True)
    if 'CDOM (ug/L) WET' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L) WET':'CDOM_WET'},inplace=True)
    if 'CDOM(ug/L)WET' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM(ug/L)WET':'CDOM_WET'},inplace=True)

    if 'CDOM (ug/L) ECO' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L) ECO':'CDOM_ECO'},inplace=True)
    if 'CDOM ECO (µg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM ECO (µg/L)':'CDOM_ECO'},inplace=True)

    if 'CDOM (ug/L) Turner' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM (ug/L) Turner':'CDOM_Turner'},inplace=True)
    if 'CDOM Turner (µg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Turner (µg/L)':'CDOM_Turner'},inplace=True)

    # CDOM Voltage (V)
    if 'CDOM Voltage (V)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage (V)':'CDOM_voltage'},inplace=True)
    if 'CDOM Voltage (V) ECO' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage (V) ECO':'CDOM_voltage_ECO'},inplace=True)
    if 'CDOM Voltage (V) Turner' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage (V) Turner':'CDOM_voltage_Turner'},inplace=True)
    if 'CDOM Voltage (V) WET' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage (V) WET':'CDOM_voltage_WET'},inplace=True)
    if 'CDOM Voltage ECO (V)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage ECO (V)':'CDOM_voltage_ECO'},inplace=True)
    if 'CDOM Voltage Turner (V)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage Turner (V)':'CDOM_voltage_Turner'},inplace=True)
    if 'CDOM Voltage WET (V)' in df_new.keys():
        df_new.rename(index=str,columns={'CDOM Voltage WET (V)':'CDOM_voltage_WET'},inplace=True)
    if 'Voltage-CDOM' in df_new.keys():
        df_new.rename(index=str,columns={'Voltage-CDOM':'CDOM_voltage'},inplace=True)

    # Chl-a (cholorphyll-a) (ug/L) 
    if 'Chl-a (ug/L)' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chl-a (ug/L)':'Chl-a'},inplace=True)
    if 'Chl-a (ug/L) ECO' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chl-a (ug/L) ECO':'Chl-a_ECO'},inplace=True)
    if 'Chl-a (ug/L) USC/UCLA' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chl-a (ug/L) USC/UCLA':'Chl-a_USC_UCLA'},inplace=True)
    if 'Chl-a USC/UCLA [~$m~#g/L]' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chl-a USC/UCLA [~$m~#g/L]':'Chl-a_USC_UCLA'},inplace=True)
    if 'Chlorophyll-a (æg/L) ECO' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chlorophyll-a (æg/L) ECO':'Chl-a_ECO'},inplace=True)
    if 'Chlorophyll-a ECO (µg/L)' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chlorophyll-a ECO (µg/L)':'Chl-a_ECO'},inplace=True)

    if 'Chlorophyll-a (æg/L) WET' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chlorophyll-a (æg/L) WET':'Chl-a_WET'},inplace=True)
    if 'Chlorophyll-a WET (µg/L)' in df_new.keys(): 
        df_new.rename(index=str,columns={'Chlorophyll-a WET (µg/L)':'Chl-a_WET'},inplace=True)

    # Chlorophyll-a Voltage (V) 
    if 'Chlorophyll-a Voltage (V) ECO' in df_new.keys():
        df_new.rename(index=str,columns={'Chlorophyll-a Voltage (V) ECO':'Chl-a_voltage_ECO'},inplace=True)
    if 'Chlorophyll-a Voltage (V) WET' in df_new.keys():
        df_new.rename(index=str,columns={'Chlorophyll-a Voltage (V) WET':'Chl-a_voltage_WET'},inplace=True)
    if 'Chlorophyll-a Voltage ECO (V)' in df_new.keys():
        df_new.rename(index=str,columns={'Chlorophyll-a Voltage ECO (V)':'Chl-a_voltage_ECO'},inplace=True)
    if 'Chlorophyll-a Voltage WET (V)' in df_new.keys():
        df_new.rename(index=str,columns={'Chlorophyll-a Voltage WET (V)':'Chl-a_voltage_WET'},inplace=True)
    if 'Voltage-Chl-a' in df_new.keys():
        df_new.rename(index=str,columns={'Voltage-Chl-a':'Chl-a_voltage_ECO'},inplace=True)
    
    # conductivity (S/m)
    if 'Conductivity (S/m)' in df_new.keys():
        df_new.rename(index=str,columns={'Conductivity (S/m)':'conductivity'},inplace=True)

    # Density (kg/m3) (specific density)
    if 'Density (kg/m?)' in df_new.keys():
        df_new.rename(index=str,columns={'Density (kg/m?)':'specific_density'},inplace=True)
    if 'Density (kg/m³)' in df_new.keys():
        df_new.rename(index=str,columns={'Density (kg/m³)':'specific_density'},inplace=True)
    if 'Density (å-theta)' in df_new.keys():
        df_new.rename(index=str,columns={'Density (å-theta)':'specific_density'},inplace=True)

    # Depth (m)
    if 'Depth (m)' in df_new.keys():
        df_new.rename(index=str,columns={'Depth (m)':'depth'},inplace=True)
    if 'Depth(m)' in df_new.keys():
        df_new.rename(index=str,columns={'Depth(m)':'depth'},inplace=True)

    # Discrete chl-a (ug/L)
    if 'Disacrete Chl-a (ug/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Disacrete Chl-a (ug/L)':'Chl-a_discrete'},inplace=True)
    if 'Discrete Chlorophyll-a (µg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Discrete Chlorophyll-a (µg/L)':'Chl-a_discrete'},inplace=True)

    # E. coli (MPN/100mL)
    if 'E.coli(MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'E.coli(MPN)':'E_coli'},inplace=True)
    if 'E. coli (MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'E. coli (MPN)':'E_coli'},inplace=True)
    if 'E. coli (MPN/100mL)' in df_new.keys():
        df_new.rename(index=str,columns={'E. coli (MPN/100mL)':'E_coli'},inplace=True)
   
    # Enterococci (MPN/100mL)
    if 'Enterococci (MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'Enterococci (MPN)':'Enterococci'},inplace=True)
    if 'Enterococci (MPN/100mL)' in df_new.keys():
        df_new.rename(index=str,columns={'Enterococci (MPN/100mL)':'Enterococci'},inplace=True)
    if 'Enterococci(MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'Enterococci(MPN)':'Enterococci'},inplace=True)
    if 'Enterococci(MPN100/mL)' in df_new.keys():
        df_new.rename(index=str,columns={'Enterococci(MPN100/mL)':'Enterococci'},inplace=True)

    # Fecal Coliform (MPN/100mL)
    if 'Fecal Colif. (MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'Fecal Colif. (MPN)':'fecal_coliforms'},inplace=True)
    if 'Fecal coliforms (MPN/100mL)' in df_new.keys():
        df_new.rename(index=str,columns={'Fecal coliforms (MPN/100mL)':'fecal_coliforms'},inplace=True)

    # Field Rep (unknown units)
    if 'Field Rep' in df_new.keys():
        df_new.rename(index=str,columns={'Field Rep':'field_rep'},inplace=True)
    if 'Field rep' in df_new.keys():
        df_new.rename(index=str,columns={'Field rep':'field_rep'},inplace=True)
    if 'Field.Rep' in df_new.keys():
        df_new.rename(index=str,columns={'Field.Rep':'field_rep'},inplace=True)

    # Normalized Irradiance (%)
    if 'Irradiance (% Norm)' in df_new.keys():
        df_new.rename(index=str,columns={'Irradiance (% Norm)':'irradiance_norm'},inplace=True)
    if 'Normalized Irradiance (%)' in df_new.keys():
        df_new.rename(index=str,columns={'Normalized Irradiance (%)':'irradiance_norm'},inplace=True)

    # Irradiance (µE/cm²·sec)
    if 'Irradiance' in df_new.keys():
        df_new.rename(index=str,columns={'Irradiance':'irradiance'},inplace=True)
    if 'Irradiance (µE/cm²·sec)' in df_new.keys():
        df_new.rename(index=str,columns={'Irradiance (µE/cm²·sec)':'irradiance'},inplace=True)
    if 'Irradiance (æE/cmýúsec)' in df_new.keys():
        df_new.rename(index=str,columns={'Irradiance (æE/cmýúsec)':'irradiance'},inplace=True)

    # latitude/longitude
    if 'Latitude (Dec. Degree)' in df_new.keys():
        df_new.rename(index=str,columns={'Latitude (Dec. Degree)':'latitude'},inplace=True)
    if 'Longitude (Dec. Degree)' in df_new.keys():
        df_new.rename(index=str,columns={'Longitude (Dec. Degree)':'longitude'},inplace=True)

    # Light transmission (%)
    if 'Light Transmission (%)' in df_new.keys(): 
        df_new.rename(index=str,columns={'Light Transmission (%)':'light_transmission'},inplace=True)

    # dissolved oxygen (mg/L)
    if 'Dissolved Oxygen (mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Dissolved Oxygen (mg/L)':'dissolved_oxygen'},inplace=True)
    if 'Oxygen (mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Oxygen (mg/L)':'dissolved_oxygen'},inplace=True)

    # oxygen saturation
    if 'Oxygen Saturation (%)' in df_new.keys():
        df_new.rename(index=str,columns={'Oxygen Saturation (%)':'oxygen_saturation_percent'},inplace=True)
    if 'Oxygen Saturation (mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'Oxygen Saturation (mg/L)':'oxygen_saturation_mg_L'},inplace=True)
    if 'SBE DO sat (%)' in df_new.keys():
        df_new.rename(index=str,columns={'SBE DO sat (%)':'oxygen_saturation_percent'},inplace=True)
    if 'SBE DO sat (mg/L)' in df_new.keys():
        df_new.rename(index=str,columns={'SBE DO sat (mg/L)':'oxygen_saturation_mg_L'},inplace=True)

    # salinity (psu)
    if 'Salinity (psu)' in df_new.keys():
        df_new.rename(index=str,columns={'Salinity (psu)':'salinity'},inplace=True)

    # stability (kg/m3/m)
    if 'Stability (E)' in df_new.keys():
        df_new.rename(index=str,columns={'Stability (E)':'stability'},inplace=True)
    if 'Stability (kg/m?/m)' in df_new.keys():
        df_new.rename(index=str,columns={'Stability (kg/m?/m)':'stability'},inplace=True)
    if 'Stability (kg/m³/m)' in df_new.keys():
        df_new.rename(index=str,columns={'Stability (kg/m³/m)':'stability'},inplace=True)

    # station ID
    if 'Station ID' in df_new.keys():
        df_new.rename(index=str,columns={'Station ID':'station_ID'},inplace=True)
    if 'Station.ID' in df_new.keys():
        df_new.rename(index=str,columns={'Station.ID':'station_ID'},inplace=True)

    # surface irradiance (µE/cm²·sec)
    if 'Surface Irradiance' in df_new.keys():
        df_new.rename(index=str,columns={'Surface Irradiance':'surface_irradiance'},inplace=True)
    if 'Surface Irradiance (µE/cm²·sec)' in df_new.keys():
        df_new.rename(index=str,columns={'Surface Irradiance (µE/cm²·sec)':'surface_irradiance'},inplace=True)
    if 'Surface Irradiance (æE/cmýúsec)' in df_new.keys():
        df_new.rename(index=str,columns={'Surface Irradiance (æE/cmýúsec)':'surface_irradiance'},inplace=True)

    # temperature C
    if 'Temperature (°C)' in df_new.keys():
        df_new.rename(index=str,columns={'Temperature (°C)':'temperature'},inplace=True)
    if 'Temperature (øC)' in df_new.keys():
        df_new.rename(index=str,columns={'Temperature (øC)':'temperature'},inplace=True)
    if 'Temperature(C)' in df_new.keys():
        df_new.rename(index=str,columns={'Temperature(C)':'temperature'},inplace=True)

    # time (s)
    if 'Time' in df_new.keys():
        df_new.rename(index=str,columns={'Time':'time'},inplace=True)
    if 'Time (s)' in df_new.keys():
        df_new.rename(index=str,columns={'Time (s)':'time_seconds'},inplace=True)
    if 'Time (seconds)' in df_new.keys():
        df_new.rename(index=str,columns={'Time (seconds)':'time_seconds'},inplace=True)

    # total coliform (MPN)
    if 'Total Colif. (MPN)' in df_new.keys():
        df_new.rename(index=str,columns={'Total Colif. (MPN)':'total_coliforms'},inplace=True)
    if 'Total coliforms (MPN/100mL)' in df_new.keys():
        df_new.rename(index=str,columns={'Total coliforms (MPN/100mL)':'total_coliforms'},inplace=True)

    # transmissivity (%)
    if 'Transmissivity (%)' in df_new.keys():
        df_new.rename(index=str,columns={'Transmissivity (%)':'transmissivity'},inplace=True)
    
    # delta T (°C/m)
    if 'delta T' in df_new.keys():
        df_new.rename(index=str,columns={'delta T':'delta_T'},inplace=True)
    if 'delta-T  (°C/m)' in df_new.keys():
        df_new.rename(index=str,columns={'delta-T  (°C/m)':'delta_T'},inplace=True)
    if 'delta-T (øC/m)' in df_new.keys():
        df_new.rename(index=str,columns={'delta-T (øC/m)':'delta_T'},inplace=True)

    # pH
    if 'pH (pH units)' in df_new.keys():
        df_new.rename(index=str,columns={'pH (pH units)':'pH'},inplace=True)


    # only 1 variation of name, so rename to remove units
    df_new.rename(index=str,columns={'Descent rate (m/s)':'descent_rate'},inplace=True)

    #####################################################
    # append dataframes to make 1 file of all time periods
    ######################################################
    df = df.append(df_new,ignore_index=True) 


# remove columns of NaNs
df = df.drop(['Unnamed: 25','Unnamed: 26','Unnamed: 27','Unnamed: 28','Unnamed: 29','Qual_EC','Qual_ENT','Qual_FC','Qual_NH3','Qual_TC','Void','Ammonia QA Batch','field_rep'],axis=1)


# get all pandas columns/series that are object type and convert to float
objs_other = ['E_coli','fecal_coliforms','total_coliforms']

objs_space = ['salinity','CDOM','CDOM_WET','descent_rate','specific_density','oxygen_saturation_percent','dissolved_oxygen']

for series in objs_other:
    df[series] = df[series].apply(lambda x: float(str(x).replace('>','')) if str(x).startswith('>') else x)
    df[series] = df[series].apply(lambda x: float(str(x).replace('<','')) if str(x).startswith('<') else x)
    df[series] = df[series].apply(lambda x: float(str(x).replace('-1','0')))
    df[series] = pd.to_numeric(df[series])

for series in objs_space:
    df[series] = df[series].apply(lambda x: float(str(x).replace(' ',str(np.nan))) if str(x).startswith(' ') else x)
    df[series] = pd.to_numeric(df[series])

# remove spaces from Date
df['Date'] = df['Date'].apply(lambda x: str(x).replace(' ','') if str(x).startswith(' ') else x)
# parse dates (put them in right format/datetime format)
df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y')

###############################
# find lat/lon for each station 
###############################
'''
lats_array = np.empty(len(df['latitude']))
lons_array = np.empty(len(df['longitude']))
for i,loc in enumerate(df['station_ID']):
    print('find lat/lon for '+str(i)+' in '+str(len(df['station_ID'])))
    ind = lat_lon_csv['Station'][lat_lon_csv['Station']==str(loc)].index[0]
    lat = lat_lon_csv['Latitude'][ind]
    lon = lat_lon_csv['Longitude'][ind]
    lats_array[i] = lat
    lons_array[i] = lon

np.save('latitude.npy',lats_array)
np.save('longitude.npy',lons_array)
'''
lats_array = np.load('latitude.npy')
lons_array = np.load('longitude.npy')


# assign df['latitude'] and df['longitude'] 
# with values in lats_list and lons_list
df['latitude'] = lats_array
df['longitude'] = lons_array

df = df.drop(['station_ID','Agency','Season','Sort','time','time_seconds'],axis=1)

# convert dates to numbers for netcdf
dt_units = 'days since 1996-01-16'
date_list = list(df['Date'])
dates_nc = date2num(date_list,dt_units)
df['date'] = np.copy(dates_nc)
df = df.drop(['Date'],axis=1)

########################
# append san diego data
########################
df_sd = pd.read_csv('SDall.csv',low_memory=False,parse_dates=['Date'])
sd_stn = pd.read_csv('SD_StationCoordinates.csv')

# dates
sd_datelist = list(df_sd['Date'])
sd_datenum = date2num(sd_datelist,dt_units)

df_sd.rename(index=str,columns={'Date':'date'},inplace=True)
df_sd['date'] = np.copy(sd_datenum)

# variables

df_sd.rename(index=str,columns={'Depth_m':'depth'},inplace=True)
df_sd.rename(index=str,columns={'Temperature_degC':'temperature'},inplace=True)
df_sd.rename(index=str,columns={'Salinity_psu':'salinity'},inplace=True)
df_sd.rename(index=str,columns={'Density_kg_m3':'specific_density'},inplace=True)
df_sd.rename(index=str,columns={'pH_pH_units':'pH'},inplace=True)
df_sd.rename(index=str,columns={'Dissolved_Oxygen_mg_L':'dissolved_oxygen'},inplace=True)

df_sd.rename(index=str,columns={'Light_Transmission_pc':'light_transmission'},inplace=True)
df_sd.rename(index=str,columns={'BeamC_1_m':'beam_C'},inplace=True)
df_sd.rename(index=str,columns={'Chlorophyll_a_ug_L_WET':'Chl-a'},inplace=True)
df_sd.rename(index=str,columns={'Chlorophyll_a_Voltage_V_WET':'Chl-a_voltage_WET'},inplace=True)
df_sd.rename(index=str,columns={'CDOM_ug-L_WET':'CDOM'},inplace=True)

# locations
sd_lat = np.empty((len(df_sd['Station'])))
sd_lon = np.empty((len(df_sd['Station'])))
for s_i in range(len(df_sd['Station'])):
    print(str(s_i)+' of '+str(len(df_sd['Station'])))
    sd_lat[s_i] = sd_stn['latitude'][np.where(df_sd['Station'][s_i]==sd_stn['station'])[0][0]] 
    sd_lon[s_i] = sd_stn['longitude'][np.where(df_sd['Station'][s_i]==sd_stn['station'])[0][0]] 

df_sd['latitude'] = sd_lat
df_sd['longitude'] = sd_lon

df_sd = df_sd.drop(['Station','Agency','Month','Season','Year','Time','Field_rep','Descent_rate_m_s','Time_seconds','Conductivity_S_m','Oxygen_Saturation_mg_L','Oxygen_Saturation_pc','CDOM_Voltage_V_WET'],axis=1)

df = df.append(df_sd,ignore_index=True)
###############
# CREATE NETCDF
###############

#df = df.set_index(['date','longitude','latitude','depth'])
ds = df.astype('float32')
#xrs = ds.to_xarray()
xrs = xr.Dataset(ds)
#xrs.reset_index('dim_0',inplace=True)

xrs.to_netcdf('central_bight_master_database_1998_2019_1D_sd.nc')

'''
xrs = xr.Dataset.from_dataframe(df)
xrs.to_netcdf('central_bight_master_database_1998_2017.nc')
'''

'''
#####################
# make netCDF file
####################
f = Dataset('central_bight_database.nc','w')

# dimensions
time = f.createDimension('time',None)
station = f.createDimension('station',None)
depth = f.createDimension('depth',None)

# variables
times = f.createVariable('time',np.float64,('time',))
depths = f.createVariable('depth',np.float32,('depth',))

lats = f.createVariable('latitude',np.float32,('lat',))
lons = f.createVariable('longitude',np.float32,('lon',))

temp     = f.createVariable('temperature',np.float32,('time','station','depth'))
cond     = f.createVariable('conductivity',np.float32,('time','station','depth'))
pH       = f.createVariable('pH',np.float32,('time','station','depth'))
oxygen   = f.createVariable('oxygen',np.float32,('time','station','depth'))
trans    = f.createVariable('transmissivity',np.float32,('time','station','depth'))
salinity = f.createVariable('salinity',np.float32,('time','station','depth'))
dens     = f.createVariable('specific_density',np.float32,('time','station','depth'))
time_s   = f.createVariable('time_seconds',np.float32,('time','station','depth'))
desc     = f.createVariable('descent_rate',np.float32,('time','station','depth'))
SBE_DO   = f.createVariable('SBE_DO',np.float32,('time','station','depth'))
SBE_beam = f.createVariable('SBE_Beam',np.float32,('time','station','depth'))
chl-a    = f.createVariable('chl-a',np.float32,('time','station','depth'))
CDOM     = f.createVariable('CDOM',np.float32,('time','station','depth'))
ammonia  = f.createVariable('ammonia-N',np.float32,('time','station','depth'))
total_colif = f.createVariable('total_colif',np.float32,('time','station','depth'))
fecal_colif = f.createVariable('fecal_colif',np.float32,('time','station','depth'))
e_coli      = f.createVariable('E.coli',np.float32,('time','station','depth'))
enterococci = f.createVariable('enterococci',np.float32,('time','station','depth'))

'''
