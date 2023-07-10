
%% DATA BIO RIVIERES AU SUD
% cd('E:\Postdoc\data\rivers\Kristassites')
cd('D:\Postdoc\data\rivers\Kristassites')
% rep_graph = 'E:\Postdoc\data\rivers\GRAPH\' ;
rep_graph = 'D:\Postdoc\data\rivers\\GRAPH\' ;
load('AlisonCreek_discharge.txt')
load('Escandido_alkalinity.txt')
load('Escandido_DOC.txt')
load('Escandido_N.txt')
load('Escandido_NH3.txt')
load('Escandido_O.txt')
load('Escandido_P.txt')
load('Escandido_pH.txt')
load('Escandido_sal.txt')
load('Escandido_T.txt')
load('LosAngelesRiver_all.txt')
% load('D:\Postdoc\data\rivers\Kristassites\LosAngelesRiver_discharge2.txt')
load('LosPanasquitos_discharge.txt')
load('SanDiegoRiver_alkalinity.txt')
load('SanDiegoRiver_discharge.txt')
load('SanDiegoRiver_DOC.txt')
load('SanDiegoRiver_PH.txt')
load('SanDiegoRiver_N.txt')
load('SanDiegoRiver_O.txt')
load('SanDiegoRiver_P.txt')
load('SanGabrielRiver_all.txt')
load('SanGabrielRiver_discharge.txt')
load('SanJoseCreek_all.txt')
load('SanJoseCreek_discharge.txt')
load('SanJuanCreek_all.txt')
load('SanJuanCreek_discharge.txt')
load('SanLuisReyRiver_alkalinity.txt')
load('SanLuisReyRiver_C.txt')
load('SanLuisReyRiver_discharge.txt')
load('SanLuisReyRiver_N.txt')
load('SanLuisReyRiver_O.txt')
load('SanLuisReyRiver_P.txt')
load('SanLuisReyRiver_pH.txt')
load('SanLuisReyRiver_sal.txt')
load('SanMateoCanyon_discharge.txt')
load('SanMateoCanyon_O.txt')
load('SanMateoCanyon_ph.txt')
load('SantaClaraRiver_discharge.txt')
load('VenturaRiver_discharge.txt')

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%% discharge %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

discharge1 = AlisonCreek_discharge(:,4).*0.0283168 ;
discharge2 = LosPanasquitos_discharge(:,4).*0.0283168 ;
discharge3 = SanDiegoRiver_discharge(:,4).*0.0283168 ;
discharge4 = SanGabrielRiver_discharge(:,4).*0.0283168 ;
discharge5 = SanJoseCreek_discharge(:,4).*0.0283168 ;
discharge6 = SanLuisReyRiver_discharge(:,4).*0.0283168 ;
discharge7 = SanMateoCanyon_discharge(:,4).*0.0283168 ;
discharge8 = SantaClaraRiver_discharge(:,4).*0.0283168 ;
discharge9 = VenturaRiver_discharge(:,4).*0.0283168 ;
discharge10 = LosAngelesRiver_discharge2(:,4).*0.0283168 ;

day1 = AlisonCreek_discharge(:,2) ;
day2 = LosPanasquitos_discharge(:,2) ;
day3 = SanDiegoRiver_discharge(:,2) ;
day4 = SanGabrielRiver_discharge(:,2) ;
day5 = SanJoseCreek_discharge(:,2) ;
day6 = SanLuisReyRiver_discharge(:,2) ;
day7 = SanMateoCanyon_discharge(:,2) ;
day8 = SantaClaraRiver_discharge(:,2) ;
day9 = VenturaRiver_discharge(:,2) ;
day10 = LosAngelesRiver_discharge2(:,2) ;

month1 = AlisonCreek_discharge(:,1) ;
month2 = LosPanasquitos_discharge(:,1) ;
month3 = SanDiegoRiver_discharge(:,1) ;
month4 = SanGabrielRiver_discharge(:,1) ;
month5 = SanJoseCreek_discharge(:,1) ;
month6 = SanLuisReyRiver_discharge(:,1) ;
month7 = SanMateoCanyon_discharge(:,1) ;
month8 = SantaClaraRiver_discharge(:,1) ;
month9 = VenturaRiver_discharge(:,1) ;
month10 = LosAngelesRiver_discharge2(:,1) ;

