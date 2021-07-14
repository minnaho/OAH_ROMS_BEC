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
yr = '2017'
repavg = dir([rep,'/ussw1_avg.Y',yr,'*.nc']) ;    
% extract all 
%repavg = dir([rep,'/ussw1_avg.Y*.nc']) ;    

% choose the option for CO2SYS 
option1=1; % put 1 if you need to calculate omega using the CO2SYS program

% choose the option for saving temp and chla and other chem
% don't save = 0
% save = 1
option3=0; 

% choose the option for saving Juranek omega
% don't save = 0
% save = 1
option4=0; 

% choose the depths for water column averaging
DD3 = 5; % bottom height - set height above bottom for KBdd 

% name appended at the end of variable name
fname = ['co2sys_bottom_',int2str(DD3),'m_',yr];

%%%%%%%%%%%%%%%%%%
% end user edits
%%%%%%%%%%%%%%%%%%


%% definitions used to create the netdcf empty files
%gp
% DICatm
ncvar_DICatm='var';
shortname_DICatm='DICatm';
longname_DICatm='DICatm at equilibrium with atmospheric CO2';
unit_DICatm='umol kg-1';
% total depth
ncvar_dep='var';
shortname_dep='dep';
longname_dep='total depth from surface to bottom';
unit_dep='meters';
% zeta
ncvar_zeta='var';
shortname_zeta='zeta';
longname_zeta='water surface elevation';
unit_zeta='meters';
% salt
ncvar_salt='var';
shortname_salt='sal';
longname_salt='salinity';
unit_salt='psu';
% po4
ncvar_po4='var';
shortname_po4='po4';
longname_po4='phosphate (po4./(dens.*0.001))';
unit_po4='umol kg-1';   %gp v18 uses units of mmol m-3, v19 converts to umol/kg
% sio3
ncvar_sio3='var';
shortname_sio3='sio3';
longname_sio3='silicate (sio3./(dens.*0.001))';
unit_sio3='umol kg-1';   %gp v18 uses units of mmol m-3, v19 converts to umol/kg
% DIC
ncvar_dic='var';
shortname_dic='dic';
longname_dic='dissolved inorganic carbon (DIC./(dens.*0.001))';
unit_dic='umol kg-1';
% TA
ncvar_alk='var';
shortname_alk='alk';
longname_alk='total alkalinity (Alk./(dens.*0.001))';
unit_alk='umol kg-1';
% temperature
ncvar_temp='var';
shortname_temp='temp';
longname_temp='temperature';
unit_temp='deg C';
% chlorophyll a
ncvar_chla='var';
shortname_chla='chla';
longname_chla='chlorophyll a';
unit_chla='mg m-3';   % volumetric conc of chla
unit_chla_areal='mg m-2';   % water column integrated areal chla 
% o2
ncvar_o2='var';
shortname_o2='o2';
longname_o2='dissolved oxygen';
unit_o2='mmol m-3';
% pH (total)
ncvar_pH='var';
shortname_pH='pH';
longname_pH='pH (total scale)';
unit_pH='total scale';
% pH (SWS)
%ncvar_pHsws='var';
%shortname_pHsws='pHsws';
%longname_pHsws='pH (seawater scale)';
%unit_pHsws='seawater scale';
% pCO2 (uatm)
ncvar_pCO2='var';
shortname_pCO2='pCO2';
longname_pCO2='pCO2';
unit_pCO2='uatm';
% xCO2 (ppm)
%ncvar_xCO2='var';
%shortname_xCO2='xCO2';
%longname_xCO2='xCO2';
%unit_xCO2='ppm';
% RF (Revelle Factor)
ncvar_RF='var';
shortname_RF='RF';
longname_RF='Revelle Factor';
unit_RF='dimensionless';
% cal (omega calcite)
%ncvar_omcal='var';
%shortname_omcal='om_cal';
%longname_omcal='omega calcite saturation state';
%unit_omcal='dimensionless';
% om (omega aragonite)
ncvar_omara='var';
shortname_omara='om_ara';
longname_omara='omega aragonite saturation state';
unit_omara='dimensionless';

% create empty nc files for writing output

