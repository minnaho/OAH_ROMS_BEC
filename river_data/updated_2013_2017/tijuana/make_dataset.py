import numpy as np
import pandas as pd

# flow gauge
gauge_csv = pd.read_csv('tijuana_river_gauge_1997_2018.csv',skiprows=2,header=None)
form = '%m/%d/%Y %H:%M'
dates = pd.to_datetime(gauge_csv[0],format=form).dt.date
gauge_csv.set_index(dates,inplace=True)
df = pd.DataFrame(gauge_csv[1])

# transboundary flows
trans_csv = pd.read_csv('transboundary_flow_Tijuana_River_daily.csv',skiprows=4,header=None)
form = '%m/%d/%Y'
dates = pd.to_datetime(trans_csv[0],format=form)
trans_csv.set_index(dates,inplace=True)
typeb_flo = trans_csv[2]
typea_flo = trans_csv[4]
typea_nam = trans_csv[5]

# combine flows
df = df.join(typeb_flo[:'2018'],how='outer')
df = df.join(typea_flo[:'2018'],how='outer')
df = df.join(typea_nam[:'2018'],how='outer')

# read in concentrations
conc_csv = pd.read_csv('tijuana_constituents.csv',skiprows=7,header=None)

# create dataframe with all data
flo = np.empty((df.shape[0]))
alk = np.empty((df.shape[0]))
nh4 = np.empty((df.shape[0]))
bod = np.empty((df.shape[0]))
doo = np.empty((df.shape[0]))
sal = np.empty((df.shape[0]))
no3 = np.empty((df.shape[0]))
no2 = np.empty((df.shape[0]))
po4 = np.empty((df.shape[0]))
phh = np.empty((df.shape[0]))
tem = np.empty((df.shape[0]))
tkn = np.empty((df.shape[0]))
tnn = np.empty((df.shape[0]))
toc = np.empty((df.shape[0]))
tpp = np.empty((df.shape[0]))
fee = np.empty((df.shape[0]))

