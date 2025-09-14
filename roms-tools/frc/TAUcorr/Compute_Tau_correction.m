% compute Tau additive correction

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all
 
rho0=1027.4 ; 

pargrd = './scow2010_ctao_mf.nc';
grdname = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_grd.nc' ;  
rep = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/RUN/LOOP3/' ;  
add2old = 1 ; 
corr2update = 'TAUcorr_PACMED25KM_2000_2010.mat' ; 

tauX_scow = ncread(pargrd,'tau_x') ; 
tauY_scow = ncread(pargrd,'tau_y') ;
lon_scow = ncread(pargrd,'lon') ;
lat_scow = ncread(pargrd,'lat') ;

lon = ncread( grdname , 'lon_rho' );
lat = ncread( grdname , 'lat_rho' );
msk = ncread( grdname , 'mask_rho');
angle = ncread( grdname , 'angle');
lon(lon<0) = lon(lon<0)+360 ;
[nx,ny] = size(lon) ; 

for m=1:12
tauX = interp2(lat_scow,lon_scow,squeeze(tauX_scow(:,:,m)),lat,lon) ; 
tauY = interp2(lat_scow,lon_scow,squeeze(tauY_scow(:,:,m)),lat,lon) ;
tauX_rotated =  cos(angle) .*  tauX + sin(angle) .*  tauY ;
tauY_rotated = -sin(angle) .*  tauX + cos(angle) .*  tauY ;
tauX_scow_interp(:,:,m) = tauX_rotated ;
tauY_scow_interp(:,:,m) = tauY_rotated ;
end


list = dir([rep 'Y*/pacmed_flx_avg*.nc']) ;
list = list(6:16) ;
sustr = zeros(nx-1,ny,12) ; svstr = zeros(nx,ny-1,12) ; 
for t=1:length(list)
    file = [list(t).folder '/' list(t).name]
    sustr = sustr + ncread(file,'sustr')*rho0 ; 
    svstr = svstr + ncread(file,'svstr')*rho0 ;
end
sustr=sustr./length(list) ; 
svstr=svstr./length(list) ;

sustr_r = zeros(nx,ny,12).*NaN ; 
sustr_r(2:end-1,:,:) = 0.5.*(sustr(1:end-1,:,:)+sustr(2:end,:,:)) ; 
svstr_r = zeros(nx,ny,12).*NaN ;
svstr_r(:,2:end-1,:) = 0.5.*(svstr(:,1:end-1,:)+svstr(:,2:end,:)) ;
for m=1:12
sustr_r(:,:,m) = inpaint_nans(squeeze(sustr_r(:,:,m)),2) ;
svstr_r(:,:,m) = inpaint_nans(squeeze(svstr_r(:,:,m)),2) ;
end

if add2old
load(corr2update) 
end

if 0 
figure
subplot(1,2,1)
pcolor(lon,lat, mean(tauX_scow_interp,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.15 0.15]) ; title('scow X')
subplot(1,2,2)
pcolor(lon,lat, mean(sustr_r,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.15 0.15]) ; title('roms run')

figure
subplot(1,2,1)
pcolor(lon,lat, mean(Tau_correc.TauX_corr,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.03 0.03]) ; title('old correc X')
subplot(1,2,2)
pcolor(lon,lat, mean(tauX_scow_interp,3)-mean(sustr_r,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.03 0.03]) ; title('new corr 2 add')

figure
subplot(1,2,1)
pcolor(lon,lat, mean(tauY_scow_interp,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.15 0.15]) ; title('scow Y')
subplot(1,2,2)
pcolor(lon,lat, mean(svstr_r,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.15 0.15]) ; title('roms run')

figure
subplot(1,2,1)
pcolor(lon,lat, mean(Tau_correc.TauY_corr,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.03 0.03]) ; title('old correc Y')
subplot(1,2,2)
pcolor(lon,lat, mean(tauY_scow_interp,3)-mean(svstr_r,3)) ;
shading flat ; colorbar ; colormap(jet) ;
caxis([-0.03 0.03]) ; title('new corr 2 add')
end


disp('UPDATE the correction by first adding the new correction, ')
disp('then smooth, then remove coastal correction, and inpaint on land')

cdist = comp_cdist_full(grdname,'dummy',0);
cdist = cdist/1e3;
mult = 1-1*exp(-0.005*cdist);
if 0
figure ; pcolor(mult) ; shading flat ; colorbar ; caxis([0 1])
end

for m=1:12
    var = Tau_correc.TauX_corr(:,:,m) + tauX_scow_interp(:,:,m)- sustr_r(:,:,m) ;
    var(msk==0) = NaN ; var = var.*mult ; 
    var = inpaint_nans(var,2) ; 
    TauX_corr(:,:,m) = var ; 
    var = Tau_correc.TauY_corr(:,:,m) + tauY_scow_interp(:,:,m)- svstr_r(:,:,m) ;
    var(msk==0) = NaN ; var = var.*mult ;
    var = inpaint_nans(var,2) ;
    TauY_corr(:,:,m) = var ;
end

Tau_correc.TauX_corr = TauX_corr ; 
Tau_correc.TauY_corr = TauY_corr ;
save('TAUcorr_PACMED25KM_2000_2010_Upt.mat','Tau_correc') ;





return


