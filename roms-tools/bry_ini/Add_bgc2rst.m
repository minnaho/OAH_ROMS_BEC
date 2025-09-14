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
grdname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_grd.nc' ; 
ininame = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_rst19960101.nc' ;
time_ref = datenum(1995,1,1) ; % reference time for ROMS`
%
% CASE 1 : vars to read from file and interpolate on density profile  
BGCname1_vars = {'NO3' 'PO4' 'SiO3' 'O2' 'Fe' 'DIC' 'Alk' 'N2O' 'CHL'} ;
bgc_file = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/BGC/pacmed_0p25_bgc_*.nc' ;  
% CASE 2 : vars derived from other vars 
BGCname2_vars = {'SPC' 'SPCHL' 'SPFE' 'SPCACO3' 'DIATC' 'DIATCHL' 'DIATFE' 'DIATSI' 'DIAZC' 'DIAZCHL' 'DIAZFE' 'ZOOC'} ;
BGCname2_coef = [3.375 0.675 1.35e-05  0.0675   0.2025   0.0675   1.35e-06  0.0675   0.0375   0.0075  7.5e-07   1.35] ;
BGCname2_vref = {'CHL' 'CHL'   'CHL'   'CHL'    'CHL'      'CHL'    'CHL'    'CHL'   'CHL'     'CHL'   'CHL'   'CHL'} ;
% CASE 3 : vars set as constant value
BGCname3_vars = {'DON' 'DONR' 'DOP' 'DOPR' 'DOFE' 'NH4' 'DOC' 'NO2' 'N2'} ;
BGCname3_coef = [ 1     0.8    0.1  0.003  0.0001  1e-6  1e-6 1e-6  1e-6] ;
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%
% Find time
list = dir(bgc_file) ;
for t=1:length(list)
    file = [list(t).folder '/' list(t).name] ; 
    frc_time(t) = ncread(file,'time')  ;
    idx_time(t) = t ; 
end
frc_time = [frc_time(end)-365.25 frc_time 365.25+frc_time(1)] ;
idx_time = [12 idx_time 1] ; 

msk = ncread(grdname,'mask_rho') ; 

ini_time = double(ncread(ininame,'ocean_time')/(24*60*60) + time_ref) ;
ini_day = ini_time - datenum(str2num(datestr(ini_time,'yyyy')),1,1) ;

NT = length(ini_time) ; 

%% Add BGC variables to rst file
file_t0 = [list(1).folder '/' list(1).name] ;
vardim = squeeze(ncread(ininame,'salt',[1 1 1 1],[inf inf inf 1])) ;
[nx,ny,nz] = size(vardim) ;
for v=1:length(BGCname1_vars)
    nccreate(ininame,BGCname1_vars{v},'Dimensions',{'xi_rho',nx,'eta_rho',ny,'s_rho',nz,'time',NT},'datatype','single');
    varat = ncreadatt(file_t0,BGCname1_vars{v},'long_name') ;
    ncwriteatt(ininame,BGCname1_vars{v},'long_name',varat);
    varat = ncreadatt(file_t0,BGCname1_vars{v},'units') ;
    ncwriteatt(ininame,BGCname1_vars{v},'units',varat);
end
for v=1:length(BGCname2_vars)
    nccreate(ininame,BGCname2_vars{v},'Dimensions',{'xi_rho',nx,'eta_rho',ny,'s_rho',nz,'time',NT},'datatype','single');
end
for v=1:length(BGCname3_vars)
    nccreate(ininame,BGCname3_vars{v},'Dimensions',{'xi_rho',nx,'eta_rho',ny,'s_rho',nz,'time',NT},'datatype','single');
end

%% Loop over time

for t=1:NT

disp(['Working in time :' num2str(t)])

t0 = find(frc_time<=ini_day(t),1,'last');
t1 = find(frc_time>ini_day(t),1,'first');
coeft(1) = idx_time(t0) ; 
coeft(2) = idx_time(t1) ;
coeft(3) = (ini_day(t)-frc_time(t0)) / (frc_time(t1)-frc_time(t0)) ;  

%%% initial density
for z=1:nz 
    salt = squeeze(ncread(ininame,'salt',[1 1 z t],[inf inf 1 1])) ; 
    temp = squeeze(ncread(ininame,'temp',[1 1 z t],[inf inf 1 1])) ;
    salt(salt<1.0) = 1.0 ; temp(temp<-1.80) = -1.8 ; 
    rho = sw_dens0(salt,temp) ; rho(msk==0) = NaN ;
    dens_int(:,:,z) = inpaint_nans(rho,2)  ;
end
[nx,ny,nz] = size(dens_int) ; 
for z=nz-1:-1:1
    dens_int(:,:,z) = dens_int(:,:,z) + z*0.0000001 ; 
end

%%% interpolate CASE 1
file_t0 = [list(coeft(1)).folder '/' list(coeft(1)).name] ; 
dens_t0 = double(sw_dens0(ncread(file_t0,'salt'),ncread(file_t0,'temp'))) ;
file_t1 = [list(coeft(2)).folder '/' list(coeft(2)).name] ;
dens_t1 = double(sw_dens0(ncread(file_t1,'salt'),ncread(file_t1,'temp'))) ;
dens_ini = coeft(3).*dens_t0 + (1-coeft(3)).*dens_t1 ;
clear dens_t0 dens_t1
for z=nz-1:-1:1
    dens_ini(:,:,z) = dens_ini(:,:,z) + z*0.0000001 ;
end
for v=1:length(BGCname1_vars)
    disp(['  Working on ' BGCname1_vars{v}])
    var_t0 = ncread(file_t0,BGCname1_vars{v}) ; 
    var_t1 = ncread(file_t1,BGCname1_vars{v}) ;
    var_ini = coeft(3).*var_t0 + (1-coeft(3)).*var_t1 ;
    clear var_t0 var_t1
    var_int=zeros(nx,ny,nz) ; 
    for i=1:nx
    for j=1:ny
%    var_int(i,j,:) = interp1(squeeze(dens_ini(i,j,:)),squeeze(var_ini(i,j,:)), ...
%                             squeeze(dens_int(i,j,:)),'nearest','extrap');
        testvec = interp1(squeeze(dens_ini(i,j,:)),squeeze(var_ini(i,j,:)), ...
                          squeeze(dens_int(i,j,:)));
        var_int(i,j,:) = fillmissing(testvec,'nearest') ;
    end
    end
    for z=1:1:nz
        var_int(:,:,z) = inpaint_nans(squeeze(var_int(:,:,z)),2) ; 
    end
    ncwrite(ininame,BGCname1_vars{v},var_int,[1 1 1 t]) ; 
end

%%% interpolate CASE 2
for v=1:length(BGCname2_vars)
    disp(['  Working on ' BGCname2_vars{v}])
    var = BGCname2_coef(v) * ncread(ininame,BGCname2_vref{v},[1 1 1 t],[inf inf inf 1]) ;
    ncwrite(ininame,BGCname2_vars{v},var,[1 1 1 t]) ;
end

%%% interpolate CASE 3
for v=1:length(BGCname3_vars)
    disp(['  Working on ' BGCname3_vars{v}])
    var = BGCname3_coef(v) * ones(nx,ny,nz) ;
    ncwrite(ininame,BGCname3_vars{v},var,[1 1 1 t]) ;
end

end


