
load_grid_ussw1

file = '/data/project4/kesf/Diagnostics/xyt/om_juranek_L1.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1997,1,1):datenum(2002,12,31);
months = str2num(datestr(date,'mm')) ;
years = str2num(datestr(date,'yyyy')) ;
% may >> august
list =find(months>4 & months<9 & years > 1998 & years < 2002);
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  0.9 ;
ThresholdDuration =  2 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_eggdev_100m_1999_2001.nc'];
