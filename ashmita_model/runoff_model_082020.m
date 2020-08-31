

load precipitations.txt
index_runoff = precipitations(1,4:end) ;
prec = precipitations(2:end,4:end) ;
year  =  precipitations(2:end,3);
month =  precipitations(2:end,1);
day   =  precipitations(2:end,2);
time = datenum(year,month,day);
prec(prec==0)=NaN ;
prec(prec<0.5)=NaN ;
coef = 0.06 ;


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








