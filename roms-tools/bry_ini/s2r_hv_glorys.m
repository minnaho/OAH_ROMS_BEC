function s2r_hv_glorys(datname,grdname,bryname,trec,chdscd,obcflag,coefs_dir);
%--------------------------------------------------------------
%  Produce a ROMS boundary file from data 
%
%  Inspired by Roms_tools (IRD).
%  Thanks to Pierrick, Patrick (IRD), Francois (UCLA), Yusuke (UCLA)
%  Jeroen Molemaker (UCLA); nmolem@ucla.edu
%--------------------------------------------------------------

% Get S-coordinate params for child grid
  theta_b_c = chdscd.theta_b;
  theta_s_c = chdscd.theta_s;
  hc_c      = chdscd.hc;
  N_c       = chdscd.N;
  scoord_c  = chdscd.scoord;

  [npc mpc] = size(ncread(grdname,'h'));
  
 for bnd = 1:4
  disp('------------------------')
  if ~obcflag(bnd)
    disp('Closed boundary')
    continue
  end
  if bnd==1 
   disp('South boundary')
   i0 = 1;
   i1 = npc;
   j0 = 1;
   j1 = 2;
   fcoef = [coefs_dir '/s2r_coefs_south.mat'];
  end
  if bnd==2 
   disp('East boundary')
   i0 = npc-1;
   i1 = npc;
   j0 = 1;
   j1 = mpc;
   fcoef = [coefs_dir '/s2r_coefs_east.mat'];
  end
  if bnd==3 
   disp('North boundary')
   i0 = 1;
   i1 = npc;
   j0 = mpc-1;
   j1 = mpc;
   fcoef = [coefs_dir '/s2r_coefs_north.mat'];
  end
  if bnd==4 
   disp('West boundary')
   i0 = 1;
   i1 = 2;
   j0 = 1;
   j1 = mpc;
   fcoef = [coefs_dir '/s2r_coefs_west.mat'];
  end

% Get topography data from childgrid

  hc   = ncread(grdname,'h'       ,[i0 j0],[i1-i0+1 j1-j0+1])';
  mask = ncread(grdname,'mask_rho',[i0 j0],[i1-i0+1 j1-j0+1])';
  angc = ncread(grdname,'angle'   ,[i0 j0],[i1-i0+1 j1-j0+1])';
  lon  = ncread(grdname,'lon_rho' ,[i0 j0],[i1-i0+1 j1-j0+1])';
  lat  = ncread(grdname,'lat_rho' ,[i0 j0],[i1-i0+1 j1-j0+1])';
  lon(lon<0) = lon(lon<0) + 360;
  cosc  = cos(angc);         sinc  = sin(angc);

%plot(loni,lati,'.k')
%plot(lon,lat,'.r');

  [Mc,Lc] = size(mask);
  maskc3d = zeros(N_c,Mc,Lc);
  for k = 1:N_c
   maskc3d(k,:,:) = mask;
  end
  umask = maskc3d(:,:,2:end).*maskc3d(:,:,1:end-1);
  vmask = maskc3d(:,2:end,:).*maskc3d(:,1:end-1,:);

  % Z-coordinate (3D) on child grid
  zr = zlevs4(hc, hc*0, theta_s_c, theta_b_c, hc_c, N_c, 'r', scoord_c);
  zw = zlevs4(hc, hc*0, theta_s_c, theta_b_c, hc_c, N_c, 'w', scoord_c);
  [Nc Mc Lc] = size(zr);


% get_glorys_data
  [u,v,temp,salt,ssh,zi,loni,lati] = get_glorys_data(datname,1,lon,lat);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  dummy_mask = ssh+99999 ; dummy_mask(isnan(dummy_mask))=0 ; 
  dummy_mask(dummy_mask~=0)=1 ;  

  if exist(fcoef,'file')
    disp('Reading interpolation coefficients from file');
    load(fcoef)
  else
    tic
    disp('Computing interpolation coefficients');
    [elem2d,coef2d,nnel] = get_tri_coef(double(loni),double(lati),lon,lat,dummy_mask);
%   plot(loni,lati,'.k');
%   hold on;plot(lon,lat,'.r');hold off
    A = get_hv_coef(zi, zr, coef2d, elem2d, loni, lati, lon, lat);
    save(fcoef,'elem2d','coef2d','nnel','A')
    toc
  end
 
  % fillmask
   temp=fillmask(temp, 1, dummy_mask, nnel);
   salt=fillmask(salt, 1, dummy_mask, nnel);
   u(isnan(u)) = 0 ; v(isnan(v)) = 0 ; 
   ssh(isnan(ssh)) = 0 ;
%   for z=1:size(temp,1)
%       temp(z,:,:) =  inpaint_nans(squeeze(temp(z,:,:)),2) ; 
%       salt(z,:,:) =  inpaint_nans(squeeze(salt(z,:,:)),2) ;
%          u(z,:,:) =  inpaint_nans(squeeze(   u(z,:,:)),2) ;
%          v(z,:,:) =  inpaint_nans(squeeze(   v(z,:,:)),2) ;
%   end
%   ssh =  inpaint_nans(ssh,2) ;

