function s2r_hv_ini(datname,grdname,ininame,chdscd);
%--------------------------------------------------------------
%  Produce a ROMS initial file from SODA 2.0.4 data for January
%
%  Inspired by Roms_tools (IRD).
%  Thanks to Pierrick, Patrick (IRD), Francois (UCLA), Yusuke (UCLA)
%  Jeroen Molemaker (UCLA); nmolem@ucla.edu
%--------------------------------------------------------------

% Get S-coordinate params for child grid
  theta_b = chdscd.theta_b;
  theta_s = chdscd.theta_s;
  hc      = chdscd.hc;
  Nc      = chdscd.N;
  scoord_c  = chdscd.scoord;

  [npc mpc] = size(ncread(grdname,'h'));
  
  trec = 1;

% Set bry_time

  % Get child grid and chunk size
    ndomx = 10;
    ndomy = 10;
    
    [Lp,Mp] = size(ncread(grdname,'h'));

    szx = floor(Lp/ndomx);
    szy = floor(Mp/ndomy);

    icmin = [0:ndomx-1]*szx;
    jcmin = [0:ndomy-1]*szy;
    icmax = [1:ndomx]*szx;
    jcmax = [1:ndomy]*szy;
    icmin(1) = 1;
    jcmin(1) = 1;
    icmax(end) = Lp;
    jcmax(end) = Mp;

	% Do the interpolation for all child chunks
    for domx = 1:ndomx
      for domy = 1:ndomy
        [ domx domy]

        icb = icmin(domx);
        ice = icmax(domx);
        jcb = jcmin(domy);
        jce = jcmax(domy);
					  
        % Get topography data from childgrid
        h    = ncread(grdname,'h'       ,[icb jcb],[ice-icb+1 jce-jcb+1])';
        mask = ncread(grdname,'mask_rho',[icb jcb],[ice-icb+1 jce-jcb+1])';
        angc = ncread(grdname,'angle'   ,[icb jcb],[ice-icb+1 jce-jcb+1])';
        lon  = ncread(grdname,'lon_rho' ,[icb jcb],[ice-icb+1 jce-jcb+1])';
        lat  = ncread(grdname,'lat_rho' ,[icb jcb],[ice-icb+1 jce-jcb+1])';
        lon(lon<0) = lon(lon<0) + 360;
        cosc  = cos(angc);         sinc  = sin(angc);

        [Mc,Lc] = size(mask);
        maskc3d = zeros(Nc,Mc,Lc);
        for k = 1:Nc
         maskc3d(k,:,:) = mask;
        end
        umask = maskc3d(:,:,2:end).*maskc3d(:,:,1:end-1);
        vmask = maskc3d(:,2:end,:).*maskc3d(:,1:end-1,:);

        % Z-coordinate (3D) on child grid
	      size(h) ;
        zr = zlevs4(h, h*0, theta_s, theta_b, hc, Nc, 'r', scoord_c);
        zw = zlevs4(h, h*0, theta_s, theta_b, hc, Nc, 'w', scoord_c);

        [u,v,temp,salt,ssh,zi,loni,lati] = get_glorys_data(datname,trec,lon,lat);

      	[nz,ny,nx] = size(u);

        tic
        disp('Computing interpolation coefficients');
        dummy_mask = ssh+99999 ; dummy_mask(isnan(dummy_mask))=0 ;
        dummy_mask(dummy_mask~=0)=1 ;
        [elem2d,coef2d,nnel] = get_tri_coef(double(loni),double(lati),lon,lat,dummy_mask);
%       figure
%       plot(loni,lati,'.k');
%       hold on;plot(lon,lat,'.r');hold off
%       pause(0.5)
%         bot_zi = squeeze(zi(1,:,:)) ;  bot_zr = squeeze(zr(1,:,:)) ;
%         bot_zr(bot_zr<min(min(bot_zi))) = min(min(bot_zi)) ;
%         zr(1,:,:)=bot_zr;
        A = get_hv_coef(zi, zr, coef2d, elem2d, double(loni), double(lati), lon, lat);
        toc
        
        % fillmask
