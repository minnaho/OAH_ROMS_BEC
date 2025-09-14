% Interpolate Tau additive correction

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all
close all
 
grdpar = '/data/project8/pdamien/ROMS_outputs/PACMED12KMnew/FORCINGS/pacmed12_grd.nc' ;  
corrfile = 'TAUcorr_PACMED12KM_2000_2010_Upt.mat' ;
grdchd = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_grd.nc' ;
corrupt = 'TAUcorr_PACGIG2KMfull_2000_2010.mat' ; 

lon = ncread( grdpar , 'lon_rho' );
lat = ncread( grdpar , 'lat_rho' );
msk = ncread( grdpar , 'mask_rho');
angle = ncread( grdpar , 'angle');
lon(lon<0) = lon(lon<0)+360 ;
[nx,ny] = size(lon) ; 

lonchd = ncread( grdchd , 'lon_rho' );
latchd = ncread( grdchd , 'lat_rho' );
mskchd = ncread( grdchd , 'mask_rho');
anglechd = ncread( grdchd , 'angle');
lonchd(lonchd<0) = lonchd(lonchd<0)+360 ;

load(corrfile)

for m=1:12
m
tauX = squeeze(Tau_correc.TauX_corr(:,:,m)) ; 
tauY = squeeze(Tau_correc.TauY_corr(:,:,m)) ;
tauE = cos(angle) .* tauX - sin(angle) .* tauY ;
tauN = sin(angle) .* tauX + cos(angle) .* tauY ;
tauE_interp = griddata(lon,lat,tauE,lonchd,latchd) ; 
tauN_interp = griddata(lon,lat,tauN,lonchd,latchd) ;
tauE_interp = inpaint_nans(tauE_interp,2) ; 
tauN_interp = inpaint_nans(tauN_interp,2) ;
tauX_interp(:,:,m) =  cos(anglechd).*tauE_interp + sin(anglechd).*tauN_interp ;
tauY_interp(:,:,m) = -sin(anglechd).*tauE_interp + cos(anglechd).*tauN_interp ;
end

clear Tau_correc
Tau_correc.TauX_corr = tauX_interp ; 
Tau_correc.TauY_corr = tauY_interp ;
save(corrupt,'Tau_correc','-v7.3') ;





return


