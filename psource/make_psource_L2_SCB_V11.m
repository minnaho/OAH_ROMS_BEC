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
addpath(genpath('/data/project3/kesf/tools_matlab/'))
addpath('/data/project3/kesf/tools_roms/B2B/packages')

psrc_title='point source for the southern California Bight L2 300-m grid';
psrc_fname='L2_scb_psourceV11bis.nc';

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc';
load_grid_L2_SCB
% max monthly-mean discharge of Abukuma River is 212.2469 m3/s.
% qave=40;	% m3/s.  ==> crudely assumed that discharge from minor rivers
%       		%            is about 1/5 of the peak discharge from Abukuma.

% number of passive tracers (must be >= 2, including T and S)
%Npas=36; % all tracers		% 4: T, S, sand, silt
% from a random file
par_file = '/data/project3/kesf/ROMS/USSW1/DAILY/ussw1_avg.Y2000M01D01.nc'
[varnames_bgc,longnames_bgc,units_bgc,varnames_bgc_or] = det_bgc_tracers(par_file);
varnames_bgc = ['temp','salt',varnames_bgc] ;
varnames_bgc = varnames_bgc([1 2 3 4 6 7 8 9 10 11 24 26 27]); % 'temp'    'salt'    'PO4'    'NO3'    'NH4'    'Fe'    'Alk'    'DOC'    'DON'    'DOP'    'NO2'
longnames_bgc = ['Temperature at the point source','Salinity at the point source',longnames_bgc];
longnames_bgc = longnames_bgc([1 2 3 4 6 7 8 9 10 11 24 26 27]);% 'temp'    'salt'    'PO4'    'NO3'    'NH4'   'Fe'    'Alk'    'DOC'    'DON'    'DOP'    'NO2'

Npas=length(varnames_bgc) ; % all BGC tracers + T and S     % 4: T, S, sand, silt
psvars = varnames_bgc ;
psname = longnames_bgc ;
units_bgc=['Degrees Celcius','psu',units_bgc] ;
psunit=units_bgc([1 2 3 4 6 8 9 7 10 11 24 26 27]) ;

%%%%%%%%%%%%%%
%% POTW MAJORS
%%%%%%%%%%%%%%
disp('MAJOR POTW ... ')
%% DEFINE THE TIME
ptime = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','time')+datenum(1970,1,1); % 
time = ptime  - datenum(1994,1,1) ;
time_t = find(time>0); 
test_t = find(ptime>=datenum(1997,1,1)) ; datestart = test_t(1) ;
psrc_time = time(test_t) ;
sz_psrc_time = size(psrc_time,1) ;

% test: tutu = psrc_time/86400 + datenum(1994,1,1)
% datestr(time(289)/86400 + datenum(1994,1,1) ) = 02-Jan-1994
pflow = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','flow'); % m3/s
pNO3 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','NO3'); % 
pNH4 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','NH4');
pNO2 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','NO2');
pPO4 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','PO4');
pFe = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','Fe');
pSO2 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','SO2');
palkalinity = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','alkalinity');
ppH = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','pH');
psulfate = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','sulfate');
pBOD = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','BOD');
pTOC = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','TOC');
pON = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','ON');
pOP = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','OP');
pO2 = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','dissolved_oxygen');
psalt = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','salinity');
ptemp = ncread('/data/project1/minnaho/potw_outfall_data/major_potw_data.nc','temperature');

