% interpolated average (weighted average by depth steps)
%% load the grid
load_grid_ussw1
bgc=1

%% choose the option
option1=1; % put 1 if you need to calculate omega using the CO2SYS program
%% choose bottom depth, averages between DD0-DD1
DD0= 100; 
DD1 = 1150; 
step = 20 % depth step to weight over

%% create the netdcf empty files
if option1==1
fout1 =   ['/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_',num2str(DD0),'_',num2str(DD1),'m_int.nc'];
ncvar='var';
shortname='pH';
longname='pH input (Total) from CO2SYS';
unit='';
create_netcdf3D_L1(fout1,ncvar,shortname,longname,unit);
else
fout2 =   ['/data/project1/minnaho/decapods/extract_nc/om_juranek_L1_',num2str(DD0),'_',num2str(DD1),'m_int.nc'];
ncvar='var';
shortname='omega';
longname='omega aragonite saturation state from Juranek et al 2014';
unit='';
create_netcdf3D_L1(fout2,ncvar,shortname,longname,unit);
end


%% find the modle outputs directories
rep = '/data/project5/kesf/ROMS/USSW1/daily/' ;
%% list the model outputs
repavg = dir([rep,'/ussw1_avg.Y*.nc']) ;
%repavg = dir([rep,'/ussw1_avg.Y2001*.nc']) ;