wet_m = [11,12,1,2,3,4]
for d_i in range(df.shape[0]):
    flo[d_i] = df[1][d_i]
    if flo[d_i] < 1.21 and df.index[d_i].month not in wet_m:
        alk[d_i] =  float(conc_csv[1][4])
        nh4[d_i] =  float(conc_csv[2][4])
        bod[d_i] =  float(conc_csv[3][4])
        doo[d_i] =  float(conc_csv[4][4])
        sal[d_i] =  float(conc_csv[5][4])
        no3[d_i] =  float(conc_csv[6][4])
        no2[d_i] =  float(conc_csv[7][4])
        po4[d_i] =  float(conc_csv[8][4])
        phh[d_i] =  float(conc_csv[9][4])
        tem[d_i] = float(conc_csv[10][4])
        tkn[d_i] = float(conc_csv[11][4])
        tnn[d_i] = float(conc_csv[12][4])
        toc[d_i] = float(conc_csv[13][4])
        tpp[d_i] = float(conc_csv[14][4])
        fee[d_i] = float(conc_csv[15][4])/1000. # ug/L
    if flo[d_i] < 1.21 and df.index[d_i].month in wet_m:
        alk[d_i] =  float(conc_csv[1][5])
        nh4[d_i] =  float(conc_csv[2][5])
        bod[d_i] =  float(conc_csv[3][5])
        doo[d_i] =  float(conc_csv[4][5])
        sal[d_i] =  float(conc_csv[5][5])
        no3[d_i] =  float(conc_csv[6][5])
        no2[d_i] =  float(conc_csv[7][5])
        po4[d_i] =  float(conc_csv[8][5])
        phh[d_i] =  float(conc_csv[9][5])
        tem[d_i] = float(conc_csv[10][5])
        tkn[d_i] = float(conc_csv[11][5])
        tnn[d_i] = float(conc_csv[12][5])
        toc[d_i] = float(conc_csv[13][5])
        tpp[d_i] = float(conc_csv[14][5])
        fee[d_i] = float(conc_csv[15][5])/1000. # ug/L
    if flo[d_i] >= 1.21:
        alk[d_i] =  float(conc_csv[1][6])
        nh4[d_i] =  float(conc_csv[2][6])
        bod[d_i] =  float(conc_csv[3][6])
        doo[d_i] =  float(conc_csv[4][6])
        sal[d_i] =  float(conc_csv[5][6])
        no3[d_i] =  float(conc_csv[6][6])
        no2[d_i] =  float(conc_csv[7][6])
        po4[d_i] =  float(conc_csv[8][6])
        phh[d_i] =  float(conc_csv[9][6])
        tem[d_i] = float(conc_csv[10][6])
        tkn[d_i] = float(conc_csv[11][6])
        tnn[d_i] = float(conc_csv[12][6])
        toc[d_i] = float(conc_csv[13][6])
        tpp[d_i] = float(conc_csv[14][6])
        fee[d_i] = float(conc_csv[15][6])/1000. # ug/L
    if (
       (flo[d_i-1] >= 1.2 and flo[d_i] < 1.2) or
       (flo[d_i-2] >= 1.2 and flo[d_i] < 1.2) or
       (flo[d_i-3] >= 1.2 and flo[d_i] < 1.2)
       ):
        alk[d_i] =  float(conc_csv[1][6])
        nh4[d_i] =  float(conc_csv[2][6])
        bod[d_i] =  float(conc_csv[3][6])
        doo[d_i] =  float(conc_csv[4][6])
        sal[d_i] =  float(conc_csv[5][6])
        no3[d_i] =  float(conc_csv[6][6])
        no2[d_i] =  float(conc_csv[7][6])
        po4[d_i] =  float(conc_csv[8][6])
        phh[d_i] =  float(conc_csv[9][6])
        tem[d_i] = float(conc_csv[10][6])
        tkn[d_i] = float(conc_csv[11][6])
        tnn[d_i] = float(conc_csv[12][6])
        toc[d_i] = float(conc_csv[13][6])
        tpp[d_i] = float(conc_csv[14][6])
        fee[d_i] = float(conc_csv[15][6])/1000. # ug/L
    # type a transboundary
    if df[4][d_i] > 0 and df[5][d_i]=='Canyon del Sol':
        # all in mg/L except iron
        flo[d_i] += df[4][d_i]
        alk[d_i] = float(conc_csv[1][1])
        nh4[d_i] = float(conc_csv[2][1])
        bod[d_i] = float(conc_csv[3][1])
        doo[d_i] = float(conc_csv[4][1])
        sal[d_i] = float(conc_csv[5][1])
        no3[d_i] = float(conc_csv[6][1])
        no2[d_i] = float(conc_csv[7][1])
        po4[d_i] = float(conc_csv[8][1])
        phh[d_i] = float(conc_csv[9][1])
        tem[d_i] = float(conc_csv[10][1])
        tkn[d_i] = float(conc_csv[11][1])
        tnn[d_i] = float(conc_csv[12][1])
        toc[d_i] = float(conc_csv[13][1])
        tpp[d_i] = float(conc_csv[14][1])
        fee[d_i] = float(conc_csv[15][1])/1000. # ug/L
    if df[4][d_i] > 0 and df[5][d_i]=='Goat Canyon':
        flo[d_i] += df[4][d_i]
        alk[d_i] =  float(conc_csv[1][2])
        nh4[d_i] =  float(conc_csv[2][2])
        bod[d_i] =  float(conc_csv[3][2])
        doo[d_i] =  float(conc_csv[4][2])
        sal[d_i] =  float(conc_csv[5][2])
        no3[d_i] =  float(conc_csv[6][2])
        no2[d_i] =  float(conc_csv[7][2])
        po4[d_i] =  float(conc_csv[8][2])
        phh[d_i] =  float(conc_csv[9][2])
        tem[d_i] = float(conc_csv[10][2])
        tkn[d_i] = float(conc_csv[11][2])
        tnn[d_i] = float(conc_csv[12][2])
        toc[d_i] = float(conc_csv[13][2])
        tpp[d_i] = float(conc_csv[14][2])
        fee[d_i] = float(conc_csv[15][2])/1000. # ug/L
    if df[4][d_i] > 0 and df[5][d_i]=='Stewart\'s Drain':
        flo[d_i] += df[4][d_i]
        alk[d_i] =  float(conc_csv[1][3])
        nh4[d_i] =  float(conc_csv[2][3])
        bod[d_i] =  float(conc_csv[3][3])
        doo[d_i] =  float(conc_csv[4][3])
        sal[d_i] =  float(conc_csv[5][3])
        no3[d_i] =  float(conc_csv[6][3])
        no2[d_i] =  float(conc_csv[7][3])
        po4[d_i] =  float(conc_csv[8][3])
        phh[d_i] =  float(conc_csv[9][3])
        tem[d_i] = float(conc_csv[10][3])
        tkn[d_i] = float(conc_csv[11][3])
        tnn[d_i] = float(conc_csv[12][3])
        toc[d_i] = float(conc_csv[13][3])
        tpp[d_i] = float(conc_csv[14][3])
        fee[d_i] = float(conc_csv[15][3])/1000. # ug/L
    # type b transboundary
    if df[2][d_i] > 0:
        # overwrites type A since type B usually orders
        # of magnitude greater in flow
        alk[d_i] =  float(conc_csv[1][7])
        nh4[d_i] =  float(conc_csv[2][7])
        bod[d_i] =  float(conc_csv[3][7])
        doo[d_i] =  float(conc_csv[4][7])
        sal[d_i] =  float(conc_csv[5][7])
        no3[d_i] =  float(conc_csv[6][7])
        no2[d_i] =  float(conc_csv[7][7])
        po4[d_i] =  float(conc_csv[8][7])
        phh[d_i] =  float(conc_csv[9][7])
        tem[d_i] = float(conc_csv[10][7])
        tkn[d_i] = float(conc_csv[11][7])
        tnn[d_i] = float(conc_csv[12][7])
        toc[d_i] = float(conc_csv[13][7])
        tpp[d_i] = float(conc_csv[14][7])
        fee[d_i] = float(conc_csv[15][7])/1000. # ug/L
        

full = pd.DataFrame({'date':df.index,'flow m3/s':flo,'alkalinity mg/L':alk,'ammonia mg/L':nh4,'BOD mg/L':bod,'dissolved oxygen mg/L':doo,'salinity PSU':sal,'nitrate mg/L':no3,'nitrite mg/L':no2,'phosphate mg/L':po4,'pH':phh,'temperature C':tem,'TKN mg/L':tkn,'TN mg/L':tnn,'TOC mg/L':toc,'TP mg/L':tpp,'iron mg/L':fee})

full.to_csv('tijuana_river_full_dataset.csv')
    






