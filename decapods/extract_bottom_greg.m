%% ============================================================ 
%% program to extract a 3D file var(x,y,t), 			
%% 2D maps of the entire domain of ROMS of omega                
%% aragonite calcualted using two options:        	        
%% 1- CO2SYS model a full carbonate system method               
%% 2- en emperical statistical model from Juranek et al 2014    
%% 						                
%% Program by Faycal Kessouri - SCCWRP/UCLA                     
%% 05/2018              				        
%%
%% 
%
%  Program modified by Greg Pelletier - SCCWRP                     
%  11/2019              				        
%
%  version history
%  v28 - change xCO2 to variable #17 from CO2SYS
%  v27 - added output of pHsws (seawater scale) and xCO2 (ppm) for existing conditions 
%        in addition to pH total scale (pH) and pCO2 (uatm)
%  v26 - started with v24 and added option for output of 0m and 200m co2sys and chem variables
%  v25 - calc 3D co2sys (abandoned, crashed when testing used >> 50%MEM, CPU time >> 8 days) 
%  v24 - converted depth (m) to (decibars) and xCO2 (ppm) to pCO2 (uatm) for CO2SYS inputs
%        same result as v19 to 4 significant figures for 0-200m omara, 
%        same to 5 signficantfigures for 0-200m pH, and pCO2, 
%        and same to 3 significant figures for bottom 5m pH
%  v23 - added Canthro for RCP 1765, 2020, 2040, 2060, 2080, and 2100 using method of Evans at al 2019 Frontiers paper
%  v22 - added Canthro for RCP 1765, 2080, and 2100 using method of Evans at al 2019 Frontiers paper
%  v20 - added output of TotalDepth and zeta
%  v19 - corrected unit conversion for po4 and si03 to umol/kg, same CO2SYS result to 4 significant figures
%  v18 - more efficient dep wt v05 (>2x faster than v03), exactly same CO2SYS result as v14 to +/- 1e-10
%  v14 - final params for CO2SYS, Lueker et al 2000, pH total scale, PRESIN=depth, depth-wt v03
%
%%
%% to include options for water column averaging 
%% and additional variables to extract
%%
%% ============================================================ 

%gp
close all
clear all
clc

disp(['2D extraction program starts .... on:  ',  datestr(now)])

%% load the matlab paths
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))

% begin user edits
%--------------------------------------------
%--------------------------------------------
%--------------------------------------------

% name of param.m file to control this extract_2D.m
param_v28_L1_19972007

%--------------------------------------------
%--------------------------------------------
%--------------------------------------------
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

%gp replace the code below with call to new function 
% to calculate dz, z, and depth weighting factors 
% for 0-200m (or to any other depth)

if option2==1   % depth-weighted avg

% % KT200 is from surface to 200m depth
% [dz, z, DepthWeight_KT200, idxKTDD, CumDepth, TotalDepth]=Fx_DepthWeight_KTDD_v05( ...
	% DD1, h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type);

% % KB5 is from bottom to 5m above bottom 
% % [DepthWeight_KB5, NumLayersTo_KB5, CumHeight, TotalDepth]=Fx_DepthWeightGivenDZ_KBDD_v03( ...
	% % DD3, dz, h, zeta);
% [dz, z, DepthWeight_KB5, idxKBDD, CumHeight, TotalDepth]=Fx_DepthWeight_KBDD_v05( ...
	% DD3, h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type);

% KT200 and KB5 at the same time
[dz, zKT, zKB, DepthWeight_KT200, DepthWeight_KB5, idxKTDD, idxKBDD, CumDepth, CumHeight, TotalDepth]=Fx_DepthWeight_KT1KB1_v05( ...
	DD1, DD3, h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type);

elseif option2==0   % unweighted avg

[dz, zKT, zKB]=Fx_MidpointDepthsAndHeights_v01( ...
	h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type);
	
TotalDepth=h+zeta;	

end   % if option2

% Faycal's original code
% [z_w,Cw1] = zlevs4(h, zeta, theta_s, theta_b, hc, NZ, 'w',sc_type);
% dz = diff(z_w);
% % find z = midpoint depths from the surface
        % zbot = flipdim(cumsum(flipdim(dz,1)),1);
        % ztop = [zbot(2:end,:,:);zeros(1,NY,NX)];
	% z = (zbot+ztop)./2 ;

%gp new code
% % find zKB = midpoint heights from bottom
        % zbotKB = cumsum(dz,1);
        % % ztopKB = [zbotKB(2:end,:,:);zeros(1,NY,NX)];
        % endKB=numel(zbotKB(:,1,1))-1;
		% % ztopKB = [zbotKB(1:endKB,:,:);zeros(numel(zbotKB(:,1,1)),NY,NX)];
        % % ztop = [zbot(end:2z,:,:);zeros(1,NY,NX)];
        % ztopKB=zeros(size(zbotKB));
        % ztopKB(2:end,:,:)=zbotKB(1:endKB,:,:);
	% zKB = (zbotKB+ztopKB)./2 ;


%% read the variables
   dataout  = ncread(file, 'rho') ;
   dataout = permute(dataout, [3 2 1]);
   dens = (squeeze(dataout(:,:,:)) + 1027.4) ;
