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
%   Parent...
%
     parscd.file    = '/data/project3/pdamien/ROMS_pdamien/config/IOP2ARCTERX/nwpac_rst.20150106001554.nc';
     pargrd = '/data/project3/pdamien/ROMS_pdamien/config/NWPAC2KM/nwpac_grd.nc'
     parscd.N       = 100 ;
     parscd.theta_s = 6.0;
     parscd.theta_b = 6.0;
     parscd.hc      = 250 ;
     parscd.tind    = 2;            % frame number in parent file
     parscd.scoord = 'new2012';    % child 'new' or 'old' type scoord
%
%   child
%
    romsdir    = '/data/project3/pdamien/ROMS_pdamien/config/IOP2ARCTERX/';
    chdgrd    = [romsdir 'arcterxIOP2_grd.nc'];
    chdini    = [romsdir 'arcterxIOP2_ini20150106.nc'];
    chdscd.theta_s = 6.0;
    chdscd.theta_b = 6.0;
    chdscd.hc     = 250.0;
    chdscd.N      = 100;
    chdscd.scoord = 'new2012';    % child 'new' or 'old' type scoord
%    
    do_slow = 1 ; % write  u_slow, v_slow, p_slow from restart file.
%    
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%

    if ~exist(chdini)
      disp(['Creating initial file: ' chdini]);
      r2r_create_ini(chdini,chdgrd,chdscd.N,chdscd,do_slow)
    end

    r2r_make_ini(pargrd, parscd.file, chdgrd, chdini, chdscd,parscd,parscd.scoord,chdscd.scoord,do_slow)
    
    
    
