        function fld = get_2Dbry_glorys(datname,grd,varname,intrp);
        %

     if grd.ext_west | grd.ext_east
       fnx1 = grd.nx_frc-grd.i0+1;
       fnx2 = grd.i1;
       vars1 = ncread(datname,varname,[grd.i0 grd.j0 1],[fnx1 grd.fny 1]);
       vars2 = ncread(datname,varname,[1  grd.j0 1],[fnx2 grd.fny 1]) ;
       vars = permute([permute(vars1,[2 1]) permute(vars2,[2 1])],[2 1]);
     else
       fnx = grd.i1-grd.i0+1;
       vars = ncread(datname,varname,[grd.i0 grd.j0 1],[fnx grd.fny 1]);
     end
 
       %vars = fliplr(vars);
       vars = inpaint_nans(vars,2);

     if intrp.tri_interp==1
       fld = sum(intrp.coef2d .* vars(intrp.elem2d), 3);
     else
       fld = interp2(grd.lon_frc,grd.lat_frc,vars',grd.lon,grd.lat,intrp.method);
     end
 
       fld = fld(grd.wi0:grd.wi1,grd.wj0:grd.wj1) ;
       if ( strcmp(grd.suffix,'_east') || strcmp(grd.suffix,'_west') )
          fld = fld';
       end      

        return

