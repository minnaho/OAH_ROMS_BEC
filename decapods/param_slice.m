%% load the grid
load_grid_ussw1

%% choose the option
option1=1; % put 1 if you need to calculate omega using the CO2SYS program
%% choose the depth DD
DD1 = 50; % set bottom depth
DD2 = DD1; % set top depth same as bottom depth to get slice

%% create the netdcf empty files
if option1==1
fout1 =   ['/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_',num2str(DD1),'m_slice.nc'];
ncvar='var';
shortname='pH';
longname='pH input (Total) from CO2SYS';
unit='';
create_netcdf3D_L1(fout1,ncvar,shortname,longname,unit);
end
fout2 =   ['/data/project1/minnaho/decapods/extract_nc/om_juranek_L1_',num2str(DD1),'m_slice.nc'];
ncvar='var';
shortname='omega';
longname='omega aragonite saturation state from Juranek et al 2014';
unit='';
create_netcdf3D_L1(fout2,ncvar,shortname,longname,unit);


%% find the modle outputs directories
rep = '/data/project5/kesf/ROMS/USSW1/daily/' ;
%% list the model outputs
repavg = dir([rep,'/ussw1_avg.Y*.nc']) ;
%repavg = dir([rep,'/ussw1_avg.Y2001*.nc']) ;



