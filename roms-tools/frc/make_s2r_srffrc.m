%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% make_s2r_srffrc
%
% This script interpolates the surface fields needed to compute
% surface flux corrections (wind stress and ssflx)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
    romsdir    = '/data/project3/pdamien/ROMS_pdamien/config/SWELL/';
    grdname    = [romsdir 'uswc1200_grd.nc'];
    outname    = [romsdir 'uswc1200_srfflx'];
    
    start_date = datenum(2017,01,01);
    end_date   = datenum(2020,12,31);
    time_ref = datenum(1995,1,1) ; % reference time for ROMS

    make_sss = 1 ; % interp sss 
    file_sss = '/data/project7/pdamien/DATA/BGC/WOA18/salt/woa18_decav_s*_04.nc' ; 
    make_tau = 0 ; % get Tau correction
    file_tau = 'TAUcorr/TAUcorr_PACGIG2KMfull_2000_2010.mat';

    coarse_frc = 0 ;  
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%

% make one bry file per year
  start_year = str2num(datestr(start_date,'YYYY')) ;
  end_year = str2num(datestr(end_date,'YYYY')) ;

%%% read the grid for interpolation

if coarse_frc
  grd.lon = ncread(grdname,'lon_coarse')';
  grd.lat = ncread(grdname,'lat_coarse')';
  [grd.ny,grd.nx] = size(grd.lon);
else
  grd.lon = ncread(grdname,'lon_rho')';
  grd.lat = ncread(grdname,'lat_rho')';
  [grd.ny,grd.nx] = size(grd.lon);
end

for yy=start_year:end_year

    disp(['Working on year ' num2str(yy)])
    outfile = [outname '_' num2str(yy) '.nc']

    if make_sss==1 
       disp('      Interpolation of SSS')
       [var,stime] = get_frc_sss(grd,file_sss);
       create_frc_srfflx(outfile,grdname,1,coarse_frc);
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,'sss_time',time2wr);
       ncwrite(outfile,'sss',var);
    end

    if make_tau==1
       disp('      Interpolation of Tau correction')
       load(file_tau)
       stime = [15.5 45 74.5 105 135.5 166 196 227.5 258 288.5 319 349.5] ; 
       create_frc_srfflx(outfile,grdname,2,coarse_frc);
       time2wr = double(stime) + datenum(yy,1,1) - time_ref ;
       ncwrite(outfile,'Taucorr_time',time2wr);
       ncwrite(outfile,'TauX_corr',Tau_correc.TauX_corr);
       ncwrite(outfile,'TauY_corr',Tau_correc.TauY_corr);
    end
    
end


