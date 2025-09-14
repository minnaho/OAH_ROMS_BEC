function [lon1,lat1] = move_and_turn(psid,thetad,alphad,lambdad, lon,lat)

% The incoming arguments are as follows:

%      psid,thetad are geographical lon,lat coordinates of the
%                      desired location of the center of the grid;
%           alphad is azimuthal rotation angle of the grid;
%          lambdad is the initial latitude of the grid center;
%
% Hence the center of the grid travels as follows
%
%         (lon,lat)=(0,lambda) --> (0,0) --> (psi,theta)
%
% Incoming "lon,lat" are expected to be in radians, however all
% four rotation angles are in degrees, so convert them into radians;

   pi=3.14159265358979323846; deg2rad=pi/180.;
   psi0=deg2rad*psid;    theta0=deg2rad*thetad;
   alpha=deg2rad*alphad; lambda=deg2rad*lambdad;

disp([ '    move_and_turn :: psi=', num2str(psid), ...
                         ' theta=', num2str(thetad), ...
                         ' alpha=', num2str(alphad), ...
                        ' lambda=', num2str(lambdad) ])


% The system of X,Y,Z Cartesian coordinates adopted here is as follows:
% X-axis originates at the center of the Earth and exists through
%        Greenwich meridian at Equator;
% Y-axis exists at 90 degrees East (thus, X-Y plane is Equatorial plane);
% Z-axis exists through North pole;

[a11,a12,a13, a21,a22,a23, a31,a32,a33] = mtrx_YXY_rotate(theta0,alpha,lambda);

[nxi,neta]=size(lon); lon1=zeros(size(lon)); lat1=zeros(size(lat));

for j=1:neta
  for i=1:nxi
    csT=cos(lat(i,j));  xr=csT*cos(lon(i,j));
     zr=sin(lat(i,j));  yr=csT*sin(lon(i,j));

    x = a11*xr +a12*yr +a13*zr;
    y = a21*xr +a22*yr +a23*zr;
    z = a31*xr +a32*yr +a33*zr;

    if (y < -abs(x))
      psi = -0.5*pi-atan(x/y);   % Here "psi" is defined
    elseif (y > abs(x))          % to be within the range
      psi =  0.5*pi-atan(x/y);   % of
    else                         %    -pi < psi <= pi
      psi = atan(y/x);           %
      if (x < 0.)                % this is the most natural
        if (y < 0.)              % way as the initial grid
          psi = psi-pi;          % is centered around 0E in
        else                     % longitudinal direction.
          psi = psi+pi;
        end
      end
    end

    rd=sqrt(x*x+y*y);
    if (z < -rd)                 % The resultant "tht"
      tht =-0.5*pi-atan(rd/z);   % is within the range
    elseif (z > rd)              % -pi/2 <= psi <= pi/2
      tht = 0.5*pi-atan(rd/z);   % Note that technically
    else                         % speaking, code on the
      tht=atan(z/rd);            % left can handle the
    end                          % situation when rd=0.

    lon1(i,j) = psi + psi0;      % add longitudinal shift
    lat1(i,j) = tht;
  end
end

% The following matrix applies three successive turns to vector [x,y,z]:
%
%  1. around Y-axis by angle "lambda", counterclockwise as seen from the
%     top of the arrow looking toward the center of the Earth (i.e, from
%     positive Y-direction to negative);
%
%  2. azimuthal rotation around X-axis by angle "alpha" counterclockwise
%     as seen from the top of the arrow;
%
%  3. around Y-axis again, this time clockwise by angle "theta";
%
% Note that in the case when alpha=0 (hence csA=1 and snA=0 below) this
% matrix degenerates into rotation by angle theta-lambda, as all surviving
% in this case csTh, csLm, snTh, and snLm appear in combinations which add
% up to either cos or sin of difference of the two angles.


function [a11,a12,a13, a21,a22,a23, a31,a32,a33] = ...
                   mtrx_YXY_rotate(theta,alpha,lambda)

csTh=cos(theta); csA=cos(alpha); csLm=cos(lambda);
snTh=sin(theta); snA=sin(alpha); snLm=sin(lambda);

a11=csTh*csLm+snTh*csA*snLm; a12=-snTh*snA; a13=csTh*snLm-snTh*csA*csLm;
             a21 = snA*snLm;     a22 = csA;              a23= -snA*csLm;
a31=snTh*csLm-csTh*csA*snLm; a32= csTh*snA; a33=snTh*snLm+csTh*csA*csLm;