year1 = AlisonCreek_discharge(:,3) ;
year2 = LosPanasquitos_discharge(:,3) ;
year3 = SanDiegoRiver_discharge(:,3) ;
year4 = SanGabrielRiver_discharge(:,3) ;
year5 = SanJoseCreek_discharge(:,3) ;
year6 = SanLuisReyRiver_discharge(:,3) ;
year7 = SanMateoCanyon_discharge(:,3) ;
year8 = SantaClaraRiver_discharge(:,3) ;
year9 = VenturaRiver_discharge(:,3) ;
year10 = LosAngelesRiver_discharge2(:,3) ;

disch_date1 = datenum(year1,month1,day1) ;
disch_date2 = datenum(year2,month2,day2) ;
disch_date3 = datenum(year3,month3,day3) ;
disch_date4 = datenum(year4,month4,day4) ;
disch_date5 = datenum(year5,month5,day5) ;
disch_date6 = datenum(year6,month6,day6) ;
disch_date7 = datenum(year7,month7,day7) ;
disch_date8 = datenum(year8,month8,day8) ;
disch_date9 = datenum(year9,month9,day9) ;
disch_date10 = datenum(year10,month10,day10) ;

%% GRAPHS

%% 

date_all = {disch_date1 disch_date2 disch_date3 disch_date4 disch_date5...
    disch_date6 disch_date7 disch_date8 disch_date9 disch_date10} ;
discharge_all = {discharge1 discharge2 discharge3 discharge4 discharge5 discharge6...
    discharge7 discharge8 discharge9 discharge10} ;
title_all = {'Alison Creek' 'Los Panasquitos' 'San Diego River' 'San Gabriel River' ...
    'San Jose Creek' 'San Luis Rey River' 'San Mateo Canyon' 'Santa Clara River' 'Ventura River' 'Los Angeles'} ;
% % % 
% % % fig = figure('visible','on') ;
% % % for i=1:9
% % %     subplot(3,3,i)
% % %     plot(date_all{i} , discharge_all{i} ,'-k')
% % %     datetick('x')
% % %     xlim([nanmin(date_all{i}) nanmax(date_all{i})])
% % %     ylim([nanmin(discharge_all{i}) nanmax(discharge_all{i})])
% % % %     set(gca, 'yscale','log')
% % %     title(title_all{i})
% % %     set(gca,'ytick',[0 floor(nanmax(discharge_all{i}))])
% % % end
% % % 
% % % set(gcf,'NextPlot','add');
% % % axes;
% % % h = title('Discharge (m^3/sec)' , 'fontsize',30);
% % % set(gca,'Visible','off');
% % % set(h,'Visible','on');
% % % % set(h,'position',[.4 .9 .5 .1])
% % % 
% % % figure_file_name = [rep_graph , 'SC_Rivers_discharge']; % sans extension
% % % % set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 24 8]); % 
% % % print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
% % % close all


%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%% BIO %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

%% NITROGEN

nitrate1 = Escandido_N(:,5) ;
% nitrate2 = (:,4) ;
% nitrate3 = (:,4) ;
nitrate4 = nanmean([SanDiegoRiver_N(:,5) SanDiegoRiver_N(:,6)],2) ;
nitrate5 = LosAngelesRiver_all(:,19) ;
nitrate6 = SanGabrielRiver_all(:,17) ;
nitrate7 = SanJoseCreek_all(:,19) ;
nitrate9 = nanmean([SanLuisReyRiver_N(:,6) SanLuisReyRiver_N(:,7)],2) ;

nitrite1 = Escandido_N(:,6) ;
% nitrite2 = (:,4) ;
% nitrite3 = (:,4) ;
nitrite4 = SanDiegoRiver_N(:,7) ;
% nitrite5 = LosAngelesRiver_all(:,4) ;
nitrite6 = SanGabrielRiver_all(:,18)-SanGabrielRiver_all(:,17)-SanGabrielRiver_all(:,7) ;
nitrite7 = SanJoseCreek_all(:,17) ;
nitrite9 = nanmean([SanLuisReyRiver_N(:,8) SanLuisReyRiver_N(:,9)],2) ;

