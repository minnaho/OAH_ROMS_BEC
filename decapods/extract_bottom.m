%% ============================================================ 
%% program to extract a 3D file var(x,y,t), 			
%% 2D maps of the entire domain of ROMS of omega                
%% aragonite calcualted using options:        	        
%% option1- CO2SYS model a full carbonate system method               
%% option3 - additional variables to extract
%% option4- en emperical statistical model from Juranek et al 2014    
%% 						                
%% Program by Faycal Kessouri - SCCWRP/UCLA                     
%% 05/2018              				        
%% to include options for water column averaging 
%% ============================================================ 

close all
clear all
clc

disp(['2D extraction program starts .... on:  ',  datestr(now)])

%% load the matlab paths
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))

% begin user edits

% name of param.m file to control this extract_2D.m
param_bottom

% end user edits

%% start of the loop
disp('start the loop ..')
cpt = 1;

for fr = 1:length(repavg)

%% find the find one by one
 file = [rep,'/',repavg(fr,1).name] ;
disp(['now reading >>>  ',file])
disp(datestr(now));

%% calculate dz
   zeta  = ncread(file, 'zeta')' ;

% function calculate bottom
[dz, zKB, DepthWeight_KB5, idxKBDD, TotalDepth]=Fx_bottom( ...
	DD3, h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type);

