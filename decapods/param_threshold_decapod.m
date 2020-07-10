
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_100_1150m_int.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  7.38 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/echinoderms_nc/echinoderm_adult_feeding_rate_100m_1150m_avg_1997_2007.nc'];
