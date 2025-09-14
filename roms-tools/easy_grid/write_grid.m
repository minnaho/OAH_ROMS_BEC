function write_grid(lone,late, lonr,latr, pn,pm, hraw,angle, size_x,size_y, ...
                            cent_lat,taper, alpha, tra_lon,tra_lat, flip_xy);

disp([ 'enter write_grid :: size_x=',num2str(size_x), ...
                          ' size_y=',num2str(size_y),  ...
                        ' cent_lat=',num2str(cent_lat), ...
                           ' taper=',num2str(taper), ...
                         ' tra_lon=',num2str(tra_lon),  ...
                         ' tra_lat=',num2str(tra_lat), ...
                           ' alpha=',num2str(alpha), ...
                         ' flip_xy=',num2str(flip_xy) ])
% Create the grid file

grdname = 'roms_grd.nc';
ncid = netcdf.create(grdname,'64BIT_OFFSET');

% Define dimensions

[xi_rho,eta_rho]=size(lonr);
xi_r_id  = netcdf.defDim(ncid, 'xi_rho',  xi_rho);
eta_r_id = netcdf.defDim(ncid, 'eta_rho', eta_rho);
r2dgrd = [xi_r_id, eta_r_id];

xi_u=xi_rho-1; eta_v=eta_rho-1;
xi_u_id  = netcdf.defDim(ncid, 'xi_u',  xi_u);
eta_v_id = netcdf.defDim(ncid, 'eta_v', eta_v);
p2dgrd = [xi_u_id, eta_v_id];


% Create variables and their attributes

sph_vid=netcdf.defVar(ncid, 'spherical', 'NC_CHAR', []);
netcdf.putAtt(ncid, sph_vid, 'long_name', 'Grid type logical switch');
netcdf.putAtt(ncid, sph_vid, 'option_T', 'spherical');

lon_r_vid=netcdf.defVar(ncid, 'lon_rho', 'NC_DOUBLE', r2dgrd);
netcdf.putAtt(ncid, lon_r_vid, 'long_name','longitude of RHO-points');
netcdf.putAtt(ncid, lon_r_vid, 'units', 'degree East');

lat_r_vid=netcdf.defVar(ncid, 'lat_rho', 'NC_DOUBLE', r2dgrd);
netcdf.putAtt(ncid, lat_r_vid, 'long_name','latitude of RHO-points');
netcdf.putAtt(ncid, lat_r_vid, 'units', 'degree North');

lon_p_vid=netcdf.defVar(ncid, 'lon_psi', 'NC_DOUBLE', p2dgrd);
netcdf.putAtt(ncid, lon_p_vid, 'long_name','longitude of PSI-points');
netcdf.putAtt(ncid, lon_p_vid, 'units', 'degree East');

lat_p_vid=netcdf.defVar(ncid, 'lat_psi', 'NC_DOUBLE', p2dgrd);
netcdf.putAtt(ncid, lat_p_vid, 'long_name','latitude of PSI-points');
netcdf.putAtt(ncid, lat_p_vid, 'units', 'degree North');


pm_vid=netcdf.defVar(ncid, 'pm', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, pm_vid, 'long_name', ...
                   'curvilinear coordinate metric in XI-direction');
netcdf.putAtt(ncid, pm_vid, 'units', 'meter-1');

pn_vid=netcdf.defVar(ncid, 'pn', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, pn_vid, 'long_name', ...
                     'curvilinear coordinate metric in ETA-direction');
netcdf.putAtt(ncid, pn_vid, 'units','meter-1');

ang_vid=netcdf.defVar(ncid, 'angle', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, ang_vid, 'long_name', ...
                              'angle between east and XI-directions');
netcdf.putAtt(ncid, ang_vid, 'units', 'degrees');

f_vid=netcdf.defVar(ncid, 'f', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, f_vid, 'long_name','Coriolis parameter at RHO-points');
netcdf.putAtt(ncid, f_vid, 'units', 'second-1');

hraw_vid=netcdf.defVar(ncid, 'hraw', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, hraw_vid, 'long_name','raw bathymetry at RHO-points');
netcdf.putAtt(ncid, hraw_vid, 'units','meter');

h_vid=netcdf.defVar(ncid, 'h', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, h_vid, 'long_name','model bathymetry at RHO-points');
netcdf.putAtt(ncid, h_vid, 'units','meter');

mask_r_vid=netcdf.defVar(ncid, 'mask_rho', 'NC_DOUBLE',  r2dgrd);
netcdf.putAtt(ncid, mask_r_vid, 'long_name', 'land/sea mask at RHO-points');
netcdf.putAtt(ncid, mask_r_vid, 'units','land/water (0/1)');

% Auxiliary variables to record translation and rotation of the grid.
% ROMS code does not use them, however they may are useful for inverse
% transformation (basically back to lon-lat coordinates), if so desired.

cent_lat_vid=netcdf.defVar(ncid, 'cent_lat', 'NC_DOUBLE',[]);
netcdf.putAtt(ncid, cent_lat_vid, 'long_name', ...
                            'Initial latitude of base grid');
netcdf.putAtt(ncid, cent_lat_vid, 'units', 'degrees North');

