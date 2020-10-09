# combine 1997-2010 dataset with 2007-2017
# to get full 1997-2017 dataset
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime
import pandas as pd
import glob as glob

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/major_potw_data_newocsd.nc'
maj_newp = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_combine_1997_2017/'

majfi = sorted(glob.glob(maj_newp+'*xlsx'))

htp_up = pd.read_excel(majfi[0],sheet_name='formatted',header=None)
jwp_up = pd.read_excel(majfi[1],sheet_name='formatted',header=None)
ocs_up = pd.read_excel(majfi[2],sheet_name='formatted',header=None,skiprows=2)
plw_up = pd.read_excel(majfi[3],sheet_name='formatted',header=None)

htp_dt = np.array(pd.to_datetime(htp_up[0][1:]))
jwp_dt = np.array(pd.to_datetime(jwp_up[0][1:]))
ocs_dt = np.array(pd.to_datetime(ocs_up[0][1:]))
plw_dt = np.array(pd.to_datetime(plw_up[0][1:]))

htp_flo = np.array(htp_up[15][1:].astype(float))
jwp_flo = np.array(jwp_up[1][1:].astype(float))
ocs_flo = np.array(ocs_up[1][1:].astype(float))
plw_flo = np.array(plw_up[10][1:].astype(float))

htp_nh4 = np.array(htp_up[9][1:].astype(float))
jwp_nh4 = np.array(jwp_up[2][1:].astype(float))
ocs_nh4 = np.array(ocs_up[17][1:].astype(float))
plw_nh4 = np.array(plw_up[3][1:].astype(float))

htp_no3 = np.array(htp_up[6][1:].astype(float))
jwp_no3 = np.array(jwp_up[19][1:].astype(float))
ocs_no3 = np.array(ocs_up[18][1:].astype(float))
plw_no3 = np.array(plw_up[5][1:].astype(float))

htp_no2 = np.array(htp_up[5][1:].astype(float))
jwp_no2 = np.array(jwp_up[6][1:].astype(float))

htp_din = np.nansum((htp_nh4,htp_no3,htp_no2),axis=0)
jwp_din = np.nansum((jwp_nh4,jwp_no3,jwp_no2),axis=0)
ocs_din = np.nansum((ocs_nh4,ocs_no3),axis=0)
plw_din = np.nansum((plw_nh4,plw_no3),axis=0)

htp_din[htp_din==0] = np.nan
jwp_din[jwp_din==0] = np.nan
ocs_din[ocs_din==0] = np.nan
plw_din[plw_din==0] = np.nan

# pandas dataframe with everything
full_dt = pd.date_range(start='1997-01-01',end='2017-01-01')

###############
# read major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time_dt = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units,only_use_cftime_datetimes=False,only_use_python_datetimes=True)

ind_1997 = 313
ind_2007 = 433 #01-01-2007

major_flo = np.array(major_nc.variables['flow'][ind_1997:ind_2007]) # m3/s
major_nh4 = np.array(major_nc.variables['NH4'][ind_1997:ind_2007]) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3'][ind_1997:ind_2007]) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2'][ind_1997:ind_2007]) # mmol/m3
major_onn = np.array(major_nc.variables['ON'][ind_1997:ind_2007]) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4'][ind_1997:ind_2007]) # mmol/m3
major_bod = np.array(major_nc.variables['BOD'][ind_1997:ind_2007]) # mmol/m3
major_opp = np.array(major_nc.variables['OP'][ind_1997:ind_2007]) # mmol/m3
major_fee  = np.array(major_nc.variables['Fe'][ind_1997:ind_2007])  # mmol/m3
major_phh  = np.array(major_nc.variables['pH'][ind_1997:ind_2007]) 
major_alk = np.array(major_nc.variables['alkalinity'][ind_1997:ind_2007]) 
major_toc = np.array(major_nc.variables['TOC'][ind_1997:ind_2007]) 
major_doo = np.array(major_nc.variables['dissolved_oxygen'][ind_1997:ind_2007]) 
major_tem = np.array(major_nc.variables['temperature'][ind_1997:ind_2007]) 
major_sal = np.array(major_nc.variables['salinity'][ind_1997:ind_2007]) 
lat_nc = np.array(major_nc.variables['latitude']) 
lon_nc = np.array(major_nc.variables['longitude']) 

major_nh4[major_nh4>1E20][ind_1997:ind_2007] = np.nan 
major_no3[major_no3>1E20][ind_1997:ind_2007] = np.nan 
major_no2[major_no2>1E20][ind_1997:ind_2007] = np.nan 
major_onn[major_onn>1E20][ind_1997:ind_2007] = np.nan 
major_opp[major_opp>1E20][ind_1997:ind_2007] = np.nan 

major_tnn = np.nansum((major_nh4,major_no3,major_no2,major_onn),axis=0)
major_tpp = major_po4+major_opp

major_tnn[major_tnn>1E20] = np.nan
major_tpp[major_tpp>1E20] = np.nan
major_toc[major_toc>1E20] = np.nan
major_po4[major_po4>1E20] = np.nan

