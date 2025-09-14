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
grdname = '/data/project8/pdamien/ROMS_outputs/ATLSMA25KM/FORCINGS/atlsma_grd.nc' ; 
ininame = '/data/project8/pdamien/ROMS_outputs/ATLSMA25KM/FORCINGS/atlsma_ini19950101_3loop.nc' ;
time_ref = datenum(1995,1,1) ; % reference time for ROMS`
%
BGCname_vars = {'NO3' 'PO4' 'SiO3' 'O2' 'Fe' 'DIC' 'Alk' 'N2O' 'SPC' 'SPCHL' 'SPFE' ...
                 'SPCACO3' 'DIATC' 'DIATCHL' 'DIATFE' 'DIATSI' 'DIAZC' 'DIAZCHL' 'DIAZFE' ...
                 'ZOOC' 'DON' 'DONR' 'DOP' 'DOPR' 'DOFE' 'NH4' 'DOC' 'NO2' 'N2'} ;
bgc_file = '/data/project8/pdamien/ROMS_outputs/ATLSMA25KM/RUN/LOOP3/Y2020/atlsma_rst.20210101120000.nc' ;  
%                                       
create_SEDVAR = 1 ; %% create the sediment tracer if not already in the init fle
create_VAR = 0    ; %% create the 3d tracer if not already in the init fle
smoothX = 4       ; %% Smoothing kernel in grid points, PD: I use 4 to interpolate the rst BGC on the Glorys physics
%
%---------------------------------------------------------------------------------------
% USER-DEFINED VARIABLES & OPTIONS END HERE
%---------------------------------------------------------------------------------------
%
%% Read salinity and temperature in restart file
salt_rst = ncread(bgc_file,'salt',[1 1 1 1],[inf inf inf 1]) ; 
temp_rst = ncread(bgc_file,'temp',[1 1 1 1],[inf inf inf 1]) ;
dens_rst = real(sw_dens0(salt_rst,temp_rst)) ;
mask = squeeze(ncread(bgc_file,'temp',[1 1 1 1],[inf inf 1 1])) ; 
mask(mask~=0)=1 ; 

[nx ny nz] = size(temp_rst) ; 

%% Add Sediment Vars
if create_SEDVAR==1 
nccreate(ininame,'Sed_POC','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',1},'datatype','single');
nccreate(ininame,'Sed_CaCO3','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',1},'datatype','single');
nccreate(ininame,'Sed_Si','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',1},'datatype','single');
end
var = ncread(bgc_file,'Sed_POC',[1 1 1],[inf inf 1]) ; 
ncwrite(ininame,'Sed_POC',var) ; 
var = ncread(bgc_file,'Sed_CaCO3',[1 1 1],[inf inf 1]) ;
ncwrite(ininame,'Sed_CaCO3',var) ;
var = ncread(bgc_file,'Sed_Si',[1 1 1],[inf inf 1]) ;
ncwrite(ininame,'Sed_Si',var) ;

%% Read, and prepare density fields 
salt_ini = ncread(ininame,'salt',[1 1 1 1],[inf inf inf 1]) ;
temp_ini = ncread(ininame,'temp',[1 1 1 1],[inf inf inf 1]) ;
dens_ini = real(sw_dens0(salt_ini,temp_ini)) ;
for z=nz-1:-1:1
    test = dens_rst(:,:,z) + z*0.0000001 ;
    test(mask==0) = NaN ; 
    dens_rst(:,:,z) = inpaint_nans(test,2) ;
    test = dens_ini(:,:,z) + z*0.0000001 ;
    test(mask==0) = NaN ;
    dens_ini(:,:,z) = inpaint_nans(double(test),2) ; 
end

%% Read, smooth, vert. interpolate, and write var
for v=1:length(BGCname_vars)
    disp(['Working on ' BGCname_vars{v}])
    var = ncread(bgc_file,BGCname_vars{v},[1 1 1 1],[inf inf inf 1]) ; 
    for z=1:nz
        var2d = squeeze(var(:,:,z)) ; 
        var2d(mask==0)=NaN ; 
        var2d = smooth2a(var2d,smoothX,smoothX) ; 
        var2d = inpaint_nans(var2d,2) ;
        var(:,:,z) = var2d ; 
    end
    var_int=zeros(nx,ny,nz) ;
    for i=1:nx
    for j=1:ny
        if mask(i,j)==0
        var_int(i,j,:) = NaN ;
        else
        testvec = interp1(squeeze(dens_rst(i,j,:)),squeeze(var(i,j,:)), ...
                          squeeze(dens_ini(i,j,:)));
        var_int(i,j,:) = fillmissing(testvec,'nearest') ;
        end
    end
    end
    for z=1:1:nz
        var2d =  inpaint_nans(squeeze(var_int(:,:,z)),2) ; 
        var2d = smooth2a(var2d,smoothX,smoothX) ;
        var_int(:,:,z) = var2d ;
    end
    if  create_VAR==1
    nccreate(ininame,BGCname_vars{v},'Dimensions',{'xi_rho',nx,'eta_rho',ny,'s_rho',nz,'time',1},'datatype','single');
    end
    ncwrite(ininame,BGCname_vars{v},var_int,[1 1 1 1]) ;
end

disp('DONE')


