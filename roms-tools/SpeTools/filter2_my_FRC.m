clear all 

rep = '/data/project3/pdamien/ROMS_pdamien/config/KUROSHIO/' ; 
name = 'kuroshio200m_frcsmooth';

list = dir([rep name '*.nc']) 
%list = list(3:end) ; 

for t=1:length(list)

file2filt = [list(t).folder '/' list(t).name]
NT_0 = length(ncread(file2filt,'time')) ;  
if t==1
   file2filt_m1 = [];
else
   file2filt_m1 = [list(t-1).folder '/' list(t-1).name];
   NT_m1 = length(ncread(file2filt_m1,'time')) ;
end
if t==length(list)
   file2filt_p1 = [];
else
   file2filt_p1 = [list(t+1).folder '/' list(t+1).name];
   NT_p1 = length(ncread(file2filt_p1,'time')) ;
end

win = 73 ; pas = (win-1)/2 ;

disp('uwnd')
if t==1
var_m1 = [] ; 
else
var_m1 = ncread(file2filt_m1,'uwnd',[1 1 NT_m1-pas+1],[inf inf pas]) ;
end
var_0  = ncread(file2filt   ,'uwnd') ;
if t==length(list)
var_p1 = [] ;
else
var_p1 = ncread(file2filt_p1,'uwnd',[1 1 1],[inf inf pas]) ;
end
if t==1
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
elseif t==length(list)
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
else
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ; 
end
ind=0;
for ti=pas+1:size(var,3)-pas
    ind = ind+1 ;
    var_filt(:,:,ind) = squeeze(nanmean(var(:,:,ti-pas:ti+pas),3)) ;
end
if t==1
   ncwrite(file2filt,'uwnd',var_filt,[1 1 pas+1]);
else
   ncwrite(file2filt,'uwnd',var_filt,[1 1 1]) ;
end

disp('vwnd')
if t==1
var_m1 = [] ;
else
var_m1 = ncread(file2filt_m1,'vwnd',[1 1 NT_m1-pas+1],[inf inf pas]) ;
end
var_0  = ncread(file2filt   ,'vwnd') ;
if t==length(list)
var_p1 = [] ;
else
var_p1 = ncread(file2filt_p1,'vwnd',[1 1 1],[inf inf pas]) ;
end
if t==1
var = permute([permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
elseif t==length(list)
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2])],[1 3 2]) ;
else
var = permute([permute(var_m1,[1 3 2]) permute(var_0,[1 3 2]) permute(var_p1,[1 3 2])],[1 3 2]) ;
end
ind=0;
for ti=pas+1:size(var,3)-pas
    ind = ind+1 ;
    var_filt(:,:,ind) = squeeze(nanmean(var(:,:,ti-pas:ti+pas),3)) ;
end
if t==1
   ncwrite(file2filt,'vwnd',var_filt,[1 1 pas+1]);
else
   ncwrite(file2filt,'vwnd',var_filt,[1 1 1]) ;
end


end




