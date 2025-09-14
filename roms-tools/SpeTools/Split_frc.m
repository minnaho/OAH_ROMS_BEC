clear all

addpath('../Make_frc/')

%%%%%%%%%%%%%%%%%%%%%%%%%

grdname = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_grd.nc' ; 
file_in = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/frc2cut/pacgig2km_frc.202211.nc' ; 

file_out1 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022110104.nc'
istr1= 1      ; iend1= 4*24 ; 
file_out2 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022110508.nc'
istr2= 4*24+1 ; iend2= 8*24 ;
file_out3 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022110912.nc'
istr3= 8*24+1 ; iend3=12*24 ;
file_out4 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022111316.nc'
istr4=12*24+1 ; iend4=16*24 ;
file_out5 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022111720.nc'
istr5=16*24+1 ; iend5=20*24 ;
file_out6 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022112124.nc'
istr6=20*24+1 ; iend6=24*24 ;
file_out7 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022112528.nc'
istr7=24*24+1 ; iend7=28*24 ;
file_out8 = '/data/project3/pdamien/ROMS_pdamien/config/PACGIG2KM/pacgig2km_frc.2022112930.nc'
istr8=28*24+1 ; iend8=30*24 ;

coarse_frc=0 ; 
dsatt = 'ERA5 (25 km nominal res)';

%%%%%%%%%%%%%%%%%%%%%%%%%

T1 = iend1-istr1+1 ; 
T2 = iend2-istr2+1 ;
T3 = iend3-istr3+1 ;
T4 = iend4-istr4+1 ;
T5 = iend5-istr5+1 ;
T6 = iend6-istr6+1 ;
T7 = iend7-istr7+1 ;
T8 = iend8-istr8+1 ;

create_frc_bulk(grdname,file_out1,coarse_frc);
ncwriteatt(file_out1,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out2,coarse_frc);
ncwriteatt(file_out2,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out3,coarse_frc);
ncwriteatt(file_out3,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out4,coarse_frc);
ncwriteatt(file_out4,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out5,coarse_frc);
ncwriteatt(file_out5,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out6,coarse_frc);
ncwriteatt(file_out6,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out7,coarse_frc);
ncwriteatt(file_out7,'/','Data Source',dsatt);
create_frc_bulk(grdname,file_out8,coarse_frc);
ncwriteatt(file_out8,'/','Data Source',dsatt);

       % ---- time -----
       var = ncread(file_in,'time',[istr1],[T1]);
       ncwrite(file_out1,'time',var);
       var = ncread(file_in,'time',[istr2],[T2]);
       ncwrite(file_out2,'time',var);
       var = ncread(file_in,'time',[istr3],[T3]);
       ncwrite(file_out3,'time',var);
       var = ncread(file_in,'time',[istr4],[T4]);
       ncwrite(file_out4,'time',var);
       var = ncread(file_in,'time',[istr5],[T5]);
       ncwrite(file_out5,'time',var);
       var = ncread(file_in,'time',[istr6],[T6]);
       ncwrite(file_out6,'time',var);
       var = ncread(file_in,'time',[istr7],[T7]);
       ncwrite(file_out7,'time',var);
       var = ncread(file_in,'time',[istr8],[T8]);
       ncwrite(file_out8,'time',var);
       % ---- rad_time -----
       var = ncread(file_in,'rad_time',[istr1],[T1]);
       ncwrite(file_out1,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr2],[T2]);
       ncwrite(file_out2,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr3],[T3]);
       ncwrite(file_out3,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr4],[T4]);
       ncwrite(file_out4,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr5],[T5]);
       ncwrite(file_out5,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr6],[T6]);
       ncwrite(file_out6,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr7],[T7]);
       ncwrite(file_out7,'rad_time',var);
       var = ncread(file_in,'rad_time',[istr8],[T8]);
       ncwrite(file_out8,'rad_time',var);

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

%%%%% File_out 3

       for t=istr3:iend3
       tw = t-istr3+1 ;
       disp(['file3 time = ' num2str(tw) '/' num2str(T3)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out3,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 4

       for t=istr4:iend4
       tw = t-istr4+1 ;
       disp(['file4 time = ' num2str(tw) '/' num2str(T4)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out4,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 5

       for t=istr5:iend5
       tw = t-istr5+1 ;
       disp(['file5 time = ' num2str(tw) '/' num2str(T5)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out5,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 6

       for t=istr6:iend6
       tw = t-istr6+1 ;
       disp(['file6 time = ' num2str(tw) '/' num2str(T6)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out6,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 7

       for t=istr7:iend7
       tw = t-istr7+1 ;
       disp(['file7 time = ' num2str(tw) '/' num2str(T7)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out7,'rain',var, [1 1 tw]) ;
       end

%%%%% File_out 8

       for t=istr8:iend8
       tw = t-istr8+1 ;
       disp(['file8 time = ' num2str(tw) '/' num2str(T8)])
       % ---- 10 meter winds -----
       var = ncread(file_in,'uwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'uwnd',var,[1 1 tw]) ;
       var = ncread(file_in,'vwnd',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'vwnd',var,[1 1 tw]) ;
       % ---- Incoming Radiation ----- 
       var = ncread(file_in,'swrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'swrad',var,[1 1 tw]) ;
       var = ncread(file_in,'lwrad',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'lwrad',var,[1 1 tw]) ;
       % ---- Absolute humidity -----
       var = ncread(file_in,'qair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'qair',var,[1 1 tw]) ;
       var = ncread(file_in,'Tair',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'Tair',var,[1 1 tw]) ;
       % ---- Rain ------
       var = ncread(file_in,'rain',[1 1 t],[inf inf 1]) ;
       ncwrite(file_out8,'rain',var, [1 1 tw]) ;
       end

