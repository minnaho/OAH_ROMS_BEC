clear all 

rep = '/data/project3/pdamien/ROMS_pdamien/config/IOP2ARCTERX/' ; 
name = 'iop2arcterx_brysmooth';
NZ =100 ;

list = dir([rep name '*.nc']) ; 
list = list(3:end) ; 

for t=4:length(list)-1

file2filt = [list(t).folder '/' list(t).name]
NT_0 = length(ncread(file2filt,'bry_time')) ;  
%if t==1
%   file2filt_m1 = '/paracas/ROMS_SOLUTIONS/PACHUG/YY2013M11/nwpac_bry.00000.nc'
%else
   file2filt_m1 = [list(t-1).folder '/' list(t-1).name];
%end
NT_m1 = length(ncread(file2filt_m1,'bry_time')) ;
%if t==length(list)
%   file2filt_p1 = '/paracas/ROMS_SOLUTIONS/PACHUG/YY2015M02/nwpac_bry.00000.nc'
%else
   file2filt_p1 = [list(t+1).folder '/' list(t+1).name];
%end
NT_p1 = length(ncread(file2filt_p1,'bry_time')) ;

indname = strfind(file2filt,'brysmooth');
file_filt = [rep name '2_' file2filt(indname+10:indname+23) '.nc']
win = 97 ; pas = (win-1)/2 ;

time = ncread(file2filt,'bry_time') ;
NT = length(time) ; 
nccreate(file_filt,'bry_time','Dimensions',{'time',NT},'datatype','double');
ncwrite(file_filt,'bry_time',time)

obcs = {'south','north','east','west'} ; 

for o=1:4

obc = obcs{o} ;

clear zeta_filt vbar_filt ubar_filt vp_filt up_filt
clear temp_filt salt_filt u_filt v_filt

disp(obc)
var_0  = ncread(file2filt   ,['zeta_' obc]) ;
var_m1 = ncread(file2filt_m1,['zeta_' obc],[1 NT_m1-pas+1],[inf pas]) ;
var_p1 = ncread(file2filt_p1,['zeta_' obc],[1 1],[inf pas]) ;
zeta = [var_m1 var_0 var_p1] ;
var_0  = ncread(file2filt   ,['ubar_' obc]) ;
var_m1 = ncread(file2filt_m1,['ubar_' obc],[1 NT_m1-pas+1],[inf pas]) ;
var_p1 = ncread(file2filt_p1,['ubar_' obc],[1 1],[inf pas]) ;
ubar = [var_m1 var_0 var_p1] ;
var_0  = ncread(file2filt   ,['up_' obc]) ;
var_m1 = ncread(file2filt_m1,['up_' obc],[1 NT_m1-pas+1],[inf pas]) ;
var_p1 = ncread(file2filt_p1,['up_' obc],[1 1],[inf pas]) ;
up = [var_m1 var_0 var_p1] ;
var_0  = ncread(file2filt   ,['vbar_' obc]) ;
var_m1 = ncread(file2filt_m1,['vbar_' obc],[1 NT_m1-pas+1],[inf pas]) ;
var_p1 = ncread(file2filt_p1,['vbar_' obc],[1 1],[inf pas]) ;
vbar = [var_m1 var_0 var_p1] ;
var_0  = ncread(file2filt   ,['vp_' obc]) ;
var_m1 = ncread(file2filt_m1,['vp_' obc],[1 NT_m1-pas+1],[inf pas]) ;
var_p1 = ncread(file2filt_p1,['vp_' obc],[1 1],[inf pas]) ;
vp = [var_m1 var_0 var_p1] ;
NX = size(zeta,1) ; 
ind=0;	
for t=pas+1:size(zeta,2)-pas
    ind = ind+1 ;	
    for d=1:size(zeta,1)
    zeta_filt(d,ind) = nanmean(squeeze(zeta(d,t-pas:t+pas))) ;
    end
    for d=1:size(vbar,1)
    vbar_filt(d,ind) = nanmean(squeeze(vbar(d,t-pas:t+pas))) ;
    vp_filt  (d,ind) = nanmean(squeeze(vp  (d,t-pas:t+pas))) ;
    end
    for d=1:size(ubar,1)
    ubar_filt(d,ind) = nanmean(squeeze(ubar(d,t-pas:t+pas))) ;
    up_filt  (d,ind) = nanmean(squeeze(up  (d,t-pas:t+pas))) ;
    end    
