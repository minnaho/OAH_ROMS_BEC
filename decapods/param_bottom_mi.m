% extract metabolic index parameters
% at the seafloor
% temp, O2, density

%% load the grid
load_grid_ussw1


%%%%%%%%%%%%%%%%%%
% begin user edits
%%%%%%%%%%%%%%%%%%

% name and directory to be used for output nc files from the extract_2D script
fdir = '/data/project1/minnaho/decapods/extract_nc/';

% edit the model outputs directories and select which years
rep = '/data/project6/ROMS/USSW1/daily/' ;

% extract by year
%yr = '2017'
%repavg = dir([rep,'/ussw1_avg.Y',yr,'*.nc']) ;    

% extract all 
repavg = dir([rep,'/ussw1_avg.Y*.nc']) ;    

% bottom height - set height above bottom for KBdd 
DD3 = 5; 

% name appended at the end of variable name
%fname = ['bottom_',int2str(DD3),'m_',yr];
fname = ['bottom_',int2str(DD3),'m'];

%%%%%%%%%%%%%%%%%%
% end user edits
%%%%%%%%%%%%%%%%%%


%% definitions used to create the netdcf empty files
%gp
% temperature
ncvar_tem='var';
shortname_tem='temp';
longname_tem='temperature';
unit_tem='deg C';
% o2
ncvar_doo='var';
shortname_doo='o2';
longname_doo='dissolved oxygen';
unit_doo='mmol m-3';
% density
ncvar_rho='var';
shortname_rho='temp';
longname_rho='temperature';
unit_rho='kg m-3';

% create empty nc files for writing output

% outputs
fout1_tem =   [fdir,'temp_',fname,'.nc'];
fout1_doo =   [fdir,'o2_',fname,'.nc'];
fout1_rho =   [fdir,'rho_',fname,'.nc'];

create_netcdf3D_L1(fout1_tem,ncvar_tem,shortname_tem,longname_tem,unit_tem);
create_netcdf3D_L1(fout1_doo,ncvar_doo,shortname_doo,longname_doo,unit_doo);   
create_netcdf3D_L1(fout1_rho,ncvar_rho,shortname_rho,longname_rho,unit_rho);   


