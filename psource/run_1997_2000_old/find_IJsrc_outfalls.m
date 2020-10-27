%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% This program is design to 
%% find Isrc and Jsrc for
%% POTW Outfalls
%% L2_SCB (dx = 300m)
%% Faycal Kessouri
%% 05/04/2018
%% SCCWRP/UCLA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% HTP JWPCP OCSD PLWTP

addpath(genpath('/data/project3/kesf/tools_matlab/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid_3/roms_grd.nc';
load_grid_L2_SCB

%% HTP
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[33.9118 33.9206 33.9017];
x=[-118.521 -118.529 -118.5267];
ly = 33.9253 ;
lx = -118.4348 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end

NSRC=9 ;
for i=2:3
        for is=1:NSRC
          Isrc1(is,i-1)= plon(i)+mod(is-1,3)-1;          
          Jsrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
	end
end

%% test duplicate points of main diffusers
        for i=2:3 % test the main diffusers
		for j=1:2 % testing the small diffusers
	        testff = find( Isrc1(:,j)==plon(i) & Jsrc1(:,j)==plat(i)) ;
		if ~isempty(testff)
		testf(i-1,j)=testff ;
		else
		testf(i-1,j)=NaN ;
		end
		end
	end
	testf(isnan(testf))=[];
%% end test duplicate point of main diffusers

%% Save all Isrc and Jsrc
%% two main diffusers
Isrc(1,1:2) = plon(2:3) ; Jsrc(1,1:2) = plat(2:3) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Isrc(1,3:6) = Isrc1(1:testf(1)-1,1) ; Jsrc(1,3:6) = Jsrc1(1:testf(1)-1,1) ;
Isrc(1,7:10) = Isrc1(testf(1)+1:end,1) ; Jsrc(1,7:10) = Jsrc1(testf(1)+1:end,1) ;
% surrounded south diffuser  & remove 5th because it represents the main diffuser
Isrc(1,11:14) = Isrc1(1:testf(2)-1,2) ; Jsrc(1,11:14) = Jsrc1(1:testf(2)-1,2) ;
Isrc(1,15:18) = Isrc1(testf(2)+1:end,2) ; Jsrc(1,15:18) = Jsrc1(testf(2)+1:end,2) ;
% add two small diffusers on the pipe's legs
Jsrc(1,19) = plat(1)-1 ; Isrc(1,19) = plon(1) ;
Jsrc(1,20) = plat(1) ;   Isrc(1,20) = plon(1)+1 ;


%% JWPCP
clear Isrc1 Jsrc1 plat plon x y NSRC

y=[33.7008 33.700737 33.697917 33.6892 33.695046];  % Y: joint_N N S L: S2 joint_S2
x=[-118.3381 -118.341962 -118.335836 -118.3167 -118.325734];
ly = 33.718374 ;
lx = -118.3214 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
NSRC=9 ;
for i=2:4
        for is=1:NSRC
          Isrc1(is,i-1)= plon(i)+mod(is-1,3)-1;
          Jsrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points & look manually to remove them
for i=1:9
	for j=1:3
	testff = find( Isrc1(i,j)==Isrc1 & Jsrc1(i,j)==Jsrc1) ;
	if size(testff,1)>1;
	testf(i,j) = testff(2) ;
	else
	testf(i,j) = 0;
	end
	end
end

%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,21:23) = plat(2:4) ; Isrc(1,21:23) = plon(2:4) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Isrc(1,24:26) = Isrc1(1:3,1) ; Jsrc(1,24:26) = Jsrc1(1:3,1) ;  % remove 4 same as 2 of second leg & 5 same as main central
Isrc(1,27) = Isrc1(6,1) ; Jsrc(1,27) = Jsrc1(6,1) ;
Isrc(1,28) = Isrc1(9,1) ; Jsrc(1,28) = Jsrc1(9,1) ; % remove 7 same as main & remove 8 same as 6th of leg 2

Isrc(1,29:30) = Isrc1(1:2,2) ; Jsrc(1,29:30) = Jsrc1(1:2,2) ; % remove 3 same as main
Isrc(1,31) = Isrc1(4,2) ; Jsrc(1,31) = Jsrc1(4,2) ;
Isrc(1,32:35) = Isrc1(6:end,2) ; Jsrc(1,32:35) = Jsrc1(6:end,2) ;

% surrounded south diffuser  & remove 5th because it represents the main diffuser
Isrc(1,36:39) = Isrc1(1:4,3) ; Jsrc(1,36:39) = Jsrc1(1:4,3) ;
Isrc(1,40:43) = Isrc1(6:end,3) ; Jsrc(1,40:43) = Jsrc1(6:end,3) ;

% add one small diffusers on the pipe's legs (S)
Jsrc(1,44) = plat(5) ; Isrc(1,44) = plon(5)-1 ;


%% OCSD
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[33.576667 33.575761];  % main diffuser is 1 junction is 2 . it's an L shape outfall: Diffuser junction_point
x=[-118.01 -118.004022];
ly = 33.630784 ;
lx = -117.958027 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
NSRC=9 ;
for i=1
        for is=1:NSRC
          Isrc1(is,i)= plon(i)+mod(is-1,3)-1;
          Jsrc1(is,i)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points of main diffusers
clear testf
        for i=1 % test the main diffusers
                for j=1 % testing the small diffusers
                testff = find( Isrc1(:,j)==plon(i) & Jsrc1(:,j)==plat(i)) ;
                if ~isempty(testff)
                testf(i,j)=testff ;
                else
                testf(i,j)=NaN ;
                end
                end
        end
        testf(isnan(testf))=[];
%% end test duplicate point of main diffusers


%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,45) = plat(1) ; Isrc(1,45) = plon(1) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Isrc(1,46:49) = Isrc1(1:testf(1)-1,1) ; Jsrc(1,46:49) = Jsrc1(1:testf(1)-1,1) ;
Isrc(1,50:53) = Isrc1(testf(1)+1:end,1) ; Jsrc(1,50:53) = Jsrc1(testf(1)+1:end,1) ;

