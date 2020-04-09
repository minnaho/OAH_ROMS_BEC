%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% This program is design to 
%% find Jsrc and Isrc for
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
clear Jsrc1 Isrc1 plat plon x y NSRC
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
          Jsrc1(is,i-1)= plon(i)+mod(is-1,3)-1;          
          Isrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
	end
end

%% test duplicate points of main diffusers
        for i=2:3 % test the main diffusers
		for j=1:2 % testing the small diffusers
	        testff = find( Jsrc1(:,j)==plon(i) & Isrc1(:,j)==plat(i)) ;
		if ~isempty(testff)
		testf(i-1,j)=testff ;
		else
		testf(i-1,j)=NaN ;
		end
		end
	end
	testf(isnan(testf))=[];
%% end test duplicate point of main diffusers

%% Save all Jsrc and Isrc
%% two main diffusers
Jsrc(1,1:2) = plon(2:3) ; Isrc(1,1:2) = plat(2:3) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Jsrc(1,3:6) = Jsrc1(1:testf(1)-1,1) ; Isrc(1,3:6) = Isrc1(1:testf(1)-1,1) ;
Jsrc(1,7:10) = Jsrc1(testf(1)+1:end,1) ; Isrc(1,7:10) = Isrc1(testf(1)+1:end,1) ;
% surrounded south diffuser  & remove 5th because it represents the main diffuser
Jsrc(1,11:14) = Jsrc1(1:testf(2)-1,2) ; Isrc(1,11:14) = Isrc1(1:testf(2)-1,2) ;
Jsrc(1,15:18) = Jsrc1(testf(2)+1:end,2) ; Isrc(1,15:18) = Isrc1(testf(2)+1:end,2) ;

% addtional source aroung big pipes AT HYPERION NORTH
Isrc(19) =Isrc(3) ; Jsrc(19) =  Jsrc(3)-1 ;
Isrc(20)=Isrc(3)-1  ; Jsrc(20) =Jsrc(3)-1;
Isrc(21) =Isrc(3)+1  ; Jsrc(21) =Jsrc(3)-1;
Isrc(22) =Isrc(3)-1  ; Jsrc(22) =Jsrc(3)+1;
Isrc(23) =Isrc(3)-1  ; Jsrc(23) =Jsrc(3);
%OPTION
%Isrc(3)-2 Jsrc(3)
%Isrc(3)-2 Jsrc(3)-1
%Isrc(3)-3 Jsrc(3)-1
% HYPERION SOUTH
Isrc(24) =Isrc(18)  ; Jsrc(24) = Jsrc(18)+1 ;
Isrc(25) =Isrc(18)+1  ; Jsrc(25) = Jsrc(18)+1 ;
Isrc(26) =Isrc(18)-1  ; Jsrc(26) = Jsrc(18)+1 ;
Isrc(27) =Isrc(18)+1  ; Jsrc(27) = Jsrc(18) ;
Isrc(28) =Isrc(18)+1  ; Jsrc(28) = Jsrc(18)-1 ;



%% JWPCP
clear Jsrc1 Isrc1 plat plon x y NSRC

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
          Jsrc1(is,i-1)= plon(i)+mod(is-1,3)-1;
          Isrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points & look manually to remove them
for i=1:9
	for j=1:3
	testff = find( Jsrc1(i,j)==Jsrc1 & Isrc1(i,j)==Isrc1) ;
	if size(testff,1)>1;
	testf(i,j) = testff(2) ;
	else
	testf(i,j) = 0;
	end
	end
end

%% Save all Jsrc and Isrc
%% two main diffusers
Isrc(1,29:31) = plat(2:4) ; Jsrc(1,29:31) = plon(2:4) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Jsrc(1,32:34) = Jsrc1(1:3,1) ; Isrc(1,32:34) = Isrc1(1:3,1) ;  % remove 4 same as 2 of second leg & 5 same as main central
Jsrc(1,35) = Jsrc1(6,1) ; Isrc(1,35) = Isrc1(6,1) ;
Jsrc(1,36) = Jsrc1(9,1) ; Isrc(1,36) = Isrc1(9,1) ; % remove 7 same as main & remove 8 same as 6th of leg 2

Jsrc(1,37:38) = Jsrc1(1:2,2) ; Isrc(1,37:38) = Isrc1(1:2,2) ; % remove 3 same as main
Jsrc(1,39) = Jsrc1(4,2) ; Isrc(1,39) = Isrc1(4,2) ;
Jsrc(1,40:43) = Jsrc1(6:end,2) ; Isrc(1,40:43) = Isrc1(6:end,2) ;

% surrounded south diffuser  & remove 5th because it represents the main diffuser
Jsrc(1,44:47) = Jsrc1(1:4,3) ; Isrc(1,44:47) = Isrc1(1:4,3) ;
Jsrc(1,48:51) = Jsrc1(6:end,3) ; Isrc(1,48:51) = Isrc1(6:end,3) ;

