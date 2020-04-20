
load_grid_ussw1

file = '/data/project3/kesf/tools_matlab/applications/pteropods/om_juranek_L1_200m_2001_2002.nc' ;
disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');

date1 = datenum(2001,1,1):datenum(2001,12,31);
months1 = str2num(datestr(date1,'mm')) ;
% june 2001 >> feb 2002
list1 =find(months1>5);

date2 = datenum(2002,1,1):datenum(2002,12,31);
months2 = str2num(datestr(date2,'mm'));
list2 =find(months1<3);
list2 = list2+365
list = [list1;list2]

InputData = squeeze(InputData(:,:,list)) ;
ThresholdMagnitude =  1.15 ;
ThresholdDuration =  14 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project3/kesf/tools_matlab/applications/pteropods/pteropods_shelldiss_severe_adult_2001_2002.nc'];
