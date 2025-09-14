clear all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Make a ROMS boundary forcing file.
%  Designed for MERCATOR-GLORYS products
%
%%%%%%%%%%%%%%%%%%%%% USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%%%
%
%  bry climatology file names:
bry_root = '/data/project7/pdamien/DATA/GLORYS12V1/';
bry_name = 'glorys12v1' ;  

% Set a date range for the forcing file
start_date = datenum(2015,01,01);
end_date   = datenum(2015,12,31);

grdname  = '/data/project3/pdamien/ROMS_pdamien/config/pacmed_0p25/grid/pacmed_0p25_grd_corrected.nc';
root_name= '/data/project3/pdamien/ROMS_pdamien/config/pacmed_0p25/out_NEW/pacmedTEST';

pars.theta_s = 6.0;
pars.theta_b = 6.0;
pars.hc     = 250.0;
pars.N      = 100;
pars.scoord = 'new2012';    % child 'new' or 'old' type scoord

obcflag        = [1 1 1 1];    % open boundaries flag (1=open , [S E N W])
time_ref = datenum(1995,1,1) ; % reference time for ROMS

intrp.tri_interp = 1 ; % if tri_interp==1, interpolation is done trough triangulation with 
                 %                   pre-computed coefficients. 
                 % if tri_interp==0, interpolation is done trough interp2
intrp.coefs_dir = 'Coefs_pacmed25km' ; % to store precomputed coefs when tri_interp==1 
intrp.method = 'Makima' ;              % Interpolation method with interp2
%
%%%%%%%%%%%%%%%%%%% END USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%

% make one bry file per year
  start_year = str2num(datestr(start_date,'YYYY')) ;   
  end_year = str2num(datestr(end_date,'YYYY')) ;

for yy=start_year:end_year

   disp(['Working on year ' num2str(yy)])

   frclist = dir([bry_root bry_name '*' num2str(yy) '*.nc']);
   nfiles = length(frclist);

   % time
   stime = zeros(nfiles,1);
   for i=1:nfiles
     datname = [frclist(i).folder '/' frclist(i).name];
     ncid = netcdf.open(datname,'nowrite');
     try
        ID = netcdf.inqVarID(ncid,'time');
     catch exception
        if strcmp(exception.identifier,'MATLAB:imagesci:netcdf:libraryFailure')
           index=strfind(datname,'Y') ;
           stime(i) = datenum(str2num(datname(index(end)+1:index(end)+4)), ...
                              str2num(datname(index(end)+6:index(end)+7)),...
                              str2num(datname(index(end)+9:index(end)+10))) + 0.5 ;
        end
      end
      netcdf.close(ncid)
      if stime(i)==0
         stime(i) = double(ncread(datname,'time',[1],[1]))/24 + datenum(1950,1,1);
      end
   end

   % grids
   datname = [frclist(1).folder '/' frclist(1).name];
   lon_frc = ncread(datname,'longitude');
   lat_frc = ncread(datname,'latitude');
   nx_frc = length(lon_frc);
   ny_frc = length(lat_frc);

   [nx,ny] = size(ncread(grdname,'h')); 

   create_obcs

   if intrp.tri_interp==1
      compute_interp_coefs
   end
 
   bry_file = [root_name '_bry.' num2str(yy) '.nc']
   if exist(bry_file)
      delete(bry_file)
   end
   disp('Creating boundary file: ');
   disp(bry_file)
   create_bry(bry_file,grdname,obcflag,pars);
   disp('Done')

   time2wr = double(stime) - time_ref ;
   ncwrite(bry_file,'bry_time',time2wr);

   %% loop over time
%   for irec = 1:nfiles
   for irec = 1:1

        if mod(irec,5)==0
        disp(['Record: ' num2str(irec)])
        end
        datname = [frclist(irec).folder '/' frclist(irec).name];

        for bnd = 1:4

            if ~obcflag(bnd)
            continue
            end

            if intrp.tri_interp==1
               load([intrp.coefs_dir '/s2r_' obcs(bnd).suffix '.mat'])
               intrp.coef2d = coef2d ; intrp.elem2d = elem2d ; 
            end

            % Zeta
            zeta = get_2Dbry_glorys(datname,obcs(bnd),'zos',intrp);
            ncwrite(bry_file,['zeta_' obcs(bnd).suffix],zeta,[1 irec]);
            
            % Temperature
            temp = get_3Dbry_glorys(datname,obcs(bnd),'thetao',intrp,pars);
            ncwrite(bry_file,['temp_' obcs(bnd).suffix],temp,[1 1 irec]);
   
            % Salinity
            salt = get_3Dbry_glorys(datname,obcs(bnd),'so',intrp,pars);
            ncwrite(bry_file,['salt_' obcs(bnd).suffix],salt,[1 1 irec]);

            % Velocities
            u = get_3Dbry_glorys(datname,obcs(bnd),'uo',intrp,pars);
            v = get_3Dbry_glorys(datname,obcs(bnd),'vo',intrp,pars);
                % Rotate to grid orientation and put to staggered u/v points  
                cosa = cos(obcs(bnd).angc(obcs(bnd).wi0:obcs(bnd).wi1,obcs(bnd).wj0:obcs(bnd).wj1)); 
                sina = sin(obcs(bnd).angc(obcs(bnd).wi0:obcs(bnd).wi1,obcs(bnd).wj0:obcs(bnd).wj1));
                us = u.*0 ; vs = v.*0 ;
                for z=1:pars.N 
                    us(:,:,z) = squeeze(u(:,:,z)).*cosa + squeeze(v(:,:,z)).*sina;
                    vs(:,:,z) = squeeze(v(:,:,z)).*cosa - squeeze(u(:,:,z)).*sina;
                end
                u = squeeze( 0.5.*(us(1:end-1,obcs(bnd).wj0:obcs(bnd).wj1,:) +...
                                   us(2:end  ,obcs(bnd).wj0:obcs(bnd).wj1,:))) ; 
                v = squeeze( 0.5.*(vs(obcs(bnd).wi0:obcs(bnd).wi1,1:end-1,:) +...
                                   vs(obcs(bnd).wi0:obcs(bnd).wi1,2:end  ,:))) ;
                % Get barotropic velocity
                dzu = squeeze( 0.5.*(obcs(bnd).dz(1:end-1,obcs(bnd).wj0:obcs(bnd).wj1,:) +...
                                     obcs(bnd).dz(2:end  ,obcs(bnd).wj0:obcs(bnd).wj1,:))) ; 
                dzv = squeeze( 0.5.*(obcs(bnd).dz(obcs(bnd).wi0:obcs(bnd).wi1,1:end-1,:) +...
                                     obcs(bnd).dz(obcs(bnd).wi0:obcs(bnd).wi1,2:end  ,:))) ;
                ubar = sum(dzu.*u,2)./sum(dzu,2) ; 
                vbar = sum(dzv.*v,2)./sum(dzv,2) ;
            ncwrite(bry_file,['ubar_' obcs(bnd).suffix],ubar,[1 irec]);
            ncwrite(bry_file,['vbar_' obcs(bnd).suffix],vbar,[1 irec]);
            ncwrite(bry_file,['u_' obcs(bnd).suffix],u,[1 1 irec]);
            ncwrite(bry_file,['v_' obcs(bnd).suffix],v,[1 1 irec]);

        end
        toc
   end



end
