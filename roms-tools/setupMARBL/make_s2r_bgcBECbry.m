%---------------------------------------------------------------------------------------
%
% make_s2r_bgcbry
%
% - Make BGC bry from physical bry
% - Interpolate the BGC fields onto the bry file
% - Require to run first Make_BGCfrc/make_s2r_bgc.m. It interpolates BGC variables from 
%   a collection of sources onto the grid. Here, the interpolation in time and density 
%   space is done
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
start_date = datenum(1995,01,01);
end_date   = datenum(1995,12,31);
%
grdname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMmarbl/FORCINGS/pacmed25_grd.nc' ;  
%
bryname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMmarbl/FORCINGS/pacmed25_bry.' ; 
bgcname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMmarbl/FORCINGS/pacmed25_bgcBECbry.' ;
obcflag = [1 1 1 1] ; % open boundary flag (1=open, [S E N W])
time_ref = datenum(1995,1,1) ; % reference time for ROMS
%
% CASE 1 : vars to read from file and interpolate on density profile  
BGCname1_vars = {'NO3' 'PO4' 'SiO3' 'O2' 'Fe' 'DIC' 'Alk' 'N2O' 'CHL'} ;
bgc_file = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/BGC/pacmed_0p25_bgc_*.nc' ;  
% CASE 2 : vars derived from other vars 
BGCname2_vars = {'SPC' 'SPCHL' 'SPFE' 'SPCACO3' 'DIATC' 'DIATCHL' 'DIATFE' 'DIATSI' 'DIAZC' 'DIAZCHL' 'DIAZFE' 'ZOOC'} ;
BGCname2_coef = [3.375 0.675 1.35e-05  0.0675   0.2025   0.0675   1.35e-06  0.0675   0.0375   0.0075  7.5e-07   1.35] ;
BGCname2_vref = {'CHL' 'CHL'   'CHL'   'CHL'    'CHL'      'CHL'    'CHL'    'CHL'   'CHL'     'CHL'   'CHL'   'CHL'} ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------

% make one bry file per year
start_year = str2num(datestr(start_date,'YYYY')) ;
end_year = str2num(datestr(end_date,'YYYY')) ;
[nx,ny]=size(ncread(grdname,'h')) ;

%
% Source time
list = dir(bgc_file) ;
file_bgc = [list(1).folder '/' list(1).name] ;
for t=1:length(list)
    file = [list(t).folder '/' list(t).name] ;
    frc_time(t) = ncread(file,'time')  ;
    idx_time(t) = t ;
end
frc_time = [frc_time(end)-365.25 frc_time 365.25+frc_time(1)] ;
idx_time = [12 idx_time 1] ;

%
% Source vars for Case 1
if obcflag(1)==1  %%   Southern boundary
   for t=1:length(list)
   file = [list(t).folder '/' list(t).name] ;
   dens_bry_south(:,:,t) = squeeze(sw_dens0(ncread(file,'salt',[1 1 1 1],[inf 1 inf 1]),ncread(file,'temp',[1 1 1 1],[inf 1 inf 1]))) ;
   for v=1:length(BGCname1_vars)
       vars_bry_south(:,:,t,v) = squeeze(ncread(file,BGCname1_vars{v},[1 1 1 1],[inf 1 inf 1])) ; 
   end
   end
end
if obcflag(2)==1  %%   Eastern boundary
   for t=1:length(list)
   file = [list(t).folder '/' list(t).name] ;
   dens_bry_east(:,:,t) = squeeze(sw_dens0(ncread(file,'salt',[nx 1 1 1],[1 inf inf 1]),ncread(file,'temp',[nx 1 1 1],[1 inf inf 1]))) ;
   for v=1:length(BGCname1_vars)
       vars_bry_east(:,:,t,v) = squeeze(ncread(file,BGCname1_vars{v},[nx 1 1 1],[1 inf inf 1])) ;
   end
   end
end
if obcflag(3)==1  %%   Northern boundary
   for t=1:length(list)
   file = [list(t).folder '/' list(t).name] ;
   dens_bry_north(:,:,t) = squeeze(sw_dens0(ncread(file,'salt',[1 ny 1 1],[inf 1 inf 1]),ncread(file,'temp',[1 ny 1 1],[inf 1 inf 1]))) ;
   for v=1:length(BGCname1_vars)
       vars_bry_north(:,:,t,v) = squeeze(ncread(file,BGCname1_vars{v},[1 ny 1 1],[inf 1 inf 1])) ;
   end
   end
end
if obcflag(4)==1  %%   Western boundary
   for t=1:length(list)
   file = [list(t).folder '/' list(t).name] ;
   dens_bry_west(:,:,t) = squeeze(sw_dens0(ncread(file,'salt',[1 1 1 1],[1 inf inf 1]),ncread(file,'temp',[1 1 1 1],[1 inf inf 1]))) ;
   for v=1:length(BGCname1_vars)
       vars_bry_west(:,:,t,v) = squeeze(ncread(file,BGCname1_vars{v},[1 1 1 1],[1 inf inf 1])) ;
   end
   end
