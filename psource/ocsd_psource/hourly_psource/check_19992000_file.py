import numpy as np
from netCDF4 import Dataset,num2date
import matplotlib.pyplot as plt

nc_file = Dataset('roms_psource_hourly_1999_2000.nc','r')

# 56-69
ocsd_nsrc = np.arange(56,70)

time_u = nc_file.variables['psrc_time'].units
time_dt = num2date(np.array(nc_file.variables['psrc_time']),time_u)

qbar = np.array(nc_file.variables['Qbar'][ocsd_nsrc])

# nan data is at 4643
st_in = 4600
en_in = 4800

plt.ion()
for q_i in qbar:
    plt.plot(time_dt[st_in:en_in],q_i[st_in:en_in])
