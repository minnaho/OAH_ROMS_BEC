%% load the grid
load_grid_ussw1


% begin user edits
% --------------------------------
% --------------------------------
% --------------------------------

% name and directory to be used for output nc files from the extract_2D script
fname ='extract_2D_v28_L1_19972007';
fdir = '/data/project4/gregp/tools_matlab/applications/pteropods/';

% edit the following lines to find the model outputs directories and select which years
% rep = '/data/project3/kesf/ROMS/USSW1/DAILY/' ;   % project5 daily L1 output files do not read correctly, should use project3 instead
rep = '/data/project5/kesf/ROMS/USSW1/daily/' ;
% repavg = dir([rep,'/ussw1_avg.Y2006*.nc']) ;   % to use year 1998 output files
% repavg = dir([rep,'/ussw1_avg.Y2006*.nc']) ;   % to use year 1998 output files
repavg = dir([rep,'/ussw1_avg.Y*.nc']) ;   % to use entire time period of model solution files

% edit the following line to create a string of dates corresponding the model output files in repavg
date = datenum(1997,2,1):datenum(2007,11,30);   % all dates in DAILY
% date = datenum(2006,1,1):datenum(2006,12,31);   % all dates in DAILY
% date = datenum(2006,1,1):datenum(2006,12,31);   % all dates in DAILY
months = str2num(datestr(date,'mm')) ;
years = str2num(datestr(date,'yyyy')) ;

% choose the option for CO2SYS 
option1=1; % put 1 if you need to calculate omega using the CO2SYS program

% choose the option for un-weighted vs depth-weighted water column averaging
option2=1; % put 0 for unweighted, 1 for depth-weighted average

% choose the option for saving temp and chla and other chem
option3=1; % put 0 for no saving of temp and chla and other chem variables, 1 for saving temp and chla and other chem

% choose the option for saving Juranek omega
option4=0; % put 0 for no saving Juranek omega, 1 for saving Juranek omega

% save total depth
option5=0;   % 0= do not save total depth, 1= save total depth

