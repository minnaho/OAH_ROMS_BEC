%---------------------------------------------------------------------------------------
%
% make_s2r_default_bgcbry
%
% - Make bry for BGC concentration profiles based on CESM
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
time_ref = datenum(1995,1,1) ; % reference time for ROMS
%
grdname = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_grd.nc' ;  
%
bgcname = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_default_bgcbry.nc' ;
obcflag = [1 1 1 0] ; % open boundary flag (1=open, [S E N W])
nz=100 ;
%
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

[nx,ny]=size(ncread(grdname,'h')) ;

%% Read VAR 
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

%
%   time2wr = [start_date end_date] - time_ref ;
%   nccreate(bgcname,'bry_time','Dimensions',{'time',2},'datatype','single');
%   ncwrite(bgcname,'bry_time',time2wr) ;
%   ncwriteatt(bgcname,'bry_time','long_name','time for boundary data');
%   ncwriteatt(bgcname,'bry_time','units','days');

   if obcflag(1)==1  %%   Southern boundary
      disp('   Southern boundary')
      hbdy = ncread(grdname,'h',[1 1],[inf 1]) ; 
      [z_rb,Crb] = zlevs4(hbdy,hbdy*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      for v=1:length(BGCname3_vars)
          clear var
          for i=1:nx
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ; 
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          ncwrite(bgcname,[BGCname3_vars{v} '_south'],var,[1 1 1]) ;
          ncwrite(bgcname,[BGCname3_vars{v} '_south'],var,[1 1 2]) ;
      end
   end

   if obcflag(2)==1  %%   Eastern boundary
      disp('   Eastern boundary')
      hbdy = ncread(grdname,'h',[nx 1],[1 inf]) ;
      [z_rb,Crb] = zlevs4(hbdy',hbdy'*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      for v=1:length(BGCname3_vars)
          clear var
          for i=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          ncwrite(bgcname,[BGCname3_vars{v} '_east'],var,[1 1 1]) ;
          ncwrite(bgcname,[BGCname3_vars{v} '_east'],var,[1 1 2]) ;
      end
   end

   if obcflag(3)==1  %%   Northern boundary
      disp('   Northern boundary')
      hbdy = ncread(grdname,'h',[1 ny],[inf 1]) ;
      [z_rb,Crb] = zlevs4(hbdy,hbdy*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      for v=1:length(BGCname3_vars)
          clear var
          for i=1:nx
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          ncwrite(bgcname,[BGCname3_vars{v} '_north'],var,[1 1 1]) ;
          ncwrite(bgcname,[BGCname3_vars{v} '_north'],var,[1 1 2]) ;
      end
   end

   if obcflag(4)==1  %%   Western boundary
      disp('   Western boundary')
      hbdy = ncread(grdname,'h',[1 1],[1 inf]) ;
      [z_rb,Crb] = zlevs4(hbdy',hbdy'*0, theta_s, theta_b, hc, NZ, 'r',sc_type);
      z_rb = z_rb' ;
      for v=1:length(BGCname3_vars)
          clear var
          for i=1:ny
              testvec(1:NZ) = interp1(-zdep1,squeeze(VARprofiles(v,:)),squeeze(z_rb(i,:))) ;
              var(i,:) = fillmissing(testvec,'nearest') ;
          end
          ncwrite(bgcname,[BGCname3_vars{v} '_west'],var,[1 1 1]) ;
          ncwrite(bgcname,[BGCname3_vars{v} '_west'],var,[1 1 2]) ;
      end
   end


