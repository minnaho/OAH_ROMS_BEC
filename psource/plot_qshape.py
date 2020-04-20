import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

psource_f = 'roms_psource.nc'
qshape_nc = Dataset(psource_f,'r').variables['Qshape']
qbar_nc = Dataset(psource_f,'r').variables['Qbar']
i_nc = Dataset(psource_f,'r').variables['Isrc']
j_nc = Dataset(psource_f,'r').variables['Jsrc']

# 56 is first ocsd point from make_psource file
# first point
p1 = 56
p2 = 62
plt.ion()

pst = 56
pen = 69
plt.figure()
for p_i in range(pst,63):
    plt.plot(qshape_nc[:,p_i],range(len(qshape_nc[:,p_i])),label=p_i)

for p_i in range(63,pen+1):
    plt.plot(qshape_nc[:,p_i],range(len(qshape_nc[:,p_i])),label=p_i,linestyle='--')

plt.ylim([0,35])
plt.title('Qshape')
plt.legend(loc='best')


plt.figure()
for p_i in range(pst,63):
    plt.scatter(i_nc[p_i],j_nc[p_i],label='Nsrc = '+str(p_i))

for p_i in range(63,pen+1):
    plt.scatter(i_nc[p_i],j_nc[p_i],label='Nsrc = '+str(p_i),marker='^')

plt.legend(loc='best')
plt.title('locations')


#pst = 56
#pen = 69
#plt.figure()
#for p_i in range(pst,63):
#    plt.plot(qbar_nc[:,p_i],range(len(qbar_nc[:,p_i])),label=p_i)
#
#for p_i in range(63,pen+1):
#    plt.plot(qbar_nc[:,p_i],range(len(qbar_nc[:,p_i])),label=p_i,linestyle='--')

#plt.ylim([0,35])
#plt.title('Qbar')
#plt.legend(loc='best')

#plt.plot(qshape_nc[:,p1],range(len(qshape_nc[:,p1])),label=p1)
#plt.plot(qshape_nc[:,p1+1],range(len(qshape_nc[:,p1+1])),label=p1+1)
#
#plt.plot(qshape_nc[:,p2],range(len(qshape_nc[:,p2])),label=p2)
#plt.plot(qshape_nc[:,p2+1],range(len(qshape_nc[:,p2+1])),label=p2+1)
#
#
#plt.plot(qshape_nc[:,0],range(len(qshape_nc[:,0])),label=0)
#plt.legend(loc='best')
#
