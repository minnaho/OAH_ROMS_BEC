%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 clear all
 close all
 
 wrk_dir     = './';
 grdname     = [wrk_dir, 'kuroshio200m_grd.nc'];

disp(' ')
disp('correcting angle')  
grdval = ncread( grdname ,'angle',[1 1],[Inf Inf]) ;

grdval = grdval*pi/180 ;

ncwrite(grdname , 'angle' , grdval ) ;
disp(' ')

ncid = netcdf.open(grdname,'NC_WRITE') ;
varid = netcdf.inqVarID(ncid,'angle');
attrvalue = netcdf.getAtt(ncid,varid,'units') ;
netcdf.putAtt(ncid,varid,'units','radians');
netcdf.close(ncid)

   
return


%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
