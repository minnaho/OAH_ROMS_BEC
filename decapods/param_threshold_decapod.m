
load_grid_ussw1

file = '/data/project1/minnaho/decapods/om_juranek_L1_50m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1997,1,1):datenum(2007,12,31);
months = str2num(datestr(date,'mm')) ;
%% june august
%list = find(months>2 & months<6);
%InputData = squeeze(InputData(:,:,list)) ;
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  1.5 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
%fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_mild_juvenile_100m_1997_2006.nc'];
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_mild_juvenile_0_200m_2001.nc'];
