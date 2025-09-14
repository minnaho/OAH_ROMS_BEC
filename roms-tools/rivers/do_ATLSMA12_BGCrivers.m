clear all

grdfile = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_grd.nc' ; 
rivfile = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_riv.nc' ;

%%% Verif riv location 
if 0 
flx = ncread(grdfile,'river_flux') ; 
flx(flx==0)=NaN ; 
figure ; pcolor(flx) ; shading flat ; colormap(jet) ; colorbar ; 
max(flx(~isnan(flx)))
min(flx(~isnan(flx)))
end

river_time = ncread(rivfile,'river_time') ; 
river_tracer = ncread(rivfile,'river_tracer') ;
river_volume = ncread(rivfile,'river_volume') ;

RIVER = river_tracer ;
eps = 1e-4 ;

%%%%%%%%%%%%%%%%% BEC TRACERS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 1=temp, 2=salt, 3=po4, 4=no3, 5=Sio3, 6=nh4, 7=Fe, 8=O2, 9=Dic, 10=Alk, 11=doc, 12=don, 13=dofe, 14=dop, 15=dopr, 16=donr, 17=zooc, 18=spc, 19=spchl, 20=spfe, 21=spcaco3, 22=diatc, 23=diatchl, 24=diatfe, 25=diatsi, 26=diazc, 27=diachl, 28=diazfe, 29= no2, 30=n2, 31=n2o

%%%%%%% STEP 1 : START WITH GLOBAL VALUES based on litterature, then update   %%%%%%%%%%%%%%%%%

%% CHOICE make a global mean value : 
%% https://ei.lehigh.edu/envirosci/watershed/wq/wqbackground/
%% - NH4 : 0.5 mg/L = 0.028 mmol/m3
%% - O2 :   6  mg/L = 187.5 mmol/m3
%% - NO3 : 3.0 mg/L = 48.4 mmol/m3, 1.5mg/L = 24.2 mmol/m3
%% - Alk : (20-200 mg/L), 150 mg/L = 2459 mmol/m3
%% - ph : 7.1 
%% - PO4 : 8 mg/L = 0.0842 mmol/m3
%% - DIC : 

%% - for DIN, mean value from Lee et al. 2019, supplementary material table 2 
%%              mean volume flux = 14557 m3/s 
%%              mean N load      = 134.6 kt/yr
%%                           -> 0.293 g/m3 = 16.25 mmol/m3

%% - for Iron : 0.1mg/l Ref : Yan for chinese rivers = 1.79 mmol/m3

%% - silicate : 1 - 100 mg/L : https://www.freedrinkingwater.com/water_quality/quality2/j-24-typical-concentrations-for-silicates-ground-n-surface-waters-page2.htm , 10 mg/L = 65.7 mmol/m3, 2mg/L = 13.14 mmol/m3

%%%% Put mean value 
RIVER(:,1,:) = 16.0     ; % temperature
RIVER(:,2,:) = 1.0      ; % salinity
RIVER(:,3,:) = 2.7      ; % po4
RIVER(:,4,:) = 24.2     ; % no3
RIVER(:,5,:) = 13.2     ; % SiO3 
RIVER(:,6,:) = 2.2      ; % Nh4
RIVER(:,7,:) = 1.79     ; % Fe
RIVER(:,8,:) = 187.5    ; % O2
RIVER(:,9,:) =  2370    ; % dic
RIVER(:,10,:) = 2310    ; % alk

% SCALED VARIABLES :
CHL = 1.0 ; %CHL
RIVER(:,11,:) = eps ; %DOC
RIVER(:,12,:) = 1.0 ;  
RIVER(:,13,:) = 0.0001 ; 
RIVER(:,14,:) = 0.1 ; 
RIVER(:,15,:) = 0.003 ;  
RIVER(:,16,:) = 0.8 ;
RIVER(:,17,:) = 1.35*CHL ; 
RIVER(:,18,:) = 3.375*CHL ; 
RIVER(:,19,:) = 0.675*CHL ;
RIVER(:,20,:) = 1.35e-5*CHL ; 
RIVER(:,21,:) = 0.0675*CHL ; 
RIVER(:,22,:) = 0.2025*CHL ;
RIVER(:,23,:) = 0.0675*CHL ; 
RIVER(:,24,:) = 1.35e-6*CHL ; 
RIVER(:,25,:) = 0.0675*CHL ;
RIVER(:,26,:) = 0.0375*CHL ; 
RIVER(:,27,:) = 0.0075*CHL ;  
RIVER(:,28,:) = 7.5e-7*CHL ;
RIVER(:,29,:) = 0.28 ; %NO2
RIVER(:,30,:) = eps ; %N2
RIVER(:,31,:) = 0.01 ; %N2O

%%%%%%%%%%%% Southern American Tropical river %%%%%%%%%%%%%%%%%%%%
   %  Amazon orinoco Tocantins Tapajos Xingu Magdalena atrato Essequibo Sao-Francisco Usumacinta
index = [  1       3         6       7     9        10     12        15            17         18 ...
         19         27       32         34      35] ; 
   % Maroni Courantyne Jamanxim Santa-Cruz Oyapoch
