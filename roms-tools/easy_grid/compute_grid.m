function [lone,late, lonr,latr, pm,pn, ang,orterr] = compute_grid( nx,ny, ...
                                           size_x,size_y,  cent_lat,taper, ...
                                           tra_lon,tra_lat,alpha, flip_xy, ...
                                                            compute_angle )

% Produces a logically rectangular curvilinear orthogonal grid with minimal
% distortion. At first it creates a patch of Mercator grid centered at a user
% specified latitude "cent_lat" on Greenwich meridian, sized as "size_y" [km]
% in north-south and "size_x" (also km] in east-west direction measured along
% the longitudinal line passing through the center of the patch.  To center
% the patch at Equator, one shouls set cent_lat=0; positive(negative) values
% move it north(sourth), which also makes it more tapered toward one of the
% poles. Thus, an infinitely small patche is almost rectangular if placed on
% Equator, while behaving more and more like a sector of polar coodinates if
% placed closer to one of the poles.  However in any case it is a perfectly
% Mercator grid with both dx,dy ~ cos(latitude) at any location.

% Then this patch is first moved toward Equator as a solid object, where it
% is asimuthally rotated around it center by angle "alpha", after which it is
% moved to the north or south to latitude "tra_lat", and finally moved east or
% west to longitude "tra_lon".

%   inputs: nx,ny: numbers of grid points in X- and Y-directions, counting
%                  only inner RHO-points (boundary rows are excluded) -- same
%                  as Lm,Mm in ROMS code, with the exception of the possibility
%                  to switch their roles if "flip_xy" is set to transpose the
%                  grid;

%   size_x,size_y: domain size in X- and Y-direction measured in [km];
%        cent_lat: latutude of of the initial location of the grid center;
%           taper: parameter for east-west tapering;

%         tra_lat: desired latitude of grid center;
%         tra_lon: desired longitude of grid center;
%           alpha: asimuthal angle of grid direction (alpha=0 means that
%                  positive X-direction at the center of the grid points
%                  exactly to the east);
%         flip_xy: flag to transpose the grid: 0 do nothing; 1 flip X-direction
%                  and transpose; 2 flip Y-direction and transpose.  Thus 1 and
%                  2 corresponds to 90-degree azimutal rotation in counter- or
%                  or clockwise directions (respectively) however this rotation
%                  is "logical" rather than physical, i.e., the two are the
%                  same for would be perfectly rectangular grid, but are not
%                  equavalent in the case of spherical.
%  compute_angle:  switch to proceed with computation of east angle, =1 yes,
%                  =0 no. This is merely to speed up the responsiveness of GUI
%                  update button because for the plotting purposes all what is
%                  needed is lon,lat, but not pm,pn, ang,orterr.


 disp(['compute_grid :: nx=',num2str(nx),          ' ny=',num2str(ny), ...
               ' size_x=',num2str(size_x),     ' size_y=',num2str(size_y),...
             ' cent_lat=',num2str(cent_lat), ' tapering=',num2str(taper)])
 disp(['        tra_lon=',num2str(tra_lon),   ' tra_lat=',num2str(tra_lat),...
                ' alpha=',num2str(alpha),     ' flip_xy=',num2str(flip_xy) ])

%% Initialize the grid, then move and rotate it to proper location and
%% orientation.

 pi=3.14159265358979323846; deg2rad=pi/180; Eradius = 6371315.;

 pm=zeros(nx+2,ny+2) ; pn=zeros(nx+2,ny+2) ;

 [lone,late, lonr,latr] = init_grid(nx,ny, size_x,size_y, cent_lat,taper);
 if (flip_xy > 0)
   lone = flipdim(lone,flip_xy)'; lonr = flipdim(lonr,flip_xy)';
   late = flipdim(late,flip_xy)'; latr = flipdim(latr,flip_xy)';
 end

 [lonr,latr] = move_and_turn(tra_lon,tra_lat,alpha,cent_lat, lonr,latr);
 [lone,late] = move_and_turn(tra_lon,tra_lat,alpha,cent_lat, lone,late);

%% Compute angles of local grid positive x-axis relative to east

 [ii,jj]=size(latr) ; ang=zeros(ii,jj) ; orterr=zeros(ii,jj) ;

 if (compute_angle == 1)
   disp('Calculating angle ...')


