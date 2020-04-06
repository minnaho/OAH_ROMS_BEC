import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from netCDF4 import Dataset,num2date,date2num

chem_monthly_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
hourly_data = '/data/project1/minnaho/validation/ocsd_george_robertson/hourly_effluent/OCSD_hourly_effluent_minna_edits.xlsx' 

# read in ocsd hourly data
df_raw = pd.read_excel(hourly_data,sheet_name=0,header=None,skiprows=1,usecols='A,C:D')

# strip time
date_str = np.array(df_raw[0].astype(str))

date_no_hr_l = []
for d_i in date_str:
    date_no_hr_l.append(dt.datetime.strptime(d_i,'%Y-%m-%d'))

date_no_hr = np.array(date_no_hr_l)

date_hr_l = []
for d_i in range(len(date_no_hr)):
    add_hours = dt.timedelta(hours=float(df_raw[2][d_i]))
    date_hr_l.append(date_no_hr[d_i] + add_hours)

date_hr = np.array(date_hr_l)

# convert MGD to m3/s
conv = 0.0438126157 # 1000000 gal/day * 1 day/86400 s * 0.00378541 m3/1 gal
flow_gal_day = np.array(df_raw[3])
flow_m3_s = flow_gal_day*conv

# get chemical data from potw input forcing file
chem_data = Dataset(chem_monthly_path,'r')
chem_time_num = np.array(chem_data.variables['time'])
time_units = chem_data.variables['time'].units

chem_time_dat = num2date(chem_time_num,time_units)

# get start and end for hourly data to find in monthly data
hr_st_yr = date_hr[0].year
hr_st_m = date_hr[0].month
hr_en_yr = date_hr[-1].year
hr_en_m = date_hr[-1].month

for d_i in range(len(chem_time_dat)):
    if chem_time_dat[d_i].year == hr_st_yr and chem_time_dat[d_i].month == hr_st_m:
        ind_st = d_i
    if chem_time_dat[d_i].year == hr_en_yr and chem_time_dat[d_i].month == hr_en_m:
        ind_en = d_i

# 2 is location index of OCSD
chem_vars = ['NO3','NH4','NO2','PO4','Fe','ON','OP','alkalinity','pH','sulfate','temperature','salinity','dissolved_oxygen']
# make netcdf
ocsd = Dataset('ocsd_hourly.nc','w')

time_dim = ocsd.createDimension('time',None)
time_var = ocsd.createVariable('time',np.float32,('time'))
time_var.units = 'hours since 1999-01-31 00:00'
time_var[:] = date2num(date_hr,time_var.units)

flow_var = ocsd.createVariable('flow',np.float64,('time'))
flow_var[:] = flow_m3_s
flow_var.units = 'm3/s'

print('filling ocsd hourly data')
for v_i in range(len(chem_vars)):
    print(chem_vars[v_i])
    t_d = 0
    var_ocsd = ocsd.createVariable(chem_vars[v_i],np.float64,('time')) 
    if chem_vars[v_i] != 'pH':
        var_ocsd.units = chem_data.variables[chem_vars[v_i]].units
    for d_i in range(len(date_hr)):
        if date_hr[d_i].month == chem_time_dat[ind_st+t_d].month:
            var_ocsd[d_i] = chem_data.variables[chem_vars[v_i]][ind_st+t_d,2,2] 
        elif date_hr[d_i].month != chem_time_dat[ind_st+t_d].month:
            #print(str(date_hr[d_i].month),str(chem_time_dat[ind_st+t_d].month))
            t_d += 1
            var_ocsd[d_i] = chem_data.variables[chem_vars[v_i]][ind_st+t_d,2,2] 
        
ocsd.close()            


# find missing dates and fix chronological order
#ocsd_unique = np.unique(date_no_hr)
# create daily dates from beginning of ocsd time to amount of continuous days
#test = pd.date_range(ocsd_unique[0],periods=ocsd_unique.shape[0]).to_pydatetime()
# compare 
#err = np.where(ocsd_unique!=test)
# to find missing/wrong dates after initial wrong dates,
# delete missing dates from test, append future dates at endk
# ex.
# >>> test2[2673]
#datetime.datetime(2006, 6, 8, 0, 0)
#>>> test2 = list(test1)
#>>> len(test2)
#6064
#>>> test2[2889]
#datetime.datetime(2007, 1, 11, 0, 0)
#>>> del test2[2889]
#>>> test2[-1]
#datetime.datetime(2015, 9, 20, 0, 0)
#>>> test2.append(dt.datetime(2015,9,21))
#>>> len(test2)
#6064
#>>> test1 = np.array(test2)
#>>> np.where(ocsd_unique==test1)
#(array([   0,    1,    2, ..., 3211, 3212, 3213]),)
#>>> np.where(ocsd_unique!=test1)
#(array([3214, 3215, 3216, ..., 6061, 6062, 6063]),)
#>>> ocsd_unique[3212:3215]
#array([datetime.datetime(2007, 12, 1, 0, 0),
#       datetime.datetime(2007, 12, 2, 0, 0),
#       datetime.datetime(2008, 1, 1, 0, 0)], dtype=object)
#>>> ocsd_unique[3212:3216]
#array([datetime.datetime(2007, 12, 1, 0, 0),
#       datetime.datetime(2007, 12, 2, 0, 0),
#       datetime.datetime(2008, 1, 1, 0, 0),
#       datetime.datetime(2008, 1, 2, 0, 0)], dtype=object)
#>>> ocsd_unique[3215]
#datetime.datetime(2008, 1, 2, 0, 0)
#>>> ocsd_unique[3214]
#datetime.datetime(2008, 1, 1, 0, 0)
#>>> ocsd_unique[3214:].shape
#(2850,)
#>>> test3 = pd.date_range(pd.datetime(2008,1,1,0,0),periods=2850).to_pydatetime()




