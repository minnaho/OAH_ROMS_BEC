%==========================================================
%  make point source forcing file for The Southern 
%  California Bight on L2 grid (300m)
% 			First program written for 
% 			Japanese Point source by
%                           7-01-2011 Yusuke Uchiyama
%     05-01-2018 Revised for SCB (california) 
%      by Faycal Kessouri (SCCWRP/UCLA kesf@atmos.ucla.edu)
%===========================================================
% The resulting ncfile  files will contains 
% data for >100 point sources and ~20 biogeochemical variables
% with qshape applied on 60 levels
% 6 time series of 12 point sources
% 145 steps = 145 qbar
% 
% What I need:
% the oly difference is the time series of concentration for each variables
% 
%===================================================================
%
% Create an empty netcdf point source file
%
%    Inputs
%     frcname:    name of the psource file
%     psvars:     variable names of passive tracers (include T and S)
%     psname:     netcdf longnames of passive tracers
%     psunit:     unit of passive tracers
%     Nsrc:       number of point source locations
%     N:          number of vertical s-layers
%     psrc_title: title in the netcdf file
%     psrc_time:  1D time array
%     psrc_cycle: cycle length
%
% Built on the Pierrick Penven's ROMS tools
%                         Yusuke Uchiyama, Kobe Univ., 6-17-2011
%                      modified to include sediments, 10-15-2013
%                      
%       modified for new matlab version and add biogeochemical tracers
%       Faycal Kessouri, SCCWRP/UCLA, Los Angeles, 04/24/2018
%
%===================================================================

clear all;
close all;
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/BGCtools/'))
addpath('/data/project3/kesf/tools_roms/B2B/packages')

psrc_title='point source for the southern California Bight L2 300-m grid';
%psrc_fname='roms_psource_V2.nc';
psrc_fname='roms_psource_102020_R4.nc';

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc';
load_grid_L2_SCB
% max monthly-mean discharge of Abukuma River is 212.2469 m3/s.
% qave=40;	% m3/s.  ==> crudely assumed that discharge from minor rivers
%       		%            is about 1/5 of the peak discharge from Abukuma.

% number of passive tracers (must be >= 2, including T and S)
%Npas=36; % all tracers		% 4: T, S, sand, silt
% from a random file
par_file = '/data/project6/kesf/ROMS/USSW1/daily/ussw1_avg.Y2000M01D01.nc'
[varnames_bgc,longnames_bgc,units_bgc,varnames_bgc_or] = det_bgc_tracers(par_file);
varnames_bgc = ['temp','salt',varnames_bgc] ;
varnames_bgc = varnames_bgc([1 2 3 4 5 6 7 8 9 10 11 24 26 27]); % 'temp'    'salt'    'PO4'    'NO3'  'SiO3'   'NH4'    'Fe'    'Alk'    'DOC'    'DON'    'DOP'    'NO2'
longnames_bgc = ['Temperature at the point source','Salinity at the point source',longnames_bgc];
longnames_bgc = longnames_bgc([1 2 3 4 5 6 7 8 9 10 11 24 26 27]);% 'temp'    'salt'    'PO4'    'NO3'  'SiO3'  'NH4'   'Fe'    'Alk'    'DOC'    'DON'    'DOP'    'NO2'

Npas=length(varnames_bgc) ; % all BGC tracers + T and S     % 4: T, S, sand, silt
psvars = varnames_bgc ;
psname = longnames_bgc ;
units_bgc=['Degrees Celcius','psu',units_bgc] ;
psunit=units_bgc([1 2 3 4 5 6 8 9 7 10 11 24 26 27]) ;

%%%%%%%%%%%%%%
%% POTW MAJORS
%%%%%%%%%%%%%%
disp('MAJOR POTW ... ')
%% DEFINE THE TIME
%repmajor = '/data/project1/minnaho/potw_outfall_data/run_1997_2000/major_potw_data_newocsd.nc';
repmajor = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/major_potw_data/major_potw_1971_2017_monthly.nc';
ptime = double(ncread(repmajor,'time')+datenum(1971,1,1)); %
time = ptime  - datenum(1994,1,1) ;
time_t = find(time>=0);
test_t = find(ptime>=datenum(1997,1,1)) ; datestart = test_t(1) ;
%test_t = test_t(1:233);
psrc_time = time(test_t) ;
sz_psrc_time = size(psrc_time,1) ;
lend = datestart+sz_psrc_time-1;

% test: tutu = psrc_time/86400 + datenum(1994,1,1)
% datestr(time(289)/86400 + datenum(1994,1,1) ) = 02-Jan-1994
pflow = ncread(repmajor,'flow'); % m3/s
pNO3 = ncread(repmajor,'NO3'); %
pNH4 = ncread(repmajor,'NH4');
pNO2 = ncread(repmajor,'NO2');
pPO4 = ncread(repmajor,'PO4');
pFe = ncread(repmajor,'dissolved_Fe');
%pSO2 = ncread(repmajor,'SO2');
palkalinity = ncread(repmajor,'alkalinity');
ppH = ncread(repmajor,'pH');
psilicate = ncread(repmajor,'SiO4');
pBOD = ncread(repmajor,'BOD');
pTOC = ncread(repmajor,'total_organic_C');
pON = ncread(repmajor,'organic_N');
pOP = ncread(repmajor,'organic_P');
pO2 = ncread(repmajor,'dissolved_oxygen');
psalt = ncread(repmajor,'salinity');
ptemp = ncread(repmajor,'temperature');

