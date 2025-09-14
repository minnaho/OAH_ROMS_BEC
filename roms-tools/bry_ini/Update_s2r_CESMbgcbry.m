%---------------------------------------------------------------------------------------
%
% make_s2r_bgcbry
%
% - Make BGC bry from physical bry
% - Interpolate the BGC fields onto the bry file
% - Require to run first Make_BGCfrc/make_s2r_bgc.m. It interpolates BGC variables from 
%   a collection of sources onto the grid. Here, the interpolation in time and density 
%   space is done
%   
%---------------------------------------------------------------------------------------
clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
%
start_date = datenum(1999,01,01);
end_date   = datenum(2012,12,31);
%
grdname = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_grd.nc' ;  
%
bgcname = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_bgcbry_' ;
obcflag = [1 1 1 0] ; % open boundary flag (1=open, [S E N W])
time_ref = datenum(1995,1,1) ; % reference time for ROMS
%
BGCname2_vars       = {'SPC' 'SPCHL' 'SPFE' 'SPCACO3' 'DIATC' 'DIATCHL' 'DIATFE' 'DIATSI' 'DIAZC' 'DIAZCHL' 'DIAZFE' 'ZOOC'} ;
BGCname2_vars_marbl = {'spC' 'spChl' 'spFe' 'spCaCO3' 'diatC' 'diatChl' 'diatFe' 'diatSi' 'diazC' 'diazChl' 'diazFe' 'zooC'} ;
CESM_file = '/data/project7/pdamien/DATA/BGC/CESM/CESM_BGC_annual_profiles.nc' ;
eps = 1e-5  ;
%
theta_s = 6.0 ; theta_b = 6.0 ;
hc = 250 ; sc_type = 'new2012'; NZ = 100 ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------

% make one bry file per year
start_year = str2num(datestr(start_date,'YYYY')) ;
end_year = str2num(datestr(end_date,'YYYY')) ;
[nx,ny]=size(ncread(grdname,'h')) ;

%
%% Read the ratio CHL-based
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


%
% Loop over years
for yy=start_year:end_year

   disp(['Working on year ' num2str(yy)])
   file_bgcbry = [bgcname num2str(yy) '.nc'] ;

   if obcflag(1)==1  %%   Southern boundary
      disp('   Southern boundary')
      hbdy = ncread(grdname,'h',[1 1],[inf 1]) ;
      [z_rb,Crb] = zlevs4(hbdy,hbdy*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      chl_bry = ncread(file_bgcbry,'CHL_south') ; 
      for v=1:length(BGCname2_vars)
          clear var
          for i=1:nx
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          for t=1:size(chl_bry,3)
              var2write = squeeze(chl_bry(:,:,t)).*var ;
              ncwrite(file_bgcbry,[BGCname2_vars{v} '_south'],var2write,[1 1 t]) ;
          end
      end
   end

   if obcflag(2)==1  %%   Eastern boundary
      disp('   Eastern boundary')
      hbdy = ncread(grdname,'h',[nx 1],[1 inf]) ;
      [z_rb,Crb] = zlevs4(hbdy',hbdy'*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      chl_bry = ncread(file_bgcbry,'CHL_east') ;
      for v=1:length(BGCname2_vars)
          clear var
          for i=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          for t=1:size(chl_bry,3)
              var2write = squeeze(chl_bry(:,:,t)).*var ;
              ncwrite(file_bgcbry,[BGCname2_vars{v} '_east'],var2write,[1 1 t]) ;
          end
      end
   end

   if obcflag(3)==1  %%   Northern boundary
      disp('   Northern boundary')
      hbdy = ncread(grdname,'h',[1 ny],[inf 1]) ;
      [z_rb,Crb] = zlevs4(hbdy,hbdy*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      chl_bry = ncread(file_bgcbry,'CHL_north') ;
      for v=1:length(BGCname2_vars)
          clear var
          for i=1:nx
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          for t=1:size(chl_bry,3)
              var2write = squeeze(chl_bry(:,:,t)).*var ;
              ncwrite(file_bgcbry,[BGCname2_vars{v} '_north'],var2write,[1 1 t]) ;
          end
      end
   end

   if obcflag(4)==1  %%   Western boundary
      disp('   Western boundary')
      hbdy = ncread(grdname,'h',[1 1],[1 inf]) ;
      [z_rb,Crb] = zlevs4(hbdy',hbdy'*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      chl_bry = ncread(file_bgcbry,'CHL_west') ;
      for v=1:length(BGCname2_vars)
          clear var
          for i=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          for t=1:size(chl_bry,3)
              var2write = squeeze(chl_bry(:,:,t)).*var ;
              ncwrite(file_bgcbry,[BGCname2_vars{v} '_west'],var2write,[1 1 t]) ;
          end
      end
   end

end