df_old = pd.DataFrame({'date':major_time_dt[ind_1997:ind_2007],
'htp flo m3/s':major_flo[:,0,0],
'jwp flo m3/s':major_flo[:,1,1],
'ocs flo m3/s':major_flo[:,2,2],
'plw flo m3/s':major_flo[:,3,3],
'htp nh4 mmol/m3':major_nh4[:,0,0],
'jwp nh4 mmol/m3':major_nh4[:,1,1],
'ocs nh4 mmol/m3':major_nh4[:,2,2],
'plw nh4 mmol/m3':major_nh4[:,3,3],
'htp no3 mmol/m3':major_no3[:,0,0],
'jwp no3 mmol/m3':major_no3[:,1,1],
'ocs no3 mmol/m3':major_no3[:,2,2],
'plw no3 mmol/m3':major_no3[:,3,3],
'htp no2 mmol/m3':major_no2[:,0,0],
'jwp no2 mmol/m3':major_no2[:,1,1],
'ocs no2 mmol/m3':major_no2[:,2,2],
'plw no2 mmol/m3':major_no2[:,3,3],
'htp onn mmol/m3':major_onn[:,0,0],
'jwp onn mmol/m3':major_onn[:,1,1],
'ocs onn mmol/m3':major_onn[:,2,2],
'plw onn mmol/m3':major_onn[:,3,3],
'htp opp mmol/m3':major_opp[:,0,0],
'jwp opp mmol/m3':major_opp[:,1,1],
'ocs opp mmol/m3':major_opp[:,2,2],
'plw opp mmol/m3':major_opp[:,3,3],
'htp po4 mmol/m3':major_po4[:,0,0],
'jwp po4 mmol/m3':major_po4[:,1,1],
'ocs po4 mmol/m3':major_po4[:,2,2],
'plw po4 mmol/m3':major_po4[:,3,3],
'htp bod mmol/m3':major_bod[:,0,0],
'jwp bod mmol/m3':major_bod[:,1,1],
'ocs bod mmol/m3':major_bod[:,2,2],
'plw bod mmol/m3':major_bod[:,3,3],
'htp fee mmol/m3':major_fee[:,0,0],
'jwp fee mmol/m3':major_fee[:,1,1],
'ocs fee mmol/m3':major_fee[:,2,2],
'plw fee mmol/m3':major_fee[:,3,3],
'htp phh mmol/m3':major_phh[:,0,0],
'jwp phh mmol/m3':major_phh[:,1,1],
'ocs phh mmol/m3':major_phh[:,2,2],
'plw phh mmol/m3':major_phh[:,3,3],
'htp alk mmol/m3':major_alk[:,0,0],
'jwp alk mmol/m3':major_alk[:,1,1],
'ocs alk mmol/m3':major_alk[:,2,2],
'plw alk mmol/m3':major_alk[:,3,3],
'htp toc mmol/m3':major_toc[:,0,0],
'jwp toc mmol/m3':major_toc[:,1,1],
'ocs toc mmol/m3':major_toc[:,2,2],
'plw toc mmol/m3':major_toc[:,3,3],
'htp doo mmol/m3':major_doo[:,0,0],
'jwp doo mmol/m3':major_doo[:,1,1],
'ocs doo mmol/m3':major_doo[:,2,2],
'plw doo mmol/m3':major_doo[:,3,3],
'htp tpp mmol/m3':major_tpp[:,0,0],
'jwp tpp mmol/m3':major_tpp[:,1,1],
'ocs tpp mmol/m3':major_tpp[:,2,2],
'plw tpp mmol/m3':major_tpp[:,3,3],
'htp tnn mmol/m3':major_tnn[:,0,0],
'jwp tnn mmol/m3':major_tnn[:,1,1],
'ocs tnn mmol/m3':major_tnn[:,2,2],
'plw tnn mmol/m3':major_tnn[:,3,3],
'htp tem mmol/m3':major_tem[:,0,0],
'jwp tem mmol/m3':major_tem[:,1,1],
'ocs tem mmol/m3':major_tem[:,2,2],
'plw tem mmol/m3':major_tem[:,3,3],
'htp sal mmol/m3':major_sal[:,0,0],
'jwp sal mmol/m3':major_sal[:,1,1],
'ocs sal mmol/m3':major_sal[:,2,2],
'plw sal mmol/m3':major_sal[:,3,3]})


df_old.set_index(df_old['date'],inplace=True)
df_old.loc[pd.to_datetime('1997-01-01')] = df_old.loc['1997-01-31']
df_old.resample('D').bfill()


kg_to_g = 1000
g_to_mol = 1./14
mol_to_mmol = 1000
mgL_to_mmolm3 = 1000./14

# conversion
convn = 14./1000 # mmol/m3 to mg/L
convp = 30.97/1000 # mmol/m3 to kg/L
convnf = (14.*86400)/1E6 # mmol/s to kg/d
convpf = (30.97*86400)/1E6 # mmol/s to kg/d
convv = 1./0.043812645072430365 # m3/s to mgd
conva = 3.78541178 # million gal/day * mg/L to kg/d

