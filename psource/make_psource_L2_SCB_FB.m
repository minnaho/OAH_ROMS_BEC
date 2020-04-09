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
psrc_fname='psource_L2_scb_FB.nc';

% input files
grdname = '/data/project5/kesf/ROMS/FlatBot/roms_grd.nc';
load_grid_FB
%%
Riv =0;
small=0;
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
pO2 = pO2.*0+(2/16*1000) ;
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
        
% OCSD : 45 --> 53 (1 MAJOR)
Qbar(:,1) = flow(:,3) ; % OCSD --> 100%

%% TRACERS: repete the same concentration by OUTFALL
for i=1
	db(1,i) = 10 ;  % above the bottom in meters (McLaughlin et al in prep)
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
 

%%%%%%%%%%%
%% Isrc &
%% Jsrc
%%%%%%%%%%

%find_IJsrc_outfalls
Isrc = 26 ;% Isrc(45) ;
Jsrc = 26 ; % Jsrc(45) ;
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
for i=1
%% pipe
DB = 25;
        for k=1:NZ % vertical levels
Zcff = 35 ;
	Zcff_disp(i) = Zcff ;
        Scff=0.1;    % 0.15 ;
        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
        Qs(k)=exp(-Scff.*( Xcff^2 )) ;
        end
        Qshape(:,i) = Qs./sum(Qs) ;

%% river
%z_r = zbot1;
%        for k=1:NZ
%        Zcff= z_r(Isrc(i),Jsrc(i),60) ;
%        Scff=0.05 ;
%        Xcff = abs(z_r(Isrc(i),Jsrc(i),k) - Zcff) ;
%            Qs(k)=exp(-Scff.*( Xcff^2 )) ;
%        end
%Qshape(:,i) = Qs./sum(Qs) ;



end % i

%% imprtant: test the size of the point psource and time scale
[timeNOW psNOW] = size(Qbar) ;

%% Dsrc
Dsrc1 = ones(psNOW,1) .* 2 ;

% DATA
%=========================
%%%%%%%%%%%
%% Nsrc
%%%%%%%%%%%
Nsrc = size(Qbar,2) ;
Nsrc = 2;
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
temp = [temp temp.*1.5] ;
        DATA(:,:,1)  = temp ;
        Lsrc(1,:) = 1 ;
salt = [salt salt.*1.5] ;
        DATA(:,:,2)  = salt ;
        Lsrc(2,:) = 1 ;
PO4 = [PO4 PO4.*1.5];
        DATA(:,:,3)  = PO4 ;
        Lsrc(3,:) = 1 ;
NO3 = [NO3 NO3.*1.5];
        DATA(:,:,4)  = NO3 ;
        Lsrc(4,:) = 1 ;
NH4 = [NH4 NH4.*1.5];
        DATA(:,:,5)  = NH4 ;
        Lsrc(5,:) = 1 ;
Fe = [Fe Fe.*1.5];
        DATA(:,:,6)  = Fe ;
        Lsrc(6,:) = 1 ;
O2 = [O2 O2.*1.5] ;
        DATA(:,:,7)  = O2 ;
        Lsrc(7,:) = 1 ;
DIC = [DIC DIC.*1.5] ;
        DATA(:,:,8)  = DIC ;
        Lsrc(8,:) = 1 ;
Alk = [Alk Alk.*1.5] ;
        DATA(:,:,9)  = Alk ;
        Lsrc(9,:) = 1 ;
DOC = [DOC DOC.*1.5] ;
        DATA(:,:,10)  = DOC ;
        Lsrc(10,:) = 1 ;
DON = [DON DON.*1.5] ;
        DATA(:,:,11)  = DON ;
        Lsrc(11,:) = 1 ;
DOP = [DOP DOP.*1.5] ;
        DATA(:,:,12)  = DOP ;
        Lsrc(12,:) = 1 ;
NO2 = [NO2 NO2.*1.5] ;
        DATA(:,1:2,13)  = NO2 ;
        Lsrc(13,:) = 1 ;