ammo1 = nanmean([Escandido_NH3(:,4) Escandido_NH3(:,5)],2) ;
% ammo2 = (:,4) ;
% ammo3 = (:,4) ;
ammo4 = SanDiegoRiver_N(:,4) ;
ammo5 = LosAngelesRiver_all(:,34) ;
ammo6 = SanGabrielRiver_all(:,7) ;
ammo7 = SanJoseCreek_all(:,16) ;
ammo9 = nanmean([SanLuisReyRiver_N(:,4) SanLuisReyRiver_N(:,5)],2) ;

%%

month1 = Escandido_N(:,1) ;
month4 = SanDiegoRiver_N(:,1) ;
month5 = LosAngelesRiver_all(:,1) ;
month6 = SanGabrielRiver_all(:,1) ;
month7 = SanJoseCreek_all(:,1) ;
month9 = SanLuisReyRiver_N(:,1) ;

day1 = Escandido_N(:,2) ;
day4 = SanDiegoRiver_N(:,2) ;
day5 = LosAngelesRiver_all(:,2) ;
day6 = SanGabrielRiver_all(:,2) ;
day7 = SanJoseCreek_all(:,2) ;
day9 = SanLuisReyRiver_N(:,2) ;

year1 = Escandido_N(:,3) ;
year4 = SanDiegoRiver_N(:,3) ;
year5 = LosAngelesRiver_all(:,3) ;
year6 = SanGabrielRiver_all(:,3) ;
year7 = SanJoseCreek_all(:,3) ;
year9 = SanLuisReyRiver_N(:,3) ;

N_date1 = datenum(year1,month1,day1) ;
N_date4 = datenum(year4,month4,day4) ;
N_date5 = datenum(year5,month5,day5) ;
N_date6 = datenum(year6,month6,day6) ;
N_date7 = datenum(year7,month7,day7) ;
N_date9 = datenum(year9,month9,day9) ;

%% PHOS

phos1 = Escandido_P(:,5) ;
% phos2 = (:,4) ;
% phos3 = (:,4) ;
phos4 = SanDiegoRiver_N(:,6) ;
phos5 = LosAngelesRiver_all(:,22) ;
phos6 = SanGabrielRiver_all(:,21) ;
phos7 = SanJoseCreek_all(:,21) ;
phos9 = SanLuisReyRiver_P(:,6) ;

month1 = Escandido_P(:,1) ;
month4 = SanDiegoRiver_P(:,1) ;
month5 = LosAngelesRiver_all(:,1) ;
month6 = SanGabrielRiver_all(:,1) ;
month7 = SanJoseCreek_all(:,1) ;
month9 = SanLuisReyRiver_N(:,1) ;

day1 = Escandido_P(:,2) ;
day4 = SanDiegoRiver_P(:,2) ;
day5 = LosAngelesRiver_all(:,2) ;
day6 = SanGabrielRiver_all(:,2) ;
day7 = SanJoseCreek_all(:,2) ;
day9 = SanLuisReyRiver_P(:,2) ;

year1 = Escandido_P(:,3) ;
year4 = SanDiegoRiver_P(:,3) ;
year5 = LosAngelesRiver_all(:,3) ;
year6 = SanGabrielRiver_all(:,3) ;
year7 = SanJoseCreek_all(:,3) ;
year9 = SanLuisReyRiver_P(:,3) ;

P_date1 = datenum(year1,month1,day1) ;
P_date4 = datenum(year4,month4,day4) ;
P_date5 = datenum(year5,month5,day5) ;
P_date6 = datenum(year6,month6,day6) ;
P_date7 = datenum(year7,month7,day7) ;
P_date9 = datenum(year9,month9,day9) ;

%% SIO3

sil5 = LosAngelesRiver_all(:,29) ;
sil7 = SanJoseCreek_all(:,23) ;

% sil1 = (:,4) ;
% sil2 = (:,4) ;
% sil3 = (:,4) ;
% sil4 = (:,4) ;
day4 = LosAngelesRiver_all(:,2) ;
day5 = SanJoseCreek_all(:,2) ;

month4 = LosAngelesRiver_all(:,1) ;
month5 = SanJoseCreek_all(:,1) ;

year4 = LosAngelesRiver_all(:,3) ;
year5 = SanJoseCreek_all(:,3) ;

Si_date4 = datenum(year4,month4,day4) ;
Si_date5 = datenum(year5,month5,day5) ;

%% DOC

% doc1 = (:,4) ;
% doc2 = (:,4) ;
% doc3 = (:,4) ;
doc4 = SanDiegoRiver_DOC(:,4) ;
doc5 = LosAngelesRiver_all(:,24) ;
don6 = SanGabrielRiver_all(:,18) ;
doc9 = SanLuisReyRiver_C(:,5) ;


