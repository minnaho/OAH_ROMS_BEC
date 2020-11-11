addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))

PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
%saltt = 33 ;
%sio3 = 20 ;
saltt = 1.5 ;
sio3 = 1459.82802514 ;

alkalinity = 6244.38005795;
phh=7.6;
temp = 25 ;
phosphate = 98;

clear DATA
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alkalinity,phh,PAR1TYPE,PAR2TYPE,...
    saltt,temp,nan,...
    0,nan,...
    sio3,phosphate,...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);

dic = DATA(:,2) ;% mmol/m3

