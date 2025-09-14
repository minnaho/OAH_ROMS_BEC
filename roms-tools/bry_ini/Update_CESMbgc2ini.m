%---------------------------------------------------------------------------------------
%
% Add_bgc2ini
%
% - Add BGC fields 
% - Interpolate the BGC fields onto the initial file
% - Require to run first Make_BGCfrc/make_s2r_bgc.m. It interpolates BGC variables from 
%   a collection of sources onto the grid. Here, only the interpolation in time and 
%   density is done
%   
%---------------------------------------------------------------------------------------
clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
%
grdname = '/data/project8/pdamien/ROMS_outputs/PACMED12KMnew/FORCINGS/pacmed12_grd.nc' ;
ininame = '/data/project8/pdamien/ROMS_outputs/PACMED12KMnew/FORCINGS/pacmed12_ini20000101.nc' ;
time_ref = datenum(1995,1,1) ; % reference time for ROMS
%
% CASE 2 : vars derived from CHL 
BGCname2_vars       = {'SPC' 'SPCHL' 'SPFE' 'SPCACO3' 'DIATC' 'DIATCHL' 'DIATFE' 'DIATSI' 'DIAZC' 'DIAZCHL' 'DIAZFE' 'ZOOC'} ;
BGCname2_vars_marbl = {'spC' 'spChl' 'spFe' 'spCaCO3' 'diatC' 'diatChl' 'diatFe' 'diatSi' 'diazC' 'diazChl' 'diazFe' 'zooC'} ;
% CASE 3 : vars derived mean value
BGCname3_vars       = {'DON' 'DONR' 'DOP' 'DOPR' 'NH4' 'DOC'} ;
BGCname3_vars_marbl = {'DON' 'DONr' 'DOP' 'DOPr' 'NH4' 'DOC'} ;
CESM_file = '/data/project7/pdamien/DATA/BGC/CESM/CESM_BGC_annual_profiles.nc' ;
eps = 1e-5  ;
%
theta_s = 6.0 ; theta_b = 6.0 ;
hc = 250 ; sc_type = 'new2012'; NZ = 100 ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%
[nx,ny]=size(ncread(grdname,'h')) ;

%%% interpolate CASE 2

zdep1 = ncread(CESM_file,'z_t') ;       nz1 = length(zdep1) ;
zdep2 = ncread(CESM_file,'z_t_150m') ;  nz2 = length(zdep2) ;
chlCESM = ncread(CESM_file,'spChl') + ncread(CESM_file,'diatChl') + ncread(CESM_file,'diazChl') ;
chlCESM =  [chlCESM' ones(1,nz1-nz2)*eps]' ;
for v=1:length(BGCname2_vars)
    var = ncread(CESM_file,BGCname2_vars_marbl{v})  ; var(var<0) = eps ;
    if length(var)==length(zdep1)
       vartype(v)=1 ;
       VARprofiles(v,:) = var./chlCESM ;
    elseif length(var)==length(zdep2)
       vartype(v)=2 ;
       VARprofiles(v,:) = [var' ones(1,nz1-nz2)*eps]'./chlCESM ;
       VARprofiles(v,nz2:nz1) = VARprofiles(v,nz2) ;
    else
       disp('Something wrong') ; stop ;
    end
end
zdep1(end) = zdep1(end)+6000 ;

      h = ncread(grdname,'h') ;
      [z_rb,Crb] = zlevs4(permute(h,[2 1]),permute(h,[2 1])*0, theta_s, theta_b, hc, NZ, 'r',sc_type) ;
      z_rb = permute(z_rb,[3 2 1]) ; 
      chl = ncread(ininame,'CHL') ;
      for v=1:length(BGCname2_vars)
      disp(['  Working on ' BGCname2_vars{v}])
          clear var
          for i=1:nx
          for j=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,j,:))) ;
              var(i,j,:) = fillmissing(testvec,'nearest') ;
          end
          end
          var = chl.*var ; 
          ncwrite(ininame,BGCname2_vars{v},var) ;
      end

%%% interpolate CASE 3

clear vartype VARprofiles
zdep1 = ncread(CESM_file,'z_t') ;       nz1 = length(zdep1) ;
zdep2 = ncread(CESM_file,'z_t_150m') ;  nz2 = length(zdep2) ;
for v=1:length(BGCname3_vars)
    var = ncread(CESM_file,BGCname3_vars_marbl{v}) ; var(var<0) = eps ;
    if length(var)==length(zdep1)
       vartype(v)=1 ;
       VARprofiles(v,:) = var ;
    elseif length(var)==length(zdep2)
       vartype(v)=2 ;
       VARprofiles(v,:) = [var' ones(1,nz1-nz2)*eps]' ;
    else
       disp('Something wrong') ; stop ;
    end
end
zdep1(end) = zdep1(end)+6000 ;

      for v=1:length(BGCname3_vars)
          disp(['  Working on ' BGCname3_vars{v}])
          clear var
          for i=1:nx
          for j=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,j,:))) ;
              var(i,j,:) = fillmissing(testvec,'nearest') ;
          end
          end
          ncwrite(ininame,BGCname3_vars{v},var) ;
      end



