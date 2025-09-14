%  Generates the i,j locations of data extraction objects
%  for use as boundary forcing in a subsequent nested grid
%
%  Writes to netcdf file the i and j locations of the places 
%  from where we want to save data. Index locations are in [0,nx], [0,ny]
%  
%  It writes a data extraction object for each set of i,j points; each boundary
%  has 3 different objects, for rho,u, and v-points. The velocity objects
%  also include and angle to which the desired velocties will be rotated
%
%  If the child grid point is not in the parent domain it is given a value
%  of -1e5 
%
%  Note the mod statements for lonc and lonp. This is an attempt to deal
%  with parent and child longitudes that are possibly 360 apart
%  It will fail for grids that straddle the dateline of the zero meridian
%  In that case, subtract 180 degrees first
%

% -- START USER INPUT ----------
% Parent grid directory and file name
pdir    = '/data/project3/pdamien/ROMS_pdamien/config/KUROSHIO/';
pname   = 'kuroshio600m_grd.nc';
ename   = 'kuroshio600m_edata.nc';

% lon =-110.0;
% lat =  0.0;
% gname = 'tao1'

% lon =-140.0;
% lat =  0.0;
% gname = 'tao2'

% lon =-110.0;
% lat =  0.0;
% gname = 'tao3'

%  lon = -140.0 ;
%  lat = 0.5 ;
%  gname = 'motive1'

% lon = -137.83 ;
% lat = 1.75 ;
% gname = 'motive2'

% lon = -140.0
% lat = 3.0;
% gname = 'motive3'

% lon = 111.5-360;
% lat = 14.0;
% gname = 'SWC1'

% lon = -125.04;
% lat = 35.91;
% gname = 'NOPP'

 lon = -211.96;
 lat = 34.0;
 gname = 'moorK'

lon = lon+360;

% Output file name and info
info  = ['indices for ' gname ' in ' pname ' , location:(' num2str(lon) ';' num2str(lat) ')'];

 period =  600;
 ang = 0;
 mooring_vars = 'zeta, temp, salt, u, v' ;

% -- END USER INPUT ------------

pname = [pdir pname];
ename = [pdir ename];

if 1
 lonp = ncread(pname,'lon_rho');        
 latp = ncread(pname,'lat_rho');
 lonp = mod(lonp,360);
else
 lonp = ncread(pname,'x_rho');        
 latp = ncread(pname,'y_rho');
end

obj_name = gname;
obj_lon = lon; % + 360;
obj_lat = lat;
obj_ang = ang;
obj_msk =   1;
add_object(ename,obj_name,lonp,latp,period,obj_lon,obj_lat,obj_msk,obj_ang);
ncwriteatt(ename,obj_name,'output_vars',mooring_vars);

ncwriteatt(ename, '/', [gname '_info'],  info);           % info on parent and child grid
