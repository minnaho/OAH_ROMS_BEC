##################################
# Prepare roms_YyyyyMmm.in
# for OPC wastewater runs
# Minna Ho, UCLA, Feb 2018 
##################################


#########################################
# CHANGE THESE INPUTS TO CHANGE NAME AND
# CONTENTS OF .in FILE 
#########################################
model = 'L2_SCB'
#model_atm = 'L2_SCB'
model_atm = 'l2_scb'
model_file = 'l2_scb'
start_year = 1999
end_year = 1999

# between 1 and 12
start_month = 1
end_month = 11

# model time step (seconds)
dt = 30
NDTFAST= 50
NINFO = 1

######################
# PATHS
######################
'''
model = 'L2_SCB'
project_path = '/data/project1/minnaho/model_conf/'
scratch_path_local = '/data/project1/minnaho/model_conf/'
scratch_path = '/data/project1/minnaho/model_conf/'
'''

model_scenario = 'ww1_inlandpotw'

savepath = './wastewater_scenarios/'+model_scenario+'/'

# paths written in .in file
other_files = 'Other_files/'
RST_path = 'RST_'+model_scenario+'/'
Atm_forcing_path = 'Atm_forcing/'
INPUTS = 'INPUTS/'
ocean_files = 'Ocean_files9799/'

# psource
psource = 'roms_psource_'+model_scenario+'.nc'

########################
# netcdf files called in
# in file
########################
BRYFILE  = 'roms_bry'
RSTFILE  = 'roms_rst'
pCO2_atm = 'pco2_1994-2011.nc'

grid_file = 'roms_grd.nc'

# forcing
strname = 'STRNAME'
surfname = 'SURFNAME'

# bulk_forcing
tide     = 'roms_tide.nc'
atm_wind = model_atm+'_wnd_'
atm_tra  = model_atm+'_tra_'
atm_rad  = model_atm+'_rad_'
atm_prec = model_atm+'_prec_'
frc      = 'roms_frc.nc'
atmdep   = 'roms_atmdep.nc'
anthpco2 = 'roms_anthpco2.nc'
#anthpco2 = 'roms_anthpco2_end.nc' # test for Expanse
#dust     = 'roms_dust.nc'

# OUTFILES
HISFILE     = model_file+'_his.nc'
AVGFILE     = model_file+'_avg.nc'
AVGBIOFILE  = model_file+'_avg_bio.nc'
BULKHISNAME = model_file+'_bdiags_his.nc'
BULKAVGNAME = model_file+'_bdiags_avg.nc'
AVGPHYSNAME = model_file+'_phys_flux.nc'

bgc_flux_his = model_file+'_bgc_flux_his.nc'
bgc_flux_avg = model_file+'_bgc_flux_avg.nc'

phys_flux_his = model_file+'_phys_flux_his.nc'

#####################################################
# other variables (unsure where to get these values)
#####################################################
theta_s = '6.d0'
theta_b = '3.d0'
hc = '250.d0'
NRREC ='2'
NRPFRST = '+2'
LDEFHHIS = 'F'
NRPFHIS = '1'
NTSAVG = '1'
NRPFAVG = '1'

# auxiliary history fields
rho_h = 'T'
Omega_h = 'T'
W_h = 'T'
Akv_h = 'T'
Akt_h = 'T'
Aks_h = 'T'
HBL_h = 'T'
HBBL_h = 'T'

# auxiliary averages
rho_a = 'T'
Omega_a = 'T'
W_a = 'T'
Akv_a = 'T'
Akt_a = 'T'
Aks_a = 'T'
HBL_a = 'T'
HBBL_a = 'T'

# bgc flux histories, same as phys flux histories
newfile = 'T'
nwrt = '3600000'
nrpfhis = '1'

rho0 = '1027.4'

lateral_visc = '0.'

# bottom drag
RDRG = '3.0E-4'
RDRG2 = '0.'
zob = '0.01'

gamma2 = '1.'

v_sponge = '5.'

# nudg cof
TauM2_in = '0.1'
TauM2_out = '180.'
attnM2 = '0.005'
TauM3_in = '1.'
TauM3_out = '100.'
TauT_in = '3.'
TauT_out = '360.'

# bulk diags histories
newfile_bd = 'F'
nwrt_bd = '999999999'
nrpfhis_bd = '1'
twenty_T = '20*T'

# bulk diags averages
newfile_bda = 'T'
ntsavg_bda = '1'
nrpfavg_bda = '1'


