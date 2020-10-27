



clear all;
close all;
addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid/roms_grd.nc';
load_grid_L2_SCB


fig=figure('visible','on','position',[0 0 800 800]);
ax1 = subplot(2,2,1);
y=[33.9118 33.9206 33.9017];
x=[-118.521 -118.529 -118.5267];
ly = 33.9253 ;
lx = -118.4348 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
for i=1:length(lx)
        [lplat(i), lplon(i)] = FindCloestPoint_ROMS( lon, lat, lx(i), ly(i), mask ) ;
end

                hold on
%                m_proj('mercator','long',[-118.7 -118.3],'lat',[33.7 34.1]);
                m_proj('mercator','long',[-118.55 -118.5],'lat',[33.88 33.94]);
                m_pcolor(lon , lat , h) ; shading interp
                m_gshhs_h('patch',[.9 .9 .9]);
                m_grid('linewi',1,'tickdir','out','FontSize',10,'xtick',3);
cmap = cmocean('deep');
colormap(ax1,cmap)
caxis([0 100])
title(['A) HTP'])
set(gca,'fontname','Courier','fontsize',10)
cb=colorbar('horiz','FontSize',10,'fontname','Courier');
p=get(cb,'position');
set(cb,'position',[p(1) p(2)-0.11 p(3) p(4)/3]);
set(gca,'fontname','Courier','fontsize',10)
m_plot(lon_psi,lat_psi,'.-k')
m_plot(lon_psi',lat_psi','.-k')
% pipe line
li = m_line([lon(lplon(1),lplat(1))  lon(plon(1),plat(1))] , [lat(lplon(1),lplat(1))  lat(plon(1),plat(1))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(2),plat(2))] , [lat(plon(1),plat(1))  lat(plon(2),plat(2))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(3),plat(3))] , [lat(plon(1),plat(1))  lat(plon(3),plat(3))] ) ;
set(li,'color','k','linewidth',1.5)
Nsrc=9 ;
for i=2:3
        for is=1:Nsrc
          Isrc(is,i-1)= plon(i)+mod(is-1,3)-1;          
          Jsrc(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
	end
end

i=1;
m_plot(lon (plon(i), plat(i)-1) , lat (plon(i), plat(i)-1) ,'.y')
m_plot(lon (plon(i)+1, plat(i)) , lat (plon(i)+1, plat(i)) ,'.y')
% junction point
i=1;
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
% around the diffuser
for i=1:2
        for j=1:Nsrc
        m_plot(lon(Isrc(j,i) , Jsrc(j,i)) , lat(Isrc(j,i) , Jsrc(j,i)) ,'.y','markersize',15)
        end
end
% location of the diffuser
for i=2:length(x)
        m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.r','markersize',25)
end


ax2 = subplot(2,2,2);
%% JWPCP
y=[33.7008 33.700737 33.697917 33.6892 33.695046];  % Y: joint_N N S L: S2 joint_S2
x=[-118.3381 -118.341962 -118.335836 -118.3167 -118.325734];
ly = 33.718374 ;
lx = -118.3214 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
for i=1:length(lx)
        [lplat(i), lplon(i)] = FindCloestPoint_ROMS( lon, lat, lx(i), ly(i), mask ) ;
end
                hold on
                m_proj('mercator','long',[-118.35 -118.3],'lat',[33.67 33.72]);
                m_pcolor(lon , lat , h) ; shading interp
                m_gshhs_h('patch',[.9 .9 .9]);
                m_grid('linewi',1,'tickdir','out','FontSize',10,'xtick',3);
cmap = cmocean('deep');
colormap(ax2,cmap)
caxis([0 100])
title(['B) JWPCP'])
set(gca,'fontname','Courier','fontsize',10)
cb=colorbar('horiz','FontSize',10,'fontname','Courier');
p=get(cb,'position');
set(cb,'position',[p(1) p(2)-0.11 p(3) p(4)/3]);
set(gca,'fontname','Courier','fontsize',10)
m_plot(lon_psi,lat_psi,'.-k')
m_plot(lon_psi',lat_psi','.-k')
Nsrc=9 ;
for i=2:4
        for is=1:Nsrc
          Isrc(is,i-1)= plon(i)+mod(is-1,3)-1;
          Jsrc(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end
% pipe line
li = m_line([lon(lplon(1),lplat(1))  lon(plon(1),plat(1))] , [lat(lplon(1),lplat(1))  lat(plon(1),plat(1))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(2),plat(2))] , [lat(plon(1),plat(1))  lat(plon(2),plat(2))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(3),plat(3))] , [lat(plon(1),plat(1))  lat(plon(3),plat(3))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(lplon(1),lplat(1))  lon(plon(5),plat(5))] , [lat(lplon(1),lplat(1))  lat(plon(5),plat(5))]) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(4),plat(4))  lon(plon(5),plat(5))] , [lat(plon(4),plat(4))  lat(plon(5),plat(5))]) ;
set(li,'color','k','linewidth',1.5)


