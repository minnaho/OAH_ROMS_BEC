
figure
hold on
m_proj('mercator','long',[-119.5 -117],'lat',[31.9 34.5]);
for i=1:19
m_plot(lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) ,'.r','markersize',10)
end
text( lon(Isrc(i) , Jsrc(i)) ,lat(Isrc(i) , Jsrc(i)) , num2str(i) )
m_grid('linewi',1,'tickdir','out','FontSize',12,'xtick',3);
m_gshhs_i('patch',[.9 .9 .9]);