##############################
# CALCULATE NTIMES FROM 
# DAYS IN EACH MONTH
# AND WRITE FILE
##############################
months = list(range(1,13))
months_with_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

for y in range(start_year,end_year+1):
    # if we are on the first year, starts at s_m
    if y == start_year:
        s_m = start_month 
    else:
        s_m = 1
    # if we are on the last year, end at e_m
    if y == end_year:
        e_m = end_month+1
    else: 
        e_m = 13
    for m in range(s_m,e_m): 
        if m in months_with_31_days:
            ndays = 31
        if m not in months_with_31_days:
            ndays = 30
            if m == 2 and y in leap_years:
                ndays = 29
            if m == 2 and y not in leap_years: 
                ndays = 28
        ntimes = int((86400./dt)*ndays)
        daytimes = int(86400./dt)

        # if month is 1, old file is month 12 and year y-1
        if m == 1: 
            file_name_old = 'roms_Y'+str(y-1)+'M'+'%02d'%months[m-2]+'.in' # gets previous month (if month is 1, gets 12) 
            year_month_old = 'Y'+str(y-1)+'M'+'%02d'%months[m-2]
        else: 
            file_name_old = 'roms_Y'+str(y)+'M'+'%02d'%months[m-2]+'.in' 
            year_month_old = 'Y'+str(y)+'M'+'%02d'%months[m-2]

        file_name = 'roms_Y'+str(y)+'M'+'%02d'%m+'.in'
        year_month = 'Y'+str(y)+'M'+'%02d'%m

        # begin writing .in file
        f = open(savepath+file_name,'w')
        f.write('title:\n')
        f.write('    '+model+' [forced by WRF6]\n\n')

        f.write('time_stepping: NTIMES   dt[sec]  NDTFAST  NINFO\n')
        f.write('               '+str(ntimes)+'   '+str(dt)+'      '+str(NDTFAST)+'   '+str(NINFO)+'\n\n')

        f.write('S-coord: THETA_S, THETA_B,   hc (m)\n')
        f.write('           '+theta_s+'   '+theta_b+'     '+hc+'\n\n')

        f.write('grid: filename\n')
        f.write('           '+other_files+grid_file+'\n\n')

        f.write('initial: NRREC / filename\n')
        f.write('           '+NRREC+'\n')
        f.write('             '+RST_path+RSTFILE+'_'+year_month_old+'.nc\n\n')

        f.write('bulk_forcing: filename\n')
        f.write('              '+other_files+tide+'\n')
        f.write('              '+Atm_forcing_path+atm_wind+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_tra+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_rad+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_prec+year_month+'.nc\n') 
        f.write('              '+other_files+frc+'\n')
        f.write('              '+other_files+atmdep+'\n')
        f.write('              '+other_files+anthpco2+'\n')

        f.write('forcing: filename\n')
        f.write('              '+INPUTS+strname+'\n') 
        f.write('              '+INPUTS+surfname+'\n\n')

        f.write('boundary: filename\n')
        f.write('              '+ocean_files+BRYFILE+'.nc\n\n')

        f.write('restart:          NRST, NRPFRST / filename\n')
        f.write('               '+str(ntimes)+'    '+NRPFRST+'\n')
        f.write('              '+RST_path+RSTFILE+'_'+year_month+'.nc\n\n') 

        f.write('history: LDEFHIS, NWRT, NRPFHIS / filename\n')
        f.write('             '+LDEFHHIS+'    '+str(ntimes)+'   '+NRPFHIS+'\n')
        f.write('              '+'AVG_'+year_month+'/'+HISFILE+'\n\n')

        f.write('averages: NTSAVG, NAVG, NRPFAVG / filename\n')
        f.write('            '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        f.write('              '+'AVG_'+year_month+'/'+AVGFILE+'\n\n')

        # unsure where these values come from, hard coded
        f.write('primary_history_fields: zeta U,VBAR  U,V   wrtT(1:NT)\n')
        f.write('            3*T  2*T  2*T 5*T 4*T 2*T T 3*T 3*T 7*T 33*F\n\n')

        f.write('auxiliary_history_fields: rho Omega W  Akv Akt Aks  HBL HBBL\n')
        f.write('                           '+rho_h+'   '+Omega_h+'    '+W_h+'   '+Akv_h+'   '+Akt_h+'   '+Aks_h+'    '+HBL_h+'   '+HBBL_h+'\n\n')

        f.write('primary_averages: zeta U,VBAR  U,V   wrtT(1:NT)\n')
        # hard coded
        f.write('      60*T\n\n')

        f.write('auxiliary_averages: rho Omega W  Akv Akt Aks  HBL HBBL\n')
        f.write('                     '+rho_a+'    '+Omega_a+'   '+W_a+'   '+Akv_a+'   '+Akt_a+'   '+Aks_a+'    '+HBL_a+'   '+HBBL_a+'\n\n')

        f.write('averages_bio: NTSAVG, NAVG, NRPFAVG / filename\n')
        f.write('           '+NTSAVG+'     '+str(daytimes)+'     '+NRPFAVG+'\n')
        f.write('                  AVG_'+year_month+'/'+AVGBIOFILE+'\n\n')

        f.write('bgc_flux_histories: newfile, nwrt, nrpfhis / filename\n')
        f.write('                      '+newfile+'      '+nwrt+'     '+nrpfhis+'\n')
        f.write('                          '+bgc_flux_his+'\n\n')
        
        f.write('bgc_flux_averages: newfile, ntsavg, navg, nrpfavg / filename\n')
        # save every day
        #f.write('            '+newfile+'   '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        # save every month
        f.write('            '+newfile+'   '+NTSAVG+'   '+str(ntimes)+'    '+NRPFAVG+'\n')
        f.write('              AVG_'+year_month+'/'+bgc_flux_avg+'\n\n')

        f.write('phys_flux_histories: newfile, nwrt, nrpfhis / filename\n')
        f.write('                      '+newfile+'      '+nwrt+'     '+nrpfhis+'\n') 
        f.write('                          '+phys_flux_his+'\n\n')

        f.write('phys_flux_averages: newfile, ntsavg, navg, nrpfavg / filename / PFA_by_tracer\n')
        # save every day
        #f.write('            '+newfile+'   '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        # save every month
        f.write('            '+newfile+'   '+NTSAVG+'   '+str(ntimes)+'    '+NRPFAVG+'\n')
        f.write('              AVG_'+year_month+'/'+AVGPHYSNAME+'\n')
        # hard coded
        f.write('              2*T F T F T F 5*T 2*F T F T 3*F T 2*F T 5*F\n\n')

        f.write('rho0:\n')
        f.write('     '+rho0+'\n\n')

        f.write('lateral_visc:   VISC2[m^2/sec]\n')
        f.write('                 '+lateral_visc+'\n\n')

        f.write('tracer_diff2: TNU2(1:NT)           [m^2/sec for all]\n')
        # hard coded
        f.write(' 0. 0. 0. 0. 0. 0. 0. 0. 0. 33*0.\n\n')

        f.write('bottom_drag:  RDRG[m/s],  RDRG2,  Zob[m]\n')
        f.write('               '+RDRG+'       '+RDRG2+'     '+zob+'\n\n')

        f.write('gamma2:\n')
        f.write('                 '+gamma2+'\n\n')

        f.write('v_sponge:           V_SPONGE [m^2/sec]\n')
        f.write('                   '+v_sponge+'\n\n')
  
        f.write('nudg_cof: TauM2_in/out  attnM2   TauM3_in/out  TauT_in/out [days for all]\n')
        f.write('              '+TauM2_in+'  '+TauM2_out+'   '+attnM2+'      '+TauM3_in+' '+TauM3_out+'      '+TauT_in+'  '+TauT_out+'\n\n')

        f.write('bulk_diags_histories: newfile, nwrt, nrpfhis / filename\n')
        f.write('                       '+newfile_bd+'     '+nwrt_bd+'   '+nrpfhis_bd+'\n')
        f.write('                   AVG_'+year_month+'/'+BULKHISNAME+'\n')
        f.write('                   '+twenty_T+'\n\n')

        f.write('bulk_diags_averages: newfile, ntsavg, navg,nrpfavg / filename\n')
        f.write('                       '+newfile_bda+'    '+ntsavg_bda+'       '+str(daytimes)+'   '+nrpfavg_bda+'\n')
        f.write('                   AVG_'+year_month+'/'+BULKAVGNAME+'\n')
        f.write('                    '+twenty_T+'\n\n')

        f.write('pCO2_atm_file:\n')
        f.write('         '+other_files+pCO2_atm+'\n')

        f.write('point_source:\n')
        f.write('         '+other_files+psource+'\n')

        f.close()
        print('Input file formed: '+file_name)







