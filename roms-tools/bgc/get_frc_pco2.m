 function [var,time] = get_frc_pco2(grd,BGCparam,n)

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

    name_vars='atm_co2' ;
    factor = 1 ;

     if ext_west | ext_east
       fnx1 = nx_frc-i0+1;
       fnx2 = i1;
       vars1 = ncread(file,name_vars,[i0 j0 1],[fnx1 fny inf]);
       vars2 = ncread(file,name_vars,[1  j0 1],[fnx2 fny inf]);
       vars = permute([permute(vars1,[2 1 3]) permute(vars2,[2 1 3])],[2 1 3]); 
    else
       fnx = i1-i0+1;
       vars = ncread(file,name_vars,[i0 j0 1],[fnx fny inf]);
     end

%     if ext_west | ext_east
%       fnx1 = nx_frc-i0+1;
%       fnx2 = i1;
%       vars1 = ncread(file,'t2m',[i0 j0 1],[fnx1 fny inf]);
%       vars2 = ncread(file,'t2m',[1  j0 1],[fnx2 fny inf]);
%       t2m = permute([permute(vars1,[2 1]) permute(vars2,[2 1])],[2 1]);
%    else
%       fnx = i1-i0+1;
%       t2m = ncread(file,'t2m',[i0 j0 1],[fnx fny inf]);
%     end
%     mult = 22.4./(0.0821.*t2m) .* 1e6./(6.022e23) ; 


 %%% inpaint mask & ascending order
 nx_frc = length(lon_frc);
 ny_frc = length(lat_frc);
 [lon_frc,lat_frc] = meshgrid(lon_frc,lat_frc);

 for t=1:size(vars,3)
     test = inpaint_nans(squeeze(vars(:,:,t)),2) ; 
     var(:,:,t) = interp2(lon_frc,lat_frc,test',grd.lon,grd.lat)' ; 
 end

 if size(vars,3)==12
    time = [15.5 45 74.5 105 135.5 166 196 227.5 258 288.5 319 349.5] ;
 else
    disp('Need to work time in get_frc_pco2')
    error
 end

 return
