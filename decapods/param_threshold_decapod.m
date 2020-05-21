
load_grid_ussw1

file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_30m_slice.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
InputData = squeeze(InputData(:,:,:)) ;
ThresholdMagnitude =  7.7 ;
ThresholdDuration =  7 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/echinoderms_nc/echinoderm_larval_behavior_30m_1997_2007.nc'];