% junction point: there are two, one for the Y northern shape and one for the L southern shape
i=1;
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
i=5
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
% this is an additional point for the onpipe diffusion
i=5;
m_plot(lon (plon(i)-1, plat(i)) , lat (plon(i)-1, plat(i)) ,'.y')
% around the diffuser
for i=1:3
        for j=1:Nsrc
        m_plot(lon(Isrc(j,i) , Jsrc(j,i)) , lat(Isrc(j,i) , Jsrc(j,i)) ,'.y','markersize',15)
        end
end
% location of the main diffuser
for i=2:length(x)-1
        m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.r','markersize',25)
end

ax3 = subplot(2,2,3) ;
%% OCSD
y=[33.576667 33.575761];  % L: Diffuser junction_point
x=[-118.01 -118.004022];
ly = 33.630784 ;
lx = -117.958027 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
for i=1:length(lx)
        [lplat(i), lplon(i)] = FindCloestPoint_ROMS( lon, lat, lx(i), ly(i), mask ) ;
end
                hold on
                m_proj('mercator','long',[-118.03 -117.98],'lat',[33.56 33.6]);
                m_pcolor(lon , lat , h) ; shading interp
                m_gshhs_h('patch',[.9 .9 .9]);
                m_grid('linewi',1,'tickdir','out','FontSize',10,'xtick',3);
cmap = cmocean('deep');
colormap(ax3,cmap)
caxis([0 150])
title(['C) OCSD'])
set(gca,'fontname','Courier','fontsize',10)
cb=colorbar('horiz','FontSize',10,'fontname','Courier');
p=get(cb,'position');
set(cb,'position',[p(1) p(2)-0.11 p(3) p(4)/3]);
set(gca,'fontname','Courier','fontsize',10)
m_plot(lon_psi,lat_psi,'.-k')
m_plot(lon_psi',lat_psi','.-k')
Nsrc=9 ;
for i=1
        for is=1:Nsrc
          Isrc(is,i)= plon(i)+mod(is-1,3)-1;
          Jsrc(is,i)= plat(i)+floor((is-1)/3)-1 ;
        end
end
% pipe line (OCSD)
li = m_line([lon(lplon(1),lplat(1))  lon(plon(2),plat(2))] , [lat(lplon(1),lplat(1))  lat(plon(2),plat(2))]) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(2),plat(2))] , [lat(plon(1),plat(1))  lat(plon(2),plat(2))]) ;
set(li,'color','k','linewidth',1.5)

% junction point: there are two, one for the Y northern shape and one for the L southern shape (OCSD)
i=1;
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
i=2
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
% around the diffusers
for i=1
        for j=1:Nsrc
        m_plot(lon(Isrc(j,i) , Jsrc(j,i)) , lat(Isrc(j,i) , Jsrc(j,i)) ,'.y','markersize',15)
        end
end
% location of the main diffusers
for i=1
        m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.r','markersize',25)
end


ax4 = subplot(2,2,4);
%% PLWTP
y=[32.665245 32.671671 32.658294];
x=[-117.323336 -117.325556 -117.324932];
ly = 32.679822 ;
lx = -117.246105 ;
for i=1:length(x)
        [plat(i), plon(i)] = FindCloestPoint_ROMS( lon, lat, x(i), y(i), mask ) ;
end
for i=1:length(lx)
        [lplat(i), lplon(i)] = FindCloestPoint_ROMS( lon, lat, lx(i), ly(i), mask ) ;
end

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
% pipe line
li = m_line([lon(lplon(1),lplat(1))  lon(plon(1),plat(1))] , [lat(lplon(1),lplat(1))  lat(plon(1),plat(1))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(2),plat(2))] , [lat(plon(1),plat(1))  lat(plon(2),plat(2))] ) ;
set(li,'color','k','linewidth',1.5)
li = m_line([lon(plon(1),plat(1))  lon(plon(3),plat(3))] , [lat(plon(1),plat(1))  lat(plon(3),plat(3))] ) ;
set(li,'color','k','linewidth',1.5)
Nsrc=9 ;
for i=2:3
        for is=1:Nsrc
          Isrc(is,i-1)= plon(i)+mod(is-1,3)-1;
          Jsrc(is,i-1)= plat(i)+floor((is-1)/3)-1 ;
        end
end
i=1;
% junction point
i=1;
m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.k','markersize',20)
% around the diffuser
for i=1:2
        for j=1:Nsrc
        m_plot(lon(Isrc(j,i) , Jsrc(j,i)) , lat(Isrc(j,i) , Jsrc(j,i)) ,'.y','markersize',15)
        end
end
% location of the main diffuser
for i=2:3
        m_plot(lon(plon(i), plat(i)) , lat(plon(i), plat(i)) ,'.r','markersize',25)
end


return



