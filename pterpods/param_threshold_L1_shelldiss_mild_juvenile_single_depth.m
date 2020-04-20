
load_grid_ussw1

%file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_100m.nc' ;
file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m_2001_mean.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
%date = datenum(1997,1,1):datenum(2006,12,31);
date = datenum(2001,1,1):datenum(2001,12,31);
months = str2num(datestr(date,'mm')) ;
%% june august
list = find(months>2 & months<6);
% 610 days
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  1.5 ;
ThresholdDuration =  5 ;
outPerDay = 1 ;

disp('data ready ')
%fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_mild_juvenile_100m_1997_2006.nc'];
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_mild_juvenile_0_200m_2001.nc'];
