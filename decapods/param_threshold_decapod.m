
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_100m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  7.4 ;
ThresholdDuration =  7 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_nc/decapods_larval_mort_100m_7days_1997_2007.nc'];
