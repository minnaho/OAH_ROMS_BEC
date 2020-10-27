


clear all;
close all;
addpath(genpath('/data/project1/kesf/matlab_paths/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid/roms_grd.nc';
load_grid_L2_SCB

z_r = zbot1;
cff=0;
y=[33.9017];
x=[-118.5267];
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Jsrc = plat ;
Isrc  = plon ;

for k=1:NZ
 Zcff=max(2.,h(Isrc,Jsrc)-20.0) ;
Scff=0.15 ;
Xcff = abs(z_r(Isrc,Jsrc,k) - Zcff) ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
end
Qshape = Qs./sum(Qs) ;

% test
plot(Qshape,-squeeze(z_r(Isrc,Jsrc,:)) ,'r')

%% RIVERS
for k=1:NZ
 Zcff= z_r(Isrc,Jsrc,60) ;
Scff=0.15 ;
Xcff = abs(z_r(Isrc,Jsrc,k) - Zcff) ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
end
Qshape = Qs./sum(Qs) ;

% test
hold on
plot(Qshape,-squeeze(z_r(Isrc,Jsrc,:)) ,'g')

legend('POTW','Rivers')
set(gca, 'fontsize',14)
title('Distribution of the AP flux weight')





for k=1:NZ
 Zcff=max(2.,h(Isrc,Jsrc)-10.0) ;
Scff=0.02 ;
Xcff = z_r(Isrc,Jsrc,k)+Zcff ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
            cff=cff+Qs(k) ;
end
for k=1:NZ
            Qs(k)=Qs(k)*cff ;
end   % ! k (vertical)
Qshape = Qs./sum(Qs) ;

% test
plot(Qshape,-squeeze(z_r(Isrc,Jsrc,:)) ,'r')
