import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from netCDF4 import Dataset,num2date,date2num
import datetime as datetime

# data paths
major_path = '/data/project1/minnaho/potw_outfall_data/major_potw_data.nc'
minor_path = '/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc'

###############
# major data [:,i,i] i=0,1,2,3; 0 = hyp, 1 = jwpcp, 2 = ocsd, 3 = plwtp
###############
major_nc = Dataset(major_path,'r')

major_time = num2date(np.array(major_nc.variables['time']),major_nc.variables['time'].units)

# convert real_datetime to datetime
major_time_l = []
for d_i in range(len(major_time)):
    major_time_l.append(major_time[d_i]+datetime.timedelta(0,1))

major_time_dt = np.array(major_time_l)

st_in = 313 #1997-01-31
en_in = 517 #2014-01-13

major_flo = np.array(major_nc.variables['flow']) # m3/s
major_nh4 = np.array(major_nc.variables['NH4']) # mmol/m3
major_no3 = np.array(major_nc.variables['NO3']) # mmol/m3
major_no2 = np.array(major_nc.variables['NO2']) # mmol/m3
major_on  = np.array(major_nc.variables['ON']) # mmol/m3
major_po4 = np.array(major_nc.variables['PO4']) # mmol/m3
major_op  = np.array(major_nc.variables['OP']) # mmol/m3
major_fe  = np.array(major_nc.variables['Fe'])  # mmol/m3
major_pH  = np.array(major_nc.variables['pH']) 
major_toc  = np.array(major_nc.variables['TOC']) 
major_alk = np.array(major_nc.variables['alkalinity']) 
major_temp = np.array(major_nc.variables['temperature']) 
major_salt = np.array(major_nc.variables['salinity']) 

major_tn = major_nh4+major_no3+major_no2+major_on
major_tp = major_po4+major_op

a = []
major_flo[major_flo>1E36]=np.nan
for m_i in range(major_flo.shape[1]):
    a.append(major_flo[:,m_i,m_i]*major_tn[:,m_i,m_i])

major_potw_fluxn = np.array(a)
major_potw_fluxalln = np.nansum(np.array(a),axis=0)

b = []
for m_i in range(major_flo.shape[1]):
    b.append(major_flo[:,m_i,m_i]*major_tp[:,m_i,m_i])

major_potw_fluxp = np.array(b)
major_potw_fluxallp = np.nansum(np.array(b),axis=0)

c = []
for m_i in range(major_flo.shape[1]):
    c.append(major_flo[:,m_i,m_i]*major_toc[:,m_i,m_i])

major_potw_fluxc = np.array(c)
major_potw_fluxallc = np.nansum(np.array(c),axis=0)


major_potw_fluxn = np.transpose(a)
major_potw_fluxp = np.transpose(b)
major_potw_fluxc = np.transpose(c)

# plotting major
figw = 10
#figw = 12
figh = 8
axis_tick_font = 14
axis_font = 14
major_names = ['HTP','JWPCP','OCSD','PLWTP']
major_linesty = ['-','--','-.',':']
lw = 3
plwtp_st = 170
iend_major = 506

t_1970 = 0
t_1980 = 109
t_1990 = 229
t_2000 = 349
t_2010 = 469

print('Average per decade')
print('HTP flow m3/s 1970: ',np.nanmean(major_flo[t_1970:t_1980,0,0]))
print('JWP flow m3/s 1970: ',np.nanmean(major_flo[t_1970:t_1980,1,1]))
print('OCS flow m3/s 1970: ',np.nanmean(major_flo[t_1970:t_1980,2,2]))
print('PLW flow m3/s 1970: ',np.nanmean(major_flo[t_1970:t_1980,3,3]))

print('HTP TN flux mmol/s 1970: ',np.nanmean(major_potw_fluxn[t_1970:t_1980,0]))
print('JWP TN flux mmol/s 1970: ',np.nanmean(major_potw_fluxn[t_1970:t_1980,1]))
print('OCS TN flux mmol/s 1970: ',np.nanmean(major_potw_fluxn[t_1970:t_1980,2]))
print('PLW TN flux mmol/s 1970: ',np.nanmean(major_potw_fluxn[t_1970:t_1980,3]))