% if option2==1   % depth-weighted avg
   % dens_KT200 = Fx_var_KTDD_v02(dens,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % dens_KB5 = Fx_var_KBDD_v02(dens,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
% elseif option2==0   % unweighted avg
   % dens_KT200 = Fx_var_KTDD_unweighted_v02(dens, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   % dens_KB5 = Fx_var_KBDD_unweighted_v02(dens, zKB, DD3);   %gp thickness-weighted average from 0-200m
% end

   dataout  = ncread(file, 'temp') ;
   dataout = permute(dataout, [3 2 1]);
   temp = squeeze(dataout(:,:,:)) ;
   temp_dataout = temp;   %gp for later use in diagnostic output
if option2==1   % depth-weighted avg
%    temp_KT50 = Fx_var_KTDD_v02(temp,DepthWeight_KT50);   %gp thickness-weighted average from 0-50m
   temp_KT200 = Fx_var_KTDD_v02(temp,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   temp_KB5 = Fx_var_KBDD_v02(temp,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   %gp temp(z>DD1 & z<DD2)=NaN; temp = squeeze(nanmean(temp,1)) ;
   % temp(z>DD1)=NaN; temp(z<DD2)=NaN; temp = squeeze(nanmean(temp,1)) ;

   % %KT200
   % temp_KT200 = temp;
   % temp_KT200(zKT>DD1)=NaN; temp_KT200(zKT<DD2)=NaN; temp_KT200 = squeeze(nanmean(temp_KT200,1)) ;
   % %KB5
   % temp_KB5 = temp;
   % temp_KB5(zKB>DD3)=NaN; temp_KB5 = squeeze(nanmean(temp_KB5,1)) ;
   % % for cases where the midpoint of the bottom layer is > DD3
   % temp_KB = squeeze(temp(1,:,:));   % bottom layer conc of temp
   % temp_KB5(isnan(temp_KB5))=temp_KB(isnan(temp_KB5));

%    temp_KT50 = Fx_var_KTDD_unweighted_v02(temp, zKT, DD4, DD2);   
   temp_KT200 = Fx_var_KTDD_unweighted_v02(temp, zKT, DD1, DD2); 
   temp_KB5 = Fx_var_KBDD_unweighted_v02(temp, zKB, DD3);  
   temp_msk=temp; temp_msk(zKT>DD1)=NaN; temp_msk(zKT<DD2)=NaN; temp_std_KT200 = squeeze(nanstd2(temp_msk,1)) ;   % vertical std dev
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			temp_D200(i,j)=temp(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   temp_D0 = squeeze(temp(NZ,:,:));  
end

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
   chla_areal_2D = squeeze(nansum2(chla_areal_3D,1));   % 2D array (x,y) of integrated water column areal total chlorophyll a mg m-2
if option2==1   % depth-weighted avg
%    chla_KT50 = Fx_var_KTDD_v02(chla,DepthWeight_KT50);   
   chla_KT200 = Fx_var_KTDD_v02(chla,DepthWeight_KT200);   
   chla_KB5 = Fx_var_KBDD_v02(chla,DepthWeight_KB5);   
elseif option2==0   % unweighted avg
%    chla_KT50 = Fx_var_KTDD_unweighted_v02(chla, zKT, DD4, DD2);
   chla_KT200 = Fx_var_KTDD_unweighted_v02(chla, zKT, DD1, DD2); 
   chla_KB5 = Fx_var_KBDD_unweighted_v02(chla, zKB, DD3);  
   chla_msk=chla; chla_msk(zKT>DD1)=NaN; chla_msk(zKT<DD2)=NaN; chla_std_KT200 = squeeze(nanstd2(chla_msk,1)) ;   % vertical std dev
end   % if option2
end   % if option3
%
if option7==1
   for i=1:NY
		for j=1:NX
			chla_D200(i,j)=chla(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   chla_D0 = squeeze(chla(NZ,:,:));  
end

   dataout  = ncread(file, 'O2') ;
   dataout = permute(dataout, [3 2 1]);
   o2 = squeeze(dataout(:,:,:)) ;
   o2 = (o2./(dens.*0.001)) ;   % mmol m-3
   % o2_KT200 = Fx_var_KTDD_v02(o2,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % o2_KB5 = Fx_var_KBDD_v02(o2,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp o2(z>DD1 & z<DD2)=NaN; o2 = squeeze(nanmean(o2,1)) ;
   % o2(z>DD1)=NaN; o2(z<DD2)=NaN; o2 = squeeze(nanmean(o2,1)) ;
if option2==1   % depth-weighted avg
%    o2_KT50 = Fx_var_KTDD_v02(o2,DepthWeight_KT50);   
   o2_KT200 = Fx_var_KTDD_v02(o2,DepthWeight_KT200);   
   o2_KB5 = Fx_var_KBDD_v02(o2,DepthWeight_KB5);   
elseif option2==0   % unweighted avg
%    o2_KT50 = Fx_var_KTDD_unweighted_v02(o2, zKT, DD4, DD2);   
   o2_KT200 = Fx_var_KTDD_unweighted_v02(o2, zKT, DD1, DD2);   
   o2_KB5 = Fx_var_KBDD_unweighted_v02(o2, zKB, DD3);   
   o2_msk=o2; o2_msk(zKT>DD1)=NaN; o2_msk(zKT<DD2)=NaN; o2_std_KT200 = squeeze(nanstd2(o2_msk,1)) ;   % vertical std dev
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			o2_D200(i,j)=o2(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   o2_D0 = squeeze(o2(NZ,:,:));  
end

% optional CO2SYS calcs if option1=1 or option6~=0
if option1==1 || option6~=0
disp(['start CO2SYS ...  '])

%
   dataout  = ncread(file, 'DIC') ;
   dataout = permute(dataout, [3 2 1]);
   dic = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3 in ROMS output
   dic = (dic./(dens.*0.001)) ;   % convert to units of umol/kg for input to CO2SYS
   % dic_KT200 = Fx_var_KTDD_v02(dic,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % dic_KB5 = Fx_var_KBDD_v02(dic,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp dic(z>DD1 & z<DD2)=NaN; dic = squeeze(nanmean(dic,1)) ;
   % dic(z>DD1)=NaN; dic(z<DD2)=NaN; dic = squeeze(nanmean(dic,1)) ;
if option2==1   % depth-weighted avg
   dic_KT200 = Fx_var_KTDD_v02(dic,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   dic_KB5 = Fx_var_KBDD_v02(dic,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   dic_KT200 = Fx_var_KTDD_unweighted_v02(dic, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   dic_KB5 = Fx_var_KBDD_unweighted_v02(dic, zKB, DD3);   %gp thickness-weighted average from 0-200m
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			dic_D200(i,j)=dic(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   dic_D0 = squeeze(dic(NZ,:,:));  
end

%
   dataout  = ncread(file, 'salt') ;
   dataout = permute(dataout, [3 2 1]);
   salt = squeeze(dataout(:,:,:)) ;
   % salt_KT200 = Fx_var_KTDD_v02(salt,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % salt_KB5 = Fx_var_KBDD_v02(salt,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp salt(z>DD1 & z<DD2)=NaN; salt = squeeze(nanmean(salt,1)) ;
   % salt(z>DD1)=NaN; salt(z<DD2)=NaN; salt = squeeze(nanmean(salt,1)) ;
if option2==1   % depth-weighted avg
   salt_KT200 = Fx_var_KTDD_v02(salt,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   salt_KB5 = Fx_var_KBDD_v02(salt,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   salt_KT200 = Fx_var_KTDD_unweighted_v02(salt, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   salt_KB5 = Fx_var_KBDD_unweighted_v02(salt, zKB, DD3);   %gp thickness-weighted average from 0-200m
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			salt_D200(i,j)=salt(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   salt_D0 = squeeze(salt(NZ,:,:));  
end

%
   dataout  = ncread(file, 'PO4') ;
   dataout = permute(dataout, [3 2 1]);
   po4 = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3
   po4 = (po4./(dens.*0.001)) ;   % convert from mmol/m^3 to umol/kg
   % po4_KT200 = Fx_var_KTDD_v02(po4,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % po4_KB5 = Fx_var_KBDD_v02(po4,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp po4(z>DD1 & z<DD2)=NaN; po4 = squeeze(nanmean(po4,1)) ;
   % po4(z>DD1)=NaN; po4(z<DD2)=NaN; po4 = squeeze(nanmean(po4,1)) ;
if option2==1   % depth-weighted avg
   po4_KT200 = Fx_var_KTDD_v02(po4,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   po4_KB5 = Fx_var_KBDD_v02(po4,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   po4_KT200 = Fx_var_KTDD_unweighted_v02(po4, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   po4_KB5 = Fx_var_KBDD_unweighted_v02(po4, zKB, DD3);   %gp thickness-weighted average from 0-200m
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			po4_D200(i,j)=po4(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   po4_D0 = squeeze(po4(NZ,:,:));  
end

%
   dataout  = ncread(file, 'SiO3') ;
   dataout = permute(dataout, [3 2 1]);
   sio3 = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3
   sio3 = (sio3./(dens.*0.001)) ;   % convert from mmol/m^3 to umol/kg
   % sio3_KT200 = Fx_var_KTDD_v02(sio3,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % sio3_KB5 = Fx_var_KBDD_v02(sio3,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp sio3(z>DD1 & z<DD2)=NaN; sio3 = squeeze(nanmean(sio3,1)) ;
   % sio3(z>DD1)=NaN; sio3(z<DD2)=NaN; sio3 = squeeze(nanmean(sio3,1)) ;
if option2==1   % depth-weighted avg
   sio3_KT200 = Fx_var_KTDD_v02(sio3,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   sio3_KB5 = Fx_var_KBDD_v02(sio3,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   sio3_KT200 = Fx_var_KTDD_unweighted_v02(sio3, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   sio3_KB5 = Fx_var_KBDD_unweighted_v02(sio3, zKB, DD3);   %gp thickness-weighted average from 0-200m
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			sio3_D200(i,j)=sio3(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   sio3_D0 = squeeze(sio3(NZ,:,:));  
end

%
   dataout  = ncread(file, 'Alk') ;
   dataout = permute(dataout, [3 2 1]);
   alk = squeeze(dataout(:,:,:)) ;   % units of mmol/m^3 in ROMS output
   alk = (alk./(dens.*0.001)) ; %./ 1.0114 ;   % convert to units of umol/kg for input to CO2SYS
   % alk_KT200 = Fx_var_KTDD_v02(alk,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   % alk_KB5 = Fx_var_KBDD_v02(alk,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
   % %gp alk(z>DD1 & z<DD2)=NaN; alk = squeeze(nanmean(alk,1)) ;
   % alk(z>DD1)=NaN; alk(z<DD2)=NaN; alk = squeeze(nanmean(alk,1)) ;
if option2==1   % depth-weighted avg
   alk_KT200 = Fx_var_KTDD_v02(alk,DepthWeight_KT200);   %gp thickness-weighted average from 0-200m
   alk_KB5 = Fx_var_KBDD_v02(alk,DepthWeight_KB5);   %gp thickness-weighted average from 0-200m
elseif option2==0   % unweighted avg
   alk_KT200 = Fx_var_KTDD_unweighted_v02(alk, zKT, DD1, DD2);   %gp thickness-weighted average from 0-200m
   alk_KB5 = Fx_var_KBDD_unweighted_v02(alk, zKB, DD3);   %gp thickness-weighted average from 0-200m
end
%
if option7==1
   for i=1:NY
		for j=1:NX
			alk_D200(i,j)=alk(idxKTDD(i,j),i,j);
		end		% for j
   end 	% for i
   alk_D0 = squeeze(alk(NZ,:,:));  
end

%
%
% ---------- CO2SYS for existing conditions ----------
%
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2, convert to db
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_co2sys = DATA(:,3) ;% pHtotal
pH_KT200_co2sys = DATA(:,33) ;% pHtotal
pHsws_KT200_co2sys = DATA(:,34) ;% pHsws
pCO2_KT200_co2sys = DATA(:,4) ;% (uatm)
xCO2_KT200_co2sys = DATA(:,17) ;% (ppm)
RF_KT200_co2sys = DATA(:,14) ;% Revelle Factor
omcal_KT200_co2sys = DATA(:,15) ;% omega calcite
omara_KT200_co2sys = DATA(:,16) ;% omega ara 16
pH3_KT200_co2sys = reshape(pH3_KT200_co2sys,NY,NX);
pH_KT200_co2sys = reshape(pH_KT200_co2sys,NY,NX);
pHsws_KT200_co2sys = reshape(pHsws_KT200_co2sys,NY,NX);
pCO2_KT200_co2sys = reshape(pCO2_KT200_co2sys,NY,NX);
xCO2_KT200_co2sys = reshape(xCO2_KT200_co2sys,NY,NX);
RF_KT200_co2sys = reshape(RF_KT200_co2sys,NY,NX);
omcal_KT200_co2sys = reshape(omcal_KT200_co2sys,NY,NX);
omara_KT200_co2sys = reshape(omara_KT200_co2sys,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_co2sys = DATA(:,33) ;% pHtotal
pHsws_KB5_co2sys = DATA(:,34) ;% pHsws
pCO2_KB5_co2sys = DATA(:,4) ;% (uatm)
xCO2_KB5_co2sys = DATA(:,17) ;% (ppm)
RF_KB5_co2sys = DATA(:,14) ;% Revelle Factor
omcal_KB5_co2sys = DATA(:,15) ;% omega calcite
omara_KB5_co2sys = DATA(:,16) ;% omega ara 16
pH_KB5_co2sys = reshape(pH_KB5_co2sys,NY,NX);
pHsws_KB5_co2sys = reshape(pHsws_KB5_co2sys,NY,NX);
pCO2_KB5_co2sys = reshape(pCO2_KB5_co2sys,NY,NX);
xCO2_KB5_co2sys = reshape(xCO2_KB5_co2sys,NY,NX);
RF_KB5_co2sys = reshape(RF_KB5_co2sys,NY,NX);
omcal_KB5_co2sys = reshape(omcal_KB5_co2sys,NY,NX);
omara_KB5_co2sys = reshape(omara_KB5_co2sys,NY,NX);

if option6~=0
disp(['start Canthro DICexcess ...  '])
%
% ---------- CO2SYS to calc Existing conditions DICatm ----------
%
% find atmospheric xCO2 (ppm)
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200 = reshape(DICatm_KT200,NY,NX);
DICexcess_KT200 = dic_KT200 - DICatm_KT200;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5 = reshape(DICatm_KB5,NY,NX);
DICexcess_KB5 = dic_KB5 - DICatm_KB5;
%
% ---------- CO2SYS to calc DICatm and DIC in year 1765 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 1765 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_1765(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_1765(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_1765(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_1765(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_1765 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_1765 = reshape(DICatm_KT200_1765,NY,NX);
dic_KT200_1765 = DICexcess_KT200 + DICatm_KT200_1765;
dic_KT200_1765(dic_KT200_1765<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_1765 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_1765 = reshape(DICatm_KB5_1765,NY,NX);
dic_KB5_1765 = DICexcess_KB5 + DICatm_KB5_1765;
dic_KB5_1765(dic_KB5_1765<0)=0;
%
% ---------- CO2SYS to calc DICatm and DIC in year 2020 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 2020 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_2020(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_2020(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_2020(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_2020(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_2020 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_2020 = reshape(DICatm_KT200_2020,NY,NX);
dic_KT200_2020 = DICexcess_KT200 + DICatm_KT200_2020;
dic_KT200_2020(dic_KT200_2020<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_2020 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_2020 = reshape(DICatm_KB5_2020,NY,NX);
dic_KB5_2020 = DICexcess_KB5 + DICatm_KB5_2020;
dic_KB5_2020(dic_KB5_2020<0)=0;
%
%
% ---------- CO2SYS to calc DICatm and DIC in year 2040 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 2040 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_2040(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_2040(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_2040(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_2040(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_2040 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_2040 = reshape(DICatm_KT200_2040,NY,NX);
dic_KT200_2040 = DICexcess_KT200 + DICatm_KT200_2040;
dic_KT200_2040(dic_KT200_2040<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_2040 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_2040 = reshape(DICatm_KB5_2040,NY,NX);
dic_KB5_2040 = DICexcess_KB5 + DICatm_KB5_2040;
dic_KB5_2040(dic_KB5_2040<0)=0;
%
%
% ---------- CO2SYS to calc DICatm and DIC in year 2060 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 2060 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_2060(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_2060(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_2060(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_2060(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_2060 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_2060 = reshape(DICatm_KT200_2060,NY,NX);
dic_KT200_2060 = DICexcess_KT200 + DICatm_KT200_2060;
dic_KT200_2060(dic_KT200_2060<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_2060 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_2060 = reshape(DICatm_KB5_2060,NY,NX);
dic_KB5_2060 = DICexcess_KB5 + DICatm_KB5_2060;
dic_KB5_2060(dic_KB5_2060<0)=0;
%
%
% ---------- CO2SYS to calc DICatm and DIC in year 2080 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 2080 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_2080(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_2080(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_2080(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_2080(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_2080 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_2080 = reshape(DICatm_KT200_2080,NY,NX);
dic_KT200_2080 = DICexcess_KT200 + DICatm_KT200_2080;
dic_KT200_2080(dic_KT200_2080<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_2080 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_2080 = reshape(DICatm_KB5_2080,NY,NX);
dic_KB5_2080 = DICexcess_KB5 + DICatm_KB5_2080;
dic_KB5_2080(dic_KB5_2080<0)=0;
%
% ---------- CO2SYS to calc DICatm and DIC in year 2100 ----------
%
% find atmospheric xCO2 (ppm)
disp(['start Canthro DIC 2100 ...  '])
if option6==1
	xCO2=Fx_RCP85_xCO2_v01(years_2100(fr));
elseif option6==2
	xCO2=Fx_RCP60_xCO2_v01(years_2100(fr));
elseif option6==3
	xCO2=Fx_RCP45_xCO2_v01(years_2100(fr));
elseif option6==4
	xCO2=Fx_RCP26_xCO2_v01(years_2100(fr));
end
xCO2IN=xCO2.*ones(numel(dic_KT200(:)),1);   %! in this version assume pCO2=xCO2
% pCO2IN=xCO2IN;   %! in this version assume pCO2=xCO2
%gp KT200
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
pCO2IN=x2pCO2(salt_KT200(:),temp_KT200(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KT200_2100 = DATA(:,2) ;% TCO2 at input condition
DICatm_KT200_2100 = reshape(DICatm_KT200_2100,NY,NX);
dic_KT200_2100 = DICexcess_KT200 + DICatm_KT200_2100;
dic_KT200_2100(dic_KT200_2100<0)=0;
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 4 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
pCO2IN=x2pCO2(salt_KB5(:),temp_KB5(:),1,xCO2IN(:));   % convert xCO2 to pCO2
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),pCO2IN(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DICatm_KB5_2100 = DATA(:,2) ;% TCO2 at input condition
DICatm_KB5_2100 = reshape(DICatm_KB5_2100,NY,NX);
dic_KB5_2100 = DICexcess_KB5 + DICatm_KB5_2100;
dic_KB5_2100(dic_KB5_2100<0)=0;

%
%
% ---------- CO2SYS for year 1765 ----------
%
%gp KT200
disp(['start Canthro CO2SYS 1765 ...  '])
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_1765(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_1765 = DATA(:,3) ;% pHtotal
pH_KT200_1765 = DATA(:,33) ;% pHtotal
pCO2_KT200_1765 = DATA(:,4) ;% (uatm)
RF_KT200_1765 = DATA(:,14) ;% Revelle Factor
omcal_KT200_1765 = DATA(:,15) ;% omega calcite
omara_KT200_1765 = DATA(:,16) ;% omega ara 16
pH3_KT200_1765 = reshape(pH3_KT200_1765,NY,NX);
pH_KT200_1765 = reshape(pH_KT200_1765,NY,NX);
pCO2_KT200_1765 = reshape(pCO2_KT200_1765,NY,NX);
RF_KT200_1765 = reshape(RF_KT200_1765,NY,NX);
omcal_KT200_1765 = reshape(omcal_KT200_1765,NY,NX);
omara_KT200_1765 = reshape(omara_KT200_1765,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_1765(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_1765 = DATA(:,33) ;% pHtotal
pCO2_KB5_1765 = DATA(:,4) ;% (uatm)
RF_KB5_1765 = DATA(:,14) ;% Revelle Factor
omcal_KB5_1765 = DATA(:,15) ;% omega calcite
omara_KB5_1765 = DATA(:,16) ;% omega ara 16
pH_KB5_1765 = reshape(pH_KB5_1765,NY,NX);
pCO2_KB5_1765 = reshape(pCO2_KB5_1765,NY,NX);
RF_KB5_1765 = reshape(RF_KB5_1765,NY,NX);
omcal_KB5_1765 = reshape(omcal_KB5_1765,NY,NX);
omara_KB5_1765 = reshape(omara_KB5_1765,NY,NX);

%
%
% ---------- CO2SYS for year 2020 ----------
%
disp(['start Canthro CO2SYS 2020 ...  '])
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_2020(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_2020 = DATA(:,3) ;% pHtotal
pH_KT200_2020 = DATA(:,33) ;% pHtotal
pCO2_KT200_2020 = DATA(:,4) ;% (uatm)
RF_KT200_2020 = DATA(:,14) ;% Revelle Factor
omcal_KT200_2020 = DATA(:,15) ;% omega calcite
omara_KT200_2020 = DATA(:,16) ;% omega ara 16
pH3_KT200_2020 = reshape(pH3_KT200_2020,NY,NX);
pH_KT200_2020 = reshape(pH_KT200_2020,NY,NX);
pCO2_KT200_2020 = reshape(pCO2_KT200_2020,NY,NX);
RF_KT200_2020 = reshape(RF_KT200_2020,NY,NX);
omcal_KT200_2020 = reshape(omcal_KT200_2020,NY,NX);
omara_KT200_2020 = reshape(omara_KT200_2020,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_2020(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_2020 = DATA(:,33) ;% pHtotal
pCO2_KB5_2020 = DATA(:,4) ;% (uatm)
RF_KB5_2020 = DATA(:,14) ;% Revelle Factor
omcal_KB5_2020 = DATA(:,15) ;% omega calcite
omara_KB5_2020 = DATA(:,16) ;% omega ara 16
pH_KB5_2020 = reshape(pH_KB5_2020,NY,NX);
pCO2_KB5_2020 = reshape(pCO2_KB5_2020,NY,NX);
RF_KB5_2020 = reshape(RF_KB5_2020,NY,NX);
omcal_KB5_2020 = reshape(omcal_KB5_2020,NY,NX);
omara_KB5_2020 = reshape(omara_KB5_2020,NY,NX);

%
%
% ---------- CO2SYS for year 2040 ----------
%
disp(['start Canthro CO2SYS 2040 ...  '])
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_2040(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_2040 = DATA(:,3) ;% pHtotal
pH_KT200_2040 = DATA(:,33) ;% pHtotal
pCO2_KT200_2040 = DATA(:,4) ;% (uatm)
RF_KT200_2040 = DATA(:,14) ;% Revelle Factor
omcal_KT200_2040 = DATA(:,15) ;% omega calcite
omara_KT200_2040 = DATA(:,16) ;% omega ara 16
pH3_KT200_2040 = reshape(pH3_KT200_2040,NY,NX);
pH_KT200_2040 = reshape(pH_KT200_2040,NY,NX);
pCO2_KT200_2040 = reshape(pCO2_KT200_2040,NY,NX);
RF_KT200_2040 = reshape(RF_KT200_2040,NY,NX);
omcal_KT200_2040 = reshape(omcal_KT200_2040,NY,NX);
omara_KT200_2040 = reshape(omara_KT200_2040,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_2040(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_2040 = DATA(:,33) ;% pHtotal
pCO2_KB5_2040 = DATA(:,4) ;% (uatm)
RF_KB5_2040 = DATA(:,14) ;% Revelle Factor
omcal_KB5_2040 = DATA(:,15) ;% omega calcite
omara_KB5_2040 = DATA(:,16) ;% omega ara 16
pH_KB5_2040 = reshape(pH_KB5_2040,NY,NX);
pCO2_KB5_2040 = reshape(pCO2_KB5_2040,NY,NX);
RF_KB5_2040 = reshape(RF_KB5_2040,NY,NX);
omcal_KB5_2040 = reshape(omcal_KB5_2040,NY,NX);
omara_KB5_2040 = reshape(omara_KB5_2040,NY,NX);

%
%
% ---------- CO2SYS for year 2060 ----------
%
disp(['start Canthro CO2SYS 2060 ...  '])
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_2060(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_2060 = DATA(:,3) ;% pHtotal
pH_KT200_2060 = DATA(:,33) ;% pHtotal
pCO2_KT200_2060 = DATA(:,4) ;% (uatm)
RF_KT200_2060 = DATA(:,14) ;% Revelle Factor
omcal_KT200_2060 = DATA(:,15) ;% omega calcite
omara_KT200_2060 = DATA(:,16) ;% omega ara 16
pH3_KT200_2060 = reshape(pH3_KT200_2060,NY,NX);
pH_KT200_2060 = reshape(pH_KT200_2060,NY,NX);
pCO2_KT200_2060 = reshape(pCO2_KT200_2060,NY,NX);
RF_KT200_2060 = reshape(RF_KT200_2060,NY,NX);
omcal_KT200_2060 = reshape(omcal_KT200_2060,NY,NX);
omara_KT200_2060 = reshape(omara_KT200_2060,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_2060(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_2060 = DATA(:,33) ;% pHtotal
pCO2_KB5_2060 = DATA(:,4) ;% (uatm)
RF_KB5_2060 = DATA(:,14) ;% Revelle Factor
omcal_KB5_2060 = DATA(:,15) ;% omega calcite
omara_KB5_2060 = DATA(:,16) ;% omega ara 16
pH_KB5_2060 = reshape(pH_KB5_2060,NY,NX);
pCO2_KB5_2060 = reshape(pCO2_KB5_2060,NY,NX);
RF_KB5_2060 = reshape(RF_KB5_2060,NY,NX);
omcal_KB5_2060 = reshape(omcal_KB5_2060,NY,NX);
omara_KB5_2060 = reshape(omara_KB5_2060,NY,NX);

%
%
% ---------- CO2SYS for year 2080 ----------
%
disp(['start Canthro CO2SYS 2080 ...  '])
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_2080(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_2080 = DATA(:,3) ;% pHtotal
pH_KT200_2080 = DATA(:,33) ;% pHtotal
pCO2_KT200_2080 = DATA(:,4) ;% (uatm)
RF_KT200_2080 = DATA(:,14) ;% Revelle Factor
omcal_KT200_2080 = DATA(:,15) ;% omega calcite
omara_KT200_2080 = DATA(:,16) ;% omega ara 16
pH3_KT200_2080 = reshape(pH3_KT200_2080,NY,NX);
pH_KT200_2080 = reshape(pH_KT200_2080,NY,NX);
pCO2_KT200_2080 = reshape(pCO2_KT200_2080,NY,NX);
RF_KT200_2080 = reshape(RF_KT200_2080,NY,NX);
omcal_KT200_2080 = reshape(omcal_KT200_2080,NY,NX);
omara_KT200_2080 = reshape(omara_KT200_2080,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_2080(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_2080 = DATA(:,33) ;% pHtotal
pCO2_KB5_2080 = DATA(:,4) ;% (uatm)
RF_KB5_2080 = DATA(:,14) ;% Revelle Factor
omcal_KB5_2080 = DATA(:,15) ;% omega calcite
omara_KB5_2080 = DATA(:,16) ;% omega ara 16
pH_KB5_2080 = reshape(pH_KB5_2080,NY,NX);
pCO2_KB5_2080 = reshape(pCO2_KB5_2080,NY,NX);
RF_KB5_2080 = reshape(RF_KB5_2080,NY,NX);
omcal_KB5_2080 = reshape(omcal_KB5_2080,NY,NX);
omara_KB5_2080 = reshape(omara_KB5_2080,NY,NX);

%
%
% ---------- CO2SYS for year 2100 ----------
%
disp(['start Canthro CO2SYS 2100 ...  '])
%gp KT200
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate KB200 at midpoint depth of 100m
PRESIN=m2db(((DD1+DD2)./2).*ones(numel(dic_KT200(:)),1));   % midpoint of DD1 and DD2 
PRESOUT=NaN(numel(dic_KT200(:)),1);   
TEMPOUT=NaN(numel(dic_KT200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KT200(:)./(1+0.0114),dic_KT200_2100(:),PAR1TYPE,PAR2TYPE,...
    salt_KT200(:),temp_KT200(:),nan,...
    PRESIN(:),nan,...
    sio3_KT200(:),po4_KT200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH3_KT200_2100 = DATA(:,3) ;% pHtotal
pH_KT200_2100 = DATA(:,33) ;% pHtotal
pCO2_KT200_2100 = DATA(:,4) ;% (uatm)
RF_KT200_2100 = DATA(:,14) ;% Revelle Factor
omcal_KT200_2100 = DATA(:,15) ;% omega calcite
omara_KT200_2100 = DATA(:,16) ;% omega ara 16
pH3_KT200_2100 = reshape(pH3_KT200_2100,NY,NX);
pH_KT200_2100 = reshape(pH_KT200_2100,NY,NX);
pCO2_KT200_2100 = reshape(pCO2_KT200_2100,NY,NX);
RF_KT200_2100 = reshape(RF_KT200_2100,NY,NX);
omcal_KT200_2100 = reshape(omcal_KT200_2100,NY,NX);
omara_KT200_2100 = reshape(omara_KT200_2100,NY,NX);
%
%gp KB5
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
TotalDepth = h + zeta;   % evaluate CO2SYS for KB5 at bottom depth
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_KB5(:)./(1+0.0114),dic_KB5_2100(:),PAR1TYPE,PAR2TYPE,...
    salt_KB5(:),temp_KB5(:),nan,...
    m2db(TotalDepth(:)),nan,...
    sio3_KB5(:),po4_KB5(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_KB5_2100 = DATA(:,33) ;% pHtotal
pCO2_KB5_2100 = DATA(:,4) ;% (uatm)
RF_KB5_2100 = DATA(:,14) ;% Revelle Factor
omcal_KB5_2100 = DATA(:,15) ;% omega calcite
omara_KB5_2100 = DATA(:,16) ;% omega ara 16
pH_KB5_2100 = reshape(pH_KB5_2100,NY,NX);
pCO2_KB5_2100 = reshape(pCO2_KB5_2100,NY,NX);
RF_KB5_2100 = reshape(RF_KB5_2100,NY,NX);
omcal_KB5_2100 = reshape(omcal_KB5_2100,NY,NX);
omara_KB5_2100 = reshape(omara_KB5_2100,NY,NX);

end   % if option6

%
if option7==1

disp(['start CO2SYS at D200m and D0m ...  '])
%
%
% ---------- CO2SYS for existing conditions at depth 200m and 0m ----------
%
%gp D200m
PAR1TYPE =  1 ; % al% 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2k
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
% evaluate at depth DD1
PRESIN=m2db(DD1.*ones(numel(dic_D200(:)),1));   % at depth DD1, convert to db
PRESOUT=NaN(numel(dic_D200(:)),1);   
TEMPOUT=NaN(numel(dic_D200(:)),1);   
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_D200(:)./(1+0.0114),dic_D200(:),PAR1TYPE,PAR2TYPE,...
    salt_D200(:),temp_D200(:),nan,...
    PRESIN(:),nan,...
    sio3_D200(:),po4_D200(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_D200_co2sys = DATA(:,33) ;% pHtotal
pHsws_D200_co2sys = DATA(:,34) ;% pHsws
pCO2_D200_co2sys = DATA(:,4) ;% (uatm)
xCO2_D200_co2sys = DATA(:,17) ;% (ppm)
RF_D200_co2sys = DATA(:,14) ;% Revelle Factor
omcal_D200_co2sys = DATA(:,15) ;% omega calcite
omara_D200_co2sys = DATA(:,16) ;% omega ara 16
pH_D200_co2sys = reshape(pH_D200_co2sys,NY,NX);
pHsws_D200_co2sys = reshape(pHsws_D200_co2sys,NY,NX);
pCO2_D200_co2sys = reshape(pCO2_D200_co2sys,NY,NX);
xCO2_D200_co2sys = reshape(xCO2_D200_co2sys,NY,NX);
RF_D200_co2sys = reshape(RF_D200_co2sys,NY,NX);
omcal_D200_co2sys = reshape(omcal_D200_co2sys,NY,NX);
omara_D200_co2sys = reshape(omara_D200_co2sys,NY,NX);
%
%gp D0m
PAR1TYPE =  1 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
PAR2TYPE = 2 ; % 1=alk, 2=dic, 3=pH, 4=pCO2, 5=fCO2
pHSCALEIN = 1 ;  %gp total scale
K1K2CONSTANTS = 10 ; %gp Lueker et al 2000
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
PRESIN=zeros(numel(dic_D0(:)),1);   % at depth DD1, convert to db
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk_D0(:)./(1+0.0114),dic_D0(:),PAR1TYPE,PAR2TYPE,...
    salt_D0(:),temp_D0(:),nan,...
    PRESIN(:),nan,...
    sio3_D0(:),po4_D0(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
pH_D0_co2sys = DATA(:,33) ;% pHtotal
pHsws_D0_co2sys = DATA(:,34) ;% pHsws
pCO2_D0_co2sys = DATA(:,4) ;% (uatm)
xCO2_D0_co2sys = DATA(:,17) ;% (ppm)
RF_D0_co2sys = DATA(:,14) ;% Revelle Factor
omcal_D0_co2sys = DATA(:,15) ;% omega calcite
omara_D0_co2sys = DATA(:,16) ;% omega ara 16
pH_D0_co2sys = reshape(pH_D0_co2sys,NY,NX);
pHsws_D0_co2sys = reshape(pHsws_D0_co2sys,NY,NX);
pCO2_D0_co2sys = reshape(pCO2_D0_co2sys,NY,NX);
xCO2_D0_co2sys = reshape(xCO2_D0_co2sys,NY,NX);
RF_D0_co2sys = reshape(RF_D0_co2sys,NY,NX);
omcal_D0_co2sys = reshape(omcal_D0_co2sys,NY,NX);
omara_D0_co2sys = reshape(omara_D0_co2sys,NY,NX);
%
end		% if option7==1

end   % if option1 || option6

% Calculate omega aragonite option4 (Juranek et al 2014, applied on USW coast)
if option4 == 1
% [OM,Err] = juranek_aragsat(temp,o2) ;
[OM_KT200,Err] = juranek_aragsat(temp_KT200,o2_KT200) ;   %gp
[OM_KB5,Err] = juranek_aragsat(temp_KB5,o2_KB5) ;   %gp
end

% CO2SYS
if option1==1
% CO2SYS
% % original unweighted avg with Millero et al 2010
% pH(pH==0)=NaN;
% pCO2(pCO2==0)=NaN;
% RF(RF==0)=NaN;
% cal(cal==0)=NaN;
% om(om==0)=NaN;
% % depth-weighted average 0-200m with Millero et al 2010
% pH_KT200(pH_KT200==0)=NaN;
% pCO2_KT200(pCO2_KT200==0)=NaN;
% RF_KT200(RF_KT200==0)=NaN;
% cal_KT200(cal_KT200==0)=NaN;
% om_KT200(om_KT200==0)=NaN;   %gp
% depth-weighted average 0-200 with Lueker et al 2000
%
% KT200
pH_KT200_co2sys(pH_KT200_co2sys==0)=NaN;
pHsws_KT200_co2sys(pHsws_KT200_co2sys==0)=NaN;
pCO2_KT200_co2sys(pCO2_KT200_co2sys==0)=NaN;
xCO2_KT200_co2sys(xCO2_KT200_co2sys==0)=NaN;
RF_KT200_co2sys(RF_KT200_co2sys==0)=NaN;
omcal_KT200_co2sys(omcal_KT200_co2sys==0)=NaN;
omara_KT200_co2sys(omara_KT200_co2sys==0)=NaN;   
% KB5
pH_KB5_co2sys(pH_KB5_co2sys==0)=NaN;
pHsws_KB5_co2sys(pHsws_KB5_co2sys==0)=NaN;
pCO2_KB5_co2sys(pCO2_KB5_co2sys==0)=NaN;
xCO2_KB5_co2sys(xCO2_KB5_co2sys==0)=NaN;
RF_KB5_co2sys(RF_KB5_co2sys==0)=NaN;
omcal_KB5_co2sys(omcal_KB5_co2sys==0)=NaN;
omara_KB5_co2sys(omara_KB5_co2sys==0)=NaN;   
%
if option7==1
% D200
pH_D200_co2sys(pH_D200_co2sys==0)=NaN;
pHsws_D200_co2sys(pHsws_D200_co2sys==0)=NaN;
pCO2_D200_co2sys(pCO2_D200_co2sys==0)=NaN;
xCO2_D200_co2sys(xCO2_D200_co2sys==0)=NaN;
RF_D200_co2sys(RF_D200_co2sys==0)=NaN;
omcal_D200_co2sys(omcal_D200_co2sys==0)=NaN;
omara_D200_co2sys(omara_D200_co2sys==0)=NaN;   
% D0
pH_D0_co2sys(pH_D0_co2sys==0)=NaN;
pHsws_D0_co2sys(pHsws_D0_co2sys==0)=NaN;
pCO2_D0_co2sys(pCO2_D0_co2sys==0)=NaN;
xCO2_D0_co2sys(xCO2_D0_co2sys==0)=NaN;
RF_D0_co2sys(RF_D0_co2sys==0)=NaN;
omcal_D0_co2sys(omcal_D0_co2sys==0)=NaN;
omara_D0_co2sys(omara_D0_co2sys==0)=NaN;   
end 	% if option7==1
%
end		% if option1==1

if option6~=0
% Existing condition
DICatm_KT200(mask==0)=NaN; 
DICatm_KB5(mask==0)=NaN; 
DICexcess_KT200(mask==0)=NaN; 
DICexcess_KB5(mask==0)=NaN; 
% 1765
% KT200
dic_KT200_1765(mask==0)=NaN; 
DICatm_KT200_1765(mask==0)=NaN; 
pH_KT200_1765(mask==0)=NaN; 
pCO2_KT200_1765(mask==0)=NaN; 
RF_KT200_1765(mask==0)=NaN; 
omcal_KT200_1765(mask==0)=NaN; 
omara_KT200_1765(mask==0)=NaN; 
% KB5
dic_KB5_1765(mask==0)=NaN; 
DICatm_KT200_1765(mask==0)=NaN; 
pH_KB5_1765(mask==0)=NaN; 
pCO2_KB5_1765(mask==0)=NaN; 
RF_KB5_1765(mask==0)=NaN; 
omcal_KB5_1765(mask==0)=NaN; 
omara_KB5_1765(mask==0)=NaN; 
% 2020
% KT200
dic_KT200_2020(mask==0)=NaN; 
DICatm_KT200_2020(mask==0)=NaN; 
pH_KT200_2020(mask==0)=NaN; 
pCO2_KT200_2020(mask==0)=NaN; 
RF_KT200_2020(mask==0)=NaN; 
omcal_KT200_2020(mask==0)=NaN; 
omara_KT200_2020(mask==0)=NaN; 
% KB5
dic_KB5_2020(mask==0)=NaN; 
DICatm_KB5_2020(mask==0)=NaN; 
pH_KB5_2020(mask==0)=NaN; 
pCO2_KB5_2020(mask==0)=NaN; 
RF_KB5_2020(mask==0)=NaN; 
omcal_KB5_2020(mask==0)=NaN; 
omara_KB5_2020(mask==0)=NaN; 
% 2040
% KT200
dic_KT200_2040(mask==0)=NaN; 
DICatm_KT200_2040(mask==0)=NaN; 
pH_KT200_2040(mask==0)=NaN; 
pCO2_KT200_2040(mask==0)=NaN; 
RF_KT200_2040(mask==0)=NaN; 
omcal_KT200_2040(mask==0)=NaN; 
omara_KT200_2040(mask==0)=NaN; 
% KB5
dic_KB5_2040(mask==0)=NaN; 
DICatm_KB5_2040(mask==0)=NaN; 
pH_KB5_2040(mask==0)=NaN; 
pCO2_KB5_2040(mask==0)=NaN; 
RF_KB5_2040(mask==0)=NaN; 
omcal_KB5_2040(mask==0)=NaN; 
omara_KB5_2040(mask==0)=NaN; 
% 2060
% KT200
dic_KT200_2060(mask==0)=NaN; 
DICatm_KT200_2060(mask==0)=NaN; 
pH_KT200_2060(mask==0)=NaN; 
pCO2_KT200_2060(mask==0)=NaN; 
RF_KT200_2060(mask==0)=NaN; 
omcal_KT200_2060(mask==0)=NaN; 
omara_KT200_2060(mask==0)=NaN; 
% KB5
dic_KB5_2060(mask==0)=NaN; 
DICatm_KB5_2060(mask==0)=NaN; 
pH_KB5_2060(mask==0)=NaN; 
pCO2_KB5_2060(mask==0)=NaN; 
RF_KB5_2060(mask==0)=NaN; 
omcal_KB5_2060(mask==0)=NaN; 
omara_KB5_2060(mask==0)=NaN; 
% 2080
% KT200
dic_KT200_2080(mask==0)=NaN; 
DICatm_KT200_2080(mask==0)=NaN; 
pH_KT200_2080(mask==0)=NaN; 
pCO2_KT200_2080(mask==0)=NaN; 
RF_KT200_2080(mask==0)=NaN; 
omcal_KT200_2080(mask==0)=NaN; 
omara_KT200_2080(mask==0)=NaN; 
% KB5
dic_KB5_2080(mask==0)=NaN; 
DICatm_KB5_2080(mask==0)=NaN; 
pH_KB5_2080(mask==0)=NaN; 
pCO2_KB5_2080(mask==0)=NaN; 
RF_KB5_2080(mask==0)=NaN; 
omcal_KB5_2080(mask==0)=NaN; 
omara_KB5_2080(mask==0)=NaN; 
% 2100
% KT200
dic_KT200_2100(mask==0)=NaN; 
DICatm_KT200_2100(mask==0)=NaN; 
pH_KT200_2100(mask==0)=NaN; 
pCO2_KT200_2100(mask==0)=NaN; 
RF_KT200_2100(mask==0)=NaN; 
omcal_KT200_2100(mask==0)=NaN; 
omara_KT200_2100(mask==0)=NaN; 
% KB5
dic_KB5_2100(mask==0)=NaN; 
DICatm_KB5_2100(mask==0)=NaN; 
pH_KB5_2100(mask==0)=NaN; 
pCO2_KB5_2100(mask==0)=NaN; 
RF_KB5_2100(mask==0)=NaN; 
omcal_KB5_2100(mask==0)=NaN; 
omara_KB5_2100(mask==0)=NaN; 
% write nc for Existing
ncwrite(fout1_DICatm_KT200, 'var', DICatm_KT200' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5, 'var', DICatm_KB5' , [1 1 cpt]);
ncwrite(fout1_DICexcess_KT200, 'var', DICexcess_KT200' , [1 1 cpt]);
ncwrite(fout1_DICexcess_KB5, 'var', DICexcess_KB5' , [1 1 cpt]);
% write nc for 1765
ncwrite(fout1_dic_KT200_1765, 'var', dic_KT200_1765' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_1765, 'var', dic_KB5_1765' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_1765, 'var', DICatm_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_1765, 'var', DICatm_KB5_1765' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_1765, 'var', pH_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_1765, 'var', pH_KB5_1765' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_1765, 'var', pCO2_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_1765, 'var', pCO2_KB5_1765' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_1765, 'var', RF_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_1765, 'var', RF_KB5_1765' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_1765, 'var', omcal_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_1765, 'var', omcal_KB5_1765' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_1765, 'var', omara_KT200_1765' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_1765, 'var', omara_KB5_1765' , [1 1 cpt]);
% write nc for 2020
ncwrite(fout1_dic_KT200_2020, 'var', dic_KT200_2020' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_2020, 'var', dic_KB5_2020' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_2020, 'var', DICatm_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_2020, 'var', DICatm_KB5_2020' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_2020, 'var', pH_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_2020, 'var', pH_KB5_2020' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_2020, 'var', pCO2_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_2020, 'var', pCO2_KB5_2020' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_2020, 'var', RF_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_2020, 'var', RF_KB5_2020' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_2020, 'var', omcal_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_2020, 'var', omcal_KB5_2020' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_2020, 'var', omara_KT200_2020' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_2020, 'var', omara_KB5_2020' , [1 1 cpt]);
% write nc for 2040
ncwrite(fout1_dic_KT200_2040, 'var', dic_KT200_2040' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_2040, 'var', dic_KB5_2040' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_2040, 'var', DICatm_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_2040, 'var', DICatm_KB5_2040' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_2040, 'var', pH_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_2040, 'var', pH_KB5_2040' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_2040, 'var', pCO2_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_2040, 'var', pCO2_KB5_2040' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_2040, 'var', RF_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_2040, 'var', RF_KB5_2040' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_2040, 'var', omcal_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_2040, 'var', omcal_KB5_2040' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_2040, 'var', omara_KT200_2040' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_2040, 'var', omara_KB5_2040' , [1 1 cpt]);
% write nc for 2060
ncwrite(fout1_dic_KT200_2060, 'var', dic_KT200_2060' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_2060, 'var', dic_KB5_2060' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_2060, 'var', DICatm_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_2060, 'var', DICatm_KB5_2060' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_2060, 'var', pH_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_2060, 'var', pH_KB5_2060' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_2060, 'var', pCO2_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_2060, 'var', pCO2_KB5_2060' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_2060, 'var', RF_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_2060, 'var', RF_KB5_2060' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_2060, 'var', omcal_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_2060, 'var', omcal_KB5_2060' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_2060, 'var', omara_KT200_2060' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_2060, 'var', omara_KB5_2060' , [1 1 cpt]);
% write nc for 2080
ncwrite(fout1_dic_KT200_2080, 'var', dic_KT200_2080' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_2080, 'var', dic_KB5_2080' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_2080, 'var', DICatm_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_2080, 'var', DICatm_KB5_2080' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_2080, 'var', pH_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_2080, 'var', pH_KB5_2080' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_2080, 'var', pCO2_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_2080, 'var', pCO2_KB5_2080' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_2080, 'var', RF_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_2080, 'var', RF_KB5_2080' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_2080, 'var', omcal_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_2080, 'var', omcal_KB5_2080' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_2080, 'var', omara_KT200_2080' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_2080, 'var', omara_KB5_2080' , [1 1 cpt]);
% write nc for 2100
ncwrite(fout1_dic_KT200_2100, 'var', dic_KT200_2100' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5_2100, 'var', dic_KB5_2100' , [1 1 cpt]);   
ncwrite(fout1_DICatm_KT200_2100, 'var', DICatm_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_DICatm_KB5_2100, 'var', DICatm_KB5_2100' , [1 1 cpt]);
ncwrite(fout1_pH_KT200_2100, 'var', pH_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_2100, 'var', pH_KB5_2100' , [1 1 cpt]);
ncwrite(fout1_pCO2_KT200_2100, 'var', pCO2_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_2100, 'var', pCO2_KB5_2100' , [1 1 cpt]);
ncwrite(fout1_RF_KT200_2100, 'var', RF_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_2100, 'var', RF_KB5_2100' , [1 1 cpt]);
ncwrite(fout1_omcal_KT200_2100, 'var', omcal_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_2100, 'var', omcal_KB5_2100' , [1 1 cpt]);
ncwrite(fout1_omara_KT200_2100, 'var', omara_KT200_2100' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_2100, 'var', omara_KB5_2100' , [1 1 cpt]);
end

% Juranek
if option4 == 1
% OM(OM==0)=NaN;
OM_KT200(OM_KT200==0)=NaN;   %gp
OM_KB5(OM_KB5==0)=NaN;   %gp
end

%% write the 2D maps

if option5==1
TotalDepth(mask==0)=NaN; 
zeta(mask==0)=NaN; 
ncwrite(fout1_dep, 'var', TotalDepth' , [1 1 cpt]);
ncwrite(fout1_zeta, 'var', zeta' , [1 1 cpt]);
end

if option1==1 || option6~=0
% CO2SYS outputs
%
% mask land
% KT200
pH_KT200_co2sys(mask==0)=NaN; 
pHsws_KT200_co2sys(mask==0)=NaN; 
pCO2_KT200_co2sys(mask==0)=NaN; 
xCO2_KT200_co2sys(mask==0)=NaN; 
RF_KT200_co2sys(mask==0)=NaN; 
omcal_KT200_co2sys(mask==0)=NaN; 
omara_KT200_co2sys(mask==0)=NaN; 
% KB5
pH_KB5_co2sys(mask==0)=NaN; 
pHsws_KB5_co2sys(mask==0)=NaN; 
pCO2_KB5_co2sys(mask==0)=NaN; 
xCO2_KB5_co2sys(mask==0)=NaN; 
RF_KB5_co2sys(mask==0)=NaN; 
omcal_KB5_co2sys(mask==0)=NaN; 
omara_KB5_co2sys(mask==0)=NaN; 
%
% write nc
% pHtotal
ncwrite(fout1_pH_KT200_co2sys, 'var', pH_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pH_KB5_co2sys, 'var', pH_KB5_co2sys' , [1 1 cpt]);
% pHsws
ncwrite(fout1_pHsws_KT200_co2sys, 'var', pHsws_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pHsws_KB5_co2sys, 'var', pHsws_KB5_co2sys' , [1 1 cpt]);
% pCO2
ncwrite(fout1_pCO2_KT200_co2sys, 'var', pCO2_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pCO2_KB5_co2sys, 'var', pCO2_KB5_co2sys' , [1 1 cpt]);
% xCO2
ncwrite(fout1_xCO2_KT200_co2sys, 'var', xCO2_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_xCO2_KB5_co2sys, 'var', xCO2_KB5_co2sys' , [1 1 cpt]);
% RF
ncwrite(fout1_RF_KT200_co2sys, 'var', RF_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_RF_KB5_co2sys, 'var', RF_KB5_co2sys' , [1 1 cpt]);
% cal (omega calcite)
ncwrite(fout1_omcal_KT200_co2sys, 'var', omcal_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_omcal_KB5_co2sys, 'var', omcal_KB5_co2sys' , [1 1 cpt]);
% om (omega aragonite)
ncwrite(fout1_omara_KT200_co2sys, 'var', omara_KT200_co2sys' , [1 1 cpt]);
ncwrite(fout1_omara_KB5_co2sys, 'var', omara_KB5_co2sys' , [1 1 cpt]);
%
if option7==1
% D200
pH_D200_co2sys(mask==0)=NaN; 
pHsws_D200_co2sys(mask==0)=NaN; 
pCO2_D200_co2sys(mask==0)=NaN; 
xCO2_D200_co2sys(mask==0)=NaN; 
RF_D200_co2sys(mask==0)=NaN; 
omcal_D200_co2sys(mask==0)=NaN; 
omara_D200_co2sys(mask==0)=NaN; 
% D0
pH_D0_co2sys(mask==0)=NaN; 
pHsws_D0_co2sys(mask==0)=NaN; 
pCO2_D0_co2sys(mask==0)=NaN; 
xCO2_D0_co2sys(mask==0)=NaN; 
RF_D0_co2sys(mask==0)=NaN; 
omcal_D0_co2sys(mask==0)=NaN; 
omara_D0_co2sys(mask==0)=NaN; 
%
% write nc
% pH (total)
ncwrite(fout1_pH_D200_co2sys, 'var', pH_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pH_D0_co2sys, 'var', pH_D0_co2sys' , [1 1 cpt]);
% pH (seawater)
ncwrite(fout1_pHsws_D200_co2sys, 'var', pHsws_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pHsws_D0_co2sys, 'var', pHsws_D0_co2sys' , [1 1 cpt]);
% pCO2
ncwrite(fout1_pCO2_D200_co2sys, 'var', pCO2_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_pCO2_D0_co2sys, 'var', pCO2_D0_co2sys' , [1 1 cpt]);
% xCO2
ncwrite(fout1_xCO2_D200_co2sys, 'var', xCO2_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_xCO2_D0_co2sys, 'var', xCO2_D0_co2sys' , [1 1 cpt]);
% RF
ncwrite(fout1_RF_D200_co2sys, 'var', RF_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_RF_D0_co2sys, 'var', RF_D0_co2sys' , [1 1 cpt]);
% cal (omega calcite)
ncwrite(fout1_omcal_D200_co2sys, 'var', omcal_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_omcal_D0_co2sys, 'var', omcal_D0_co2sys' , [1 1 cpt]);
% om (omega aragonite)
ncwrite(fout1_omara_D200_co2sys, 'var', omara_D200_co2sys' , [1 1 cpt]);
ncwrite(fout1_omara_D0_co2sys, 'var', omara_D0_co2sys' , [1 1 cpt]);
end		% if option7==1
%
end

% Juranek outputs
if option4 == 1
% mask land
OM_KT200(mask==0)=NaN; 
OM_KB5(mask==0)=NaN; 
% write nc
ncwrite(fout2_KT200, 'var', OM_KT200' , [1 1 cpt]);   %gp
ncwrite(fout2_KB5, 'var', OM_KB5' , [1 1 cpt]);   %gp
end

% temp, chla and other chem outputs
if option3 == 1
%
% mask land
% KT200
salt_KT200(mask==0)=NaN; 
po4_KT200(mask==0)=NaN; 
sio3_KT200(mask==0)=NaN; 
dic_KT200(mask==0)=NaN; 
alk_KT200(mask==0)=NaN; 
temp_KT200(mask==0)=NaN; 
o2_KT200(mask==0)=NaN; 
chla_KT200(mask==0)=NaN; 
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
ncwrite(fout1_salt_KT200, 'var', salt_KT200' , [1 1 cpt]);   
ncwrite(fout1_salt_KB5, 'var', salt_KB5' , [1 1 cpt]);   
% po4
ncwrite(fout1_po4_KT200, 'var', po4_KT200' , [1 1 cpt]);   
ncwrite(fout1_po4_KB5, 'var', po4_KB5' , [1 1 cpt]);   
% sio3
ncwrite(fout1_sio3_KT200, 'var', sio3_KT200' , [1 1 cpt]);   
ncwrite(fout1_sio3_KB5, 'var', sio3_KB5' , [1 1 cpt]);   
% dic
ncwrite(fout1_dic_KT200, 'var', dic_KT200' , [1 1 cpt]);   
ncwrite(fout1_dic_KB5, 'var', dic_KB5' , [1 1 cpt]);   
% alk
ncwrite(fout1_alk_KT200, 'var', alk_KT200' , [1 1 cpt]);   
ncwrite(fout1_alk_KB5, 'var', alk_KB5' , [1 1 cpt]);   
% temp
% ncwrite(fout1_temp_KT50, 'var', temp_KT50' , [1 1 cpt]);   
ncwrite(fout1_temp_KT200, 'var', temp_KT200' , [1 1 cpt]);   
ncwrite(fout1_temp_KB5, 'var', temp_KB5' , [1 1 cpt]);   
% chla
% ncwrite(fout1_chla_KT50, 'var', chla_KT50' , [1 1 cpt]);   
ncwrite(fout1_chla_KT200, 'var', chla_KT200' , [1 1 cpt]);   
ncwrite(fout1_chla_KB5, 'var', chla_KB5' , [1 1 cpt]);   
ncwrite(fout1_chla_areal, 'var', chla_areal_2D' , [1 1 cpt]);   
% temp
% ncwrite(fout1_o2_KT50, 'var', o2_KT50' , [1 1 cpt]);   
ncwrite(fout1_o2_KT200, 'var', o2_KT200' , [1 1 cpt]);   
ncwrite(fout1_o2_KB5, 'var', o2_KB5' , [1 1 cpt]);   
if option2==0   % vertical std dev
% mask land
% KT200
temp_std_KT200(mask==0)=NaN; 
chla_std_KT200(mask==0)=NaN; 
o2_std_KT200(mask==0)=NaN; 
% write nc
ncwrite(fout1_temp_std_KT200, 'var', temp_std_KT200' , [1 1 cpt]);   
ncwrite(fout1_chla_std_KT200, 'var', chla_std_KT200' , [1 1 cpt]);   
ncwrite(fout1_o2_std_KT200, 'var', o2_std_KT200' , [1 1 cpt]);   
end    % if option2
%
if option7==1
% mask land
% D200
salt_D200(mask==0)=NaN; 
po4_D200(mask==0)=NaN; 
sio3_D200(mask==0)=NaN; 
dic_D200(mask==0)=NaN; 
alk_D200(mask==0)=NaN; 
temp_D200(mask==0)=NaN; 
o2_D200(mask==0)=NaN; 
chla_D200(mask==0)=NaN; 
% D0
salt_D0(mask==0)=NaN; 
po4_D0(mask==0)=NaN; 
sio3_D0(mask==0)=NaN; 
dic_D0(mask==0)=NaN; 
alk_D0(mask==0)=NaN; 
temp_D0(mask==0)=NaN; 
o2_D0(mask==0)=NaN; 
chla_D0(mask==0)=NaN; 
%
% write nc
% salt
ncwrite(fout1_salt_D200, 'var', salt_D200' , [1 1 cpt]);   
ncwrite(fout1_salt_D0, 'var', salt_D0' , [1 1 cpt]);   
% po4
ncwrite(fout1_po4_D200, 'var', po4_D200' , [1 1 cpt]);   
ncwrite(fout1_po4_D0, 'var', po4_D0' , [1 1 cpt]);   
% sio3
ncwrite(fout1_sio3_D200, 'var', sio3_D200' , [1 1 cpt]);   
ncwrite(fout1_sio3_D0, 'var', sio3_D0' , [1 1 cpt]);   
% dic
ncwrite(fout1_dic_D200, 'var', dic_D200' , [1 1 cpt]);   
ncwrite(fout1_dic_D0, 'var', dic_D0' , [1 1 cpt]);   
% alk
ncwrite(fout1_alk_D200, 'var', alk_D200' , [1 1 cpt]);   
ncwrite(fout1_alk_D0, 'var', alk_D0' , [1 1 cpt]);   
% temp
ncwrite(fout1_temp_D200, 'var', temp_D200' , [1 1 cpt]);   
ncwrite(fout1_temp_D0, 'var', temp_D0' , [1 1 cpt]);   
% chla
ncwrite(fout1_chla_D200, 'var', chla_D200' , [1 1 cpt]);   
ncwrite(fout1_chla_D0, 'var', chla_D0' , [1 1 cpt]);   
% temp
ncwrite(fout1_o2_D200, 'var', o2_D200' , [1 1 cpt]);   
ncwrite(fout1_o2_D0, 'var', o2_D0' , [1 1 cpt]);   
end		% if option7==1
%
end    % if option3


% %gp diagnostic output for debugging/checking
% % offshore
% i=700;
% j=50;
% col1=transpose(1:1:60);
% col2=dz(:,i,j);
% col3=CumDepth(:,i,j);
% col4=DepthWeight_KT200(:,i,j);
% col5=temp_dataout(:,i,j);
% col6=DepthWeight_KT200(:,i,j).*temp_dataout(:,i,j);
        % clear T
        % T=table( ...
            % col1, ...
            % col2, ...
            % col3, ...
            % col4, ...
            % col5, ...
            % col6);
        % T.Properties.VariableNames = { ...
            % 'Layer' ...
            % 'dz' ...
            % 'CumDepth' ...
            % 'DepthWeight_KT200' ...
            % 'temp' ...
            % 'temp_x_DepthWeight_KT200'};
        % filename = ['/data/project4/gregp/tools_matlab/applications/pteropods/check_depwt_offshore_i700j50_v08.xls'];
        % writetable(T,filename,'Sheet',1,'Range','A1');
% % coast
% i=700;
% j=570;
% col1=transpose(1:1:60);
% col2=dz(:,i,j);
% col3=CumDepth(:,i,j);
% col4=DepthWeight_KT200(:,i,j);
% col5=temp_dataout(:,i,j);
% col6=DepthWeight_KT200(:,i,j).*temp_dataout(:,i,j);
        % clear T
        % T=table( ...
            % col1, ...
            % col2, ...
            % col3, ...
            % col4, ...
            % col5, ...
            % col6);
        % T.Properties.VariableNames = { ...
            % 'Layer' ...
            % 'dz' ...
            % 'CumDepth' ...
            % 'DepWeight_KT200' ...
            % 'temp' ...
            % 'temp_x_DepthWeight_KT200'};
        % filename = ['/data/project4/gregp/tools_matlab/applications/pteropods/check_depwt_coast_i700j570_v08.xls'];
        % writetable(T,filename,'Sheet',1,'Range','A1');

% % nearshore KB5
% i=700;
% j=660;
% col1=transpose(1:1:60);
% col2=dz(:,i,j);
% col3=CumHeight(:,i,j);
% col4=DepthWeight_KB5(:,i,j);
% col5=temp_dataout(:,i,j);
% col6=DepthWeight_KB5(:,i,j).*temp_dataout(:,i,j);
        % clear T
        % T=table( ...
            % col1, ...
            % col2, ...
            % col3, ...
            % col4, ...
            % col5, ...
            % col6);
        % T.Properties.VariableNames = { ...
            % 'Layer' ...
            % 'dz' ...
            % 'CumHeight' ...
            % 'DepWeight_KB5' ...
            % 'temp' ...
            % 'temp_x_DepthWeight_KB5'};
        % filename = ['/data/project4/gregp/tools_matlab/applications/pteropods/check_depwt_nearshore_KB5_i700j660_v08.xls'];
        % writetable(T,filename,'Sheet',1,'Range','A1');



   cpt = cpt+1 ;

end % fr

disp(['2D Omega aragonite program ends .... on:  ',  datestr(now)])

%figure
%pcolor(lon,lat,squeeze(OW(:,:,1))) ; shading flat ; colorbar

