addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
call_ncviewcolors
dir_gr = '/data/project3/kesf/tools_matlab/outputs/maps/pteropods/' ;
dir_ =  '/data/project3/kesf/tools_matlab/applications/pteropods/' ;
Severity = ncread([dir_,'pteropods_eggdev.nc'],'Severity') ;

cmin1 = 1 ;
cmax1 = 100 ;
cmin2 = 1 ;
cmax2 = 100 ;
cmin3 = 1 ;
cmax3 = 100 ;
load_grid_ussw1

link_cpt1='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/oc/';
cptc1 = 'radar.cpt' ;

link_cpt2='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/hult/';
cptc2 = 'gr38_hult.cpt' ;

link_cpt3='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/imagej/';
cptc3 = 'cequal.cpt';


fig  = figure('visible','off','position',[0 0 800 450]);

ax1 = subplot (1,3,1);
                hold on
                mapd = Frequency ;
                pcolor(mapd') ; shading flat
%               [c0 z0] = contour(log10(mapd)', [log10(1) log10(3) log10(10)],'-w')
                ylim([20 1000])
                xlim([300 770])
set(gca,'xaxisLocation','top')
caxis([cmin1 cmax1])
title('Frequency')
set(gca, 'fontsize', 11)
cb=colorbar('horiz','FontSize',10);
p=get(cb,'position');
%set(cb,'ytick',([8 12 16 20 24]),'yticklabel',[8 0.2 1 5 10],'tickdir','out');
%set(cb,'ytick',log10([0.1 0.2 1 5 13]),'yticklabel',[0.1 0.2 1 5 13],'tickdir','out');
set(cb,'position',[p(1) p(2)-0.05 p(3) p(4)/3]);
xlabel(cb,'Events')
box on ; set(gca,'linewidth',1)
cptcmap(ax1,[link_cpt1,cptc1])

ax2 = subplot (1,3,2);
                hold on
                mapd = Duration ;
                pcolor(mapd') ; shading flat
%               [c0 z0] = contour(log10(mapd)', [log10(1) log10(3) log10(10)],'-w')
                ylim([20 1000])
                xlim([300 770])
set(gca,'xaxisLocation','top')
caxis([cmin2 cmax2])
title(['{Survival (Juvenil)} ; {Total duration}'])
set(gca, 'fontsize', 11)
cb=colorbar('horiz','FontSize',10);
p=get(cb,'position');
%set(cb,'ytick',([8 12 16 20 24]),'yticklabel',[8 0.2 1 5 10],'tickdir','out');
%set(cb,'ytick',log10([0.1 0.2 1 5 13]),'yticklabel',[0.1 0.2 1 5 13],'tickdir','out');
set(cb,'position',[p(1) p(2)-0.05 p(3) p(4)/3]);
xlabel(cb,'Events')
box on ; set(gca,'linewidth',1)
cptcmap(ax2,[link_cpt2,cptc2])

ax3 = subplot (1,3,3);
                hold on
                mapd = Severity ;
                pcolor(mapd') ; shading flat
%               [c0 z0] = contour(log10(mapd)', [log10(1) log10(3) log10(10)],'-w')
                ylim([20 1000])
                xlim([300 770])
set(gca,'xaxisLocation','top')
caxis([cmin3 cmax3])
title(['Total duration'])
set(gca, 'fontsize', 11)
cb=colorbar('horiz','FontSize',10);
p=get(cb,'position');
%set(cb,'ytick',([8 12 16 20 24]),'yticklabel',[8 0.2 1 5 10],'tickdir','out');
%set(cb,'ytick',log10([0.1 0.2 1 5 13]),'yticklabel',[0.1 0.2 1 5 13],'tickdir','out');
set(cb,'position',[p(1) p(2)-0.05 p(3) p(4)/3]);
xlabel(cb,'Events')
box on ; set(gca,'linewidth',1)
cptcmap(ax3,[link_cpt3,cptc3])

figure_file_name = [dir_gr,'Survival_juvenil'] ;
printpng(figure_file_name)
close all

