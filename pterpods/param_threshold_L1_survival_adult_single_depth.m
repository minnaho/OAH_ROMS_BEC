
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');

% june >> feb of next year

date = datenum(1997,1,1):datenum(2006,12,31);
months = str2num(datestr(date,'mm'));
list1 = find(months>5);
list2 = find(months<3);

list = sort([list1;list2])
% length is 2732 days

InputData = squeeze(InputData(:,:,list)) ;

ThresholdMagnitude =  0.95 ;
ThresholdDuration =  14 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_survival_adult_200m_1997_2006.nc'];

