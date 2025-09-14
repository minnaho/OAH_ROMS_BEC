clear all

repin = '/data/project8/pdamien/ROMS_outputs/PACGIG2KM/FORCINGS/' ; 
filein = [repin 'pacgig2km_ini20220501.nc'] ; 
repout = '/data/project8/pdamien/ROMS_outputs/PACGIG2KM/FORCINGS/partition/'
fileout = 'pacgig2km_ini20220501_' ; 
NZ = 100 ;

zeta = ncread(filein,'zeta') ;
[NX,NY] = size(zeta) ; 

for z=1:NZ
      
    if z==1

       file = [repout fileout num2str(z,'%3.3d') '.nc'] 
   
       var  = ncread(filein,'tstart') ; 
       nccreate(file,'tstart','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'tstart','long_name','Start processing day');
       ncwriteatt(file,'tstart','units','day');
       ncwrite(file,'tstart',var) ; 
       
       var    = ncread(filein,'tend') ; 
       nccreate(file,'tend','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'tend','long_name','End processing day');
       ncwriteatt(file,'tend','units','day');
       ncwrite(file,'tend',var) ;

       var = ncread(filein,'theta_s') ;
       nccreate(file,'theta_s','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'theta_s','long_name','S-coordinate surface control parameter');
       ncwriteatt(file,'theta_s','units','nondimensional');
       ncwrite(file,'theta_s',var) ;

       var = ncread(filein,'theta_b') ;
       nccreate(file,'theta_b','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'theta_b','long_name','S-coordinate bottom control parameter');
       ncwriteatt(file,'theta_b','units','nondimensional');
       ncwrite(file,'theta_b',var) ;

       var = ncread(filein,'Tcline') ;
       nccreate(file,'Tcline','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'Tcline','long_name','S-coordinate surface/bottom layer width');
       ncwriteatt(file,'Tcline','units','meter');
       ncwrite(file,'Tcline',var) ;

       var = ncread(filein,'hc') ;
       nccreate(file,'hc','Dimensions',{'one',1},'datatype','single');
       ncwriteatt(file,'hc','long_name','S-coordinate parameter critical depth');
       ncwriteatt(file,'hc','units','meter');
       ncwrite(file,'hc',var) ;

       var = ncread(filein,'sc_r') ;
       nccreate(file,'sc_r','Dimensions',{'s_rho',NZ},'datatype','single');
       ncwriteatt(file,'sc_r','long_name','S-coordinate at RHO-points');
       ncwriteatt(file,'sc_r','units','-');
       ncwrite(file,'sc_r',var) ;

       var = ncread(filein,'Cs_r') ;
       nccreate(file,'Cs_r','Dimensions',{'s_rho',NZ},'datatype','single');
       ncwriteatt(file,'Cs_r','long_name','S-coordinate stretching curves at RHO-points');
       ncwriteatt(file,'Cs_r','units','-');
       ncwrite(file,'Cs_r',var) ;

       var = ncread(filein,'ocean_time') ;
       nccreate(file,'ocean_time','Dimensions',{'time',1},'datatype','single');
       ncwriteatt(file,'ocean_time','long_name','time since initialization');
       ncwriteatt(file,'ocean_time','units','second');
       ncwrite(file,'ocean_time',var) ;

       var = ncread(filein,'ubar') ;
       nccreate(file,'ubar','Dimensions',{'xi_u',NX-1,'eta_u',NY,'time',1},'datatype','single');
       ncwriteatt(file,'ubar','long_name','vertically integrated u-flux component');
       ncwriteatt(file,'ubar','units','meter second-1');
       ncwrite(file,'ubar',var) ;

       var = ncread(filein,'vbar') ;
       nccreate(file,'vbar','Dimensions',{'xi_v',NX,'eta_v',NY-1,'time',1},'datatype','single');
       ncwriteatt(file,'vbar','long_name','vertically integrated v-flux component');
       ncwriteatt(file,'vbar','units','meter second-1');
       ncwrite(file,'vbar',var) ;

       var = ncread(filein,'zeta') ;
       nccreate(file,'zeta','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'zeta','long_name','free surface');
       ncwriteatt(file,'zeta','units','meter');
       ncwrite(file,'zeta',var) ;

       var = ncread(filein,'u',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'u','Dimensions',{'xi_u',NX-1,'eta_u',NY,'time',1},'datatype','single');
       ncwriteatt(file,'u','long_name','u-flux component');
       ncwriteatt(file,'u','units','meter second-1');
       ncwrite(file,'u',var) ;

       var = ncread(filein,'v',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'v','Dimensions',{'xi_v',NX,'eta_v',NY-1,'time',1},'datatype','single');
       ncwriteatt(file,'v','long_name','v-flux component');
       ncwriteatt(file,'v','units','meter second-1');
       ncwrite(file,'v',var) ;

       var = ncread(filein,'w',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'w','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'w','long_name','w-flux component');
       ncwriteatt(file,'w','units','meter second-1');
       ncwrite(file,'w',var) ;

       var = ncread(filein,'temp',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'temp','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'temp','long_name','potential temperature');
       ncwriteatt(file,'temp','units','Celcius');
       ncwrite(file,'temp',var) ;

       var = ncread(filein,'salt',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'salt','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'salt','long_name','Salinity');
       ncwriteatt(file,'salt','units','PSU');
       ncwrite(file,'salt',var) ;

       else

       file = [repout fileout num2str(z,'%3.3d') '.nc']

       var = ncread(filein,'u',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'u','Dimensions',{'xi_u',NX-1,'eta_u',NY,'time',1},'datatype','single');
       ncwriteatt(file,'u','long_name','u-flux component');
       ncwriteatt(file,'u','units','meter second-1');
       ncwrite(file,'u',var) ;

       var = ncread(filein,'v',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'v','Dimensions',{'xi_v',NX,'eta_v',NY-1,'time',1},'datatype','single');
       ncwriteatt(file,'v','long_name','v-flux component');
       ncwriteatt(file,'v','units','meter second-1');
       ncwrite(file,'v',var) ;

       var = ncread(filein,'w',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'w','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'w','long_name','w-flux component');
       ncwriteatt(file,'w','units','meter second-1');
       ncwrite(file,'w',var) ;

       var = ncread(filein,'temp',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'temp','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'temp','long_name','potential temperature');
       ncwriteatt(file,'temp','units','Celcius');
       ncwrite(file,'temp',var) ;

       var = ncread(filein,'salt',[1 1 z 1],[inf inf 1 1]) ;
       nccreate(file,'salt','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
       ncwriteatt(file,'salt','long_name','Salinity');
       ncwriteatt(file,'salt','units','PSU');
       ncwrite(file,'salt',var) ;       

       end

end

z=NZ+1
file = [repout fileout num2str(z,'%3.3d') '.nc']
var = ncread(filein,'w',[1 1 z 1],[inf inf 1 1]) ;
nccreate(file,'w','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
ncwriteatt(file,'w','long_name','w-flux component');
ncwriteatt(file,'w','units','meter second-1');
ncwrite(file,'w',var) ;




