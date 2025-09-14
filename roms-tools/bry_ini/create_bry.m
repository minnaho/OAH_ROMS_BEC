function create_bry(bryname,grdname,obcflag,param);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   function l2r_create_bry(bryname,grdname,obcflag,...
%                          chdscd,cycle)
%
%   Input:
%
%   bryname      Netcdf climatology file name (character string)
%   grdname      Netcdf grid file name (character string)
%   obcflag      open boundary flag (1=open, [S E N W])
%   chdscd       S-coordinate parameters (object)
%   cycle        Length (days) for cycling the climatology (real)

%
%
% get S-coordinate parameters
%
theta_b = param.theta_b;
theta_s = param.theta_s;
hc      = param.hc;
N       = param.N;
%
%
%  Read the grid file and check the topography
%
[nx,ny] = size(ncread(grdname,'h'));
%
%  Create the boundary file
%
nccreate(bryname,'bry_time','Dimensions',{'time',0},'datatype','single');
ncwriteatt(bryname,'bry_time','long_name','time for boundary data');
ncwriteatt(bryname,'bry_time','units','days');
%
if obcflag(1)==1  %%   Southern boundary
%
  nccreate(bryname,'temp_south','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'temp_south','long_name','southern boundary potential temperature');
  ncwriteatt(bryname,'temp_south','units','Celsius');
%
  nccreate(bryname,'salt_south','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'salt_south','long_name','southern boundary salinity');
  ncwriteatt(bryname,'salt_south','units','PSU');
%
  nccreate(bryname,'u_south','Dimensions',{'xi_u',nx-1,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'u_south','long_name','southern boundary u-momentum component');
  ncwriteatt(bryname,'u_south','units','meter second-1');
%
  nccreate(bryname,'v_south','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'v_south','long_name','southern boundary v-momentum component');
  ncwriteatt(bryname,'v_south','units','meter second-1');
%
  nccreate(bryname,'ubar_south','Dimensions',{'xi_u',nx-1,'time',0},'datatype','single');
  ncwriteatt(bryname,'ubar_south','long_name','southern boundary vertically integrated u-momentum component');
  ncwriteatt(bryname,'ubar_south','units','meter second-1');
%
  nccreate(bryname,'vbar_south','Dimensions',{'xi_rho',nx,'time',0},'datatype','single');
  ncwriteatt(bryname,'vbar_south','long_name','southern boundary vertically integrated v-momentum component');
  ncwriteatt(bryname,'vbar_south','units','meter second-1');
%
  nccreate(bryname,'zeta_south','Dimensions',{'xi_rho',nx,'time',0},'datatype','single');
  ncwriteatt(bryname,'zeta_south','long_name','southern boundary sea surface height');
  ncwriteatt(bryname,'zeta_south','units','meter');
end
%
%
if obcflag(2)==1  %%   Eastern boundary
%
  nccreate(bryname,'temp_east','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'temp_east','long_name','eastern boundary potential temperature');
  ncwriteatt(bryname,'temp_east','units','Celsius');
%
  nccreate(bryname,'salt_east','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'salt_east','long_name','eastern boundary salinity');
  ncwriteatt(bryname,'salt_east','units','PSU');
%
  nccreate(bryname,'u_east','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'u_east','long_name','eastern boundary u-momentum component');
  ncwriteatt(bryname,'u_east','units','meter second-1');
%
  nccreate(bryname,'v_east','Dimensions',{'eta_v',ny-1,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'v_east','long_name','eastern boundary v-momentum component');
  ncwriteatt(bryname,'v_east','units','meter second-1');
%
  nccreate(bryname,'ubar_east','Dimensions',{'eta_rho',ny,'time',0},'datatype','single');
  ncwriteatt(bryname,'ubar_east','long_name','eastern boundary vertically integrated u-momentum component');
  ncwriteatt(bryname,'ubar_east','units','meter second-1');
%
  nccreate(bryname,'vbar_east','Dimensions',{'eta_v',ny-1,'time',0},'datatype','single');
  ncwriteatt(bryname,'vbar_east','long_name','eastern boundary vertically integrated v-momentum component');
  ncwriteatt(bryname,'vbar_east','units','meter second-1');
%
  nccreate(bryname,'zeta_east','Dimensions',{'eta_rho',ny,'time',0},'datatype','single');
  ncwriteatt(bryname,'zeta_east','long_name','eastern boundary sea surface height');
  ncwriteatt(bryname,'zeta_east','units','meter');
end
%
if obcflag(3)==1  %%   Northern boundary
%
  nccreate(bryname,'temp_north','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'temp_north','long_name','northern boundary potential temperature');
  ncwriteatt(bryname,'temp_north','units','Celsius');
%
  nccreate(bryname,'salt_north','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'salt_north','long_name','northern boundary salinity');
  ncwriteatt(bryname,'salt_north','units','PSU');
%
  nccreate(bryname,'u_north','Dimensions',{'xi_u',nx-1,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'u_north','long_name','orthern boundary u-momentum component');
  ncwriteatt(bryname,'u_north','units','meter second-1');
%
  nccreate(bryname,'v_north','Dimensions',{'xi_rho',nx,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'v_north','long_name','northern boundary v-momentum component');
  ncwriteatt(bryname,'v_north','units','meter second-1'); 
%
  nccreate(bryname,'ubar_north','Dimensions',{'xi_u',nx-1,'time',0},'datatype','single');
  ncwriteatt(bryname,'ubar_north','long_name','northern boundary vertically integrated u-momentum component');
  ncwriteatt(bryname,'ubar_north','units','meter second-1');
%
  nccreate(bryname,'vbar_north','Dimensions',{'xi_rho',nx,'time',0},'datatype','single');
  ncwriteatt(bryname,'vbar_north','long_name','northern boundary vertically integrated v-momentum component');
  ncwriteatt(bryname,'vbar_north','units','meter second-1');
%
  nccreate(bryname,'zeta_north','Dimensions',{'xi_rho',nx,'time',0},'datatype','single');
  ncwriteatt(bryname,'zeta_north','long_name','northern boundary sea surface height');
  ncwriteatt(bryname,'zeta_north','units','meter');
end
%
if obcflag(4)==1  %%   Western boundary
% 
  nccreate(bryname,'temp_west','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'temp_west','long_name','western boundary potential temperature');
  ncwriteatt(bryname,'temp_west','units','Celsius');
%
  nccreate(bryname,'salt_west','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'salt_west','long_name','western boundary salinity');
  ncwriteatt(bryname,'salt_west','units','PSU');
%
  nccreate(bryname,'u_west','Dimensions',{'eta_rho',ny,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'u_west','long_name','western boundary u-momentum component');
  ncwriteatt(bryname,'u_west','units','meter second-1');
%
  nccreate(bryname,'v_west','Dimensions',{'eta_v',ny-1,'s_rho',N,'time',0},'datatype','single');
  ncwriteatt(bryname,'v_west','long_name','western boundary v-momentum component');
  ncwriteatt(bryname,'v_west','units','meter second-1');
%
  nccreate(bryname,'ubar_west','Dimensions',{'eta_rho',ny,'time',0},'datatype','single');
  ncwriteatt(bryname,'ubar_west','long_name','western boundary vertically integrated u-momentum component');
  ncwriteatt(bryname,'ubar_west','units','meter second-1');
%
  nccreate(bryname,'vbar_west','Dimensions',{'eta_v',ny-1,'time',0},'datatype','single');
  ncwriteatt(bryname,'vbar_west','long_name','western boundary vertically integrated v-momentum component');
  ncwriteatt(bryname,'vbar_west','units','meter second-1');
%
  nccreate(bryname,'zeta_west','Dimensions',{'eta_rho',ny,'time',0},'datatype','single');
  ncwriteatt(bryname,'zeta_west','long_name','western boundary sea surface height');
  ncwriteatt(bryname,'zeta_west','units','meter');
end
%
%
% Create global attributes
%
 ncwriteatt(bryname,'/','Title',['Boundary file for' grdname]);
 ncwriteatt(bryname,'/','Date',date);
 ncwriteatt(bryname,'/','type','BOUNDARY file');
 ncwriteatt(bryname,'/','theta_s',theta_s);
 ncwriteatt(bryname,'/','theta_b',theta_b);
 ncwriteatt(bryname,'/','hc',hc);










