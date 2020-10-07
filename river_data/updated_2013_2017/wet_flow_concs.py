# separate wet/dry weather flows 
# for wet/dry concentration
# average wet season flows (Nov-Apr)
import pandas as pd
import numpy as np
from netCDF4 import Dataset,date2num

# calculate baseflow form USGS HYSEP
def fixed_interval_filter(ts, size):
    """USGS HYSEP fixed interval method
    
    The USGS HYSEP fixed interval method as described in `Sloto & Crouse, 1996`_.
    
    .. _Slot & Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. HYSEP: A Computer Program for Streamflow Hydrograph Separation and 
        Analysis. USGS Numbered Series. Water-Resources Investigations Report. Geological Survey (U.S.), 1996. 
        http://pubs.er.usgs.gov/publication/wri964040.
    
    :param size: 
    :param ts: 
    :return: 
    """
    intervals = np.arange(len(ts)) // size
    baseflow = pd.Series(data=ts.groupby(intervals).transform('min'), index=ts.index)
    quickflow = ts - baseflow

    baseflow.name = 'baseflow'
    quickflow.name = 'quickflow'

    return baseflow, quickflow

def sliding_interval_filter(ts, size):
    """USGS HYSEP sliding interval method
    
        The USGS HYSEP sliding interval method as described in `Sloto & Crouse, 1996`_.
        
        The flow series is filter with scipy.ndimage.genericfilter1D using numpy.nanmin function
        over a window of size `size`
    
    .. _Slot & Crouse, 1996:
        Sloto, Ronald A., and Michele Y. Crouse. “HYSEP: A Computer Program for Streamflow Hydrograph Separation and 
        Analysis.” USGS Numbered Series. Water-Resources Investigations Report. Geological Survey (U.S.), 1996. 
        http://pubs.er.usgs.gov/publication/wri964040.
    
    :param size: 
    :param ts: 
    :return: 
    """
    from scipy.ndimage.filters import minimum_filter1d, generic_filter
    # TODO ckeck the presence of nodata
    if (ts.isnull()).any():
        blocks, nfeatures = label(~ts.isnull())
        block_list = [ts[blocks == i] for i in range(1, nfeatures + 1)]
        na_df = ts[blocks == 0]
        block_bf = [pd.Series(data=minimum_filter1d(block, size, mode='reflect'), index=block.index) for block in
                    block_list]
        baseflow = pd.concat(block_bf + [na_df], axis=0)
        baseflow.sort_index(inplace=True)
    else:
        baseflow = pd.Series(data=minimum_filter1d(ts, size, mode='reflect'), index=ts.index)

    quickflow = ts - baseflow

    baseflow.name = 'baseflow'
    quickflow.name = 'quickflow'

    return baseflow, quickflow



# wet/dry months
wet_m = [11,12,1,2,3,4]
dry_m = [5,6,7,8,9,10]

fi = '/data/project1/minnaho/river_data/updated_2013_2017/formatted/arroyo_trabuco_creek_2007_2018.csv'

#fi = glob.glob(fi)
#rnames = 

df = pd.read_csv(fi)
df['date'] = pd.to_datetime(df['date'])
df.set_index(df['date'],inplace=True)

# usgs flow data
flow = df['dry flow cfs'][1:]

baseflow_fixed,quickflow_fixed = fixed_interval_filter(flow,flow.shape[0])
baseflow_slide,quickflow_slide = sliding_interval_filter(flow,flow.shape[0])




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
print('wet median: ',wet_med)

dry_flows = np.array(dry_flows_l)
dry_med = np.nanmedian(dry_flows)
print('dry median: ',dry_med)

'''
# use wet concentrations for 3 days after flow/wet_med > 2
for d_i in range(flow.shape[0]):
    print('flow: ',flow[d_i])
    if flow[d_i]/wet_med >= 2:
        # use wet flow conc
        print('wet conc')
    elif (
        (flow[d_i-1]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
        (flow[d_i-2]/wet_med >= 2 and flow[d_i]/wet_med < 2) or
        (flow[d_i-3]/wet_med >= 2 and flow[d_i]/wet_med < 2)
       ):
        # use wet flow conc
        print('wet conc')
    elif flow[d_i]/wet_med < 2:
        # use dry flow conc
        print('dry conc')

'''