dodic=1;
for i=1:4 % (POTWs)
	flow(:,i) = squeeze(pflow(i,datestart:lend)) ; % m3/s
	nitrate(:,i) = squeeze(pNO3(i,datestart:lend)) ; % mmol/m3
	ammonium(:,i) = squeeze(pNH4(i,datestart:lend)) ;% mmol/m3
	nitrite(:,i) = squeeze(pNO2(i,datestart:lend)) ;% mmol/m3
	phosphate(:,i) = squeeze(pPO4(i,datestart:lend)) ;% mmol/m3
	iron(:,i) = squeeze(pFe(i,datestart:lend)) ;% mmol/m3
%	sulfuredioxyde(:,i) = squeeze(pSO2(i,i,datestart:end)) ;% mmol/m3
	alkalinity(:,i) = squeeze(palkalinity(i,datestart:lend)) ;% mmol/m3
	ph(:,i) = squeeze(ppH(i,datestart:lend)) ;
	silicate(:,i) = squeeze(psilicate(i,datestart:lend)) ;% mmol/m3
	bod(:,i) = squeeze(pBOD(i,datestart:lend)) ;% mmol/m3
	toc(:,i) = squeeze(pTOC(i,datestart:lend)) ;% mmol/m3
	on(:,i) = squeeze(pON(i,datestart:lend)) ;% mmol/m3
	op(:,i) = squeeze(pOP(i,datestart:lend)) ;% mmol/m3
        sal(:,i) = squeeze(psalt(i,datestart:lend)) ;% mmol/m3
        o2(:,i) = squeeze(pO2(i,datestart:lend)) ;% mmol/m3
        tem(:,i) = squeeze(ptemp(i,datestart:lend)) ;% mmol/m3

if dodic
%% estimation of omega omegainite using the full carbon system (alkanility)
PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = 33 ;
%temp = 28 ;
sio3 = 20 ;

if i==1
phh = 7;
elseif i==2
phh=7.7;
elseif i==3
phh=7.6;
elseif i==4
phh=7.5;
end
clear DATA
sill = silicate(:,i);
sill(sill>400)=400;

[DATA,HEADERS,NICEHEADERS]=CO2SYS(alkalinity(:,i),phh,1,3,...
    saltt,tem(:,i),nan,...
    0,nan,...
    sill,phosphate(:,i),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
dic(:,i) = DATA(:,2) ;% mmol/m3
end % dodic
end % (i = POTWs)

% FLOWS : FOR 4 OUTFALLS WITH (8 MAJOR DIFFUSERS SURROUNDED BY 63 MINOR DIFFUSERS)

%%%%%% -------------------
%%%%%% |  5% |  5% |  5% |
%%%%%% -------------------
%%%%%% |  5% | 60% |  5% |
%%%%%% -------------------
%%%%%% |  5% |  5% |  5% |
%%%%%% -------------------
        
% HTP : 1 --> 20 (2 MAJORS) 
Qbar(:,1) = flow(:,1 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,2) = flow(:,1 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,3) = flow(:,1 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,18) = flow(:,1).*(5/28) ; % HTP Small flow around the main diffusers

Qbar(:,7) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,9) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,4) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,6) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,19) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,23) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers

Qbar(:,5) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,8) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,10) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,20) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,21) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,22) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers


Qbar(:,24) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,27) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,15) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,17) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,14) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,12) = flow(:,1).*((1/2)/28) ; % HTP Small flow around the main diffusers

Qbar(:,26) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,28) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,25) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,11) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,16) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,13) = flow(:,1).*((1/6)/28) ; % HTP Small flow around the main diffusers



% JWPCP : 21 --> 44 (3 MAJORS: 1S AND 2N)
Qbar(:,29) = flow(:,2 ).*.65.*(5/14) ; % HTP Small flow around the main diffusers
Qbar(:,30) = flow(:,2 ).*.65.*(5/14) ; % HTP Small flow around the main diffusers
Qbar(:,31) = flow(:,2 ).*.175.*(5/14) ; % HTP Small flow around the main diffusers
Qbar(:,51) = flow(:,2).*.175.*(5/14) ; % HTP Small flow around the main diffusers

Qbar(:,35) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,33) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,38) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,40) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,39) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,42) = flow(:,2).*.65.*((1/2)/14) ; % HTP Small flow around the main diffusers

Qbar(:,34) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,36) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,32) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,37) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,43) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,41) = flow(:,2).*.65.*((1/6)/14) ; % HTP Small flow around the main diffusers


