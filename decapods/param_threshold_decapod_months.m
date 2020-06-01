
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_100m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
date = datenum(1997,2,1):datenum(2007,11,30);
months = str2num(datestr(date,'mm')) ;
%% april to august
list = find(months>2 & months<8);
InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  7.75 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_nc/decapod_juvenile_mort_100m_upwell_1997_2007.nc'];