%% ang=0.5*cos(latr);  %% <-- temporally
%%
%% a11 = ang .* ( lone(2:ii+1,2:jj+1) -lone(1:ii,2:jj+1) ... % cos(Lat)*dLon/dX
%%               +lone(2:ii+1,1:jj  ) -lone(1:ii,1:jj  ) ) ;
%%
%% a12 = ang .* ( lone(1:ii,2:jj+1) +lone(2:ii+1,2:jj+1) ... % cos(Lat)*dLon/dY
%%               -lone(1:ii,1:jj  ) -lone(2:ii+1,1:jj  ) ) ;
%%
%% a21 =  0.5 * ( late(2:ii+1,2:jj+1) -late(1:ii,2:jj+1) ... %     dLat/dX
%%               +late(2:ii+1,1:jj  ) -late(1:ii,1:jj  ) ) ;
%%
%% a22 =  0.5 * ( late(1:ii,2:jj+1) +late(2:ii+1,2:jj+1) ... %     dLat/dY
%%               -late(1:ii,1:jj  ) -late(2:ii+1,1:jj  ) ) ;

   for j=1:jj
     for i=1:ii
       dLnX1=lone(i+1,j+1)-lone(i,j+1);        % Most of the time "lone"
       if (dLnX1 > pi)                         % is expected to be a smooth
         dLnX1=dLnX1-2*pi;                     % function of its indices,
       elseif (dLnX1 < -pi)                    % however it may experience
         dLnX1=dLnX1+2*pi;                     % 2*pi jumps due to periodicity
       end                                     % resulting in large valies of
       dLnX=lone(i+1,j)-lone(i,j);             % differences dLnX,dLnY. If this
       if (dLnX > pi)                          % happes, 2*pi is added or
         dLnX=dLnX-2*pi;                       % subtracted as appropriate.
       elseif (dLnX < -pi)
         dLnX=dLnX+2*pi;
       end

       dLnY1=lone(i+1,j+1)-lone(i+1,j);        % Because of this possibility,
       if (dLnY1 > pi)                         % the elegant Matlab-style array
         dLnY1=dLnY1-2*pi;                     % syntax code above is commented
       elseif (dLnY1 < -pi)                    % out permanently, but still
         dLnY1=dLnY1+2*pi;                     % left here for Matlab lovers
       end                                     % to admire, while quasi-Fortran
       dLnY=lone(i,j+1)-lone(i,j);             % code of the left does the job.
       if (dLnY > pi)
         dLnY=dLnY-2*pi;
       elseif (dLnY < -pi)
         dLnY=dLnY+2*pi;
       end

       cff=0.5*cos(latr(i,j));
       a11=cff*(dLnX+dLnX1);                    % cos(Lat)*dLon/dX

       a12=cff*(dLnY+dLnY1);                    % cos(Lat)*dLon/dY

       a21=0.5*( late(i+1,j+1) -late(i,j+1) ... %     dLat/dX
                +late(i+1,j  ) -late(i,j  ) ) ;

       a22=0.5*( late(i,j+1) +late(i+1,j+1) ... %     dLat/dY
                -late(i,j  ) -late(i+1,j  ) ) ;
                                               % Note that this computation
       pm(i,j)=1./(Eradius*sqrt(a11^2+a21^2)); % of pm and pn overwrites their
       pn(i,j)=1./(Eradius*sqrt(a12^2+a22^2)); % previously computed analytical
                                               % counterparts from init_grid.m
       if (a21 < -abs(a11))
         ang1 = -0.5*pi-atan(a11/a21);         % For a perfectly othogonal
       elseif (a21 > abs(a11))                 % curvilinear grid "ang1" and
         ang1 =  0.5*pi-atan(a11/a21);         % "ang2" should be the same.
       else                                    % Here we chose to compute both
         ang1 = atan(a21/a11);                 % of them, use their average as
         if (a11 < 0.)                         % the final accepted value for
           if (a21 < 0.)                       % east angle and also compute
             ang1=ang1-pi;                     % and save their difference as
           else                                % the measure for orthogonality
             ang1=ang1+pi;                     % error.
           end
         end
       end

       if (a12 < -abs(a22))
         ang2 = 0.5*pi +atan(a22/a12);
       elseif (a12 > abs(a22))
         ang2 = -0.5*pi +atan(a22/a12);
       else
         ang2 = -atan(a12/a22);
         if (a22 < 0.)
           if (a12 < 0.)
             ang2 = ang2 +pi;
           else
             ang2 = ang2 -pi;
           end
         end
       end

       ang(i,j)=0.5*(ang1+ang2);  %% the two should be same or very close
       orterr(i,j) = ang1-ang2 ;  %% orthogonality error

     end  %% <-- for i=1:ii
   end  %% <-- for j=1:jj
   disp('fully updated compute_grid')
 else
   disp('updated lon,lat in compute_grid')
 end  %% <-- if compute_angle
