
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m_1999.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1999,1,1):datenum(1999,12,31);
months = str2num(datestr(date,'mm')) ;
% june >> august
list = find(months>5 & months<9);
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  1.2 ;
ThresholdDuration =  14 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_sever.nc'];
