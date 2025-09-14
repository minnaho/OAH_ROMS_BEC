   for bnd = 1:4

         lon_frc = ncread(datname,'longitude');
         lat_frc = ncread(datname,'latitude');
         
         obcs(bnd).nx_frc = length(lon_frc);
         obcs(bnd).ny_frc = length(lat_frc);

       if ~obcflag(bnd)
           disp('Closed boundary')
       continue
       end
       if bnd==1
          disp('South boundary')
          obcs(bnd).i0 = 1; obcs(bnd).i1 = nx;
          obcs(bnd).j0 = 1; obcs(bnd).j1 =  2;
          obcs(bnd).suffix = 'south' ;
          obcs(bnd).wi0 = 1 ; obcs(bnd).wi1 = nx ;
          obcs(bnd).wj0 = 1 ; obcs(bnd).wj1 =  1 ;
       end
       if bnd==2
          disp('East boundary')
          obcs(bnd).i0 = nx-1; obcs(bnd).i1 = nx;
          obcs(bnd).j0 = 1   ; obcs(bnd).j1 = ny;
          obcs(bnd).suffix = 'east' ;
          obcs(bnd).wi0 = 2 ; obcs(bnd).wi1 =  2 ;
          obcs(bnd).wj0 = 1 ; obcs(bnd).wj1 = ny ;
       end
       if bnd==3
          disp('North boundary')
          obcs(bnd).i0 = 1   ; obcs(bnd).i1 = nx;
          obcs(bnd).j0 = ny-1; obcs(bnd).j1 = ny;
          obcs(bnd).suffix = 'north' ;
          obcs(bnd).wi0 = 1 ; obcs(bnd).wi1 = nx ;
          obcs(bnd).wj0 = 2 ; obcs(bnd).wj1 =  2 ;
       end
       if bnd==4
          disp('West boundary')
          obcs(bnd).i0 = 1; obcs(bnd).i1 =  2;
          obcs(bnd).j0 = 1; obcs(bnd).j1 = ny;
          obcs(bnd).suffix = 'west' ;
          obcs(bnd).wi0 = 1 ; obcs(bnd).wi1 =  1 ;
          obcs(bnd).wj0 = 1 ; obcs(bnd).wj1 = ny ;
       end

       h              = ncread(grdname,'h'       ,[obcs(bnd).i0 obcs(bnd).j0], ...
                      [obcs(bnd).i1-obcs(bnd).i0+1 obcs(bnd).j1-obcs(bnd).j0+1]);
       obcs(bnd).angc = ncread(grdname,'angle'   ,[obcs(bnd).i0 obcs(bnd).j0], ...
                      [obcs(bnd).i1-obcs(bnd).i0+1 obcs(bnd).j1-obcs(bnd).j0+1]);
       obcs(bnd).lon  = ncread(grdname,'lon_rho' ,[obcs(bnd).i0 obcs(bnd).j0], ...
                      [obcs(bnd).i1-obcs(bnd).i0+1 obcs(bnd).j1-obcs(bnd).j0+1]);
       obcs(bnd).lat  = ncread(grdname,'lat_rho' ,[obcs(bnd).i0 obcs(bnd).j0], ...
                      [obcs(bnd).i1-obcs(bnd).i0+1 obcs(bnd).j1-obcs(bnd).j0+1]);

       obcs(bnd).z  = zlevs4(h',0*h',pars.theta_s,pars.theta_b,pars.hc,pars.N,'r',pars.scoord);
       obcs(bnd).z  = permute(obcs(bnd).z,[3 2 1]);
       zw  = zlevs4(h',0*h',pars.theta_s,pars.theta_b,pars.hc,pars.N,'w',pars.scoord);
       obcs(bnd).dz = permute(diff(zw),[3 2 1]) ; 

       lon0 = min(obcs(bnd).lon(:));
       lon1 = max(obcs(bnd).lon(:));
       lat0 = min(obcs(bnd).lat(:));
       lat1 = max(obcs(bnd).lat(:));

       % figure out periodic extention of data
       if lon0<min(lon_frc)
          disp('     extending west')
          obcs(bnd).ext_west = 1;
          obcs(bnd).i0 = find(lon_frc-360<lon0,1,'last');
       else
          obcs(bnd).ext_west = 0;
          obcs(bnd).i0 = find(lon_frc<lon0,1,'last');
       end
       if lon1>max(lon_frc)
          disp('     extending east')
          obcs(bnd).ext_east = 1;
          obcs(bnd).i1 = find(lon_frc+360>lon1,1,'first');
       else
          obcs(bnd).ext_east = 0;
          obcs(bnd).i1 = find(lon_frc>lon1,1,'first');
       end

       obcs(bnd).j0 = find(lat_frc<lat0,1,'last');
       obcs(bnd).j1 = find(lat_frc>lat1,1,'first');
       obcs(bnd).fny = obcs(bnd).j1-obcs(bnd).j0+1;

       if obcs(bnd).ext_west
          obcs(bnd).lon_frc= [lon_frc(obcs(bnd).i0:end)'-360 lon_frc(1:obcs(bnd).i1)'];
       elseif obcs(bnd).ext_east
          obcs(bnd).lon_frc= [lon_frc(obcs(bnd).i0:end)' lon_frc(1:obcs(bnd).i1)'+360];
       else
          obcs(bnd).lon_frc= lon_frc(obcs(bnd).i0:obcs(bnd).i1)';
       end
          obcs(bnd).lat_frc = lat_frc(obcs(bnd).j0:obcs(bnd).j1);

end
