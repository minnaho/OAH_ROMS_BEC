# separate wet/dry weather flows 
# for wet/dry concentration
# average wet season flows (Nov-Apr)
import pandas as pd
import numpy as np
from netCDF4 import Dataset,date2num
import glob as glob

# wet/dry months
wet_m = [11,12,1,2,3,4]
dry_m = [5,6,7,8,9,10]

# flow data
riv_path = '/data/project1/minnaho/river_data/updated_2013_2017/formatted/'
riv_fi = sorted(glob.glob(riv_path+'*'))

# conc data
con_path = '/data/project1/minnaho/river_data/updated_2013_2017/river_sources.xlsx'
con_fi = pd.read_excel(con_path,skiprows=2,header=None)


# river names
rnames = []
for f_i in riv_fi:
    rnames.append(f_i[62:f_i.index('_2007')])

# put the in alphabetical order
rnames = sorted(rnames)

# example
df = pd.read_csv(riv_fi[0])
df['date'] = pd.to_datetime(df['date'])
df.set_index(df['date'],inplace=True)


sm = pd.read_csv(riv_fi[rnames.index('santa_margarita')])
sm['date'] = pd.to_datetime(sm['date'])
sm.set_index(sm['date'],inplace=True)
sm_temp = sm['temperature C']
sm_temp_mean = sm['temperature C'].resample('M').mean()

endind = 4018 # ends at 2017-12-31
# usgs flow data
flow = df['combined flow m3/s'][:endind]


time_unit = 'days since 2007-01-01'
dat_arr = date2num(df.index.to_pydatetime(),time_unit)

lat_arr = np.empty((len(rnames)))
lon_arr = np.empty((len(rnames)))

flo_arr = np.empty((flow.shape[0],len(rnames)))
toc_arr = np.empty((flow.shape[0],len(rnames)))
nh4_arr = np.empty((flow.shape[0],len(rnames)))
no3_arr = np.empty((flow.shape[0],len(rnames)))
po4_arr = np.empty((flow.shape[0],len(rnames)))
tnn_arr = np.empty((flow.shape[0],len(rnames)))
tpp_arr = np.empty((flow.shape[0],len(rnames)))
onn_arr = np.empty((flow.shape[0],len(rnames)))
val_on = 1.68
onn_arr.fill(val_on)
opp_arr = np.empty((flow.shape[0],len(rnames)))
val_op = 0.3
opp_arr.fill(val_op)
dfe_arr = np.empty((flow.shape[0],len(rnames)))
val_df = .021508 # value based of 20% of average
val_tf = .10787 # value based of 20% of average
tfe_arr = np.empty((flow.shape[0],len(rnames)))
alk_arr = np.empty((flow.shape[0],len(rnames)))
sal_arr = np.empty((flow.shape[0],len(rnames)))
val_sa = 0.52
sal_arr.fill(val_sa)
tem_arr = np.empty((flow.shape[0],len(rnames)))
# set all temps to santa margarita temperature, except
# tijuana, bell c, arroyo honda, refugio that is changed in the loop
for r_i in range(tem_arr.shape[1]):
    tem_arr[:,r_i] = sm_temp[:endind]

# only tijuana and santa margarita have dissolved o
doo_arr = np.empty((flow.shape[0],len(rnames)))
val_do = 7
doo_arr.fill(val_do)
# only tijuana and santa margarita have pH
phh_arr = np.empty((flow.shape[0],len(rnames)))
val_ph = 7.5
phh_arr.fill(val_ph)
# only santa margarita has TIC
tic_arr = np.empty((flow.shape[0],len(rnames)))
tic_arr.fill(np.nan)
# add silicate, but only for available rivers
sil_arr = np.empty((flow.shape[0],len(rnames)))
val_si = 19.17
sil_arr.fill(val_si)