DATA(DATA==0)=NaN ;
Qbar(Qbar==0)=NaN ;
Qbar(isnan(Qbar)) = 0 ;
DATA(isnan(DATA)) = 0 ;
%=========================
% Dsrc
%=========================
% 0 xi direction 1 rho direction 2 s directon
if Riv==1
Dsrc = [Dsrc1 ; Dsrc2 ; Dsrc3 ; Dsrc4] ;
elseif small==1
Dsrc = [Dsrc1 ; Dsrc2];
else
Dsrc = [Dsrc1];
end

%=========================
%=========================

Msrc=length(Isrc);
Tsrc = size(psrc_time,1) ;

%% CORRECTIONS AFTER REVIEW : RIVERS
J= Jsrc;
I= Isrc;

for k=1
J(k) = Jsrc(k) ;
I(k) = Isrc(k) ;
end

%%%%%%
%%%%%% end of the reding program
%%%%%% DATA ARE READY
%%%%%%
%======================================================
%======================================================
% WRITE IN A NETCDF FILE
%======================================================
%======================================================
%for i=2:size(Qshape,2)
%Qshape(:,i) = Qshape(:,1) ;
%end

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
Qbar = [Qbar Qbar.*2] ;
q    =  netcdf.defVar(ncid,'Qbar', 'double', [dimpsr_time dimNsrc]);
netcdf.putAtt(ncid,q,'units','meter3 second-1');
netcdf.putAtt(ncid,q,'long_name','vertically integrated mass transport of point');
netcdf.putVar(ncid,q,Qbar);
% Weight
Qshape=Qshape';
Qshape = [Qshape ; Qshape] ;
w    =  netcdf.defVar(ncid,'Qshape', 'double', [dimNsrc dims_rho]);
netcdf.putAtt(ncid,w,'units','no units');
netcdf.putAtt(ncid,w,'long_name','Vertical weight of the flux for each psource cell');
netcdf.putVar(ncid,w,Qshape);
% Isrc
J = [J J];
ii    =  netcdf.defVar(ncid,'Isrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,ii,'units','no units');
netcdf.putAtt(ncid,ii,'long_name','global xi-directional grid number of the point sources');
netcdf.putVar(ncid,ii,J);
% Jsrc
I = [I I+10];
jj    =  netcdf.defVar(ncid,'Jsrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,jj,'units','no units');
netcdf.putAtt(ncid,jj,'long_name','global eta-directional grid number of the point sources');
netcdf.putVar(ncid,jj,I);
% state variables
for i=1:Npas
        pastr    =  netcdf.defVar(ncid,varnames_bgc{i}, 'double', [dimpsr_time dimNsrc]);
	netcdf.putAtt(ncid,pastr,'units',psunit{i});
	netcdf.putAtt(ncid,pastr,'long_name',psname{i});
        netcdf.putVar(ncid,pastr,squeeze(DATA(:,:,i)));
end
% Dsrc
dd    =  netcdf.defVar(ncid,'Dsrc', 'double', [dimNsrc]);
netcdf.putAtt(ncid,dd,'units','no units');
netcdf.putAtt(ncid,dd,'long_name','flag to determine direction of the mass point source');
netcdf.putVar(ncid,dd,[Dsrc Dsrc]);
% Lsrc
ll    =  netcdf.defVar(ncid,'Lsrc', 'double', [dimNsrc dimNpas]);
netcdf.putAtt(ncid,ll,'long_name','logical switch for any tracers at every point source locations');
netcdf.putVar(ncid,ll,Lsrc);


 % insert global attribute
  NC_GLOBAL = netcdf.getConstant('NC_GLOBAL');
netcdf.putAtt(ncid,NC_GLOBAL,'title','ROMS point fource file')
netcdf.putAtt(ncid,NC_GLOBAL,'long_title',psrc_title)
netcdf.putAtt(ncid,NC_GLOBAL,'institution','UCLA/UW/SCCWRP')
netcdf.putAtt(ncid,NC_GLOBAL,'source','roms')

return


