%======================================================
%  make point source forcing file for Tohoku 3 km
%                           7-01-2011 Yusuke Uchiyama
%     10-15-2013 Revised for niida_150m sediment test
%     10-24-2013 Revised for a storm event (5/19)
%======================================================
clear all;
close all;

psrc_title='point source for Tohoku L3 150-m grid';
psrc_fname='niida_150m_event_psource.nc';

% input files
grdname = '/home/yusuke/Research/Cesium/L3/grid/niida_150m_grd.nc';

% max monthly-mean discharge of Abukuma River is 212.2469 m3/s.
%qave=40;	% m3/s.  ==> crudely assumed that discharge from minor rivers
%       		%            is about 1/5 of the peak discharge from Abukuma.

% number of passive tracers (must be >= 2, including T and S)
Npas=6;		% 4: T, S, sand, silt
psvars={'temp','salt','tpas1','sediment1','sediment2','sediment3'};
psname={'temperature','salinity','passive tracer','sand concentration',...
        'silt concentration','clay concentration'};
psunit={'deg. C','psu','no dimension','mg/L','mg/L','mg/L'};

qmax=40; %470;  % max discharge in m3/s
sedmax=[100 100 100];  % max sediment concentration in mg/L 
%sedmax=[1000 1000 1000];  % max sediment concentration in mg/L 

% define value of variables (T, S, tpas1, tpas2,...)

psvals=[18.0, 0, 1,sedmax(1), sedmax(2), sedmax(3)];

%---------------------------------------------------------------------
% Niida River discharge during a typhoon (data from Prof. Nagao)
% 2011/09/21 17:00	155.67
% 2011/09/21 18:00	171.06
% 2011/09/21 19:00	187.18
% 2011/09/21 20:00	253.4
% 2011/09/21 21:00	398.51
% 2011/09/21 22:00	459.06
% 2011/09/21 23:00	470.18  <-- peak, 7 hours since initialization
% 2011/09/22 00:00	440.8
% 2011/09/22 01:00	384.89
% 2011/09/22 02:00	332.77
% 2011/09/22 03:00	290.27
%
% Idealized Niida freshwater & sediment discharge: forced to [May 30, 2011]
tinit=mjd(2011,5,30,12)-7/24;	% peak time in MJD (UTC) is noon,5-30-2011
qq=[155.67 171.06 187.18 253.4 398.51 459.06 470.18 440.8 384.89 332.77 290.27];
tq=[0:1/6:24]; qp=max(0,qmax*sin(tq./14*pi));
sedim=qp.^2./max(qp.^2);
% test plot
%figure; plot(tq,qp,'-b',[1:11],qq,'-m');
%figure; plot(tq,sedim,'-b');

%---------------------------------------------------------------------

% locations and direction of river months
% (Isrc, Jsrc) is grid location (rho-point)
% Dsrc: direction (0:I-dir, 1:J-dir, 2:K-dir)
% Dsgn is 1: positive, -1:negtive (westward discharge --> Dsgn=-1)
%================================
% Mano River, i=19 ,j=162:164
% Niida River, i=27 ,j=127:129
% Ota River, i=28 ,j=91:93
% Kotaka River, i=28 ,j=77:79
% Isrc and Jsrc determine the grid where Q comes out.
% In case of niida_150m, they are on land cells.
 Isrc=[ 19  19  19  27  27  27  28  28  28  28  28  28];
 Jsrc=[162 163 164 127 128 129  91  92  93  77  78  79];
 Dsrc=[  0   0   0   0   0   0   0   0   0   0   0   0];
 Dsgn=[  1   1   1   1   1   1   1   1   1   1   1   1];
 Rate=[1/4 1/2 1/4 1/4 1/2 1/4 1/4 1/2 1/4 1/4 1/2 1/4];

% period to apply river discharge in ocean_time
psrc_time(1)=mjd(2011, 3,1,0); Qbar(1)=0; Sed(1)=0;
for tind=1:length(tq);
  psrc_time(tind+1)=tinit+tq(tind)./24;
  Qbar(tind+1)=qp(tind);
  Sed(tind+1)=sedim(tind);
end;
psrc_time(tind+2)=mjd(2011,12,31,23);
Qbar(tind+2)=0; Sed(tind+2)=0;

% test for initial tpas release
Qbar=Qbar+1;

% recycling? (zero for non-recycle)
psrc_cycle=0;

% s-coordinate attributes: must be consistenc with BRY/INI
N      = 24;	% number of vertical s-layers
thetas = 6.0;
thetab = 2.5;
hc     = 200.0;
scoord = 'new';

% Qshape type
Qs_type=2;	% 1: vertically uniform
            % 2: upper (peaked at z=-hpeak)
            % 3: lower (peaked at z=-h+hpeak, hpeak: height above bed)