dodic=1;
for i=1:4 % (POTWs)
	flow(:,i) = squeeze(pflow(i,i,datestart:end)) ; % m3/s
	nitrate(:,i) = squeeze(pNO3(i,i,datestart:end)) ; % mmol/m3
	ammonium(:,i) = squeeze(pNH4(i,i,datestart:end)) ;% mmol/m3
	nitrite(:,i) = squeeze(pNO2(i,i,datestart:end)) ;% mmol/m3
	phosphate(:,i) = squeeze(pPO4(i,i,datestart:end)) ;% mmol/m3
	iron(:,i) = squeeze(pFe(i,i,datestart:end)) ;% mmol/m3
	sulfuredioxyde(:,i) = squeeze(pSO2(i,i,datestart:end)) ;% mmol/m3
	alkalinity(:,i) = squeeze(palkalinity(i,i,datestart:end)) ;% mmol/m3
	ph(:,i) = squeeze(ppH(i,i,datestart:end)) ;
	sulfate(:,i) = squeeze(psulfate(i,i,datestart:end)) ;% mmol/m3
	bod(:,i) = squeeze(pBOD(i,i,datestart:end)) ;% mmol/m3
	toc(:,i) = squeeze(pTOC(i,i,datestart:end)) ;% mmol/m3
	on(:,i) = squeeze(pON(i,i,datestart:end)) ;% mmol/m3
	op(:,i) = squeeze(pOP(i,i,datestart:end)) ;% mmol/m3
        sal(:,i) = squeeze(psalt(i,i,datestart:end)) ;% mmol/m3
        o2(:,i) = squeeze(pO2(i,i,datestart:end)) ;% mmol/m3
        tem(:,i) = squeeze(ptemp(i,i,datestart:end)) ;% mmol/m3

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
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alkalinity(:,i),phh,1,3,...
    saltt,tem(:,i),nan,...
    0,nan,...
    sio3,phosphate(:,i),...
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
Qbar(:,1) = flow(:,1).*(9/36) ; % HTP1 (N)
Qbar(:,2) = flow(:,1).*(9/36) ; % HTP2 (S)
for i=3:20
	Qbar(:,i) = flow(:,1).*(1/36) ; % HTP Small flow around the main diffusers
end

% JWPCP : 21 --> 44 (3 MAJORS: 1S AND 2N)
Qbar(:,21) = flow(:,2).*.65.*(11/20) ; % JWPCP1 --> 65% of total (S)
Qbar(:,22) = flow(:,2).*.175.*(6/24) ; % JWPCP2 --> 17.5% of total (N)
Qbar(:,23) = flow(:,2).*.175.*(6/24) ; % JWPCP3 __> 17.5% of total (N)
for i=24:32
        Qbar(:,i) = flow(:,2).*.65.*(1/20) ; % HTP Small flow around the main diffusers 1 (S)
end
for i=33:44
        Qbar(:,i) = flow(:,2).*.175.*(1/24) ; % HTP Small flow around the main diffusers 2 and 3 (N)
end

% OCSD : 45 --> 53 (1 MAJOR)
Qbar(:,45) = flow(:,3).*(10/18) ; % OCSD --> 100% 
for i=46:53
        Qbar(:,i) = flow(:,3).*(1/18) ; % HTP Small flow around the main diffusers 2 and 3 (N)
end

% PLWTP : 54 --> 71 (2 MAJORS)
Qbar(:,54) = flow(:,1).*(8/32) ; % PLWTP1 (N)
Qbar(:,55) = flow(:,1).*(8/32) ; % PLWTP2 (S)
for i=56:71
        Qbar(:,i) = flow(:,1).*(1/32) ; % PLWTP Small flow around the main diffusers
end

%% TRACERS: reprete the same concentration by OUTFALL
%% HTP
for i = 1:20
        db(1,i) = 20 ; % above the bottom in meters (Uchiyama et al 2014)
	NO3(:,i) = nitrate(:,1);
	NH4(:,i) = ammonium(:,1);
	NO2(:,i) = nitrite(:,1);
	PO4(:,i) = phosphate(:,1);
	Fe(:,i) = iron (:,1);
%	SO2 = sulfuredioxyde(:,1);
	Alk(:,i) = alkalinity(:,1);
	PH(:,i) = ph(:,1);
%	sulfate = (:,1);
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
for i= 21:44
        db(1,i) = 30 ; % above the bottom in meters (McLaughlin et al in prep)
        NO3(:,i) = nitrate(:,2);
        NH4(:,i) = ammonium(:,2);
        NO2(:,i) = nitrite(:,2);
        PO4(:,i) = phosphate(:,2);
        Fe(:,i) = iron (:,2);
%       SO2 = sulfuredioxyde(:,1);
        Alk(:,i) = alkalinity(:,2);
        PH(:,i) = ph(:,2);
%       sulfate = (:,1);
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
for i=45:53
	db(1,i) = 30 ;  % above the bottom in meters (McLaughlin et al in prep)
        NO3(:,i) = nitrate(:,3);
        NH4(:,i) = ammonium(:,3);
        NO2(:,i) = nitrite(:,3);
        PO4(:,i) = phosphate(:,3);
        Fe(:,i) = iron (:,3);
%       SO2 = sulfuredioxyde(:,3);
        Alk(:,i) = alkalinity(:,3);
        PH(:,i) = ph(:,3);
