###############################
# turn river data from
# daily to monthly
# by taking average every month
###############################
import xarray as xr
import subprocess

nc_file1 = 'south_coast_rivers_24_years_new.nc'
nc_file1_mo = 'south_coast_rivers_24_years_monthly_new.nc'
f1 = xr.open_dataset(nc_file1)
monthly_data1 = f1.resample(freq='m',dim='time',how='mean')
monthly_data1.to_netcdf(nc_file1_mo)


nc_file2 = 'south_coast_rivers_10_years_no_watershed_new.nc'
nc_file2_mo = 'south_coast_rivers_10_years_monthly_new.nc'
f2 = xr.open_dataset(nc_file2)
monthly_data2 = f2.resample(freq='m',dim='time',how='mean')
monthly_data2.to_netcdf(nc_file2_mo)


######################
# edit monthly .nc file
# with descriptions of units,
# title, etc
#######################

# 10 years data
subprocess.call('ncatted -a units,\'temperature\',c,c,\'degrees Celsius\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'flow\',c,c,\'m3/s\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'ammonium\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'nitrate\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'phosphate\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'total_nitrogen\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'total_phosphorus\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 
subprocess.call('ncatted -a units,\'alkalinity\',c,c,\'mmol/m3\' '+nc_file2_mo,shell=True) 

subprocess.call('ncatted -a title,global,a,c,\'Southern California Bight Coastal River Data, 10 years of data\' '+nc_file2_mo,shell=True)

subprocess.call('ncatted -a source,global,a,c,\'Southern California Bight \'08 Data, USGS Gauge data\' '+nc_file2_mo,shell=True)

#subprocess.call('ncatted -a description,global,a,c,\'Rivers in this data set: 341-LAHarbor, 154-San_Juan_Crk, 151-LAHarbor, 345-Goleta_SanJose, 350-Montecito, 237-SanDiegoR, 257-Sweetwater, 109-Solstice Canyon, 32-LARiver, 345-Goleta_Atascadero, 189-Salt Creek, 98-little Sycamore, 34-StaAnaRiver, 119-Pena Canyon, 177-Moro Canyon, 85-Ballona_Crk, 262-Tijuana, Santa Margarita River, 143-LAHarbor, 285-MissionBay, 116-Tuna Canyon, 351-Rincon, 317-Marie Canyon, 45-Santa_Clara, 91-Santa Monica Canyon, 210-Aliso Canyon, 108-Las Flores Canyon, 267-MissionBay, 288-Otay, 256-LPL(Los Penasquitos), 331-Encinas, 95- Arroyo Sequit, 141-SanDiegoCrk, 7-VenturaRiv, 130-RedondoBchKingHarbor, 354-Mission Creek, 112-Walnut Canyon, 101-Trancas canyon, 111-Carbon Canyon, 37-Calleguas, 36-SanGabrielR, 201-SanLuisReyR, 227-AguaHedionda, 221-BuenaVista, 224-EscondidoCrk, 206-LasFlores, 217-SanDieguito, 199-SanOnofreCrk, 225-SanMarcosCrk, 279-TecoloteCrk, 287-Chollas-Crk\' south_coast_rivers_10_years_monthly.nc',shell=True) 

# 24 years data
subprocess.call('ncatted -a units,\'temperature\',c,c,\'degrees Celsius\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'flow\',c,c,\'m3/s\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'ammonium\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'nitrate\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'phosphate\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'total_nitrogen\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'total_phosphorus\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 
subprocess.call('ncatted -a units,\'alkalinity\',c,c,\'mmol/m3\' '+nc_file1_mo,shell=True) 

subprocess.call('ncatted -a title,global,a,c,\'Southern California Bight Coastal River Data, 24 years of data\' '+nc_file1_mo,shell=True)

subprocess.call('ncatted -a source,global,a,c,\'Rational Methods, Ashmita Sengupta\'s model\' '+nc_file1_mo,shell=True)

#subprocess.call('ncatted -a description,global,a,c,\'Rivers in this data set: Arroyo Trabuco, Bolsa Chica Westminster Channel, Bonita Creek, Carpinteria, Costa Mesa Chanel, Coyote Creek, Cristianitos Creek, Devereux Lagoon, Dominguez, E Garden Grove Wintersberg Channel, Goleta Tecolotito, Laguna Canyon, Malibu Creek, Prima Desch, Revolon, San Mateo, San Pedro Creek, Santa Ana Delhi, Segunda Desch, Topanga, Zuma Canyon, Arroyo Burro, Canada de la Gaviota, Franklin Creek\' south_coast_rivers_24_years_monthly.nc',shell=True) 


