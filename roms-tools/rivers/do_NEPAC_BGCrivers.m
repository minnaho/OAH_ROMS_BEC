clear all

% 1=temp, 2=salt, 3=po4, 4=no3, 5=Sio3, 6=nh4, 7=Fe, 8=O2, 9=Dic, 10=Alk, 11=doc, 12=don, 13=dofe, 14=dop, 15=dopr, 16=donr, 17=zooc, 18=spc, 19=spchl, 20=spfe, 21=spcaco3, 22=diatc, 23=diatchl, 24=diatfe, 25=diatsi, 26=diazc, 27=diachl, 28=diazfe, 29= no2, 30=n2, 31=n2o

RIVER(1:31,1:12) = NaN ;
eps = 1e-4 ; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Columbia River %%%%%%%%%%%%%%%%%%%%%%%
% Bruland et al., 2008; 
RIVER(1,1:12) = [14 16 14 13 10 9 5 5 6 7 8 10] ; % temp
RIVER(2,1:12) = ones(1,12)*1.0 ; % salt
RIVER(4,1:12) = [26 28 34 30 25 18 10 8 8.5 10 15 18] ; % no3
RIVER(5,1:12) = [5 4.5 5.5 8 12 15 18 20 19 14 11 7] ; % SiO3 
% Park et al., 1970;
RIVER(3,1:12) = [1 1.5 2 1.8 1.5 0.2 0.2 0.2 0.2 0.5 0.7 0.9] ; % po4
RIVER(9,1:12) = ones(1,12)*2275 ; %dic
RIVER(10,1:12) = ones(1,12)*2275 ; %alk
RIVER(7,1:12) = ones(1,12)*1.5 ; %Fe
% Gilbert et al., 2012
RIVER(6,1:12) = ones(1,12)*2.0 ; %Nh4
CHL(1:12) = ones(1,12)*3.8 ; %CHL
RIVER(8,1:12) = ones(1,12)*176 ; %O2
% SCALED VARIABLES :
RIVER(12,1:12) = 1.0 ;  RIVER(13,1:12) = 0.0001 ; RIVER(14,1:12) = 0.1 ; RIVER(15,1:12) = 0.003 ;  RIVER(16,1:12) = 0.8 ;
RIVER(17,1:12) = 1.35*CHL(1:12) ; RIVER(18,1:12) = 3.375*CHL(1:12) ; RIVER(19,1:12) = 0.675*CHL(1:12) ; 
RIVER(20,1:12) = 1.35e-5*CHL(1:12) ; RIVER(21,1:12) = 0.0675*CHL(1:12) ; RIVER(22,1:12) = 0.2025*CHL(1:12) ;
RIVER(23,1:12) = 0.0675*CHL(1:12) ; RIVER(24,1:12) = 1.35e-6*CHL(1:12) ; RIVER(25,1:12) = 0.0675*CHL(1:12) ;
RIVER(26,1:12) = 0.0375*CHL(1:12) ; RIVER(27,1:12) = 0.0075*CHL(1:12) ;  RIVER(28,1:12) = 7.5e-7*CHL(1:12) ;
% eps
RIVER(11,1:12) = eps ; %DOC
RIVER(29,1:12) = 0.28 ; %NO2
RIVER(30,1:12) = eps ; %N2
RIVER(31,1:12) = 0.01 ; %N2O

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Fraser River %%%%%%%%%%%%%%%%%%%%%%%
% Harrison 1991
RIVER(1,1:12) = ones(1,12)*17 ; % temp
RIVER(4,1:12) = ones(1,12)*28 ; % no3
RIVER(6,1:12) = ones(1,12)*5.6 ; %Nh4
RIVER(3,1:12) = ones(1,12)*9.3 ; % po4

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Sacramento River %%%%%%%%%%%%%%%%%%%%%%%
% Saleh, 2021; Glibert, 2010
RIVER(4,1:12) = ones(1,12)*57 ; % no3
RIVER(6,1:12) = ones(1,12)*3.5 ; % Nh4
RIVER(3,1:12) = ones(1,12)*1.9 ; % po4

%%%%% Susitna River %%%%%%%%%%%%%%%%%%%%%%%
% little-susitna-river-2007-adec.pdf
RIVER(4,1:12) = ones(1,12)*21.4 ; % no3
RIVER(3,1:12) = ones(1,12)*19.3 ; % po4

%%%%% Skeena River %%%%%%%%%%%%%%%%%%%%%%%
% Bhangu & Whitfield 1997
RIVER(7,1:12) = ones(1,12)*9.1 ; %Fe


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

river_file = 'uswc1200_riv.nc' ;
nb_river = 2 ; 

RIVER = RIVER' ;
RIVERfull(1,:,:) = [RIVER(12,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' ...
                     RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' ...
                     RIVER(:,:)' RIVER(:,:)' RIVER(:,:)' RIVER(:,:)'];

ncwrite(river_file,'river_tracer',RIVERfull,[nb_river 1 1]) ;
 