Qbar(:,52) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,55) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,48) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,50) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,47) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,45) = flow(:,2).*.175.*((1/2)/14) ; % HTP Small flow around the main diffusers

Qbar(:,44) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,49) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,46) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,56) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,54) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,53) = flow(:,2).*.175.*((1/6)/14) ; % HTP Small flow around the main diffusers



% OCSD : 45 --> 53 (1 MAJOR)

Qbar(:,57) = flow(:,3 ).*(5/14) ; % HTP Small flow around the main diffusers
Qbar(:,63) = flow(:,3 ).*(5/14) ; % HTP Small flow around the main diffusers

Qbar(:,61) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,66) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,64) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,67) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,62) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers
Qbar(:,59) = flow(:,3).*((1/2)/14) ; % HTP Small flow around the main diffusers

Qbar(:,60) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,65) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,58) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,70) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,69) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers
Qbar(:,68) = flow(:,3).*((1/6)/14) ; % HTP Small flow around the main diffusers


% PLWTP : 54 --> 71 (2 MAJORS)

Qbar(:,71) = flow(:,4 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,73) = flow(:,4 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,72) = flow(:,4 ).*(5/28) ; % HTP Small flow around the main diffusers
Qbar(:,88) = flow(:,4).*(5/28) ; % HTP Small flow around the main diffusers

Qbar(:,77) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,79) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,74) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,76) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,89) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,93) = flow(:,4).*(((1/2)+(1/6))/28) ; % HTP Small flow around the main diffusers

Qbar(:,75) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,78) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,80) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
%Qbar(:,90) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,90) = flow(:,4).*(((1/2)+(1/6))/28) ; % HTP Small flow around the main diffusers
Qbar(:,91) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,92) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers

Qbar(:,84) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,82) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,87) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,85) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
Qbar(:,96) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers
%Qbar(:,90) = flow(:,4).*((1/2)/28) ; % HTP Small flow around the main diffusers

Qbar(:,81) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,86) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,83) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,94) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
Qbar(:,95) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers
%Qbar(:,93) = flow(:,4).*((1/6)/28) ; % HTP Small flow around the main diffusers




%% TRACERS: reprete the same concentration by OUTFALL
%% HTP
for i = 1:28
        db(1,i) = 42 ; % above the bottom in meters (Uchiyama et al 2014)
	NO3(:,i) = nitrate(:,1);
	NH4(:,i) = ammonium(:,1);
	NO2(:,i) = nitrite(:,1);
	PO4(:,i) = phosphate(:,1);
	Fe(:,i) = iron (:,1);
%	SO2 = sulfuredioxyde(:,1);
	Alk(:,i) = alkalinity(:,1);
	PH(:,i) = ph(:,1);
	SIO4(:,i) = silicate(:,1);
%	BOD (:,1);
	DIC(:,i) = dic(:,1);
	DOC(:,i) = toc(:,1);
	DON(:,i) = on  (:,1);
	DOP(:,i) = op (:,1);
%        O2(:,i) = 0.*NO3(:,i) + 125 ;
        O2(:,i) = o2(:,1)  ;
	salt(:,i) = sal(:,1)  ;
        temp(:,i) = tem(:,1)  ;
end
%% JWPCP
for i= 29:56
        db(1,i) = 50 ; % above the bottom in meters (McLaughlin et al in prep)
        NO3(:,i) = nitrate(:,2);
        NH4(:,i) = ammonium(:,2);
        NO2(:,i) = nitrite(:,2);
        PO4(:,i) = phosphate(:,2);
        Fe(:,i) = iron (:,2);
%       SO2 = sulfuredioxyde(:,1);
        Alk(:,i) = alkalinity(:,2);
        PH(:,i) = ph(:,2);
        SIO4(:,i) = silicate(:,2);
%       BOD (:,1);
        DIC(:,i) = dic(:,2);
        DOC(:,i) = toc(:,2);
        DON(:,i) = on  (:,2);
        DOP(:,i) = op (:,2);
%        O2(:,i) = 0.*NO3(:,i) + 125 ;
        O2(:,i) = o2(:,2)  ;
        salt(:,i) = sal(:,2)  ;
        temp(:,i) = tem(:,2)  ;
end
%% OCSD
for i=57:70
	db(1,i) = 50 ;  % above the bottom in meters (McLaughlin et al in prep)
        NO3(:,i) = nitrate(:,3);
        NH4(:,i) = ammonium(:,3);
        NO2(:,i) = nitrite(:,3);
        PO4(:,i) = phosphate(:,3);
        Fe(:,i) = iron (:,3);
%       SO2 = sulfuredioxyde(:,3);
        Alk(:,i) = alkalinity(:,3);
        PH(:,i) = ph(:,3);
        SIO4(:,i) = silicate(:,3);
%       BOD (:,3);
        DIC(:,i) = dic(:,3);
        DOC(:,i) = toc(:,3);
        DON(:,i) = on  (:,3);
        DOP(:,i) = op (:,3);
