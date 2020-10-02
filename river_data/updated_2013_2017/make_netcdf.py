###############################
# take 2007-2018 river data
# and turn to netcdf
# for psource model input
##############################
import numpy as np
from netCDF4 import Dataset,date2num
import pandas as pd
import glob

# path to files
fol = '/data/project1/minnaho/river_data/updated_2013_2017/formatted/'
fnames = sorted(glob.glob(fol+'*'))

# get river names
# order of rivers in netcdf will be alphabetical
rnames = []
for f_i in fnames:
    rnames.append(f_i[62:f_i.index('_2007')])

example = pd.read_csv(fnames[0],header=None)

# time array
pddate = pd.to_datetime(example[1][1:])
timeunit = 'days since 2007-01-01'

# make arrays
tim_arr = np.arange(0,pddate.shape[0])
lat_arr = np.empty((len(fnames)))
lon_arr = np.empty((len(fnames)))
flo_arr = np.empty((pddate.shape,len(fnames)))
tnn_arr = np.empty((pddate.shape,len(fnames)))
tpp_arr = np.empty((pddate.shape,len(fnames)))
nh4_arr = np.empty((pddate.shape,len(fnames)))
no3_arr = np.empty((pddate.shape,len(fnames)))
po4_arr = np.empty((pddate.shape,len(fnames)))
alk_arr = np.empty((pddate.shape,len(fnames)))

# loop through files
for f_i in range(len(fnames)):
    riv = pd.read_csv(fnames[f_i],header=None)
    flo_arr[:,f_i] = np.array(riv[6][1:]).astype(float)
    tnn_arr[:,f_i] = np.array(riv[7][1:]).astype(float)
    tpp_arr[:,f_i] = np.array(riv[8][1:]).astype(float)
    nh4_arr[:,f_i] = np.array(riv[9][1:]).astype(float)
    no3_arr[:,f_i] = np.array(riv[10][1:]).astype(float)
    po4_arr[:,f_i] = np.array(riv[11][1:]).astype(float)
    alk_arr[:,f_i] = np.array(riv[12][1:]).astype(float)

