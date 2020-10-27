



%clear all;
%close all;
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

%Isrc = ncread('psource_L2_scv_NewRivers.nc','Isrc') ;
%Jsrc = ncread('psource_L2_scv_NewRivers.nc','Jsrc') ;
%Isrc = ncread('psource_L2_scbV7_CONC.nc','Isrc') ;
%Jsrc = ncread('psource_L2_scbV7_CONC.nc','Jsrc') ;
Isrc = ncread('L2_scb_psourceV12.nc','Isrc') ;
Jsrc = ncread('L2_scb_psourceV12.nc','Jsrc') ;
%Isrc(30+1-1)=Isrc(30+8) ;
%Isrc(30+3-1)=Isrc(38) ;
%Isrc(30+19-1)=Isrc(38) ;
%Isrc(30+61-1)=Isrc(38) ;

%Jsrc(30+1-1)=Jsrc(30+8) ;
%Jsrc(30+3-1)=Jsrc(38) ;
%Jsrc(30+19-1)=Jsrc(38) ;
%Jsrc(30+61-1)=Jsrc(38) ;



% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid/roms_grd.nc';
load_grid_L2_SCB



fig=figure('visible','on','position',[0 0 800 800]);
%% OCSD
                hold on
                m_proj('mercator','long',[-119 -117],'lat',[32.5 34.2]);
                m_pcolor(lon , lat , h) ; shading interp
                m_gshhs_h('patch',[.9 .9 .9]);
                m_grid('linewi',1,'tickdir','out','FontSize',10,'xtick',3);
cmap = cmocean('deep');
colormap(cmap)
caxis([0 150])
title(['C) OCSD'])
set(gca,'fontname','Courier','fontsize',10)
cb=colorbar('horiz','FontSize',10,'fontname','Courier');
p=get(cb,'position');
set(cb,'position',[p(1) p(2)-0.11 p(3) p(4)/3]);
set(gca,'fontname','Courier','fontsize',10)
%for i=1:15
%for i=1:71
for i=1:96
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.r','markersize',15)
m_text(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,num2str(i))
end
for i=97:110
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.y','markersize',15)
m_text(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,num2str(i))
end
for i=111:182
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.b','markersize',15)
m_text(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,num2str(i))
end

return



%% LA
124 : Venice channel
117
127 out of 117

105 (small outfall)
167 out of 105

%% san gabriel
160 on coast
148 out of coast % huge flux of nutrients, huge Qbar and huge Nutrients concentrations
164 sane as 148



return


i=3;
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.r','markersize',15)


% HYPERION 1
Jsrc(19) =Jsrc(3) ; Isrc(19) =  Isrc-1(3) ;
Jsrc(20)=Jsrc(3)-1  ; Isrc(20) =Isrc(3)-1;
Jsrc(21) =Jsrc(3)+1  ; Isrc(21) =Isrc(3)-1;
Jsrc(22) =Jsrc(3)-1  ; Isrc(22) =Isrc(3)+1;
Jsrc(23) =Jsrc(3)-1  ; Isrc(23) =Isrc(3);
%OPTION
%Jsrc(3)-2 Isrc(3)
%Jsrc(3)-2 Isrc(3)-1
%Jsrc(3)-3 Isrc(3)-1
% HYPERION 2
Jsrc(24) =Jsrc(18)  ; Isrc(24) = Isrc(18)+1
Jsrc(25) =Jsrc(18)+1  ; Isrc(25) = Isrc(18)+1
Jsrc(26) =Jsrc(18)-1  ; Isrc(26) = Isrc(18)+1
Jsrc(27) =Jsrc(18)+1  ; Isrc(27) = Isrc(18)

%% JWPCP
Jsrc(52) =Jsrc(43+9-2)  ; Isrc(51) = Isrc(43+7)+1
Jsrc(53) =Jsrc(43+9-2)+1   ; Isrc(52) =Isrc(43+7)+1
Jsrc(54) =Jsrc(43+9-2)+1   ; Isrc(53) =Isrc(43+9-2)-1
Jsrc(55) =Jsrc(43+9-2)+1   ; Isrc(54) =Isrc(43+9-2)
Jsrc(56) =Jsrc(43+9-2)-1   ; Isrc(55) =Isrc(43+9-2)+1

%% OCSD
Jsrc(66) =Jsrc(51+12)   ; Isrc(86) =Isrc(51+12)+1
Jsrc(67) =Jsrc(51+12)+1   ; Isrc(87) =Isrc(51+12)+1
Jsrc(68) =Jsrc(51+12)-1   ; Isrc(88) =Isrc(51+12)+1
Jsrc(69) =Jsrc(51+12)-1   ; Isrc(89) =Isrc(51+12)
Jsrc(70) =Jsrc(51+12)-1   ; Isrc(90) =Isrc(51+12)-1


%% PL SD

Jsrc(91) =Jsrc(56+17)   ; Isrc(91) =Isrc-1(56+17)
Jsrc(92) =Jsrc(56+17)-1   ; Isrc(92) =Isrc(56+17)-1
Jsrc(93) =Jsrc(56+17)+1   ; Isrc(93) =Isrc(56+17)-1
Jsrc(94) =Jsrc(56+17)-1   ; Isrc(94) =Isrc(56+17)+1
Jsrc(95) =Jsrc(56+17)-1   ; Isrc(95) =Isrc(56+17)

Jsrc(96) = Jsrc(71+17)-1   ; Isrc(96) =Isrc(71+17)+1
Jsrc(97) = Jsrc(71+17)+1   ; Isrc(97) =Isrc(71+17)-1




for i=21:44
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.r','markersize',15)
end

for i=45:53
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.r','markersize',15)
end

for i=54:71
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.r','markersize',15)
end


return


%for i=16:16+13
for i=71:71+13
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.g','markersize',15)
end
for i=71+13+1:157
%for i=16+13+1:104
m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.b','markersize',15)
end

%for i=30:40
%m_plot(lon(Jsrc(i),Isrc(i)) , lat(Jsrc(i),Isrc(i)) ,'.y','markersize',15)
%end

for i=1:157
%for i=16+13+1:104
mask_ps(i) = mask(Jsrc(i),Isrc(i))
end

return

%m_plot(lon_psi,lat_psi,'.-k')
%m_plot(lon_psi',lat_psi','.-k')

for i=13:15
m_plot(lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) ,'.r','markersize',10)
end

ax4 = subplot(2,2,4);
%% PLWTP
                hold on
                m_proj('mercator','long',[-117.34 -117.3],'lat',[32.645 32.695]);
                m_pcolor(lon , lat , h) ; shading interp
                m_gshhs_h('patch',[.9 .9 .9]);
                m_grid('linewi',1,'tickdir','out','FontSize',10,'xtick',3);
cmap = cmocean('deep');
colormap(ax4,cmap)
caxis([0 150])
title(['D) PLWTP'])
set(gca,'fontname','Courier','fontsize',10)
cb=colorbar('horiz','FontSize',10,'fontname','Courier');
p=get(cb,'position');
set(cb,'position',[p(1) p(2)-0.11 p(3) p(4)/3]);
set(gca,'fontname','Courier','fontsize',10)
m_plot(lon_psi,lat_psi,'.-k')
m_plot(lon_psi',lat_psi','.-k')
for i=16:19
m_plot(lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) ,'.r','markersize',10)
end

return



