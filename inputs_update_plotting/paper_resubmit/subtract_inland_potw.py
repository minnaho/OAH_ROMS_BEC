import numpy as np
import pandas as pd
from netCDF4 import Dataset
import pickle

xl_path = '../../potw_outfall_data/Inland POTW data.xlsx'

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
tpp_val[3] = pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][14]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][15]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][16]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][17]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][18]

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
# dip value as 90% of TP
dip_val.append((pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][9]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][10]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][11]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][12])*.9)

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
#dip_val[-1] = dip_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[9],header=None)[1][16]*lb_to_kg)

# Whittier Narrows-San Gabriel
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[10],header=None)[1][7]*lb_to_kg)
#dip_val[-1] = dip_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[10],header=None)[1][15]*lb_to_kg)

# Long Beach - San Gabriel
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[11],header=None)[1][8]*lb_to_kg)
# no P values
# San Gabriel DIP value as 90% of TP
dip_val.append((pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][14]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][15]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][16]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][17]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][18])*.9)
   
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
#dip_val.append(np.nan)
# no DIP value

# Calleguas river DIP as 90%
dip_val.append((pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][22]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][23]+pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][24])*.9)

# Santa Clara River
# Ventura WWR-SAnta Clara River E
din_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[16],header=None)[1][18]*lb_to_kg)
#dip_val.append(pd.read_excel(xl_path,sheet_name=xls.sheet_names[16],header=None)[1][8]*lb_to_kg)

# Saugus- Santa Clara r
din_val[-1] = din_val[-1]+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[17],header=None)[1][8]*lb_to_kg)
# no DIP values
# Santa Clara R set as 90% of DIP
dip_val.append((pd.read_excel(xl_path,sheet_name=xls.sheet_names[16],header=None)[1][8]*lb_to_kg)+(pd.read_excel(xl_path,sheet_name=xls.sheet_names[0],header=None)[4][26]*.9))

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

'''
tn_val_new_region = np.array((tn_val_new[5],tn_val_new[0],tn_val_new[1],tn_val_new[2]+tn_val_new[3],tn_val_new[4]+din_val_new[4],tn_val_new[6]+tn_val_new[7]+tn_val_new[8],np.nan,np.sum(tn_val_new)+din_val_new[4]))
tp_val_new_region = np.array((tp_val_new[5],tp_val_new[0],tp_val_new[1],tp_val_new[2]+tp_val_new[3],tp_val_new[4],tp_val_new[6]+tp_val_new[7]+tp_val_new[8],np.nan,np.sum(tp_val_new)))
din_val_new_region = np.array((din_val_new[5],din_val_new[0],din_val_new[1],din_val_new[2]+din_val_new[3],din_val_new[4],din_val_new[6]+din_val_new[7]+din_val_new[8],np.nan,np.sum(din_val_new)))
dip_val_new_region = np.array((dip_val_new[5],dip_val_new[0],dip_val_new[1],dip_val_new[2]+dip_val_new[3],dip_val_new[4],dip_val_new[6]+dip_val_new[7]+dip_val_new[8],np.nan,np.sum(dip_val_new)))
'''
