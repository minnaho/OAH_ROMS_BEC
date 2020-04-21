%% ============================================================ %%
%% program to extract a 3D file var(x,y,t), 			%%
%% 2D maps of the entire domain of ROMS of omega                %%
%% aragonite calcualted using two options:        	        %%
%% 1- CO2SYS model a full carbonate system method               %%
%% 2- en emperical statistical model from Juranek et al 2014    %%
%% 						                %%
%% Program by Faycal Kessouri - SCCWRP/UCLA                     %%
%% 05/2018              				        %%
%% ============================================================ %%
disp(['2D Omega aragonite program starts .... on:  ',  datestr(now)])

%% load the matlab paths
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%% enter the parameter by the user
param_isop
%%%%%%%% end of changing part
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% start of the loop
disp('start the loop ..')
cpt = 1;
for fr = 1:length(repavg)
%% find the find one by one
 file = [rep,'/',repavg(fr,1).name] ;
disp(['now reading >>>  ',file])

%% calculate dz
   zeta  = ncread(file, 'zeta')' ;
[z_w,Cw1] = zlevs4(h, zeta, theta_s, theta_b, hc, NZ, 'w',sc_type);
dz = diff(z_w);
        zbot = flipdim(cumsum(flipdim(dz,1)),1);
        ztop = [zbot(2:end,:,:);zeros(1,NY,NX)];
	z = (zbot+ztop)./2 ;

%% read the variables
   dataout  = ncread(file, 'rho') ;
   dataout = permute(dataout, [3 2 1]);
   dens = (squeeze(dataout(:,:,:)) + 1027.4) ;

   dataout  = ncread(file, 'temp') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     temp = Var ;

   dataout  = ncread(file, 'O2') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     o2 = Var ;


if option1==1
   dataout  = ncread(file, 'DIC') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     dic = Var ;

   dataout  = ncread(file, 'salt') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     salt = Var ;

   dataout  = ncread(file, 'PO4') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     po4 = Var ;

   dataout  = ncread(file, 'SiO3') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     sio3 = Var ;

   dataout  = ncread(file, 'Alk') ;
   var = permute(dataout, [3 2 1]);
if bgc==1
   dataout  = ncread(file, 'rho') ;
   dens = permute(dataout, [3 2 1]);
   dens = dens + 1027.4 ;
   var = (var./(dens.*0.001)) ;
end
     Var  = vinterp ( var, -(abs(dens)) ,  -abs(DDfix) ) ;
     Var(Var==0)=NaN;
     alk = Var ;

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
end

%%%%% Calculate omega aragonite option2 (Juranek et al 2014, applied on USW coast)
[OM,Err] = juranek_aragsat(temp',o2') ;

if option1==1
om(om==0)=NaN;
om(om<0)=NaN;
end
OM(OM==0)=NaN;
OM(OM<0)=NaN;

%% write the 2D maps
if option1==1
ncwrite(fout1, 'var', om , [1 1 cpt]);
end
ncwrite(fout2, 'var', OM' , [1 1 cpt]);
   cpt = cpt+1 ;

end % fr

disp(['2D Omega aragonite program ends .... on:  ',  datestr(now)])

%figure
%pcolor(lon,lat,squeeze(OW(:,:,1))) ; shading flat ; colorbar

