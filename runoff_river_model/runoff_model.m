
%cd('C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\SCCWRP_CLOUD\For Karen')

data_surf = load('Annual total runoff_2.txt') ;


gr = data_surf(:,1) ;
uniq_gr = unique(gr) ;
id = data_surf(:,2) ;
uniq_id = unique(id) ;

ag = data_surf(:,3) ;
com = data_surf(:,4) ;
ind = data_surf(:,5) ;
open = data_surf(:,6) ;
res = data_surf(:,7) ;
other = data_surf(:,8) ;
water = data_surf(:,9) ;


load precipitations.txt
index_runoff = precipitations(1,4:end) ;
prec = precipitations(2:end,4:end) ;
year  =  precipitations(2:end,3);
month =  precipitations(2:end,1);
day   =  precipitations(2:end,2);
time = datenum(year,month,day);
prec(prec==0)=NaN ;
prec(prec<0.5)=NaN ;



%coef = load('Coef.txt') ;
%coef = load('Coef_preindustrial.txt') ; % all coefficients as open space
%no3 = rand(224,9) ;
coef = 0.06 ;

data_runoff = load ('Runoff-rec2.txt') ;

index_runoff = data_runoff(1,4:end) ;
data_runoff2 = data_runoff(2:end ,4:end) ;
year = index_runoff(2:end,3) ;
month = index_runoff(2:end,1) ;
day = index_runoff(2:end,2) ;
date = datenum(year,month,day) ; 

for j=1:length(uniq_gr)
    
    kk = uniq_gr(j) ;
    numj = id(gr==j) ;

for i=1:length(numj)

    k = numj(i) ;

    num = find(index_runoff==k) ;
run = data_runoff2(:,num) ;

if isempty (run)

    R(:,i) = nan(365,1);
    R_gr(:,j)  = nan(365,1);
    
else
num = find(id==k) ;

R(:,i) = ag(num(1)).*run.* coef(1) + com(num(1)).*run.* coef(2) + ind(num(1)).*run.* coef(3) +...
    open(num(1)).*run.* coef(4) + res(num(1)).*run.* coef(5) + other(num(1)).*run.* coef(6) + ...
    + water(num(1)).*run.* coef(7);

R_gr(:,j) = nansum(R,2) ;

end
%clear R
end

    
    
end


size(R_gr)








