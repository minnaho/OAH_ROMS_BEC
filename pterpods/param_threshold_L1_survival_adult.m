
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m_1999.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1999,1,1):datenum(1999,12,31);
months = str2num(datestr(date,'mm')) ;
% may june
% july september (adult)
list = find(months>6 & months<10);
InputData = squeeze(InputData(:,:,list)) ;

ThresholdMagnitude =  0.95 ;
ThresholdDuration =  14 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_survival_adult.nc'];

