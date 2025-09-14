clear all

addpath('../Make_frc/')

%%%%%%%%%%%%%%%%%%%%%%%%%

grdname = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_grd.nc' ; 
file_in = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/frc2cut/pacgig2km_frc.2022072131.nc' ;
length(ncread(file_in,'time'))
length(ncread(file_in,'time'))/24
 
file_out1 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022072125.nc'
istr1=1 ; iend1=5*24 ; 
file_out2 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022072631.nc'
istr2=5*24+1 ; iend2=10*24 ;

coarse_frc=0 ; 
dsatt = 'ERA5 (25 km nominal res)';

%%%%%%%%%%%%%%%%%%%%%%%%%

T1 = iend1-istr1+1 ; 
T2 = iend2-istr2+1 ;

create_frc_bulk(grdname,file_out1,coarse_frc);
ncwriteatt(file_out1,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out2,coarse_frc);
ncwriteatt(file_out2,'/','Data Source',dsatt);

       % ---- time -----
       var = ncread(file_in,'time',[istr1],[T1]);
       ncwrite(file_out1,'time',var);
       var = ncread(file_in,'time',[istr2],[T2]);
       ncwrite(file_out2,'time',var);
       % ---- rad_time -----
       var = ncread(file_in,'rad_time',[istr1],[T1]);
       ncwrite(file_out1,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr2],[T2]);
       ncwrite(file_out2,'rad_time',var);

%%%%% File_out 1

       for t=istr1:iend1
       tw = t-istr1+1 ; 
       disp(['file1 time = ' num2str(tw) '/' num2str(T1)])    
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ; 
       ncwrite(file_out1,'uwnd',var,[1 1 tw]) ; 
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'vwnd',var,[1 1 tw]) ;  
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'lwrad',var,[1 1 tw]) ;     
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'Tair',var,[1 1 tw]) ; 
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out1,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 2

       for t=istr2:iend2
       tw = t-istr2+1 ;
       disp(['file2 time = ' num2str(tw) '/' num2str(T2)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out2,'rain',var, [1 1 tw]) ;
       end