month4 = SanDiegoRiver_P(:,1) ;
month5 = LosAngelesRiver_all(:,1) ;
month6 = SanGabrielRiver_all(:,1) ;
month9 = SanLuisReyRiver_N(:,1) ;

day4 = SanDiegoRiver_P(:,2) ;
day5 = LosAngelesRiver_all(:,2) ;
day6 = SanGabrielRiver_all(:,2) ;
day9 = SanLuisReyRiver_P(:,2) ;

year4 = SanDiegoRiver_P(:,3) ;
year5 = LosAngelesRiver_all(:,3) ;
year6 = SanGabrielRiver_all(:,3) ;
year9 = SanLuisReyRiver_P(:,3) ;

D_date4 = datenum(year4,month4,day4) ;
D_date5 = datenum(year5,month5,day5) ;
D_date6 = datenum(year6,month6,day6) ;
D_date9 = datenum(year9,month9,day9) ;

%%


% sal1 = (:,4) ;
% sal2 = (:,4) ;
% sal3 = (:,4) ;
% sal4 = (:,4) ;
% sal5 = (:,4) ;

% sal7 = SanJoseCreek_all(:,4) ;
% sal8 = SanJuanCreek_all(:,4) ;
% sal9 = SanLuisReyRiver_sal(:,4) ;

%% Alkalinity

alk1= Escandido_alkalinity(:,4) ;
alk4 = SanDiegoRiver_alkalinity(:,4) ;
alk6 = SanGabrielRiver_all(:,5) ;
alk7 = SanJoseCreek_all(:,28) ;
alk9 = nanmean([SanLuisReyRiver_alkalinity(:,4) SanLuisReyRiver_alkalinity(:,5)],2) ;

month1 = Escandido_P(:,1) ;
month4 = SanDiegoRiver_P(:,1) ;
month6 = SanGabrielRiver_all(:,1) ;
month7 = SanJoseCreek_all(:,1) ;
month9 = SanLuisReyRiver_N(:,1) ;

day1 = Escandido_P(:,2) ;
day4 = SanDiegoRiver_P(:,2) ;
day6 = SanGabrielRiver_all(:,2) ;
day7 = SanJoseCreek_all(:,2) ;
day9 = SanLuisReyRiver_P(:,2) ;

year1 = Escandido_P(:,3) ;
year4 = SanDiegoRiver_P(:,3) ;
year6 = SanGabrielRiver_all(:,3) ;
year7 = SanJoseCreek_all(:,3) ;
year9 = SanLuisReyRiver_P(:,3) ;

A_date1 = datenum(year1,month1,day1) ;
A_date4 = datenum(year4,month4,day4) ;
A_date6 = datenum(year6,month6,day6) ;
A_date7 = datenum(year7,month7,day7) ;
A_date9 = datenum(year9,month9,day9) ;

%% pH

ph1 = Escandido_pH(:,4) ;
ph4 = SanDiegoRiver_PH(:,4) ;
ph5 = LosAngelesRiver_all(:,9) ;
ph6 = SanGabrielRiver_all(:,23) ;
ph7 = SanJoseCreek_all(:,13) ;
ph9 = SanLuisReyRiver_pH(:,4) ;
ph10 = SanMateoCanyon_ph(:,4) ;

month1 = Escandido_pH(:,1) ;
month4 = SanDiegoRiver_PH(:,1) ;
month5 = LosAngelesRiver_all(:,1) ;
month6 = SanGabrielRiver_all(:,1) ;
month7 = SanJoseCreek_all(:,1) ;
month9 = SanLuisReyRiver_pH(:,1) ;
month10 = SanMateoCanyon_ph(:,1) ;

day1 = Escandido_pH(:,2) ;
day4 = SanDiegoRiver_PH(:,2) ;
day5 = LosAngelesRiver_all(:,2) ;
day6 = SanGabrielRiver_all(:,2) ;
day7 = SanJoseCreek_all(:,2) ;
day9 = SanLuisReyRiver_pH(:,2) ;
day10 = SanMateoCanyon_ph(:,2) ;

