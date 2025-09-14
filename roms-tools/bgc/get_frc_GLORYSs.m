 function var = get_frc_GLORYSs(grd,BGCparam,n,t,bgctime)

 chl_corr = 1 ; % apply a correction on chl based on obs
 file_corr = '/data/project7/pdamien/DATA/BGC/GLORYS2V4/CHL_correction.nc' ;  
 if chl_corr == 1 ; 
    disp('       CHL correction applied')
 end

 file = BGCparam.file_vars{n} ; 
 if bgctime==1
    disp(['ERROR : ' BGCparam.name_vars{n} ' bgctime = 1 Not coded in get_frc_GLORYSs'])
    disp(['TO DO : work in get_frc_GLORYSs to create a annual mean from input file'])
    error
 elseif bgctime==12
    time_frc = t ;
 else
    disp(['ERROR : ' BGCparam.name_vars{n} ' bgctime = ' num2str(bgctime) ' Not coded in get_frc_IRONs'])
    error
 end

 disp(['    --> Working on file : ' file])

   lon0 = min(grd.lon(:));
   lon1 = max(grd.lon(:));
   lat0 = min(grd.lat(:));
   lat1 = max(grd.lat(:));

 %%% get var, lon, lat, depth
 lon_frc = ncread(file,'longitude') ; 
 lat_frc = ncread(file,'latitude') ;
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

   depth = ncread(file,'depth') ;
   nz_frc = length(depth) ; 

 if strcmp(BGCparam.name_vars{n},'CHL')==1
    name_vars='chl' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'NO3')==1
    name_vars='no3' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'PO4')==1
    name_vars='po4' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'O2')==1
    name_vars='o2' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'SiO3')==1
    name_vars='si' ;
    factor = 1 ;
 elseif strcmp(BGCparam.name_vars{n},'Fe')==1
    name_vars='fe' ;
    factor = 1 ;
 else
    disp(['ERROR : ' BGCparam.name_vars{n} ' Not coded in get_frc_GLORYSs'])
 end


     if ext_west | ext_east
       fnx1 = nx_frc-i0+1;
       fnx2 = i1;
       vars1 = ncread(file,name_vars,[i0 j0 1 time_frc],[fnx1 fny inf 1]);
       vars2 = ncread(file,name_vars,[1  j0 1 time_frc],[fnx2 fny inf 1]);
       vars = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]); 
    else
       fnx = i1-i0+1;
       vars = ncread(file,name_vars,[i0 j0 1 time_frc],[fnx fny inf 1]);
     end

 if ( chl_corr==1 && strcmp(BGCparam.name_vars{n},'CHL')==1 )
     if ext_west | ext_east
       fnx1 = nx_frc-i0+1;
       fnx2 = i1;
       vars1 = ncread(file_corr,'chl_corr',[i0 j0 time_frc],[fnx1 fny 1]);
       vars2 = ncread(file_corr,'chl_corr',[1  j0 time_frc],[fnx2 fny 1]);
       corr = permute([permute(vars1,[2 1]) permute(vars2,[2 1])],[2 1]);
    else
       fnx = i1-i0+1;
       corr = ncread(file_corr,'chl_corr',[i0 j0 time_frc],[fnx fny 1]);
     end
 else
     corr=squeeze(vars(:,:,1))*0 + 1 ;
 end

 %%% inpaint mask & ascending order
 disp('    --> Inpaint NaNs & ascending order')
 nx_frc = length(lon_frc);
 ny_frc = length(lat_frc);
 [lon_frc,lat_frc] = meshgrid(lon_frc,lat_frc);
 vari= zeros(nz_frc,ny_frc,nx_frc);
 zi  = zeros(nz_frc,ny_frc,nx_frc);
 for z=1:nz_frc
     vari(nz_frc+1-z,:,:) = inpaint_nans(squeeze(vars(:,:,z))',2).*inpaint_nans(double(corr)',2) ; 
     zi  (nz_frc+1-z,:,:) = -depth(z) ;
 end

 %%% Compute or retrieve interpolation coefs through triangulation
  fcoef_glorys = [BGCparam.coefs_dir '/s2r_GLORYS_' BGCparam.name_vars{n} '.mat'] ;
  dummy_mask = squeeze(vari(end,:,:)) ; dummy_mask(dummy_mask~=0)=1 ;
  if exist(fcoef_glorys,'file')
     disp('    --> Reading interpolation coefficients from file');
     load(fcoef_glorys)
  else
     tic
     disp('    --> Computing interpolation coefficients');
     [elem2d,coef2d,nnel] = get_tri_coef(double(lon_frc),double(lat_frc), ...
                          grd.lon,grd.lat,dummy_mask) ;
     A = get_hv_coef(zi, grd.zr, coef2d, elem2d, double(lon_frc), double(lat_frc), grd.lon, grd.lat);
     save(fcoef_glorys,'elem2d','coef2d','nnel','A','-v7.3')
     toc
  end

 %%% Do interpolation
  var = reshape(A*reshape(vari,nz_frc*ny_frc*nx_frc,1),grd.nz,grd.ny,grd.nx); 
  var = permute(var,[3 2 1]).*factor ; 
  var(var<0)=0 ;


 return
