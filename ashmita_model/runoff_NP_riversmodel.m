%% directory for graphics
rep = 'C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\SCCWRP_CLOUD\ANTHROPOGENIC_INPUTS\Rivers\SoCAL\';

rep_data = 'C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\SCCWRP_CLOUD\For_Karen\Runoff_model_all\' ;

%% read the precipitation data
cd([rep_data,'Precip'])

%% 1990
for i=1990:2013
filename = [rep_data,'Precip\AllPrecip_',num2str(i),'.csv'];
delimiter = ',';
formatSpec = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);
%% Close the text file.
fclose(fileID);
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = dataArray{col};
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));
for col=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367]
    % Converts strings in the input cell array to numbers. Replaced non-numeric
    % strings with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1);
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData{row}, regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if any(numbers==',');
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(thousandsRegExp, ',', 'once'));
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric strings to numbers.
            if ~invalidThousandsSeparator;
                numbers = textscan(strrep(numbers, ',', ''), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch me
        end
    end
end
R = cellfun(@(x) ~isnumeric(x) && ~islogical(x),raw); % Find non-numeric cells
raw(R) = {NaN}; % Replace non-numeric cells
AllPrecip{i-1989} = cell2mat(raw);
clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me R;
i
end

%% read the watershed parameters

data_surf = load([rep_data,'Annual total runoff_2.txt']) ;
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

coef = load([rep_data,'Coef.txt']) ;
%coord = load([rep_data,'coordinates_river_mouths.txt']) ;

%lon = coord(:,3) ;
%lat = coord(:,2) ;
%id_rivers = coord(:,1) ;

% %% read the mean annual runoff data
% data_runoff = load([rep_data,'Runoff-rec2.txt']) ;
% index_runoff = data_runoff(1,4:end) ;
% data_runoff2 = data_runoff(2:end ,4:end) ;

%%
% R(:,i) = ag(num(1)).*run.* coef(1) + com(num(1)).*run.* coef(2) + ind(num(1)).*run.* coef(3) +...
%     open(num(1)).*run.* coef(4) + res(num(1)).*run.* coef(5) + other(num(1)).*run.* coef(6) + ...
%     + water(num(1)).*run.* coef(7);
% 
%% name and position and name of rivers where BGD data are available

name{1} = 'Agua Hedionda' ;
name{2} = 'Arroyo Trabuco' ;
name{3} = 'Ballona Creek' ;
name{4} = 'Bolsa Chica Westminster Channel' ;
name{5} = 'Bonita Creek' ;
name{6} = 'Buena Vista' ;
name{7} = 'Calleguas' ;
name{8} = 'Carpinteria' ;
name{9} = 'Chollas Creek' ;
name{10} = 'Costa Mesa Chanel' ;
name{11} = 'Coyote Creek' ;
name{12} = 'Cristianitos Creek' ;
name{13} = 'Devereux Lagoon' ;
name{14} = 'Dominguez' ;
name{15} = 'E Garden Grove Wintersberg Channel' ;
name{16} = 'Escondito Creek' ;
name{17} = 'Goleta Atascadero' ;
name{18} = 'Goleta San Jose' ;
name{19} = 'Goleta Tecolotito' ;
name{20} = 'LA River' ;
name{21} = 'Laguna Canyon' ;
name{22} = 'Las Flores' ;
name{23} = 'Los Penesquitos' ;
name{24} = 'Malibu Creek' ;
name{25} = 'Prima Desch' ;
name{26} = 'Revolon' ;
name{27} = 'San Diego Creek' ;
name{28} = 'San Diego River' ;
name{29} = 'San Dieguito' ;
name{30} = 'San Gabriel River' ;
name{31} = 'San Juan Creek' ;
name{32} = 'San Luis Rey' ;
name{33} = 'San Marcos Creek' ;
name{34} = 'San Mateo' ;
name{35} = 'San Onofre Creek' ;
name{36} = 'San Pedro Creek' ;
name{37} = 'Santa Ana Delhi' ;
name{38} = 'Santa Ana River' ;
name{39} = 'Santa Clara' ;
name{40} = 'Santa Margarita' ;
name{41} = 'Segunda Desch' ;
name{42} = 'Sweetwater' ;
name{43} = 'Tecolote Creek' ;
name{44} = 'Tijuna' ;
name{45} = 'Topanga' ;
name{46} = 'Ventura River' ;
name{47} = 'Zuma Canyon' ;

list(1) = 227 ;
list(2) = 154 ;
list(3) = 85 ;
list(4) = 34 ;
list(5) = 141 ;
list(6) = 221 ;
list(7) = 37 ;
list(8) = 352 ;
list(9) = 287 ;
list(10) = 141 ;
list(11) = 36 ;
list(12) = 174 ;
list(13) = 345 ;
list(14) = 131 ;
list(15) = 34 ;
list(16) = 224 ;
list(17) = 345 ;
list(18) = 345 ;
list(19) = 345 ;
list(20) = 32 ;
list(21) = 176 ;
list(22) = 206 ;
list(23) = 256 ;
list(24) = 71 ;
list(25) = 192 ;
list(26) = 37 ;
list(27) = 141 ;
list(28) = 237 ;
list(29) = 217 ;
list(30) = 36 ;
list(31) = 154 ;
list(32) = 201 ;
list(33) = 225 ;
list(34) = 174 ;
list(35) = 199 ;
list(36) = 345 ;
list(37) = 141 ;
list(38) = 34 ;
list(39) = 45 ;
list(40) = 153 ;
list(41) = 193 ;
list(42) = 257 ;
list(43) = 279 ;
list(44) = 262 ;
list(45) = 86 ;
list(46) = 7 ;
list(47) = 103 ;

%% date

date_all = nan(24,366) ;
for i=1990:2013
   date_all(i-1989,1:length(datenum(i,01,01):datenum(i,12,31))) = datenum(i,01,01):datenum(i,12,31) ; 
end
date_all = date_all' ;
date_all_vec = date_all(:) ;

%%%%%%%%%%%%%%
%%%%%%%%%%%%%%
%% Calculate the runoff using the precipitation
clear R_gr
R_gr = nan(2013-1989 , 366 , 98) ;
for annee = 1990:2013

        RUN = AllPrecip{annee-1989} ;
        RUN = RUN(2:end , 2:end) ;
clear Riv
    for j=1:length(uniq_gr)

            numj = id(gr==uniq_gr(j)) ;
            k = find(gr==uniq_gr(j)) ;
            
            for i=1:length(numj)
                    run = RUN(:,numj(i)) .*1e-2; % cm to m     
                    R(:,i) = ag(k(i)).*run.* coef(1) + com(k(i)).*run.* coef(2) + ind(k(i)).*run.* coef(3) +...
                        open(k(i)).*run.* coef(4) + res(k(i)).*run.* coef(5) + other(k(i)).*run.* coef(6) + ...
                        + water(k(i)).*run.* coef(7) ;
            end   
                  Riv(:,j) = nansum(R,2) ;
            clear run R
    end
    disp(['Year ==>  ',num2str(annee)])
    [xxx yyy] = size(Riv) ;
    R_gr(annee-1989 , 1:xxx , 1:yyy) = Riv ;
end
R_gr = abs(R_gr) ;  % RUNOFF for 98 rivers 24: number of year, 366: numver of days

%% extract runoff only where BGC data are available
data_mean = load([rep_data,'mean_nutrients.txt']) ;
riv_index = data_mean(:,1) ;

for annee = 1990:2013 ;

    for i = 1:size(riv_index)
            num = find(uniq_gr==riv_index(i)) ;
            runoff_BGC(annee-1989,: ,i) = R_gr(annee-1989 , : , num )' ;
     end
end
runoff_BGC(runoff_BGC<0)=NaN ;
runoff_BGC = runoff_BGC./86400 ; % from day to second

%% put the data in one vector per river mouth
runoff_BGC_vec = nan(length(date_all_vec)+1,length(list)+1) ;
runoff_BGC_vec(1,2:length(list)+1) = list ;
runoff_BGC_vec(2:length(date_all_vec)+1,1) = date_all_vec ;

for num=1:size(riv_index)
    R_gr_num = squeeze(runoff_BGC(:,:,num)) ;  
%     R_gr_num_bis = R_gr_num' ;
    R_gr_num_bis = R_gr_num(:) ;
%     R_gr_num_bis(isnan(date_all_vec))=NaN ;
    runoff_BGC_vec(2:length(R_gr_num_bis)+1,num+1) = R_gr_num_bis ;
end

% test
% figure
% hold on
% plot( R_gr_num_bis(:) ,'r')
% plot( R_gr_num(:) ,'b')

%%  Nutrients
%%%%%%%%%%%%
%%%%%%%%%%%%
%% Nutrients and organic matter data in wet weather at dry and wet seasons

dry_tn = data_mean(:,1+1) ;
dry_tp = data_mean(:,2+1) ;
dry_nh4 = data_mean(:,3+1) ;
dry_no3 = data_mean(:,4+1) ;
dry_po4 = data_mean(:,3+1) ;
dry_orgn = dry_tn-(dry_nh4+dry_no3) ;
dry_orgp = dry_tp-dry_po4 ;

wet_tn = data_mean(:,6+1) ;
wet_tp = data_mean(:,5+1) ;
wet_nh4 = data_mean(:,8+1) ;
wet_no3 = data_mean(:,9+1) ;
wet_po4 = data_mean(:,10+1) ;
wet_orgn = wet_tn-(wet_nh4+wet_no3) ;
wet_orgp = wet_tp-wet_po4 ;

%% Reading the data per year throughout two seasons wet-dry-wet

wet_no3bis = wet_no3' ;
dry_no3bis = dry_no3' ;
dry1 = repmat(dry_no3bis, 273-91 ,1)  ;
wet1 = repmat(wet_no3bis, 91 ,1)  ;
wet2 = repmat(wet_no3bis, 366-273 ,1)  ;
mean_no3_conc = [wet1 ; dry1 ; wet2] ;

wet_nh4bis = wet_nh4' ;
dry_nh4bis = dry_nh4' ;
dry1 = repmat(dry_nh4bis, 273-91 ,1)  ;
wet1 = repmat(wet_nh4bis, 91 ,1)  ;
wet2 = repmat(wet_nh4bis, 366-273 ,1)  ;
mean_nh4_conc = [wet1 ; dry1 ; wet2] ;

wet_po4bis = wet_po4' ;
dry_po4bis = dry_po4' ;
dry1 = repmat(dry_po4bis, 273-91 ,1)  ;
wet1 = repmat(wet_po4bis, 91 ,1)  ;
wet2 = repmat(wet_po4bis, 366-273 ,1)  ;
mean_po4_conc = [wet1 ; dry1 ; wet2] ;

wet_tnbis = wet_tn' ;
dry_tnbis = dry_tn' ;
dry1 = repmat(dry_tnbis, 273-91 ,1)  ;
wet1 = repmat(wet_tnbis, 91 ,1)  ;
wet2 = repmat(wet_tnbis, 366-273 ,1)  ;
mean_tn_conc = [wet1 ; dry1 ; wet2] ;

wet_tpbis = wet_tp' ;
dry_tpbis = dry_tp' ;
dry1 = repmat(dry_tpbis, 273-91 ,1)  ;
wet1 = repmat(wet_tpbis, 91 ,1)  ;
wet2 = repmat(wet_tpbis, 366-273 ,1)  ;
mean_tp_conc = [wet1 ; dry1 ; wet2] ;

%% creation a time serie for 24 years (1990-2014)
mean_no3_conc_vecbis = repmat(mean_no3_conc,24,1) ;
no3_conc_vec = nan(length(date_all_vec)+1,length(list)+1) ;
no3_conc_vec(1,2:length(list)+1) = list ;
no3_conc_vec(2:length(date_all_vec)+1,1) = date_all_vec ;
            for i=1:47
               tutu =  mean_no3_conc_vecbis(:,i) ;
               tutu(isnan(date_all_vec))=NaN ;
               no3_conc_vec(2:length(tutu)+1,i+1) = tutu ;
            end
 % nh4 
mean_nh4_conc_vecbis = repmat(mean_nh4_conc,24,1) ;
nh4_conc_vec = nan(length(date_all_vec)+1,length(list)+1) ;
nh4_conc_vec(1,2:length(list)+1) = list ;
nh4_conc_vec(2:length(date_all_vec)+1,1) = date_all_vec ;
            for i=1:47
               tutu =  mean_nh4_conc_vecbis(:,i) ;
               tutu(isnan(date_all_vec))=NaN ;
               nh4_conc_vec(2:length(tutu)+1,i+1) = tutu ;
            end
   
             % po4 
mean_po4_conc_vecbis = repmat(mean_po4_conc,24,1) ;
po4_conc_vec = nan(length(date_all_vec)+1,length(list)+1) ;
po4_conc_vec(1,2:length(list)+1) = list ;
po4_conc_vec(2:length(date_all_vec)+1,1) = date_all_vec ;
            for i=1:47
               tutu =  mean_po4_conc_vecbis(:,i) ;
               tutu(isnan(date_all_vec))=NaN ;
               po4_conc_vec(2:length(tutu)+1,i+1) = tutu ;
            end
             % tn 
mean_tn_conc_vecbis = repmat(mean_tn_conc,24,1) ;
tn_conc_vec = nan(length(date_all_vec)+1,length(list)+1) ;
tn_conc_vec(1,2:length(list)+1) = list ;
tn_conc_vec(2:length(date_all_vec)+1,1) = date_all_vec ;
            for i=1:47
               tutu =  mean_tn_conc_vecbis(:,i) ;
               tutu(isnan(date_all_vec))=NaN ;
               tn_conc_vec(2:length(tutu)+1,i+1) = tutu ;
            end      
           
            % tp 
mean_tp_conc_vecbis = repmat(mean_tp_conc,24,1) ;
tp_conc_vec = nan(length(date_all_vec)+1,length(list)+1) ;
tp_conc_vec(1,2:length(list)+1) = list ;
tp_conc_vec(2:length(date_all_vec)+1,1) = date_all_vec ;
            for i=1:47
               tutu =  mean_tp_conc_vecbis(:,i) ;
               tutu(isnan(date_all_vec))=NaN ;
               tp_conc_vec(2:length(tutu)+1,i+1) = tutu ;
            end       

            
            %% SAVING THE DATA:
           Flow =  runoff_BGC_vec ; % 
           NO3 = no3_conc_vec ;
           NH4 = nh4_conc_vec ;
           PO4 = po4_conc_vec ;
           ON = tn_conc_vec - (no3_conc_vec+nh4_conc_vec)  ;
           OP = tp_conc_vec - po4_conc_vec ;
           ON(ON<0)=NaN ;
           OP(OP<0)=NaN ;
         
           save(['C:\Users\Faycal\Documents\POSTDOC_UCLA_SCCWRP\SCCWRP_CLOUD\ANTHROPOGENIC_INPUTS\Rivers\SoCAL\','SCB_RIVERS.mat'] , ...
               'name','list',...
               'Flow',...
               'NO3','NH4','ON',...
               'PO4','OP') 

%% FIGURES
fig = figure('visible','on') ;
plot(Flow(:,1) , Flow(:,3),'.-')