%        O2(:,i) = 0.*NO3(:,i) + 125 ;
        O2(:,i) = o2(:,3)  ;
        salt(:,i) = sal(:,3)  ;
        temp(:,i) = tem(:,3)  ;
end
%% PLWTP
for i=71:96
	db(1,i) = 65 ;% above the bottom in meters
        NO3(:,i) = nitrate(:,4);
        NH4(:,i) = ammonium(:,4);
        NO2(:,i) = nitrite(:,4);
        PO4(:,i) = phosphate(:,4);
        Fe(:,i) = iron (:,4);
%       SO2 = sulfuredioxyde(:,4);
        Alk(:,i) = alkalinity(:,4);
        PH(:,i) = ph(:,4);
        SIO4(:,i) = silicate(:,4);
%       BOD (:,4);
        DIC(:,i) = dic(:,4);
        DOC(:,i) = toc(:,4);
        DON(:,i) = on  (:,4);
        DOP(:,i) = op (:,4);
%        O2(:,i) = 0.*NO3(:,i) + 125 ;
        O2(:,i) = o2(:,4)  ;
        salt(:,i) = sal(:,4)  ;
        temp(:,i) = tem(:,4)  ;
end
 

%%%%%%%%%%%
%% Isrc &
%% Jsrc
%%%%%%%%%%

%find_IJsrc_outfalls
%Jszbot1rc(19)=Jsrc(19)-1;
find_IJsrc_outfallsV12

%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% mimiking the buyancy flux of the seawage coming from the outfalls
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
z_r = (ztop1 + zbot1)./2;
cff=0;

%% METHODOLOGY 1
%% calculate the qshape
%for i=1:size(Isrc,2) % by diffuser
%DB = db(1,i) ;
%DB = 25;
%        for k=1:NZ % vertical levels
%        Zcff=max(2.,h(Isrc(i),Jsrc(i))-DB) ;

%if i<=28
%Zcff = 45 ;
%elseif (i>=21 & i<=44)
%Zcff = 45 ;
%elseif (i>=45 & i<=53)
%Zcff = 45 ;
%elseif (i>=54 & i<71)
%Zcff = 65 ;
%end

%        Zcff_disp(i) = Zcff ;
%       disp([num2str(Zcff) , '  - ' , num2str(i)])
%        Scff=0.02;    % 0.15 ;
%        Xcff = abs(z_r(Jsrc(i),Isrc(i),k) - Zcff) ;
%        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
%        end
%        Qshape(:,i) = Qs./sum(Qs) ;
%end


%% METHODOLOGY 2
%% calculate the qshape
for i=1:size(Isrc,2) % by diffuser
%DB = db(1,i) ;
Zcff = db(1,i) ;
        for k=1:NZ % vertical levels
%        Zcff=max(2.,h(Jsrc(i),Isrc(i))-DB) ;
%        Zcff_disp(i) = DB ;
        Scff=0.02 ;
%        Xcff = abs(z_r(Jsrc(i),Isrc(i),k) - Zcff) ;
        Xcff =-abs(z_r(Jsrc(i),Isrc(i),k)) + Zcff ;
%        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
        end
        Qshape(:,i) = Qs./sum(Qs) ;
end


%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;

%% Dsrc
Dsrc1 = ones(psNOW,1) .* 2 ;

%======================================================
%======================================================
%% PART 2
disp('Minor POTW ... ')
repminor = '/data/project1/minnaho/potw_outfall_data/updated_2013_2017/minor_potw_data/minor_potw_1997_2017_monthly.nc';
%% time
ptime = double(ncread(repminor,'time')+datenum(1997,1,1)); %
time = ptime  - datenum(1994,1,1) ;
time_t = find(time>=0);
test_t = find(ptime>=datenum(1997,1,1)) ; datestart = test_t(1) ;
%test_t = test_t(1:233);
psrc_time = time(test_t) ;
sz_psrc_time = size(psrc_time,1) ;
dateend = datestart+sz_psrc_time-1;

%% variables
pflow = ncread(repminor,'flow'); % m3/s
pNO3 = ncread(repminor,'NO3'); %
pNH4 = ncread(repminor,'NH4'); %
pNO2 = ncread(repminor,'NO2'); %
pPO4 = ncread(repminor,'PO4'); %
palkalinity = ncread(repminor,'alkalinity'); %
pph = ncread(repminor,'pH'); %
ptoc =  ncread(repminor,'total_organic_C'); %
ptemp =  ncread(repminor,'temperature'); %
psilicate =  ncread(repminor,'SiO4'); %
pON = ncread(repminor,'organic_N');
pOP = ncread(repminor,'organic_P');
pFe =  ncread(repminor,'dissolved_Fe'); %

