#######################
# make major inputs
# for 2013-2017
# hyperion, jwppc, ocsd, plwtp
########################
from netCDF4 import Dataset,num2date,date2num
import numpy as np
import pandas as pd
import datetime as datetime

oldf = Dataset('../run_1997_2000/major_potw_data_newocsd.nc','r')

newf = Dataset('major_potw_data_2013_2017.nc','w')

# read goleta data
mgd_to_m3s = 0.043812645072430365
mgL_to_mmolm3 = 1000./14 #mg/L N to mmol/m3 N
mgL_do = 1000./16 # mg/L O to mmol/m3 O
mgL_c = 1000./12 # mg/L C to mmol/m3 C
mgL_p = 1000./30.97 # mg/L C to mmol/m3 C

# get datetime
ind_end = 5*12 # 48 monthly points for 4 years 2013-2016
gdf = pd.read_excel('OO17-Goleta_2013_2017.xlsx',header=None)

# datetime
gd_dat_l = []
for d_i in range(1,len(gdf[0][1:ind_end+1])+1):
    gd_dat_l.append(gdf[0][d_i].to_pydatetime())

gd_dat = np.array(gd_dat_l)

# monthly 2013-2017
numdat = date2num(gd_dat,'days since 2013-01-01')
nummon = len(numdat)