%       sulfate = (:,3);
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
for i=54:71
	db(1,i) = 40 ;% above the bottom in meters
        NO3(:,i) = nitrate(:,4);
        NH4(:,i) = ammonium(:,4);
        NO2(:,i) = nitrite(:,4);
        PO4(:,i) = phosphate(:,4);
        Fe(:,i) = iron (:,4);
%       SO2 = sulfuredioxyde(:,4);
        Alk(:,i) = alkalinity(:,4);
        PH(:,i) = ph(:,4);
%       sulfate = (:,4);
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

find_IJsrc_outfalls

%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% mimiking the buyancy flux of the seawage coming from the outfalls
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
z_r = zbot1;
cff=0;
%% calculate the qshape
for i=1:size(Isrc,2) % by diffuser
%DB = db(1,i) ;
%DB = 25;
        for k=1:NZ % vertical levels
%        Zcff=max(2.,h(Isrc(i),Jsrc(i))-DB) ;

if i<=20
Zcff = 40 ;
elseif (i>=21 & i<=44)
Zcff = 40 ;
elseif (i>=45 & i<=53)
Zcff = 40 ;
elseif (i>=54 & i<71)
Zcff = 60 ;
end

        Zcff_disp(i) = Zcff ;
%       disp([num2str(Zcff) , '  - ' , num2str(i)])
        Scff=0.02;    % 0.15 ;
        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
        end
        Qshape(:,i) = Qs./sum(Qs) ;
end

%for i=1:size(Isrc,2) % by diffuser
%DB = db(1,i) ;
%        for k=1:NZ % vertical levels
%        Zcff=max(2.,h(Isrc(i),Jsrc(i))-DB) ;
%        Scff=0.02 ;
%        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
%        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
%        end
%        Qshape(:,i) = Qs./sum(Qs) ;
%end

%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;

%% Dsrc
Dsrc1 = ones(psNOW,1) .* 2 ;

%======================================================
%======================================================
%% PART 2
disp('Minor POTW ... ')
pflow = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','flow'); % m3/s
pNO3 = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','NO3'); %
pNH4 = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','NH4'); % 
pNO2 = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','NO2'); %
pPO4 = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','PO4'); %
palkalinity = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','alkalinity'); %
pph = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','pH'); %
ptoc =  ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','TOC'); %
ptemp =  ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','temperature'); %

%% DEFINE THE TIME
ptime = ncread('/data/project1/minnaho/potw_outfall_data/minor_potw_data.nc','time'); %
time = ptime  + datenum(1997,1,1) ;
test_t = find(time>=datenum(1997,1,1)) ;

%test_t = test_t(1:180) ;
time_l = time(test_t)-datenum(1994,1,1) ;
test = find(psrc_time<time_l(1)) ;
if isempty(test)
datestart =1; dateend = datestart+size(time_l,1)-1 ;
else
datestart = test(end)+1 ; dateend = datestart+size(time_l,1)-1 ;
end
%% IMPRTANT : TEST THE NUMBER OF POINT SOURCES
num= size(pflow,1) ;
clear flow nitrate ammonium nitrite phosphate alkalinity ph toc tem
for i=1:num % (POTWs)
        flow(:,i) = squeeze(pflow(i,i,test_t)) ; % m3/s
        nitrate(:,i) = squeeze(pNO3(i,i,test_t)) ; % mmol/m3
        ammonium(:,i) = squeeze(pNH4(i,i,test_t)) ;% mmol/m3
        nitrite(:,i) = squeeze(pNO2(i,i,test_t)) ;% mmol/m3
        phosphate(:,i) = squeeze(pPO4(i,i,test_t)) ;% mmol/m3
        alkalinity(:,i) = squeeze(palkalinity(i,i,test_t)) ;% mmol/m3
        ph(:,i) = squeeze(pph(i,i,test_t)) ;% mmol/m3
        toc(:,i) = squeeze(ptoc(i,i,test_t)) ;% mmol/m3
        tem(:,i) = squeeze(ptemp(i,i,test_t)) ;% C
end


