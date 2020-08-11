import numpy as np
import pandas as pd
from netCDF4 import Dataset
import pickle

xl_path = '../potw_outfall_data/Inland POTW data.xlsx'

xls = pd.ExcelFile(xl_path)

# get TN and TP from summary sheet
tnn_val = np.empty((9))
tpp_val = np.empty((9))

# City of Escondido-Escondido Creek
tnn_val[0] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][4]
tpp_val[0] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][4]

# Michaelson-San Diego Creek
tnn_val[1] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][6]
tpp_val[1] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][6]

# LA river
tnn_val[2] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][9]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][10]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][11]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][12]
tpp_val[2] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][9]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][10]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][11]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][12]

# San Gabriel river
tnn_val[3] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][14]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][15]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][16]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][17]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][18]
tpp_val[4] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][14]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][15]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][16]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][17]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][18]

# Tapia- Malibu Creek
tnn_val[4] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][20]
tpp_val[4] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][20]

# Padre Dam-San Diego River
tnn_val[5] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][2]
tpp_val[5] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][2]

# Calleguas Creek
tnn_val[6] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][22]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][23]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][24]
tpp_val[6] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][22]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][23]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][24]

# Santa Clara River
tnn_val[7] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][27]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][26]
tpp_val[7] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][27]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][26]

# Ventura
tnn_val[8] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[3][29]
tpp_val[8] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][29]

lb_to_kg = 0.45359237

# append manually DIN/DIP value for each river
din_val = []
dip_val = []

# City of Escondido-Escondido Creek
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[1],header=None)[1][4]*lb_to_kg)
dip_val.append(np.nan) # no P values

# Michaelson-San Diego Creek
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[2],header=None)[1][13]*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[2],header=None)[1][15]*lb_to_kg)

# LA river
# City of LA Tillman- LA River
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[3],header=None)[1][8]*lb_to_kg)
dip_val.append(np.nan) # no P values

# Pomona-LA RIver
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[4],header=None)[1][8]*lb_to_kg)
 # no P values

# Brubank-LA River
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[5],header=None)[1][9]*lb_to_kg)
 # no P values

# LA River- Glendale
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[6],header=None)[1][9]*lb_to_kg)
 # no P values

# San Gabriel river
# San Jose - San Gabriel River
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[7],header=None)[1][9]*lb_to_kg)
 # no P values

# Valencia-San Gabriel, same river so add
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[8],header=None)[1][7]*lb_to_kg)
# no P values

# Los Coyotes- San Gabriel
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[9],header=None)[1][9]*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[9],header=None)[1][16]*lb_to_kg)

# Whittier Narrows-San Gabriel
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[10],header=None)[1][7]*lb_to_kg)
dip_val[-1] = dip_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[10],header=None)[1][15]*lb_to_kg)

# Long Beach - San Gabriel
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[11],header=None)[1][8]*lb_to_kg)
# no P values

# Tapia- Malibu Creek
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[12],header=None)[1][8]*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[12],header=None)[1][11]*lb_to_kg)

# Padre Dam-San Diego River
din_val.append((pd.read_excel(xl_path,sheet_name=xls.sheet_names[13],header=None)[1][7]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[13],header=None)[1][9]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[13],header=None)[1][10]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[13],header=None)[1][12])*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[13],header=None)[1][8]*lb_to_kg)

# Calleguas Creek
# Simi valley- Calleugas Creek
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[14],header=None)[1][9]*lb_to_kg)
# no DIP value

# HillCanyon-Calleguas Creek
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[15],header=None)[1][8]*lb_to_kg)
dip_val.append(np.nan)
# no DIP value

# Santa Clara River
# Ventura WWR-SAnta Clara River E
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[16],header=None)[1][18]*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[16],header=None)[1][8]*lb_to_kg)

# Saugus- Santa Clara r
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[17],header=None)[1][8]*lb_to_kg)
# no DIP values

# Ojai-VEntura River
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[18],header=None)[1][8]*lb_to_kg)
dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[18],header=None)[1][12]*lb_to_kg)

# Camarillo-Conejo - Conejo Creek feeds into Calleguas Creek
din_val[-3] = din_val[-3]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[19],header=None)[1][7]*lb_to_kg)
# no DIP value

# Lompoc WWT- Santa Inez (Santa Ynez) discharges above Point Conception
#din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[20],header=None)[1][8]*lb_to_kg)
#dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[20],header=None)[1][11]*lb_to_kg)