%        temp=fillmask(temp, 1, dummy_mask, nnel);
%        salt=fillmask(salt, 1, dummy_mask, nnel);
%        u(isnan(u)) = 0 ; v(isnan(v)) = 0 ;
%        ssh(isnan(ssh)) = 0 ;
        temp=double(temp) ; salt=double(salt) ;
        u=double(u) ; v=double(v) ;
        ssh=double(ssh) ;
        for z=1:size(temp,1)
           temp(z,:,:) =  inpaint_nans(squeeze(temp(z,:,:)),2) ; 
           salt(z,:,:) =  inpaint_nans(squeeze(salt(z,:,:)),2) ;
              u(z,:,:) =  inpaint_nans(squeeze(   u(z,:,:)),2) ;
              v(z,:,:) =  inpaint_nans(squeeze(   v(z,:,:)),2) ;
        end
        ssh =  inpaint_nans(ssh,2) ;

        % interp
        temp = reshape(A*reshape(temp,nz*ny*nx,1),Nc,Mc,Lc);
        salt = reshape(A*reshape(salt,nz*ny*nx,1),Nc,Mc,Lc);
        u    = reshape(A*reshape(u,   nz*ny*nx,1),Nc,Mc,Lc);
        v    = reshape(A*reshape(v,   nz*ny*nx,1),Nc,Mc,Lc);

        % Rotate to child orientation
        us = zeros(Nc,Mc,Lc);
        vs = zeros(Nc,Mc,Lc);
        for k=1:Nc
          us(k,:,:) = squeeze(u(k,:,:)).*cosc + squeeze(v(k,:,:)).*sinc;
          vs(k,:,:) = squeeze(v(k,:,:)).*cosc - squeeze(u(k,:,:)).*sinc;
        end
        u = 0.5*(us(:,:,1:Lc-1) + us(:,:,2:Lc));  %% back to staggered u points
        v = 0.5*(vs(:,1:Mc-1,:) + vs(:,2:Mc,:));  %% back to staggered v points
%        u = u.*umask;
%        v = v.*vmask;

        % Get barotropic velocity
        if sum(sum(sum(isnan(u)))) > 0
          error('nans in u velocity!')
        end
        if sum(sum(sum(isnan(v)))) > 0
          error('nans in v velocity!')
        end

        %   Prepare for estimating barotropic velocity
        dz  = zw(2:end,:,:)-zw(1:end-1,:,:);
        dzu = 0.5*(dz(:,:,1:end-1)+dz(:,:,2:end));
        dzv = 0.5*(dz(:,1:end-1,:)+dz(:,2:end,:));

        hu   = sum(dzu.*u); hv   = sum(dzv.*v);
        D_u  = sum(dzu);    D_v  = sum(dzv);
        [dum Mu Lu] = size(hu);
        [dum Mv Lv] = size(hv);
        ubar = reshape(hu./D_u,Mu, Lu);     
        vbar = reshape(hv./D_v,Mv, Lv);

        % Sea surface height on ROMS grid
        zetac = sum(coef2d .* ssh(elem2d), 3);
%	      zetac = zetac.*mask;

        disp(' Writing ini file')

        ncwrite(ininame,'temp'   ,permute(temp ,[3 2 1]),[icb jcb 1 1])
        ncwrite(ininame,'salt'   ,permute(salt ,[3 2 1]),[icb jcb 1 1])
        ncwrite(ininame,'u'      ,permute(u    ,[3 2 1]),[icb jcb 1 1])
        ncwrite(ininame,'v'      ,permute(v    ,[3 2 1]),[icb jcb 1 1])
        ncwrite(ininame,'zeta'   ,permute(zetac,[2 1])  ,[icb jcb 1])
        ncwrite(ininame,'ubar'   ,permute(ubar ,[2 1])  ,[icb jcb 1])
        ncwrite(ininame,'vbar'   ,permute(vbar ,[2 1])  ,[icb jcb 1])


      end
    end


  return























