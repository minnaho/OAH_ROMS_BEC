import numpy as np
import pandas as pd
import h5py
import scipy.io


outpath = './data/2016/'

#date_dat = pd.read_csv('./data/2017/bight_profil_date.mat')

date_dat = h5py.File(outpath+'bight_profil_date.mat','r')
f = scipy.io.loadmat(outpath+'bight_profil_date.mat')
dates = f['bight_profil_date']

dt = pd.to_datetime(datemat-719529, unit='D')