############
# hyperion
############
skipr = 7
htp_df = pd.read_excel('NPDESMonitoringData_CA0109991_HTP.xlsx',header=None,skiprows=skipr)
#flow
htp_fl_noninterp = htp_df[20][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan).astype(float)*mgd_to_m3s
htp_fl = np.array(htp_fl_noninterp.interpolate().values.ravel().tolist())
# ammonia
htp_nh = np.array(htp_df[29][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C','NODI: Q'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(htp_nh)
xp = ok.ravel().nonzero()[0]
fp = htp_nh[~np.isnan(htp_nh)]
x  = np.isnan(htp_nh).ravel().nonzero()[0]
htp_nh[np.isnan(htp_nh)] = np.interp(x, xp, fp)
# take mean of max/min for pH
htp_ph = np.nanmean((np.array(htp_df[80][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float),np.array(htp_df[81][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)),axis=0)
# temperature
htp_tm = (np.array(htp_df[73][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)-32)/1.8
# dissolved oxygen
htp_do = np.array(htp_df[37][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_do
# total organic carbon
htp_tc = np.array(htp_df[14][182-skipr:ind_end+182-skipr].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_c

# data that is only collected every 3 months
# total organic nitrogen
htp_tn = np.empty((htp_fl.shape[0]))
htp_tn.fill(np.nan)
htp_tn[2::3] = np.array(htp_df[84][247-skipr:247-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
# interpolate missing values
ok = ~np.isnan(htp_tn)
xp = ok.ravel().nonzero()[0]
fp = htp_tn[~np.isnan(htp_tn)]
x  = np.isnan(htp_tn).ravel().nonzero()[0]
htp_tn[np.isnan(htp_tn)] = np.interp(x, xp, fp)
# total phosphorus
htp_tp = np.empty((htp_fl.shape[0]))
htp_tp.fill(np.nan)
htp_tp[2::3] = np.array(htp_df[88][247-skipr:247-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_p
# interpolate missing values
ok = ~np.isnan(htp_tp)
xp = ok.ravel().nonzero()[0]
fp = htp_tp[~np.isnan(htp_tp)]
x  = np.isnan(htp_tp).ravel().nonzero()[0]
htp_tp[np.isnan(htp_tp)] = np.interp(x, xp, fp)

###################
# jwpcp
###################
jwp_df = pd.read_excel('NPDESMonitoringData_CA0053813_JWPCP.xlsx',header=None,skiprows=skipr)
#flow
jwp_fl = np.array(jwp_df[39][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgd_to_m3s
#nh4
jwp_nh = np.array(jwp_df[43][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
# temp
jwp_tm = (np.array(jwp_df[81][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)-32)/1.8
# take mean of max/min for pH
jwp_ph = np.nanmean((np.array(jwp_df[89][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float),np.array(jwp_df[90][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)),axis=0)
#total organic carbon
jwp_tc = np.array(jwp_df[12][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_c
# data only collected every 3 months
# total organic nitrogen
jwp_tn = np.empty((jwp_fl.shape[0]))
jwp_tn.fill(np.nan)
jwp_tn[2::3] = np.array(jwp_df[72][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(jwp_tn)
xp = ok.ravel().nonzero()[0]
fp = jwp_tn[~np.isnan(jwp_tn)]
x  = np.isnan(jwp_tn).ravel().nonzero()[0]
jwp_tn[np.isnan(jwp_tn)] = np.interp(x, xp, fp)
# total phosphorus
jwp_tp = np.empty((jwp_fl.shape[0]))
jwp_tp.fill(np.nan)
jwp_tp[2::3] = np.array(jwp_df[75][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_p
ok = ~np.isnan(jwp_tp)
xp = ok.ravel().nonzero()[0]
fp = jwp_tp[~np.isnan(jwp_tp)]
x  = np.isnan(jwp_tp).ravel().nonzero()[0]
jwp_tp[np.isnan(jwp_tp)] = np.interp(x, xp, fp)
# nitrate
jwp_na = np.empty((jwp_fl.shape[0]))
jwp_na.fill(np.nan)
jwp_na[2::3] = np.array(jwp_df[70][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(jwp_na)
xp = ok.ravel().nonzero()[0]
fp = jwp_na[~np.isnan(jwp_na)]
x  = np.isnan(jwp_na).ravel().nonzero()[0]
jwp_na[np.isnan(jwp_na)] = np.interp(x, xp, fp)
# nitrite
jwp_ni = np.empty((jwp_fl.shape[0]))
jwp_ni.fill(np.nan)
jwp_ni[2::3] = np.array(jwp_df[71][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(jwp_ni)
xp = ok.ravel().nonzero()[0]
fp = jwp_ni[~np.isnan(jwp_ni)]
x  = np.isnan(jwp_ni).ravel().nonzero()[0]
jwp_ni[np.isnan(jwp_ni)] = np.interp(x, xp, fp)

############
# ocsd
############
ocs_df = pd.read_excel('NPDESMonitoringData_CA0110604_OCSD.xlsx',header=None,skiprows=skipr)
#flow
ocs_fl = np.array(ocs_df[49][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgd_to_m3s
# ammonium
ocs_nh = np.array(ocs_df[67][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
# take mean of max/min for pH
ocs_ph = np.nanmean((np.array(ocs_df[102][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float),np.array(ocs_df[103][3:ind_end+3].replace(to_replace=['NODI: B','NODI: C'],value=np.nan)).astype(float)),axis=0)
# data only collected every 3 months
# nitrate
ocs_na = np.empty((ocs_fl.shape[0]))
ocs_na.fill(np.nan)
ocs_na[2::3] = np.array(ocs_df[21][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(ocs_na)
xp = ok.ravel().nonzero()[0]
fp = ocs_na[~np.isnan(ocs_na)]
x  = np.isnan(ocs_na).ravel().nonzero()[0]
ocs_na[np.isnan(ocs_na)] = np.interp(x, xp, fp)
# nitrite
ocs_ni = np.empty((ocs_fl.shape[0]))
ocs_ni.fill(np.nan)
ocs_ni[2::3] = np.array(ocs_df[22][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(ocs_ni)
xp = ok.ravel().nonzero()[0]
fp = ocs_ni[~np.isnan(ocs_ni)]
x  = np.isnan(ocs_ni).ravel().nonzero()[0]
ocs_ni[np.isnan(ocs_ni)] = np.interp(x, xp, fp)
# total organic nitrogen
ocs_tn = np.empty((ocs_fl.shape[0]))
ocs_tn.fill(np.nan)
ocs_tn[2::3] = np.array(ocs_df[23][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: X','NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_to_mmolm3
ok = ~np.isnan(ocs_tn)
xp = ok.ravel().nonzero()[0]
fp = ocs_tn[~np.isnan(ocs_tn)]
x  = np.isnan(ocs_tn).ravel().nonzero()[0]
ocs_tn[np.isnan(ocs_tn)] = np.interp(x, xp, fp)
# total phosphorus
ocs_tp = np.empty((ocs_fl.shape[0]))
ocs_tp.fill(np.nan)
ocs_tp[2::3] = np.array(ocs_df[27][75-skipr:75-skipr+int(ind_end/3)].replace(to_replace=['NODI: E','NODI: 9','NODI: B','NODI: C'],value=np.nan)).astype(float)*mgL_p
ok = ~np.isnan(ocs_tp)
xp = ok.ravel().nonzero()[0]
fp = ocs_tp[~np.isnan(ocs_tp)]
x  = np.isnan(ocs_tp).ravel().nonzero()[0]
ocs_tp[np.isnan(ocs_tp)] = np.interp(x, xp, fp)

############
# plwtp
############
plw_df = pd.read_excel('NPDESMonitoringData_CA0107409_PLWTP.xlsx',header=None,skiprows=skipr)
#flow
plw_fl_noninterp = plw_df[251][3:ind_end+3].replace(to_replace=['NODI: R','NODI: B','NODI: C'],value=np.nan).astype(float)*mgd_to_m3s
plw_fl = np.array(plw_fl_noninterp.interpolate().values.ravel().tolist())
# ammonium
plw_nh_noninterp = plw_df[340][3:ind_end+3].replace(to_replace=['NODI: R','NODI: B','NODI: C'],value=np.nan).astype(float)*(1./1000)*mgL_to_mmolm3 # ug/L
plw_nh = np.array(plw_nh_noninterp.interpolate().values.ravel().tolist())
# temperature
plw_tm_noninterp = plw_df[409][3:ind_end+3].replace(to_replace=['NODI: R','NODI: B','NODI: C'],value=np.nan).astype(float)
plw_tm = np.array(plw_tm_noninterp.interpolate().values.ravel().tolist())
# take mean of max/min for pH
plw_ph = np.nanmean((np.array(plw_df[447][3:ind_end+3].replace(to_replace=['NODI: R','NODI: B','NODI: C'],value=np.nan)).astype(float),np.array(plw_df[448][3:ind_end+3].replace(to_replace=['NODI: R','NODI: B','NODI: C'],value=np.nan)).astype(float)),axis=0)
ok = ~np.isnan(plw_ph)
xp = ok.ravel().nonzero()[0]
fp = plw_ph[~np.isnan(plw_ph)]
x  = np.isnan(plw_ph).ravel().nonzero()[0]
plw_ph[np.isnan(plw_ph)] = np.interp(x, xp, fp)


################
# make netcdf
################
#dimensions
tim_d = newf.createDimension('time',None)
lat_d = newf.createDimension('lat',4) # 19 minor potws
lon_d = newf.createDimension('lon',4)

#variables
tim_v = newf.createVariable('time',np.float32,('time'))
lat_v = newf.createVariable('latitude',np.float32,('lat'))
lon_v = newf.createVariable('longitude',np.float32,('lon'))
flow_v = newf.createVariable('flow',np.float64,('time','lat','lon'))
NO3_v = newf.createVariable('NO3',np.float64,('time','lat','lon'))
NH4_v = newf.createVariable('NH4',np.float64,('time','lat','lon'))
NO2_v = newf.createVariable('NO2',np.float64,('time','lat','lon'))
tp_v = newf.createVariable('total_phosphorus',np.float64,('time','lat','lon'))
ton_v = newf.createVariable('TON',np.float64,('time','lat','lon'))
TOC_v = newf.createVariable('TOC',np.float64,('time','lat','lon'))
do_v = newf.createVariable('dissolved_oxygen',np.float64,('time','lat','lon'))
pH_v = newf.createVariable('pH',np.float64,('time','lat','lon'))
temperature_v = newf.createVariable('temperature',np.float64,('time','lat','lon'))
salinity_v = newf.createVariable('salinity',np.float64,('time','lat','lon'))

ton_v.longname = 'total organic nitrogen'
TOC_v.longname = 'total organic carbon'

tim_v.units = 'days since 2013-01-01'
lat_v.units = oldf.variables['latitude'].units
lon_v.units = oldf.variables['longitude'].units
flow_v.units = oldf.variables['flow'].units
NO3_v.units = oldf.variables['NO3'].units
NH4_v.units = oldf.variables['NH4'].units
NO2_v.units = oldf.variables['NO2'].units
tp_v.units = oldf.variables['PO4'].units
TOC_v.units = oldf.variables['TOC'].units
ton_v.units = oldf.variables['TOC'].units
do_v.units = oldf.variables['dissolved_oxygen'].units
temperature_v.units = oldf.variables['temperature'].units
salinity_v.units = oldf.variables['salinity'].units

# assign values
tim_v[:] = numdat
lat_v[:] = np.array(oldf.variables['latitude'])
lon_v[:] = np.array(oldf.variables['longitude'])

empty_arr = np.empty((jwp_na.shape[0]))
empty_arr.fill(np.nan)

flow_v[:,0,0] = htp_fl
flow_v[:,1,1] = jwp_fl
flow_v[:,2,2] = ocs_fl
flow_v[:,3,3] = plw_fl

NO3_v[:,0,0] = empty_arr
NO3_v[:,1,1] = jwp_na
NO3_v[:,2,2] = ocs_na
NO3_v[:,3,3] = empty_arr

NH4_v[:,0,0] = htp_nh
NH4_v[:,1,1] = jwp_nh
NH4_v[:,2,2] = ocs_nh
NH4_v[:,3,3] = plw_nh

NO2_v[:,0,0] = empty_arr
NO2_v[:,1,1] = jwp_ni
NO2_v[:,2,2] = ocs_ni
NO2_v[:,3,3] = empty_arr

tp_v[:,0,0] = htp_tp
tp_v[:,1,1] = jwp_tp
tp_v[:,2,2] = ocs_tp
tp_v[:,3,3] = empty_arr

ton_v[:,0,0] = htp_tn
ton_v[:,1,1] = jwp_tn
ton_v[:,2,2] = ocs_tn
ton_v[:,3,3] = empty_arr

TOC_v[:,0,0] = htp_tc
TOC_v[:,1,1] = jwp_tc
TOC_v[:,2,2] = empty_arr
TOC_v[:,3,3] = empty_arr

do_v[:,0,0] = htp_do
do_v[:,1,1] = empty_arr
do_v[:,2,2] = empty_arr
do_v[:,3,3] = empty_arr

pH_v[:,0,0] = htp_ph
pH_v[:,1,1] = jwp_ph
pH_v[:,2,2] = ocs_ph
pH_v[:,3,3] = plw_ph

temperature_v[:,0,0] = htp_tm
temperature_v[:,1,1] = jwp_tm
temperature_v[:,2,2] = np.array(oldf.variables['temperature'][:60,2,2])
temperature_v[:,3,3] = plw_tm

salinity_v[:,0,0] = np.array(oldf.variables['salinity'][:60,0,0])
salinity_v[:,1,1] = np.array(oldf.variables['salinity'][:60,1,1])
salinity_v[:,2,2] = np.array(oldf.variables['salinity'][:60,2,2])
salinity_v[:,3,3] = np.array(oldf.variables['salinity'][:60,3,3])

newf.close()
