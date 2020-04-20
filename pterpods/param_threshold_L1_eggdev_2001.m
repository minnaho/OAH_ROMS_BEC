
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_30m_2001.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
% march >> april
date = datenum(2001,1,1):datenum(2001,12,31);
months = str2num(datestr(date,'mm')) ;
list =find(months>2 & months<4);
InputData = squeeze(InputData(:,:,list)) ;

ThresholdMagnitude =  .9 ;
ThresholdDuration =  2 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_eggdev_2001.nc'];
