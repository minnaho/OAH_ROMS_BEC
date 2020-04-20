
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');

ThresholdMagnitude =  1 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_behavior_L1_omega_',num2str(ThresholdMagnitude),'_',num2str(ThresholdDuration),'days.nc'];