year1 = Escandido_pH(:,3) ;
year4 = SanDiegoRiver_PH(:,3) ;
year5 = LosAngelesRiver_all(:,3) ;
year6 = SanGabrielRiver_all(:,3) ;
year7 = SanJoseCreek_all(:,3) ;
year9 = SanLuisReyRiver_pH(:,3) ;
year10 = SanMateoCanyon_ph(:,3) ;

ph_date1 = datenum(year1,month1,day1) ;
ph_date4 = datenum(year4,month4,day4) ;
ph_date5 = datenum(year5,month5,day5) ;
ph_date6 = datenum(year6,month6,day6) ;
ph_date7 = datenum(year7,month7,day7) ;
ph_date9 = datenum(year9,month9,day9) ;
ph_date10 = datenum(year10,month10,day10) ;
%%

oxygen1 = Escandido_O(:,4) ;
% oxygen2 = (:,4) ;
% oxygen3 = (:,4) ;
oxygen4 = SanDiegoRiver_O(:,4) ;
oxygen5 = LosAngelesRiver_all(:,7) ;
oxygen7 = SanJoseCreek_all(:,11) ;
oxygen9 = SanLuisReyRiver_O(:,4) ;
oxygen10 = nanmean([SanMateoCanyon_O(:,4) SanMateoCanyon_O(:,4)],2) ;

month1 = Escandido_P(:,1) ;
month4 = SanDiegoRiver_P(:,1) ;
month5 = LosAngelesRiver_all(:,1) ;
month7 = SanJoseCreek_all(:,1) ;
month9 = SanLuisReyRiver_N(:,1) ;

day1 = Escandido_P(:,2) ;
day4 = SanDiegoRiver_P(:,2) ;
day5 = LosAngelesRiver_all(:,2) ;
day7 = SanJoseCreek_all(:,2) ;
day9 = SanLuisReyRiver_P(:,2) ;

year1 = Escandido_P(:,3) ;
year4 = SanDiegoRiver_P(:,3) ;
year5 = LosAngelesRiver_all(:,3) ;
year7 = SanJoseCreek_all(:,3) ;
year9 = SanLuisReyRiver_P(:,3) ;

O_date1 = datenum(year1,month1,day1) ;
O_date4 = datenum(year4,month4,day4) ;
O_date5 = datenum(year5,month5,day5) ;
O_date7 = datenum(year7,month7,day7) ;
O_date9 = datenum(year9,month9,day9) ;

%%
% %%
% 
% day1 = AlisonCreek_discharge(:,2) ;
% day2 = LosPanasquitos_discharge(:,2) ;
% day3 = SanDiegoRiver_discharge(:,2) ;
% day4 = SanGabrielRiver_discharge(:,2) ;
% day5 = SanJoseCreek_discharge(:,2) ;
% day6 = SanLuisReyRiver_discharge(:,2) ;
% day7 = SanMateoCanyon_discharge(:,2) ;
% day8 = SantaClaraRiver_discharge(:,2) ;
% day9 = VenturaRiver_discharge(:,2) ;
% day10 = VenturaRiver_discharge(:,2) ;
% 
% month1 = AlisonCreek_discharge(:,1) ;
% month2 = LosPanasquitos_discharge(:,1) ;
% month3 = SanDiegoRiver_discharge(:,1) ;
% month4 = SanGabrielRiver_discharge(:,1) ;
% month5 = SanJoseCreek_discharge(:,1) ;
% month6 = SanLuisReyRiver_discharge(:,1) ;
% month7 = SanMateoCanyon_discharge(:,1) ;
% month8 = SantaClaraRiver_discharge(:,1) ;
% month9 = VenturaRiver_discharge(:,1) ;
% month10 = VenturaRiver_discharge(:,1) ;
% 
% year1 = AlisonCreek_discharge(:,3) ;
% year2 = LosPanasquitos_discharge(:,3) ;
% year3 = SanDiegoRiver_discharge(:,3) ;
% year4 = SanGabrielRiver_discharge(:,3) ;
% year5 = SanJoseCreek_discharge(:,3) ;
% year6 = SanLuisReyRiver_discharge(:,3) ;
% year7 = SanMateoCanyon_discharge(:,3) ;
% year8 = SantaClaraRiver_discharge(:,3) ;
% year9 = VenturaRiver_discharge(:,3) ;
% year10 = VenturaRiver_discharge(:,3) ;
% 
% date1 = datenum(year1,month1,day1) ;
% date2 = datenum(year2,month2,day2) ;
% date3 = datenum(year3,month3,day3) ;
% date4 = datenum(year4,month4,day4) ;
% date5 = datenum(year5,month5,day5) ;
% date6 = datenum(year6,month6,day6) ;
% date7 = datenum(year7,month7,day7) ;
% date8 = datenum(year8,month8,day8) ;
% date9 = datenum(year9,month9,day9) ;
% date10 = datenum(year10,month10,day10) ;


