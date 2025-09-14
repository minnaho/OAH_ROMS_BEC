 function [var,time] = get_frc_iron(grd,BGCparam,n)

 file = BGCparam.file_vars{n} ;
 disp(['    --> Working on file : ' file])

   lon0 = min(grd.lon(:));
   lon1 = max(grd.lon(:));
   lat0 = min(grd.lat(:));
   lat1 = max(grd.lat(:));

 file = BGCparam.file_vars{n} ;
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

 if strcmp(BGCparam.name_vars{n},'dust')==1  
    name_vars='fe_dst' ; % ton/month/m2
%    factor = 17.9e12 /( 30*24*60*60 *1e4) / (0.35*1e3) ; %ton/month/m2 to nmol/s/cm2 + iron 2 dust
%     convert dust flux into kg/m2/s
%           fe to dust   ton to kg       month to sec 
    factor = 1/0.035    *   1000    /   (30.5*24*60*60) ; 
 elseif strcmp(BGCparam.name_vars{n},'iron')==1
    name_vars='fe_totsol' ;
    factor = 17.9e12 /( 30*24*60*60 * 1e4) ; %ton/month/m2 to nmol/s/cm2
 else
    disp(['ERROR : ' BGCparam.name_vars{n} ' Not coded in get_frc_GLORYSs'])
 end
 

     if ext_west | ext_east
       fnx1 = nx_frc-i0+1;
       fnx2 = i1;
       vars1 = ncread(file,name_vars,[i0 j0 1],[fnx1 fny inf]);
       vars2 = ncread(file,name_vars,[1  j0 1],[fnx2 fny inf]);
       vars = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]); 
       area1 = ncread(file,'area',[i0 j0],[fnx1 fny]);
       area2 = ncread(file,'area',[1  j0],[fnx2 fny]);
       area = permute([permute(area1,[2 1]) permute(area2,[2 1])],[2 1]);
    else
       fnx = i1-i0+1;
       vars = ncread(file,name_vars,[i0 j0 1],[fnx fny inf]);
       area = ncread(file,'area',[i0 j0],[fnx fny]);
     end

     vars = (1/3) * ( vars(:,:,1:12)+vars(:,:,13:24)+vars(:,:,25:36) ) ;

 %%% inpaint mask & ascending order
 nx_frc = length(lon_frc);
 ny_frc = length(lat_frc);
 [lon_frc,lat_frc] = meshgrid(lon_frc,lat_frc);

 for t=1:size(vars,3)
     test = inpaint_nans(double(squeeze(vars(:,:,t))),2) ; 
     test= test./area ; 
     var(:,:,t) = interp2(lon_frc,lat_frc,test',grd.lon,grd.lat)' ; 
 end

 var=var.*factor ; 

 if size(vars,3)==12
    time = [15.5 45 74.5 105 135.5 166 196 227.5 258 288.5 319 349.5] ;
 else
    disp('Need to work time in get_frc_iron')
    error
 end

 return