%% IMPRTANT : TEST THE NUMBER OF POINT SOURCES
num= size(pflow,1) ;
clear flow nitrate ammonium nitrite phosphate alkalinity ph toc tem silicate pon pop
for i=1:num % (POTWs)
        flow(:,i) = squeeze(pflow(i,test_t)) ; % m3/s
        nitrate(:,i) = squeeze(pNO3(i,test_t)) ; % mmol/m3
        ammonium(:,i) = squeeze(pNH4(i,test_t)) ;% mmol/m3
        nitrite(:,i) = squeeze(pNO2(i,test_t)) ;% mmol/m3
        phosphate(:,i) = squeeze(pPO4(i,test_t)) ;% mmol/m3
        alkalinity(:,i) = squeeze(palkalinity(i,test_t)) ;% mmol/m3
        ph(:,i) = squeeze(pph(i,test_t)) ;% mmol/m3
        toc(:,i) = squeeze(ptoc(i,test_t)) ;% mmol/m3
        tem(:,i) = squeeze(ptemp(i,test_t)) ;% C
        iron(:,i) = squeeze(pFe(i,test_t)) ;% C
        silicate(:,i) = squeeze(psilicate(i,test_t)) ;% mmol/m3
        pon(:,i) = squeeze(pON(i,test_t)) ;% mmol/m3
        pop(:,i) = squeeze(pOP(i,test_t)) ;% mmol/m3
end

%% start from the end of MAJOR POTWS
for i=psNOW+1:psNOW+num
	Qbar(datestart:dateend,i) = flow(:,i-psNOW);
        NO3(datestart:dateend,i) = nitrate(:,i-psNOW);
        NH4(datestart:dateend,i) = ammonium(:,i-psNOW);
        NO2(datestart:dateend,i) = nitrite(:,i-psNOW);
        PO4(datestart:dateend,i) = phosphate(:,i-psNOW);
	
	Fe(datestart:dateend,i) = iron(:,i-psNOW);
        Alk(datestart:dateend,i) = alkalinity(:,i-psNOW);
	PH(datestart:dateend,i) = ph(:,i-psNOW);
        DOC(datestart:dateend,i) = toc(:,i-psNOW);
%        DON(datestart:dateend,i) = 0.137.*toc(:,i-psNOW);
%        DOP(datestart:dateend,i) = 0.0625.*toc(:,i-psNOW);
	O2(datestart:dateend,i) = 0.*flow(:,i-psNOW)+(5.6/16*1000);
        salt(datestart:dateend,i) = 0.*flow(:,i-psNOW) + 1 ;
        temp(datestart:dateend,i) = tem(:,i-psNOW) ;
        SIO4(datestart:dateend,i) = silicate(:,i-psNOW) ;
        DON(datestart:dateend,i) = pon(:,i-psNOW) ;
        DOP(datestart:dateend,i) = pop(:,i-psNOW) ;

PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = salt(datestart:dateend,i) ; % 13 ;
ttemp = temp(datestart:dateend,i) ; % 28 ;
ssio3 = SIO4(datestart:dateend,i) ; % 20 ;
phh = 7.5 ;
ppo4 = PO4(datestart:dateend,i) ;
aalk=Alk(datestart:dateend,i) ;

