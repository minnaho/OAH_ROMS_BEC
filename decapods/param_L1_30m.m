%% load the grid
load_grid_ussw1

%% choose the option
option1=0; % put 1 if you need to calculate omega using the CO2SYS program
%% choose the depth DD
DD1 = 30; % set bottom depth
DD2 = 0; % set top depth

%% create the netdcf empty files
if option1==1
fout1 =   '/data/project3/kesf/tools_matlab/applications/pteropods/om_co2sys_L1.nc';
create_netcdf3D_L1(fout1);
end
fout2 =   '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_30m_2001.nc';
create_netcdf3D_L1(fout2);

%% find the modle outputs directories
rep = '/data/project3/kesf/ROMS/USSW1/DAILY/' ;
%% list the model outputs
%repavg = dir([rep,'/ussw1_avg.Y1999*.nc']) ;
repavg = dir([rep,'/ussw1_avg.Y2001*.nc']) ;



