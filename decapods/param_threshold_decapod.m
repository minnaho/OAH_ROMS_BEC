
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_50m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  7.52 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_juvenile_mort_50m_1997_2007.nc'];