%% SUMMARY

[nanmean(nitrate1)  nanmin(nitrate1) nanmax(nitrate1)]
[nanmean(nitrate4)  nanmin(nitrate4) nanmax(nitrate4)]
[nanmean(nitrate6)  nanmin(nitrate6) nanmax(nitrate6)]
[nanmean(nitrate7)  nanmin(nitrate7) nanmax(nitrate7)]
[nanmean(nitrate9)  nanmin(nitrate9) nanmax(nitrate9)]


%% POSITIONS

all_rivers_pos = load('E:\Postdoc\data\rivers\pos_rivers.txt') ;

lat_allrivers_pos = all_rivers_pos(:,1) ;
lon_allrivers_pos = all_rivers_pos(:,2) ;
% num1 = ([267 288 291 292 313 315]-1)' ;
num1 = ([288 291 292 313 315]-1)' ;
num2 = ([300 304 305 311 ]-1)' ;
num12 = ([301 306 310]-1)' ;

%% discharge
% lat_disch(1) = 33.5 ;
% lat_disch(2) = 32.9 ;
% lat_disch(3) = 32.75 ;
% lat_disch(4) = 34 ;
% lat_disch(5) = 34.48 ;
% lat_disch(6) = 33.33 ;
% lat_disch(7) = 33.23 ;
% lat_disch(8) = 34.25 ;
% lat_disch(9) = 34.3 ;
% 
% lon_disch(1) = -117.6 ;
% lon_disch(2) = -117.75 ;
% lon_disch(3) = -117.2 ;
% lon_disch(4) = -118 ;
% lon_disch(5) = -119 ;
% lon_disch(6) = -116.9 ;
% lon_disch(7) = -117.5 ;
% lon_disch(8) = -119 ;
% lon_disch(9) = -119.3 ;

%% rivers model
% C_rivers = load('E:\Postdoc\data\rivers\data from central coast\rivers_central_coast.txt') ;
% C_rivers_pos = load('E:\Postdoc\data\rivers\data from central coast\rivers_central_coast_position.txt') ;

C_rivers = load('C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\data\rivers\data from central coast\rivers_central_coast.txt') ;
C_rivers_pos = load('C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\data\rivers\data from central coast\rivers_central_coast_position.txt') ;

% day = C_rivers(:,2) ;
% month = C_rivers(:,1) ;
% year = C_rivers(:,3) ;
% C_rivers_date = datenum(year,month,day) ;
% variable = C_rivers(:,7) ;
% cfd_measured = C_rivers(:,5) ;
% cfd_modeled = C_rivers(:,6) ;
% load_day = C_rivers(:,8) ;
% Waterbody = C_rivers(:,4) ;
% flow_30 = C_rivers(:,9) ;
% load_30 = C_rivers(:,10) ;

Waterbody_pos = C_rivers_pos(:,1) ;
C_lat_pos = C_rivers_pos(:,4) ;
C_lon_pos = C_rivers_pos(:,5) ;
water_Type = C_rivers_pos(:,2) ;
WbType = C_rivers_pos(:,3) ;


%% FIGURE

fig = figure ('visible','on') ;
hold on
% m_proj('mercator','long',[-123 -116],'lat',[31 38]);      
m_proj('mercator','long',[-121 -117],'lat',[32 35]);      

%       m_plot(C_lon_pos , C_lat_pos ,'.k' ,'markersize',25)

%       m_plot(lon_allrivers_pos , lat_allrivers_pos ,'.k' ,'markersize',15)
      m_plot(lon_allrivers_pos(num1) , lat_allrivers_pos(num1) ,'.b' ,'markersize',25)
      m_plot(lon_allrivers_pos(num2) , lat_allrivers_pos(num2) ,'.g' ,'markersize',25)
      m_plot(lon_allrivers_pos(num12) , lat_allrivers_pos(num12) ,'.r' ,'markersize',25)
      
      h=legend('Modeled','Biogeochemical Insitu','Discharge Insitu','Biogeo and Disch Insitu') ;
      set(h,'location','northeast')
