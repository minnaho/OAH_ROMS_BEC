function [u,v,temp,salt,ssh,zi,loni,lati] = get_glorys_Fdata(datname,trec);

% Processes and returns temp, salt and ssh from SODA monthly climatology that is mask filled
% and extended from -180 to 360 degrees.

  disp('get_glorys')
% Get 3d temperature, salinity and mask from SODA climatology
  loni = ncread(datname,'longitude');
  disp('WARNING : GLORYS special fix on longitude made for Pacifique')
%  loni = [loni(2161:end)' loni(1:2160)']' ;
  loni = [loni(3100:end)' loni(1:1700)']' ;
  loni(loni<0) = loni(loni<0) + 360;
  lati = ncread(datname,'latitude');
  i0 = 1;
  i1 = length(loni);
  j0 = 1;
  j1 = length(lati);
  [loni,lati] = meshgrid(loni,lati);
% figure(1);plot(lon,lat,'.k')
% figure(2);plot(loni,lati,'.k')
% error
  loni = loni(j0:j1,i0:i1);
  lati = lati(j0:j1,i0:i1);
  
  lev = ncread(datname,'depth')';
  nz = length(lev);
% [month j0 j1 i0 i1]
  [ny,nx] = size(loni);
  zi = zeros(nz,ny,nx);
  for k = 1:nz
    zi(k,:,:) = -lev(k);
  end
  
%   temp = permute(squeeze(ncread(soda_mon_data,'temp',[i0 j0 1 month],[i1-i0+1 j1-j0+1 Inf 1])),[3 2 1]);
%   salt = permute(squeeze(ncread(soda_mon_data,'salt',[i0 j0 1 month],[i1-i0+1 j1-j0+1 Inf 1])),[3 2 1]);
  temp = ncread(datname,'thetao') ;  
%  temp = permute([permute(temp(2161:end,:,:),[2 1 3]) permute(temp(1:2160,:,:),[2 1 3])],[2 1 3]) ;
  temp = permute([permute(temp(3100:end,:,:),[2 1 3]) permute(temp(1:1700,:,:),[2 1 3])],[2 1 3]) ;
  temp = temp(i0:i1,j0:j1,:) ; temp = permute(temp,[3 2 1]) ;
  salt = ncread(datname,'so') ; 
%  salt = permute([permute(salt(2161:end,:,:),[2 1 3]) permute(salt(1:2160,:,:),[2 1 3])],[2 1 3]) ;
  salt = permute([permute(salt(3100:end,:,:),[2 1 3]) permute(salt(1:1700,:,:),[2 1 3])],[2 1 3]) ;
  salt = salt(i0:i1,j0:j1,:) ; salt = permute(salt,[3 2 1]) ;

%   u = permute(squeeze(ncread(soda_mon_data,'u',[i0 j0 1 month],[i1-i0+1 j1-j0+1 Inf 1])),[3 2 1]);
%   v = permute(squeeze(ncread(soda_mon_data,'v',[i0 j0 1 month],[i1-i0+1 j1-j0+1 Inf 1])),[3 2 1]);
  u = ncread(datname,'uo') ;  
%  u = permute([permute(u(2161:end,:,:),[2 1 3]) permute(u(1:2160,:,:),[2 1 3])],[2 1 3]) ;
  u = permute([permute(u(3100:end,:,:),[2 1 3]) permute(u(1:1700,:,:),[2 1 3])],[2 1 3]) ;
  u = u(i0:i1,j0:j1,:) ; u = permute(u,[3 2 1]) ;  
  v = ncread(datname,'vo') ; 
%  v = permute([permute(v(2161:end,:,:),[2 1 3]) permute(v(1:2160,:,:),[2 1 3])],[2 1 3]) ;
  v = permute([permute(v(3100:end,:,:),[2 1 3]) permute(v(1:1700,:,:),[2 1 3])],[2 1 3]) ;
  v = v(i0:i1,j0:j1,:) ; v = permute(v,[3 2 1]) ;  
  
  
  disp('WARNING : GLORYS fix for 5days soda to Pacifique : bottom')
  for i=1:i1-i0+1
  for j=1:j1-j0+1
      indnan = min(find(isnan(squeeze(temp(:,j,i))))) ;
      if (indnan~=1)
      temp(indnan:nz,j,i) = temp(indnan-1,j,i);
      salt(indnan:nz,j,i) = salt(indnan-1,j,i);
      u   (indnan:nz,j,i) = u   (indnan-1,j,i);
      v   (indnan:nz,j,i) = v   (indnan-1,j,i);
      end
  end
  end
  temp(isnan(temp))=0;  
  salt(isnan(salt))=0;
  u(isnan(u))=0;
  v(isnan(v))=0;
  
%   ssh = permute(squeeze(ncread(soda_mon_data,'ssh',[i0 j0 month],[i1-i0+1 j1-j0+1 1])),[2 1]);
  ssh = ncread(datname,'zos') ; 
%  ssh = [ssh(2161:end,:)' ssh(1:2160,:)']'  ; 
  ssh = [ssh(3100:end,:)' ssh(1:1700,:)']'  ;
  ssh = ssh(i0:i1,j0:j1) ; ssh = permute(ssh,[2 1]) ;  
  ssh(isnan(ssh))=0;
 
%disp('WARNING : GLORYS return 5days soda vertical in the ascending order') 
%for k=1:nz
%    temp_new(k,:,:) = temp(nz-k+1,:,:) ;
%    salt_new(k,:,:) = salt(nz-k+1,:,:) ;
%    u_new   (k,:,:) = u   (nz-k+1,:,:) ;
%    v_new   (k,:,:) = v   (nz-k+1,:,:) ; 
%    zi_new  (k,:,:) = zi  (nz-k+1,:,:) ;
%end
%temp= temp_new ;
%salt= salt_new ;
%u   = u_new    ;
%v   = v_new    ;
%zi  = zi_new   ;

end

% mypcolor(loni,lati,squeeze(u(end,:,:)));set(gca,'ydir','normal');colorbar
% mypcolor(loni,lati,ssh);set(gca,'ydir','normal');colorbar
% load /batavia/nmolem/OBSERV/COAST/coast_atl
% hold on;plot(clon,clat,'k');hold off
% error('testing get soda data')


   
