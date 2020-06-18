
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_30m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1997,2,1):datenum(2007,11,30);
months = str2num(datestr(date,'mm')) ;
%% april to august
list = find(months>5 & months<12);
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  7.7 ;
ThresholdDuration =  7 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/echinoderms_nc/echinoderm_behavior_30m_jun_nov_1997_2007.nc'];
