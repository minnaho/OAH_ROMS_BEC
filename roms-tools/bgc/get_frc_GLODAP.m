 function var = get_frc_GLODAP(grd,BGCparam,n,t,bgctime,bgcname)

 interp_density=1 ; 
 meandens_ref = 'WOA' ; % options: WOA/GLODAP

 file = BGCparam.file_vars{n} ; 
 disp(['    --> Working on file : ' file])
 if interp_density==1 
 disp('     --> monthly interpolation on density space')
 if strcmp(meandens_ref,'GLODAP')==1
 file_temp = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/GLODAPv2.2016b.temperature.nc' ; 
 file_salt = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/GLODAPv2.2016b.salinity.nc' ;
 elseif strcmp(meandens_ref,'WOA')==1
 file_temp = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/WOA_to_GLODAPv2.temp.nc' ;
 file_salt = '/data/project7/pdamien/DATA/BGC/GLODAP/GLODAPv2.2016b_MappedClimatologies/WOA_to_GLODAPv2.salt.nc' ;
 else
 disp('       ERROR : define the salt/temp reference to compute density')
 error
 end
 end

   lon0 = min(grd.lon(:));
   lon1 = max(grd.lon(:));
   lat0 = min(grd.lat(:));
   lat1 = max(grd.lat(:));

 %%% get var, lon, lat, depth
 lon_frc = ncread(file,'lon') ; 
 lat_frc = ncread(file,'lat') ;
 nx_frc = length(lon_frc);
 ny_frc = length(lat_frc);

   % figure out periodic extention of data
   if lon0<min(lon_frc)
     disp('     extending west')
     ext_west = 1;
     i0 = find(lon_frc-360<lon0,1,'last');
   else
     ext_west = 0;
     i0 = find(lon_frc<lon0,1,'last');
   end
   if lon1>max(lon_frc)
     disp('     extending east')
     ext_east = 1;
     i1 = find(lon_frc+360>lon1,1,'first');
   else
     ext_east = 0;
     i1 = find(lon_frc>lon1,1,'first');
   end

   j0 = find(lat_frc<lat0,1,'last');
   j1 = find(lat_frc>lat1,1,'first');
   fny = j1-j0+1;

   if ext_west
     lon_frc= [lon_frc(i0:end)'-360 lon_frc(1:i1)'];
   elseif ext_east
     lon_frc= [lon_frc(i0:end)' lon_frc(1:i1)'+360];
   else
     lon_frc= lon_frc(i0:i1);
   end
   lat_frc = lat_frc(j0:j1);

   depth = ncread(file,'Depth') ;
   nz_frc = length(depth) ; 

 if strcmp(BGCparam.name_vars{n},'DIC')==1
    name_vars='TCO2' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'Alk')==1
    name_vars='TAlk' ;
    factor = 1 ;
 else
    disp(['ERROR : ' BGCparam.name_vars{n} ' Not coded in get_frc_GLODAP'])
 end

     if ext_west | ext_east
       fnx1 = nx_frc-i0+1;
       fnx2 = i1;
       vars1 = ncread(file,name_vars,[i0 j0 1],[fnx1 fny inf]);
       vars2 = ncread(file,name_vars,[1  j0 1],[fnx2 fny inf]);
       vars = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]);
       if ( interp_density==1 ) 
       vars1 = ncread(file_temp,'temperature',[i0 j0 1],[fnx1 fny inf]);
       vars2 = ncread(file_temp,'temperature',[1  j0 1],[fnx2 fny inf]);
       temp_frc = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]); 
       vars1 = ncread(file_salt,'salinity',[i0 j0 1],[fnx1 fny inf]);
       vars2 = ncread(file_salt,'salinity',[1  j0 1],[fnx2 fny inf]);
       salt_frc = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]);
       end
    else
       fnx = i1-i0+1;
       vars = ncread(file,name_vars,[i0 j0 1],[fnx fny inf]);
       if ( interp_density==1 )
       temp_frc = ncread(file_temp,'temperature',[i0 j0 1],[fnx fny inf]);
       salt_frc = ncread(file_salt,'salinity',[i0 j0 1],[fnx fny inf]);
       end
     end


 %%% inpaint mask & ascending order
 disp('    --> Inpaint NaNs & ascending order')
 nx_frc = length(lon_frc);
 ny_frc = length(lat_frc);
 [lon_frc,lat_frc] = meshgrid(lon_frc,lat_frc);
 vari= zeros(nz_frc,ny_frc,nx_frc);
 zi  = zeros(nz_frc,ny_frc,nx_frc);
 for z=1:nz_frc
     vari(nz_frc+1-z,:,:) = inpaint_nans( squeeze(vars(:,:,z))' , 2 ) ;
%     vari(nz_frc+1-z,:,:) = squeeze(vars(:,:,z))' ;
     if ( interp_density==1 )
        zi  (nz_frc+1-z,:,:) = -inpaint_nans(sw_dens0(squeeze(salt_frc(:,:,z))',squeeze(temp_frc(:,:,z))'),2) ;
%        zi  (nz_frc+1-z,:,:) = - sw_dens0(squeeze(salt_frc(:,:,z))',squeeze(temp_frc(:,:,z))') ;
     else
        zi  (nz_frc+1-z,:,:) = -depth(z) ;
     end
 end

 %%% read density in bgc file for vertical interpolation 
 if interp_density==1
    salt = ncread(bgcname,'salt',[1 1 1 1],[inf inf inf 1]) ; 
    temp = ncread(bgcname,'temp',[1 1 1 1],[inf inf inf 1]) ;
    dens = -permute(sw_dens0(salt,temp),[3 2 1]) ;
    %%% Fix for surface and bottom density mismatch
    zi  (nz_frc,:,:) = zi  (nz_frc,:,:)+100 ; 
    zi  (1,:,:) = zi  (1,:,:)-100 ;
 end

 %%% Compute or retrieve interpolation coefs through triangulation
  fcoef_glodap = [BGCparam.coefs_dir '/s2r_Glodap_' BGCparam.name_vars{n} '.mat'] ;
  dummy_mask = squeeze(vari(end,:,:)) ; dummy_mask(dummy_mask~=0)=1 ;
  if ( exist(fcoef_glodap,'file') && interp_density==0 )
     disp('    --> Reading interpolation coefficients from file');
     load(fcoef_glodap)
  else
     tic
     disp('    --> Computing interpolation coefficients');
     [elem2d,coef2d,nnel] = get_tri_coef(double(lon_frc),double(lat_frc), ...
                          grd.lon,grd.lat,dummy_mask) ;
     if interp_density==1
     A = get_hv_coef(zi, dens, coef2d, elem2d, double(lon_frc), double(lat_frc), grd.lon, grd.lat);
     else
     A = get_hv_coef(zi, grd.zr, coef2d, elem2d, double(lon_frc), double(lat_frc), grd.lon, grd.lat);
     save(fcoef_glodap,'elem2d','coef2d','nnel','A','-v7.3')
     end
     toc
  end

 %%% Do interpolation
  var = reshape(A*reshape(vari,nz_frc*ny_frc*nx_frc,1),grd.nz,grd.ny,grd.nx); 
  var = permute(var,[3 2 1]).*factor ; 

 return