din_val = np.array(din_val)
dip_val = np.array(dip_val)
dip_val[np.isnan(dip_val)] = 0

r_names = ['Escondido Creek','San Diego Creek','LA River','San Gabriel River','Malibu Creek','San Diego River','Calleguas Creek','Santa Clara River','Ventura River']

# load river data
s_to_d = 86400
d_to_mo = 30
mmol_to_mol = 1./1000
g_to_kg = 1./1000
g_N = 14

#r10 = Dataset('../river_data/south_coast_rivers_10_years_monthly_new.nc','r')
r10 = Dataset('../river_data/south_coast_rivers_updated_14_years_1997_2010_monthly.nc','r')
r24 = Dataset('../river_data/south_coast_rivers_24_years_monthly_new.nc','r')

river_names_10 = pickle.load(open('../river_data/river_names_10.pkl','rb'))
river_names_24 = pickle.load(open('../river_data/river_names_24.pkl','rb'))

flo10 = np.array(r10.variables['flow'])
tn10 = np.array(r10.variables['total_nitrogen'])
tp10 = np.array(r10.variables['total_phosphorus'])
nh4_10 = np.array(r10.variables['ammonium']) # mmol/m3
no3_10 = np.array(r10.variables['nitrate']) # mmol/m3
po4_10 = np.array(r10.variables['phosphate']) # mmol/m3

flo10[flo10>1E20] = np.nan
tn10[tn10>1E20] = np.nan
tp10[tp10>1E20] = np.nan
nh4_10[nh4_10>1E20] = np.nan
no3_10[no3_10>1E20] = np.nan
po4_10[po4_10>1E20] = np.nan

din_10 = nh4_10+no3_10
dip_10 = po4_10


r_minor_st_in = 84 # index for start of 1997
r_minor_en_in = 251 # index for end of 2010

flo24 = np.array(r24.variables['flow'][r_minor_st_in:r_minor_en_in+1])
tn24 = np.array(r24.variables['total_nitrogen'][r_minor_st_in:r_minor_en_in+1])
tp24 = np.array(r24.variables['total_phosphorus'][r_minor_st_in:r_minor_en_in+1])
nh4_24 = np.array(r24.variables['ammonium'][r_minor_st_in:r_minor_en_in+1]) # mmol/m3
no3_24 = np.array(r24.variables['nitrate'][r_minor_st_in:r_minor_en_in+1]) # mmol/m3
po4_24 = np.array(r24.variables['phosphate'][r_minor_st_in:r_minor_en_in+1]) # mmol/m3

flo24[flo24>1E20] = np.nan
tn24[tn24>1E20] = np.nan
tp24[tp24>1E20] = np.nan
nh4_24[nh4_24>1E20] = np.nan
no3_24[no3_24>1E20] = np.nan
po4_24[po4_24>1E20] = np.nan

din_24 = nh4_24+no3_24
dip_24 = po4_24

ry0 = 14
ry1 = 14

#multiply by flow, kg/month
tn_10 = tn10*flo10*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
tn_24 = tn24*flo24*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

tp_10 = tp10*flo10*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol
tp_24 = tp24*flo24*s_to_d*d_to_mo*g_N*g_to_kg*mmol_to_mol

# kg/year
tn_data = np.array((np.nansum(np.nanmean(tn_10[:,41,41].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,29,29].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,6,6].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,37,37].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_24[:,12,12].reshape(ry1,12),axis=0)),np.nansum(np.nanmean(tn_10[:,3,3].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,36,36].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,20,20].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tn_10[:,30,30].reshape(ry0,12),axis=0))))

tp_data = np.array((np.nansum(np.nanmean(tp_10[:,41,41].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,29,29].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,6,6].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,37,37].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_24[:,12,12].reshape(ry1,12),axis=0)),np.nansum(np.nanmean(tp_10[:,3,3].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,36,36].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,20,20].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(tp_10[:,30,30].reshape(ry0,12),axis=0))))

din_data = np.array((np.nansum(np.nanmean(din_10[:,41,41].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,29,29].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,6,6].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,37,37].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_24[:,12,12].reshape(ry1,12),axis=0)),np.nansum(np.nanmean(din_10[:,3,3].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,36,36].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,20,20].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(din_10[:,30,30].reshape(ry0,12),axis=0))))

dip_data = np.array((np.nansum(np.nanmean(dip_10[:,41,41].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,29,29].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,6,6].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,37,37].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_24[:,12,12].reshape(ry1,12),axis=0)),np.nansum(np.nanmean(dip_10[:,3,3].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,36,36].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,20,20].reshape(ry0,12),axis=0)),np.nansum(np.nanmean(dip_10[:,30,30].reshape(ry0,12),axis=0))))

