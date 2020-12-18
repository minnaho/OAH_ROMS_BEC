import pandas as pd
import glob as glob
import numpy as np

prismf = '/data/project1/minnaho/river_data/updated_2013_2017/rational_method_rivers/prism_ppt/*'
precip_old = '/data/project1/minnaho/runoff_river_model/Precip/A*.csv'

prism_fi = glob.glob(prismf)[:-1]
preci_fi = glob.glob(precip_old)

prcip_old = pd.read_csv('/data/project1/minnaho/runoff_river_model/precipitations.txt',sep='\t')
# slice for just rain values already in cm
prcip_sli = prcip_old.iloc[:-3,3:-1]
rshp = np.asarray(prcip_sli).reshape(14,365,366)
#rshp[rshp<0.5] = np.nan
# average over all watersheds then find annual sum
annual_mean = np.nansum(np.nanmean(rshp,axis=2),axis=1)
old_med = np.nanmedian(annual_mean)
old25 = np.percentile(annual_mean,25)
old75 = np.percentile(annual_mean,75)
# values much higher because of large rain event in 2011

# rain event = 0.2 inches = 0.5 cm

ppt = pd.read_csv(prism_fi[0],header=None,skiprows=11) # read file
river_ts = np.empty((ppt[0].shape[0],len(prism_fi)))

for r_i in range(len(prism_fi)):
    print('river '+str(r_i)+' of '+str(len(prism_fi)))
    ppt = pd.read_csv(prism_fi[r_i],header=None,skiprows=11) # read file
    precip = np.array(ppt[1])*(1./10) # precipitation convert mm to cm
    river_ts[:,r_i] = precip

# skip 2007-2010 and exclude 2018
rshp = river_ts[4*365:-368,:].reshape(7,365,47)
annual_mean = np.nansum(np.nanmean(rshp,axis=2),axis=1)
new_med = np.nanmedian(annual_mean)
new25 = np.percentile(annual_mean,25)
new75 = np.percentile(annual_mean,75)

print('old med',old_med)
print('old 25',old25)
print('old 75',old75)

print('new med',new_med)
print('new 25',new25)
print('new 75',new75)