print('HTP TP flux mmol/s 1970: ',np.nanmean(major_potw_fluxp[t_1970:t_1980,0]))
print('JWP TP flux mmol/s 1970: ',np.nanmean(major_potw_fluxp[t_1970:t_1980,1]))
print('OCS TP flux mmol/s 1970: ',np.nanmean(major_potw_fluxp[t_1970:t_1980,2]))
print('PLW TP flux mmol/s 1970: ',np.nanmean(major_potw_fluxp[t_1970:t_1980,3]))

print('HTP TOC flux mmol/s 1970: ',np.nanmean(major_potw_fluxc[t_1970:t_1980,0]))
print('JWP TOC flux mmol/s 1970: ',np.nanmean(major_potw_fluxc[t_1970:t_1980,1]))
print('OCS TOC flux mmol/s 1970: ',np.nanmean(major_potw_fluxc[t_1970:t_1980,2]))
print('PLW TOC flux mmol/s 1970: ',np.nanmean(major_potw_fluxc[t_1970:t_1980,3]))


print('HTP flow m3/s 1980: ',np.nanmean(major_flo[t_1980:t_1990,0,0]))
print('JWP flow m3/s 1980: ',np.nanmean(major_flo[t_1980:t_1990,1,1]))
print('OCS flow m3/s 1980: ',np.nanmean(major_flo[t_1980:t_1990,2,2]))
print('PLW flow m3/s 1980: ',np.nanmean(major_flo[t_1980:t_1990,3,3]))

print('HTP TN flux mmol/s 1980: ',np.nanmean(major_potw_fluxn[t_1980:t_1990,0]))
print('JWP TN flux mmol/s 1980: ',np.nanmean(major_potw_fluxn[t_1980:t_1990,1]))
print('OCS TN flux mmol/s 1980: ',np.nanmean(major_potw_fluxn[t_1980:t_1990,2]))
print('PLW TN flux mmol/s 1980: ',np.nanmean(major_potw_fluxn[t_1980:t_1990,3]))

print('HTP TP flux mmol/s 1980: ',np.nanmean(major_potw_fluxp[t_1980:t_1990,0]))
print('JWP TP flux mmol/s 1980: ',np.nanmean(major_potw_fluxp[t_1980:t_1990,1]))
print('OCS TP flux mmol/s 1980: ',np.nanmean(major_potw_fluxp[t_1980:t_1990,2]))
print('PLW TP flux mmol/s 1980: ',np.nanmean(major_potw_fluxp[t_1980:t_1990,3]))

print('HTP TOC flux mmol/s 1980: ',np.nanmean(major_potw_fluxc[t_1980:t_1990,0]))
print('JWP TOC flux mmol/s 1980: ',np.nanmean(major_potw_fluxc[t_1980:t_1990,1]))
print('OCS TOC flux mmol/s 1980: ',np.nanmean(major_potw_fluxc[t_1980:t_1990,2]))
print('PLW TOC flux mmol/s 1980: ',np.nanmean(major_potw_fluxc[t_1980:t_1990,3]))

print('HTP flow m3/s 1990: ',np.nanmean(major_flo[t_1990:t_2000,0,0]))
print('JWP flow m3/s 1990: ',np.nanmean(major_flo[t_1990:t_2000,1,1]))
print('OCS flow m3/s 1990: ',np.nanmean(major_flo[t_1990:t_2000,2,2]))
print('PLW flow m3/s 1990: ',np.nanmean(major_flo[t_1990:t_2000,3,3]))

print('HTP TN flux mmol/s 1990: ',np.nanmean(major_potw_fluxn[t_1990:t_2000,0]))
print('JWP TN flux mmol/s 1990: ',np.nanmean(major_potw_fluxn[t_1990:t_2000,1]))
print('OCS TN flux mmol/s 1990: ',np.nanmean(major_potw_fluxn[t_1990:t_2000,2]))
print('PLW TN flux mmol/s 1990: ',np.nanmean(major_potw_fluxn[t_1990:t_2000,3]))