taper_vid=netcdf.defVar(ncid, 'tapering', 'NC_DOUBLE',[]);
netcdf.putAtt(ncid, taper_vid, 'long_name', ...
               'East-west tapering parameter of base grid');
netcdf.putAtt(ncid, taper_vid, 'units', 'nondimensional');


tra_lat_vid=netcdf.defVar(ncid, 'tra_lat', 'NC_DOUBLE', []);
netcdf.putAtt(ncid, tra_lat_vid, 'long_name', ...
                    'Latitudinal translation of base grid');
netcdf.putAtt(ncid, tra_lat_vid, 'units', 'degree North');

tra_lon_vid=netcdf.defVar(ncid, 'tra_lon', 'NC_DOUBLE', []);
netcdf.putAtt(ncid, tra_lon_vid, 'long_name', ...
                   'Longitudinal translation of base grid');
netcdf.putAtt(ncid, tra_lon_vid, 'units','degree East');


rotate_vid=netcdf.defVar(ncid, 'rotate', 'NC_DOUBLE', []);
netcdf.putAtt(ncid, rotate_vid, 'long_name', ...
                                   'Rotation of base grid');
netcdf.putAtt(ncid, rotate_vid, 'units','degree');

flip_xy_vid=netcdf.defVar(ncid, 'flip_xy', 'NC_DOUBLE', []);
netcdf.putAtt(ncid, flip_xy_vid, 'long_name', ...
                          '90-degree turn of logical grid');
netcdf.putAtt(ncid, flip_xy_vid, 'units', ...
                  '0 = none; 1 = counter-; 2 = clock-wise');

%% Global attributes

if (flip_xy > 0)
  jj=xi_rho-2; ii=eta_rho-2;   %% <-- reverse order
else
  ii=xi_rho-2; jj=eta_rho-2;
end

settings = ['nx=',num2str(ii),             ' ny=',num2str(jj), ...
       ' size_x=',num2str(size_x/1e3), ' size_y=',num2str(size_y/1e3), ...
     ' cent_lat=',num2str(cent_lat), ' tapering=',num2str(taper), ... 
          ' Lat=',num2str(tra_lat),       ' Lon=',num2str(tra_lon), ...
       ' rotate=',num2str(alpha),     ' flip_xy=',num2str(flip_xy)];

varid=netcdf.getConstant('GLOBAL');
netcdf.putAtt(ncid, varid, 'Title', 'ROMS grid produced by Easy Grid');
netcdf.putAtt(ncid, varid, 'Settings', settings);
netcdf.putAtt(ncid, varid, 'Date', date);

netcdf.endDef(ncid);  %% <-- complete file definition

%% Fill the file with data

disp('writing spherical...')
netcdf.putVar(ncid, sph_vid, 'T');

pi=3.14159265358979323846; rad2deg=180/pi;
disp(['writing lon_r, size = ', num2str(size(latr))])
netcdf.putVar(ncid, lon_r_vid, rad2deg*lonr); %% <-- convert to degrees

disp(['writing lat_r, size = ', num2str(size(latr))])
netcdf.putVar(ncid, lat_r_vid, rad2deg*latr); %% <-- convert to degrees

tmp_p=zeros(xi_u,eta_v);
tmp_p=rad2deg*lone(2:xi_u+1,2:eta_v+1);
disp(['writing lon_p, size of lonp = ',num2str(size(tmp_p))])
netcdf.putVar(ncid, lon_p_vid, tmp_p);

tmp_p=rad2deg*late(2:xi_u+1,2:eta_v+1);
disp(['writing lat_p, size of latp = ',num2str(size(tmp_p))])
netcdf.putVar(ncid, lat_p_vid, tmp_p);
clear tmp_p;

disp(['writing pm, size = ', num2str(size(pm))])
netcdf.putVar(ncid, pm_vid, pm);

disp(['writing pn, size = ', num2str(size(pn))])
netcdf.putVar(ncid, pn_vid, pn);

disp(['writing angle, size = ', num2str(size(angle))])
netcdf.putVar(ncid, ang_vid, rad2deg*angle);


f=4*pi*sin(latr)/(23.9344699*3600); %% <-- 4*pi/T where T is SIDEREAL day
disp(['writing f, size = ', num2str(size(f))])
netcdf.putVar(ncid, f_vid, f);
clear f;

disp(['writing hraw, size = ', num2str(size(hraw))])
netcdf.putVar(ncid, hraw_vid, hraw);

mask = ones(xi_rho,eta_rho);  %%  Compute land mask
mask(hraw > 0) = 0;
disp(['writing mask_rho, size = ', num2str(size(mask))])
netcdf.putVar(ncid, mask_r_vid, mask);
clear mask;

% Auxiliary variables

netcdf.putVar(ncid, cent_lat_vid, cent_lat);
netcdf.putVar(ncid, taper_vid,    taper);
netcdf.putVar(ncid, tra_lon_vid,  tra_lon);
netcdf.putVar(ncid, tra_lat_vid,  tra_lat);
netcdf.putVar(ncid, rotate_vid,   alpha);
netcdf.putVar(ncid, flip_xy_vid,  flip_xy);

disp('closing file...')
netcdf.close(ncid)
disp('done write_grid')