end

%
% Loop over years
for yy=start_year:end_year

   disp(['Working on year ' num2str(yy)])
   file_bry = [bryname num2str(yy) '.nc'] ; 
   file_bgcbry = [bgcname num2str(yy) '.nc'] ;

   bry_time = double(ncread(file_bry,'bry_time') + time_ref) ;
   bry_day = bry_time - datenum(str2num(datestr(bry_time,'yyyy')),1,1) ;

   clear coeft
   for t=1:length(bry_day)
   t0 = find(frc_time<=bry_day(t),1,'last');
   t1 = find(frc_time>bry_day(t),1,'first');
   coeft(t,1) = idx_time(t0) ; 
   coeft(t,2) = idx_time(t1) ;
   coeft(t,3) = (bry_day(t)-frc_time(t0)) / (frc_time(t1)-frc_time(t0)) ;  
   end

   nccreate(file_bgcbry,'bry_time','Dimensions',{'time',0},'datatype','single');
   ncwrite(file_bgcbry,'bry_time',ncread(file_bry,'bry_time')) ;
   varat = ncreadatt(file_bry,'bry_time','long_name') ;
   ncwriteatt(file_bgcbry,'bry_time','long_name',varat);
   varat = ncreadatt(file_bry,'bry_time','units') ;
   ncwriteatt(file_bgcbry,'bry_time','units',varat);

   if obcflag(1)==1  %%   Southern boundary
      disp('   Southern boundary')
      dens_bry = sw_dens0(ncread(file_bry,'salt_south'),ncread(file_bry,'temp_south')) ; 
      nz=size(dens_bry,2) ;
      for z=nz-1:-1:1
          dens_bry(:,z,:) = dens_bry(:,z,:) + z*0.0000001 ;
      end
      for v=1:length(BGCname1_vars)
      var_int = dens_bry.*0 ;
      for t=1:length(bry_day)
          rho_t = dens_bry_south(:,:,coeft(t,1))   + coeft(t,3).*(dens_bry_south(:,:,coeft(t,2))  -dens_bry_south(:,:,coeft(t,1))  );
          for z=nz-1:-1:1
          rho_t(:,z) = rho_t(:,z) + z*0.0000001 ;
          end 
          var_t = vars_bry_south(:,:,coeft(t,1),v) + coeft(t,3).*(vars_bry_south(:,:,coeft(t,2),v)-vars_bry_south(:,:,coeft(t,1),v));
          for i=1:size(rho_t,1)
              var_int(i,:,t) = interp1(squeeze(rho_t(i,:)),squeeze(var_t(i,:)), ...
                                       squeeze(dens_bry(i,:,t)),'nearest','extrap');
          end
      end
      nccreate(file_bgcbry,[BGCname1_vars{v} '_south'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',0},'datatype','single');
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'long_name') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_south'],'long_name',varat);
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'units') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_south'],'units',varat);
      ncwrite(file_bgcbry,[BGCname1_vars{v} '_south'],var_int) ;
      end
      for v=1:length(BGCname2_vars)
          var = BGCname2_coef(v) * ncread(file_bgcbry,[BGCname2_vref{v} '_south']) ;
          nccreate(file_bgcbry,[BGCname2_vars{v} '_south'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',0},'datatype','single');
          ncwrite(file_bgcbry,[BGCname2_vars{v} '_south'],var) ;
      end
   end

   if obcflag(2)==1  %%   Eastern boundary
      disp('   Eastern boundary')
      dens_bry = sw_dens0(ncread(file_bry,'salt_east'),ncread(file_bry,'temp_east')) ;
      nz=size(dens_bry,2) ;
      for z=nz-1:-1:1
          dens_bry(:,z,:) = dens_bry(:,z,:) + z*0.0000001 ;
      end
      for v=1:length(BGCname1_vars)
      var_int = dens_bry.*0 ;
      for t=1:length(bry_day)
          rho_t = dens_bry_east(:,:,coeft(t,1))   + coeft(t,3).*(dens_bry_east(:,:,coeft(t,2))  -dens_bry_east(:,:,coeft(t,1))  );
          for z=nz-1:-1:1
          rho_t(:,z) = rho_t(:,z) + z*0.0000001 ;
          end
          var_t = vars_bry_east(:,:,coeft(t,1),v) + coeft(t,3).*(vars_bry_east(:,:,coeft(t,2),v)-vars_bry_east(:,:,coeft(t,1),v));
          for i=1:size(rho_t,1)
              var_int(i,:,t) = interp1(squeeze(rho_t(i,:)),squeeze(var_t(i,:)), ...
                                       squeeze(dens_bry(i,:,t)),'nearest','extrap');
          end
      end
      nccreate(file_bgcbry,[BGCname1_vars{v} '_east'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',0},'datatype','single');
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'long_name') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_east'],'long_name',varat);
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'units') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_east'],'units',varat);
      ncwrite(file_bgcbry,[BGCname1_vars{v} '_east'],var_int) ;
      end
      for v=1:length(BGCname2_vars)
          var = BGCname2_coef(v) * ncread(file_bgcbry,[BGCname2_vref{v} '_east']) ;
          nccreate(file_bgcbry,[BGCname2_vars{v} '_east'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',0},'datatype','single');
          ncwrite(file_bgcbry,[BGCname2_vars{v} '_east'],var) ;
      end
   end

   if obcflag(3)==1  %%   Northern boundary
      disp('   Northern boundary')
      dens_bry = sw_dens0(ncread(file_bry,'salt_north'),ncread(file_bry,'temp_north')) ;
      nz=size(dens_bry,2) ;
      for z=nz-1:-1:1
          dens_bry(:,z,:) = dens_bry(:,z,:) + z*0.0000001 ;
      end
      for v=1:length(BGCname1_vars)
      var_int = dens_bry.*0 ;
      for t=1:length(bry_day)
          rho_t = dens_bry_north(:,:,coeft(t,1))   + coeft(t,3).*(dens_bry_north(:,:,coeft(t,2))  -dens_bry_north(:,:,coeft(t,1))  );
          for z=nz-1:-1:1
          rho_t(:,z) = rho_t(:,z) + z*0.0000001 ;
          end
          var_t = vars_bry_north(:,:,coeft(t,1),v) + coeft(t,3).*(vars_bry_north(:,:,coeft(t,2),v)-vars_bry_north(:,:,coeft(t,1),v));
          for i=1:size(rho_t,1)
              var_int(i,:,t) = interp1(squeeze(rho_t(i,:)),squeeze(var_t(i,:)), ...
                                       squeeze(dens_bry(i,:,t)),'nearest','extrap');
          end
      end
      nccreate(file_bgcbry,[BGCname1_vars{v} '_north'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',0},'datatype','single');
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'long_name') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_north'],'long_name',varat);
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'units') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_north'],'units',varat);
      ncwrite(file_bgcbry,[BGCname1_vars{v} '_north'],var_int) ;
      end
      for v=1:length(BGCname2_vars)
          var = BGCname2_coef(v) * ncread(file_bgcbry,[BGCname2_vref{v} '_north']) ;
          nccreate(file_bgcbry,[BGCname2_vars{v} '_north'],'Dimensions',{'xi_rho',nx,'s_rho',nz,'time',0},'datatype','single');
          ncwrite(file_bgcbry,[BGCname2_vars{v} '_north'],var) ;
      end
   end

   if obcflag(4)==1  %%   Western boundary
      disp('   Western boundary')
      dens_bry = sw_dens0(ncread(file_bry,'salt_west'),ncread(file_bry,'temp_west')) ;
      nz = size(dens_bry,2) ;
      for z=nz-1:-1:1
          dens_bry(:,z,:) = dens_bry(:,z,:) + z*0.0000001 ;
      end
      for v=1:length(BGCname1_vars)
      var_int = dens_bry.*0 ;
      for t=1:length(bry_day)
          rho_t = dens_bry_west(:,:,coeft(t,1))   + coeft(t,3).*(dens_bry_west(:,:,coeft(t,2))  -dens_bry_west(:,:,coeft(t,1))  );
          for z=nz-1:-1:1
          rho_t(:,z) = rho_t(:,z) + z*0.0000001 ;
          end
          var_t = vars_bry_west(:,:,coeft(t,1),v) + coeft(t,3).*(vars_bry_west(:,:,coeft(t,2),v)-vars_bry_west(:,:,coeft(t,1),v));
          for i=1:size(rho_t,1)
              var_int(i,:,t) = interp1(squeeze(rho_t(i,:)),squeeze(var_t(i,:)), ...
                                       squeeze(dens_bry(i,:,t)),'nearest','extrap');
          end
      end
      nccreate(file_bgcbry,[BGCname1_vars{v} '_west'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',0},'datatype','single');
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'long_name') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_west'],'long_name',varat);
      varat = ncreadatt(file_bgc,BGCname1_vars{v},'units') ;
      ncwriteatt(file_bgcbry,[BGCname1_vars{v} '_west'],'units',varat);
      ncwrite(file_bgcbry,[BGCname1_vars{v} '_west'],var_int) ;
      end
      for v=1:length(BGCname2_vars)
          var = BGCname2_coef(v) * ncread(file_bgcbry,[BGCname2_vref{v} '_west']) ;
          nccreate(file_bgcbry,[BGCname2_vars{v} '_west'],'Dimensions',{'eta_rho',ny,'s_rho',nz,'time',0},'datatype','single');
          ncwrite(file_bgcbry,[BGCname2_vars{v} '_west'],var) ;
      end
   end

end


