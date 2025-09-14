clear all

grdfile = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_grd.nc' ; 
rivfile = '/data/project8/pdamien/ROMS_outputs/PACMED25KMnew/FORCINGS/pacmed25_riv.nc' ;

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

% 1=temp, 2=salt, 3=po4, 4=no3, 5=Sio3, 6=nh4, 7=Fe, 8=O2, 9=Dic, 10=Alk, 11=doc, 12=don, 13=dofe, 14=dop, 15=dopr, 16=donr, 17=zooc, 18=spc, 19=spchl, 20=spfe, 21=spcaco3, 22=diatc, 23=diatchl, 24=diatfe, 25=diatsi, 26=diazc, 27=diachl, 28=diazfe, 29= no2, 30=n2, 31=n2o

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

RIVER = river_tracer ;
eps = 1e-4 ;

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
CHL = 2.0 ; %CHL
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


ncwrite(rivfile,'river_tracer',RIVER) ;