% RCP scenarios using DICexcess and DICatm
option6=0;	% 0=no DICexcess or DICatm, 1=use RCP8.5 xCO2 to calc DICexcess and DICatm, 2=use RCP6.0 xCO2, 3=use RCP4.5 xCO2, 4=use RCP2.6 xCO2 
if option6~=0
	option2=1;   % use dep-wt if using option6
	% only need the following if option6~=0:
	date_1765 = datenum(1765,1,1):datenum(1765,12,31);   % must be at least as many days as the number of days in repavg
	date_2020 = datenum(2020,1,1):datenum(2020,12,31);   % must be at least as many days as the number of days in repavg
	date_2040 = datenum(2040,1,1):datenum(2040,12,31);   % must be at least as many days as the number of days in repavg
	date_2060 = datenum(2060,1,1):datenum(2060,12,31);   % must be at least as many days as the number of days in repavg
	date_2080 = datenum(2080,1,1):datenum(2080,12,31);   % must be at least as many days as the number of days in repavg
	date_2100 = datenum(2100,1,1):datenum(2100,12,31);   % must be at least as many days as the number of days in repavg
	years_1765 = str2num(datestr(date_1765,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
	years_2020 = str2num(datestr(date_2020,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
	years_2040 = str2num(datestr(date_2040,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
	years_2060 = str2num(datestr(date_2060,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
	years_2080 = str2num(datestr(date_2080,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
	years_2100 = str2num(datestr(date_2100,'yyyy')) ;   % years_RCP is used to find the atmospheric xCO2
    if option6==1
		RCP='RCP85';
    elseif option6==2
		RCP='RCP60';
    elseif option6==3
		RCP='RCP45';
    elseif option6==4
		RCP='RCP26';
	end
end

% choose the depths for water column averaging
DD1 = 200; % habitat depth - set bottom depth for KTdd (used for option2=0 and option2=1)
DD2 = 0; % surface depth - set top depth for KTdd (used for option2=0)
DD3 = 5; % bottom height - set height above bottom for KBdd (used for option2=0 and option2=1)
% DD4 = 50; % euphotic zone depth - for chla (used for chla if option3=1) (not used in this version)

% output at depths D0m and D200m
option7=1;
if option7==1
	option2=1;  % use depth-weighting to get the layer index of D200m
end

% --------------------------------
% --------------------------------
% --------------------------------
% end user edits


%% definitions used to create the netdcf empty files
%gp
% DICatm
ncvar_DICatm='var';
shortname_DICatm='DICatm';
longname_DICatm='DICatm at equilibrium with atmospheric CO2';
unit_DICatm='umol kg-1';
% DICexcess
ncvar_DICexcess='var';
shortname_DICexcess='DICexcess';
longname_DICexcess='DICexcess above equilibrium with atmospheric CO2';
unit_DICexcess='umol kg-1';
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
ncvar_pHsws='var';
shortname_pHsws='pHsws';
longname_pHsws='pH (seawater scale)';
unit_pHsws='seawater scale';
% pCO2 (uatm)
ncvar_pCO2='var';
shortname_pCO2='pCO2';
longname_pCO2='pCO2';
unit_pCO2='uatm';
% xCO2 (ppm)
ncvar_xCO2='var';
shortname_xCO2='xCO2';
longname_xCO2='xCO2';
unit_xCO2='ppm';
% RF (Revelle Factor)
ncvar_RF='var';
shortname_RF='RF';
longname_RF='Revelle Factor';
unit_RF='dimensionless';
% cal (omega calcite)
ncvar_omcal='var';
shortname_omcal='om_cal';
longname_omcal='omega calcite saturation state';
unit_omcal='dimensionless';
% om (omega aragonite)
ncvar_omara='var';
shortname_omara='om_ara';
longname_omara='omega aragonite saturation state';
unit_omara='dimensionless';

% create empty nc files for writing output

if option6~=0
% existing conditions (e.g. 1997-2007)
fout1_DICexcess_KT200 =   [fdir,fname,'_DICexcess_KT200.nc'];  
fout1_DICexcess_KB5 =   [fdir,fname,'_DICexcess_KB5.nc'];  
fout1_DICatm_KT200 =   [fdir,fname,'_DICatm_KT200.nc'];  
fout1_DICatm_KB5 =   [fdir,fname,'_DICatm_KB5.nc'];  
create_netcdf3D_L1(fout1_DICexcess_KT200,ncvar_DICexcess,shortname_DICexcess,longname_DICexcess,unit_DICexcess);   
create_netcdf3D_L1(fout1_DICexcess_KB5,ncvar_DICexcess,shortname_DICexcess,longname_DICexcess,unit_DICexcess);   
create_netcdf3D_L1(fout1_DICatm_KT200,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 1765
fout1_DICatm_KT200_1765 =   [fdir,fname,'_DICatm_KT200_',RCP,'_1765.nc'];  
fout1_DICatm_KB5_1765 =   [fdir,fname,'_DICatm_KB5_',RCP,'_1765.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_1765,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_1765,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 2020
fout1_DICatm_KT200_2020 =   [fdir,fname,'_DICatm_KT200_',RCP,'_2020.nc'];  
fout1_DICatm_KB5_2020 =   [fdir,fname,'_DICatm_KB5_',RCP,'_2020.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_2020,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_2020,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 2040
fout1_DICatm_KT200_2040 =   [fdir,fname,'_DICatm_KT200_',RCP,'_2040.nc'];  
fout1_DICatm_KB5_2040 =   [fdir,fname,'_DICatm_KB5_',RCP,'_2040.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_2040,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_2040,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 2060
fout1_DICatm_KT200_2060 =   [fdir,fname,'_DICatm_KT200_',RCP,'_2060.nc'];  
fout1_DICatm_KB5_2060 =   [fdir,fname,'_DICatm_KB5_',RCP,'_2060.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_2060,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_2060,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 2080
fout1_DICatm_KT200_2080 =   [fdir,fname,'_DICatm_KT200_',RCP,'_2080.nc'];  
fout1_DICatm_KB5_2080 =   [fdir,fname,'_DICatm_KB5_',RCP,'_2080.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_2080,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_2080,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 2100
fout1_DICatm_KT200_2100 =   [fdir,fname,'_DICatm_KT200_',RCP,'_2100.nc'];  
fout1_DICatm_KB5_2100 =   [fdir,fname,'_DICatm_KB5_',RCP,'_2100.nc'];  
create_netcdf3D_L1(fout1_DICatm_KT200_2100,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
create_netcdf3D_L1(fout1_DICatm_KB5_2100,ncvar_DICatm,shortname_DICatm,longname_DICatm,unit_DICatm);   
% RCP scenario 1765
fout1_dic_KT200_1765 =   [fdir,fname,'_dic_KT200dw_',RCP,'_1765.nc'];
fout1_dic_KB5_1765 =   [fdir,fname,'_dic_KB5dw_',RCP,'_1765.nc'];
fout1_pH_KT200_1765 =   [fdir,fname,'_pH_KT200dw_',RCP,'_1765.nc'];  
fout1_pH_KB5_1765 =   [fdir,fname,'_pH_KB5dw_',RCP,'_1765.nc'];
fout1_pCO2_KT200_1765 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_1765.nc'];
fout1_pCO2_KB5_1765 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_1765.nc'];
fout1_RF_KT200_1765 =   [fdir,fname,'_RF_KT200dw_',RCP,'_1765.nc'];
fout1_RF_KB5_1765 =   [fdir,fname,'_RF_KB5dw_',RCP,'_1765.nc'];
fout1_omcal_KT200_1765 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_1765.nc'];
fout1_omcal_KB5_1765 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_1765.nc'];
fout1_omara_KT200_1765 =   [fdir,fname,'_omara_KT200dw_',RCP,'_1765.nc'];
fout1_omara_KB5_1765 =   [fdir,fname,'_omara_KB5dw_',RCP,'_1765.nc'];
% RCP scenario 2020
fout1_dic_KT200_2020 =   [fdir,fname,'_dic_KT200dw_',RCP,'_2020.nc'];
fout1_dic_KB5_2020 =   [fdir,fname,'_dic_KB5dw_',RCP,'_2020.nc'];
fout1_pH_KT200_2020 =   [fdir,fname,'_pH_KT200dw_',RCP,'_2020.nc'];  
fout1_pH_KB5_2020 =   [fdir,fname,'_pH_KB5dw_',RCP,'_2020.nc'];
fout1_pCO2_KT200_2020 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_2020.nc'];
fout1_pCO2_KB5_2020 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_2020.nc'];
fout1_RF_KT200_2020 =   [fdir,fname,'_RF_KT200dw_',RCP,'_2020.nc'];
fout1_RF_KB5_2020 =   [fdir,fname,'_RF_KB5dw_',RCP,'_2020.nc'];
fout1_omcal_KT200_2020 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_2020.nc'];
fout1_omcal_KB5_2020 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_2020.nc'];
fout1_omara_KT200_2020 =   [fdir,fname,'_omara_KT200dw_',RCP,'_2020.nc'];
fout1_omara_KB5_2020 =   [fdir,fname,'_omara_KB5dw_',RCP,'_2020.nc'];
% RCP scenario 2040
fout1_dic_KT200_2040 =   [fdir,fname,'_dic_KT200dw_',RCP,'_2040.nc'];
fout1_dic_KB5_2040 =   [fdir,fname,'_dic_KB5dw_',RCP,'_2040.nc'];
fout1_pH_KT200_2040 =   [fdir,fname,'_pH_KT200dw_',RCP,'_2040.nc'];  
fout1_pH_KB5_2040 =   [fdir,fname,'_pH_KB5dw_',RCP,'_2040.nc'];
fout1_pCO2_KT200_2040 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_2040.nc'];
fout1_pCO2_KB5_2040 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_2040.nc'];
fout1_RF_KT200_2040 =   [fdir,fname,'_RF_KT200dw_',RCP,'_2040.nc'];
fout1_RF_KB5_2040 =   [fdir,fname,'_RF_KB5dw_',RCP,'_2040.nc'];
fout1_omcal_KT200_2040 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_2040.nc'];
fout1_omcal_KB5_2040 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_2040.nc'];
fout1_omara_KT200_2040 =   [fdir,fname,'_omara_KT200dw_',RCP,'_2040.nc'];
fout1_omara_KB5_2040 =   [fdir,fname,'_omara_KB5dw_',RCP,'_2040.nc'];
% RCP scenario 2060
fout1_dic_KT200_2060 =   [fdir,fname,'_dic_KT200dw_',RCP,'_2060.nc'];
fout1_dic_KB5_2060 =   [fdir,fname,'_dic_KB5dw_',RCP,'_2060.nc'];
fout1_pH_KT200_2060 =   [fdir,fname,'_pH_KT200dw_',RCP,'_2060.nc'];  
fout1_pH_KB5_2060 =   [fdir,fname,'_pH_KB5dw_',RCP,'_2060.nc'];
fout1_pCO2_KT200_2060 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_2060.nc'];
fout1_pCO2_KB5_2060 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_2060.nc'];
fout1_RF_KT200_2060 =   [fdir,fname,'_RF_KT200dw_',RCP,'_2060.nc'];
fout1_RF_KB5_2060 =   [fdir,fname,'_RF_KB5dw_',RCP,'_2060.nc'];
fout1_omcal_KT200_2060 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_2060.nc'];
fout1_omcal_KB5_2060 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_2060.nc'];
fout1_omara_KT200_2060 =   [fdir,fname,'_omara_KT200dw_',RCP,'_2060.nc'];
fout1_omara_KB5_2060 =   [fdir,fname,'_omara_KB5dw_',RCP,'_2060.nc'];
% RCP scenario 2080
fout1_dic_KT200_2080 =   [fdir,fname,'_dic_KT200dw_',RCP,'_2080.nc'];
fout1_dic_KB5_2080 =   [fdir,fname,'_dic_KB5dw_',RCP,'_2080.nc'];
fout1_pH_KT200_2080 =   [fdir,fname,'_pH_KT200dw_',RCP,'_2080.nc'];  
fout1_pH_KB5_2080 =   [fdir,fname,'_pH_KB5dw_',RCP,'_2080.nc'];
fout1_pCO2_KT200_2080 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_2080.nc'];
fout1_pCO2_KB5_2080 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_2080.nc'];
fout1_RF_KT200_2080 =   [fdir,fname,'_RF_KT200dw_',RCP,'_2080.nc'];
fout1_RF_KB5_2080 =   [fdir,fname,'_RF_KB5dw_',RCP,'_2080.nc'];
fout1_omcal_KT200_2080 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_2080.nc'];
fout1_omcal_KB5_2080 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_2080.nc'];
fout1_omara_KT200_2080 =   [fdir,fname,'_omara_KT200dw_',RCP,'_2080.nc'];
fout1_omara_KB5_2080 =   [fdir,fname,'_omara_KB5dw_',RCP,'_2080.nc'];
% RCP scenario 2100
fout1_dic_KT200_2100 =   [fdir,fname,'_dic_KT200dw_',RCP,'_2100.nc'];
fout1_dic_KB5_2100 =   [fdir,fname,'_dic_KB5dw_',RCP,'_2100.nc'];
fout1_pH_KT200_2100 =   [fdir,fname,'_pH_KT200dw_',RCP,'_2100.nc'];  
fout1_pH_KB5_2100 =   [fdir,fname,'_pH_KB5dw_',RCP,'_2100.nc'];
fout1_pCO2_KT200_2100 =   [fdir,fname,'_pCO2_KT200dw_',RCP,'_2100.nc'];
fout1_pCO2_KB5_2100 =   [fdir,fname,'_pCO2_KB5dw_',RCP,'_2100.nc'];
fout1_RF_KT200_2100 =   [fdir,fname,'_RF_KT200dw_',RCP,'_2100.nc'];
fout1_RF_KB5_2100 =   [fdir,fname,'_RF_KB5dw_',RCP,'_2100.nc'];
fout1_omcal_KT200_2100 =   [fdir,fname,'_omcal_KT200dw_',RCP,'_2100.nc'];
fout1_omcal_KB5_2100 =   [fdir,fname,'_omcal_KB5dw_',RCP,'_2100.nc'];
fout1_omara_KT200_2100 =   [fdir,fname,'_omara_KT200dw_',RCP,'_2100.nc'];
fout1_omara_KB5_2100 =   [fdir,fname,'_omara_KB5dw_',RCP,'_2100.nc'];
% RCP scenario 1765
create_netcdf3D_L1(fout1_dic_KT200_1765,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_1765,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_1765,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_1765,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_1765,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_1765,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_1765,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_1765,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_1765,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_1765,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_1765,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_1765,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RCP scenario 2020
create_netcdf3D_L1(fout1_dic_KT200_2020,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_2020,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_2020,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_2020,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_2020,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_2020,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_2020,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_2020,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_2020,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_2020,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_2020,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_2020,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RCP scenario 2040
create_netcdf3D_L1(fout1_dic_KT200_2040,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_2040,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_2040,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_2040,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_2040,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_2040,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_2040,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_2040,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_2040,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_2040,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_2040,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_2040,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RCP scenario 2060
create_netcdf3D_L1(fout1_dic_KT200_2060,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_2060,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_2060,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_2060,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_2060,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_2060,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_2060,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_2060,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_2060,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_2060,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_2060,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_2060,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RCP scenario 2080
create_netcdf3D_L1(fout1_dic_KT200_2080,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_2080,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_2080,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_2080,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_2080,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_2080,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_2080,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_2080,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_2080,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_2080,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_2080,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_2080,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RCP scenario 2100
create_netcdf3D_L1(fout1_dic_KT200_2100,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5_2100,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_pH_KT200_2100,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_2100,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KT200_2100,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_2100,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KT200_2100,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_2100,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KT200_2100,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_2100,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KT200_2100,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_2100,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
end

if option5==1
fout1_dep =   [fdir,fname,'_TotalDepth.nc'];  
fout1_zeta =   [fdir,fname,'_zeta.nc'];  
create_netcdf3D_L1(fout1_dep,ncvar_dep,shortname_dep,longname_dep,unit_dep);   
create_netcdf3D_L1(fout1_zeta,ncvar_zeta,shortname_zeta,longname_zeta,unit_zeta);   
end

% CO2SYS outputs
if option1==1 || option6~=0
if option2==1   % depth-weighted avg
% pHsws (pHsws)
fout1_pHsws_KT200_co2sys =   [fdir,fname,'_pHsws_KT200dw.nc'];   % CO2SYS output 33
fout1_pHsws_KB5_co2sys =   [fdir,fname,'_pHsws_KB5dw.nc'];
% pH (pHtotal)
fout1_pH_KT200_co2sys =   [fdir,fname,'_pH_KT200dw.nc'];   % CO2SYS output 33
fout1_pH_KB5_co2sys =   [fdir,fname,'_pH_KB5dw.nc'];
% pCO2 (uatm)
fout1_pCO2_KT200_co2sys =   [fdir,fname,'_pCO2_KT200dw.nc'];
fout1_pCO2_KB5_co2sys =   [fdir,fname,'_pCO2_KB5dw.nc'];
% xCO2 (ppm)
fout1_xCO2_KT200_co2sys =   [fdir,fname,'_xCO2_KT200dw.nc'];
fout1_xCO2_KB5_co2sys =   [fdir,fname,'_xCO2_KB5dw.nc'];
% RF (Revelle Factor)
fout1_RF_KT200_co2sys =   [fdir,fname,'_RF_KT200dw.nc'];
fout1_RF_KB5_co2sys =   [fdir,fname,'_RF_KB5dw.nc'];
% cal (omega calcite)
fout1_omcal_KT200_co2sys =   [fdir,fname,'_omcal_KT200dw.nc'];
fout1_omcal_KB5_co2sys =   [fdir,fname,'_omcal_KB5dw.nc'];
% om (omega aragonite)
fout1_omara_KT200_co2sys =   [fdir,fname,'_omara_KT200dw.nc'];
fout1_omara_KB5_co2sys =   [fdir,fname,'_omara_KB5dw.nc'];
elseif option2==0   % unweighted avg
% pHsws (pHsws)
fout1_pHsws_KT200_co2sys =   [fdir,fname,'_pHsws_KT200uw.nc'];   % CO2SYS output 33
fout1_pHsws_KB5_co2sys =   [fdir,fname,'_pHsws_KB5uw.nc'];
% pH (pHtotal)
fout1_pH_KT200_co2sys =   [fdir,fname,'_pH_KT200uw.nc'];   % CO2SYS output 33
fout1_pH_KB5_co2sys =   [fdir,fname,'_pH_KB5uw.nc'];
% pCO2 (uatm)
fout1_pCO2_KT200_co2sys =   [fdir,fname,'_pCO2_KT200uw.nc'];
fout1_pCO2_KB5_co2sys =   [fdir,fname,'_pCO2_KB5uw.nc'];
% xCO2 (uatm)
fout1_xCO2_KT200_co2sys =   [fdir,fname,'_xCO2_KT200uw.nc'];
fout1_xCO2_KB5_co2sys =   [fdir,fname,'_xCO2_KB5uw.nc'];
% RF (Revelle Factor)
fout1_RF_KT200_co2sys =   [fdir,fname,'_RF_KT200uw.nc'];
fout1_RF_KB5_co2sys =   [fdir,fname,'_RF_KB5uw.nc'];
% cal (omega calcite)
fout1_omcal_KT200_co2sys =   [fdir,fname,'_omcal_KT200uw.nc'];
fout1_omcal_KB5_co2sys =   [fdir,fname,'_omcal_KB5uw.nc'];
% om (omega aragonite)
fout1_omara_KT200_co2sys =   [fdir,fname,'_omara_KT200uw.nc'];
fout1_omara_KB5_co2sys =   [fdir,fname,'_omara_KB5uw.nc'];
end   % if option2 unweighed vs depth-weighted avg
%gp create_netcdf3D_L1(fout1);
% pHsws (seawater scale)
create_netcdf3D_L1(fout1_pHsws_KT200_co2sys,ncvar_pHsws,shortname_pHsws,longname_pHsws,unit_pHsws);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pHsws_KB5_co2sys,ncvar_pHsws,shortname_pHsws,longname_pHsws,unit_pHsws);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% pH (total scale)
create_netcdf3D_L1(fout1_pH_KT200_co2sys,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pH_KB5_co2sys,ncvar_pH,shortname_pH,longname_pH,unit_pH);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% pCO2 (pCO2)
create_netcdf3D_L1(fout1_pCO2_KT200_co2sys,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_pCO2_KB5_co2sys,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% xCO2 (xCO2)
create_netcdf3D_L1(fout1_xCO2_KT200_co2sys,ncvar_xCO2,shortname_xCO2,longname_xCO2,unit_xCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_xCO2_KB5_co2sys,ncvar_xCO2,shortname_xCO2,longname_xCO2,unit_xCO2);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% RF (Revelle Factor)
create_netcdf3D_L1(fout1_RF_KT200_co2sys,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_RF_KB5_co2sys,ncvar_RF,shortname_RF,longname_RF,unit_RF);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% omcal (omega calcite)
create_netcdf3D_L1(fout1_omcal_KT200_co2sys,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omcal_KB5_co2sys,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
% omara (omega aragonite)
create_netcdf3D_L1(fout1_omara_KT200_co2sys,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
create_netcdf3D_L1(fout1_omara_KB5_co2sys,ncvar_omara,shortname_omara,longname_omara,unit_omara);   % CO2SYS w/ Lueker et al 2000 using dep-wt avg
%
if option7==1
% pHsws (pHsws)
fout1_pHsws_D200_co2sys =   [fdir,fname,'_pHsws_D200m.nc'];   % CO2SYS output 33
fout1_pHsws_D0_co2sys =   [fdir,fname,'_pHsws_D0m.nc'];
% pH (pHtotal)
fout1_pH_D200_co2sys =   [fdir,fname,'_pH_D200m.nc'];   % CO2SYS output 33
fout1_pH_D0_co2sys =   [fdir,fname,'_pH_D0m.nc'];
% pCO2 (uatm)
fout1_pCO2_D200_co2sys =   [fdir,fname,'_pCO2_D200m.nc'];
fout1_pCO2_D0_co2sys =   [fdir,fname,'_pCO2_D0m.nc'];
% xCO2 (ppm)
fout1_xCO2_D200_co2sys =   [fdir,fname,'_xCO2_D200m.nc'];
fout1_xCO2_D0_co2sys =   [fdir,fname,'_xCO2_D0m.nc'];
% RF (Revelle Factor)
fout1_RF_D200_co2sys =   [fdir,fname,'_RF_D200m.nc'];
fout1_RF_D0_co2sys =   [fdir,fname,'_RF_D0m.nc'];
% cal (omega calcite)
fout1_omcal_D200_co2sys =   [fdir,fname,'_omcal_D200m.nc'];
fout1_omcal_D0_co2sys =   [fdir,fname,'_omcal_D0m.nc'];
% om (omega aragonite)
fout1_omara_D200_co2sys =   [fdir,fname,'_omara_D200m.nc'];
fout1_omara_D0_co2sys =   [fdir,fname,'_omara_D0m.nc'];
% pHsws (seawater scale)
create_netcdf3D_L1(fout1_pHsws_D200_co2sys,ncvar_pHsws,shortname_pHsws,longname_pHsws,unit_pHsws);  
create_netcdf3D_L1(fout1_pHsws_D0_co2sys,ncvar_pHsws,shortname_pHsws,longname_pHsws,unit_pHsws); 
% pH (total scale)
create_netcdf3D_L1(fout1_pH_D200_co2sys,ncvar_pH,shortname_pH,longname_pH,unit_pH);  
create_netcdf3D_L1(fout1_pH_D0_co2sys,ncvar_pH,shortname_pH,longname_pH,unit_pH); 
% pCO2 (pCO2 uatm)
create_netcdf3D_L1(fout1_pCO2_D200_co2sys,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);  
create_netcdf3D_L1(fout1_pCO2_D0_co2sys,ncvar_pCO2,shortname_pCO2,longname_pCO2,unit_pCO2);  
% xCO2 (xCO2 pppm)
create_netcdf3D_L1(fout1_xCO2_D200_co2sys,ncvar_xCO2,shortname_xCO2,longname_xCO2,unit_xCO2);  
create_netcdf3D_L1(fout1_xCO2_D0_co2sys,ncvar_xCO2,shortname_xCO2,longname_xCO2,unit_xCO2);  
% RF (Revelle Factor)
create_netcdf3D_L1(fout1_RF_D200_co2sys,ncvar_RF,shortname_RF,longname_RF,unit_RF);  
create_netcdf3D_L1(fout1_RF_D0_co2sys,ncvar_RF,shortname_RF,longname_RF,unit_RF);  
% omcal (omega calcite)
create_netcdf3D_L1(fout1_omcal_D200_co2sys,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   
create_netcdf3D_L1(fout1_omcal_D0_co2sys,ncvar_omcal,shortname_omcal,longname_omcal,unit_omcal);   
% omara (omega aragonite)
create_netcdf3D_L1(fout1_omara_D200_co2sys,ncvar_omara,shortname_omara,longname_omara,unit_omara);   
create_netcdf3D_L1(fout1_omara_D0_co2sys,ncvar_omara,shortname_omara,longname_omara,unit_omara);  
%
end   % if option7==1
%
end   % if option1==1  || option6~=0 CO2SYS

% Juranek outputs
if option4 == 1
if option2==1   % depth-weighted avg
fout2_KT200 =   [fdir,fname,'_om_juranek_KT200dw.nc'];
fout2_KB5 =   [fdir,fname,'_om_juranek_KB5dw.nc'];
elseif option2==0   % unweighted avg
fout2_KT200 =   [fdir,fname,'_om_juranek_KT200uw.nc'];
fout2_KB5 =   [fdir,fname,'_om_juranek_KB5uw.nc'];
end 
create_netcdf3D_L1(fout2_KT200,ncvar_omara,shortname_omara,longname_omara,unit_omara);  % Juranek using depwt avg
create_netcdf3D_L1(fout2_KB5,ncvar_omara,shortname_omara,longname_omara,unit_omara);  % Juranek using depwt avg
end    % if option4

% chem outputs
if option3==1   % save temp and chla and other chem
if option2==1   % depth-weighted avg
% salt
fout1_salt_KT200 =   [fdir,fname,'_salt_KT200dw.nc'];
fout1_salt_KB5 =   [fdir,fname,'_salt_KB5dw.nc'];
% po4
fout1_po4_KT200 =   [fdir,fname,'_po4_KT200dw.nc'];
fout1_po4_KB5 =   [fdir,fname,'_po4_KB5dw.nc'];
% sio3
fout1_sio3_KT200 =   [fdir,fname,'_sio3_KT200dw.nc'];
fout1_sio3_KB5 =   [fdir,fname,'_sio3_KB5dw.nc'];
% alk
fout1_alk_KT200 =   [fdir,fname,'_alk_KT200dw.nc'];
fout1_alk_KB5 =   [fdir,fname,'_alk_KB5dw.nc'];
% dic
fout1_dic_KT200 =   [fdir,fname,'_dic_KT200dw.nc'];
fout1_dic_KB5 =   [fdir,fname,'_dic_KB5dw.nc'];
% temp
% fout1_temp_KT50 =   [fdir,fname,'_temp_KT50dw.nc'];  
fout1_temp_KT200 =   [fdir,fname,'_temp_KT200dw.nc'];
fout1_temp_KB5 =   [fdir,fname,'_temp_KB5dw.nc'];
% chla
% fout1_chla_KT50 =   [fdir,fname,'_chla_KT50dw.nc'];  
fout1_chla_KT200 =   [fdir,fname,'_chla_KT200dw.nc'];   
fout1_chla_KB5 =   [fdir,fname,'_chla_KB5dw.nc'];
fout1_chla_areal =   [fdir,fname,'_chla_areal.nc'];  
% o2
% fout1_o2_KT50 =   [fdir,fname,'_o2_KT50dw.nc'];   
fout1_o2_KT200 =   [fdir,fname,'_o2_KT200dw.nc'];   
fout1_o2_KB5 =   [fdir,fname,'_o2_KB5dw.nc'];
elseif option2==0   % unweighted avg
% salt
fout1_salt_KT200 =   [fdir,fname,'_salt_KT200uw.nc'];
fout1_salt_KB5 =   [fdir,fname,'_salt_KB5uw.nc'];
% po4
fout1_po4_KT200 =   [fdir,fname,'_po4_KT200uw.nc'];
fout1_po4_KB5 =   [fdir,fname,'_po4_KB5uw.nc'];
% sio3
fout1_sio3_KT200 =   [fdir,fname,'_sio3_KT200uw.nc'];
fout1_sio3_KB5 =   [fdir,fname,'_sio3_KB5uw.nc'];
% alk
fout1_alk_KT200 =   [fdir,fname,'_alk_KT200uw.nc'];
fout1_alk_KB5 =   [fdir,fname,'_alk_KB5uw.nc'];
% dic
fout1_dic_KT200 =   [fdir,fname,'_dic_KT200uw.nc'];
fout1_dic_KB5 =   [fdir,fname,'_dic_KB5uw.nc'];
% temp
% fout1_temp_KT50 =   [fdir,fname,'_temp_KT50uw.nc'];   
fout1_temp_KT200 =   [fdir,fname,'_temp_KT200uw.nc']; 
fout1_temp_KB5 =   [fdir,fname,'_temp_KB5uw.nc'];
fout1_temp_std_KT200 =   [fdir,fname,'_temp_std_KT200uw.nc'];    % vertical std dev
% chla
% fout1_chla_KT50 =   [fdir,fname,'_chla_KT50uw.nc'];  
fout1_chla_KT200 =   [fdir,fname,'_chla_KT200uw.nc'];  
fout1_chla_KB5 =   [fdir,fname,'_chla_KB5uw.nc'];
fout1_chla_areal =   [fdir,fname,'_chla_areal2.nc'];   
fout1_chla_std_KT200 =   [fdir,fname,'_chla_std_KT200uw.nc'];  % vertical std dev
% o2
% fout1_o2_KT50 =   [fdir,fname,'_o2_KT50uw.nc'];   
fout1_o2_KT200 =   [fdir,fname,'_o2_KT200uw.nc'];   
fout1_o2_KB5 =   [fdir,fname,'_o2_KB5uw.nc'];
fout1_o2_std_KT200 =   [fdir,fname,'_o2_std_KT200uw.nc'];   % vertical std dev  
end   % if option2
% salt
create_netcdf3D_L1(fout1_salt_KT200,ncvar_salt,shortname_salt,longname_salt,unit_salt);  
create_netcdf3D_L1(fout1_salt_KB5,ncvar_salt,shortname_salt,longname_salt,unit_salt);  
% po4
create_netcdf3D_L1(fout1_po4_KT200,ncvar_po4,shortname_po4,longname_po4,unit_po4);  
create_netcdf3D_L1(fout1_po4_KB5,ncvar_po4,shortname_po4,longname_po4,unit_po4);  
% sio3
create_netcdf3D_L1(fout1_sio3_KT200,ncvar_sio3,shortname_sio3,longname_sio3,unit_sio3);  
create_netcdf3D_L1(fout1_sio3_KB5,ncvar_sio3,shortname_sio3,longname_sio3,unit_sio3);  
% dic
create_netcdf3D_L1(fout1_dic_KT200,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_KB5,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
% alk
create_netcdf3D_L1(fout1_alk_KT200,ncvar_alk,shortname_alk,longname_alk,unit_alk);  
create_netcdf3D_L1(fout1_alk_KB5,ncvar_alk,shortname_alk,longname_alk,unit_alk);  
% temp
% create_netcdf3D_L1(fout1_temp_KT50,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
create_netcdf3D_L1(fout1_temp_KT200,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
create_netcdf3D_L1(fout1_temp_KB5,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
% chla
% create_netcdf3D_L1(fout1_chla_KT50,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_chla_KT200,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_chla_KB5,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_chla_areal,ncvar_chla,shortname_chla,longname_chla,unit_chla_areal);  
% o2
% create_netcdf3D_L1(fout1_o2_KT50,ncvar_o2,shortname_o2,longname_o2,unit_o2);  
create_netcdf3D_L1(fout1_o2_KT200,ncvar_o2,shortname_o2,longname_o2,unit_o2);  
create_netcdf3D_L1(fout1_o2_KB5,ncvar_o2,shortname_o2,longname_o2,unit_o2);  
if option2==0   % vertical std dev
create_netcdf3D_L1(fout1_temp_std_KT200,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
create_netcdf3D_L1(fout1_chla_std_KT200,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_o2_std_KT200,ncvar_o2,shortname_o2,longname_o2,unit_o2);  
end   % if option2

%
if option7==1
% salt
fout1_salt_D200 =   [fdir,fname,'_salt_D200m.nc'];
fout1_salt_D0 =   [fdir,fname,'_salt_D0m.nc'];
% po4
fout1_po4_D200 =   [fdir,fname,'_po4_D200m.nc'];
fout1_po4_D0 =   [fdir,fname,'_po4_D0m.nc'];
% sio3
fout1_sio3_D200 =   [fdir,fname,'_sio3_D200m.nc'];
fout1_sio3_D0 =   [fdir,fname,'_sio3_D0m.nc'];
% alk
fout1_alk_D200 =   [fdir,fname,'_alk_D200m.nc'];
fout1_alk_D0 =   [fdir,fname,'_alk_D0m.nc'];
% dic
fout1_dic_D200 =   [fdir,fname,'_dic_D200m.nc'];
fout1_dic_D0 =   [fdir,fname,'_dic_D0m.nc'];
% temp
fout1_temp_D200 =   [fdir,fname,'_temp_D200m.nc'];
fout1_temp_D0 =   [fdir,fname,'_temp_D0m.nc'];
% chla
fout1_chla_D200 =   [fdir,fname,'_chla_D200m.nc'];   
fout1_chla_D0 =   [fdir,fname,'_chla_D0m.nc'];
% o2
fout1_o2_D200 =   [fdir,fname,'_o2_D200m.nc'];   
fout1_o2_D0 =   [fdir,fname,'_o2_D0m.nc'];
% salt
create_netcdf3D_L1(fout1_salt_D200,ncvar_salt,shortname_salt,longname_salt,unit_salt);  
create_netcdf3D_L1(fout1_salt_D0,ncvar_salt,shortname_salt,longname_salt,unit_salt);  
% po4
create_netcdf3D_L1(fout1_po4_D200,ncvar_po4,shortname_po4,longname_po4,unit_po4);  
create_netcdf3D_L1(fout1_po4_D0,ncvar_po4,shortname_po4,longname_po4,unit_po4);  
% sio3
create_netcdf3D_L1(fout1_sio3_D200,ncvar_sio3,shortname_sio3,longname_sio3,unit_sio3);  
create_netcdf3D_L1(fout1_sio3_D0,ncvar_sio3,shortname_sio3,longname_sio3,unit_sio3);  
% dic
create_netcdf3D_L1(fout1_dic_D200,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
create_netcdf3D_L1(fout1_dic_D0,ncvar_dic,shortname_dic,longname_dic,unit_dic);  
% alk
create_netcdf3D_L1(fout1_alk_D200,ncvar_alk,shortname_alk,longname_alk,unit_alk);  
create_netcdf3D_L1(fout1_alk_D0,ncvar_alk,shortname_alk,longname_alk,unit_alk);  
% temp
create_netcdf3D_L1(fout1_temp_D200,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
create_netcdf3D_L1(fout1_temp_D0,ncvar_temp,shortname_temp,longname_temp,unit_temp);  
% chla
create_netcdf3D_L1(fout1_chla_D200,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
create_netcdf3D_L1(fout1_chla_D0,ncvar_chla,shortname_chla,longname_chla,unit_chla);  
% o2
create_netcdf3D_L1(fout1_o2_D200,ncvar_o2,shortname_o2,longname_o2,unit_o2);  
create_netcdf3D_L1(fout1_o2_D0,ncvar_o2,shortname_o2,longname_o2,unit_o2);  

end		% if option7==1 
%
end   % if option3