%% start from the end of MAJOR POTWS
for i=psNOW+1:psNOW+num
	Qbar(datestart:dateend,i) = flow(:,i-psNOW);
        NO3(datestart:dateend,i) = nitrate(:,i-psNOW);
        NH4(datestart:dateend,i) = ammonium(:,i-psNOW);
        NO2(datestart:dateend,i) = nitrite(:,i-psNOW);
        PO4(datestart:dateend,i) = phosphate(:,i-psNOW);
	
	Fe(datestart:dateend,i) = 0.*flow(:,i-psNOW);
        Alk(datestart:dateend,i) = alkalinity(:,i-psNOW);
	PH(datestart:dateend,i) = ph(:,i-psNOW);
        DOC(datestart:dateend,i) = toc(:,i-psNOW);
        DON(datestart:dateend,i) = 0.137.*toc(:,i-psNOW);
        DOP(datestart:dateend,i) = 0.0625.*toc(:,i-psNOW);
	O2(datestart:dateend,i) = 0.*flow(:,i-psNOW)+(5.6/16*1000);
        salt(datestart:dateend,i) = 0.*flow(:,i-psNOW) + 1 ;
        temp(datestart:dateend,i) = tem(:,i-psNOW) ;

PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = 13 ;
ttemp = 28 ;
sio3 = 20 ;
phh = 7.5 ;
clear DATA
[DATA,HEADERS,NICEHEADERS]=CO2SYS(Alk(datestart:dateend,i),phh,1,3,...
    saltt,ttemp,nan,...
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
lon_minor_potw
lat_minor_potw

x = ln_minpotw ;
y = lt_minpotw ;
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Jsrc(psNOW+1:psNOW+num)  = mplat ;
Isrc(psNOW+1:psNOW+num)  = mplon ;
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
z_r = zbot1;
cff=0;
%% calculate the qshape
for i=psNOW+1:psNOW+num % by diffuser
DB = 20 ;
        for k=1:NZ % vertical levels
        Zcff=max(2.,h(Isrc(i),Jsrc(i))-DB) ;
        Scff=0.02 ;
        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
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
disp('RIVERS 10 Y ... ')

pflow = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','flow'); % m3/s
pNO3 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','nitrate'); %
pNH4 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','ammonium'); %
pPO4 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','phosphate'); %
pTON = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','total_nitrogen'); %
pTOP = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','total_phosphorus'); %
palkalinity = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','alkalinity'); %
ptemp = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','temperature'); %
pDON = pTON - (pNH4+pNO3); pDON(pDON<0)=1e-10 ;
pDOP = pTOP - pPO4 ; pPO4(pPO4<0)=1e-10 ;

%% DEFINE THE TIME
ptime = ncread('/data/project1/minnaho/river_data/south_coast_rivers_10_years_monthly_new.nc','time'); %
%time = ( ptime + datenum(1997,1,1)  - datenum(1994,1,1) +1 ).*86400;
time = ( ptime + datenum(1997,1,1)  - datenum(1994,1,1) ) ;
test_t = find(time>0);
time_l = time(test_t) ;
test = find(psrc_time<time_l(1)) ;
if isempty(test)
datestart =1;; dateend = datestart+size(time_l,1)-1 ;
else
datestart = test(end)+1 ; dateend = datestart+size(time_l,1)-1 ;
end
%% IMPRTANT : TEST THE NUMBER OF POINT SOURCES
num= size(pflow,1) ;

clear flow nitrate ammonium phosphate don dop alkalinity Temp 
for i=1:num
        flow(:,i) = squeeze(pflow(i,i,test_t)) ; % m3/s
        nitrate(:,i) = squeeze(pNO3(i,i,test_t)) ; % mmol/m3
        ammonium(:,i) = squeeze(pNH4(i,i,test_t)) ;% mmol/m3
        phosphate(:,i) = squeeze(pPO4(i,i,test_t)) ;% mmol/m3
        don(:,i) = squeeze(pDON(i,i,test_t)) ;% mmol/m3
        dop(:,i) = squeeze(pDOP(i,i,test_t)) ;% mmol/m3
        alkalinity(:,i) = squeeze(palkalinity(i,i,test_t)) ;% mmol/m3
        Temp(:,i) = squeeze(ptemp(i,i,test_t)) ;% mmol/m3
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

        Fe(datestart:dateend,i) = 0.*flow(:,i-psNOW);
        Alk(datestart:dateend,i) = alkalinity(:,i-psNOW);
        DOC(datestart:dateend,i) = (1/0.137).*don(:,i-psNOW);
	NO2(datestart:dateend,i) = 0.*flow(:,i-psNOW);
	O2(datestart:dateend,i) = 0.*flow(:,i-psNOW) + (7/16*1000) ;
        temp(datestart:dateend,i) = Temp(:,i-psNOW);
	salt(datestart:dateend,i) = 0.*flow(:,i-psNOW) + 13 ;
PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = 13 ;
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
lat_rivers_new ;
lon_rivers_new ;

x = ln_riv (1:48);
y = lt_riv (1:48);
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Jsrc(psNOW+1:psNOW+num)  = mplat ;
Isrc(psNOW+1:psNOW+num)  = mplon ;
%% Dsrc
Dsrc3 = ones(length(x),1) .* 1 ;
%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% distribution of the flux on the top layers
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
z_r = zbot1;
for i = psNOW+1:psNOW+num
	for k=1:NZ
	Zcff= z_r(Isrc(i),Jsrc(i),60) ;
	Scff=0.02 ;
	Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
	end
Qshape(:,i) = Qs./sum(Qs) ;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;
disp('RIVERS 24 Y ... ')
%% OTHER RIVERS
pflow = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','flow'); % m3/s
pNO3 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','nitrate'); %
pNH4 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','ammonium'); %
pPO4 = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','phosphate'); %
pTON = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','total_nitrogen'); %
pTOP = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','total_phosphorus'); %
palkalinity = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','alkalinity'); %
ptemp = ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','temperature'); %
pDON = pTON - (pNH4+pNO3); pDON(pDON<0)=1e-10 ;
pDOP = pTOP - pPO4 ; pPO4(pPO4<0)=1e-10 ;

%% DEFINE THE TIME
ptime = double(ncread('/data/project1/minnaho/river_data/south_coast_rivers_24_years_monthly_new.nc','time')) + datenum(1990,1,1) ; %
%time = ( ptime + datenum(1990,1,1)  - datenum(1994,1,1) +1 ).*86400;
time = ( ptime - datenum(1994,1,1) ) ;
test_t = find(time>0);
time_l = time(test_t) ;

indx = datenum(1997,1,1)-datenum(1994,1,1);
list_t = find(time_l>=indx)+test_t(1)-1 ;
time_l = time(list_t) ;
test_t = list_t ; 

test = find(psrc_time<time_l(1)) ;
if isempty(test)
datestart =1;; dateend = datestart+size(time_l,1)-1 ;
else 
datestart = test(end)+1 ; dateend = datestart+size(time_l,1)-1 ;
end
%% IMPRTANT : TEST THE NUMBER OF POINT SOURCES
num= size(pflow,1) ;

clear flow nitrate ammonium phosphate don dop alkalinity Temp
for i=1:num
        flow(:,i) = squeeze(pflow(i,i,test_t)) ; % m3/s
        nitrate(:,i) = squeeze(pNO3(i,i,test_t)) ; % mmol/m3
        ammonium(:,i) = squeeze(pNH4(i,i,test_t)) ;% mmol/m3
        phosphate(:,i) = squeeze(pPO4(i,i,test_t)) ;% mmol/m3
        don(:,i) = squeeze(pDON(i,i,test_t)) ;% mmol/m3
        dop(:,i) = squeeze(pDOP(i,i,test_t)) ;% mmol/m3
        alkalinity(:,i) = squeeze(palkalinity(i,i,test_t)) ;% mmol/m3
        Temp(:,i) = squeeze(ptemp(i,i,test_t)) ;% mmol/m3
end

%% start from the end of MAJOR POTWS
for i=psNOW+1:psNOW+num
%        db(1,i) = 20 ; % above the bottom in meters (Uchiyama et al 2014)
        Qbar(datestart:dateend,i) = flow(:,i-psNOW);
        NO3(datestart:dateend,i) = nitrate(:,i-psNOW);
        NH4(datestart:dateend,i) = ammonium(:,i-psNOW);
        PO4(datestart:dateend,i) = phosphate(:,i-psNOW);
        DON(datestart:dateend,i) = don(:,i-psNOW);
        DOP(datestart:dateend,i) = dop(:,i-psNOW);

        Fe(datestart:dateend,i) = 0.*flow(:,i-psNOW);
        Alk(datestart:dateend,i) = alkalinity(:,i-psNOW);
        DOC(datestart:dateend,i) = (1/0.137).*don(:,i-psNOW);
        NO2(datestart:dateend,i) = 0.*flow(:,i-psNOW);
        O2(datestart:dateend,i) = 0.*flow(:,i-psNOW) + (7/16*1000) ;
	temp(datestart:dateend,i) = Temp(:,i-psNOW);
        salt(datestart:dateend,i) = 0.*flow(:,i-psNOW) + 13 ;
PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
saltt = 13 ;
%temp = 28 ;
sio3 = 20 ;
phh = 7.5 ;
clear DATA
t = temp(datestart:dateend,i) ;
t(isnan(t) | t==0) = 26 ;
ppo4 = PO4(datestart:dateend,i) ;
ppo4(ppo4==0)=1.27;
[DATA,HEADERS,NICEHEADERS]=CO2SYS(Alk(datestart:dateend,i),phh,1,3,...
    saltt,t,nan,...
    0,nan,...
    sio3,ppo4(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
DIC(datestart:dateend,i) = DATA(:,2) ;% mmol/m3

end


%%%%%%%%%%%%%%%
%% Isrc Jsrc %%
%%%%%%%%%%%%%%%

% find the location of I and J
lat_rivers_new ;
lon_rivers_new ;

x = ln_riv(49:72) ;
y = lt_riv(49:72) ;
clear mplat mplon
for i=1:length(x)
        [mplat(i), mplon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
Jsrc(psNOW+1:psNOW+num)  = mplat ;
Isrc(psNOW+1:psNOW+num)  = mplon ;

%% Dsrc
Dsrc4 = ones(length(x),1) .* 1 ;

%%%%%%%%%%%%
%% QSHAPE %%
%%%%%%%%%%%%
%% distribution of the flux on the top layers
%%
% h is the bathyemtry
% NZ : number of vertical levels
% z_r : depth calculated in ROMS for zeta=0
% db : in m above the bottom in meters
z_r = zbot1;
for i = psNOW+1:psNOW+num
        for k=1:NZ
        Zcff= z_r(Isrc(i),Jsrc(i),60) ;
        Scff=0.02 ;
        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
        end
Qshape(:,i) = Qs./sum(Qs) ;
end

%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;

%% ALL RIVERS END
%======================================================
%======================================================
%=========================
% DATA
%=========================
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

clear DATA

        DATA(:,:,1)  = temp ;
        Lsrc(:,1) = 1 ;
        DATA(:,:,2)  = salt ;
        Lsrc(:,2) = 1 ;
        DATA(:,:,3)  = PO4 ;
        Lsrc(:,3) = 1 ;
        DATA(:,:,4)  = NO3 ;
        Lsrc(:,4) = 1 ;
        DATA(:,:,5)  = NH4 ;
        Lsrc(:,5) = 1 ;
        DATA(:,:,6)  = Fe ;
        Lsrc(:,6) = 1 ;

        DATA(:,:,7)  = O2 ;
        Lsrc(:,7) = 1 ;
        DATA(:,:,8)  = DIC ;
        Lsrc(:,8) = 1 ;

        DATA(:,:,9)  = Alk ;
        Lsrc(:,9) = 1 ;
        DATA(:,:,10)  = DOC ;
        Lsrc(:,10) = 1 ;
        DATA(:,:,11)  = DON ;
        Lsrc(:,11) = 1 ;
        DATA(:,:,12)  = DOP ;
        Lsrc(:,12) = 1 ;
        DATA(:,:,13)  = NO2 ;
        Lsrc(:,13) = 1 ;

DATA(DATA==0)=NaN ;
Qbar(Qbar==0)=NaN ;
Qbar(isnan(Qbar)) = 0 ;
DATA(isnan(DATA)) = 0 ;
%=========================
% Dsrc
%=========================
% 0 xi direction 1 rho direction 2 s directon
Dsrc = [Dsrc1 ; Dsrc2 ; Dsrc3 ; Dsrc4] ;
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
netcdf.putVar(ncid,ii,Jsrc);
% Jsrc
jj    =  netcdf.defVar(ncid,'Jsrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,jj,'units','no units');
netcdf.putAtt(ncid,jj,'long_name','global eta-directional grid number of the point sources');
netcdf.putVar(ncid,jj,Isrc);
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




ncread('L2_psrc_POTW.nc','psrc_time')


nccreate(psrc_fname,psr_time,'Dimensions',{'psrc_time',dimpsr_time},'Datatype','double') ;

% fill the variables

% globall attributes



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