print('HTP TP flux mmol/s 1990: ',np.nanmean(major_potw_fluxp[t_1990:t_2000,0]))
print('JWP TP flux mmol/s 1990: ',np.nanmean(major_potw_fluxp[t_1990:t_2000,1]))
print('OCS TP flux mmol/s 1990: ',np.nanmean(major_potw_fluxp[t_1990:t_2000,2]))
print('PLW TP flux mmol/s 1990: ',np.nanmean(major_potw_fluxp[t_1990:t_2000,3]))

print('HTP TOC flux mmol/s 1990: ',np.nanmean(major_potw_fluxc[t_1990:t_2000,0]))
print('JWP TOC flux mmol/s 1990: ',np.nanmean(major_potw_fluxc[t_1990:t_2000,1]))
print('OCS TOC flux mmol/s 1990: ',np.nanmean(major_potw_fluxc[t_1990:t_2000,2]))
print('PLW TOC flux mmol/s 1990: ',np.nanmean(major_potw_fluxc[t_1990:t_2000,3]))

print('HTP flow m3/s 2000: ',np.nanmean(major_flo[t_2000:t_2010,0,0]))
print('JWP flow m3/s 2000: ',np.nanmean(major_flo[t_2000:t_2010,1,1]))
print('OCS flow m3/s 2000: ',np.nanmean(major_flo[t_2000:t_2010,2,2]))
print('PLW flow m3/s 2000: ',np.nanmean(major_flo[t_2000:t_2010,3,3]))

print('HTP TN flux mmol/s 2000: ',np.nanmean(major_potw_fluxn[t_2000:t_2010,0]))
print('JWP TN flux mmol/s 2000: ',np.nanmean(major_potw_fluxn[t_2000:t_2010,1]))
print('OCS TN flux mmol/s 2000: ',np.nanmean(major_potw_fluxn[t_2000:t_2010,2]))
print('PLW TN flux mmol/s 2000: ',np.nanmean(major_potw_fluxn[t_2000:t_2010,3]))

print('HTP TP flux mmol/s 2000: ',np.nanmean(major_potw_fluxp[t_2000:t_2010,0]))
print('JWP TP flux mmol/s 2000: ',np.nanmean(major_potw_fluxp[t_2000:t_2010,1]))
print('OCS TP flux mmol/s 2000: ',np.nanmean(major_potw_fluxp[t_2000:t_2010,2]))
print('PLW TP flux mmol/s 2000: ',np.nanmean(major_potw_fluxp[t_2000:t_2010,3]))

print('HTP TOC flux mmol/s 2000: ',np.nanmean(major_potw_fluxc[t_2000:t_2010,0]))
print('JWP TOC flux mmol/s 2000: ',np.nanmean(major_potw_fluxc[t_2000:t_2010,1]))
print('OCS TOC flux mmol/s 2000: ',np.nanmean(major_potw_fluxc[t_2000:t_2010,2]))
print('PLW TOC flux mmol/s 2000: ',np.nanmean(major_potw_fluxc[t_2000:t_2010,3]))


print('HTP flow m3/s 2010: ',np.nanmean(major_flo[t_2010:,0,0]))
print('JWP flow m3/s 2010: ',np.nanmean(major_flo[t_2010:,1,1]))
print('OCS flow m3/s 2010: ',np.nanmean(major_flo[t_2010:,2,2]))
print('PLW flow m3/s 2010: ',np.nanmean(major_flo[t_2010:,3,3]))

print('HTP TN flux mmol/s 2010: ',np.nanmean(major_potw_fluxn[t_2010:,0]))
print('JWP TN flux mmol/s 2010: ',np.nanmean(major_potw_fluxn[t_2010:,1]))
print('OCS TN flux mmol/s 2010: ',np.nanmean(major_potw_fluxn[t_2010:,2]))
print('PLW TN flux mmol/s 2010: ',np.nanmean(major_potw_fluxn[t_2010:,3]))

print('HTP TP flux mmol/s 2010: ',np.nanmean(major_potw_fluxp[t_2010:,0]))
print('JWP TP flux mmol/s 2010: ',np.nanmean(major_potw_fluxp[t_2010:,1]))
print('OCS TP flux mmol/s 2010: ',np.nanmean(major_potw_fluxp[t_2010:,2]))
print('PLW TP flux mmol/s 2010: ',np.nanmean(major_potw_fluxp[t_2010:,3]))

