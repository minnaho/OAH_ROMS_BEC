%% ============================================================ 
%% program to extract a 3D file var(x,y,t), 			
%% 2D maps of the seafloor in ROMS of metabolic index parameteres
%% 						                
%% Program by Greg Pelletier and Minna Ho - SCCWRP                     
%% 07/2021              				        
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
param_bottom_mi

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
   %thickness-weighted average
   rho_KB5 = Fx_var_KBDD_v02(dens,DepthWeight_KB5);   

   dataout  = ncread(file, 'temp') ;
   dataout = permute(dataout, [3 2 1]);
   temp = squeeze(dataout(:,:,:)) ;
   %thickness-weighted average 
   temp_KB5 = Fx_var_KBDD_v02(temp,DepthWeight_KB5);   

   dataout  = ncread(file, 'O2') ;
   dataout = permute(dataout, [3 2 1]);
   o2 = squeeze(dataout(:,:,:)) ;
   o2 = (o2./(dens.*0.001)) ;   % mmol m-3
   %thickness-weighted average
   o2_KB5 = Fx_var_KBDD_v02(o2,DepthWeight_KB5);   


rho_KB5(rho_KB5==0)=NaN;
temp_KB5(temp_KB5==0)=NaN;
o2_KB5(o2_KB5==0)=NaN;

rho_KB5(mask==0)=NaN; 
temp_KB5(mask==0)=NaN; 
o2_KB5(mask==0)=NaN; 

% write nc
ncwrite(fout1_tem, 'var', temp_KB5' , [1 1 cpt]);
ncwrite(fout1_doo, 'var', o2_KB5' , [1 1 cpt]);
ncwrite(fout1_rho, 'var', rho_KB5' , [1 1 cpt]);

cpt = cpt+1 ;
end % fr


disp(['seafloor extraction ends on: ',datestr(now)])

