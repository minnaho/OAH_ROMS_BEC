
load precipitations.txt
prec = precipitations(2:end,4:end) ;
year  =  precipitations(2:end,3);
month =  precipitations(2:end,1);
day   =  precipitations(2:end,2);
time = datenum(year,month,day);
prec(prec==0)=NaN ;
prec(prec<0.5)=NaN ;


list = [1 365 365*2 365*3 365*4 365*5 365*6 365*7 365*8 365*9 365*10 365*11 365*12 365*13 365*14] ;

for i=1:14
data = prec(list(i):list(i+1) , :);
sdata(1:367,i) = nansum(data,1);
end
sdata(sdata==0)=NaN;

mdata = nanmean(sdata,1);



return

plot(time,prec(:,1))
datetick('x')

