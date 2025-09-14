%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% make_s2r_BGC
%
% This script interpolates the BGC fields from different sources
% Onto a ROMS domains. It is further used to produce the initial 
% conditions of a run, or for validation of the solution 
%
% Pierre DAMIEN, inspired from Jeroen Molemaker, UCLA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% checks and verifications needed : 
% 1 - density interpolation (salinity, temperature pot, or not), ...
%            maybe better to use mean temperature of bgcname for monthly interp instead of glodap temp and salt
%            Need to compare density in woa to density in glodap
% 2 - To add, CHL interpolation based on surface CHL from obs + vertical profile based on lee

clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
    romsdir    = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/';
    grdname    = [romsdir 'FORCINGS/atlmed_grd.nc'];
    outname    = [romsdir 'BGC/atlmed_bgc'];
    bgctime    = 12 ; % 1 for climato, 12 for seasonal 
    pars.theta_s = 6.0;
    pars.theta_b = 6.0;
    pars.hc     = 250.0;
    pars.N      = 100  ; 
    pars.scoord = 'new2012';    % child 'new' or 'old' type scoord
    BGCparam.Ntrc = 11 ;        % Number of 3d tracers to interpolate  
    BGCparam.coefs_dir = 'Coefs_atlmed12' ; %'Coefs_pacmed' ;      
%--   interpolation routine defined by BGCparam.interp 
%--   BGCparam.interp==1 : WOA18 seasonal  
%--   BGCparam.interp==2 : Iron seasonal from Huang et al., 2022 
%--   BGCparam.interp==3 : GLODAPv2.2016b, data from the years 1972-2013 and normalized to 2002 
%--   BGCparam.interp==4 : N2O seasonal from machine learning product, see Yang et al., 2020
%--   BGCparam.interp==5 : Mercator GLORYS2V4 hincast seasonal
% ------ Temperature 
    BGCparam.name_vars{1} = 'temp' ;
    BGCparam.long_name{1} = 'potential temperature' ;
    BGCparam.units{1} = 'degree Celsius' ;
    BGCparam.file_vars{1} = '/data/project7/pdamien/DATA/BGC/WOA18/temp/woa18_decav_t*_04.nc' ;  
    BGCparam.interp(1)=1 ; 
% ------ Salinity 
    BGCparam.name_vars{2} = 'salt' ;
    BGCparam.long_name{2} = 'salinity' ;
    BGCparam.units{2} = 'PSU' ;
    BGCparam.file_vars{2} = '/data/project7/pdamien/DATA/BGC/WOA18/salt/woa18_decav_s*_04.nc' ;
    BGCparam.interp(2)=1 ;
% ------ Nitrate  
    BGCparam.name_vars{3} = 'NO3' ;
    BGCparam.long_name{3} = 'nitrate' ;
    BGCparam.units{3} = 'mMol N m-3' ;    
    BGCparam.file_vars{3} = '/data/project7/pdamien/DATA/BGC/WOA18/nitr/woa18_all_n*_01.nc' ;
    BGCparam.interp(3)=1 ;
% ------ Phosphate
    BGCparam.name_vars{4} = 'PO4' ;
    BGCparam.long_name{4} = 'Phosphate' ;
    BGCparam.units{4} = 'mMol P m-3' ;
    BGCparam.file_vars{4} = '/data/project7/pdamien/DATA/BGC/WOA18/phos/woa18_all_p*_01.nc' ;
    BGCparam.interp(4)=1 ;
% ------ Silicate 
    BGCparam.name_vars{5} = 'SiO3' ;
    BGCparam.long_name{5} = 'Silicate' ;
    BGCparam.units{5} = 'mMol Si m-3' ;
    BGCparam.file_vars{5} = '/data/project7/pdamien/DATA/BGC/WOA18/silc/woa18_all_i*_01.nc' ;
    BGCparam.interp(5)=1 ;
% ------ Oxygen
    BGCparam.name_vars{6} = 'O2' ;
    BGCparam.long_name{6} = 'Oxygen' ;
    BGCparam.units{6} = 'mMol O2 m-3' ;
    BGCparam.file_vars{6} = '/data/project7/pdamien/DATA/BGC/WOA18/oxyg/woa18_all_o*_01.nc' ;
    BGCparam.interp(6)=1 ;
% ------ Iron
    BGCparam.name_vars{7} = 'Fe' ;
    BGCparam.long_name{7} = 'Iron' ;
    BGCparam.units{7} = 'mMol Fe m-3' ;
    BGCparam.file_vars{7} = '/data/project7/pdamien/DATA/BGC/MappedIron/Monthly_dFe.nc' ;
    BGCparam.interp(7)=2 ;