%% PLWTP
clear Isrc1 Jsrc1 plat plon x y NSRC
y=[32.665245 32.671671 32.658294];
x=[-117.323336 -117.325556 -117.324932];
ly = 32.679822 ;
lx = -117.246105 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
NSRC=9 ;
for i=2:3
        for is=1:NSRC
          Isrc1(is,i-1)= plon(i)+mod(is-1,3)-1;
          Jsrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points of main diffusers
        for i=2:3 % test the main diffusers
                for j=1:2 % testing the small diffusers
                testff = find( Isrc1(:,j)==plon(i) & Jsrc1(:,j)==plat(i)) ;
                if ~isempty(testff)
                testf(i-1,j)=testff ;
                else
                testf(i-1,j)=NaN ;
                end
                end
        end
        testf(isnan(testf))=[];
%% end test duplicate point of main diffusers

%% Save all Isrc and Jsrc
%% two main diffusers
Jsrc(1,54:55) = plat(2:3) ; Isrc(1,54:55) = plon(2:3) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Isrc(1,56:59) = Isrc1(1:testf(1)-1,1) ; Jsrc(1,56:59) = Jsrc1(1:testf(1)-1,1) ;
Isrc(1,60:63) = Isrc1(testf(1)+1:end,1) ; Jsrc(1,60:63) = Jsrc1(testf(1)+1:end,1) ;
% surrounded south diffuser  & remove 5th because it represents the main diffuser
Isrc(1,64:67) = Isrc1(1:testf(2)-1,2) ; Jsrc(1,64:67) = Jsrc1(1:testf(2)-1,2) ;
Isrc(1,68:71) = Isrc1(testf(2)+1:end,2) ; Jsrc(1,68:71) = Jsrc1(testf(2)+1:end,2) ;

clear NSRC

return



