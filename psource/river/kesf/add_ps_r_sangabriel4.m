
tot = psNOW+num+3 ;
newnum = psNOW+1+51 ;
Dsrc(newnum) = 2;

%% additional cells for san gabriel river
Dsrc(tot+1) = Dsrc(newnum);
Dsrc(tot+2) = Dsrc(newnum);
Dsrc(tot+3) = Dsrc(newnum);
Dsrc(tot+4) = Dsrc(newnum);

Isrc(tot+1) = Isrc(newnum)-1;
Jsrc(tot+1) = Jsrc(newnum)+2;

Isrc(tot+2) = Isrc(newnum)-1;
Jsrc(tot+2) = Jsrc(newnum)+1;

Isrc(tot+3) = Isrc(newnum)-1;
Jsrc(tot+3) = Jsrc(newnum);

Isrc(tot+4) = Isrc(newnum)-1;
Jsrc(tot+4) = Jsrc(newnum)-1;

Isrc(newnum) = Isrc(newnum)-1; % change the main cell
Jsrc(newnum) = Jsrc(newnum)-2; % change the main cell

Qshape(:,tot+1) = Qshape(:,newnum) ;
Qshape(:,tot+2) = Qshape(:,newnum) ;
Qshape(:,tot+3) = Qshape(:,newnum) ;
Qshape(:,tot+4) = Qshape(:,newnum) ;

Qbar(:,tot+1) = Qbar(:,newnum)./5 ;
Qbar(:,tot+2) = Qbar(:,newnum)./5 ;
Qbar(:,tot+3) = Qbar(:,newnum)./5 ;
Qbar(:,tot+4) = Qbar(:,newnum)./5 ;
Qbar(:,newnum) = Qbar(:,newnum)./5 ;

DIC(:,tot+1) = DIC(:,newnum) ;
DIC(:,tot+2) = DIC(:,newnum) ;
DIC(:,tot+3) = DIC(:,newnum) ;
DIC(:,tot+4) = DIC(:,newnum) ;

temp(:,tot+1) = temp(:,newnum) ;
temp(:,tot+2) = temp(:,newnum) ;
temp(:,tot+3) = temp(:,newnum) ;
temp(:,tot+4) = temp(:,newnum) ;

salt(:,tot+1) = salt(:,newnum) ;
salt(:,tot+2) = salt(:,newnum) ;
salt(:,tot+3) = salt(:,newnum) ;
salt(:,tot+4) = salt(:,newnum) ;

PO4(:,tot+1) = PO4(:,newnum) ;
PO4(:,tot+2) = PO4(:,newnum) ;
PO4(:,tot+3) = PO4(:,newnum) ;
PO4(:,tot+4) = PO4(:,newnum) ;

NO3(:,tot+1) = NO3(:,newnum) ;
NO3(:,tot+2) = NO3(:,newnum) ;
NO3(:,tot+3) = NO3(:,newnum) ;
NO3(:,tot+4) = NO3(:,newnum) ;


NH4(:,tot+1) = NH4(:,newnum) ;
NH4(:,tot+2) = NH4(:,newnum) ;
NH4(:,tot+3) = NH4(:,newnum) ;
NH4(:,tot+4) = NH4(:,newnum) ;

Fe(:,tot+1) = Fe(:,newnum) ;
Fe(:,tot+2) = Fe(:,newnum) ;
Fe(:,tot+3) = Fe(:,newnum) ;
Fe(:,tot+4) = Fe(:,newnum) ;

O2(:,tot+1) = O2(:,newnum) ;
O2(:,tot+2) = O2(:,newnum) ;
O2(:,tot+3) = O2(:,newnum) ;
O2(:,tot+4) = O2(:,newnum) ;

Alk(:,tot+1) = Alk(:,newnum) ;
Alk(:,tot+2) = Alk(:,newnum) ;
Alk(:,tot+3) = Alk(:,newnum) ;
Alk(:,tot+4) = Alk(:,newnum) ;

DOC(:,tot+1) = DOC(:,newnum) ;
DOC(:,tot+2) = DOC(:,newnum) ;
DOC(:,tot+3) = DOC(:,newnum) ;
DOC(:,tot+4) = DOC(:,newnum) ;

DON(:,tot+1) = DON(:,newnum) ;
DON(:,tot+2) = DON(:,newnum) ;
DON(:,tot+3) = DON(:,newnum) ;
DON(:,tot+4) = DON(:,newnum) ;

DOP(:,tot+1) = DOP(:,newnum) ;
DOP(:,tot+2) = DOP(:,newnum) ;
DOP(:,tot+3) = DOP(:,newnum) ;
DOP(:,tot+4) = DOP(:,newnum) ;

NO2(:,tot+1) = NO2(:,newnum) ;
NO2(:,tot+2) = NO2(:,newnum) ;
NO2(:,tot+3) = NO2(:,newnum) ;
NO2(:,tot+4) = NO2(:,newnum) ;

SIO4(:,tot+1) = SIO4(:,newnum) ;
SIO4(:,tot+2) = SIO4(:,newnum) ;
SIO4(:,tot+3) = SIO4(:,newnum) ;
SIO4(:,tot+4) = SIO4(:,newnum) ;
