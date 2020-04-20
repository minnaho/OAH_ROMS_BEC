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
disp(['Omega thereshlod experiment program starts .... on:  ',  datestr(now)])
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))

%% user can change here:
%% load the grid
param_threshold_L1_shelldiss_sever
%% loop over each point of the grid
for i=1:NY
for j=1:NX
	[Duration(i,j), Frequency(i,j), Intensity(i,j), Severity(i,j), Recovery(i,j)] = ...
        Fx_PteropodThresholds_v02(ThresholdMagnitude, ThresholdDuration, squeeze(InputData(i,j,:))', outPerDay) ;
end
end

disp('write the nc file...')
% create the ncfile
ncid = netcdf.create(fout,'netcdf4');
% extract the dimensions
  dimY    = netcdf.defDim   (       ncid,   'eta_rho', NY           ) ;
  dimX    = netcdf.defDim   (       ncid,   'xi_rho' , NX           ) ;
%  dimtime = netcdf.defDim   (       ncid,   'time'   , size(InputData,3) ) ;

% create the variables
% Duration
D    =  netcdf.defVar(ncid,'Duration', 'double', [dimY dimX]);
netcdf.putAtt(ncid,D,'units','days');
netcdf.putAtt(ncid,D,'long_name','cumulative duration (days) of events below the Threshold Magnitude for events longer than Threshold Duration for each model node');
netcdf.putVar(ncid,D,Duration);

% Recovery
R    =  netcdf.defVar(ncid,'Recovery', 'double', [dimY dimX]);
netcdf.putAtt(ncid,R,'units','days');
netcdf.putAtt(ncid,R,'long_name','the average recovery period (days) between adverse events');
netcdf.putVar(ncid,R,Recovery);

% Frequency
F    =  netcdf.defVar(ncid,'Frequency', 'double', [dimY dimX]);
netcdf.putAtt(ncid,F,'units','number of events');
netcdf.putAtt(ncid,F,'long_name','the cumulative frequency (number of events) of events below the ThresholdMagnitude for events longer than ThresholdDuration for each model node');
netcdf.putVar(ncid,F,Frequency);

% Intensity
I    =  netcdf.defVar(ncid,'Intensity', 'double', [dimY dimX]);
netcdf.putAtt(ncid,I,'units','omega unit');
netcdf.putAtt(ncid,I,'long_name','the mean value of Omega-aragonite of events below the ThresholdMagnitude for events longer than the ThresholdDuration for each model node (Hauri et al 2013 eqn 1)');
netcdf.putVar(ncid,I,Intensity);

% Severity
S    =  netcdf.defVar(ncid,'Severity', 'double', [dimY dimX]);
netcdf.putAtt(ncid,S,'units','no unit');
netcdf.putAtt(ncid,S,'long_name','the product of Intensity and Duration for each model node (Hauri et al eqn 2)');
netcdf.putVar(ncid,S,Severity);


 % insert global attribute
  NC_GLOBAL = netcdf.getConstant('NC_GLOBAL');
netcdf.putAtt(ncid,NC_GLOBAL,'title','Pterpods thresholds analysis')
netcdf.putAtt(ncid,NC_GLOBAL,'long_title','Pterpods thresholds analysis on ROMS L1 California state wide model')
netcdf.putAtt(ncid,NC_GLOBAL,'institution','UCLA/UW/SCCWRP')
netcdf.putAtt(ncid,NC_GLOBAL,'source','roms')


