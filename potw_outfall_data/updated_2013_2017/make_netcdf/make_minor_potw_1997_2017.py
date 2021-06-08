###############################
# take 2007-2017 minor potw monthly data
# and turn to netcdf
# for psource model input
##############################
import numpy as np
from netCDF4 import Dataset,date2num
import pandas as pd
import glob
import datetime as datetime

# path to files
fol = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/formatted/'
fnames = sorted(glob.glob(fol+'*'))

# get potw minor names
# order of potw minors in netcdf will be alphabetical
rnames = []
for f_i in fnames:
    rnames.append(f_i[85:f_i.index('.xl')])

example = pd.read_excel(fnames[0],sheet_name='reordered',header=None,skiprows=1)
#example[0][0] = '01/01/2007' # set first time to 01/01/2007
example[0] = pd.to_datetime(example[0]) # make dates index to resample to daily
example.set_index(0,inplace=True)
example.loc[pd.to_datetime('1997-01-01')] = example.loc['2000-01-31']
daily_ex = example.resample('D').bfill()

df = daily_ex.loc['1997':'2017']

# make arrays
tim_arr = np.arange(0,df.shape[0])

lat_arr = np.empty((len(fnames)))
lon_arr = np.empty((len(fnames)))
flo_arr = np.empty((df.shape[0],len(fnames)))
nh4_arr = np.empty((df.shape[0],len(fnames)))
no3_arr = np.empty((df.shape[0],len(fnames)))
doo_arr = np.empty((df.shape[0],len(fnames)))
tem_arr = np.empty((df.shape[0],len(fnames)))
bod_arr = np.empty((df.shape[0],len(fnames)))
phh_arr = np.empty((df.shape[0],len(fnames)))
tpp_arr = np.empty((df.shape[0],len(fnames)))
po4_arr = np.empty((df.shape[0],len(fnames)))
opp_arr = np.empty((df.shape[0],len(fnames)))
toc_arr = np.empty((df.shape[0],len(fnames)))
onn_arr = np.empty((df.shape[0],len(fnames)))
tfe_arr = np.empty((df.shape[0],len(fnames)))
sil_arr = np.empty((df.shape[0],len(fnames)))
alk_arr = np.empty((df.shape[0],len(fnames)))
sal_arr = np.empty((df.shape[0],len(fnames)))
dfe_arr = np.empty((df.shape[0],len(fnames)))

mgd_to_m3s = 0.043812645072430365

# mg/L to mmol/m3
mg_l_n = 1000./14
mg_l_p = 1000./30.97
mg_l_o = 1000./16
mg_l_c = 1000./12
mg_l_f = 1000./55.845
mg_l_s = 1000./28.0855

# Hale and Oceanside - extend 2007 back to 2001 and use 2000 for 1997-2000
# SBR - extend 2007 back to 2002 (plant came online in 2002)
exceptions = ['HaleAveResource','OceansideOceanOutfall','SouthBayReclamation']

# loop through files
for f_i in range(len(fnames)):
    # read file
    dat_fi = pd.read_excel(fnames[f_i],sheet_name='reordered',header=None,skiprows=1)
    # make monthly into daily data
    dat_fi[0] = pd.to_datetime(dat_fi[0]) # make dates index to resample to daily
    dat_fi.set_index(0,inplace=True)
    # extend dataset back to 1997