%       m_plot(lon_disch , lat_disch,'.r' ,'markersize',20)

      m_gshhs_h('patch',[.9 .9 .9]);
      m_grid('linewi',1,'tickdir','out','FontSize',9,'xtick',3);

%       m_plot(C_lon_pos , C_lat_pos ,'.k' ,'markersize',25)

      m_plot(lon_allrivers_pos(num1) , lat_allrivers_pos(num1) ,'.b' ,'markersize',25)
      m_plot(lon_allrivers_pos(num2) , lat_allrivers_pos(num2) ,'.g' ,'markersize',25)
      m_plot(lon_allrivers_pos(num12) , lat_allrivers_pos(num12) ,'.r' ,'markersize',25)
      
figure_file_name = [rep_graph , 'Rivers_MAP_Bight']; % sans extension
% figure_file_name = [rep_graph , 'Rivers_MAP']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all

%%
%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%

%% NITRATE
title_all = {'Escandido' , 'LosAngelesRiver' , 'SanDiegoRiver', 'SanGabrielRiver' ,...
    'SanJoseCreek' , 'SanLuisReyRiver' } ;


fig = figure('visible','off') ;
subplot(3,2,1)
box on
hold on
plot(N_date1 , nitrate1 ,'.b','markersize',15)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,2,2)
box on
hold on
plot(N_date4 , nitrate4 ,'.b','markersize',15)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,2,3)
box on
hold on
plot(N_date5 , nitrate5 ,'.b','markersize',15)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,2,4)
box on
hold on
plot(N_date6 , nitrate6 ,'.b','markersize',15)
datetick('x')
title(title_all{4}, 'fontsize',12)

subplot(3,2,5)
box on
hold on
plot(N_date7 , nitrate7 ,'.b','markersize',15)
datetick('x')
title(title_all{5}, 'fontsize',12)

subplot(3,2,6)
box on
hold on
plot(N_date9 , nitrate9 ,'.b','markersize',15)
datetick('x')
title(title_all{6}, 'fontsize',12)


set(gcf,'NextPlot','add');
axes;
h = title('Nitrate (uM)' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_Nitrate']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all


%% NITRITE
title_all = {'Escandido' , 'SanDiegoRiver', 'SanGabrielRiver' ,...
    'SanJoseCreek' , 'SanLuisReyRiver' } ;


fig = figure('visible','off') ;
subplot(3,2,1)
box on
hold on
plot(N_date1 , nitrate1 ,'.b','markersize',15)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,2,2)
box on
hold on
plot(N_date4 , nitrate4 ,'.b','markersize',15)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,2,3)
box on
hold on
plot(N_date6 , nitrate6 ,'.b','markersize',15)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,2,4)
box on
hold on
plot(N_date7 , nitrate7 ,'.b','markersize',15)
datetick('x')
title(title_all{4}, 'fontsize',12)

subplot(3,2,5)
box on
hold on
plot(N_date9 , nitrate9 ,'.b','markersize',15)
datetick('x')
title(title_all{5}, 'fontsize',12)


set(gcf,'NextPlot','add');
axes;
h = title('Nitrite (uM)' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_Nitrite']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all


%% Ammonium
title_all = {'Escandido' ,  'SanDiegoRiver' ,'LosAngelesRiver' , 'SanGabrielRiver' ,...
    'SanJoseCreek' , 'SanLuisReyRiver' } ;


fig = figure('visible','off') ;
subplot(3,2,1)
box on
hold on
plot(N_date1 , ammo1 ,'.b','markersize',15)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,2,2)
box on
hold on
plot(N_date4 , ammo4 ,'.b','markersize',15)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,2,3)
box on
hold on
plot(N_date5 , ammo5 ,'.b','markersize',15)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,2,4)
box on
hold on
plot(N_date6 , ammo6 ,'.b','markersize',15)
datetick('x')
title(title_all{4}, 'fontsize',12)

subplot(3,2,5)
box on
hold on
plot(N_date7 , ammo7 ,'.b','markersize',15)
datetick('x')
title(title_all{5}, 'fontsize',12)

subplot(3,2,6)
box on
hold on
plot(N_date9 , ammo9 ,'.b','markersize',15)
datetick('x')
title(title_all{6}, 'fontsize',12)


