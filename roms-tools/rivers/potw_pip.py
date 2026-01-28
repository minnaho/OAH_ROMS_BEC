# create POTW ROMS file
# e.g., mc60_pip.nc

import numpy as np
from scipy.io import loadmat
from netCDF4 import num2date,Dataset,date2num

ncfile = '/data/project9/minnaho/swel/mc60_pip.nc'


data0 = loadmat('ROMS_CC_new.mat')

data = data0['ROMS']

print(data.dtype.names)

dt = num2date(data['time'][0,0].flatten(),'days since 1994-01-01')

target_year = 2019
target_month = 4

# Find matching index for time
idx = np.where([(d.year == target_year and d.month == target_month) for d in dt])[0][0]

# get correct POTWs for region manually by looking at data
# Carmel Area     data['name'][0,0][7]
# Monterey One    data['name'][0,0][6]
# Watsonville     data['name'][0,0][5]
# Santa Cruz      data['name'][0,0][4]

# POTW indices
pind = [4,5,6,7]
# target time range +-2
tind = range(idx-2,idx+2)

# 1D attributes
attr = ['lon', 'lat', 'depth', 'name']
attrnc = []

# order of tracers in ROMS
ntracers = ['temp','salt','PO4','NO3','SIO3','NH4','FE','O2','DIC','ALK','DOC','Don','Dofe','Dop','Dopr','Donr','ZOOC','SPCHL','SPC','SPFE','SPCACO3','DIATCHL','DIATC','DIATFE','DIATSI','Diazchl','Diazc','Diazfe','NO2','N2','N2O']

# Prepare a lowercase version of ntracers for comparison
ntracers_lower = [item.lower() for item in ntracers]


# create pipe_tracer variable
pipt = np.ones((len(tind),len(ntracers),len(pind)))*np.nan
# create pipe_volume variable
pipv = np.ones((len(tind),len(pind)))*np.nan

# loop through pipes to get attributes
# pipe volume
for p_i in range(len(pind)):
    pipv[:,p_i] = data['flow'][0][0][pind[p_i],tind]

# pipe tracer
for p_i in range(len(pind)):
    # loop through variables
    for v_i in range(8,len(list(data.dtype.names))):
        # check if variable is in the data
        if list(data.dtype.names)[v_i].lower() in ntracers_lower:
            # for the given variable, find 
            # and assign the correct index for ROMS
            pipt[:,ntracers_lower.index(list(data.dtype.names)[v_i].lower()),p_i] = data[list(data.dtype.names)[v_i]][0,0][pind[p_i],tind]
        
# create the pipe_time
pipe_time_unit = 'days since 1995-01-01' # ROMS time
pipe_time_dt = date2num(dt,pipe_time_unit)[tind]
            
pipnc = Dataset(ncfile,'w')
ptime = pipnc.createDimension('pipe_time',len(tind))
npipe = pipnc.createDimension('npipe',len(pind))
nt    = pipnc.createDimension('ntracers',len(ntracers))
pipe_time = pipnc.createVariable('pipe_time','f8',('pipe_time'))
pipe_volume = pipnc.createVariable('pipe_volume','f4',('pipe_time','npipe'))
pipe_tracer = pipnc.createVariable('pipe_tracer','f4',('pipe_time','ntracers','npipe'))

pipe_time[:] = pipe_time_dt
pipe_time.units = pipe_time_unit

pipe_volume[:,:] = pipv
pipe_volume.units = 'm3/s'

pipe_tracer[:,:,:] = pipt
pipe_tracer.units = 'C or PSU or mmol/m3'

pipnc.Pipe_01 = str(data['name'][0,0][4][0][0])+' ('+str(data['lon'][0,0][4][0])+', '+str(data['lat'][0,0][4][0])+')'
pipnc.Pipe_02 = str(data['name'][0,0][5][0][0])+' ('+str(data['lon'][0,0][5][0])+', '+str(data['lat'][0,0][5][0])+')'
pipnc.Pipe_03 = str(data['name'][0,0][6][0][0])+' ('+str(data['lon'][0,0][6][0])+', '+str(data['lat'][0,0][6][0])+')'
pipnc.Pipe_04 = str(data['name'][0,0][7][0][0])+' ('+str(data['lon'][0,0][7][0])+', '+str(data['lat'][0,0][7][0])+')'

pipnc.close()
