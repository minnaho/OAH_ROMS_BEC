%function [pH om omega_juranek] = extract_pH_omega(file,DDfix)
disp(['now reading >>>  ',file])

%% calculate dz
%zeta  = ncread(file, 'zeta')' ;
%[z_w,Cw1] = zlevs4(h, zeta, theta_s, theta_b, hc, NZ, 'w',sc_type);
%dz = diff(z_w);
%        zbot = flipdim(cumsum(flipdim(dz,1)),1);
%        ztop = [zbot(2:end,:,:);zeros(1,NY,NX)];
%        z_rho = (zbot+ztop)./2 ;

%% read the vvariables
   dataout  = ncread(file, 'rho') ;
   dataout = permute(dataout, [3 2 1]);
   dens = (squeeze(dataout(:,:,:)) + 1027.4) ;

   dataout  = ncread(file, 'temp') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   temp  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

   dataout  = ncread(file, 'O2') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   vvar = (vvar./(dens.*0.001)) ;
     o2  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

om_juranek = juranek_aragsat(temp,o2) ;

%% pH and omega with CO2SYS
   dataout  = ncread(file, 'DIC') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   vvar = (vvar./(dens.*0.001)) ;
     dic  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;
     dic(dic==0)=NaN;

   dataout  = ncread(file, 'salt') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   salt  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

   dataout  = ncread(file, 'PO4') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   vvar = (vvar./(dens.*0.001)) ; %./ 1.0114 ;
   po4  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

   dataout  = ncread(file, 'SiO3') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   vvar = (vvar./(dens.*0.001)) ; %./ 1.0114 ;
   vvar = squeeze(dataout(:,:,:)) ;
   sio3  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

   dataout  = ncread(file, 'Alk') ;
   dataout = permute(dataout, [3 2 1]);
   vvar = squeeze(dataout(:,:,:)) ;
   vvar = (vvar./(dens.*0.001))./(1+0.0114) ; %./ 1.0114 ;
   alk  = vinterp ( vvar, -(abs(z_rho)) ,  -abs(depth) ) ;

%%%%% Calculate omega aragonite option1
%% parameters
PAR1TYPE =  1 ; % alk
PAR2TYPE = 3 ; % dic 2 , pH 3
pHSCALEIN = 2 ;  % sea water scale
K1K2CONSTANTS = 14 ; % Millero et al, 2010  T:    0-depthlim  S:  1-depthlim. Seaw. scale. Real seawater.
KSO4CONSTANTS = 1 ; % KSO4 of Dickson & TB of Uppstrom 1979  (PREFERRED)
clear DATA
%% calculation
[DATA,HEADERS,NICEHEADERS]=CO2SYS(alk(:),dic(:),1,2,...
    salt(:),temp(:),nan,...
    0,nan,...
    sio3(:),po4(:),...
    pHSCALEIN,...
    K1K2CONSTANTS,KSO4CONSTANTS);
om = DATA(:,16) ;% omega 16
om = reshape(om,NY,NX);
pH = DATA(:,33) ; % pH
pH = reshape(pH,NY,NX);

