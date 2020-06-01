%% ============================================================ %%
%% program allows to calculate 					%%
%% duration, frequency, intensity, severity and recovery        %%
%% According to Hauri et al 2013				%%
%% of a species faced to variable omega aragonite conditions    %%
%% the program needs a 3D file of omega(lon,lat,time) 	        %%
%% at one vertical level or depth-integrated or depth-averaged  %%
%% calculation and give a a netcdf file with the indices        %%
%% in form of maps ready to map                                 %%
%% 								%% 
%% Program by Faycal Kessouri - SCCWRP/UCLA                     %%
%% 05/2018                                                      %%
%% ============================================================ %%
disp(['pH threshold experiment program starts .... on:  ',  datestr(now)])
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
addpath(genpath('/data/project1/minnaho/decapods/'))

%% user can change here:
%% load the grid
%param_threshold_decapod_yearlyfreq

load_grid_ussw1

% loop through years to calculate and save each year as separate file
all_years = 1997:2007;
for y_i=1:size(all_years,2)
disp(['year: ',num2str(all_years(y_i))])
file = '/data/project1/minnaho/decapods/extract_nc/pH_co2sys_L1_100m_slice.nc' ;
% pick year to subsample output
year_select = all_years(y_i);

disp('data reading in progress ... ... ... ')
InputData = ncread(file,'var');
% total time that output file accounts for (daily timestep)
date = datenum(1997,2,1):datenum(2007,11,30);
mmyear = str2num(datestr(date,'mm yyyy'));
% select year and months
list = find(mmyear(:,2)==year_select & mmyear(:,1)>2 & mmyear(:,1)<8);
InputData = squeeze(InputData(:,:,list)) ;

ThresholdMagnitude =  7.75 ;
ThresholdDuration =  30 ;
outPerDay = 1 ;

disp('data ready ')
fout =   ['/data/project1/minnaho/decapods/decapods_nc/yearly_freq/decapods_juvenile_mort_100m_upwell_',num2str(year_select),'.nc'];


per_InputData = permute(InputData,[2 1 3]);
%% loop over each point of the grid
for i=1:NY
disp(['i = ',num2str(i),' of ',num2str(NY)])
for j=1:NX
if mask(i,j)==0 ;
Frequency_yearly(i,j) = NaN;

else
	Frequency_yearly(i,j) = threshold_freq_yearly(ThresholdMagnitude, ThresholdDuration, squeeze(per_InputData(i,j,:))', outPerDay) ;
end
end
end

Frequency_yearly(mask==0)=NaN;

disp('write the nc file...')
% create the ncfile
ncid = netcdf.create(fout,'netcdf4');
% extract the dimensions
  dimY    = netcdf.defDim   (       ncid,   'eta_rho', NY           ) ;
  dimX    = netcdf.defDim   (       ncid,   'xi_rho' , NX           ) ;

% create the variables

% Frequency
F    =  netcdf.defVar(ncid,'Frequency', 'double', [dimY dimX]);
netcdf.putAtt(ncid,F,'units','number of events');
netcdf.putAtt(ncid,F,'long_name','the cumulative frequency (number of events) of events below the ThresholdMagnitude for events longer than ThresholdDuration for each model node');
netcdf.putVar(ncid,F,Frequency_yearly);


 % insert global attribute
NC_GLOBAL = netcdf.getConstant('NC_GLOBAL');
netcdf.putAtt(ncid,NC_GLOBAL,'title','Decapods thresholds analysis')
netcdf.putAtt(ncid,NC_GLOBAL,'long_title','Decapods thresholds analysis on ROMS L1 California state wide model')
netcdf.putAtt(ncid,NC_GLOBAL,'institution','UCLA/UW/SCCWRP')
netcdf.putAtt(ncid,NC_GLOBAL,'source','roms')
netcdf.putAtt(ncid,NC_GLOBAL,'description',['ThresholdMagnitude = ',num2str(ThresholdMagnitude),', ThresholdDuration = ',num2str(ThresholdDuration)])
netcdf.close(ncid)

end
