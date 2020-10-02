# separate wet/dry weather flows 
# for wet/dry concentration
# average wet season flows (Nov-Apr)
import pandas as pd
import numpy as np
from netCDF4 import Dataset,date2num

# wet months
wet_m = [11,12,1,2,3,4]

fi = '/data/project1/minnaho/river_data/updated_2013_2017/formatted/arroyo_trabuco_creek_2007_2018.csv'

df = pd.read_csv(fi)
df['date'] = pd.to_datetime(df['date'])
df.set_index(df['date'],inplace=True)

flow = df['dry flow cfs'][1:]

wet_flows_l = []
for f_i in range(flow.shape[0]):
    if flow.index[f_i].month in wet_m:
        wet_flows_l.append(flow[f_i])

wet_flows = np.array(wet_flows_l)
wet_med = np.nanmedian(wet_flows)
print('wet median: ',wet_med)

# use wet concentrations for 3 days after flow/wet_med > 2
for d_i in range(flow.shape[0]):
    print('flow: ',flow[d_i])
    if flow[d_i]/wet_med >= 2:
        # use wet flow conc
        print('wet conc')
    if (
        (flow[d_i-1]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
        (flow[d_i-2]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
        (flow[d_i-3]/wet_med >= 2 and flow[d_i]/wet_med < 2)
       ):
        # use wet flow conc
        print('wet conc')
    else:
        # use dry flow conc
        print('dry conc')

 
