        function fo = get_3Dbry_glorys(datname,grd,varname,intrp,pars);
        %

       dep_frc = ncread(datname,'depth') ;
       nz_frc = length(dep_frc) ;

       [nx,ny] = size(grd.lon) ;
       fld=zeros(nx,ny,nz_frc).*NaN ; 
       fo =zeros(nx,ny,pars.N).*NaN ;

     % Read 
       if grd.ext_west | grd.ext_east
         fnx1 = grd.nx_frc-grd.i0+1;
         fnx2 = grd.i1;
         vars1 = ncread(datname,varname,[grd.i0 grd.j0 1 1],[fnx1 grd.fny nz_frc 1]);
         vars2 = ncread(datname,varname,[1  grd.j0 1 1],[fnx2 grd.fny nz_frc 1]) ;
         vars = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]);
       else
         fnx = grd.i1-grd.i0+1;
         vars = ncread(datname,varname,[grd.i0 grd.j0 1 1],[fnx grd.fny nz_frc 1]);
       end

     % Horizontal interpolation
     tic
     for z=1:nz_frc 
       v2d = squeeze(vars(:,:,z));       
       if any(isnan(v2d(:))==0)
          v2d = inpaint_nans(v2d,2);
          if intrp.tri_interp==1
             fld(:,:,z) = sum(intrp.coef2d .* v2d(intrp.elem2d), 3);
          else
             fld(:,:,z) = interp2(grd.lon_frc,grd.lat_frc,v2d',grd.lon,grd.lat,intrp.method);
          end
       end
     end
     toc

    % Vertical interpolation
    for i = 1:nx
    for j = 1:ny
      vec = squeeze(fld(i,j,:)) ; 
      fint = interp1(-dep_frc(~isnan(vec)),vec(~isnan(vec)),squeeze(grd.z(i,j,:)),'linear','extrap');
      fo(i,j,:) = fint;
    end 
    end
       
       if (strcmp(varname,'uo')==0 && strcmp(varname,'vo')==0)
          fo = squeeze(fo(grd.wi0:grd.wi1,grd.wj0:grd.wj1,:)) ;
       end

        return

