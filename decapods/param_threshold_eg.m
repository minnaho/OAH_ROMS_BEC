load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1.nc' ;
data = ncread(file,'var');

fout =   '/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_behavior_L1.nc';

DATA = squeeze(data(i,j,:)) ;
ThresholdMagnitude = 1.5 ;
ThresholdDuration = 7 ;
InputData = DATA' ;
outPerDay = 1 ;

