addpath(genpath('/data/project3/kesf/tools_matlab/matlab_paths/'))
call_ncviewcolors
dir_gr = '/data/project3/kesf/tools_matlab/outputs/maps/pteropods/' ;
dir_ =  '/data/project3/kesf/tools_matlab/applications/pteropods/' ;
Frequency = ncread([dir_,'pteropods_eggdev.nc'],'Frequency') ;
Duration = ncread([dir_,'pteropods_eggdev.nc'],'Duration') ;
Severity = ncread([dir_,'pteropods_eggdev.nc'],'Severity') ;

cmin1 = 1 ;
cmax1 = 10 ;
cmin2 = 1 ;
cmax2 = 50 ;
cmin3 = 1 ;
cmax3 = 10 ;
load_grid_ussw1

link_cpt1='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/ncl/';
cptc1 = 'radar.cpt' ;

link_cpt2='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/hult/';
cptc2 = 'gr38_hult.cpt' ;

link_cpt3='/data/project3/kesf/tools_matlab/matlab_paths/cpt_all/imagej/';
cptc3 = 'cequal.cpt';

fig  = figure('visible','on','position',[0 0 800 650]);

ax1 = subplot (1,3,1);
                hold on
                mapd = Frequency ; mapd(mask==0)=NaN;
                pcolor(mapd) ; shading flat
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
cptcmap([link_cpt1,cptc1])
%freezeColors
ax2 = subplot (1,3,2);
                hold on
                mapd = Duration ;mapd(mask==0)=NaN;
                pcolor(mapd) ; shading flat
%               [c0 z0] = contour(log10(mapd)', [log10(1) log10(3) log10(10)],'-w')
                ylim([20 1000])
                xlim([300 770])
set(gca,'xaxisLocation','top')
caxis([cmin2 cmax2])
title(['{Egg development} ; {Total duration}'])
set(gca, 'fontsize', 11)
cb=colorbar('horiz','FontSize',10);
p=get(cb,'position');
%set(cb,'ytick',([8 12 16 20 24]),'yticklabel',[8 0.2 1 5 10],'tickdir','out');
%set(cb,'ytick',log10([0.1 0.2 1 5 13]),'yticklabel',[0.1 0.2 1 5 13],'tickdir','out');
set(cb,'position',[p(1) p(2)-0.05 p(3) p(4)/3]);
xlabel(cb,'Events')
box on ; set(gca,'linewidth',1)
cptcmap([link_cpt2,cptc2])
%freezeColors
ax3 = subplot (1,3,3);
                hold on
                mapd = Severity ; mapd(mask==0)=NaN;
                pcolor(mapd) ; shading flat
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
cptcmap([link_cpt3,cptc3])
%freezeColors
return

figure_file_name = [dir_gr,'EggDev'] ;
printpng(figure_file_name)
close all

