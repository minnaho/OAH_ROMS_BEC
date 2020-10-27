%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% This program is design to 
%% find Isrc and Jsrc for
%% POTW Outfalls
%% L2_SCB (dx = 300m)
%% Faycal Kessouri
%% 05/04/2018
%% SCCWRP/UCLA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% HTP JWPCP OCSD PLWTP

addpath(genpath('/data/project3/kesf/tools_matlab/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc';
load_grid_L2_SCB

%% HTP
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[33.9118 33.9206];
x=[-118.521 -118.529];
for i=1:length(x)
        [pplat(i), pplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
%N

plat(1) = pplat(1)-1  ;
plat(2) = pplat(1)-2  ;
plon(1) = pplon(1) ;
plon(2) = pplon(1) ;
%S
plat(3) = pplat(2)  ;
plat(4) = pplat(2)  ;
plon(3) = pplon(2)+1 ;
plon(4) = pplon(2)+2 ;

Jsrc(1,1:4) = plat(1:4) ; Isrc(1,1:4) = plon(1:4) ;

%% JWPCP
clear Isrc1 Jsrc1 plat plon x y NSRC

y=[33.7008 33.700737 33.697917 33.6892];  % Y: joint_N N S     L: S2
x=[-118.3381 -118.341962 -118.335836 -118.3167];
ly = 33.718374 ;
lx = -118.3214 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
plat(5) = plat(4)  ;
plon(5) = plon(4)+1  ;
%plat(6) = plat(4)  ;
%plon(6) = plon(4)+2  ;

%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,5:9) = plat(1:5) ; Isrc(1,5:9) = plon(1:5) ;

%% OCSD
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[33.576667];  % main diffuser is 1 junction is 2 . it's an L shape outfall: Diffuser junction_point
x=[-118.01];
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
plat(2) = plat(1)+1  ;
plon(2) = plon(1)  ;
plat(3) = plat(2)  ;
plon(3) = plon(2)+1  ;
plat(1) = plat(2)+1  ;
plon(1) = plon(2)  ;

%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,10) = plat(1) ; Isrc(1,10) = plon(1) ;
Jsrc(1,11) = plat(3) ; Isrc(1,11) = plon(3) ;

%% PLWTP
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[32.665245 32.671671];
x=[-117.323336 -117.325556];
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
%N
plat(3) = plat(1)+1  ;
plon(3) = plon(1) ;
%S
plat(4) = plat(2)  ;
plon(4) = plon(2)-1 ;
%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,12:15) = plat(1:4) ; Isrc(1,12:15) = plon(1:4) ;

clear NSRC

return



