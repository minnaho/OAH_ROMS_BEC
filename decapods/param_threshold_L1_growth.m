
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m_1999.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1999,1,1):datenum(1999,12,31);
months = str2num(datestr(date,'mm')) ;
% june >> july
list =find(months>3 & months<9);
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  1.05 ;
ThresholdDuration =  7 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_growth.nc'];