print('HTP TOC flux mmol/s 2010: ',np.nanmean(major_potw_fluxc[t_2010:,0]))
print('JWP TOC flux mmol/s 2010: ',np.nanmean(major_potw_fluxc[t_2010:,1]))
print('OCS TOC flux mmol/s 2010: ',np.nanmean(major_potw_fluxc[t_2010:,2]))
print('PLW TOC flux mmol/s 2010: ',np.nanmean(major_potw_fluxc[t_2010:,3]))

#print('HTP flow m3/s 1970: ',major_flo[t_1970,0,0])
#print('JWP flow m3/s 1970: ',major_flo[t_1970,1,1])
#print('OCS flow m3/s 1970: ',major_flo[t_1970,2,2])
#print('PLW flow m3/s 1970: ',major_flo[t_1970,3,3])
#
#print('HTP TN flux mmol/s 1970: ',major_potw_fluxn[t_1970,0])
#print('JWP TN flux mmol/s 1970: ',major_potw_fluxn[t_1970,1])
#print('OCS TN flux mmol/s 1970: ',major_potw_fluxn[t_1970,2])
#print('PLW TN flux mmol/s 1970: ',major_potw_fluxn[t_1970,3])
#
#print('HTP TP flux mmol/s 1970: ',major_potw_fluxp[t_1970,0])
#print('JWP TP flux mmol/s 1970: ',major_potw_fluxp[t_1970,1])
#print('OCS TP flux mmol/s 1970: ',major_potw_fluxp[t_1970,2])
#print('PLW TP flux mmol/s 1970: ',major_potw_fluxp[t_1970,3])
#
#print('HTP TOC flux mmol/s 1970: ',major_potw_fluxc[t_1970,0])
#print('JWP TOC flux mmol/s 1970: ',major_potw_fluxc[t_1970,1])
#print('OCS TOC flux mmol/s 1970: ',major_potw_fluxc[t_1970,2])
#print('PLW TOC flux mmol/s 1970: ',major_potw_fluxc[t_1970,3])
#
#
#print('HTP flow m3/s 1980: ',major_flo[t_1980,0,0])
#print('JWP flow m3/s 1980: ',major_flo[t_1980,1,1])
#print('OCS flow m3/s 1980: ',major_flo[t_1980,2,2])
#print('PLW flow m3/s 1980: ',major_flo[t_1980,3,3])
#
#print('HTP TN flux mmol/s 1980: ',major_potw_fluxn[t_1980,0])
#print('JWP TN flux mmol/s 1980: ',major_potw_fluxn[t_1980,1])
#print('OCS TN flux mmol/s 1980: ',major_potw_fluxn[t_1980,2])
#print('PLW TN flux mmol/s 1980: ',major_potw_fluxn[t_1980,3])
#
#print('HTP TP flux mmol/s 1980: ',major_potw_fluxp[t_1980,0])
#print('JWP TP flux mmol/s 1980: ',major_potw_fluxp[t_1980,1])
#print('OCS TP flux mmol/s 1980: ',major_potw_fluxp[t_1980,2])
#print('PLW TP flux mmol/s 1980: ',major_potw_fluxp[t_1980,3])
#
#print('HTP TOC flux mmol/s 1980: ',major_potw_fluxc[t_1980,0])
#print('JWP TOC flux mmol/s 1980: ',major_potw_fluxc[t_1980,1])
#print('OCS TOC flux mmol/s 1980: ',major_potw_fluxc[t_1980,2])
#print('PLW TOC flux mmol/s 1980: ',major_potw_fluxc[t_1980,3])
#
#print('HTP flow m3/s 1990: ',major_flo[t_1990,0,0])
#print('JWP flow m3/s 1990: ',major_flo[t_1990,1,1])
#print('OCS flow m3/s 1990: ',major_flo[t_1990,2,2])
#print('PLW flow m3/s 1990: ',major_flo[t_1990,3,3])
#
#print('HTP TN flux mmol/s 1990: ',major_potw_fluxn[t_1990,0])
#print('JWP TN flux mmol/s 1990: ',major_potw_fluxn[t_1990,1])
#print('OCS TN flux mmol/s 1990: ',major_potw_fluxn[t_1990,2])
#print('PLW TN flux mmol/s 1990: ',major_potw_fluxn[t_1990,3])
#
#print('HTP TP flux mmol/s 1990: ',major_potw_fluxp[t_1990,0])
#print('JWP TP flux mmol/s 1990: ',major_potw_fluxp[t_1990,1])
#print('OCS TP flux mmol/s 1990: ',major_potw_fluxp[t_1990,2])
#print('PLW TP flux mmol/s 1990: ',major_potw_fluxp[t_1990,3])
#
#print('HTP TOC flux mmol/s 1990: ',major_potw_fluxc[t_1990,0])
#print('JWP TOC flux mmol/s 1990: ',major_potw_fluxc[t_1990,1])
#print('OCS TOC flux mmol/s 1990: ',major_potw_fluxc[t_1990,2])
#print('PLW TOC flux mmol/s 1990: ',major_potw_fluxc[t_1990,3])
#
#print('HTP flow m3/s 2000: ',major_flo[t_2000,0,0])
#print('JWP flow m3/s 2000: ',major_flo[t_2000,1,1])
#print('OCS flow m3/s 2000: ',major_flo[t_2000,2,2])
#print('PLW flow m3/s 2000: ',major_flo[t_2000,3,3])
#
#print('HTP TN flux mmol/s 2000: ',major_potw_fluxn[t_2000,0])
#print('JWP TN flux mmol/s 2000: ',major_potw_fluxn[t_2000,1])
#print('OCS TN flux mmol/s 2000: ',major_potw_fluxn[t_2000,2])
#print('PLW TN flux mmol/s 2000: ',major_potw_fluxn[t_2000,3])
#
#print('HTP TP flux mmol/s 2000: ',major_potw_fluxp[t_2000,0])
#print('JWP TP flux mmol/s 2000: ',major_potw_fluxp[t_2000,1])
#print('OCS TP flux mmol/s 2000: ',major_potw_fluxp[t_2000,2])
#print('PLW TP flux mmol/s 2000: ',major_potw_fluxp[t_2000,3])
#
#print('HTP TOC flux mmol/s 2000: ',major_potw_fluxc[t_2000,0])
#print('JWP TOC flux mmol/s 2000: ',major_potw_fluxc[t_2000,1])
#print('OCS TOC flux mmol/s 2000: ',major_potw_fluxc[t_2000,2])
#print('PLW TOC flux mmol/s 2000: ',major_potw_fluxc[t_2000,3])
#
#
#print('HTP flow m3/s 2010: ',major_flo[t_2010,0,0])
#print('JWP flow m3/s 2010: ',major_flo[t_2010,1,1])
#print('OCS flow m3/s 2010: ',major_flo[t_2010,2,2])
#print('PLW flow m3/s 2010: ',major_flo[t_2010,3,3])
#
#print('HTP TN flux mmol/s 2010: ',major_potw_fluxn[t_2010,0])
#print('JWP TN flux mmol/s 2010: ',major_potw_fluxn[t_2010,1])
#print('OCS TN flux mmol/s 2010: ',major_potw_fluxn[t_2010,2])
#print('PLW TN flux mmol/s 2010: ',major_potw_fluxn[t_2010,3])
#
#print('HTP TP flux mmol/s 2010: ',major_potw_fluxp[t_2010,0])
#print('JWP TP flux mmol/s 2010: ',major_potw_fluxp[t_2010,1])
#print('OCS TP flux mmol/s 2010: ',major_potw_fluxp[t_2010,2])
#print('PLW TP flux mmol/s 2010: ',major_potw_fluxp[t_2010,3])
#
#print('HTP TOC flux mmol/s 2010: ',major_potw_fluxc[t_2010,0])
#print('JWP TOC flux mmol/s 2010: ',major_potw_fluxc[t_2010,1])
#print('OCS TOC flux mmol/s 2010: ',major_potw_fluxc[t_2010,2])
#print('PLW TOC flux mmol/s 2010: ',major_potw_fluxc[t_2010,3])
