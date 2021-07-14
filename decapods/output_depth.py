# make 3d output of pH, omega aragonite, and pCO2
import os
import sys
sys.path.append('/data/project3/minnaho/global/')
import l1grid as l1grid
import ROMS_depths as depths
from netCDF4 import Dataset,num2date
import numpy as np
import PyCO2SYS as pyco2
import seawater as sw

# choose years and months
start_year = 2016
end_year = 2016

start_month = 1
end_month = 12

dtunit = 'days since '+str(start_year)+'-'+'%02d'%start_month+'-01'

grid_nc = l1grid.grid_nc

# read in model output
outpath = '/data/project6/ROMS/USSW1/daily/'
# path to save co2sys output
savepath = '/data/project6/minnaho/bio_interp/co2sys_output/'

model_name = 'ussw1_avg.'

# parameters
par1type =  1 # first input parameter - Alk
par2type = 2 # second input parameter - 2 for DIC, 3 for pH
pHscale = 1 # 1 = total pH, 2 = sea water scale
k1k2c = 14 # Millero et al, 2010 sea water scale
kso4c = 1 # bisulfate ion dissociation Dickson (1990) J. Chem. Thermodyn.
kbors = 1 # boron:salt relationship Uppstrom 1979

lat_sw = 35

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

gst = 350

# define these so don't have to calculate
shpeta = 1410
shpxi = 770

for y_i in range(start_year,end_year+1):
    # if we are on the first year, starts at s_m
    if y_i == start_year:
        s_m = start_month
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y_i == end_year:
        e_m = end_month+1
    else:
        e_m = 13
    for m_i in range(s_m,e_m):
        if m_i in months_w_31_days:
            ndays = 31
        if m_i not in months_w_31_days:
            ndays = 30
            if m_i == 2 and y_i in leap_years:
                ndays = 29
            if m_i == 2 and y_i not in leap_years:
                ndays = 28 
        # set days if stops in middle of one month
        #if m_i == 1 and y_i == 2017:
        #    stday = 3
        #else:
        #    stday = 1
        stday = 1
        for d_i in list(range(stday,ndays+1)):
            year_month = 'Y'+str(y_i)+'M'+'%02d'%m_i+'D'+'%02d'%d_i
            print(year_month)
            datanc = Dataset(outpath+model_name+year_month+'.nc','r')
            # get values from model
            z_r = depths.get_zr_tind(datanc,grid_nc,0,[0,shpeta,gst,shpxi])
            z_r[z_r>1E10] = np.nan

            # write to nc file
            ncfile = Dataset(savepath+model_name+year_month+'_depth.nc','w')
            ncfile.createDimension('s_rho',z_r.shape[0])
            ncfile.createDimension('eta_rho',z_r.shape[1])
            ncfile.createDimension('xi_rho',z_r.shape[2])
            dep_var = ncfile.createVariable('depth','float64',('s_rho','eta_rho','xi_rho'))
            dep_var.unit = 'm'
            dep_var[:,:,:] = z_r

            ncfile.close()
