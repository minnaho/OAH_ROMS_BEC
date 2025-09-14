clear all

NPx_part = 40 ; 
NPy_part = 32 ;

NZ = 100 ;

repin = '/data/project8/pdamien/ROMS_outputs/PACGIG2KM/FORCINGS/partition/40x32/'
filein = 'pacgig2km_ini20220501' ; 

NBpart = NPx_part*NPy_part ;

for p=1:NBpart

    disp(['Working on partition ' num2str(p-1,'%4.4d')])

    frclist = dir([repin filein '_*.' num2str(p-1,'%4.4d') '.nc']); 
    fileout = [repin filein '.' num2str(p-1,'%4.4d') '.nc'] ; 
    disp('Loop on z')

    for z=1:NZ
        file = [frclist(z).folder '/' frclist(z).name] ; 
        if z==1
           %
           var  = ncread(file,'tstart') ;
           nccreate(fileout,'tstart','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'tstart','long_name','Start processing day');
           ncwriteatt(fileout,'tstart','units','day');
           ncwrite(fileout,'tstart',var) ;
           %
           var    = ncread(file,'tend') ;
           nccreate(fileout,'tend','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'tend','long_name','End processing day');
           ncwriteatt(fileout,'tend','units','day');
           ncwrite(fileout,'tend',var) ;
           %
           var = ncread(file,'theta_s') ;
           nccreate(fileout,'theta_s','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'theta_s','long_name','S-coordinate surface control parameter');
           ncwriteatt(fileout,'theta_s','units','nondimensional');
           ncwrite(fileout,'theta_s',var) ;
           %
           var = ncread(file,'theta_b') ;
           nccreate(fileout,'theta_b','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'theta_b','long_name','S-coordinate bottom control parameter');
           ncwriteatt(fileout,'theta_b','units','nondimensional');
           ncwrite(fileout,'theta_b',var) ;
           %
           var = ncread(file,'Tcline') ;
           nccreate(fileout,'Tcline','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'Tcline','long_name','S-coordinate surface/bottom layer width');
           ncwriteatt(fileout,'Tcline','units','meter');
           ncwrite(fileout,'Tcline',var) ;
           %
           var = ncread(file,'hc') ;
           nccreate(fileout,'hc','Dimensions',{'one',1},'datatype','single');
           ncwriteatt(fileout,'hc','long_name','S-coordinate parameter critical depth');
           ncwriteatt(fileout,'hc','units','meter');
           ncwrite(fileout,'hc',var) ;
           %
           var = ncread(file,'sc_r') ;
           nccreate(fileout,'sc_r','Dimensions',{'s_rho',NZ},'datatype','single');
           ncwriteatt(fileout,'sc_r','long_name','S-coordinate at RHO-points');
           ncwriteatt(fileout,'sc_r','units','-');
           ncwrite(fileout,'sc_r',var) ;
           %
           var = ncread(file,'Cs_r') ;
           nccreate(fileout,'Cs_r','Dimensions',{'s_rho',NZ},'datatype','single');
           ncwriteatt(fileout,'Cs_r','long_name','S-coordinate stretching curves at RHO-points');
           ncwriteatt(fileout,'Cs_r','units','-');
           ncwrite(fileout,'Cs_r',var) ;
           %
           var = ncread(file,'ocean_time') ;
           nccreate(fileout,'ocean_time','Dimensions',{'time',1},'datatype','single');
           ncwriteatt(fileout,'ocean_time','long_name','time since initialization');
           ncwriteatt(fileout,'ocean_time','units','second');
           ncwrite(fileout,'ocean_time',var) ;
           %
           var = ncread(file,'ubar') ; [NXu,NY] = size(var) ; 
           nccreate(fileout,'ubar','Dimensions',{'xi_u',NXu,'eta_rho',NY,'time',1},'datatype','single');
           ncwriteatt(fileout,'ubar','long_name','vertically integrated u-flux component');
           ncwriteatt(fileout,'ubar','units','meter second-1');
           ncwrite(fileout,'ubar',var) ;
           %
           var = ncread(file,'vbar') ; [NX,NYv] = size(var) ;
           nccreate(fileout,'vbar','Dimensions',{'xi_rho',NX,'eta_v',NYv,'time',1},'datatype','single');
           ncwriteatt(fileout,'vbar','long_name','vertically integrated v-flux component');
           ncwriteatt(fileout,'vbar','units','meter second-1');
           ncwrite(fileout,'vbar',var) ;
           %
           var = ncread(file,'zeta') ; [NX,NY] = size(var) ;
           nccreate(fileout,'zeta','Dimensions',{'xi_rho',NX,'eta_rho',NY,'time',1},'datatype','single');
           ncwriteatt(fileout,'zeta','long_name','free surface');
           ncwriteatt(fileout,'zeta','units','meter');
           ncwrite(fileout,'zeta',var) ;
           %
           var = ncread(file,'u') ;
           nccreate(fileout,'u','Dimensions',{'xi_u',NXu,'eta_rho',NY,'s_rho',NZ,'time',1},'datatype','single');
           ncwriteatt(fileout,'u','long_name','u-flux component');
           ncwriteatt(fileout,'u','units','meter second-1');
           ncwrite(fileout,'u',var,[1 1 z 1]) ;
           %
           var = ncread(file,'v') ;
           nccreate(fileout,'v','Dimensions',{'xi_rho',NX,'eta_v',NYv,'s_rho',NZ,'time',1},'datatype','single');
           ncwriteatt(fileout,'v','long_name','v-flux component');
           ncwriteatt(fileout,'v','units','meter second-1');
           ncwrite(fileout,'v',var,[1 1 z 1]) ;
           %
           var = ncread(file,'w') ;
           nccreate(fileout,'w','Dimensions',{'xi_rho',NX,'eta_rho',NY,'s_w',NZ+1,'time',1},'datatype','single');
           ncwriteatt(fileout,'w','long_name','w-flux component');
           ncwriteatt(fileout,'w','units','meter second-1');
           ncwrite(fileout,'w',var,[1 1 z 1]) ;
           %
           var = ncread(file,'temp') ;
           nccreate(fileout,'temp','Dimensions',{'xi_rho',NX,'eta_rho',NY,'s_rho',NZ,'time',1},'datatype','single');
           ncwriteatt(fileout,'temp','long_name','potential temperature');
           ncwriteatt(fileout,'temp','units','Celcius');
           ncwrite(fileout,'temp',var,[1 1 z 1]) ;
           %
           var = ncread(file,'salt') ;
           nccreate(fileout,'salt','Dimensions',{'xi_rho',NX,'eta_rho',NY,'s_rho',NZ,'time',1},'datatype','single');
           ncwriteatt(fileout,'salt','long_name','Salinity');
           ncwriteatt(fileout,'salt','units','PSU');
           ncwrite(fileout,'salt',var,[1 1 z 1]) ;
           %
           var = ncreadatt(file,'/','partition') ; 
           ncwriteatt(fileout,'/','partition',var);
           %
        else
           %
           var = ncread(file,'u') ;
           ncwrite(fileout,'u',var,[1 1 z 1]) ;
           %
           var = ncread(file,'v') ;
           ncwrite(fileout,'v',var,[1 1 z 1]) ;
           %
           var = ncread(file,'w') ;
           ncwrite(fileout,'w',var,[1 1 z 1]) ;
           %
           var = ncread(file,'temp') ;
           ncwrite(fileout,'temp',var,[1 1 z 1]) ;
           %
           var = ncread(file,'salt') ;
           ncwrite(fileout,'salt',var,[1 1 z 1]) ;
           %
        end
    end
    z=NZ+1 ; 
    file = [frclist(z).folder '/' frclist(z).name] ; 
    var = ncread(file,'w') ;
    ncwrite(fileout,'w',var,[1 1 z 1]) ; 
    disp('remove z sliced files')
    for z=1:NZ+1
    delete([frclist(z).folder '/' frclist(z).name])
    end
end






