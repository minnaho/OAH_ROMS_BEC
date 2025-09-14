clear all
close all
disp(' ')
%---------------------------------------------------------------------------------------
%  USER-DEFINED VARIABLES & OPTIONS START HERE
%---------------------------------------------------------------------------------------
%
%---------------------------------------------------------------------------------------
%  1.  GENERAL
%---------------------------------------------------------------------------------------
%
    romsdir    = '/data/project3/pdamien/ROMS_pdamien/config/pachug6km/out_MERCATOR/';
    chdgrd    = [romsdir 'pachug_grd.nc'];
    chdbry    = [romsdir 'pachug_bry_2021.nc'];
%
    obcflag=[0 1 1 0];    % open boundaries flag (1=open , [S E N W])
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  disp(chdbry)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  if obcflag(1)==1  %%   Southern boundary
    disp('Southern boundary')
    %
    zeta = ncread(chdbry,'zeta_south') ;
    temp = ncread(chdbry,'temp_south') ;
    salt = ncread(chdbry,'salt_south') ;
%    mask = zeta(:,1) ; mask(mask>1e20)=NaN ; 
    mask = squeeze(temp(:,end,1)) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        zeta(IndNaN(i),:) = zeta(IndReplace(i),:);
        temp(IndNaN(i),:,:) = temp(IndReplace(i),:,:);
        salt(IndNaN(i),:,:) = salt(IndReplace(i),:,:);
    end     
    ncwrite(chdbry,'zeta_south',zeta);
    ncwrite(chdbry,'temp_south',temp);
    ncwrite(chdbry,'salt_south',salt);
    %
    %
    ubar = ncread(chdbry,'ubar_south') ;
    u    = ncread(chdbry,'u_south') ;
    up   = ncread(chdbry,'up_south') ;
    mask = ubar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        ubar(IndNaN(i),:) = ubar(IndReplace(i),:);
        up  (IndNaN(i),:) = up  (IndReplace(i),:);
        u   (IndNaN(i),:,:) = u(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'ubar_south',ubar);
    ncwrite(chdbry,'u_south',u);
    ncwrite(chdbry,'up_south',up);
    %
    vbar = ncread(chdbry,'vbar_south') ;
    v    = ncread(chdbry,'v_south') ;
    vp   = ncread(chdbry,'vp_south') ;
    mask = vbar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        vbar(IndNaN(i),:) = vbar(IndReplace(i),:);
        vp  (IndNaN(i),:) = vp(IndReplace(i),:);
        v   (IndNaN(i),:,:) = v(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'vbar_south',vbar);
    ncwrite(chdbry,'v_south',v);
    ncwrite(chdbry,'vp_south',vp);
    %
    %
  end


  if obcflag(2)==1  %%   Eastern boundary
    disp('Eastern boundary')
   %
    zeta = ncread(chdbry,'zeta_east') ;
    temp = ncread(chdbry,'temp_east') ;
    salt = ncread(chdbry,'salt_east') ;
%    mask = zeta(:,1) ; mask(mask>1e20)=NaN ;
    mask = squeeze(temp(:,end,1)) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        zeta(IndNaN(i),:) = zeta(IndReplace(i),:);
        temp(IndNaN(i),:,:) = temp(IndReplace(i),:,:);
        salt(IndNaN(i),:,:) = salt(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'zeta_east',zeta);
    ncwrite(chdbry,'temp_east',temp);
    ncwrite(chdbry,'salt_east',salt);
    %
    %
    ubar = ncread(chdbry,'ubar_east') ;
    up   = ncread(chdbry,'up_east') ;
    u    = ncread(chdbry,'u_east') ;
    mask = ubar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        ubar(IndNaN(i),:) = ubar(IndReplace(i),:);
        up  (IndNaN(i),:) = up(IndReplace(i),:);
        u   (IndNaN(i),:,:) = u(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'ubar_east',ubar);
    ncwrite(chdbry,'up_east',up);
    ncwrite(chdbry,'u_east',u);
    %
    vbar = ncread(chdbry,'vbar_east') ;
    vp   = ncread(chdbry,'vp_east') ;
    v    = ncread(chdbry,'v_east') ;
    mask = vbar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        vbar(IndNaN(i),:) = vbar(IndReplace(i),:);
        vp  (IndNaN(i),:) = vp(IndReplace(i),:);
        v   (IndNaN(i),:,:) = v(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'vbar_east',vbar);
    ncwrite(chdbry,'vp_east',vp);
    ncwrite(chdbry,'v_east',v);
    %
    %
  end

  if obcflag(3)==1  %%   Northern boundary
    disp('Northern boundary')
   %
    zeta = ncread(chdbry,'zeta_north') ;
    temp = ncread(chdbry,'temp_north') ;
    salt = ncread(chdbry,'salt_north') ;
