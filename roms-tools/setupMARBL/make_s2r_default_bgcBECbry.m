%---------------------------------------------------------------------------------------
%
% make_s2r_default_bgcbry
%
% - Make bry for constant BGC concentration 
% @Pierre Damien, ucla, March 2024
%   
%---------------------------------------------------------------------------------------
clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
%
start_date = datenum(1994,01,01);
end_date   = datenum(2023,12,31);
time_ref = datenum(1995,1,1) ; % reference time for ROMS
%
grdname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_grd.nc' ;  
%
bgcname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMmarbl/FORCINGS/pacmed25_default_bgcBECbry.nc' ;
obcflag = [1 1 1 1] ; % open boundary flag (1=open, [S E N W])
nz=100 ;
%
BGCname3_vars = {'DON' 'DONR' 'DOP' 'DOPR' 'DOFE' 'NH4' 'DOC' 'NO2' 'N2' 'pas1' 'pas2' 'pas3'} ;
BGCname3_coef = [ 1     0.8    0.1  0.003  0.0001  1e-6  1e-6 1e-6  1e-6     1      1      1] ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------

[nx,ny]=size(ncread(grdname,'h')) ;

%
   time2wr = [start_date end_date] - time_ref ;
   nccreate(bgcname,'bry_time','Dimensions',{'time',2},'datatype','single');
   ncwrite(bgcname,'bry_time',time2wr) ;
   ncwriteatt(bgcname,'bry_time','long_name','time for boundary data');
   ncwriteatt(bgcname,'bry_time','units','days');

   if obcflag(1)==1  %%   Southern boundary
      disp('   Southern boundary')
      for v=1:length(BGCname3_vars)
          var = ones(nx,nz,2).*BGCname3_coef(v) ;
          nccreate(bgcname,[BGCname3_vars{v} '_south'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',2},'datatype','single');
          ncwrite(bgcname,[BGCname3_vars{v} '_south'],var) ;
      end
   end

   if obcflag(2)==1  %%   Eastern boundary
      disp('   Eastern boundary')
      for v=1:length(BGCname3_vars)
          var = ones(ny,nz,2).*BGCname3_coef(v) ;
          nccreate(bgcname,[BGCname3_vars{v} '_east'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',2},'datatype','single');
          ncwrite(bgcname,[BGCname3_vars{v} '_east'],var) ;
      end
   end

   if obcflag(3)==1  %%   Northern boundary
      disp('   Northern boundary')
      for v=1:length(BGCname3_vars)
          var = ones(nx,nz,2).*BGCname3_coef(v) ;
          nccreate(bgcname,[BGCname3_vars{v} '_north'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',2},'datatype','single');
          ncwrite(bgcname,[BGCname3_vars{v} '_north'],var) ;
      end
   end

   if obcflag(4)==1  %%   Western boundary
      disp('   Western boundary')
      for v=1:length(BGCname3_vars)
          var = ones(ny,nz,2).*BGCname3_coef(v) ;
          nccreate(bgcname,[BGCname3_vars{v} '_west'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',2},'datatype','single');
          ncwrite(bgcname,[BGCname3_vars{v} '_west'],var) ;
      end
   end


