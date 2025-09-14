
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Make a ROMS bulk forcing file using hourly data Atmospheric data.
%  Choice of ERA5 (25km), IFS (9km), or HRRR (3km)  (USA coastal regions only)
%
%  2020-2024, Jeroen Molemaker, Pierre Damien, UCLA
%
%
%%%%%%%%%%%%%%%%%%%%% USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%%%
%
%  frc climatology file names:
frc_root = '/data/project5/pdamien/DATA/ERA5/';

frc_source = 'ERA5';  % ERA5/IFS/HRRR

% Set a date range for the forcing file
start_date = datenum(2012,08,01);
end_date   = datenum(2021,01,31);

grdname  = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_grd.nc';
root_name= '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed' ;

% Only needed in case of wind_dropoff=1
disname  = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_cdist.mat';

coarse_frc   = 0; % forcing files at half the resolution of the grid
rad_corr     = 1; % Multiplicative correction of swr and lwr to observations

wind_dropoff = 1; % Spatial field to represent coastal wind dropoff 
add_rivers   = 0; % Adds river runoff as additional precipitation (obsolete)

dateref = datenum(1995,1,1) ;  %ROMS reference time
%
%%%%%%%%%%%%%%%%%%% END USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%

switch frc_source
  case 'ERA5'
    disp('Using ERA5 atmospheric data')
    dsatt = 'ERA5 (25 km nominal res)';

    frc_dir = [frc_root '1hourly/'];
    maskname = [frc_root 'ERA5_mask.nc'];
    rcorname = [frc_root 'SSR_correction.nc'];
    fill_frc_ecnwf
  case 'IFS'
    disp('Using IFS atmospheric data')
    dsatt = 'IFS (9 km nominal res)';

    frc_dir = [frc_root 'IFS/'];
%    rcorname = [frc_dir 'IFS_rad_cor.nc'];
    rcorname = [frc_dir 'IFS_rad_cor_core.nc'];
    maskname = [frc_dir 'IFS_mask.nc'];
    fill_frc_ecnwf
  case 'HRRR'
    disp('Using HRRR atmospheric data')

    frc_dir = [frc_root 'HRRR/'];
    swcorrname = [frc_dir 'none'];
    fill_frc_hrrr
  otherwise
    disp('Unknown atmospheric data source')
end