% Drake et al 2021, puse of the Amazon; luxes of DOC, N fron the worlds lagest river
RIVER(index,3,:) = 0.4      ; % po4
RIVER(index,4,:) = 7.4      ; % no3
RIVER(index,5,:) = 65.8     ; % SiO3 
RIVER(index,6,:) = 1.48     ; % Nh4
RIVER(index,8,:) = 145.0    ; % O2
%RIVER(index,11,:) = 76.0    ; % DOC (all bio is in the form of CHL derived, it (should!!) equilibrates quickly)
%RIVER(index,12,:) = 8.0     ; % DON
% Benedetti 2003, Carbon and metal concentration fuxes in major rivers in the amazon
RIVER(index,7,:) = 0.45     ; % Fe

%%%%%%%%%%%% African river %%%%%%%%%%%%%%%%%%%%
   % Congo Niger Ogooue Sanaga Eboniyi Volta
index = [2    13     14     16      23    38];
% Descy 2017 Phytoplankton dynamic inthe congo river 
% Spencer 2016 Origins seasonality of fluxes in the Congo river
RIVER(index,3,:) =   1.8    ; % po4
RIVER(index,4,:) =  20.0    ; % no3
RIVER(index,5,:) = 132.0    ; % SiO3
%RIVER(index,11,:) = 125.0   ; % DOC (all bio is in the form of CHL derived, it (should!!) equilibrates quickly)
%RIVER(index,12,:) = 12.5    ; % DON
% Viera 2020 unprecedented Fe delivery from Cong River
RIVER(index,7,:) = 1.4     ; % Fe

%%%%%%%%%%%% Mississipi river %%%%%%%%%%%%%%%%%%%%
   % Mississippi Alabama 
index =[       4      30] ;
% Pellerin 2014 Mississipi river nitrate load from measurement 
% Turner 2024 Water qualitey at the end of the Mississipi river
% Bussan 2017 Concentratiosn of selected dissolved trace element and anthorpogenic organic ...
% Turner et al. 2023 Total ammonia and coliform concentratiosn at the en do
RIVER(index,4,:) =  24.2    ; % no3
RIVER(index,3,:) =   8.0    ; % po4
RIVER(index,5,:) = 110.0    ; % SiO3
RIVER(index,7,:) =   0.4    ; % Fe
RIVER(index,6,:) =   3.2    ; % Nh4

%%%%%%%%%%%% Southern Amercian ARG-URU river %%%%%%%%%%%%%%%%%%%%
   % Parana Uruguay Jacui
index = [ 5      11    22];
% Primost 2022 Nutrient dynamics in the Parana river delta
% Lucas 2022 Nutrients levels, trophic status and land use influence on ...
RIVER(index,1,:) =  19.0    ; % Temp
RIVER(index,4,:) =   3.3    ; % no3
RIVER(index,6,:) =   2.2    ; % Nh4
RIVER(index,8,:) = 250.0    ; % O2

%%%%%%%%%%%% Northern Amercian Canada river %%%%%%%%%%%%%%%%%%%%
   % Saint-Lawrence Caniapiscau Albany La-Grande Ottawa Saguenay Eastmain Susquehanna
index = [         8          21     24        25     26       29       31          33 ...
         36       37  40];
   % George Nottaway Red
% Nutrients in the Saint Lawrence river, Canadian Environmental sustainability indicators 2021
% Jutras 2020 nutrient cycling in the lower st lawrence estuary , response to evironemental perturbations
% Cossa 1990 seasonality in the iron and manganese concentration of the Saint Lawrence
RIVER(index,1,:) =  12.0    ; % Temp
RIVER(index,4,:) =  16.2    ; % no3
RIVER(index,3,:) =   1.8    ; % po4
RIVER(index,5,:) =  25.0    ; % SiO3
RIVER(index,8,:) = 305.0    ; % O2
RIVER(index,7,:) =   1.4    ; % Fe

%%%%%%%%%%%% Rhine river %%%%%%%%%%%%%%%%%%%%
index = 20 ;
% The Rhine annual report 2020 Dr G.J. Stroomberg RIWA RIJN
% report 1996 water quality of large river Peter Kristensen
RIVER(index,1,:) =  13.5    ; % Temp
RIVER(index,4,:) =  64.5    ; % no3
RIVER(index,3,:) =   2.1    ; % po4
RIVER(index,5,:) =  31.6    ; % SiO3
RIVER(index,8,:) = 290.6    ; % O2
RIVER(index,7,:) =   9.8    ; % Fe
RIVER(index,6,:) =   4.4    ; % Nh4

%%%%%%%%%%%% Rhone river %%%%%%%%%%%%%%%%%%%%
index = 28 ;
% Moose Netweork Website
% Peter Kristensen 1996 
RIVER(index,1,:) =  14.0    ; % Temp
RIVER(index,4,:) =  69.5    ; % no3
RIVER(index,3,:) =   1.8    ; % po4
RIVER(index,5,:) =  75.0    ; % SiO3
RIVER(index,7,:) =   0.5    ; % Fe
RIVER(index,6,:) =   3.0    ; % Nh4

%%%%%%%%%%%% Garonne river %%%%%%%%%%%%%%%%%%%%
index = 39 ;
% Peter Kristensen 1996 report
% Muylaert 2009 Eutrophication and its effect on Si concentrations in Garonne
RIVER(index,1,:) =  17.0    ; % Temp
RIVER(index,4,:) =  35.5    ; % no3
RIVER(index,3,:) =   1.0    ; % po4
RIVER(index,5,:) =  83.3    ; % SiO3
RIVER(index,6,:) =  22.1    ; % Nh4


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ncwrite(rivfile,'river_tracer',RIVER) ;




