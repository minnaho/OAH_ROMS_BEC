function create_frc_srfflx(frcfile,grdname,var,coarse_frc)
%               
%   Create ROMS SRF file
% 
%

if coarse_frc
  [nx,ny] = size(ncread(grdname,'h_coarse'));
else
  [nx,ny] = size(ncread(grdname,'h'));
end

%
%  Create variables
%

if var==1
nccreate(frcfile,'sss_time','Dimensions',{'time',12},'datatype','double');
ncwriteatt(frcfile,'sss_time','long_name','time');
ncwriteatt(frcfile,'sss_time','units','day');

nccreate(frcfile,'sss','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',12},'datatype','single');
ncwriteatt(frcfile,'sss','long_name','Sea surface Salinity');
ncwriteatt(frcfile,'sss','units','PSU');
ncwriteatt(frcfile,'sss','note','From WOA; 1955-2017');
end

if var==2
nccreate(frcfile,'Taucorr_time','Dimensions',{'time',12},'datatype','double');
ncwriteatt(frcfile,'Taucorr_time','long_name','time');
ncwriteatt(frcfile,'Taucorr_time','units','day');

nccreate(frcfile,'TauX_corr','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',12},'datatype','single');
ncwriteatt(frcfile,'TauX_corr','long_name','TauX additive correction');
ncwriteatt(frcfile,'TauX_corr','units','N.m-2');
ncwriteatt(frcfile,'TauX_corr','note','Homemade to match SCOW stress');

nccreate(frcfile,'TauY_corr','Dimensions',{'xi_rho',nx,'eta_rho',ny,'time',12},'datatype','single');
ncwriteatt(frcfile,'TauY_corr','long_name','TauY additive correction');
ncwriteatt(frcfile,'TauY_corr','units','N.m-2');
ncwriteatt(frcfile,'TauY_corr','note','Homemade to match SCOW stress');
end

%
%
%  Write global attributes
%
 ncwriteatt(frcfile,'/','Title','ROMS SRF field');
 ncwriteatt(frcfile,'/','Date',date);
 ncwriteatt(frcfile,'/','gridfile',grdname);
%
%
%
return
