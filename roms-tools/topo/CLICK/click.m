
 load coast_pac
%load coast_cali

  clon = clon + 360;
  clon = clon + 0.01;

 gridfile = '../nepac4km_grd.nc';

lon = ncread(gridfile,'lon_rho')';
 [m,n] = size(lon);
 if 1
   i0 =    1;
   i1 =    n;
   j0 =    1;
   j1 =    m;
 else
  i0 =  round(0*n/4)+1;
  i1 =  round(3*n/4);
  j0 =  round(1.5*m/4+1);
  j1 =  round(4.0*m/4);
  i0 =  460-200;
  i1 =  460+200;
  j0 =  1040-200;
  j1 =  1040+200;
 end

lon = ncread(gridfile,'lon_rho')';
lat = ncread(gridfile,'lat_rho')';
lon = lon(j0:j1,i0:i1);
lat = lat(j0:j1,i0:i1);

if 0
  lonp = nc{'lon_psi'}(j0:j1-1,i0:i1-1);
  latp = nc{'lat_psi'}(j0:j1-1,i0:i1-1);
else
  lonp = 0.25*(lon(1:end-1,1:end-1)+lon(2:end,1:end-1)+lon(1:end-1,2:end)+lon(2:end,2:end));
  latp = 0.25*(lat(1:end-1,1:end-1)+lat(2:end,1:end-1)+lat(1:end-1,2:end)+lat(2:end,2:end));
end
hraw = ncread(gridfile,'h')';
hraw = hraw(j0:j1,i0:i1);
mask = ncread(gridfile,'mask_rho')';
mask = mask(j0:j1,i0:i1);
%lon(lon<0) = lon(lon<0) + 360;
%lonp(lonp<0) = lonp(lonp<0) + 360;
i = 1;j=1;
lon0 = mean(mean(lon));
lat0 = mean(mean(lat));

%[lon,lat] = gnomonic(lon,lat,lon0,lat0);
%[lonp,latp] = gnomonic(lonp,latp,lon0,lat0);

sc1 = max(max(hraw));
sc1 = 500;
sc1 =  50;
sc0 =-2*sc1/255;
%
 figure('WindowButtonDownFcn',{@wbdcb,i,j,lon,lat,lonp,latp,hraw,mask,sc0,sc1})


%mypcolor(lon,lat,h.*mask)
nmask = 0*mask;
nmask(~mask) = -1e5;
mypcolor(lon(2:end-1,2:end-1),lat(2:end-1,2:end-1),hraw(2:end-1,2:end-1)+nmask(2:end-1,2:end-1))
clear jet
cm = colormap(jet(256));
cm(1,:) = [204 153 0]/255;
colormap(cm);
caxis([sc0 sc1]);
hold on
plot(clon,clat,'k','linewidth',1.5)
title('Easy edit')