# use wet concentrations for 3 days after flow/wet_med > 2
for r_i in range(len(riv_fi)):
    print('r_i:',r_i)
    print(rnames[r_i])
    df = pd.read_csv(riv_fi[r_i])
    try:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index(df['date'],inplace=True)
    except:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index(df['Date'],inplace=True)
    lat_arr[r_i] = df['lat'][0]
    lon_arr[r_i] = df['lon'][0]
    print('lat:',lat_arr[r_i])
    flow = df['combined flow m3/s'][:endind]
    flo_arr[:,r_i] = flow
    wet_flows_l = []
    for f_i in range(flow.shape[0]):
        if flow.index[f_i].month in wet_m:
            wet_flows_l.append(flow[f_i])
    
    dry_flows_l = []
    for f_i in range(flow.shape[0]):
        if flow.index[f_i].month in dry_m:
            dry_flows_l.append(flow[f_i])
    
    wet_flows = np.array(wet_flows_l)
    wet_med = np.nanmedian(wet_flows)
    if wet_med == 0:
        wet_med = np.nanmean(wet_flows)
    print('wet median: ',wet_med)
    
    dry_flows = np.array(dry_flows_l)
    dry_med = np.nanmedian(dry_flows)
    if dry_med == 0:
        dry_med = np.nanmean(dry_flows)
    print('dry median: ',dry_med)
    # use river conc spreadsheet
    if rnames[r_i] in list(con_fi[0]):
        # river rows
        rind = np.where(con_fi[0]==rnames[r_i])[0]
        # wet conc
        wettoc = con_fi[2][rind[0]]
        wetnh4 = con_fi[3][rind[0]]
        wetno3 = con_fi[4][rind[0]]
        wetpo4 = con_fi[5][rind[0]]
        wettnn = con_fi[6][rind[0]]
        wettpp = con_fi[7][rind[0]]
        wetonn = con_fi[8][rind[0]]
        wetopp = con_fi[9][rind[0]]
        wetdfe = con_fi[10][rind[0]]
        wettfe = con_fi[11][rind[0]]
        wetalk = con_fi[12][rind[0]]
        wetsil = con_fi[14][rind[0]]
        # winter dry conc
        wintoc = con_fi[2][rind[1]]
        winnh4 = con_fi[3][rind[1]]
        winno3 = con_fi[4][rind[1]]
        winpo4 = con_fi[5][rind[1]]
        wintnn = con_fi[6][rind[1]]
        wintpp = con_fi[7][rind[1]]
        winonn = con_fi[8][rind[1]]
        winopp = con_fi[9][rind[1]]
        windfe = con_fi[10][rind[1]]
        wintfe = con_fi[11][rind[1]]
        winalk = con_fi[12][rind[1]]
        winsil = con_fi[14][rind[1]]
        # summer dry conc
        sumtoc = con_fi[2][rind[2]]
        sumnh4 = con_fi[3][rind[2]]
        sumno3 = con_fi[4][rind[2]]
        sumpo4 = con_fi[5][rind[2]]
        sumtnn = con_fi[6][rind[2]]
        sumtpp = con_fi[7][rind[2]]
        sumonn = con_fi[8][rind[2]]
        sumopp = con_fi[9][rind[2]]
        sumdfe = con_fi[10][rind[2]]
        sumtfe = con_fi[11][rind[2]]
        sumalk = con_fi[12][rind[2]]
        sumsil = con_fi[14][rind[2]]

    if rnames[r_i] not in list(con_fi[0]):
        # wet conc
        wettoc = np.nan
        wetnh4 = df['Wet Ammonia (mg/L)'][0]
        wetno3 = df['Wet Nitrate (mg/L)'][0]
        try:
            wetpo4 = df['Wet Phosphate (mg/L)'][0]
        except:
            wetpo4 = df['Wet Phosphate  (mg/L)'][0]
        wettnn = df['Wet TN (mg/L)'][0]
        wettpp = df['Wet TP (mg/L)'][0]
        wetonn = val_on
        wetopp = val_op
        wetdfe = val_df
        wettfe = val_tf 
        wetalk = df['alkalinity mg/L'][0]
        wetsil = val_si 
        winsil = val_si 
        sumsil = val_si 
        # winter dry conc
        if np.isnan(df['Dry Ammonia (mg/L)'][0]):
            wintoc = wettoc
            winnh4 = wetnh4
            winno3 = wetno3
            winpo4 = wetpo4
            wintnn = wettnn
            wintpp = wettpp
            winonn = wetonn
            winopp = wetopp
            windfe = wetdfe
            wintfe = wettfe
            winalk = wetalk
        else:
            wintoc = np.nan
            winnh4 = df['Dry Ammonia (mg/L)'][0]
            try:
                winno3 = df['Dry Nitrate\n (mg/L)'][0]
            except:
                winno3 = df['Dry Nitrate\n(mg/L)'][0]
            winpo4 = df['Dry Phosphate \n(mg/L)'][0]
            wintnn = df['Dry TN (mg/L)'][0]
            wintpp = df['Dry TP (mg/L)'][0]
            winonn = val_on 
            winopp = val_op 
            windfe = val_df 
            wintfe = val_tf 
            winalk = df['alkalinity mg/L'][0]
        # summer dry conc
        if np.isnan(df['Dry Ammonia (mg/L)'][0]):
            sumtoc = wettoc
            sumnh4 = wetnh4
            sumno3 = wetno3
            sumpo4 = wetpo4
            sumtnn = wettnn
            sumtpp = wettpp
            sumonn = wetonn
            sumopp = wetopp
            sumdfe = wetdfe
            sumtfe = wettfe
            sumalk = wetalk
        else:
            sumtoc = np.nan
            sumnh4 = df['Dry Ammonia (mg/L)'][0]
            try:
                sumno3 = df['Dry Nitrate\n (mg/L)'][0]
            except:
                sumno3 = df['Dry Nitrate\n(mg/L)'][0]
            sumpo4 = df['Dry Phosphate \n(mg/L)'][0]
            sumtnn = df['Dry TN (mg/L)'][0]
            sumtpp = df['Dry TP (mg/L)'][0]
            sumonn = val_on 
            sumopp = val_op 
            sumdfe = val_df 
            sumtfe = val_tf 
            sumalk = df['alkalinity mg/L'][0]

    for d_i in range(flow.shape[0]):
        if flow[d_i]/wet_med >= 2:
            # use wet flow conc
            toc_arr[d_i,r_i] = wettoc 
            nh4_arr[d_i,r_i] = wetnh4 
            no3_arr[d_i,r_i] = wetno3 
            po4_arr[d_i,r_i] = wetpo4 
            tnn_arr[d_i,r_i] = wettnn 
            tpp_arr[d_i,r_i] = wettpp 
            onn_arr[d_i,r_i] = wetonn 
            opp_arr[d_i,r_i] = wetopp 
            dfe_arr[d_i,r_i] = wetdfe 
            tfe_arr[d_i,r_i] = wettfe 
            alk_arr[d_i,r_i] = wetalk 
            sil_arr[d_i,r_i] = wetsil
                             
        elif (
            (flow[d_i-1]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
            (flow[d_i-2]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
            (flow[d_i-3]/wet_med >= 2 and flow[d_i]/wet_med < 2)
           ):
            # use wet flow conc
            toc_arr[d_i,r_i] = wettoc 
            nh4_arr[d_i,r_i] = wetnh4 
            no3_arr[d_i,r_i] = wetno3 
            po4_arr[d_i,r_i] = wetpo4 
            tnn_arr[d_i,r_i] = wettnn 
            tpp_arr[d_i,r_i] = wettpp 
            onn_arr[d_i,r_i] = wetonn 
            opp_arr[d_i,r_i] = wetopp 
            dfe_arr[d_i,r_i] = wetdfe 
            tfe_arr[d_i,r_i] = wettfe 
            alk_arr[d_i,r_i] = wetalk 
            sil_arr[d_i,r_i] = wetsil

        elif flow[d_i]/wet_med < 2 and df.index[d_i].month in dry_m:
            # use summer dry flow conc
            toc_arr[d_i,r_i] = sumtoc 
            nh4_arr[d_i,r_i] = sumnh4 
            no3_arr[d_i,r_i] = sumno3 
            po4_arr[d_i,r_i] = sumpo4 
            tnn_arr[d_i,r_i] = sumtnn 
            tpp_arr[d_i,r_i] = sumtpp 
            onn_arr[d_i,r_i] = sumonn 
            opp_arr[d_i,r_i] = sumopp 
            dfe_arr[d_i,r_i] = sumdfe 
            tfe_arr[d_i,r_i] = sumtfe 
            alk_arr[d_i,r_i] = sumalk 
            sil_arr[d_i,r_i] = sumsil

        elif flow[d_i]/wet_med < 2 and df.index[d_i].month in wet_m:
            # use winter dry flow conc
            toc_arr[d_i,r_i] = wintoc 
            nh4_arr[d_i,r_i] = winnh4 
            no3_arr[d_i,r_i] = winno3 
            po4_arr[d_i,r_i] = winpo4 
            tnn_arr[d_i,r_i] = wintnn 
            tpp_arr[d_i,r_i] = wintpp 
            onn_arr[d_i,r_i] = winonn 
            opp_arr[d_i,r_i] = winopp 
            dfe_arr[d_i,r_i] = windfe 
            tfe_arr[d_i,r_i] = wintfe 
            alk_arr[d_i,r_i] = winalk 
            sil_arr[d_i,r_i] = winsil


    if rnames[r_i] == 'tijuana_river':
        for d_i in range(flow.shape[0]):
            toc_arr[d_i,r_i] = df['TOC mg/L'][d_i]
            nh4_arr[d_i,r_i] = df['ammonia mg/L'][d_i]
            no3_arr[d_i,r_i] = df['nitrate mg/L'][d_i]
            po4_arr[d_i,r_i] = df['phosphate mg/L'][d_i]
            tnn_arr[d_i,r_i] = df['TN mg/L'][d_i]
            tpp_arr[d_i,r_i] = df['TP mg/L'][d_i]
            onn_arr[d_i,r_i] = df['TN mg/L'][d_i] - (df['ammonia mg/L'][d_i]+df['nitrate mg/L'][d_i]+df['nitrite mg/L'][d_i])
            opp_arr[d_i,r_i] = df['TP mg/L'][d_i] - df['phosphate mg/L'][d_i]
            # convert to ug/L because all other iron units are ug/L
            dfe_arr[d_i,r_i] = df['iron mg/L'][d_i]*.2*1000
            tfe_arr[d_i,r_i] = df['iron mg/L'][d_i]*1000
            alk_arr[d_i,r_i] = df['alkalinity mg/L'][d_i]
            sal_arr[d_i,r_i] = df['salinity PSU'][d_i]
            tem_arr[d_i,r_i] = df['temperature C'][d_i]
            doo_arr[d_i,r_i] = df['dissolved oxygen mg/L'][d_i]
            phh_arr[d_i,r_i] = df['pH'][d_i]
            sil_arr[d_i,r_i] = con_fi[14][np.where(con_fi[0]=='tijuana_river')[0][0]]

    if rnames[r_i] == 'santa_margarita':
        for d_i in range(flow.shape[0]):
            toc_arr[d_i,r_i] = np.nan 
            nh4_arr[d_i,r_i] = df['Ammonia (mg/L)'][d_i]
            no3_arr[d_i,r_i] = df['Nitrate (mg/L)'][d_i]
            po4_arr[d_i,r_i] = df['Phosphate (mg/L)'][d_i]
            tnn_arr[d_i,r_i] = df['TN (mg/L)'][d_i]
            tpp_arr[d_i,r_i] = df['TP (mg/L)'][d_i]
            onn_arr[d_i,r_i] = df['TN (mg/L)'][d_i] - (df['Ammonia (mg/L)'][d_i]+df['Nitrate (mg/L)'][d_i])
            opp_arr[d_i,r_i] = df['TP (mg/L)'][d_i] - df['Phosphate (mg/L)'][d_i]
            dfe_arr[d_i,r_i] = np.nan 
            tfe_arr[d_i,r_i] = np.nan 
            alk_arr[d_i,r_i] = df['alkalinity mg/L'][d_i]
            sal_arr[d_i,r_i] = val_sa
            tem_arr[d_i,r_i] = df['temperature C'][d_i]
            doo_arr[d_i,r_i] = df['dissolved oxygen mg/L'][d_i]
            phh_arr[d_i,r_i] = df['pH'][d_i]
            tic_arr[d_i,r_i] = df['TIC mg/L total inorganic C'][d_i]
    if (
        rnames[r_i] == 'bell_canyon' or
        rnames[r_i] == 'arroyo_honda_creek' or
        rnames[r_i] == 'refugio_creek'):
        df['temperature C'] = df['temperature C'].interpolate()
        df['temperature C'] = df['temperature C'].bfill()
        for d_i in range(flow.shape[0]):
            tem_arr[d_i,r_i] = df['temperature C'][d_i]
        
        
        

# mg/L to mmol/m3 
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855 # silicon
mg_l_a = 1000/100.09 # mg/L CaCO3 to mmol/m3 CaCO3

flo_arr[np.isnan(flo_arr)]=0
toc_arr = toc_arr*mg_l_c
nh4_arr = nh4_arr*mg_l_n
no3_arr = no3_arr*mg_l_n
po4_arr = po4_arr*mg_l_p
tnn_arr = tnn_arr*mg_l_n
tpp_arr = tpp_arr*mg_l_p
onn_arr = onn_arr*mg_l_n
opp_arr = opp_arr*mg_l_p
dfe_arr = dfe_arr*(mg_l_f/1000.) # ug/L to mmol/m3
tfe_arr = tfe_arr*(mg_l_f/1000.) # ug/L to mmol/m3
alk_arr = alk_arr*mg_l_a
doo_arr = doo_arr*mg_l_o
tic_arr = tic_arr*mg_l_c
sil_arr = sil_arr*mg_l_s

toc_arr[toc_arr<0] = 0
nh4_arr[nh4_arr<0] = 0
no3_arr[no3_arr<0] = 0
po4_arr[po4_arr<0] = 0
tnn_arr[tnn_arr<0] = 0
tpp_arr[tpp_arr<0] = 0
onn_arr[onn_arr<0] = 0
opp_arr[opp_arr<0] = 0
dfe_arr[dfe_arr<0] = 0
tfe_arr[tfe_arr<0] = 0
alk_arr[alk_arr<0] = 0
doo_arr[doo_arr<0] = 0
tic_arr[tic_arr<0] = 0
sil_arr[sil_arr<0] = 0

# time array
timeunit = 'days since 2007-01-01'
timenum = date2num(df.index.to_pydatetime()[:flo_arr.shape[0]],timeunit)

# make netcdf
ncf = Dataset('rivers_2007_2017.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 75 rivers

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
tic_v = ncf.createVariable('total_inorganic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'C'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
tic_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'PSU'
dfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_arr
lon_v[:] = lon_arr
flo_v[:,:] = flo_arr
nh4_v[:,:] = nh4_arr
no3_v[:,:] = no3_arr
doo_v[:,:] = doo_arr
tem_v[:,:] = tem_arr
phh_v[:,:] = phh_arr
tpp_v[:,:] = tpp_arr
tnn_v[:,:] = tnn_arr
po4_v[:,:] = po4_arr
opp_v[:,:] = opp_arr
toc_v[:,:] = toc_arr
tic_v[:,:] = tic_arr
onn_v[:,:] = onn_arr
tfe_v[:,:] = tfe_arr
alk_v[:,:] = alk_arr
sal_v[:,:] = sal_arr
dfe_v[:,:] = dfe_arr
sil_v[:,:] = sil_arr

ncf.close()


writer = pd.ExcelWriter('rivers_2007_2017.xlsx')

# print to excel file
for r_i in range(flo_arr.shape[1]):
    lat_tem = np.empty((flo_arr.shape[0]))
    lat_tem.fill(lat_arr[r_i])
    lon_tem = np.empty((flo_arr.shape[0]))
    lon_tem.fill(lon_arr[r_i])
    save_df = pd.DataFrame({'date':df.index.date[:endind],
    'flow m3/s':flo_arr[:,r_i],
    'NH4 mmol/m3':nh4_arr[:,r_i],
    'NO3 mmol/m3':no3_arr[:,r_i],
    'DO mmol/m3':doo_arr[:,r_i],
    'temperature C':tem_arr[:,r_i],
    'pH':phh_arr[:,r_i],
    'TN mmol/m3':tnn_arr[:,r_i],
    'TP mmol/m3':tpp_arr[:,r_i],
    'PO4 mmol/m3':po4_arr[:,r_i],
    'OP mmol/m3':opp_arr[:,r_i],
    'TOC mmol/m3':toc_arr[:,r_i],
    'ON mmol/m3':onn_arr[:,r_i],
    'total Fe mmol/m3':tfe_arr[:,r_i],
    'Alk mmol/m3':alk_arr[:,r_i],
    'salinity PSU':sal_arr[:,r_i],
    'dissolved Fe mmol/m3':dfe_arr[:,r_i],
    'TIC mmol/m3':tic_arr[:,r_i],
    'SiO4 mmol/m3':sil_arr[:,r_i],
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df.to_excel(writer,sheet_name=rnames[r_i][:31])

writer.save()

# make monthly arrays
# date index/size, monthly
dat_mon = pd.date_range(start='2007-01-01',end='2017-12-31',freq='M')

# combined datasets
flo_mon = np.empty((dat_mon.shape[0],len(rnames)))
toc_mon = np.empty((dat_mon.shape[0],len(rnames)))
nh4_mon = np.empty((dat_mon.shape[0],len(rnames)))
no3_mon = np.empty((dat_mon.shape[0],len(rnames)))
po4_mon = np.empty((dat_mon.shape[0],len(rnames)))
tnn_mon = np.empty((dat_mon.shape[0],len(rnames)))
tpp_mon = np.empty((dat_mon.shape[0],len(rnames)))
onn_mon = np.empty((dat_mon.shape[0],len(rnames)))
opp_mon = np.empty((dat_mon.shape[0],len(rnames)))
dfe_mon = np.empty((dat_mon.shape[0],len(rnames)))
tfe_mon = np.empty((dat_mon.shape[0],len(rnames)))
alk_mon = np.empty((dat_mon.shape[0],len(rnames)))
sal_mon = np.empty((dat_mon.shape[0],len(rnames)))
sal_mon = np.empty((dat_mon.shape[0],len(rnames)))
tem_mon = np.empty((dat_mon.shape[0],len(rnames)))
doo_mon = np.empty((dat_mon.shape[0],len(rnames)))
doo_mon.fill(np.nan)
phh_mon = np.empty((dat_mon.shape[0],len(rnames)))
phh_mon.fill(np.nan)
tic_mon = np.empty((dat_mon.shape[0],len(rnames)))
tic_mon.fill(np.nan)
sil_mon = np.empty((dat_mon.shape[0],len(rnames)))
sil_mon.fill(np.nan)

for r_i in range(flo_arr.shape[1]):
    lat_tem = np.empty((flo_arr.shape[0]))
    lat_tem.fill(lat_arr[r_i])
    lon_tem = np.empty((flo_arr.shape[0]))
    lon_tem.fill(lon_arr[r_i])
    day_df = pd.DataFrame({'date':df.index.date[:endind],
       'flow m3/s':flo_arr[:,r_i],
       'NH4 mmol/m3':nh4_arr[:,r_i],
       'NO3 mmol/m3':no3_arr[:,r_i],
       'DO mmol/m3':doo_arr[:,r_i],
       'temperature C':tem_arr[:,r_i],
       'pH':phh_arr[:,r_i],
       'TN mmol/m3':tnn_arr[:,r_i],
       'TP mmol/m3':tpp_arr[:,r_i],
       'PO4 mmol/m3':po4_arr[:,r_i],
       'OP mmol/m3':opp_arr[:,r_i],
       'TOC mmol/m3':toc_arr[:,r_i],
       'ON mmol/m3':onn_arr[:,r_i],
       'total Fe mmol/m3':tfe_arr[:,r_i],
       'Alk mmol/m3':alk_arr[:,r_i],
       'salinity PSU':sal_arr[:,r_i],
       'dissolved Fe mmol/m3':dfe_arr[:,r_i],
       'TIC mmol/m3':tic_arr[:,r_i],
       'SiO4 mmol/m3':sil_arr[:,r_i]},
       index=df.index[:endind],columns=None)
    mon_df = day_df.resample('M').mean()
    flo_mon[:,r_i] = mon_df['flow m3/s']
    nh4_mon[:,r_i] = mon_df['NH4 mmol/m3']
    no3_mon[:,r_i] = mon_df['NO3 mmol/m3']
    doo_mon[:,r_i] = mon_df['DO mmol/m3']
    tem_mon[:,r_i] = mon_df['temperature C']
    phh_mon[:,r_i] = mon_df['pH']
    tnn_mon[:,r_i] = mon_df['TN mmol/m3']
    tpp_mon[:,r_i] = mon_df['TP mmol/m3']
    po4_mon[:,r_i] = mon_df['PO4 mmol/m3']
    opp_mon[:,r_i] = mon_df['OP mmol/m3']
    toc_mon[:,r_i] = mon_df['TOC mmol/m3']
    onn_mon[:,r_i] = mon_df['ON mmol/m3']
    tfe_mon[:,r_i] = mon_df['total Fe mmol/m3']
    alk_mon[:,r_i] = mon_df['Alk mmol/m3']
    sal_mon[:,r_i] = mon_df['salinity PSU']
    dfe_mon[:,r_i] = mon_df['dissolved Fe mmol/m3']
    tic_mon[:,r_i] = mon_df['TIC mmol/m3']
    tic_mon[:,r_i] = mon_df['TIC mmol/m3']
    sil_mon[:,r_i] = mon_df['SiO4 mmol/m3']

# add 1997-2007 inputs, except for
# tijuana, and 3 additional rivers
import numpy as np
from netCDF4 import Dataset
import pickle

nm10 = pickle.load(open('../inputs_1997_2000/river_names_10.pkl','rb'))
nm24 = pickle.load(open('../inputs_1997_2000/river_names_24.pkl','rb'))

# rename
nm10 = ['san_juan_creek',
'san_jose_creek',
'montecito_creek',
'san_diego_river',
'sweetwater_river',
'solstice_canyon',
'los_angeles_river',
'atascadero_creek',
'salt_creek',
'little_sycamore',
'santa_ana_river',
'pena_canyon',
'moro_canyon',
'ballona_creek',
'tijuana_river',
'santa_margarita',
'los_angeles_harbor',
'tuna_canyon',
'rincon_creek',
'marle_canyon',
'santa_clara',
'santa_monica_canyon',
'aliso_creek',
'las_flores_canyon',
'mission_bay',
'otay_river',
'los_penasquitos_lagoon',
'encinas_creek',
'arroyo_sequit_creek',
'san_diego_creek',
'ventura_river',
'redondo_beach_king_harbor',
'mission_creek',
'walnut_canyon',
'trancas_canyon',
'carbon_canyon',
'calleguas_creek',
'san_gabriel_river',
'san_luis_rey_river',
'agua_hedionda_lagoon',
'buena_vista_creek',
'escondido_creek',
'las_flores_creek',
'san_dieguito_river',
'san_onofre_creek',
'san_marcos_creek',
'tecolote_creek',
'chollas_creek']

nm24 = [
'arroyo_trabuco_creek',
'bolsa_chica_westminster_channel',
'bonita_creek',
'carpinteria_creek',
'costa_mesa_channel',
'coyote_creek',
'cristianitos_creek',
'devereux_lagoon',
'dominguez_channel',
'e_garden_grove_wintersburg_channel',
'goleta_tecolotito_creek',
'laguna_canyon',
'malibu_creek',
'prima_deshecha',
'revolon_slough',
'san_mateo_creek',
'san_pedro_creek',
'santa_ana_delhi',
'segunda_deshecha',
'topanga_creek',
'zuma_canyon_lagoon',
'arroyo_burro_creek',
'canada_de_la_gaviota',
'franklin_creek']

# load old netcdf
nc10 = Dataset('../inputs_1997_2000/south_coast_rivers_10_years_monthly_new.nc','r')
nc24 = Dataset('../inputs_1997_2000/south_coast_rivers_24_years_monthly_new.nc','r')

lat10 = np.array(nc10.variables['latitude'])

flo10 = np.array(nc10.variables['flow'])
nh410 = np.array(nc10.variables['ammonium'])
no310 = np.array(nc10.variables['nitrate'])
po410 = np.array(nc10.variables['phosphate'])
tnn10 = np.array(nc10.variables['total_nitrogen'])
tpp10 = np.array(nc10.variables['total_phosphorus'])
alk10 = np.array(nc10.variables['alkalinity'])
tem10 = np.array(nc10.variables['temperature'])

flo24 = np.array(nc24.variables['flow'])
nh424 = np.array(nc24.variables['ammonium'])
no324 = np.array(nc24.variables['nitrate'])
po424 = np.array(nc24.variables['phosphate'])
tnn24 = np.array(nc24.variables['total_nitrogen'])
tpp24 = np.array(nc24.variables['total_phosphorus'])
alk24 = np.array(nc24.variables['alkalinity'])
tem24 = np.array(nc24.variables['temperature'])

# date index/size, monthly
dat_com = pd.date_range(start='1997-01-01',end='2017-12-31',freq='M')

# combined datasets
flo_com = np.empty((dat_com.shape[0],len(rnames)))
toc_com = np.empty((dat_com.shape[0],len(rnames)))
val_to = np.nanmean(toc_arr*.2)
toc_com.fill(val_to)
nh4_com = np.empty((dat_com.shape[0],len(rnames)))
val_nh = np.nanmean(nh4_arr*.2)
nh4_com.fill(val_nh)
no3_com = np.empty((dat_com.shape[0],len(rnames)))
val_no = np.nanmean(no3_arr*.2)
no3_com.fill(val_no)
po4_com = np.empty((dat_com.shape[0],len(rnames)))
val_po = np.nanmean(po4_arr*.2)
po4_com.fill(val_po)
tnn_com = np.empty((dat_com.shape[0],len(rnames)))
tpp_com = np.empty((dat_com.shape[0],len(rnames)))
onn_com = np.empty((dat_com.shape[0],len(rnames)))
onn_com.fill(val_on*mg_l_n)
opp_com = np.empty((dat_com.shape[0],len(rnames)))
opp_com.fill(val_op*mg_l_p)
dfe_com = np.empty((dat_com.shape[0],len(rnames)))
val_df = np.nanmean(dfe_arr*.2)
dfe_com.fill(val_df)
tfe_com = np.empty((dat_com.shape[0],len(rnames)))
val_tf = np.nanmean(tfe_arr*.2)
tfe_com.fill(val_tf)
alk_com = np.empty((dat_com.shape[0],len(rnames)))
val_al = np.nanmean(alk_arr*.2)
alk_com.fill(val_al)
sal_com = np.empty((dat_com.shape[0],len(rnames)))
sal_com.fill(val_sa)
tem_com = np.empty((dat_com.shape[0],len(rnames)))
tem_com[flo10.shape[0]:,r_i] = sm_temp_mean['2007':'2017']
tem_com[:flo10.shape[0],r_i] = np.array(list(sm_temp_mean['2007-01':'2007-12'])*10)
doo_com = np.empty((dat_com.shape[0],len(rnames)))
doo_com.fill(val_do*mg_l_o)
phh_com = np.empty((dat_com.shape[0],len(rnames)))
phh_com.fill(val_ph)
tic_com = np.empty((dat_com.shape[0],len(rnames)))
val_ti = np.nanmean(tic_com*.2*(12/1000))
tic_com.fill(val_ti*mg_l_c)
sil_com = np.empty((dat_com.shape[0],len(rnames)))
sil_com.fill(val_si*mg_l_s)

for r_i in range(len(nm10)):
    rind = rnames.index(nm10[r_i])
    flo_com[:flo10.shape[0],rind] = flo10[:,r_i,r_i]
    flo_com[flo10.shape[0]:,rind] = flo_mon[:,rind]
    nh4_com[:nh410.shape[0],rind] = nh410[:,r_i,r_i]
    nh4_com[nh410.shape[0]:,rind] = nh4_mon[:,rind]
    no3_com[:no310.shape[0],rind] = no310[:,r_i,r_i]
    no3_com[no310.shape[0]:,rind] = no3_mon[:,rind]
    po4_com[:po410.shape[0],rind] = po410[:,r_i,r_i]
    po4_com[po410.shape[0]:,rind] = po4_mon[:,rind]
    tnn_com[:tnn10.shape[0],rind] = tnn10[:,r_i,r_i]
    tnn_com[tnn10.shape[0]:,rind] = tnn_mon[:,rind]
    tpp_com[:tpp10.shape[0],rind] = tpp10[:,r_i,r_i]
    tpp_com[tpp10.shape[0]:,rind] = tpp_mon[:,rind]
    alk_com[:alk10.shape[0],rind] = alk10[:,r_i,r_i]
    alk_com[alk10.shape[0]:,rind] = alk_mon[:,rind]
    tem_com[:tem10.shape[0],rind] = tem10[:,r_i,r_i]
    tem_com[tem10.shape[0]:,rind] = tem_mon[:,rind]
    doo_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*doo_mon[0,rind]
    doo_com[flo10.shape[0]:,rind] = doo_mon[:,rind]
    phh_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*phh_mon[0,rind]
    phh_com[flo10.shape[0]:,rind] = phh_mon[:,rind]
    tic_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*tic_mon[0,rind]
    tic_com[flo10.shape[0]:,rind] = tic_mon[:,rind]
    sil_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*sil_mon[0,rind]
    sil_com[flo10.shape[0]:,rind] = sil_mon[:,rind]

ind24_1997 = 84  # 1997-01-31
ind24_2006 = 204 # 2007-01-31
for r_i in range(len(nm24)):
    rind = rnames.index(nm24[r_i])
    flo_com[:flo10.shape[0],rind] = flo24[ind24_1997:ind24_2006,r_i,r_i]
    flo_com[flo10.shape[0]:,rind] = flo_mon[:,rind]
    nh4_com[:nh410.shape[0],rind] = nh424[ind24_1997:ind24_2006,r_i,r_i]
    nh4_com[nh410.shape[0]:,rind] = nh4_mon[:,rind]
    no3_com[:no310.shape[0],rind] = no324[ind24_1997:ind24_2006,r_i,r_i]
    no3_com[no310.shape[0]:,rind] = no3_mon[:,rind]
    po4_com[:po410.shape[0],rind] = po424[ind24_1997:ind24_2006,r_i,r_i]
    po4_com[po410.shape[0]:,rind] = po4_mon[:,rind]
    tnn_com[:tnn10.shape[0],rind] = tnn24[ind24_1997:ind24_2006,r_i,r_i]
    tnn_com[tnn10.shape[0]:,rind] = tnn_mon[:,rind]
    tpp_com[:tpp10.shape[0],rind] = tpp24[ind24_1997:ind24_2006,r_i,r_i]
    tpp_com[tpp10.shape[0]:,rind] = tpp_mon[:,rind]
    alk_com[:alk10.shape[0],rind] = alk24[ind24_1997:ind24_2006,r_i,r_i]
    alk_com[alk10.shape[0]:,rind] = alk_mon[:,rind]
    tem_com[:tem10.shape[0],rind] = tem24[ind24_1997:ind24_2006,r_i,r_i]
    tem_com[tem10.shape[0]:,rind] = tem_mon[:,rind]
    doo_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*doo_mon[0,rind]
    doo_com[flo10.shape[0]:,rind] = doo_mon[:,rind]
    phh_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*phh_mon[0,rind]
    phh_com[flo10.shape[0]:,rind] = phh_mon[:,rind]
    tic_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*tic_mon[0,rind]
    tic_com[flo10.shape[0]:,rind] = tic_mon[:,rind]
    sil_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*sil_mon[0,rind]
    sil_com[flo10.shape[0]:,rind] = sil_mon[:,rind]

# tijuana 1997-2017
tjdf = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/tijuana/tijuana_river_full_dataset.csv')
rind = rnames.index('tijuana_river')
tjdf['date'] = pd.to_datetime(tjdf['date'])
tjdf.set_index(tjdf['date'],inplace=True)
tjmon = tjdf.resample('M').mean()

flo_com[:flo10.shape[0],rind] = tjmon['flow m3/s']['1997':'2006']
toc_com[:flo10.shape[0],rind] = tjmon['TOC mg/L']['1997':'2006']*mg_l_c
nh4_com[:flo10.shape[0],rind] = tjmon['ammonia mg/L']['1997':'2006']*mg_l_n
no3_com[:flo10.shape[0],rind] = tjmon['nitrate mg/L']['1997':'2006']*mg_l_n
po4_com[:flo10.shape[0],rind] = tjmon['phosphate mg/L']['1997':'2006']*mg_l_p
tnn_com[:flo10.shape[0],rind] = tjmon['TN mg/L']['1997':'2006']*mg_l_n
tpp_com[:flo10.shape[0],rind] = tjmon['TP mg/L']['1997':'2006']*mg_l_p
onn_com[:flo10.shape[0],rind] = (tjmon['TN mg/L']['1997':'2006']-(tjmon['ammonia mg/L']['1997':'2006']+tjmon['nitrate mg/L']['1997':'2006']+tjmon['nitrite mg/L']['1997':'2006']))*mg_l_n
opp_com[:flo10.shape[0],rind] = (tjmon['TP mg/L']['1997':'2006']-tjmon['phosphate mg/L']['1997':'2006'])*mg_l_p
dfe_com[:flo10.shape[0],rind] = tjmon['iron mg/L']['1997':'2006']*mg_l_f*.2
tfe_com[:flo10.shape[0],rind] = tjmon['iron mg/L']['1997':'2006']*mg_l_f*.2
alk_com[:flo10.shape[0],rind] = tjmon['alkalinity mg/L']['1997':'2006']*mg_l_a
sal_com[:flo10.shape[0],rind] = tjmon['salinity PSU']['1997':'2006']
sal_com[flo10.shape[0]:,rind] = tjmon['salinity PSU']['2007':'2017']
tem_com[:flo10.shape[0],rind] = tjmon['temperature C']['1997':'2006']
doo_com[:flo10.shape[0],rind] = tjmon['dissolved oxygen mg/L']['1997':'2006']*mg_l_o
doo_com[flo10.shape[0]:,rind] = tjmon['dissolved oxygen mg/L']['2007':'2017']*mg_l_o
phh_com[:flo10.shape[0],rind] = tjmon['pH']['1997':'2006']
sil_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*sil_mon[0,rind]

# santa margarita 1997-2006
smdf = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/hspfbin/smr_1997_2006_daily_full.csv')
rind = rnames.index('santa_margarita')
smdf['20d'] = pd.to_datetime(smdf['20d'])
smdf.set_index(smdf['20d'],inplace=True)
smmon = smdf.resample('M').mean()

flo_com[:flo10.shape[0],rind] = smmon['flow m3/s']['1997':'2006']
flo_com[:,rind][np.isnan(flo_com[:,rind])] = 0
toc_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*np.nan
nh4_com[:flo10.shape[0],rind] = smmon['NH4 mg/L']['1997':'2006']*mg_l_n
no3_com[:flo10.shape[0],rind] = smmon['NO3 mg/L']['1997':'2006']*mg_l_n
po4_com[:flo10.shape[0],rind] = smmon['PO4 mg/L']['1997':'2006']*mg_l_p
tnn_com[:flo10.shape[0],rind] = (smmon['NH4 mg/L']+smmon['NO3 mg/L']+smmon['NO2 mg/L'])*mg_l_n
tpp_com[:flo10.shape[0],rind] = smmon['PO4 mg/L']['1997':'2006']*mg_l_p
onn_com[:flo10.shape[0],r_i] = np.array(list(onn_mon[:12,rind])*10)
onn_com[flo10.shape[0]:,r_i] = onn_mon[:,rind]
opp_com[:flo10.shape[0],r_i] = np.array(list(opp_mon[:12,rind])*10)
opp_com[flo10.shape[0]:,r_i] = opp_mon[:,rind]
tfe_com[:flo10.shape[0],r_i] = np.array(list(tfe_mon[:12,rind])*10)
tfe_com[flo10.shape[0]:,r_i] = tfe_mon[:,rind]
dfe_com[:flo10.shape[0],r_i] = np.array(list(dfe_mon[:12,rind])*10)
dfe_com[flo10.shape[0]:,r_i] = dfe_mon[:,rind]
alk_com[:flo10.shape[0],rind] = smmon['alk mg/L']['1997':'2006']*mg_l_a
sal_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*val_sa
tem_com[:flo10.shape[0],rind] = np.array((list(tem_com[:12,rind])*10))
doo_com[:flo10.shape[0],rind] = smmon['DO mg/L']['1997':'2006']*mg_l_o
phh_com[:flo10.shape[0],rind] = smmon['pH']['1997':'2006']
tic_com[:flo10.shape[0],rind] = smmon['TIC mg/L']['1997':'2006']
sil_com[:flo10.shape[0],rind] = np.ones(flo10.shape[0])*sil_mon[0,rind]

# bell canyon
bcdf = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/supplemental_rivers/bell_canyon_daily_1997_2018.csv')
bcdf['2'] = pd.to_datetime(bcdf['2'])
bcdf.set_index(bcdf['2'],inplace=True)
bcmon = bcdf.resample('M').mean()
bcmon['4'][np.isnan(bcmon['4'])] = 0
r_i = rnames.index('bell_canyon')
tem_com[:,r_i] = bcmon['5']
doo_com[:,r_i] = doo_com[:,r_i]*mg_l_o

wet_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in wet_m:
        wet_flows_l.append(bcmon['4'][f_i])

dry_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in dry_m:
        dry_flows_l.append(bcmon['4'][f_i])

wet_flows = np.array(wet_flows_l)
wet_med = np.nanmedian(wet_flows)
if wet_med == 0:
    wet_med = np.nanmean(wet_flows)
print('wet median: ',wet_med)

dry_flows = np.array(dry_flows_l)
dry_med = np.nanmedian(dry_flows)
if dry_med == 0:
    dry_med = np.nanmean(dry_flows)

print('dry median: ',dry_med)
# use river conc spreadsheet
# river rows
rind = np.where(con_fi[0]==rnames[r_i])[0]
# wet conc
wettoc = con_fi[2][rind[0]]*mg_l_c
wetnh4 = con_fi[3][rind[0]]*mg_l_n
wetno3 = con_fi[4][rind[0]]*mg_l_n
wetpo4 = con_fi[5][rind[0]]*mg_l_p
wettnn = con_fi[6][rind[0]]*mg_l_n
wettpp = con_fi[7][rind[0]]*mg_l_p
wetonn = con_fi[8][rind[0]]*mg_l_n
wetopp = con_fi[9][rind[0]]*mg_l_p
wetdfe = con_fi[10][rind[0]]*mg_l_f*(1./1000)
wettfe = con_fi[11][rind[0]]*mg_l_f*(1./1000)
wetalk = con_fi[12][rind[0]]*mg_l_a
wetsil = con_fi[14][rind[0]]*mg_l_s
# winter dry conc
wintoc = con_fi[2][rind[1]]*mg_l_c
winnh4 = con_fi[3][rind[1]]*mg_l_n
winno3 = con_fi[4][rind[1]]*mg_l_n
winpo4 = con_fi[5][rind[1]]*mg_l_p
wintnn = con_fi[6][rind[1]]*mg_l_n
wintpp = con_fi[7][rind[1]]*mg_l_p
winonn = con_fi[8][rind[1]]*mg_l_n
winopp = con_fi[9][rind[1]]*mg_l_p
windfe = con_fi[10][rind[1]]*mg_l_f*(1./1000)
wintfe = con_fi[11][rind[1]]*mg_l_f*(1./1000)
winalk = con_fi[12][rind[1]]*mg_l_a
winsil = con_fi[14][rind[1]]*mg_l_s
# summer dry conc
sumtoc = con_fi[2][rind[2]]*mg_l_c
sumnh4 = con_fi[3][rind[2]]*mg_l_n
sumno3 = con_fi[4][rind[2]]*mg_l_n
sumpo4 = con_fi[5][rind[2]]*mg_l_p
sumtnn = con_fi[6][rind[2]]*mg_l_n
sumtpp = con_fi[7][rind[2]]*mg_l_p
sumonn = con_fi[8][rind[2]]*mg_l_n
sumopp = con_fi[9][rind[2]]*mg_l_p
sumdfe = con_fi[10][rind[2]]*mg_l_f*(1./1000)
sumtfe = con_fi[11][rind[2]]*mg_l_f*(1./1000)
sumalk = con_fi[12][rind[2]]*mg_l_a
sumsil = con_fi[14][rind[2]]*mg_l_s

for d_i in range(bcmon['4'].shape[0]):
    flo_com[d_i,r_i] = bcmon['4'][d_i]
    if bcmon['4'][d_i]/wet_med >= 2:
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif (
        (bcmon['4'][d_i-1]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-2]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-3]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2)
       ):
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in dry_m:
        # use summer dry flow conc
        toc_com[d_i,r_i] = sumtoc 
        nh4_com[d_i,r_i] = sumnh4 
        no3_com[d_i,r_i] = sumno3 
        po4_com[d_i,r_i] = sumpo4 
        tnn_com[d_i,r_i] = sumtnn 
        tpp_com[d_i,r_i] = sumtpp 
        onn_com[d_i,r_i] = sumonn 
        opp_com[d_i,r_i] = sumopp 
        dfe_com[d_i,r_i] = sumdfe 
        tfe_com[d_i,r_i] = sumtfe 
        alk_com[d_i,r_i] = sumalk 
        sil_com[d_i,r_i] = sumsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in wet_m:
        # use winter dry flow conc
        toc_com[d_i,r_i] = wintoc 
        nh4_com[d_i,r_i] = winnh4 
        no3_com[d_i,r_i] = winno3 
        po4_com[d_i,r_i] = winpo4 
        tnn_com[d_i,r_i] = wintnn 
        tpp_com[d_i,r_i] = wintpp 
        onn_com[d_i,r_i] = winonn 
        opp_com[d_i,r_i] = winopp 
        dfe_com[d_i,r_i] = windfe 
        tfe_com[d_i,r_i] = wintfe 
        alk_com[d_i,r_i] = winalk 
        sil_com[d_i,r_i] = winsil 

# arroyo honda
bcdf = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/supplemental_rivers/arroyo_honda_creek_daily_1997_2018.csv')
bcdf['2'] = pd.to_datetime(bcdf['2'])
bcdf.set_index(bcdf['2'],inplace=True)
bcmon = bcdf.resample('M').mean()
bcmon['4'][np.isnan(bcmon['4'])] = 0
r_i = rnames.index('arroyo_honda_creek')
tem_com[:,r_i] = bcmon['5']
doo_com[:,r_i] = doo_com[:,r_i]*mg_l_o

wet_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in wet_m:
        wet_flows_l.append(bcmon['4'][f_i])

dry_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in dry_m:
        dry_flows_l.append(bcmon['4'][f_i])

wet_flows = np.array(wet_flows_l)
wet_med = np.nanmedian(wet_flows)
if wet_med == 0:
    wet_med = np.nanmean(wet_flows)
print('wet median: ',wet_med)

dry_flows = np.array(dry_flows_l)
dry_med = np.nanmedian(dry_flows)
if dry_med == 0:
    dry_med = np.nanmean(dry_flows)

print('dry median: ',dry_med)
# use river conc spreadsheet
# river rows
rind = np.where(con_fi[0]==rnames[r_i])[0]
# wet conc
wettoc = con_fi[2][rind[0]]*mg_l_c
wetnh4 = con_fi[3][rind[0]]*mg_l_n
wetno3 = con_fi[4][rind[0]]*mg_l_n
wetpo4 = con_fi[5][rind[0]]*mg_l_p
wettnn = con_fi[6][rind[0]]*mg_l_n
wettpp = con_fi[7][rind[0]]*mg_l_p
wetonn = con_fi[8][rind[0]]*mg_l_n
wetopp = con_fi[9][rind[0]]*mg_l_p
wetdfe = con_fi[10][rind[0]]*mg_l_f*(1./1000)
wettfe = con_fi[11][rind[0]]*mg_l_f*(1./1000)
wetalk = con_fi[12][rind[0]]*mg_l_a
wetsil = con_fi[14][rind[0]]*mg_l_s
# winter dry conc
wintoc = con_fi[2][rind[1]]*mg_l_c
winnh4 = con_fi[3][rind[1]]*mg_l_n
winno3 = con_fi[4][rind[1]]*mg_l_n
winpo4 = con_fi[5][rind[1]]*mg_l_p
wintnn = con_fi[6][rind[1]]*mg_l_n
wintpp = con_fi[7][rind[1]]*mg_l_p
winonn = con_fi[8][rind[1]]*mg_l_n
winopp = con_fi[9][rind[1]]*mg_l_p
windfe = con_fi[10][rind[1]]*mg_l_f*(1./1000)
wintfe = con_fi[11][rind[1]]*mg_l_f*(1./1000)
winalk = con_fi[12][rind[1]]*mg_l_a
winsil = con_fi[14][rind[1]]*mg_l_s
# summer dry conc
sumtoc = con_fi[2][rind[2]]*mg_l_c
sumnh4 = con_fi[3][rind[2]]*mg_l_n
sumno3 = con_fi[4][rind[2]]*mg_l_n
sumpo4 = con_fi[5][rind[2]]*mg_l_p
sumtnn = con_fi[6][rind[2]]*mg_l_n
sumtpp = con_fi[7][rind[2]]*mg_l_p
sumonn = con_fi[8][rind[2]]*mg_l_n
sumopp = con_fi[9][rind[2]]*mg_l_p
sumdfe = con_fi[10][rind[2]]*mg_l_f*(1./1000)
sumtfe = con_fi[11][rind[2]]*mg_l_f*(1./1000)
sumalk = con_fi[12][rind[2]]*mg_l_a
sumsil = con_fi[14][rind[2]]*mg_l_s

for d_i in range(bcmon['4'].shape[0]):
    flo_com[d_i,r_i] = bcmon['4'][d_i]
    if bcmon['4'][d_i]/wet_med >= 2:
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif (
        (bcmon['4'][d_i-1]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-2]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-3]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2)
       ):
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in dry_m:
        # use summer dry flow conc
        toc_com[d_i,r_i] = sumtoc 
        nh4_com[d_i,r_i] = sumnh4 
        no3_com[d_i,r_i] = sumno3 
        po4_com[d_i,r_i] = sumpo4 
        tnn_com[d_i,r_i] = sumtnn 
        tpp_com[d_i,r_i] = sumtpp 
        onn_com[d_i,r_i] = sumonn 
        opp_com[d_i,r_i] = sumopp 
        dfe_com[d_i,r_i] = sumdfe 
        tfe_com[d_i,r_i] = sumtfe 
        alk_com[d_i,r_i] = sumalk 
        sil_com[d_i,r_i] = sumsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in wet_m:
        # use winter dry flow conc
        toc_com[d_i,r_i] = wintoc 
        nh4_com[d_i,r_i] = winnh4 
        no3_com[d_i,r_i] = winno3 
        po4_com[d_i,r_i] = winpo4 
        tnn_com[d_i,r_i] = wintnn 
        tpp_com[d_i,r_i] = wintpp 
        onn_com[d_i,r_i] = winonn 
        opp_com[d_i,r_i] = winopp 
        dfe_com[d_i,r_i] = windfe 
        tfe_com[d_i,r_i] = wintfe 
        alk_com[d_i,r_i] = winalk 
        sil_com[d_i,r_i] = winsil 

# refugio creek
bcdf = pd.read_csv('/data/project1/minnaho/river_data/updated_2013_2017/supplemental_rivers/refugio_creek_daily_1997_2018.csv')
bcdf['2'] = pd.to_datetime(bcdf['2'])
bcdf.set_index(bcdf['2'],inplace=True)
bcmon = bcdf.resample('M').mean()
bcmon['4'][np.isnan(bcmon['4'])] = 0
r_i = rnames.index('refugio_creek')
tem_com[:,r_i] = bcmon['5']
doo_com[:,r_i] = doo_com[:,r_i]*mg_l_o

wet_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in wet_m:
        wet_flows_l.append(bcmon['4'][f_i])

dry_flows_l = []
for f_i in range(bcmon['4'].shape[0]):
    if bcmon.index[f_i].month in dry_m:
        dry_flows_l.append(bcmon['4'][f_i])

wet_flows = np.array(wet_flows_l)
wet_med = np.nanmedian(wet_flows)
if wet_med == 0:
    wet_med = np.nanmean(wet_flows)
print('wet median: ',wet_med)

dry_flows = np.array(dry_flows_l)
dry_med = np.nanmedian(dry_flows)
if dry_med == 0:
    dry_med = np.nanmean(dry_flows)

print('dry median: ',dry_med)
# use river conc spreadsheet
# river rows
rind = np.where(con_fi[0]==rnames[r_i])[0]
# wet conc
wettoc = con_fi[2][rind[0]]*mg_l_c
wetnh4 = con_fi[3][rind[0]]*mg_l_n
wetno3 = con_fi[4][rind[0]]*mg_l_n
wetpo4 = con_fi[5][rind[0]]*mg_l_p
wettnn = con_fi[6][rind[0]]*mg_l_n
wettpp = con_fi[7][rind[0]]*mg_l_p
wetonn = con_fi[8][rind[0]]*mg_l_n
wetopp = con_fi[9][rind[0]]*mg_l_p
wetdfe = con_fi[10][rind[0]]*mg_l_f*(1./1000)
wettfe = con_fi[11][rind[0]]*mg_l_f*(1./1000)
wetalk = con_fi[12][rind[0]]*mg_l_a
wetsil = con_fi[14][rind[0]]*mg_l_s
# winter dry conc
wintoc = con_fi[2][rind[1]]*mg_l_c
winnh4 = con_fi[3][rind[1]]*mg_l_n
winno3 = con_fi[4][rind[1]]*mg_l_n
winpo4 = con_fi[5][rind[1]]*mg_l_p
wintnn = con_fi[6][rind[1]]*mg_l_n
wintpp = con_fi[7][rind[1]]*mg_l_p
winonn = con_fi[8][rind[1]]*mg_l_n
winopp = con_fi[9][rind[1]]*mg_l_p
windfe = con_fi[10][rind[1]]*mg_l_f*(1./1000)
wintfe = con_fi[11][rind[1]]*mg_l_f*(1./1000)
winalk = con_fi[12][rind[1]]*mg_l_a
winsil = con_fi[14][rind[1]]*mg_l_s
# summer dry conc
sumtoc = con_fi[2][rind[2]]*mg_l_c
sumnh4 = con_fi[3][rind[2]]*mg_l_n
sumno3 = con_fi[4][rind[2]]*mg_l_n
sumpo4 = con_fi[5][rind[2]]*mg_l_p
sumtnn = con_fi[6][rind[2]]*mg_l_n
sumtpp = con_fi[7][rind[2]]*mg_l_p
sumonn = con_fi[8][rind[2]]*mg_l_n
sumopp = con_fi[9][rind[2]]*mg_l_p
sumdfe = con_fi[10][rind[2]]*mg_l_f*(1./1000)
sumtfe = con_fi[11][rind[2]]*mg_l_f*(1./1000)
sumalk = con_fi[12][rind[2]]*mg_l_a
sumsil = con_fi[14][rind[2]]*mg_l_s

for d_i in range(bcmon['4'].shape[0]):
    flo_com[d_i,r_i] = bcmon['4'][d_i]
    if bcmon['4'][d_i]/wet_med >= 2:
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif (
        (bcmon['4'][d_i-1]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-2]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2) or
        (bcmon['4'][d_i-3]/wet_med >= 2 and bcmon['4'][d_i]/wet_med < 2)
       ):
        # use wet flow conc
        toc_com[d_i,r_i] = wettoc 
        nh4_com[d_i,r_i] = wetnh4 
        no3_com[d_i,r_i] = wetno3 
        po4_com[d_i,r_i] = wetpo4 
        tnn_com[d_i,r_i] = wettnn 
        tpp_com[d_i,r_i] = wettpp 
        onn_com[d_i,r_i] = wetonn 
        opp_com[d_i,r_i] = wetopp 
        dfe_com[d_i,r_i] = wetdfe 
        tfe_com[d_i,r_i] = wettfe 
        alk_com[d_i,r_i] = wetalk 
        sil_com[d_i,r_i] = wetsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in dry_m:
        # use summer dry flow conc
        toc_com[d_i,r_i] = sumtoc 
        nh4_com[d_i,r_i] = sumnh4 
        no3_com[d_i,r_i] = sumno3 
        po4_com[d_i,r_i] = sumpo4 
        tnn_com[d_i,r_i] = sumtnn 
        tpp_com[d_i,r_i] = sumtpp 
        onn_com[d_i,r_i] = sumonn 
        opp_com[d_i,r_i] = sumopp 
        dfe_com[d_i,r_i] = sumdfe 
        tfe_com[d_i,r_i] = sumtfe 
        alk_com[d_i,r_i] = sumalk 
        sil_com[d_i,r_i] = sumsil 
    elif bcmon['4'][d_i]/wet_med < 2 and df.index[d_i].month in wet_m:
        # use winter dry flow conc
        toc_com[d_i,r_i] = wintoc 
        nh4_com[d_i,r_i] = winnh4 
        no3_com[d_i,r_i] = winno3 
        po4_com[d_i,r_i] = winpo4 
        tnn_com[d_i,r_i] = wintnn 
        tpp_com[d_i,r_i] = wintpp 
        onn_com[d_i,r_i] = winonn 
        opp_com[d_i,r_i] = winopp 
        dfe_com[d_i,r_i] = windfe 
        tfe_com[d_i,r_i] = wintfe 
        alk_com[d_i,r_i] = winalk 
        sil_com[d_i,r_i] = winsil 

toc_com[toc_com<0] = 0
nh4_com[nh4_com<0] = 0
no3_com[no3_com<0] = 0
po4_com[po4_com<0] = 0
tnn_com[tnn_com<0] = 0
tpp_com[tpp_com<0] = 0
onn_com[onn_com<0] = 0
opp_com[opp_com<0] = 0
dfe_com[dfe_com<0] = 0
dfe_com[np.isnan(dfe_com)] = val_df
tfe_com[tfe_com<0] = 0
tfe_com[np.isnan(tfe_com)] = val_tf
alk_com[alk_com<0] = 0
doo_com[doo_com<0] = 0
tic_com[tic_com<0] = 0
sil_com[sil_com<0] = 0

for s_i in range(sil_com.shape[1]):
    sil_com[:,s_i] = np.nanmax(sil_com[:,s_i])  
#    if s_i != rnames.index('tijuana_river'):
#        dfe_com[:,s_i] = np.nanmax(dfe_com[:,s_i])  

# time array
timeunit = 'days since 1997-01-01'
timenum = date2num(bcmon.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('rivers_1997_2017_monthly.nc','w')
ncf.description = ','.join(rnames)

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 75 rivers

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
tic_v = ncf.createVariable('total_inorganic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'C'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
tic_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'PSU'
dfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_arr
lon_v[:] = lon_arr
flo_v[:,:] = flo_com
nh4_v[:,:] = nh4_com
no3_v[:,:] = no3_com
doo_v[:,:] = doo_com
tem_v[:,:] = tem_com
phh_v[:,:] = phh_com
tpp_v[:,:] = tpp_com
tnn_v[:,:] = tnn_com
po4_v[:,:] = po4_com
opp_v[:,:] = opp_com
toc_v[:,:] = toc_com
tic_v[:,:] = tic_com
onn_v[:,:] = onn_com
tfe_v[:,:] = tfe_com
alk_v[:,:] = alk_com
sal_v[:,:] = sal_com
dfe_v[:,:] = dfe_com
sil_v[:,:] = sil_com

ncf.close()

# monthly xlsx

writer = pd.ExcelWriter('rivers_1997_2017_monthly.xlsx')

# print to excel file
for r_i in range(flo_com.shape[1]):
    lat_tem = np.empty((flo_com.shape[0]))
    lat_tem.fill(lat_arr[r_i])
    lon_tem = np.empty((flo_com.shape[0]))
    lon_tem.fill(lon_arr[r_i])
    save_df = pd.DataFrame({'date':bcmon.index.date,
    'flow m3/s':flo_com[:,r_i],
    'NH4 mmol/m3':nh4_com[:,r_i],
    'NO3 mmol/m3':no3_com[:,r_i],
    'DO mmol/m3':doo_com[:,r_i],
    'temperature C':tem_com[:,r_i],
    'pH':phh_com[:,r_i],
    'TN mmol/m3':tnn_com[:,r_i],
    'TP mmol/m3':tpp_com[:,r_i],
    'PO4 mmol/m3':po4_com[:,r_i],
    'OP mmol/m3':opp_com[:,r_i],
    'TOC mmol/m3':toc_com[:,r_i],
    'ON mmol/m3':onn_com[:,r_i],
    'total Fe mmol/m3':tfe_com[:,r_i],
    'Alk mmol/m3':alk_com[:,r_i],
    'salinity PSU':sal_com[:,r_i],
    'dissolved Fe mmol/m3':dfe_com[:,r_i],
    'TIC mmol/m3':tic_com[:,r_i],
    'SiO4 mmol/m3':sil_com[:,r_i],
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df.to_excel(writer,sheet_name=rnames[r_i][:31])

writer.save()

# make daily data that is monthly interpolated 1997-2006 and daily 2007-2017
pd_daily = pd.date_range(start='1997-01-01',end='2017-12-31',freq='D')
in07 = 3652

flo_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
nh4_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
no3_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
doo_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
tem_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
phh_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
tpp_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
tnn_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
po4_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
opp_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
toc_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
tic_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
onn_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
tfe_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
alk_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
sal_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
dfe_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan
sil_day = np.ones((pd_daily.shape[0],len(rnames)))*np.nan

flo_day[in07:,:] = flo_arr[:,:]
nh4_day[in07:,:] = nh4_arr[:,:]
no3_day[in07:,:] = no3_arr[:,:]
doo_day[in07:,:] = doo_arr[:,:]
tem_day[in07:,:] = tem_arr[:,:]
phh_day[in07:,:] = phh_arr[:,:]
tpp_day[in07:,:] = tpp_arr[:,:]
tnn_day[in07:,:] = tnn_arr[:,:]
po4_day[in07:,:] = po4_arr[:,:]
opp_day[in07:,:] = opp_arr[:,:]
toc_day[in07:,:] = toc_arr[:,:]
tic_day[in07:,:] = tic_arr[:,:]
onn_day[in07:,:] = onn_arr[:,:]
tfe_day[in07:,:] = tfe_arr[:,:]
alk_day[in07:,:] = alk_arr[:,:]
sal_day[in07:,:] = sal_arr[:,:]
dfe_day[in07:,:] = dfe_arr[:,:]
sil_day[in07:,:] = sil_arr[:,:]

for r_i in range(flo_com.shape[1]):
    lat_tem = np.empty((flo_com.shape[0]))
    lat_tem.fill(lat_arr[r_i])
    lon_tem = np.empty((flo_com.shape[0]))
    lon_tem.fill(lon_arr[r_i])
    save_df = pd.DataFrame({'date':bcmon.index.date,
    'flow m3/s':flo_com[:,r_i],
    'NH4 mmol/m3':nh4_com[:,r_i],
    'NO3 mmol/m3':no3_com[:,r_i],
    'DO mmol/m3':doo_com[:,r_i],
    'temperature C':tem_com[:,r_i],
    'pH':phh_com[:,r_i],
    'TN mmol/m3':tnn_com[:,r_i],
    'TP mmol/m3':tpp_com[:,r_i],
    'PO4 mmol/m3':po4_com[:,r_i],
    'OP mmol/m3':opp_com[:,r_i],
    'TOC mmol/m3':toc_com[:,r_i],
    'ON mmol/m3':onn_com[:,r_i],
    'total Fe mmol/m3':tfe_com[:,r_i],
    'Alk mmol/m3':alk_com[:,r_i],
    'salinity PSU':sal_com[:,r_i],
    'dissolved Fe mmol/m3':dfe_com[:,r_i],
    'TIC mmol/m3':tic_com[:,r_i],
    'SiO4 mmol/m3':sil_com[:,r_i],
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df['date'] = pd.to_datetime(save_df['date'])
    save_df.set_index(save_df['date'],inplace=True)
    save_df.loc[pd.to_datetime('1997-01-01')] = np.nan
    save_df.loc['1997-01-01'] = save_df.loc['1997-01-31'].values
    day_df = save_df.resample('D').interpolate()
    flo_day[:in07,r_i] = day_df['flow m3/s'][:in07]
    nh4_day[:in07,r_i] = day_df['NH4 mmol/m3'][:in07]
    no3_day[:in07,r_i] = day_df['NO3 mmol/m3'][:in07]
    doo_day[:in07,r_i] = day_df['DO mmol/m3'][:in07]
    tem_day[:in07,r_i] = day_df['temperature C'][:in07]
    phh_day[:in07,r_i] = day_df['pH'][:in07]
    tpp_day[:in07,r_i] = day_df['TN mmol/m3'][:in07]
    tnn_day[:in07,r_i] = day_df['TP mmol/m3'][:in07]
    po4_day[:in07,r_i] = day_df['PO4 mmol/m3'][:in07]
    opp_day[:in07,r_i] = day_df['OP mmol/m3'][:in07]
    toc_day[:in07,r_i] = day_df['TOC mmol/m3'][:in07]
    tic_day[:in07,r_i] = day_df['ON mmol/m3'][:in07]
    onn_day[:in07,r_i] = day_df['total Fe mmol/m3'][:in07]
    tfe_day[:in07,r_i] = day_df['Alk mmol/m3'][:in07]
    alk_day[:in07,r_i] = day_df['salinity PSU'][:in07]
    sal_day[:in07,r_i] = day_df['dissolved Fe mmol/m3'][:in07]
    dfe_day[:in07,r_i] = day_df['TIC mmol/m3'][:in07]
    sil_day[:in07,r_i] = day_df['SiO4 mmol/m3'][:in07]


# daily xlsx

writer = pd.ExcelWriter('rivers_1997_2017_daily.xlsx')

# print to excel file
for r_i in range(flo_day.shape[1]):
    lat_tem = np.empty((flo_day.shape[0]))
    lat_tem.fill(lat_arr[r_i])
    lon_tem = np.empty((flo_day.shape[0]))
    lon_tem.fill(lon_arr[r_i])
    save_df = pd.DataFrame({'date':day_df.index.date,
    'flow m3/s':flo_day[:,r_i],
    'NH4 mmol/m3':nh4_day[:,r_i],
    'NO3 mmol/m3':no3_day[:,r_i],
    'DO mmol/m3':doo_day[:,r_i],
    'temperature C':tem_day[:,r_i],
    'pH':phh_day[:,r_i],
    'TN mmol/m3':tnn_day[:,r_i],
    'TP mmol/m3':tpp_day[:,r_i],
    'PO4 mmol/m3':po4_day[:,r_i],
    'OP mmol/m3':opp_day[:,r_i],
    'TOC mmol/m3':toc_day[:,r_i],
    'ON mmol/m3':onn_day[:,r_i],
    'total Fe mmol/m3':tfe_day[:,r_i],
    'Alk mmol/m3':alk_day[:,r_i],
    'salinity PSU':sal_day[:,r_i],
    'dissolved Fe mmol/m3':dfe_day[:,r_i],
    'TIC mmol/m3':tic_day[:,r_i],
    'SiO4 mmol/m3':sil_day[:,r_i],
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df.to_excel(writer,sheet_name=rnames[r_i][:31])

writer.save()


# daily 1997-2017 netcdf
# time array
timeunit = 'days since 1997-01-01'
timenum = date2num(day_df.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('rivers_1997_2017_daily.nc','w')
ncf.description = ','.join(rnames)

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 75 rivers

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
tnn_v = ncf.createVariable('total_N',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
tic_v = ncf.createVariable('total_inorganic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'C'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
tnn_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
tic_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'PSU'
dfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_arr
lon_v[:] = lon_arr
flo_v[:,:] = flo_day
nh4_v[:,:] = nh4_day
no3_v[:,:] = no3_day
doo_v[:,:] = doo_day
tem_v[:,:] = tem_day
phh_v[:,:] = phh_day
tpp_v[:,:] = tpp_day
tnn_v[:,:] = tnn_day
po4_v[:,:] = po4_day
opp_v[:,:] = opp_day
toc_v[:,:] = toc_day
tic_v[:,:] = tic_day
onn_v[:,:] = onn_day
tfe_v[:,:] = tfe_day
alk_v[:,:] = alk_day
sal_v[:,:] = sal_day
dfe_v[:,:] = dfe_day
sil_v[:,:] = sil_day

ncf.close()