%% read the variables
   dataout  = ncread(file, 'rho') ;
   dataout = permute(dataout, [3 2 1]);
   dens = (squeeze(dataout(:,:,:)) + 1027.4) ;

   dataout  = ncread(file, 'temp') ;
   dataout = permute(dataout, [3 2 1]);
   temp = squeeze(dataout(:,:,:)) ;
   temp_dataout = temp;   %gp for later use in diagnostic output
   temp_KB5 = Fx_var_KBDD_v02(temp,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
%

% chlorophyll a
if option3 ==1
   dataout  = ncread(file, 'DIATCHL') ;
   dataout = permute(dataout, [3 2 1]);
   VAR1 = squeeze(dataout(:,:,:)) ;
   dataout  = ncread(file, 'SPCHL') ;
   dataout = permute(dataout, [3 2 1]);
   VAR2 = squeeze(dataout(:,:,:)) ;
   dataout  = ncread(file, 'DIAZCHL') ;
   dataout = permute(dataout, [3 2 1]);
   VAR3 = squeeze(dataout(:,:,:)) ;
   chla = VAR1+VAR2+VAR3;   % total chlorophyll a mg m-3
   chla(chla<0)=0;   % set negative values to zero
   chla_areal_3D = chla .* dz;   % 3D array (layer,x,y) of areal total chlorophyll a in each layer mg m-2
   chla_areal_2D = squeeze(nansum(chla_areal_3D,1));   % 2D array (x,y) of integrated water column areal total chlorophyll a mg m-2
   chla_KB5 = Fx_var_KBDD_v02(chla,DepthWeight_KB5);   
end   % if option3

   dataout  = ncread(file, 'O2') ;
   dataout = permute(dataout, [3 2 1]);
   o2 = squeeze(dataout(:,:,:)) ;
   o2 = (o2./(dens.*0.001)) ;   % mmol m-3
   o2_KB5 = Fx_var_KBDD_v02(o2,DepthWeight_KB5);   


% optional CO2SYS calcs if option1=1 or option6~=0
if option1==1
disp(['start CO2SYS ...  '])

   dataout  = ncread(file, 'DIC') ;
   dataout = permute(dataout, [3 2 1]);
   dic = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3 in ROMS output
   dic = (dic./(dens.*0.001)) ;   % convert to units of umol/kg for input to CO2SYS
   dic_KB5 = Fx_var_KBDD_v02(dic,DepthWeight_KB5); 


   dataout  = ncread(file, 'salt') ;
   dataout = permute(dataout, [3 2 1]);
   salt = squeeze(dataout(:,:,:)) ;
   salt_KB5 = Fx_var_KBDD_v02(salt,DepthWeight_KB5); 

   dataout  = ncread(file, 'PO4') ;
   dataout = permute(dataout, [3 2 1]);
   po4 = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3
   po4 = (po4./(dens.*0.001)) ;   % convert from mmol/m^3 to umol/kg
   po4_KB5 = Fx_var_KBDD_v02(po4,DepthWeight_KB5); 

   dataout  = ncread(file, 'SiO3') ;
   dataout = permute(dataout, [3 2 1]);
   sio3 = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3
   sio3 = (sio3./(dens.*0.001)) ;   % convert from mmol/m^3 to umol/kg
   sio3_KB5 = Fx_var_KBDD_v02(sio3,DepthWeight_KB5); 

   dataout  = ncread(file, 'Alk') ;
   dataout = permute(dataout, [3 2 1]);
   alk = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3 in ROMS output
   alk = (alk./(dens.*0.001)) ; %./ 1.0114 ;   % convert to units of umol/kg for input to CO2SYS
   alk_KB5 = Fx_var_KBDD_v02(alk,DepthWeight_KB5);


   PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
   PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
   pHSCALEIN = 1 ;  % 1=total pH, 2= sea water scale
   K1K2CONSTANTS = 14 ; % Millero et al, 2010
   KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
   clear DATA
   TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
   [DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5(:),...
       PAR1TYPE,PAR2TYPE,...
       salt_KB5(:),temp_KB5(:),nan,...
       m2db(TotalDepth(:)),nan,...
       sio3_KB5(:),po4_KB5(:),...
       pHSCALEIN,...
       K1K2CONSTANTS,KSO4CONSTANTS);
   pH_KB5_co2sys = DATA(:,33) ;% pHtotal
   %pHsws_KB5_co2sys = DATA(:,34) ;% pHsws
   pCO2_KB5_co2sys = DATA(:,4) ;% (uatm)
   %xCO2_KB5_co2sys = DATA(:,17) ;% (ppm)
   RF_KB5_co2sys = DATA(:,14) ;% Revelle Factor
   %omcal_KB5_co2sys = DATA(:,15) ;% omega calcite
   omara_KB5_co2sys = DATA(:,16) ;% omega ara 16
   pH_KB5_co2sys = reshape(pH_KB5_co2sys,NY,NX);
   %pHsws_KB5_co2sys = reshape(pHsws_KB5_co2sys,NY,NX);
   pCO2_KB5_co2sys = reshape(pCO2_KB5_co2sys,NY,NX);
   %xCO2_KB5_co2sys = reshape(xCO2_KB5_co2sys,NY,NX);
   RF_KB5_co2sys = reshape(RF_KB5_co2sys,NY,NX);
   %omcal_KB5_co2sys = reshape(omcal_KB5_co2sys,NY,NX);
   omara_KB5_co2sys = reshape(omara_KB5_co2sys,NY,NX);

end   % if option1 

% Calculate omega aragonite option4 (Juranek et al 2014, applied on USW coast)
if option4 == 1
% [OM,Err] = juranek_aragsat(temp,o2) ;
[OM_KB5,Err] = juranek_aragsat(temp_KB5,o2_KB5) ;   %gp
end

% CO2SYS
if option1==1
pH_KB5_co2sys(pH_KB5_co2sys==0)=NaN;
%pHsws_KB5_co2sys(pHsws_KB5_co2sys==0)=NaN;
pCO2_KB5_co2sys(pCO2_KB5_co2sys==0)=NaN;
%xCO2_KB5_co2sys(xCO2_KB5_co2sys==0)=NaN;
RF_KB5_co2sys(RF_KB5_co2sys==0)=NaN;
%omcal_KB5_co2sys(omcal_KB5_co2sys==0)=NaN;
omara_KB5_co2sys(omara_KB5_co2sys==0)=NaN;   
end		% if option1==1

% Juranek
if option4 == 1
% OM(OM==0)=NaN;
OM_KB5(OM_KB5==0)=NaN;   %gp
end

if option1==1
% CO2SYS outputs
% KB5
pH_KB5_co2sys(mask==0)=NaN; 
%pHsws_KB5_co2sys(mask==0)=NaN; 
pCO2_KB5_co2sys(mask==0)=NaN; 
%xCO2_KB5_co2sys(mask==0)=NaN; 
RF_KB5_co2sys(mask==0)=NaN; 
%omcal_KB5_co2sys(mask==0)=NaN; 
omara_KB5_co2sys(mask==0)=NaN; 

% write nc
% pHtotal
ncwrite(fout1_pH_KB5_co2sys, 'var', pH_KB5_co2sys' , [1 1 cpt]);
% pHsws
%ncwrite(fout1_pHsws_KB5_co2sys, 'var', pHsws_KB5_co2sys' , [1 1 cpt]);
% pCO2
ncwrite(fout1_pCO2_KB5_co2sys, 'var', pCO2_KB5_co2sys' , [1 1 cpt]);
% xCO2
%ncwrite(fout1_xCO2_KB5_co2sys, 'var', xCO2_KB5_co2sys' , [1 1 cpt]);
% RF
ncwrite(fout1_RF_KB5_co2sys, 'var', RF_KB5_co2sys' , [1 1 cpt]);
% cal (omega calcite)
%ncwrite(fout1_omcal_KB5_co2sys, 'var', omcal_KB5_co2sys' , [1 1 cpt]);
% om (omega aragonite)
ncwrite(fout1_omara_KB5_co2sys, 'var', omara_KB5_co2sys' , [1 1 cpt]);
end

% Juranek outputs
if option4 == 1
% mask land
OM_KB5(mask==0)=NaN; 
% write nc
ncwrite(fout2_KB5, 'var', OM_KB5' , [1 1 cpt]);   %gp
end

% temp, chla and other chem outputs
if option3 == 1
%
% mask land
chla_areal_2D(mask==0)=NaN; 
% KB5
salt_KB5(mask==0)=NaN; 
po4_KB5(mask==0)=NaN; 
sio3_KB5(mask==0)=NaN; 
dic_KB5(mask==0)=NaN; 
alk_KB5(mask==0)=NaN; 
temp_KB5(mask==0)=NaN; 
o2_KB5(mask==0)=NaN; 
chla_KB5(mask==0)=NaN; 
%
% write nc
% salt
ncwrite(fout1_salt_KB5, 'var', salt_KB5' , [1 1 cpt]);   
% po4
ncwrite(fout1_po4_KB5, 'var', po4_KB5' , [1 1 cpt]);   
% sio3
ncwrite(fout1_sio3_KB5, 'var', sio3_KB5' , [1 1 cpt]);   
% dic
ncwrite(fout1_dic_KB5, 'var', dic_KB5' , [1 1 cpt]);   
% alk
ncwrite(fout1_alk_KB5, 'var', alk_KB5' , [1 1 cpt]);   
% temp
% ncwrite(fout1_temp_KT50, 'var', temp_KT50' , [1 1 cpt]);   
ncwrite(fout1_temp_KB5, 'var', temp_KB5' , [1 1 cpt]);   
% chla
% ncwrite(fout1_chla_KT50, 'var', chla_KT50' , [1 1 cpt]);   
ncwrite(fout1_chla_KB5, 'var', chla_KB5' , [1 1 cpt]);   
ncwrite(fout1_chla_areal, 'var', chla_areal_2D' , [1 1 cpt]);   
% temp
% ncwrite(fout1_o2_KT50, 'var', o2_KT50' , [1 1 cpt]);   
ncwrite(fout1_o2_KB5, 'var', o2_KB5' , [1 1 cpt]);   
end    % if option3

cpt = cpt+1 ;

end % fr

disp(['2D Omega aragonite program ends .... on:  ',  datestr(now)])

