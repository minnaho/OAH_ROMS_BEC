



%clear all;
%close all;
addpath(genpath('/data/project1/kesf/matlab_paths/'))
%addpath('/data/project3/kesf/tools_roms/B2B/packages')
call_ncviewcolors

% input files
grdname = '/data/project4/kesf/ROMS/L2_SCB/grid/roms_grd.nc';
load_grid_L2_SCB


fig=figure('visible','on','position',[0 0 800 800]);
ax1 = subplot(2,2,1);
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
%li = m_line([lon(lplon(1),lplat(1))  lon(plon(1),plat(1))] , [lat(lplon(1),lplat(1))  lat(plon(1),plat(1))] ) ;
%set(li,'color','k','linewidth',1.5)
%li = m_line([lon(plon(1),plat(1))  lon(plon(2),plat(2))] , [lat(plon(1),plat(1))  lat(plon(2),plat(2))] ) ;
%set(li,'color','k','linewidth',1.5)
%li = m_line([lon(plon(1),plat(1))  lon(plon(3),plat(3))] , [lat(plon(1),plat(1))  lat(plon(3),plat(3))] ) ;
%set(li,'color','k','linewidth',1.5)

        for i=1:6
m_plot(lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) ,'.r','markersize',10)
        end


ax2 = subplot(2,2,2);
%% JWPCP
y=[33.7008 33.700737 33.697917 33.6892 33.695046];  % Y: joint_N N S L: S2 joint_S2
x=[-118.3381 -118.341962 -118.335836 -118.3167 -118.325734];
ly = 33.718374 ;
lx = -118.3214 ;
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

for i=7:12;
m_plot(lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) ,'.r','markersize',10)
end

ax3 = subplot(2,2,3) ;
%% OCSD
                hold on
                m_proj('mercator','long',[-118.03 -117.98],'lat',[33.56 33.6]);
                m_proj('mercator','long',[-119 -117.5],'lat',[33.1 34.2]);
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



