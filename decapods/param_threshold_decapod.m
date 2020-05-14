
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_300m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  7.76 ;
ThresholdDuration =  9 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_nc/decapods_adult_mort_300m_9d_1997_2007.nc'];
