addpath(genpath('/data/project3/kesf/tools_matlab/'))
addpath('/data/project3/kesf/tools_roms/B2B/packages')

grdname = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc';
load_grid_L2_SCB

%% ten years
lat_rivers_new ;
lon_rivers_new ;
% find the location of I and J
x = ln_riv (1:48);
y = lt_riv (1:48);
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
num=size(x) ;

Isrc(1:num)  = mplat ;
Jsrc(1:num)  = mplon ;
%% Dsrc
Dsrc3 = ones(length(x),1) .* 2 ;

%% 24 years
% find the location of I and J
lat_rivers_new ;
lon_rivers_new ;

x = ln_riv(49:72) ;
y = lt_riv(49:72) ;
num2=size(x) ;
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Isrc(49:72)  = mplat ;
Jsrc(49:72)  = mplon ;

%% Dsrc
Dsrc4 = ones(length(x),1) .* 2 ;



