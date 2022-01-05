
tot = psNOW+num+7 ;
newnum = psNOW+63 ;
Dsrc(newnum) = 2;

%% additional cells for santa margarita river
Dsrc(tot+1) = Dsrc(newnum);
Dsrc(tot+2) = Dsrc(newnum);
Dsrc(tot+3) = Dsrc(newnum);

%% location
Isrc(tot+1) = 552;
Jsrc(tot+1) = 278;

Isrc(tot+2) = 552;
Jsrc(tot+2) = 276;

Isrc(tot+3) = 551;
Jsrc(tot+3) = 275;

Isrc(newnum) = 552; % change main cell
Jsrc(newnum) = 277; % change main cell

Qshape(:,tot+1) = Qshape(:,newnum) ;
Qshape(:,tot+2) = Qshape(:,newnum) ;
Qshape(:,tot+3) = Qshape(:,newnum) ;

Qbar(:,tot+1) = Qbar(:,newnum)./4 ;
Qbar(:,tot+2) = Qbar(:,newnum)./4 ;
Qbar(:,tot+3) = Qbar(:,newnum)./4 ;
Qbar(:,newnum) = Qbar(:,newnum)./4 ;  % change main cell

DIC(:,tot+1) = DIC(:,newnum) ;
DIC(:,tot+2) = DIC(:,newnum) ;
DIC(:,tot+3) = DIC(:,newnum) ;

temp(:,tot+1) = temp(:,newnum) ;
temp(:,tot+2) = temp(:,newnum) ;
temp(:,tot+3) = temp(:,newnum) ;

salt(:,tot+1) = salt(:,newnum) ;
salt(:,tot+2) = salt(:,newnum) ;
salt(:,tot+3) = salt(:,newnum) ;

PO4(:,tot+1) = PO4(:,newnum) ;
PO4(:,tot+2) = PO4(:,newnum) ;
PO4(:,tot+3) = PO4(:,newnum) ;

NO3(:,tot+1) = NO3(:,newnum) ;
NO3(:,tot+2) = NO3(:,newnum) ;
NO3(:,tot+3) = NO3(:,newnum) ;


NH4(:,tot+1) = NH4(:,newnum) ;
NH4(:,tot+2) = NH4(:,newnum) ;
NH4(:,tot+3) = NH4(:,newnum) ;

Fe(:,tot+1) = Fe(:,newnum) ;
Fe(:,tot+2) = Fe(:,newnum) ;
Fe(:,tot+3) = Fe(:,newnum) ;

O2(:,tot+1) = O2(:,newnum) ;
O2(:,tot+2) = O2(:,newnum) ;
O2(:,tot+3) = O2(:,newnum) ;

Alk(:,tot+1) = Alk(:,newnum) ;
Alk(:,tot+2) = Alk(:,newnum) ;
Alk(:,tot+3) = Alk(:,newnum) ;

DOC(:,tot+1) = DOC(:,newnum) ;
DOC(:,tot+2) = DOC(:,newnum) ;
DOC(:,tot+3) = DOC(:,newnum) ;

DON(:,tot+1) = DON(:,newnum) ;
DON(:,tot+2) = DON(:,newnum) ;
DON(:,tot+3) = DON(:,newnum) ;

DOP(:,tot+1) = DOP(:,newnum) ;
DOP(:,tot+2) = DOP(:,newnum) ;
DOP(:,tot+3) = DOP(:,newnum) ;

NO2(:,tot+1) = NO2(:,newnum) ;
NO2(:,tot+2) = NO2(:,newnum) ;
NO2(:,tot+3) = NO2(:,newnum) ;

SIO4(:,tot+1) = SIO4(:,newnum) ;
SIO4(:,tot+2) = SIO4(:,newnum) ;
SIO4(:,tot+3) = SIO4(:,newnum) ;
