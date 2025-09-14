%---------------------------------------------------------------------------------------
%
%  make_s2r
%
%  Generate boundary perimeter file from WOA and SSH  data.
%
%  Note that when run this script it tests for the presence of a .mat file
%  which contains various interpolation coefficients related to your child
%  and parent grids.  If the .mat file is not there it will calculate the coefficients
%
%
%  Jeroen Molemaker and Evan Mason in 2007-2009 at UCLA
%
%---------------------------------------------------------------------------------------
clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
%
grdname = '/data/project8/pdamien/ROMS_outputs/PACGIG2KM/FORCINGS/pacgig2km_grd.nc' ;
ininame = '/data/project8/pdamien/ROMS_outputs/PACGIG2KM/FORCINGS/pacgig2km_ini20211231.nc' ;

%datname = '/data/project7/pdamien/DATA/GLORYS12V1_FORECAST/2022/mercatorglorys12v1_gl12_mean_20220501.nc' ; 
datname = '/data/project7/pdamien/DATA/GLORYS12V1/glorys12v1_Y2021M12D31.nc' ;

pars.theta_s = 6.0;
pars.theta_b = 6.0;
pars.hc     = 250.0;
pars.N      = 100;
pars.scoord = 'new2012';    % child 'new' or 'old' type scoord

time_ref = datenum(2000,1,1) ; % reference time for ROMS
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------

    if ~exist(ininame)
      disp(['Creating initial file: ' ininame]);
      r2r_create_ini(ininame,grdname,pars.N,pars,0);
    end

     stime=0 ;
     ncid = netcdf.open(datname,'nowrite');
     try
        ID = netcdf.inqVarID(ncid,'time');
     catch exception
        if strcmp(exception.identifier,'MATLAB:imagesci:netcdf:libraryFailure')
           index=strfind(datname,'Y') ;
           stime = datenum(str2num(datname(index(end)+1:index(end)+4)), ...
                           str2num(datname(index(end)+6:index(end)+7)),...
                           str2num(datname(index(end)+9:index(end)+10))) + 0.5 ;
        end
      end
      netcdf.close(ncid)
      if stime==0
         stime = double(ncread(datname,'time',[1],[1]))/24 + datenum(1950,1,1);
      end
      disp(['Initial time for date ' datestr(stime) ' with ROMS ref time ' datestr(time_ref)])
      time2wr = double(stime) - time_ref ;
      time2wr = time2wr.*24*3600 ;     % day to sec
      ncwrite(ininame,'ocean_time',time2wr);

    s2r_hv_ini(datname,grdname,ininame,pars)

    