Pdirection=0; hpeak=0; Scff=0.12;		% xi-dir flux
%Pdirection=2; hpeak=20; Scff=0.01;		% vertical flux
			% Qshape = exp(-Scff*(z+zpeak)^2)

%===============================================================
% rivers

Nsrc=length(Isrc);
for ii=1:Nsrc;
% Qs_type          Zcff(hpeak)  Scff          
  Qtp(ii)=Qs_type; Zpp(ii)=0;   Sss(ii)=Scff;
% temp          salt          tpas1          sand          silt          clay
%%%  Lsrc(1,ii)=0; Lsrc(2,ii)=1; Lsrc(3,ii)=0; Lsrc(4,ii)=1; Lsrc(5,ii)=1; Lsrc(6,ii)=1;
  Lsrc(1,ii)=0; Lsrc(2,ii)=1; Lsrc(3,ii)=1; Lsrc(4,ii)=1; Lsrc(5,ii)=1; Lsrc(6,ii)=1;
end;

% u- and v- directions need one grid-pont shift (u-point/rho-point difference)
%ind=find(Dsrc==0 & Dsgn== 1); Isrc(ind)=Isrc(ind)-1; clear ind;
%ind=find(Dsrc==0 & Dsgn==-1); Isrc(ind)=Isrc(ind);   clear ind;
%ind=find(Dsrc==1 & Dsgn== 1); Jsrc(ind)=Jsrc(ind)-1; clear ind;
%ind=find(Dsrc==1 & Dsgn==-1); Jsrc(ind)=Jsrc(ind);   clear ind;

%======================================================
% Read the grid file

nc=netcdf(grdname,'r');
h=nc{'h'}(:);
mask=nc{'mask_rho'}(:);
close(nc);
hmin=min(min(h));
zr=my_zlevs_new(h,h.*0,thetas,thetab,hc,N,'r',scoord);

%======================================================
% Qshape

for is=1:Nsrc;
  cff=0.0;
  i=Isrc(is);
  j=Jsrc(is);
  zz=squeeze(zr(:,j,i));
  if mask(j,i)==0;
    ierr=0;
    if Dsrc(is)==0 & Dsgn(is)==1  & mask(j,i+1)==0; ierr=1; end;
    if Dsrc(is)==0 & Dsgn(is)==-1 & mask(j,i)==0;   ierr=1; end;
    if Dsrc(is)==1 & Dsgn(is)==1  & mask(j+1,i)==0; ierr=1; end;
    if Dsrc(is)==1 & Dsgn(is)==-1 & mask(j,i)==0;   ierr=1; end;
    if ierr==1;
      disp(['Warning: psource defined on land cell. is = ' int2str(is) '.']);
    end;
  end;
  Qs_type=Qtp(is); hpeak=Zpp(is); Scff=Sss(is);
  for k=1:N;
    if Qs_type==1; Qshape(k,is)=1.0;    % uniform
    else;
      if Qs_type==2;                    % upper
        Zcff=hpeak;
      else;                             % lower
        Zcff=h(j,i)-hpeak;
      end;
      Qshape(k,is)=exp(-Scff*((zz(k)+Zcff)^2));
    end;
    cff=cff+Qshape(k,is);   % Qsrc=Qbar*Qshape: mass flux (m3/s), usrc*Hz
  end;
  for k=1:N;
    Qshape(k,is)=Qshape(k,is)./cff;
  end;
end;

%======================================================
% write down everything to the point source file

Msrc=length(Isrc);
display(['creating ' psrc_fname ' with ' int2str(Msrc) ' psorces.']);
create_psource(psrc_fname,psvars,psname,psunit,Msrc,N,psrc_title,psrc_time,psrc_cycle);

nc=netcdf(psrc_fname,'w');
icc=0;
display(['damping out the data to ' psrc_fname '.']);
for is=1:Nsrc;
    icc=icc+1;
    nc{'Lsrc'}(:,icc)=squeeze(Lsrc(:,is));
    nc{'Isrc'}(icc)=Isrc(is);
    nc{'Jsrc'}(icc)=Jsrc(is);
    nc{'Dsrc'}(icc)=Dsrc(is);
    nc{'Qbar'}(:,icc)=Qbar.*Rate(is);
    for itrc=1:Npas;
      svv=char(psvars(itrc));
      if itrc<=3;	% T, S and tpas1 
        nc{svv}(:,icc)=psvals(itrc);
      else;			% sediments
        nc{svv}(:,icc)=psvals(itrc).*Sed;
      end;
    end;
    nc{'Qshape'}(:,icc)=squeeze(Qshape(:,is));
end;
close(nc);


return;