%   Prepare for estimating barotropic velocity
    dz  = zw(2:end,:,:)-zw(1:end-1,:,:);
    dzu = 0.5*(dz(:,:,1:end-1)+dz(:,:,2:end));
    dzv = 0.5*(dz(:,1:end-1,:)+dz(:,2:end,:));

%   Process scalar 3D variables
    for vint = 1:2 % Loop on the tracers
      if (vint==1)
        svar='temp';
	var = double(temp);
     	[nz,ny,nx] = size(temp);
      elseif (vint==2)
        svar='salt';
	var = double(salt);
      end
      var = reshape(A*reshape(var,nz*ny*nx,1),Nc,Mc,Lc);
      if (bnd ==1 )
        ncwrite(bryname,[svar '_south'],permute(var(:, 1, :),[3 1 2]),[1 1 trec])
      end
      if (bnd ==2 )
        ncwrite(bryname,[svar '_east'],permute(var(:, :, end),[2 1 3]),[1 1 trec])
      end
      if (bnd == 3 )
        ncwrite(bryname,[svar '_north'],permute(var(:, end, :),[3 1 2]),[1 1 trec])
      end
      if (bnd == 4 )
        ncwrite(bryname,[svar '_west'],permute(var(:, :, 1),[2 1 3]),[1 1 trec])
      end
    end  % End loop on vint

    % 3d interpolation of u_r and v_r to roms grid
    u = double(u) ; v = double(v) ;
    ud = reshape(A*reshape(u, nz*ny*nx,1), Nc,Mc,Lc);
    vd = reshape(A*reshape(v, nz*ny*nx,1), Nc,Mc,Lc);

    % Rotate to child orientation
    us = zeros(Nc,Mc,Lc);
    vs = zeros(Nc,Mc,Lc);
    for k=1:Nc
      us(k,:,:) = squeeze(ud(k,:,:)).*cosc + squeeze(vd(k,:,:)).*sinc;
      vs(k,:,:) = squeeze(vd(k,:,:)).*cosc - squeeze(ud(k,:,:)).*sinc;
    end
    u = 0.5*(us(:,:,1:Lc-1) + us(:,:,2:Lc));  %% back to staggered u points
    v = 0.5*(vs(:,1:Mc-1,:) + vs(:,2:Mc,:));  %% back to staggered v points

    u = u.*umask;
    v = v.*vmask;

    % Get barotropic velocity
    if sum(sum(sum(isnan(u)))) > 0
      error('nans in u velocity!')
    end
    if sum(sum(sum(isnan(v)))) > 0
      error('nans in v velocity!')
    end

    hu   = sum(dzu.*u); hv   = sum(dzv.*v);
    D_u  = sum(dzu);    D_v  = sum(dzv);
    [dum Mu Lu] = size(hu);
    [dum Mv Lv] = size(hv);
    ubar = reshape(hu./D_u,Mu, Lu);     
    vbar = reshape(hv./D_v,Mv, Lv);


    % Sea surface height on ROMS grid
    ssh = double(ssh) ; 
    zetac = sum(coef2d .* ssh(elem2d), 3);
    
    if (bnd ==1)
      ncwrite(bryname,'ubar_south',permute( ubar(1, :),[2 1]),[1 trec])
      ncwrite(bryname,'vbar_south',permute( vbar(1, :),[2 1]),[1 trec])
      ncwrite(bryname,'zeta_south',permute(zetac(1, :),[2 1]),[1 trec])
      ncwrite(bryname,'u_south',permute(u(:, 1, :),[3 1 2]),[1 1 trec])
      ncwrite(bryname,'v_south',permute(v(:, 1, :),[3 1 2]),[1 1 trec])     
    end
    if (bnd == 2)
      ncwrite(bryname,'ubar_east',         ubar(:,Lu)       ,[1 trec])
      ncwrite(bryname,'vbar_east',         vbar(:,Lv)       ,[1 trec])
      ncwrite(bryname,'zeta_east',        zetac(:,Lc)       ,[1 trec])
      ncwrite(bryname,'u_east',permute(u(:,:,Lu),[2 1 3]),[1 1 trec])
      ncwrite(bryname,'v_east',permute(v(:,:,Lv),[2 1 3]),[1 1 trec])  
    end
    if (bnd == 3)
      ncwrite(bryname,'ubar_north',permute( ubar(Mu, :),[2 1]),[1 trec])
      ncwrite(bryname,'vbar_north',permute( vbar(Mv, :),[2 1]),[1 trec])
      ncwrite(bryname,'zeta_north',permute(zetac(Mc, :),[2 1]),[1 trec])
      ncwrite(bryname,'u_north',permute(u(:,Mu, :),[3 1 2]),[1 1 trec])
      ncwrite(bryname,'v_north',permute(v(:,Mv, :),[3 1 2]),[1 1 trec])  
    end
    if (bnd == 4)
      ncwrite(bryname,'ubar_west',         ubar(:, 1)       ,[1 trec])
      ncwrite(bryname,'vbar_west',         vbar(:, 1)       ,[1 trec])
      ncwrite(bryname,'zeta_west',        zetac(:, 1)       ,[1 trec])
      ncwrite(bryname,'u_west',permute(u(:, :, 1),[2 1 3]),[1 1 trec])
      ncwrite(bryname,'v_west',permute(v(:, :, 1),[2 1 3]),[1 1 trec]) 
    end

 end    % End loop bnd

  return