set(gcf,'NextPlot','add');
axes;
h = title('Ammonium (uM)' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_Ammonium']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all



%% PHOSPHATE
title_all = {'Escandido' , 'SanDiegoRiver', 'SanGabrielRiver' ,...
    'SanJoseCreek' , 'SanLuisReyRiver' } ;


fig = figure('visible','off') ;
subplot(3,2,1)
box on
hold on
plot(P_date1 , phos1 ,'.b','markersize',15)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,2,2)
box on
hold on
plot(P_date4 , phos4 ,'.b','markersize',15)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,2,3)
box on
hold on
plot(P_date6 , phos6 ,'.b','markersize',15)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,2,4)
box on
hold on
plot(P_date7 , phos7 ,'.b','markersize',15)
datetick('x')
title(title_all{4}, 'fontsize',12)

subplot(3,2,5)
box on
hold on
plot(P_date9 , phos9 ,'.b','markersize',15)
datetick('x')
title(title_all{5}, 'fontsize',12)


set(gcf,'NextPlot','add');
axes;
h = title('Phosphate (uM)' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_Phosphate']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all


%% Discharge
title_all = {'AlisonCreek' , 'LosPanasquitos' , 'SanDiegoRiver', 'SanGabrielRiver' ,...
    'SanJoseCreek' , 'SanLuisReyRiver' , 'SanMateoCanyon' ,...
    'SantaClaraRiver','VenturaRiver' } ;


fig = figure('visible','off') ;
subplot(3,3,1)
box on
hold on
plot(disch_date1 , discharge1 ,'.-b','markersize',5)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,3,2)
box on
hold on
plot(disch_date2 , discharge2 ,'.-b','markersize',5)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,3,3)
box on
hold on
plot(disch_date3 , discharge3 ,'.-b','markersize',5)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,3,4)
box on
hold on
plot(disch_date4 , discharge4 ,'.-b','markersize',5)
datetick('x')
title(title_all{4}, 'fontsize',12)

subplot(3,3,5)
box on
hold on
plot(disch_date5 , discharge5 ,'.-b','markersize',5)
datetick('x')
title(title_all{5}, 'fontsize',12)

subplot(3,3,6)
box on
hold on
plot(disch_date6 , discharge6 ,'.-b','markersize',5)
datetick('x')
title(title_all{6}, 'fontsize',12)

subplot(3,3,7)
box on
hold on
plot(disch_date7 , discharge7 ,'.-b','markersize',5)
datetick('x')
title(title_all{7}, 'fontsize',12)

subplot(3,3,8)
box on
hold on
plot(disch_date8 , discharge8 ,'.-b','markersize',5)
datetick('x')
title(title_all{8}, 'fontsize',12)

subplot(3,3,9)
box on
hold on
plot(disch_date9 , discharge9 ,'.-b','markersize',5)
datetick('x')
title(title_all{9}, 'fontsize',12)

set(gcf,'NextPlot','add');
axes;
h = title('Discharge ()' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_Discharge']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all



%% DOC
title_all = {'SanDiegoRiver' , 'LosAngelesRiver' ,  'SanGabrielRiver' ,...
    'SanLuisReyRiver' } ;


fig = figure('visible','off') ;
subplot(3,2,1)
box on
hold on
plot(D_date4 , ammo4 ,'.b','markersize',15)
datetick('x')
title(title_all{1}, 'fontsize',12)

subplot(3,2,2)
box on
hold on
plot(D_date5 , ammo5 ,'.b','markersize',15)
datetick('x')
title(title_all{2}, 'fontsize',12)

subplot(3,2,3)
box on
hold on
plot(D_date6 , ammo6 ,'.b','markersize',15)
datetick('x')
title(title_all{3}, 'fontsize',12)

subplot(3,2,4)
box on
hold on
plot(D_date9 , ammo9 ,'.b','markersize',15)
datetick('x')
title(title_all{4}, 'fontsize',12)

set(gcf,'NextPlot','add');
axes;
h = title('DOC (uM)' , 'fontsize',12);
set(gca,'Visible','off');
set(h,'Visible','on');

figure_file_name = [rep_graph , 'Rivers_Insitu_DOC']; % sans extension
% set(fig, 'paperunits', 'centimeters', 'paperposition', [0 0 200 140]); % 
print(fig, '-dpng', '-r300', figure_file_name); % résolution et 
close all

