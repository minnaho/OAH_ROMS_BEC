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
sm_temp = sm['temperature C']

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
opp_arr = np.empty((flow.shape[0],len(rnames)))
dfe_arr = np.empty((flow.shape[0],len(rnames)))
tfe_arr = np.empty((flow.shape[0],len(rnames)))
alk_arr = np.empty((flow.shape[0],len(rnames)))
sal_arr = np.empty((flow.shape[0],len(rnames)))
sal_arr.fill(0.52)
tem_arr = np.empty((flow.shape[0],len(rnames)))
# set all temps to santa monica temperature, except
# tijuana that is changed in the loop
for r_i in range(tem_arr.shape[1]):
    tem_arr[:,r_i] = sm_temp[:endind]

# only tijuana and santa margarita have dissolved o
doo_arr = np.empty((flow.shape[0],len(rnames)))
doo_arr.fill(np.nan)
# only tijuana and santa margarita have pH
phh_arr = np.empty((flow.shape[0],len(rnames)))
phh_arr.fill(np.nan)
# only santa margarita has TIC
tic_arr = np.empty((flow.shape[0],len(rnames)))
tic_arr.fill(np.nan)

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
        wetonn = np.nan 
        wetopp = np.nan 
        wetdfe = np.nan 
        wettfe = np.nan 
        wetalk = df['alkalinity mg/L'][0]
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
            winonn = np.nan 
            winopp = np.nan 
            windfe = np.nan 
            wintfe = np.nan 
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
            sumonn = np.nan 
            sumopp = np.nan 
            sumdfe = np.nan 
            sumtfe = np.nan 
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
            sal_arr[d_i,r_i] = 0.52
            tem_arr[d_i,r_i] = df['temperature C'][d_i]
            doo_arr[d_i,r_i] = df['dissolved oxygen mg/L'][d_i]
            phh_arr[d_i,r_i] = df['pH'][d_i]
            tic_arr[d_i,r_i] = df['TIC mg/L total inorganic C'][d_i]

# mg/L to mmol/m3 
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855

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
alk_arr = alk_arr*mg_l_c
doo_arr = doo_arr*mg_l_o
tic_arr = tic_arr*mg_l_c


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
    'latitude':lat_tem,
    'longitude':lon_tem},
    index=None,columns=None)
    save_df.to_excel(writer,sheet_name=rnames[r_i][:31])

writer.save()

