
disp(' Computing interpolation coefs through triangulation ')

if ~exist(intrp.coefs_dir)
   mkdir(intrp.coefs_dir)
end

   for bnd = 1:4

       if ~obcflag(bnd)
           disp('Closed boundary')
       continue
       end

       disp(['  For Boundary ' obcs(bnd).suffix])

       fcoef = [intrp.coefs_dir '/s2r_' obcs(bnd).suffix '.mat'] ;

       if exist(fcoef,'file')
       disp('  Coefs already known ')
       else 
       disp('  Computing coefs ')
       [lonfrc,latfrc]=meshgrid(double(obcs(bnd).lon_frc),double(obcs(bnd).lat_frc)) ; 
       dummy_mask = obcs(bnd).lon_frc*0 + 1 ; 
       [elem2d,coef2d,nnel] = get_tri_coef(lonfrc',latfrc',obcs(bnd).lon,obcs(bnd).lat,dummy_mask) ;
       save(fcoef,'elem2d','coef2d','nnel','-v7.3') 
       end

%        A = get_hv_coef(zi, grd.zr, coef2d, elem2d, double(lon_frc), double(lat_frc), grd.lon, grd.lat);
%        save(fcoef_woa18,'elem2d','coef2d','nnel','A','-v7.3')

   end