diff_tn = tn_data-tnn_val
diff_tp = tp_data-tpp_val

diff_din = din_data-din_val
diff_dip = dip_data-dip_val

# some values of inland POTW data larger than river data, 
# so make it 95% of TN/TP according to Martha
tn_val_new = np.array((tn_data[0]*.95,tn_data[1]*.95,tn_data[2]*.95,tn_data[3]*.95,tn_data[4]*.95,tnn_val[5],tn_data[6]*.95,tn_data[7]*.95,tn_data[8]*.95))
tp_val_new = np.array((tp_data[0]*.95,tp_data[1]*.95,tpp_val[2],tpp_val[3],tp_data[4]*.95,tpp_val[5],tp_data[6]*.95,tp_data[7]*.95,tp_data[8]*.95))

diff_tn_new = tn_data-tn_val_new
diff_tp_new = tp_data-tp_val_new

din_val_new = np.array((din_data[0]*.95,din_data[1]*.95,din_data[2]*.95,din_data[3]*.95,din_data[4]*.95,din_val[5],din_data[6]*.95,din_data[7]*.95,din_data[8]*.95))
dip_val_new = np.array((dip_val[0],dip_data[1]*.95,dip_val[2],dip_data[3]*.95,dip_data[4]*.95,dip_data[5]*.95,dip_val[6],dip_data[7]*.95,dip_data[8]*.95))

diff_din_new = din_data-din_val_new
diff_dip_new = dip_data-dip_val_new

# separate into regions
# will use numbers in excel for SI table 6 and 7, 
# but use numbers calculated here for Figure 3
# order values by region ssd,nsd,occ,spp,smm,ven, sbb, scb
r_names = ['Escondido Creek','San Diego Creek','LA River','San Gabriel River','Malibu Creek','San Diego River','Calleguas Creek','Santa Clara River','Ventura River']
tnn_val_region = np.array((tnn_val[5],tnn_val[0],tnn_val[1],tnn_val[2]+tnn_val[3],tnn_val[4],tnn_val[6]+tnn_val[7]+tnn_val[8],np.nan,np.sum(tnn_val)))
tpp_val_region = np.array((tpp_val[5],tpp_val[0],tpp_val[1],tpp_val[2]+tpp_val[3],tpp_val[4],tpp_val[6]+tpp_val[7]+tpp_val[8],np.nan,np.sum(tpp_val)))
din_val_region = np.array((din_val[5],din_val[0],din_val[1],din_val[2]+din_val[3],din_val[4],din_val[6]+din_val[7]+din_val[8],np.nan,np.sum(din_val)))
dip_val_region = np.array((dip_val[5],dip_val[0],dip_val[1],dip_val[2]+dip_val[3],dip_val[4],dip_val[6]+dip_val[7]+dip_val[8],np.nan,np.sum(dip_val)))
# Santa Barbara has no inland POTW

np.save('inland_potw_tnn_region.npy',tnn_val_region)
np.save('inland_potw_tpp_region.npy',tpp_val_region)
np.save('inland_potw_din_region.npy',din_val_region)
np.save('inland_potw_dip_region.npy',dip_val_region)

tn_val_new_region = np.array((tn_val_new[5],tn_val_new[0],tn_val_new[1],tn_val_new[2]+tn_val_new[3],tn_val_new[4]+din_val_new[4],tn_val_new[6]+tn_val_new[7]+tn_val_new[8],np.nan,np.sum(tn_val_new)+din_val_new[4]))
tp_val_new_region = np.array((tp_val_new[5],tp_val_new[0],tp_val_new[1],tp_val_new[2]+tp_val_new[3],tp_val_new[4],tp_val_new[6]+tp_val_new[7]+tp_val_new[8],np.nan,np.sum(tp_val_new)))
din_val_new_region = np.array((din_val_new[5],din_val_new[0],din_val_new[1],din_val_new[2]+din_val_new[3],din_val_new[4],din_val_new[6]+din_val_new[7]+din_val_new[8],np.nan,np.sum(din_val_new)))
dip_val_new_region = np.array((dip_val_new[5],dip_val_new[0],dip_val_new[1],dip_val_new[2]+dip_val_new[3],dip_val_new[4],dip_val_new[6]+dip_val_new[7]+dip_val_new[8],np.nan,np.sum(dip_val_new)))
