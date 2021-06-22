# make 3d output of pH, omega aragonite, and pCO2
import os
import sys
from netCDF4 import Dataset,num2date
import numpy as np
import PyCO2SYS as pyco2

# choose years and months
start_year = 2017
end_year = 2017

start_month = 1
end_month = 12

dtunit = 'days since '+str(start_year)+'-'+'%02d'%start_month+'-01'

# read in model output
outpath = '/data/project6/ROMS/USSW1/daily/'
# path to save co2sys output
savepath = '/data/project1/minnaho/decapods/co2sys_output/'

model_name = 'ussw1_avg.'

# parameters
par1type =  1 # first input parameter - Alk
par2type = 2 # second input parameter - 2 for DIC, 3 for pH
pHscale = 2 # sea water scale
k1k2c = 14 # Millero et al, 2010 sea water scale
kso4c = 1 # bisulfate ion dissociation Dickson (1990) J. Chem. Thermodyn.
kbors = 1 # boron:salt relationship Uppstrom 1979

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

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
        for d_i in list(range(1,ndays+1)):
            year_month = 'Y'+str(y_i)+'M'+'%02d'%m_i+'D'+'%02d'%d_i
            print(year_month)
            datanc = Dataset(outpath+model_name+year_month+'.nc','r')
            # get values from model
            rhonc = np.squeeze(datanc.variables['rho'])+1027.4
            alknc = np.squeeze(datanc.variables['Alk'])
            dicnc = np.squeeze(datanc.variables['DIC'])
            salnc = np.squeeze(datanc.variables['salt'])
            temnc = np.squeeze(datanc.variables['temp'])
            silnc = np.squeeze(datanc.variables['SiO3'])
            po4nc = np.squeeze(datanc.variables['PO4'])

            rhonc[rhonc>1E10] = np.nan
            alknc[alknc>1E10] = np.nan
            dicnc[dicnc>1E10] = np.nan
            salnc[salnc>1E10] = np.nan
            temnc[temnc>1E10] = np.nan
            silnc[silnc>1E10] = np.nan
            po4nc[po4nc>1E10] = np.nan

            # convert from mmol/m3 to umol/kg
            alknc = alknc/(rhonc*0.001)
            dicnc = dicnc/(rhonc*0.001)
            silnc = silnc/(rhonc*0.001)
            po4nc = po4nc/(rhonc*0.001)

            # run co2sys
            co2dict = pyco2.sys(
                par1=alknc,
                par2=dicnc,
                par1_type=par1type,
                par2_type=par2type,
                salinity=salnc,
                temperature=temnc,
                total_silicate=silnc,
                total_phosphate=po4nc,
                opt_pH_scale=pHscale,
                opt_k_carbonic=k1k2c,
                opt_k_bisulfate=kso4c,
                opt_total_borate=kbors)

            # output
            pH = co2dict['pH_total']
            pco2 = co2dict['pCO2']
            omega = co2dict['saturation_aragonite']
            
            del co2dict
            
            # write to nc file
            ncfile = Dataset(savepath+model_name+year_month+'_co2sys.nc','w')
            ncfile.createDimension('s_rho',alknc.shape[0])
            ncfile.createDimension('eta_rho',alknc.shape[1])
            ncfile.createDimension('xi_rho',alknc.shape[2])

            phh_var = ncfile.createVariable('pH','float64',('s_rho','eta_rho','xi_rho'))
            pco_var = ncfile.createVariable('pCO2','float64',('s_rho','eta_rho','xi_rho'))
            omm_var = ncfile.createVariable('omega','float64',('s_rho','eta_rho','xi_rho'))
            
            pco_var.unit = 'uatm' 
            
            phh_var[:,:,:] = pH
            pco_var[:,:,:] = pco2
            omm_var[:,:,:] = omega

            ncfile.close()
    
            del alknc
            del dicnc
            del salnc
            del temnc
            del silnc
            del po4nc
            del pH
            del pco2
            del omega

