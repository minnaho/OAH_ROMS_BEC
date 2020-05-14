
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_300m_slice.nc' ;
% pick year to subsample output
year_select = 1998;

disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
% total time that output file accounts for (daily timestep)
date = datenum(1997,2,1):datenum(2007,11,30);
year = str2num(datestr(date,'yyyy'));
list = find(year==year_select);
InputData = squeeze(InputData(:,:,list)) ;

ThresholdMagnitude =  7.76 ;
ThresholdDuration =  9 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_nc/yearly_freq/decapods_adult_search_300m_9d_',num2str(year_select),'.nc'];
