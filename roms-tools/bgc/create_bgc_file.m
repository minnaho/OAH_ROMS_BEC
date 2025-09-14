function create_bgc_file(grdname,bgcname,bgctime,pars,BGCparam,t)
%
%   Create ROMS BGC file
% 
%

[nx,ny] = size(ncread(grdname,'h'));

%
%  Create variables
%

disp(['Creating file : ' bgcname])

%nccreate(bgcname,'time','Dimensions',{'time',bgctime},'datatype','double');
nccreate(bgcname,'time','Dimensions',{'time',1},'datatype','double');
ncwriteatt(bgcname,'time','long_name','time since 1 january');
ncwriteatt(bgcname,'time','units','day');
ncwriteatt(bgcname,'time','cycle_length',365.25);
time = [0.5:bgctime] * 365.25/bgctime ; 
ncwrite(bgcname,'time',time(t)) ; 

for n=1:BGCparam.Ntrc
   nccreate(bgcname,BGCparam.name_vars{n},'Dimensions',{'xi_rho',nx,'eta_rho',ny,'s_rho',pars.N,'time',1},'datatype','double');
   ncwriteatt(bgcname,BGCparam.name_vars{n},'long_name',BGCparam.long_name{n});
   ncwriteatt(bgcname,BGCparam.name_vars{n},'units',BGCparam.units{n});
   ncwriteatt(bgcname,BGCparam.name_vars{n},'source',BGCparam.file_vars{n});
end

%
%
%  Write global attributes
%
 ncwriteatt(bgcname,'/','Title','ROMS BGC file');
 ncwriteatt(bgcname,'/','Date',date);
 ncwriteatt(bgcname,'/','gridfile',grdname);
 ncwriteatt(bgcname,'/','theta_s',pars.theta_s);
 ncwriteatt(bgcname,'/','theta_b',pars.theta_b);
 ncwriteatt(bgcname,'/','hc',pars.hc);
%
%
return