end
if (strcmp(obc,'south')==1 || strcmp(obc,'north')==1)
nccreate(file_filt,['zeta_' obc],'Dimensions',{'xi_rho',NX,'time',NT_0},'datatype','double');
nccreate(file_filt,['ubar_' obc],'Dimensions',{'xi_u',NX-1,'time',NT_0},'datatype','double');
nccreate(file_filt,['up_' obc],'Dimensions',{'xi_u',NX-1,'time',NT_0},'datatype','double');
nccreate(file_filt,['vbar_' obc],'Dimensions',{'xi_rho',NX,'time',NT_0},'datatype','double');
nccreate(file_filt,['vp_' obc],'Dimensions',{'xi_rho',NX,'time',NT_0},'datatype','double');
elseif (strcmp(obc,'east')==1 || strcmp(obc,'west')==1)
nccreate(file_filt,['zeta_' obc],'Dimensions',{'eta_rho',NX,'time',NT_0},'datatype','double');
nccreate(file_filt,['ubar_' obc],'Dimensions',{'eta_rho',NX,'time',NT_0},'datatype','double');
nccreate(file_filt,['up_' obc],'Dimensions',{'eta_rho',NX,'time',NT_0},'datatype','double');
nccreate(file_filt,['vbar_' obc],'Dimensions',{'eta_v',NX-1,'time',NT_0},'datatype','double');
nccreate(file_filt,['vp_' obc],'Dimensions',{'eta_v',NX-1,'time',NT_0},'datatype','double');
else
	disp('ERROR dimension ') ; stop ;
end
ncwrite(file_filt,['zeta_' obc],zeta_filt)
ncwrite(file_filt,['ubar_' obc],ubar_filt)
ncwrite(file_filt,['up_' obc]  ,up_filt  )
ncwrite(file_filt,['vbar_' obc],vbar_filt)
ncwrite(file_filt,['vp_' obc]  ,vp_filt  )


if (strcmp(obc,'south')==1 || strcmp(obc,'north')==1)
nccreate(file_filt,['temp_' obc],'Dimensions',{'xi_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['salt_' obc],'Dimensions',{'xi_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['u_' obc],'Dimensions',{'xi_u',NX-1,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['v_' obc],'Dimensions',{'xi_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
elseif (strcmp(obc,'east')==1 || strcmp(obc,'west')==1)
nccreate(file_filt,['temp_' obc],'Dimensions',{'eta_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['salt_' obc],'Dimensions',{'eta_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['u_' obc],'Dimensions',{'eta_rho',NX,'s_rho',NZ,'time',NT_0},'datatype','double');
nccreate(file_filt,['v_' obc],'Dimensions',{'eta_v',NX-1,'s_rho',NZ,'time',NT_0},'datatype','double');
else
        disp('ERROR dimension 2') ; stop ;
end
for z=1:NZ
disp(['--> ' num2str(z)	'/' num2str(NZ)])
var_0  = ncread(file2filt   ,['temp_' obc],[1 z 1],[inf 1 inf]) ;
var_m1 = ncread(file2filt_m1,['temp_' obc],[1 z NT_m1-pas+1],[inf 1 pas]) ;
var_p1 = ncread(file2filt_p1,['temp_' obc],[1 z 1],[inf 1 pas]) ;
temp = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_0  = ncread(file2filt   ,['salt_' obc],[1 z 1],[inf 1 inf]) ;
var_m1 = ncread(file2filt_m1,['salt_' obc],[1 z NT_m1-pas+1],[inf 1 pas]) ;
var_p1 = ncread(file2filt_p1,['salt_' obc],[1 z 1],[inf 1 pas]) ;
salt = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_0  = ncread(file2filt   ,['u_' obc],[1 z 1],[inf 1 inf]) ;
var_m1 = ncread(file2filt_m1,['u_' obc],[1 z NT_m1-pas+1],[inf 1 pas]) ;
var_p1 = ncread(file2filt_p1,['u_' obc],[1 z 1],[inf 1 pas]) ;
u = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
var_0  = ncread(file2filt   ,['v_' obc],[1 z 1],[inf 1 inf]) ;
var_m1 = ncread(file2filt_m1,['v_' obc],[1 z NT_m1-pas+1],[inf 1 pas]) ;
var_p1 = ncread(file2filt_p1,['v_' obc],[1 z 1],[inf 1 pas]) ;
v = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
ind=0;
for t=pas+1:size(zeta,2)-pas
    ind = ind+1 ;
    for d=1:size(zeta,1)
    temp_filt(d,1,ind) = nanmean(squeeze(temp(d,1,t-pas:t+pas))) ;
    salt_filt(d,1,ind) = nanmean(squeeze(salt(d,1,t-pas:t+pas))) ;
    end
    for d=1:size(v,1)
    v_filt  (d,1,ind) = nanmean(squeeze(v  (d,1,t-pas:t+pas))) ;
    end
    for d=1:size(u,1)
    u_filt  (d,1,ind) = nanmean(squeeze(u  (d,1,t-pas:t+pas))) ;
    end
end
ncwrite(file_filt,['temp_' obc],temp_filt,[1 z 1])
ncwrite(file_filt,['salt_' obc],salt_filt,[1 z 1])
ncwrite(file_filt,['u_' obc],u_filt,[1 z 1])
ncwrite(file_filt,['v_' obc],v_filt,[1 z 1])
end

end

end