% CO2SYS outputs
% pHsws (pHsws)
%fout1_pHsws_KB5_co2sys =   [fdir,fname,'_pHsws.nc'];
% pH (pHtotal)
fout1_pH_KB5_co2sys =   [fdir,'pH_',fname,'.nc'];
% pCO2 (uatm)
fout1_pCO2_KB5_co2sys =   [fdir,'pCO2_',fname,'.nc'];
% xCO2 (ppm)
%fout1_xCO2_KB5_co2sys =   [fdir,'xCO2_',fname,'.nc'];
% RF (Revelle Factor)
fout1_RF_KB5_co2sys =   [fdir,'RF_',fname,'.nc'];
% cal (omega calcite)
%fout1_omcal_KB5_co2sys =   [fdir,'omcal_',fname,'.nc'];
% om (omega aragonite)
fout1_omara_KB5_co2sys =   [fdir,'omega_ara_',fname,'.nc'];

if option1==1
%create_netcdf3D_L1(fout1);
% CO2SYS w/ Lueker et al 2000 using dep-wt avg
% pHsws (seawater scale)
%create_netcdf3D_L1(fout1_pHsws_KB5_co2sys,ncvar_pHsws,shortname_pHsws,longname_pHsws,unit_pHsws);   
% pH (total scale)
create_netcdf3D_L1(fout1_pH_KB5_co2sys,ncvar_pH,shortname_pH,longname_pH,unit_pH);
% pCO2 (pCO2)
create_netcdf3D_L1(fout1_pCO2_KB5_co2sys,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   
% xCO2 (xCO2)
%create_netcdf3D_L1(fout1_xCO2_KB5_co2sys,ncvar_xCO2,shortname_xCO2,longname_xCO2,unit_xCO2);   
% RF (Revelle Factor)
create_netcdf3D_L1(fout1_RF_KB5_co2sys,ncvar_RF,shortname_RF,longname_RF,unit_RF);   
% omcal (omega calcite)
%create_netcdf3D_L1(fout1_omcal_KB5_co2sys,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);
% omara (omega aragonite)
create_netcdf3D_L1(fout1_omara_KB5_co2sys,ncvar_omara,shortname_omara,longname_omara,unit_omara);

end   % if option1==1

% Juranek outputs
if option4 == 1
fout2_KB5 =   [fdir,fname,'_om_juranek_KB5dw.nc'];
create_netcdf3D_L1(fout2_KB5,ncvar_omara,shortname_omara,longname_omara,unit_omara);  % Juranek using depwt avg
end    % if option4

% chem outputs
if option3==1   % save temp and chla and other chem
% salt
fout1_salt_KB5 =   [fdir,fname,'_salt_KB5dw.nc'];
% po4
fout1_po4_KB5 =   [fdir,fname,'_po4_KB5dw.nc'];
% sio3
fout1_sio3_KB5 =   [fdir,fname,'_sio3_KB5dw.nc'];
% alk
fout1_alk_KB5 =   [fdir,fname,'_alk_KB5dw.nc'];
% dic
fout1_dic_KB5 =   [fdir,fname,'_dic_KB5dw.nc'];
% temp
fout1_temp_KB5 =   [fdir,fname,'_temp_KB5dw.nc'];
% chla
fout1_chla_KB5 =   [fdir,fname,'_chla_KB5dw.nc'];
fout1_chla_areal =   [fdir,fname,'_chla_areal.nc'];  
% o2
fout1_o2_KB5 =   [fdir,fname,'_o2_KB5dw.nc'];

% salt
create_netcdf3D_L1(fout1_salt_KB5,ncvar_salt,shortname_salt,longname_salt,unit_salt);  
% po4
create_netcdf3D_L1(fout1_po4_KB5,ncvar_po4,shortname_po4,longname_po4,unit_po4);  
% sio3
create_netcdf3D_L1(fout1_sio3_KB5,ncvar_sio3,shortname_sio3,longname_sio3,unit_sio3);  
% dic
create_netcdf3D_L1(fout1_dic_KB5,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
% alk
create_netcdf3D_L1(fout1_alk_KB5,ncvar_alk,shortname_alk,longname_alk,unit_alk);  
% temp
create_netcdf3D_L1(fout1_temp_KB5,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
% chla
create_netcdf3D_L1(fout1_chla_KB5,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_chla_areal,ncvar_chla,shortname_chla,longname_chla,unit_chla_areal);  
% o2
create_netcdf3D_L1(fout1_o2_KB5,ncvar_o2,shortname_o2,longname_o2,unit_o2);  

end   % if option3





