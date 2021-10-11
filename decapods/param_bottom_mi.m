% extract metabolic index parameters
% at the seafloor
% temp, O2, density

grid_res = 'L2';

%% load the grid
if grid_res == 'L1'
    load_grid_ussw1 % L1 grid
elseif grid_res == 'L2'
    load_grid_L2_SCB % L2 grid
end


%%%%%%%%%%%%%%%%%%
% begin user edits
%%%%%%%%%%%%%%%%%%

% directory to be used for output ncfile
fdir = '/data/project1/minnaho/decapods/extract_nc/';

% bottom height - set height above bottom for KBdd 
DD3 = 5; 

% edit the model outputs directories and select which years
if grid_res == 'L1'
    rep = '/data/project6/ROMS/USSW1/daily/' ;  % L1
elseif grid_res == 'L2'
    rep = '/data/project6/ROMS/L2SCB/daily_2012_2017/' ;% L2
end

% extract by year
%yr = '2017'
%repavg = dir([rep,'/ussw1_avg.Y',yr,'*.nc']) ;    

% extract all 
if grid_res == 'L1'
    repavg = dir([rep,'/ussw1_avg.Y*.nc']) ; % L1
    fname = ['_bottom_',int2str(DD3),'m'];
elseif grid_res == 'L2'
    repavg = dir([rep,'/l2_scb_avg.Y2017M12*.nc']) ; % L2
    fname = ['L2CT_2012_2017_bottom_',int2str(DD3),'m_2017M12'];
end


% name appended at the end of variable name
%fname = ['bottom_',int2str(DD3),'m_',yr]; % if calculating yearly

%%%%%%%%%%%%%%%%%%
% end user edits
%%%%%%%%%%%%%%%%%%


%% definitions used to create the netdcf empty files
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

if grid_res == 'L1'
    create_netcdf3D_L1(fout1_tem,ncvar_tem,shortname_tem,longname_tem,unit_tem);
    create_netcdf3D_L1(fout1_doo,ncvar_doo,shortname_doo,longname_doo,unit_doo);   
    create_netcdf3D_L1(fout1_rho,ncvar_rho,shortname_rho,longname_rho,unit_rho);   
elseif grid_res == 'L2'
    create_netcdf3D_L2(fout1_tem,ncvar_tem,shortname_tem,longname_tem,unit_tem);
    create_netcdf3D_L2(fout1_doo,ncvar_doo,shortname_doo,longname_doo,unit_doo);   
    create_netcdf3D_L2(fout1_rho,ncvar_rho,shortname_rho,longname_rho,unit_rho);   
end