%% ADDTIONAL SOURCE AROUND PIPES
Isrc(52) =Isrc(51)  ; Jsrc(52) = Jsrc(51)+1 ;
Isrc(53) =Isrc(51)+1   ; Jsrc(53) =Jsrc(51)+1 ;
Isrc(54) =Isrc(51)+1   ; Jsrc(54) =Jsrc(51)-1 ;
Isrc(55) =Isrc(51)+1   ; Jsrc(55) =Jsrc(51) ;
Isrc(56) =Isrc(51)-1   ; Jsrc(56) =Jsrc(51)+1 ;


%% OCSD
clear Jsrc1 Isrc1 plat plon x y NSRC
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
          Jsrc1(is,i)= plon(i)+mod(is-1,3)-1;
          Isrc1(is,i)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points of main diffusers
clear testf
        for i=1 % test the main diffusers
                for j=1 % testing the small diffusers
                testff = find( Jsrc1(:,j)==plon(i) & Isrc1(:,j)==plat(i)) ;
                if ~isempty(testff)
                testf(i,j)=testff ;
                else
                testf(i,j)=NaN ;
                end
                end
        end
        testf(isnan(testf))=[];
%% end test duplicate point of main diffusers


%% Save all Jsrc and Isrc
%% two main diffusers
Isrc(1,57) = plat(1) ; Jsrc(1,57) = plon(1) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Jsrc(1,58:61) = Jsrc1(1:testf(1)-1,1) ; Isrc(1,58:61) = Isrc1(1:testf(1)-1,1) ;
Jsrc(1,62:65) = Jsrc1(testf(1)+1:end,1) ; Isrc(1,62:65) = Isrc1(testf(1)+1:end,1) ;

%% ADDITIONAL SOURCE AROUND PIPE
Isrc(66) =Isrc(63)+1   ; Jsrc(66) =Jsrc(63) ;
Isrc(67) =Isrc(63)   ; Jsrc(67) =Jsrc(63)-1 ;
Isrc(68) =Isrc(63)+1   ; Jsrc(68) =Jsrc(63)-1 ;
Isrc(69) =Isrc(63)+1   ; Jsrc(69) =Jsrc(63)+1 ;
Isrc(70) =Isrc(63)-1   ; Jsrc(70) =Jsrc(63)-1 ;


%% PLWTP
clear Jsrc1 Isrc1 plat plon x y NSRC
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
          Jsrc1(is,i-1)= plon(i)+mod(is-1,3)-1;
          Isrc1(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end

%% test duplicate points of main diffusers
        for i=2:3 % test the main diffusers
                for j=1:2 % testing the small diffusers
                testff = find( Jsrc1(:,j)==plon(i) & Isrc1(:,j)==plat(i)) ;
                if ~isempty(testff)
                testf(i-1,j)=testff ;
                else
                testf(i-1,j)=NaN ;
                end
                end
        end
        testf(isnan(testf))=[];
%% end test duplicate point of main diffusers

%% Save all Jsrc and Isrc
%% two main diffusers
Isrc(1,71:72) = plat(2:3) ; Jsrc(1,71:72) = plon(2:3) ;
% surrounded north diffuser & remove 5th because it represents the main diffuser
Jsrc(1,73:76) = Jsrc1(1:testf(1)-1,1) ; Isrc(1,73:76) = Isrc1(1:testf(1)-1,1) ;
Jsrc(1,77:80) = Jsrc1(testf(1)+1:end,1) ; Isrc(1,77:80) = Isrc1(testf(1)+1:end,1) ;
% surrounded south diffuser  & remove 5th because it represents the main diffuser
Jsrc(1,81:84) = Jsrc1(1:testf(2)-1,2) ; Isrc(1,81:84) = Isrc1(1:testf(2)-1,2) ;
Jsrc(1,85:88) = Jsrc1(testf(2)+1:end,2) ; Isrc(1,85:88) = Isrc1(testf(2)+1:end,2) ;

Isrc(89) =Isrc(56+17)   ; Jsrc(89) =Jsrc(56+17)-1 ;
Isrc(90) =Isrc(56+17)-1   ; Jsrc(90) =Jsrc(56+17)-1 ;
Isrc(91) =Isrc(56+17)+1   ; Jsrc(91) =Jsrc(56+17)-1 ;
Isrc(92) =Isrc(56+17)-1   ; Jsrc(92) =Jsrc(56+17)+1 ;
Isrc(93) =Isrc(56+17)-1   ; Jsrc(93) =Jsrc(56+17) ;

Isrc(94) = Isrc(71+17)-1   ; Jsrc(94) =Jsrc(71+17)+1 ;
Isrc(95) = Isrc(71+17)+1   ; Jsrc(95) =Jsrc(71+17)-1 ;
Isrc(96) = Isrc(71+17)   ; Jsrc(96) =Jsrc(71+17)+1 ;

clear NSRC

return