clear DATA
[DATA,HEADERS,NICEHEADERS]=CO2SYS(aalk,phh,1,3,...
    saltt,ttemp,nan,...
    0,nan,...
    ssio3,ppo4,...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DIC(datestart:dateend,i) = DATA(:,2) ;% mmol/m3

end

[DATA,HEADERS,NICEHEADERS]=CO2SYS(100,phh,1,3,...
    saltt,ttemp,nan,...
    0,nan,...
    40,9,...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);

%%%%%%%%%%%%%%%
%% Isrc Jsrc %%
%%%%%%%%%%%%%%%
% find the location of I and J
%lon_minor_potw
%lat_minor_potw

lon_minor_potw_2020
lat_minor_potw_2020

x = ln_minpotw ;
y = lt_minpotw ;
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Isrc(psNOW+1:psNOW+num)  = mplat ;
Jsrc(psNOW+1:psNOW+num)  = mplon ;
%% Dsrc
Dsrc2 = ones(length(x),1) .* 2 ;
%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% mimiking the buyancy flux of the seawage coming from the outfalls
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
cff=0;
%% calculate the qshape
for i=psNOW+1:psNOW+num % by diffuser
DB = 10 ;
        for k=1:NZ % vertical levels
        Zcff=max(2.,h(Jsrc(i),Isrc(i))-DB) ;
        Scff=0.02 ;
%        Xcff = abs(z_r(Jsrc(i),Isrc(i),k) - Zcff) ;
        Xcff =-abs(z_r(Jsrc(i),Isrc(i),k)) + Zcff ;
        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
        end
        Qshape(:,i) = Qs./sum(Qs) ;
end

%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;


%% SMALL POTW END
%======================================================
%======================================================

%======================================================
%======================================================
%% PART 3 RIVERS
disp('RIVERS ... ')
reprivers = '/data/project1/minnaho/river_data/updated_2013_2017/rivers_1997_2017_monthly.nc';

%% time
ptime = double(ncread(reprivers,'time')+datenum(1997,1,1)); %
time = ptime  - datenum(1994,1,1) ;
time_t = find(time>=0);
test_t = find(ptime>=datenum(1997,1,1)) ; datestart = test_t(1) ;
%test_t = test_t(1:233);
psrc_time = time(test_t) ;
sz_psrc_time = size(psrc_time,1) ;
lend = datestart+sz_psrc_time-1;

% variables
pflow = ncread(reprivers,'flow'); % m3/s
pNO3 = ncread(reprivers,'NO3'); %
pNH4 = ncread(reprivers,'NH4'); %
pPO4 = ncread(reprivers,'PO4'); %
pTON = ncread(reprivers,'total_N'); %
pTOP = ncread(reprivers,'total_P'); %
palkalinity = ncread(reprivers,'alkalinity'); %
ptemp = ncread(reprivers,'temperature'); %
psalt = ncread(reprivers,'salinity'); %
psilicate =  ncread(reprivers,'SiO4'); %
pFe =  ncread(reprivers,'dissolved_Fe'); %

pDON = pTON - (pNH4+pNO3); pDON(pDON<0)=1e-10 ;
pDOP = pTOP - pPO4 ; pPO4(pPO4<0)=1e-10 ;

%% DEFINE THE TIME
%% IMPRTANT : TEST THE NUMBER OF POINT SOURCES
num= size(pflow,1) ;

clear flow nitrate ammonium phosphate don dop alkalinity Temp Salt
for i=1:num
        flow(:,i) = squeeze(pflow(i,test_t)) ; % m3/s
        nitrate(:,i) = squeeze(pNO3(i,test_t)) ; % mmol/m3
        ammonium(:,i) = squeeze(pNH4(i,test_t)) ;% mmol/m3
        phosphate(:,i) = squeeze(pPO4(i,test_t)) ;% mmol/m3
        don(:,i) = squeeze(pDON(i,test_t)) ;% mmol/m3
        dop(:,i) = squeeze(pDOP(i,test_t)) ;% mmol/m3
        alkalinity(:,i) = squeeze(palkalinity(i,test_t)) ;% mmol/m3
        Temp(:,i) = squeeze(ptemp(i,test_t)) ;% mmol/m3
	Salt(:,i) = squeeze(psalt(i,test_t)) ;% mmol/m3
        silicate(:,i) = squeeze(psilicate(i,test_t)) ;% mmol/m3
        iron(:,i) = squeeze(pFe(i,test_t)) ;% mmol/m3
end

%% start from the end of MAJOR POTWS
for i=psNOW+1:psNOW+num
%        db(1,i) = 20 ; % above the bottom in meters (Uchiyama et al 2014)
        Qbar(datestart:dateend,i) = flow(:,i-psNOW);
        NO3(datestart:dateend,i) = nitrate(:,i-psNOW);
        NH4(datestart:dateend,i) = ammonium(:,i-psNOW);
        PO4(datestart:dateend,i) = phosphate(:,i-psNOW);
        DON(datestart:dateend,i) = don (:,i-psNOW);
        DOP(datestart:dateend,i) = dop(:,i-psNOW);

        SIO4(datestart:dateend,i) = silicate(:,i-psNOW);
        Fe(datestart:dateend,i) = iron(:,i-psNOW);
        Alk(datestart:dateend,i) = alkalinity(:,i-psNOW);
        DOC(datestart:dateend,i) = (1/0.137).*don(:,i-psNOW);
	NO2(datestart:dateend,i) = 0.*flow(:,i-psNOW);
	O2(datestart:dateend,i) = 0.*flow(:,i-psNOW) + (7/16*1000) ;
        temp(datestart:dateend,i) = Temp(:,i-psNOW);
	salt(datestart:dateend,i) = Salt(:,i-psNOW) ;
PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = salt(datestart:dateend,i) ;
saltt(saltt<10)=10;
%temp = 28 ;
sio3 = 20 ;
phh = 7.5 ;
clear DATA
t = temp(datestart:dateend,i) ;
t(isnan(t) | t==0) = 26 ;

[DATA,HEADERS,NICEHEADERS]=CO2SYS(Alk(datestart:dateend,i),phh,1,3,...
    saltt,t,nan,...
    0,nan,...
    sio3,PO4(datestart:dateend,i),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DIC(datestart:dateend,i) = DATA(:,2) ;% mmol/m3
end


%%%%%%%%%%%%%%%
%% Isrc Jsrc %%
%%%%%%%%%%%%%%%
% find the location of I and J

river_i_water
river_j_water
% add +1 because the python program that generated the i and j location of the river starts with 0
%% adjust manually river refugio_creek cause it was on land
%Isrc(45+115) = Isrc(45+115)-2 ;

%riv_i_land;
%riv_j_land;
%Isrc(psNOW+1:psNOW+num) = ln_i+1-1 ;
%Jsrc(psNOW+1:psNOW+num) = ln_j+1 ;
%Isrc(45+115) = Isrc(45+115)-2 ;

Isrc(psNOW+1:psNOW+num) = riv_i+1 ;
Jsrc(psNOW+1:psNOW+num) = riv_j+1 ;

%% Dsrc
Dsrc3 = ones(length(riv_i),1) .* 2 ;
%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% distribution of the flux on the top layers
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
for i = psNOW+1:psNOW+num
	for k=1:NZ
	Zcff= z_r(Jsrc(i),Isrc(i),60) ;
	Scff=0.001 ;
%	Xcff = abs(z_r(Jsrc(i),Isrc(i),k) - Zcff) ;
        Xcff =-abs(z_r(Jsrc(i),Isrc(i),k)) + Zcff ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
	end
Qshape(:,i) = Qs./sum(Qs) ;
end

%% imprtant: test the size of the point psource and time scale
%[timeNOW psNOW] = size(Qbar) ;

%% ALL RIVERS END
disp('complete readin data')
%======================================================
%======================================================
%=========================
% DATA
%=========================
%% change the Dsrc
Qbar_scalar
DIRsrc = abs(DIRsrc) ;

readDsrc
RDsrc = (RDsrc.*0)+2 ;

Qbar(:,psNOW+1:psNOW+num) = Qbar(:,psNOW+1:psNOW+num).*repmat(DIRsrc,1,252)' ;
Dsrc(psNOW+1:psNOW+num) = RDsrc ;

%=========================
% Dsrc
%=========================
% 0 xi direction 1 rho direction 2 s directon
Dsrc = [Dsrc1 ; Dsrc2 ; RDsrc] ;
%for i=1:7
%Dsrc(182+i) = 2 ;
%end

%% spread cells of rivers San Gabriel and Los Angeles and move them in the ocean with Dsrc=2

add_ps_r_lariver4
add_ps_r_sangabriel4
add_ps_r_santamargarita

%%%%%%%%%%%
%% Nsrc
%%%%%%%%%%%
Nsrc = size(Qbar,2) ;
Tsrc = size(psrc_time,1) ;
%=========================
% Lsrc
%=========================
% 1 for true 0 for false
disp('Lsrc ...')
Lsrc = zeros(Npas,Nsrc) ;

%temp = ones(Tsrc , Nsrc).*28 ;
%salt = ones(Tsrc , Nsrc).*15 ;

%% fill the oxygen data to remove concentrations zeros and nans
O2(O2==0)=437.5;
O2(isnan(O2))=437.5;

clear DATA

        DATA(:,:,1)  = temp ;
        Lsrc(:,1) = 1 ;
        DATA(:,:,2)  = salt ;
        Lsrc(:,2) = 1 ;
        DATA(:,:,3)  = PO4 ;
        Lsrc(:,3) = 1 ;
        DATA(:,:,4)  = NO3 ;
        Lsrc(:,4) = 1 ;

        DATA(:,:,5)  = SIO4 ;
        Lsrc(:,5) = 1 ;

        DATA(:,:,6)  = NH4 ;
        Lsrc(:,6) = 1 ;
        DATA(:,:,7)  = Fe ;
        Lsrc(:,7) = 1 ;

        DATA(:,:,8)  = O2 ;
        Lsrc(:,8) = 1 ;
        DATA(:,:,9)  = DIC ;
        Lsrc(:,9) = 1 ;

        DATA(:,:,10)  = Alk ;
        Lsrc(:,10) = 1 ;
        DATA(:,:,11)  = DOC ;
        Lsrc(:,11) = 1 ;
        DATA(:,:,12)  = DON ;
        Lsrc(:,12) = 1 ;
        DATA(:,:,13)  = DOP ;
        Lsrc(:,13) = 1 ;
        DATA(:,:,14)  = NO2 ;
        Lsrc(:,14) = 1 ;

DATA(DATA==0)=NaN ;
Qbar(Qbar==0)=NaN ;
Qbar(isnan(Qbar)) = 0 ;
DATA(isnan(DATA)) = 0 ;

%=========================
%=========================

Msrc=length(Isrc);
Tsrc = size(psrc_time,1) ;

%%%%%%
%%%%%% end of the reding program
%%%%%% DATA ARE READY
%%%%%%
%======================================================
%======================================================
% WRITE IN A NETCDF FILE
%======================================================
%======================================================
disp('writing the nc file...')
% create the ncfile
ncid = netcdf.create(psrc_fname,'netcdf4');
% extract the dimensions
  dimNsrc    = netcdf.defDim    (       ncid,   'Nsrc', Nsrc    );
  dimNpas    = netcdf.defDim    (       ncid,   'Npas',         Npas      ) ;
  dims_rho    = netcdf.defDim   (       ncid,   's_rho',        NZ         ) ;
  dimpsr_time = netcdf.defDim   (       ncid,   'psrc_time',     Tsrc ) ;

% create the variables
% time
psr_time    =  netcdf.defVar(ncid,'psrc_time', 'double', [dimpsr_time]);
netcdf.putAtt(ncid,psr_time,'units','s');
netcdf.putAtt(ncid,psr_time,'long_name','point source time from 1994-1-1');
%psrc_time = ( psrc_time./86400 )-1 ;
netcdf.putVar(ncid,psr_time,psrc_time-1);
% Qbar
q    =  netcdf.defVar(ncid,'Qbar', 'double', [dimpsr_time dimNsrc]);
%q    =  netcdf.defVar(ncid,'Qbar', 'double', [dimNsrc dimpsr_time]);
netcdf.putAtt(ncid,q,'units','meter3 second-1');
netcdf.putAtt(ncid,q,'long_name','vertically integrated mass transport of point');
netcdf.putVar(ncid,q,Qbar);
% Weight
%w    =  netcdf.defVar(ncid,'Qshape', 'double', [dims_rho dimNsrc]);
w    =  netcdf.defVar(ncid,'Qshape', 'double', [dimNsrc dims_rho]);
netcdf.putAtt(ncid,w,'units','no units');
netcdf.putAtt(ncid,w,'long_name','Vertical weight of the flux for each psource cell');
netcdf.putVar(ncid,w,Qshape');
% Isrc
ii    =  netcdf.defVar(ncid,'Isrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,ii,'units','no units');
netcdf.putAtt(ncid,ii,'long_name','global xi-directional grid number of the point sources');
netcdf.putVar(ncid,ii,Isrc);
% Jsrc
jj    =  netcdf.defVar(ncid,'Jsrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,jj,'units','no units');
netcdf.putAtt(ncid,jj,'long_name','global eta-directional grid number of the point sources');
netcdf.putVar(ncid,jj,Jsrc);
% state variables
for i=1:Npas
	pastr    =  netcdf.defVar(ncid,varnames_bgc{i}, 'double', [dimpsr_time dimNsrc]);
%        pastr    =  netcdf.defVar(ncid,varnames_bgc{i}, 'double', [dimNsrc dimpsr_time]);
	netcdf.putAtt(ncid,pastr,'units',psunit{i});
	netcdf.putAtt(ncid,pastr,'long_name',psname{i});
	netcdf.putVar(ncid,pastr,squeeze(DATA(:,:,i)));
end
% Dsrc
dd    =  netcdf.defVar(ncid,'Dsrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,dd,'units','no units');
netcdf.putAtt(ncid,dd,'long_name','flag to determine direction of the mass point source');
netcdf.putVar(ncid,dd,Dsrc);
% Lsrc
%ll    =  netcdf.defVar(ncid,'Lsrc', 'double', [dimNpas dimNsrc]);
ll    =  netcdf.defVar(ncid,'Lsrc', 'double', [dimNsrc dimNpas]);
netcdf.putAtt(ncid,ll,'long_name','logical switch for any tracers at every point source locations');
netcdf.putVar(ncid,ll,Lsrc');


 % insert global attribute
  NC_GLOBAL = netcdf.getConstant('NC_GLOBAL');
netcdf.putAtt(ncid,NC_GLOBAL,'title','ROMS point fource file')
netcdf.putAtt(ncid,NC_GLOBAL,'long_title',psrc_title)
netcdf.putAtt(ncid,NC_GLOBAL,'institution','UCLA/UW/SCCWRP')
netcdf.putAtt(ncid,NC_GLOBAL,'source','roms')


return

change_river

return




ncread('L2_psrc_POTW.nc','psrc_time')


nccreate(psrc_fname,psr_time,'Dimensions',{'psrc_time',dimpsr_time},'Datatype','double') ;

% fill the variables

% globall attributes

change_river

return


%---------------------------------------------------------------------
% Idealized Niida freshwater & sediment discharge: forced to [May 30, 2011]
%Pdirection=2; hpeak=20; Scff=0.01;		% vertical flux

%===============================================================
% rivers
%======================================================
%======================================================
% Qshape
%======================================================
% write down everything to the point source file
Msrc=length(Isrc);
display(['creating ' psrc_fname ' with ' int2str(Msrc) ' psorces.']);
create_psource(psrc_fname,psvars,psname,psunit,Msrc,N,psrc_title,psrc_time,psrc_cycle);

nc=netcdf(psrc_fname,'w');
icc=0;
display(['damping out the data to ' psrc_fname '.']);
for is=1:Nsrc;
    icc=icc+1;
    nc{'Lsrc'}(:,icc)=squeeze(Lsrc(:,is));
    nc{'Isrc'}(icc)=Isrc(is);
    nc{'Jsrc'}(icc)=Jsrc(is);
    nc{'Dsrc'}(icc)=Dsrc(is);
    nc{'Qbar'}(:,icc)=Qbar.*Rate(is);
    for itrc=1:Npas;
      svv=char(psvars(itrc));
      if itrc<=3;	% T, S and tpas1 
        nc{svv}(:,icc)=psvals(itrc);
      else;			% sediments
        nc{svv}(:,icc)=psvals(itrc).*Sed;
      end;
    end;
    nc{'Qshape'}(:,icc)=squeeze(Qshape(:,is));
end;
close(nc);


return;
