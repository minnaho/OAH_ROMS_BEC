%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% make_s2r_bgcSRF
%
% This script interpolates the surface fileds needed to computed 
% BGC flux from different sources Onto a ROMS domains. 
%
% Pierre DAMIEN, inspired from Jeroen Molemaker, UCLA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
close all
disp(' ')
addpath(genpath('/data/project3/pdamien/tools_matlab'))
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
    romsdir    = '/data/project9/minnaho/swel/';
    grdname    = [romsdir 'sfshelf60_grd.nc'];
    outname    = [romsdir 'sfshelf60_bgcflx'];
%    bgctime    = 12 ; % 1 for climato, 12 for seasonal 
    start_date = datenum(2019,01,01);
    end_date   = datenum(2019,12,31);
    time_ref = datenum(1995,1,1) ; % reference time for ROMS
    BGCparam.Ntrc = 3 ;        % Number of tracers/flx to interpolate  
%--   interpolation routine defined by BGCparam.interp 
%--   BGCparam.interp==1 : PCo2 
%--   BGCparam.interp==2 : Iron/dust
% ------ CO2
    BGCparam.name_vars{1} = 'pco2_air' ;
    BGCparam.long_name{1} = 'atmospheric pco2' ;
    BGCparam.units{1} = 'ppmv' ;
    BGCparam.file_vars{1} = '/data/project7/pdamien/DATA/BGC/pCO2/OCADS/OCADS_ref2002.nc' ;
    BGCparam.interp(1)=1 ;
% ------ dust
    BGCparam.name_vars{2} = 'dust' ;
    BGCparam.long_name{2} = 'dust deposition' ;
    BGCparam.units{2} = 'kg/m2/s' ; %'nmol/cm2/s' ;
%    BGCparam.file_vars{2} = '/data/project7/pdamien/DATA/BGC/Srf_BGC_Flx/IronDeposition/Iron_soldep_2010.nc' ;
%    BGCparam.interp(2)=2 ; 
    BGCparam.file_vars{2} = '/data/project7/pdamien/DATA/BGC/Srf_BGC_Flx/KoK2021/DustCOMM_totdep_seas_bin.nc' ;
    BGCparam.interp(2)=3 ;
% ------ Iron
    BGCparam.name_vars{3} = 'iron' ;
    BGCparam.long_name{3} = 'iron deposition' ;
    BGCparam.units{3} = 'nmol/cm2/s' ;
%    BGCparam.file_vars{3} = '/data/project7/pdamien/DATA/BGC/Srf_BGC_Flx/IronDeposition/Iron_soldep_2010.nc' ;
%    BGCparam.interp(3)=2 ;
    BGCparam.file_vars{3} = '/data/project7/pdamien/DATA/BGC/Srf_BGC_Flx/IronDeposition_Hamilton/Hamilton2022/CAM6-MIMI_2002-2020CLIMOMEAN_IRONDEP.nc' ;
    BGCparam.interp(3)=4 ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%

% make one bry file per year
  start_year = str2num(datestr(start_date,'YYYY')) ;
  end_year = str2num(datestr(end_date,'YYYY')) ;

%%% read the grid for interpolation
  grd.lon = ncread(grdname,'lon_rho')';
  grd.lat = ncread(grdname,'lat_rho')';
  [grd.ny,grd.nx] = size(grd.lon);

for yy=start_year:end_year

    disp(['Working on year ' num2str(yy)])
    outfile = [outname '_' num2str(yy) '.nc']

for n=1:BGCparam.Ntrc
    disp(' **** ')
    disp(['Working on trc : ' num2str(n) '/' num2str(BGCparam.Ntrc) ' , ' BGCparam.long_name{n}])
    if BGCparam.interp(n)==1
       disp('      Interpolation of pCO2')
       [var,stime] = get_frc_pco2(grd,BGCparam,n);
       create_bgcflx(outfile,grdname,BGCparam,n,length(stime));
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,'pco2_time',time2wr);
       ncwrite(outfile,'pco2_air',var);
    elseif BGCparam.interp(n)==2
       disp('      Interpolation of dust/iron from Liu 2022')
       [var,stime] = get_frc_dust_iron(grd,BGCparam,n);
       create_bgcflx(outfile,grdname,BGCparam,n,length(stime));
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,[BGCparam.name_vars{n} '_time'],time2wr);
       ncwrite(outfile,BGCparam.name_vars{n},var);
    elseif BGCparam.interp(n)==3
       disp('      Interpolation of Jasper KoK''s dataset published in 2021')
       [var,stime] = get_frc_dust_Kok2021(grd,BGCparam,n);
       create_bgcflx(outfile,grdname,BGCparam,n,length(stime));
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,[BGCparam.name_vars{n} '_time'],time2wr);
       ncwrite(outfile,BGCparam.name_vars{n},var);
    elseif BGCparam.interp(n)==4
       disp('      Interpolation of Douglas Hamilton''s dataset published in 2022')
       [var,stime] = get_frc_iron_Hamilton2022(grd,BGCparam,n);
       create_bgcflx(outfile,grdname,BGCparam,n,length(stime));
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,[BGCparam.name_vars{n} '_time'],time2wr);
       ncwrite(outfile,BGCparam.name_vars{n},var);
    end
end





end


