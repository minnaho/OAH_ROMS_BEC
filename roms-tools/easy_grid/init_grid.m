function [lone,late, lonr,latr] = init_grid(nx,ny, size_x,size_y, ...
                                                   cent_lat,taper)

  pi=3.14159265358979323846 ;  deg2rad=pi/180.;  Eradius=6371315. ;

  theta=deg2rad*cent_lat ;                 %% latitude of grid center and
  dtht=0.5*size_y/Eradius ;                %% half of its north-south extent
  ymax=lat_to_eta( theta + dtht );         %% expressed in radians
  ymin=lat_to_eta( theta - dtht );
  dy=(ymax-ymin)/double(ny);

  x_size=size_x/(Eradius*cos(theta)) ;     %% east-west extents of
  xmin=-0.5*x_size ; xmax=+0.5*x_size ;    %% the grid expressed in
  dx=x_size/double(nx) ;                   %% radians


  disp(['ISOTROPY ERROR (dx/dy)-1 = ', num2str(dx/dy -1.) ])

  lone=zeros(nx+3,ny+3) ; lonr=zeros(nx+2,ny+2) ;
  late=zeros(nx+3,ny+3) ; latr=zeros(nx+2,ny+2) ;

  xe=zeros(nx+3,ny+3) ;  xr=zeros(nx+2,ny+2) ;
  ye=zeros(nx+3,ny+3) ;  yr=zeros(nx+2,ny+2) ;

  if (abs(taper) > 0.001)
    x0=(xmin+xmax)/2.0 -(xmax-xmin)/taper ;    %% Setup a segment of polar
    rmin=xmin-x0 ; rmax=xmax-x0 ;              %% grid centered at (x0,y0)
    drho=( log(rmax/rmin) )/double(nx);        %% on a flat plane which is
                                               %% Mercator projection plane

%%  dalpha=drho;  %%% <-- perfectly isotropic
    dalpha=dy*drho/dx ;

    alpha_max=dalpha*double(ny)/2. ;
    alpha_min=-alpha_max ;
    y0=0.5*(ymin+ymax) ;

    disp(['x0=',num2str(x0), ' rmin=',num2str(rmin), ' rmax=',num2str(rmax)])
    disp(['alpha_min=',num2str(alpha_min), ' alpha_max=',num2str(alpha_max)])

    for j=1:ny+3
      for i=1:nx+3
        r=rmin*exp( drho*double(i-2) ) ;
        alpha=alpha_min+dalpha*double(j-2) ;

        xe(i,j)=x0 +r*cos(alpha) ;
        ye(i,j)=y0 +r*sin(alpha) ;
      end
    end
    for j=1:ny+2
      for i=1:nx+2
        r=rmin*exp( drho * (double(i)-1.5) ) ;
        alpha=alpha_min+dalpha*(double(j)-1.5);

        xr(i,j)=x0 +r*cos(alpha) ;
        yr(i,j)=y0 +r*sin(alpha) ;
      end
    end
  else
    for j=1:ny+3
      for i=1:nx+3
        xe(i,j)=xmin+dx*double(i-2)  ;
        ye(i,j)=ymin+dy*double(j-2) ;
      end
    end
    for j=1:ny+2
      for i=1:nx+2
        xr(i,j)=xmin+dx*(double(i)-1.5)  ;
        yr(i,j)=ymin+dy*(double(j)-1.5) ;
      end
    end
  end


  for j=1:ny+3                             %% at extended PSI-points
    for i=1:nx+3
      late(i,j)=asin(tanh(ye(i,j))) ;      %% latitude in radians
      lone(i,j)=xe(i,j) ;                  %% longitude in radians
    end
  end

  for j=1:ny+2                             %% at RHO-points
    for i=1:nx+2
      latr(i,j)=asin(tanh(yr(i,j))) ;      %% keep in radians
      lonr(i,j)=xr(i,j) ;                  %% longitude in radians
    end
  end

  clear xe ye xr yr ; 


  function eta = lat_to_eta(theta)
  pi=3.14159265358979323846;
  if (-0.5*pi < theta && theta < 0.5*pi)
    cff=sin(theta);
    eta=0.5*log( (1.+cff)/(1.-cff) );
  else
    disp(['lat_to_eta :: theta=', num2str(theta)])
    error('### ERROR: Latitude range exception.')
  end