% ------ DIC
    BGCparam.name_vars{8} = 'DIC' ;
    BGCparam.long_name{8} = 'Dissolved Inorganic Carbon' ;
    BGCparam.units{8} = 'mMol C m-3' ;
    BGCparam.file_vars{8} = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/GLODAPv2.2016b.TCO2.nc' ;
    BGCparam.interp(8)=3 ;
% ------ Alk
    BGCparam.name_vars{9} = 'Alk' ;
    BGCparam.long_name{9} = 'Alkalinity' ;
    BGCparam.units{9} = 'mMol C m-3' ;
    BGCparam.file_vars{9} = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/GLODAPv2.2016b.TAlk.nc' ;
    BGCparam.interp(9)=3 ;
% ------ N2O
    BGCparam.name_vars{10} = 'N2O' ;
    BGCparam.long_name{10} = 'Nitrous oxyde' ;
    BGCparam.units{10} = 'mMol N m-3' ;
    BGCparam.file_vars{10} = '/data/project7/pdamien/DATA/BGC/Ncycle/n2ofromnn.nc' ;
    BGCparam.interp(10)=4 ;
% ------ CHL
    BGCparam.name_vars{11} = 'CHL' ;
    BGCparam.long_name{11} = 'Total Chlorophyl' ;
    BGCparam.units{11} = 'mg Chl m-3' ;
    BGCparam.file_vars{11} = '/data/project7/pdamien/DATA/BGC/GLORYS2V4/glorys2v4_mean_2000-2020.nc' ;
    BGCparam.interp(11)=5 ;
% -----  AirSea flx (pCo2, Iron, dust) 
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%

 %%% create a folder to store the interpolation coeficients (computed once)
if ~exist(BGCparam.coefs_dir)
   mkdir(BGCparam.coefs_dir)
end

 %%% read the grid for interpolation
grd.lon = ncread(grdname,'lon_rho')';
grd.lat = ncread(grdname,'lat_rho')';
grd.h   = ncread(grdname,'h')';
grd.zr  = zlevs4(grd.h,grd.h*0,pars.theta_s,pars.theta_b,pars.hc,pars.N,'r',pars.scoord);
[grd.ny,grd.nx] = size(grd.h);
grd.nz = pars.N ;

for t=1:bgctime

 %%% Get file name and create netcdf file
if bgctime==1
   bgcname = [outname '_00.nc'] ; 
elseif bgctime==12
   bgcname  = [outname '_' num2str(t, '%2.2d') '.nc'] ;
else
   disp('ERROR : bgctime has to be 1 or 12')
   error
end
if ~exist(bgcname,'file')
   create_bgc_file(grdname,bgcname,bgctime,pars,BGCparam,t)
end

 %%% Loop over tracers, 3d interpolation, write in file
for n=1:BGCparam.Ntrc
    disp(' **** ') 
    disp(['Working on trc : ' num2str(n) '/' num2str(BGCparam.Ntrc) ' , ' BGCparam.long_name{n}])
    if BGCparam.interp(n)==1
       disp('      Interpolation of seasonal WOA18; check in get_frc_woa18s for spec & options')
       var = get_frc_WOA18s(grd,BGCparam,n,t,bgctime);
       ncwrite(bgcname,BGCparam.name_vars{n},var,[1 1 1 1]);
    elseif BGCparam.interp(n)==2
       disp('      Interpolation of seasonal Iron from Huang et al., 2022; check in get_frc_IRONs for spec & options')
       var = get_frc_IRONs(grd,BGCparam,n,t,bgctime);
       ncwrite(bgcname,BGCparam.name_vars{n},var,[1 1 1 1]);
    elseif BGCparam.interp(n)==3
       disp('      Interpolation of mean GLODAP; check in get_frc_GLODAP for spec & options')
       var = get_frc_GLODAP(grd,BGCparam,n,t,bgctime,bgcname);
       ncwrite(bgcname,BGCparam.name_vars{n},var,[1 1 1 1]);
    elseif BGCparam.interp(n)==4
       disp('      Interpolation of seasonal N2O from Yang et al., 2020; check in get_frc_N2Os for spec & options')
       var = get_frc_N2Os(grd,BGCparam,n,t,bgctime);
       ncwrite(bgcname,BGCparam.name_vars{n},var,[1 1 1 1]);
    elseif BGCparam.interp(n)==5
       disp('      Interpolation of seasonal GLORYS reanalysis; check in get_frc_GLORYSs for spec & options')
       var = get_frc_GLORYSs(grd,BGCparam,n,t,bgctime);
       ncwrite(bgcname,BGCparam.name_vars{n},var,[1 1 1 1]);
    else
       disp(['ERROR : option ' num2str(BGCparam.interp(n)) ' unavailable for interpolation'])
       return
    end
end

end
