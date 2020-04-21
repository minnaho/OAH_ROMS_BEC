%% load the grid
load_grid_ussw1

%% choose the option
option1=0; % put 1 if you need to calculate omega using the CO2SYS program
%% choose the depth DD
DD1 = 200; % set bottom depth
DD2 = 0; % set top depth

%% create the netdcf empty files
fout2 =   '/data/project3/kesf/tools_matlab/applications/pteropods/total_prod_L1_200m_1997_2007.nc';
create_netcdf3D_L1(fout2);

%% find the modle outputs directories
rep = '/data/project4/kesf/ROMS/USSW1/BGC_DAILY/' ;
%% list the model outputs
%repavg = dir([rep,'/ussw1_avg.Y1999*.nc']) ;
repavg = dir([rep,'/ussw1_bgc.Y*.nc']) ;

rep_avg = '/data/project3/kesf/ROMS/USSW1/DAILY/';
repavg_avg = dir([rep_avg,'/ussw1_avg.Y*.nc']);



