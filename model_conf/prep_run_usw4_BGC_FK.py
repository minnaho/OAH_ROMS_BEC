##################################
# Prepare roms_YyyyyMmm.in
# for usw42 biogeochemical model
# Minna Ho, UCLA, Feb 2018 
##################################


#########################################
# CHANGE THESE INPUTS TO CHANGE NAME AND
# CONTENTS OF .in FILE 
#########################################
model = 'USW4'
model_file = 'usw42'
start_year = 1996
end_year = 2016

# between 1 and 12
start_month = 1
end_month = 12

# model time step (seconds)
dt = 240
NDTFAST= 77
NINFO = 1

######################
# PATHS
######################
'''
model = 'usw42'
project_path = '/data/project1/minnaho/model_conf/'
scratch_path_local = '/data/project1/minnaho/model_conf/'
scratch_path = '/data/project1/minnaho/model_conf/'
'''

# paths written in .in file
other_files = 'Other_files/'
RST_path = 'RST/'
Atm_forcing_path = 'Atm_forcing/'
INPUTS = 'INPUTS/'
ocean_files = 'Ocean_files/'

########################
# netcdf files called in
# in file
########################
GRDFILE  = model_file+'_grd'
SSSFILE  = model_file+'_frc'
DUSTFILE = model_file+'_dust'
WNDFILE  = model_file+'_wnd'
TRAFILE  = model_file+'_tra'
RADFILE  = model_file+'_rad'
PRECFILE = model_file+'_prec'
BRYFILE  = model_file+'_bryV1'
RSTFILE  = model_file+'_rst'
pCO2_atm = 'pco2_1994-2011.nc'

grid_file = model_file+'_grd.nc'

# forcing
strname = 'STRNAME'
surfname = 'SURFNAME'

# bulk_forcing
atm_wind = model_file+'_wnd_'
atm_tra  = model_file+'_tra_'
atm_rad  = model_file+'_rad_'
atm_prec = model_file+'_prec_'
frc      = 'usw1_frc.nc'
dust     = model_file+'_dust.nc'

# OUTFILES
HISFILE     = model_file+'_his.nc'
HISBIOFILE  = model_file+'_his_BIO.nc'
AVGFILE     = model_file+'_avg.nc'
#AVGBIOFILE  = 'usw42_avg_BIO.nc'
AVGBIOFILE  = model_file+'_avg_bio.nc'
BULKHISNAME = model_file+'_bdiags_his.nc'
BULKAVGNAME = model_file+'_bdiags_avg.nc'
HISDIAG     = model_file+'_eddy_his.nc'
AVGDIAG     = model_file+'_eddy_avg.nc'
AVGPHYSNAME = model_file+'_phys_flux.nc'

bgc_flux_his = 'uswc4_bgc_flux_his.nc'
bgc_flux_avg = 'uswc4_bgc_flux_avg.nc'

phys_flux_his = model_file+'_phys_flux_his.nc'

#####################################################
# other variables (unsure where to get these values)
#####################################################
theta_s = '6.d0'
theta_b = '3.d0'
hc = '250.d0'
NRREC ='1'
NRPFRST = '+2'
LDEFHHIS = 'F'
NRPFHIS = '1'
NTSAVG = '1'
NRPFAVG = '1'

# auxiliary history fields
rho_h = 'F'
Omega_h = 'F'
W_h = 'T'
Akv_h = 'T'
Akt_h = 'T'
Aks_h = 'F'
HBL_h = 'T'
HBBL_h = 'F'

# auxiliary averages
rho_a = 'T'
Omega_a = 'F'
W_a = 'T'
Akv_a = 'T'
Akt_a = 'T'
Aks_a = 'F'
HBL_a = 'T'
HBBL_a = 'F'

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

v_sponge = '400.'

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
navg_bda = '360'
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
        ntimes = (86400 / dt) * ndays
	daytimes = 86400 / dt

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
        f = open(file_name,'w')
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
        f.write('              '+Atm_forcing_path+atm_wind+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_tra+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_rad+year_month+'.nc\n')
        f.write('              '+Atm_forcing_path+atm_prec+year_month+'.nc\n') 
        f.write('              '+other_files+frc+'\n')
        f.write('              '+other_files+dust+'\n\n')

        f.write('forcing: filename\n')
        f.write('              '+INPUTS+strname+'\n') 
        f.write('              '+INPUTS+surfname+'\n\n')

        f.write('boundary: filename\n')
        f.write('              '+ocean_files+BRYFILE+'.nc\n\n')

        f.write('restart:          NRST, NRPFRST / filename\n')
        f.write('               '+str(ntimes)+'    '+NRPFRST+'\n')
        f.write('              '+RST_path+RSTFILE+year_month+'.nc\n\n') 

        f.write('history: LDEFHIS, NWRT, NRPFHIS / filename\n')
        f.write('             '+LDEFHHIS+'    '+str(ntimes)+'   '+NRPFHIS+'\n')
        f.write('              '+'AVG_'+year_month+'/'+HISFILE+'\n\n')

	f.write('averages: NTSAVG, NAVG, NRPFAVG / filename\n')
        f.write('            '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        f.write('              '+'AVG_'+year_month+'/'+AVGFILE+'\n\n')

        # unsure where these values come from, hard coded
        f.write('primary_history_fields: zeta U,VBAR  U,V   wrtT(1:NT)\n')
        f.write('      3*T  2*T  2*T 5*T 4*F 2*T F 3*T 3*F 2*T 33*F\n\n')

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
        f.write('            '+newfile+'   '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        f.write('              AVG_'+year_month+'/'+bgc_flux_avg+'\n\n')

        f.write('phys_flux_histories: newfile, nwrt, nrpfhis / filename\n')
        f.write('                      '+newfile+'      '+nwrt+'     '+nrpfhis+'\n') 
        f.write('                          '+phys_flux_his+'\n\n')

        f.write('phys_flux_averages: newfile, ntsavg, navg, nrpfavg / filename / PFA_by_tracer\n')
        f.write('            '+newfile+'   '+NTSAVG+'   '+str(daytimes)+'    '+NRPFAVG+'\n')
        f.write('              AVG_'+year_month+'/'+AVGPHYSNAME+'\n')
        # hard coded
        f.write('           2*T F T F T F 2*T F 2*T 2*F T F T 3*F T 2*F T 5*F\n\n')

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

        f.close()
        print('Input file formed: '+file_name)







