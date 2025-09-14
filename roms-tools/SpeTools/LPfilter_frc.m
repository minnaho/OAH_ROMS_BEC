clear all 

rep = '/data/project3/pdamien/ROMS_pdamien/config/PHISUBM600/' ; 
name = 'phisubm600_frc.';

%win_rad = 49 ; pas_rad = (win_rad-1)/2 ;
win_rad = 73 ; pas_rad = (win_rad-1)/2 ;
win_wnd = 49 ; pas_wnd = (win_wnd-1)/2 ;

list = dir([rep name '*.nc']) ; 

for t=1:length(list)

file2filt = [list(t).folder '/' list(t).name]
NT_0 = length(ncread(file2filt,'time')) ;  
if t==1
   file2filt_m1 = 'none';
   NT_m1 = 0 ;
else
   file2filt_m1 = [list(t-1).folder '/' list(t-1).name];
   NT_m1 = length(ncread(file2filt_m1,'time')) ;
end
if t==length(list)
   file2filt_p1 = 'none' ;
   NT_p1 = 0 ;
else
   file2filt_p1 = [list(t+1).folder '/' list(t+1).name];
   NT_p1 = length(ncread(file2filt_p1,'time')) ;
end

file_filt = [file2filt(1:end-3) '_2.nc']
system(['cp ',file2filt,' ',file_filt]) ;

disp('swrad')
clear var var_filt 
if t==1
var_0  = ncread(file2filt   ,'swrad') ;
var_p1 = ncread(file2filt_p1,'swrad',[1 1 1],[inf inf pas_rad]) ;
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = pas_rad ;
elseif t==length(list)
var_0  = ncread(file2filt   ,'swrad') ;
var_m1 = ncread(file2filt_m1,'swrad',[1 1 NT_m1-pas_rad+1],[inf inf pas_rad]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
else
var_0  = ncread(file2filt   ,'swrad') ;
var_m1 = ncread(file2filt_m1,'swrad',[1 1 NT_m1-pas_rad+1],[inf inf pas_rad]) ;
var_p1 = ncread(file2filt_p1,'swrad',[1 1 1],[inf inf pas_rad]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ; 
end
for it=pas_rad+1:size(var,3)-pas_rad
    istr = istr+1 ;
    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_rad:it+pas_rad),3)) ;
end
ncwrite(file_filt,'swrad',var_filt) ;

disp('lwrad')
clear var var_filt 
if t==1
var_0  = ncread(file2filt   ,'lwrad') ;
var_p1 = ncread(file2filt_p1,'lwrad',[1 1 1],[inf inf pas_rad]) ;
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = pas_rad ;
elseif t==length(list)
var_0  = ncread(file2filt   ,'lwrad') ;
var_m1 = ncread(file2filt_m1,'lwrad',[1 1 NT_m1-pas_rad+1],[inf inf pas_rad]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
else
var_0  = ncread(file2filt   ,'lwrad') ;
var_m1 = ncread(file2filt_m1,'lwrad',[1 1 NT_m1-pas_rad+1],[inf inf pas_rad]) ;
var_p1 = ncread(file2filt_p1,'lwrad',[1 1 1],[inf inf pas_rad]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
end
for it=pas_rad+1:size(var,3)-pas_rad
    istr = istr+1 ;
    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_rad:it+pas_rad),3)) ;
end
ncwrite(file_filt,'lwrad',var_filt) ;

%disp('uwnd')
%clear var var_filt
%if t==1
%var_0  = ncread(file2filt   ,'uwnd') ;
%var_p1 = ncread(file2filt_p1,'uwnd',[1 1 1],[inf inf pas_wnd]) ;
%var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = pas_wnd ;
%elseif t==length(list)
%var_0  = ncread(file2filt   ,'uwnd') ;
%var_m1 = ncread(file2filt_m1,'uwnd',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
%var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = 0 ;
%else
%var_0  = ncread(file2filt   ,'uwnd') ;
%var_m1 = ncread(file2filt_m1,'uwnd',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
%var_p1 = ncread(file2filt_p1,'uwnd',[1 1 1],[inf inf pas_wnd]) ;
%var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = 0 ;
%end
%for it=pas_wnd+1:size(var,3)-pas_wnd
%    istr = istr+1 ;
%    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_wnd:it+pas_wnd),3)) ;
%end
%ncwrite(file_filt,'uwnd',var_filt) ;

%disp('vwnd')
%clear var var_filt
%if t==1
%var_0  = ncread(file2filt   ,'vwnd') ;
%var_p1 = ncread(file2filt_p1,'vwnd',[1 1 1],[inf inf pas_wnd]) ;
%var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = pas_wnd ;
%elseif t==length(list)
%var_0  = ncread(file2filt   ,'vwnd') ;
%var_m1 = ncread(file2filt_m1,'vwnd',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
%var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = 0 ;
%else
%var_0  = ncread(file2filt   ,'vwnd') ;
%var_m1 = ncread(file2filt_m1,'vwnd',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
%var_p1 = ncread(file2filt_p1,'vwnd',[1 1 1],[inf inf pas_wnd]) ;
%var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
%var_filt = var_0 ; istr = 0 ;
%end
%for it=pas_wnd+1:size(var,3)-pas_wnd
%    istr = istr+1 ;
%    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_wnd:it+pas_wnd),3)) ;
%end
%ncwrite(file_filt,'vwnd',var_filt) ;

%disp('rain')
%var_0  = ncread(file2filt   ,'rain') ;
%ncwrite(file_filt,'rain',var_0.*0) ;

disp('Tair')
clear var var_filt
if t==1
var_0  = ncread(file2filt   ,'Tair') ;
var_p1 = ncread(file2filt_p1,'Tair',[1 1 1],[inf inf pas_wnd]) ;
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = pas_wnd ;
elseif t==length(list)
var_0  = ncread(file2filt   ,'Tair') ;
var_m1 = ncread(file2filt_m1,'Tair',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
else
var_0  = ncread(file2filt   ,'Tair') ;
var_m1 = ncread(file2filt_m1,'Tair',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
var_p1 = ncread(file2filt_p1,'Tair',[1 1 1],[inf inf pas_wnd]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
end
for it=pas_wnd+1:size(var,3)-pas_wnd
    istr = istr+1 ;
    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_wnd:it+pas_wnd),3)) ;
end
ncwrite(file_filt,'Tair',var_filt) ;

disp('qair')
clear var var_filt
if t==1
var_0  = ncread(file2filt   ,'qair') ;
var_p1 = ncread(file2filt_p1,'qair',[1 1 1],[inf inf pas_wnd]) ;
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = pas_wnd ;
elseif t==length(list)
var_0  = ncread(file2filt   ,'qair') ;
var_m1 = ncread(file2filt_m1,'qair',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
else
var_0  = ncread(file2filt   ,'qair') ;
var_m1 = ncread(file2filt_m1,'qair',[1 1 NT_m1-pas_wnd+1],[inf inf pas_wnd]) ;
var_p1 = ncread(file2filt_p1,'qair',[1 1 1],[inf inf pas_wnd]) ;
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_filt = var_0 ; istr = 0 ;
end
for it=pas_wnd+1:size(var,3)-pas_wnd
    istr = istr+1 ;
    var_filt(:,:,istr) = squeeze(nanmean(var(:,:,it-pas_wnd:it+pas_wnd),3)) ;
end
ncwrite(file_filt,'qair',var_filt) ;

end




