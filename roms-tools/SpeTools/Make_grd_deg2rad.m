
clear all

 grdname = '/data/project3/pdamien/ROMS_pdamien/config/PHISUBM600/phisubm600_grd.nc' ;

disp(' ')
disp('correcting angle')
grdval = ncread( grdname ,'angle') ;

grdval = grdval*pi/180 ;

ncwrite(grdname , 'angle' , grdval) ;
disp(' ')

ncid = netcdf.open(grdname,'NC_WRITE') ;
varid = netcdf.inqVarID(ncid,'angle');
attrvalue = netcdf.getAtt(ncid,varid,'units') ;
netcdf.putAtt(ncid,varid,'units','radians');
netcdf.close(ncid)

