function create_bgcflx(bgcname,grdname,BGCparam,n,bgctime)
%               
%   Create ROMS BGC file
% 
%

[nx,ny] = size(ncread(grdname,'lon_rho'));

%
%  Create variables
%

if strcmp(BGCparam.name_vars{n},'pco2_air')

nccreate(bgcname,'pco2_time','Dimensions',{'ptime',bgctime},'datatype','double');
ncwriteatt(bgcname,'pco2_time','long_name','time since ref ROMS time');
ncwriteatt(bgcname,'pco2_time','units','day');

nccreate(bgcname,'pco2_air','Dimensions',{'xi_rho',nx,'eta_rho',ny,'ptime',bgctime},'datatype','single');
ncwriteatt(bgcname,'pco2_air','long_name',BGCparam.long_name{n});
ncwriteatt(bgcname,'pco2_air','units',BGCparam.units{n});
ncwriteatt(bgcname,'pco2_air','source',BGCparam.file_vars{n});

elseif strcmp(BGCparam.name_vars{n},'dust')

nccreate(bgcname,'dust_time','Dimensions',{'dtime',bgctime},'datatype','double');
ncwriteatt(bgcname,'dust_time','long_name','time since ref ROMS time');
ncwriteatt(bgcname,'dust_time','units','day');

nccreate(bgcname,'dust','Dimensions',{'xi_rho',nx,'eta_rho',ny,'dtime',bgctime},'datatype','single');
ncwriteatt(bgcname,'dust','long_name',BGCparam.long_name{n});
ncwriteatt(bgcname,'dust','units',BGCparam.units{n});
ncwriteatt(bgcname,'dust','source',BGCparam.file_vars{n});

elseif strcmp(BGCparam.name_vars{n},'iron')

nccreate(bgcname,'iron_time','Dimensions',{'itime',bgctime},'datatype','double');
ncwriteatt(bgcname,'iron_time','long_name','time since ref ROMS time');
ncwriteatt(bgcname,'iron_time','units','day');

nccreate(bgcname,'iron','Dimensions',{'xi_rho',nx,'eta_rho',ny,'itime',bgctime},'datatype','single');
ncwriteatt(bgcname,'iron','long_name',BGCparam.long_name{n});
ncwriteatt(bgcname,'iron','units',BGCparam.units{n});
ncwriteatt(bgcname,'iron','source',BGCparam.file_vars{n});

else

  disp('ERROR Variable does not exist in create_bgcflx')
  error

end






%
%
%  Write global attributes
%
 ncwriteatt(bgcname,'/','Title','ROMS BGC file');
 ncwriteatt(bgcname,'/','Date',date);
 ncwriteatt(bgcname,'/','gridfile',grdname);
%
%
return