%    mask = zeta(:,1) ; mask(mask>1e20)=NaN ;
    mask = squeeze(temp(:,end,1)) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        zeta(IndNaN(i),:) = zeta(IndReplace(i),:);
        temp(IndNaN(i),:,:) = temp(IndReplace(i),:,:);
        salt(IndNaN(i),:,:) = salt(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'zeta_north',zeta);
    ncwrite(chdbry,'temp_north',temp);
    ncwrite(chdbry,'salt_north',salt);
    %
    %
    ubar = ncread(chdbry,'ubar_north') ;
    up = ncread(chdbry,'up_north') ;
    u    = ncread(chdbry,'u_north') ;
    mask = ubar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        ubar(IndNaN(i),:) = ubar(IndReplace(i),:);
        up  (IndNaN(i),:) = up(IndReplace(i),:);
        u   (IndNaN(i),:,:) = u(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'ubar_north',ubar);
    ncwrite(chdbry,'up_north',up);
    ncwrite(chdbry,'u_north',u);
    %
    vbar = ncread(chdbry,'vbar_north') ;
    vp   = ncread(chdbry,'vp_north') ;
    v    = ncread(chdbry,'v_north') ;
    mask = vbar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        vbar(IndNaN(i),:) = vbar(IndReplace(i),:);
        vp  (IndNaN(i),:) = vp(IndReplace(i),:);
        v   (IndNaN(i),:,:) = v(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'vbar_north',vbar);
    ncwrite(chdbry,'vp_north',vp);
    ncwrite(chdbry,'v_north',v);
    %
    %
  end

  if obcflag(4)==1  %%   Western boundary
    disp('Western boundary')
   %
    zeta = ncread(chdbry,'zeta_west') ;
    temp = ncread(chdbry,'temp_west') ;
    salt = ncread(chdbry,'salt_west') ;
%    mask = zeta(:,1) ; mask(mask>1e20)=NaN ;
    mask = squeeze(temp(:,end,1)) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        zeta(IndNaN(i),:) = zeta(IndReplace(i),:);
        temp(IndNaN(i),:,:) = temp(IndReplace(i),:,:);
        salt(IndNaN(i),:,:) = salt(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'zeta_west',zeta);
    ncwrite(chdbry,'temp_west',temp);
    ncwrite(chdbry,'salt_west',salt);
    %
    %
    ubar = ncread(chdbry,'ubar_west') ;
    up   = ncread(chdbry,'up_west') ;
    u    = ncread(chdbry,'u_west') ;
    mask = ubar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        ubar(IndNaN(i),:) = ubar(IndReplace(i),:);
        up  (IndNaN(i),:) = up(IndReplace(i),:);
        u   (IndNaN(i),:,:) = u(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'ubar_west',ubar);
    ncwrite(chdbry,'up_west',up);
    ncwrite(chdbry,'u_west',u);
    %
    vbar = ncread(chdbry,'vbar_west') ;
    vp   = ncread(chdbry,'vp_west') ;
    v    = ncread(chdbry,'v_west') ;
    mask = vbar(:,1) ; mask(mask>1e20)=NaN ;
    mask = mask*0+1 ; mask(isnan(mask)) = 0 ;
    IndNaN = find(mask==0);
    IndReplace = IndNaN*0 ;
    for i=1:length(IndNaN)
        ind1=0;
        while ( (IndNaN(i)-ind1)>=1 && mask(IndNaN(i)-ind1)==0 )
            ind1 = ind1+1;
        end
        ind2=0;
        while ( (IndNaN(i)+ind2)<=length(mask) && mask(IndNaN(i)+ind2)==0 )
            ind2 = ind2+1;
        end
        if ( (IndNaN(i)-ind1)==0 )
           IndReplace(i)=IndNaN(i)+ind2 ;
        elseif ( (IndNaN(i)+ind2)==length(mask)+1 )
           IndReplace(i)=IndNaN(i)-ind1 ;
        elseif ( abs(ind1)<=abs(ind2) )
           IndReplace(i)=IndNaN(i)-ind1;
        elseif ( abs(ind1)>abs(ind2) )
           IndReplace(i)=IndNaN(i)+ind2;
        end
    end
    for i=1:length(IndNaN)
        vbar(IndNaN(i),:) = vbar(IndReplace(i),:);
        vp(IndNaN(i),:)   = vp(IndReplace(i),:);
        v   (IndNaN(i),:,:) = v(IndReplace(i),:,:);
    end
    ncwrite(chdbry,'vbar_west',vbar);
    ncwrite(chdbry,'vp_west',vp);
    ncwrite(chdbry,'v_west',v);
    %
    %
  end




