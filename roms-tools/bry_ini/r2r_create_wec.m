function r2r_create_wec(inifile,gridfile,parfile)
%
%   Input: 
% 
%   inifile      Netcdf initial file name (character string).
%   gridfile     Netcdf grid file name (character string).
%   parfile      Netcdf parent file name (string); needed for
%                for length of time index
%                
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%  Read the grid file
%
h       = ncread(gridfile,'h')';
%tdim    = size(ncread(parfile,'wwv_time'));
%tdim    = tdim(1);
[Mp,Lp] = size(h);

nccreate(inifile,'wwv_time','Dimensions',{'wwv_time',0},'datatype','single');
ncwriteatt(inifile,'wwv_time','long_name','surface gravity wave time');
ncwriteatt(inifile,'wwv_time','units','days');

nccreate(inifile,'Awave','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'Awave','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'Awave','units','meter');

% converted to correct angle and radians in wec code
nccreate(inifile,'Dwave','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'Dwave','long_name','clockwise mean wind wave direction from true north');
ncwriteatt(inifile,'Dwave','units','degree');

nccreate(inifile,'Pwave','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'Pwave','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'Pwave','units','meter');

nccreate(inifile,'uorb','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'uorb','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'uorb','units','meter');

nccreate(inifile,'vorb','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'vorb','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'vorb','units','meter');

nccreate(inifile,'ust2d','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'ust2d','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'ust2d','units','meter');

nccreate(inifile,'vst2d','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'vst2d','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'vst2d','units','meter');

nccreate(inifile,'ust0','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'ust0','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'ust0','units','meter');

nccreate(inifile,'vst0','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'vst0','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'vst0','units','meter');

nccreate(inifile,'ed','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'ed','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'ed','units','meter');

nccreate(inifile,'eb','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'eb','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'eb','units','meter');

nccreate(inifile,'qb','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'qb','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'qb','units','meter');

nccreate(inifile,'sup','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'sup','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'sup','units','meter');

nccreate(inifile,'lmw','Dimensions',{'xi_rho',Lp,'eta_rho',Mp,'wwv_time'},'datatype','single');
ncwriteatt(inifile,'lmw','long_name','mean wind wave amplitude (Hsig/2/sqrt(2))');
ncwriteatt(inifile,'lmw','units','meter');

%
%  Write global attributes
%
 ncwriteatt(inifile,'/','Title',['R2R initial file for' gridfile]);
 ncwriteatt(inifile,'/','Date',date);

return