#    try:
#    dat_fi.loc[pd.to_datetime('1997-01-31')] = dat_fi.loc['2000-01-31']
#    dat_fi.loc[pd.to_datetime('1997-02-28')] = dat_fi.loc['2000-02-29']
#    dat_fi.loc[pd.to_datetime('1997-03-31')] = dat_fi.loc['2000-03-31']
#    dat_fi.loc[pd.to_datetime('1997-04-30')] = dat_fi.loc['2000-04-30']
#    dat_fi.loc[pd.to_datetime('1997-05-31')] = dat_fi.loc['2000-05-31']
#    dat_fi.loc[pd.to_datetime('1997-06-30')] = dat_fi.loc['2000-06-30']
#    dat_fi.loc[pd.to_datetime('1997-07-31')] = dat_fi.loc['2000-07-31']
#    dat_fi.loc[pd.to_datetime('1997-08-31')] = dat_fi.loc['2000-08-31']
#    dat_fi.loc[pd.to_datetime('1997-09-30')] = dat_fi.loc['2000-09-30']
#    dat_fi.loc[pd.to_datetime('1997-10-31')] = dat_fi.loc['2000-10-31']
#    dat_fi.loc[pd.to_datetime('1997-11-30')] = dat_fi.loc['2000-11-30']
#    dat_fi.loc[pd.to_datetime('1997-12-31')] = dat_fi.loc['2000-12-31']
# 
#    dat_fi.loc[pd.to_datetime('1998-01-31')] = dat_fi.loc['2000-01-31']
#    dat_fi.loc[pd.to_datetime('1998-02-28')] = dat_fi.loc['2000-02-29']
#    dat_fi.loc[pd.to_datetime('1998-03-31')] = dat_fi.loc['2000-03-31']
#    dat_fi.loc[pd.to_datetime('1998-04-30')] = dat_fi.loc['2000-04-30']
#    dat_fi.loc[pd.to_datetime('1998-05-31')] = dat_fi.loc['2000-05-31']
#    dat_fi.loc[pd.to_datetime('1998-06-30')] = dat_fi.loc['2000-06-30']
#    dat_fi.loc[pd.to_datetime('1998-07-31')] = dat_fi.loc['2000-07-31']
#    dat_fi.loc[pd.to_datetime('1998-08-31')] = dat_fi.loc['2000-08-31']
#    dat_fi.loc[pd.to_datetime('1998-09-30')] = dat_fi.loc['2000-09-30']
#    dat_fi.loc[pd.to_datetime('1998-10-31')] = dat_fi.loc['2000-10-31']
#    dat_fi.loc[pd.to_datetime('1998-11-30')] = dat_fi.loc['2000-11-30']
#    dat_fi.loc[pd.to_datetime('1998-12-31')] = dat_fi.loc['2000-12-31']
# 
#    dat_fi.loc[pd.to_datetime('1999-01-31')] = dat_fi.loc['2000-01-31']
#    dat_fi.loc[pd.to_datetime('1999-02-28')] = dat_fi.loc['2000-02-29']
#    dat_fi.loc[pd.to_datetime('1999-03-31')] = dat_fi.loc['2000-03-31']
#    dat_fi.loc[pd.to_datetime('1999-04-30')] = dat_fi.loc['2000-04-30']
#    dat_fi.loc[pd.to_datetime('1999-05-31')] = dat_fi.loc['2000-05-31']
#    dat_fi.loc[pd.to_datetime('1999-06-30')] = dat_fi.loc['2000-06-30']
#    dat_fi.loc[pd.to_datetime('1999-07-31')] = dat_fi.loc['2000-07-31']
#    dat_fi.loc[pd.to_datetime('1999-08-31')] = dat_fi.loc['2000-08-31']
#    dat_fi.loc[pd.to_datetime('1999-09-30')] = dat_fi.loc['2000-09-30']
#    dat_fi.loc[pd.to_datetime('1999-10-31')] = dat_fi.loc['2000-10-31']
#    dat_fi.loc[pd.to_datetime('1999-11-30')] = dat_fi.loc['2000-11-30']
#    dat_fi.loc[pd.to_datetime('1999-12-31')] = dat_fi.loc['2000-12-31']
# 
#    dat_fi.loc[pd.to_datetime('1997-01-01')] = dat_fi.loc['2000-01-31']
#    except:
    dat_fi.loc[pd.to_datetime('1997-01-01')] = np.nan

    dat_fi.loc[pd.to_datetime('1997-01-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-02-28')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-03-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-04-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-05-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-06-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-07-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-08-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-09-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-10-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-11-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1997-12-31')] = np.nan

    dat_fi.loc[pd.to_datetime('1998-01-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-02-28')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-03-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-04-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-05-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-06-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-07-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-08-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-09-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-10-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-11-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1998-12-31')] = np.nan

    dat_fi.loc[pd.to_datetime('1999-01-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-02-28')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-03-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-04-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-05-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-06-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-07-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-08-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-09-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-10-31')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-11-30')] = np.nan
    dat_fi.loc[pd.to_datetime('1999-12-31')] = np.nan

    dat_fi.loc['1997-01-01'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1997-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1997-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1997-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1997-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1997-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1997-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1997-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1997-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1997-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1997-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1997-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1997-12-31'] = dat_fi.loc['2000-12-31']

    dat_fi.loc['1998-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1998-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1998-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1998-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1998-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1998-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1998-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1998-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1998-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1998-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1998-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1998-12-31'] = dat_fi.loc['2000-12-31']

    dat_fi.loc['1999-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1999-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1999-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1999-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1999-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1999-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1999-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1999-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1999-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1999-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1999-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1999-12-31'] = dat_fi.loc['2000-12-31']

    if fnames[f_i] not in exceptions:
        # linearly interpolate by month
        int01 = np.linspace(dat_fi.loc['2000-01-31'].astype(float),dat_fi.loc['2007-01-31'].astype(float),6)[0][0]
        int02 = np.linspace(dat_fi.loc['2000-02-29'].astype(float),dat_fi.loc['2007-02-28'].astype(float),6)[0][0]
        int03 = np.linspace(dat_fi.loc['2000-03-31'].astype(float),dat_fi.loc['2007-03-31'].astype(float),6)[0][0]
        int04 = np.linspace(dat_fi.loc['2000-04-30'].astype(float),dat_fi.loc['2007-04-30'].astype(float),6)[0][0]
        int05 = np.linspace(dat_fi.loc['2000-05-31'].astype(float),dat_fi.loc['2007-05-31'].astype(float),6)[0][0]
        int06 = np.linspace(dat_fi.loc['2000-06-30'].astype(float),dat_fi.loc['2007-06-30'].astype(float),6)[0][0]
        int07 = np.linspace(dat_fi.loc['2000-07-31'].astype(float),dat_fi.loc['2007-07-31'].astype(float),6)[0][0]
        int08 = np.linspace(dat_fi.loc['2000-08-31'].astype(float),dat_fi.loc['2007-08-31'].astype(float),6)[0][0]
        int09 = np.linspace(dat_fi.loc['2000-09-30'].astype(float),dat_fi.loc['2007-09-30'].astype(float),6)[0][0]
        int10 = np.linspace(dat_fi.loc['2000-10-31'].astype(float),dat_fi.loc['2007-10-31'].astype(float),6)[0][0]
        int11 = np.linspace(dat_fi.loc['2000-11-30'].astype(float),dat_fi.loc['2007-11-30'].astype(float),6)[0][0]
        int12 = np.linspace(dat_fi.loc['2000-12-31'].astype(float),dat_fi.loc['2007-12-31'].astype(float),6)[0][0]

        dat_fi.loc['2001-01-31'] = int01[0]
        dat_fi.loc['2002-01-31'] = int01[1]
        dat_fi.loc['2003-01-31'] = int01[2]
        dat_fi.loc['2004-01-31'] = int01[3]
        dat_fi.loc['2005-01-31'] = int01[4]
        dat_fi.loc['2006-01-31'] = int01[5]

        dat_fi.loc['2001-02-28'] = int02[0]
        dat_fi.loc['2002-02-28'] = int02[1]
        dat_fi.loc['2003-02-28'] = int02[2]
        dat_fi.loc['2004-02-28'] = int02[3]
        dat_fi.loc['2005-02-28'] = int02[4]
        dat_fi.loc['2006-02-28'] = int02[5]

        dat_fi.loc['2001-03-31'] = int03[0]
        dat_fi.loc['2002-03-31'] = int03[1]
        dat_fi.loc['2003-03-31'] = int03[2]
        dat_fi.loc['2004-03-31'] = int03[3]
        dat_fi.loc['2005-03-31'] = int03[4]
        dat_fi.loc['2006-03-31'] = int03[5]

        dat_fi.loc['2001-04-30'] = int04[0]
        dat_fi.loc['2002-04-30'] = int04[1]
        dat_fi.loc['2003-04-30'] = int04[2]
        dat_fi.loc['2004-04-30'] = int04[3]
        dat_fi.loc['2005-04-30'] = int04[4]
        dat_fi.loc['2006-04-30'] = int04[5]

        dat_fi.loc['2001-05-31'] = int05[0]
        dat_fi.loc['2002-05-31'] = int05[1]
        dat_fi.loc['2003-05-31'] = int05[2]
        dat_fi.loc['2004-05-31'] = int05[3]
        dat_fi.loc['2005-05-31'] = int05[4]
        dat_fi.loc['2006-05-31'] = int05[5]

        dat_fi.loc['2001-06-30'] = int06[0]
        dat_fi.loc['2002-06-30'] = int06[1]
        dat_fi.loc['2003-06-30'] = int06[2]
        dat_fi.loc['2004-06-30'] = int06[3]
        dat_fi.loc['2005-06-30'] = int06[4]
        dat_fi.loc['2006-06-30'] = int06[5]

        dat_fi.loc['2001-07-31'] = int07[0]
        dat_fi.loc['2002-07-31'] = int07[1]
        dat_fi.loc['2003-07-31'] = int07[2]
        dat_fi.loc['2004-07-31'] = int07[3]
        dat_fi.loc['2005-07-31'] = int07[4]
        dat_fi.loc['2006-07-31'] = int07[5]

        dat_fi.loc['2001-08-31'] = int08[0]
        dat_fi.loc['2002-08-31'] = int08[1]
        dat_fi.loc['2003-08-31'] = int08[2]
        dat_fi.loc['2004-08-31'] = int08[3]
        dat_fi.loc['2005-08-31'] = int08[4]
        dat_fi.loc['2006-08-31'] = int08[5]

        dat_fi.loc['2001-09-30'] = int09[0]
        dat_fi.loc['2002-09-30'] = int09[1]
        dat_fi.loc['2003-09-30'] = int09[2]
        dat_fi.loc['2004-09-30'] = int09[3]
        dat_fi.loc['2005-09-30'] = int09[4]
        dat_fi.loc['2006-09-30'] = int09[5]

        dat_fi.loc['2001-10-31'] = int10[0]
        dat_fi.loc['2002-10-31'] = int10[1]
        dat_fi.loc['2003-10-31'] = int10[2]
        dat_fi.loc['2004-10-31'] = int10[3]
        dat_fi.loc['2005-10-31'] = int10[4]
        dat_fi.loc['2006-10-31'] = int10[5]

        dat_fi.loc['2001-11-30'] = int11[0]
        dat_fi.loc['2002-11-30'] = int11[1]
        dat_fi.loc['2003-11-30'] = int11[2]
        dat_fi.loc['2004-11-30'] = int11[3]
        dat_fi.loc['2005-11-30'] = int11[4]
        dat_fi.loc['2006-11-30'] = int11[5]

        dat_fi.loc['2001-12-31'] = int12[0]
        dat_fi.loc['2002-12-31'] = int12[1]
        dat_fi.loc['2003-12-31'] = int12[2]
        dat_fi.loc['2004-12-31'] = int12[3]
        dat_fi.loc['2005-12-31'] = int12[4]
        dat_fi.loc['2006-12-31'] = int12[5]

    # special cases 
    if fnames[f_i] in exceptions:
        if fnames[f_i] == 'HaleAveResource' or fnames[f_i] == 'OceansideOceanOutfall':
            for y_i in range(2001,2007):
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']
                dat_fi.loc[str(y_i)+'-02-28'] = dat_fi.loc['2007-02-28']
                dat_fi.loc[str(y_i)+'-03-31'] = dat_fi.loc['2007-03-31']
                dat_fi.loc[str(y_i)+'-04-30'] = dat_fi.loc['2007-04-30']
                dat_fi.loc[str(y_i)+'-05-31'] = dat_fi.loc['2007-05-31']
                dat_fi.loc[str(y_i)+'-06-30'] = dat_fi.loc['2007-06-30']
                dat_fi.loc[str(y_i)+'-07-31'] = dat_fi.loc['2007-07-31']
                dat_fi.loc[str(y_i)+'-08-31'] = dat_fi.loc['2007-08-31']
                dat_fi.loc[str(y_i)+'-09-30'] = dat_fi.loc['2007-09-30']
                dat_fi.loc[str(y_i)+'-10-31'] = dat_fi.loc['2007-10-31']
                dat_fi.loc[str(y_i)+'-11-30'] = dat_fi.loc['2007-11-30']
                dat_fi.loc[str(y_i)+'-12-31'] = dat_fi.loc['2007-12-31']
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']

        if fnames[f_i] == 'SouthBayReclamation':
            # set to 0 before 2002 - plant not online
            dat_fi.loc['2001-01-31'] = dat_fi.loc['2000-01-31']
            dat_fi.loc['2001-02-28'] = dat_fi.loc['2000-02-28']
            dat_fi.loc['2001-03-31'] = dat_fi.loc['2000-03-31']
            dat_fi.loc['2001-04-30'] = dat_fi.loc['2000-04-30']
            dat_fi.loc['2001-05-31'] = dat_fi.loc['2000-05-31']
            dat_fi.loc['2001-06-30'] = dat_fi.loc['2000-06-30']
            dat_fi.loc['2001-07-31'] = dat_fi.loc['2000-07-31']
            dat_fi.loc['2001-08-31'] = dat_fi.loc['2000-08-31']
            dat_fi.loc['2001-09-30'] = dat_fi.loc['2000-09-30']
            dat_fi.loc['2001-10-31'] = dat_fi.loc['2000-10-31']
            dat_fi.loc['2001-11-30'] = dat_fi.loc['2000-11-30']
            dat_fi.loc['2001-12-31'] = dat_fi.loc['2000-12-31']
            for y_i in range(2002,2007):
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']
                dat_fi.loc[str(y_i)+'-02-28'] = dat_fi.loc['2007-02-28']
                dat_fi.loc[str(y_i)+'-03-31'] = dat_fi.loc['2007-03-31']
                dat_fi.loc[str(y_i)+'-04-30'] = dat_fi.loc['2007-04-30']
                dat_fi.loc[str(y_i)+'-05-31'] = dat_fi.loc['2007-05-31']
                dat_fi.loc[str(y_i)+'-06-30'] = dat_fi.loc['2007-06-30']
                dat_fi.loc[str(y_i)+'-07-31'] = dat_fi.loc['2007-07-31']
                dat_fi.loc[str(y_i)+'-08-31'] = dat_fi.loc['2007-08-31']
                dat_fi.loc[str(y_i)+'-09-30'] = dat_fi.loc['2007-09-30']
                dat_fi.loc[str(y_i)+'-10-31'] = dat_fi.loc['2007-10-31']
                dat_fi.loc[str(y_i)+'-11-30'] = dat_fi.loc['2007-11-30']
                dat_fi.loc[str(y_i)+'-12-31'] = dat_fi.loc['2007-12-31']
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']
        
    dat_fi = dat_fi.resample('D').interpolate()
    dat_fi = dat_fi.resample('D').bfill()
    dat_fi = dat_fi.resample('D').ffill()

    # have to repeat for some reason
    dat_fi.loc['1997-01-01'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1997-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1997-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1997-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1997-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1997-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1997-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1997-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1997-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1997-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1997-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1997-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1997-12-31'] = dat_fi.loc['2000-12-31']

    dat_fi.loc['1998-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1998-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1998-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1998-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1998-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1998-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1998-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1998-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1998-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1998-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1998-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1998-12-31'] = dat_fi.loc['2000-12-31']

    dat_fi.loc['1999-01-31'] = dat_fi.loc['2000-01-31']
    dat_fi.loc['1999-02-28'] = dat_fi.loc['2000-02-29']
    dat_fi.loc['1999-03-31'] = dat_fi.loc['2000-03-31']
    dat_fi.loc['1999-04-30'] = dat_fi.loc['2000-04-30']
    dat_fi.loc['1999-05-31'] = dat_fi.loc['2000-05-31']
    dat_fi.loc['1999-06-30'] = dat_fi.loc['2000-06-30']
    dat_fi.loc['1999-07-31'] = dat_fi.loc['2000-07-31']
    dat_fi.loc['1999-08-31'] = dat_fi.loc['2000-08-31']
    dat_fi.loc['1999-09-30'] = dat_fi.loc['2000-09-30']
    dat_fi.loc['1999-10-31'] = dat_fi.loc['2000-10-31']
    dat_fi.loc['1999-11-30'] = dat_fi.loc['2000-11-30']
    dat_fi.loc['1999-12-31'] = dat_fi.loc['2000-12-31']
    # have to repeat for some reason
    if fnames[f_i] not in exceptions:
        dat_fi.loc['2001-01-31'] = int01[0]
        dat_fi.loc['2002-01-31'] = int01[1]
        dat_fi.loc['2003-01-31'] = int01[2]
        dat_fi.loc['2004-01-31'] = int01[3]
        dat_fi.loc['2005-01-31'] = int01[4]
        dat_fi.loc['2006-01-31'] = int01[5]

        dat_fi.loc['2001-02-28'] = int02[0]
        dat_fi.loc['2002-02-28'] = int02[1]
        dat_fi.loc['2003-02-28'] = int02[2]
        dat_fi.loc['2004-02-28'] = int02[3]
        dat_fi.loc['2005-02-28'] = int02[4]
        dat_fi.loc['2006-02-28'] = int02[5]

        dat_fi.loc['2001-03-31'] = int03[0]
        dat_fi.loc['2002-03-31'] = int03[1]
        dat_fi.loc['2003-03-31'] = int03[2]
        dat_fi.loc['2004-03-31'] = int03[3]
        dat_fi.loc['2005-03-31'] = int03[4]
        dat_fi.loc['2006-03-31'] = int03[5]

        dat_fi.loc['2001-04-30'] = int04[0]
        dat_fi.loc['2002-04-30'] = int04[1]
        dat_fi.loc['2003-04-30'] = int04[2]
        dat_fi.loc['2004-04-30'] = int04[3]
        dat_fi.loc['2005-04-30'] = int04[4]
        dat_fi.loc['2006-04-30'] = int04[5]

        dat_fi.loc['2001-05-31'] = int05[0]
        dat_fi.loc['2002-05-31'] = int05[1]
        dat_fi.loc['2003-05-31'] = int05[2]
        dat_fi.loc['2004-05-31'] = int05[3]
        dat_fi.loc['2005-05-31'] = int05[4]
        dat_fi.loc['2006-05-31'] = int05[5]

        dat_fi.loc['2001-06-30'] = int06[0]
        dat_fi.loc['2002-06-30'] = int06[1]
        dat_fi.loc['2003-06-30'] = int06[2]
        dat_fi.loc['2004-06-30'] = int06[3]
        dat_fi.loc['2005-06-30'] = int06[4]
        dat_fi.loc['2006-06-30'] = int06[5]

        dat_fi.loc['2001-07-31'] = int07[0]
        dat_fi.loc['2002-07-31'] = int07[1]
        dat_fi.loc['2003-07-31'] = int07[2]
        dat_fi.loc['2004-07-31'] = int07[3]
        dat_fi.loc['2005-07-31'] = int07[4]
        dat_fi.loc['2006-07-31'] = int07[5]

        dat_fi.loc['2001-08-31'] = int08[0]
        dat_fi.loc['2002-08-31'] = int08[1]
        dat_fi.loc['2003-08-31'] = int08[2]
        dat_fi.loc['2004-08-31'] = int08[3]
        dat_fi.loc['2005-08-31'] = int08[4]
        dat_fi.loc['2006-08-31'] = int08[5]

        dat_fi.loc['2001-09-30'] = int09[0]
        dat_fi.loc['2002-09-30'] = int09[1]
        dat_fi.loc['2003-09-30'] = int09[2]
        dat_fi.loc['2004-09-30'] = int09[3]
        dat_fi.loc['2005-09-30'] = int09[4]
        dat_fi.loc['2006-09-30'] = int09[5]

        dat_fi.loc['2001-10-31'] = int10[0]
        dat_fi.loc['2002-10-31'] = int10[1]
        dat_fi.loc['2003-10-31'] = int10[2]
        dat_fi.loc['2004-10-31'] = int10[3]
        dat_fi.loc['2005-10-31'] = int10[4]
        dat_fi.loc['2006-10-31'] = int10[5]

        dat_fi.loc['2001-11-30'] = int11[0]
        dat_fi.loc['2002-11-30'] = int11[1]
        dat_fi.loc['2003-11-30'] = int11[2]
        dat_fi.loc['2004-11-30'] = int11[3]
        dat_fi.loc['2005-11-30'] = int11[4]
        dat_fi.loc['2006-11-30'] = int11[5]

        dat_fi.loc['2001-12-31'] = int12[0]
        dat_fi.loc['2002-12-31'] = int12[1]
        dat_fi.loc['2003-12-31'] = int12[2]
        dat_fi.loc['2004-12-31'] = int12[3]
        dat_fi.loc['2005-12-31'] = int12[4]
        dat_fi.loc['2006-12-31'] = int12[5]

    if fnames[f_i] in exceptions:
        if fnames[f_i] == 'HaleAveResource' or fnames[f_i] == 'OceansideOceanOutfall':
            for y_i in range(2001,2007):
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']
                dat_fi.loc[str(y_i)+'-02-28'] = dat_fi.loc['2007-02-28']
                dat_fi.loc[str(y_i)+'-03-31'] = dat_fi.loc['2007-03-31']
                dat_fi.loc[str(y_i)+'-04-30'] = dat_fi.loc['2007-04-30']
                dat_fi.loc[str(y_i)+'-05-31'] = dat_fi.loc['2007-05-31']
                dat_fi.loc[str(y_i)+'-06-30'] = dat_fi.loc['2007-06-30']
                dat_fi.loc[str(y_i)+'-07-31'] = dat_fi.loc['2007-07-31']
                dat_fi.loc[str(y_i)+'-08-31'] = dat_fi.loc['2007-08-31']
                dat_fi.loc[str(y_i)+'-09-30'] = dat_fi.loc['2007-09-30']
                dat_fi.loc[str(y_i)+'-10-31'] = dat_fi.loc['2007-10-31']
                dat_fi.loc[str(y_i)+'-11-30'] = dat_fi.loc['2007-11-30']
                dat_fi.loc[str(y_i)+'-12-31'] = dat_fi.loc['2007-12-31']
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']

        if fnames[f_i] == 'SouthBayReclamation':
            # set to 0 before 2002 - plant not online
            dat_fi.loc['2001-01-31'] = dat_fi.loc['2000-01-31']
            dat_fi.loc['2001-02-28'] = dat_fi.loc['2000-02-28']
            dat_fi.loc['2001-03-31'] = dat_fi.loc['2000-03-31']
            dat_fi.loc['2001-04-30'] = dat_fi.loc['2000-04-30']
            dat_fi.loc['2001-05-31'] = dat_fi.loc['2000-05-31']
            dat_fi.loc['2001-06-30'] = dat_fi.loc['2000-06-30']
            dat_fi.loc['2001-07-31'] = dat_fi.loc['2000-07-31']
            dat_fi.loc['2001-08-31'] = dat_fi.loc['2000-08-31']
            dat_fi.loc['2001-09-30'] = dat_fi.loc['2000-09-30']
            dat_fi.loc['2001-10-31'] = dat_fi.loc['2000-10-31']
            dat_fi.loc['2001-11-30'] = dat_fi.loc['2000-11-30']
            dat_fi.loc['2001-12-31'] = dat_fi.loc['2000-12-31']
            for y_i in range(2002,2007):
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']
                dat_fi.loc[str(y_i)+'-02-28'] = dat_fi.loc['2007-02-28']
                dat_fi.loc[str(y_i)+'-03-31'] = dat_fi.loc['2007-03-31']
                dat_fi.loc[str(y_i)+'-04-30'] = dat_fi.loc['2007-04-30']
                dat_fi.loc[str(y_i)+'-05-31'] = dat_fi.loc['2007-05-31']
                dat_fi.loc[str(y_i)+'-06-30'] = dat_fi.loc['2007-06-30']
                dat_fi.loc[str(y_i)+'-07-31'] = dat_fi.loc['2007-07-31']
                dat_fi.loc[str(y_i)+'-08-31'] = dat_fi.loc['2007-08-31']
                dat_fi.loc[str(y_i)+'-09-30'] = dat_fi.loc['2007-09-30']
                dat_fi.loc[str(y_i)+'-10-31'] = dat_fi.loc['2007-10-31']
                dat_fi.loc[str(y_i)+'-11-30'] = dat_fi.loc['2007-11-30']
                dat_fi.loc[str(y_i)+'-12-31'] = dat_fi.loc['2007-12-31']
                dat_fi.loc[str(y_i)+'-01-31'] = dat_fi.loc['2007-01-31']

    dat_fi = dat_fi.interpolate()
    dat_fi = dat_fi.bfill()
    dat_fi = dat_fi.ffill()
    # get only 1997-01-01 - 2017-12-31
    dat_fi = dat_fi['1997-01-01':'2017-12-31']
    # assign values
    lat_arr[f_i] = dat_fi[18][0]
    lon_arr[f_i] = dat_fi[19][0]
    flo_arr[:,f_i] = np.array(dat_fi[1]).astype(float)*mgd_to_m3s
    nh4_arr[:,f_i] = np.array(dat_fi[2].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_n
    no3_arr[:,f_i] = np.array(dat_fi[3]).astype(float)*mg_l_n
    doo_arr[:,f_i] = np.array(dat_fi[4]).astype(float)*mg_l_o
    tem_arr[:,f_i] = np.array(dat_fi[5]).astype(float)
    bod_arr[:,f_i] = np.array(dat_fi[6]).astype(float)*mg_l_o
    phh_arr[:,f_i] = np.array(dat_fi[7]).astype(float)
    tpp_arr[:,f_i] = np.array(dat_fi[8]).astype(float)*mg_l_p
    po4_arr[:,f_i] = np.array(dat_fi[9]).astype(float)*mg_l_p
    opp_arr[:,f_i] = np.array(dat_fi[10]).astype(float)*mg_l_p
    toc_arr[:,f_i] = np.array(dat_fi[11]).astype(float)*mg_l_c
    onn_arr[:,f_i] = np.array(dat_fi[12].replace(to_replace=' ',value=np.nan)).astype(float)*mg_l_n
    tfe_arr[:,f_i] = (np.array(dat_fi[13]).astype(float)*mg_l_f)/1000
    sil_arr[:,f_i] = np.array(dat_fi[14]).astype(float)*mg_l_s
    alk_arr[:,f_i] = np.array(dat_fi[15]).astype(float)*mg_l_c
    sal_arr[:,f_i] = np.array(dat_fi[16]).astype(float)
    dfe_arr[:,f_i] = (np.array(dat_fi[17]).astype(float)*mg_l_f)/1000

# time array
timeunit = 'days since 1997-01-01'
timenum = date2num(dat_fi.index.to_pydatetime(),timeunit)

# make netcdf
ncf = Dataset('minor_potw_1997_2017.nc','w')

tim_d = ncf.createDimension('time',None)
loc_d = ncf.createDimension('location',lat_arr.shape[0]) # 19 minor potws

tim_v = ncf.createVariable('time',np.float32,('time'))
lat_v = ncf.createVariable('latitude',np.float32,('location'))
lon_v = ncf.createVariable('longitude',np.float32,('location'))
flo_v = ncf.createVariable('flow',np.float64,('time','location'))
nh4_v = ncf.createVariable('NH4',np.float64,('time','location'))
no3_v = ncf.createVariable('NO3',np.float64,('time','location'))
doo_v = ncf.createVariable('dissolved_oxygen',np.float64,('time','location'))
tem_v = ncf.createVariable('temperature',np.float64,('time','location'))
bod_v = ncf.createVariable('BOD',np.float64,('time','location'))
phh_v = ncf.createVariable('pH',np.float64,('time','location'))
tpp_v = ncf.createVariable('total_P',np.float64,('time','location'))
po4_v = ncf.createVariable('PO4',np.float64,('time','location'))
opp_v = ncf.createVariable('organic_P',np.float64,('time','location'))
toc_v = ncf.createVariable('total_organic_C',np.float64,('time','location'))
onn_v = ncf.createVariable('organic_N',np.float64,('time','location'))
tfe_v = ncf.createVariable('total_Fe',np.float64,('time','location'))
sil_v = ncf.createVariable('SiO4',np.float64,('time','location'))
alk_v = ncf.createVariable('alkalinity',np.float64,('time','location'))
sal_v = ncf.createVariable('salinity',np.float64,('time','location'))
dfe_v = ncf.createVariable('dissolved_Fe',np.float64,('time','location'))

tim_v.units = timeunit
flo_v.units = 'm3/s'
nh4_v.units = 'mmol/m3'
no3_v.units = 'mmol/m3'
doo_v.units = 'mmol/m3'
tem_v.units = 'mmol/m3'
bod_v.units = 'mmol/m3'
phh_v.units = 'mmol/m3'
tpp_v.units = 'mmol/m3'
po4_v.units = 'mmol/m3'
opp_v.units = 'mmol/m3'
toc_v.units = 'mmol/m3'
onn_v.units = 'mmol/m3'
tfe_v.units = 'mmol/m3'
sil_v.units = 'mmol/m3'
alk_v.units = 'mmol/m3'
sal_v.units = 'mmol/m3'
dfe_v.units = 'mmol/m3'

tim_v[:] = timenum
lat_v[:] = lat_arr
lon_v[:] = lon_arr
flo_v[:,:] = flo_arr
nh4_v[:,:] = nh4_arr
no3_v[:,:] = no3_arr
doo_v[:,:] = doo_arr
tem_v[:,:] = tem_arr
bod_v[:,:] = bod_arr
phh_v[:,:] = phh_arr
tpp_v[:,:] = tpp_arr
po4_v[:,:] = po4_arr
opp_v[:,:] = opp_arr
toc_v[:,:] = toc_arr
onn_v[:,:] = onn_arr
tfe_v[:,:] = tfe_arr
sil_v[:,:] = sil_arr
alk_v[:,:] = alk_arr
sal_v[:,:] = sal_arr
dfe_v[:,:] = dfe_arr

ncf.close()

writer = pd.ExcelWriter('minor_potw_1997_2017.xlsx')

# print to excel file
for p_i in range(flo_arr.shape[1]):
    df = pd.DataFrame({'date':dat_fi.index.date,
    'flow m3/s':flo_arr[:,p_i],
    'NH4 mmol/m3':nh4_arr[:,p_i],
    'NO3 mmol/m3':no3_arr[:,p_i],
    'DO mmol/m3':doo_arr[:,p_i],
    'temperature C':tem_arr[:,p_i],
    'BOD mmol/m3':bod_arr[:,p_i],
    'pH':phh_arr[:,p_i],
    'TP mmol/m3':tpp_arr[:,p_i],
    'PO4 mmol/m3':po4_arr[:,p_i],
    'OP mmol/m3':opp_arr[:,p_i],
    'TOC mmol/m3':toc_arr[:,p_i],
    'ON mmol/m3':onn_arr[:,p_i],
    'total Fe mmol/m3':tfe_arr[:,p_i],
    'SiO4 mmol/m3':sil_arr[:,p_i],
    'Alk mmol/m3':alk_arr[:,p_i],
    'salinity PSU':sal_arr[:,p_i],
    'dissolved Fe mmol/m3':dfe_arr[:,p_i],
    'latitude':lat_arr[p_i],
    'longitude':lon_arr[p_i]},index=None,columns=None)
    df.to_excel(writer,sheet_name=rnames[p_i])

writer.save()
