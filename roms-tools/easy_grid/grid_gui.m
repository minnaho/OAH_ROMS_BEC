function grid_gui

 addpath('/data/project9/minnaho/sfbay/ucla-tools/Make_frc/m_map');

 %========================== GLOBAL VARIABLES =================================
 global pi deg2rad rad2deg Eradius
 global nx ny size_x size_y cent_lat taper tra_lat tra_lon rot flip_xy
 global plot_parent icount cstdata projtype
 pi=3.14159265358979323846 ; deg2rad=pi/180.; rad2deg=180/pi;
 Eradius = 6371315.; icount=0; cstdata='coarse'; projtype='Mercator';

 %========================== SCREEN ADJUSTMENT ================================
 set(0,'Units','pixels')
 screen=get(0,'ScreenSize');

 sl = screen(1); % left
 sb = screen(2); % bottom

 sh = 0.9*screen(4);    %% height of the window set as fixed fraction
                        %%                          of the screen height;
 bhgt=40;               %% dialog box height measured in pixels;
 pnlwdth=200;           %% horizontal width of control panel in pixels;
 pnlft=sh+bhgt;         %% left edge of control panel (allowing bhgt-wide
                        %%   interval between map area and control panel);
 sw=pnlft+pnlwdth+bhgt; %% total horizontal width of the entire window;

 pspc = sh/16;          %% vertical spacing between control panel entries;

 %========================== DEFAULT GRID VALUES ==============================
 % Check if settings file exist, if not use the default values
 % to generate a settings file

 if exist('grid_settings.mat','file')
  load('grid_settings');
 else
   disp('Using internal defaults and generating new settings file...')
   nx=1408; ny=768   ; size_x=1400e3  ; size_y=700e3;
   cent_lat=50; taper=0; tra_lat=33.90; tra_lon=-123.11; rot=-49.54;
   flip_xy=0; plot_parent=0;
 end

 %========================== CREATE UI ========================================
 f = figure('Visible','off','Position',[sl,sb,sw,sh]);

%% FIRST GROUP OF CONTROL INPUTS: select projection type, GSHHS coastline
%% resolution, and checkbox to fill land with color (just draw lines is not
%% checked to save time:)

 projpopup=uicontrol('Style','popupmenu', 'String',{ 'Mercator','Lambert', ...
                                 'Stereographic','Satellite','Gnomonic', }, ...
                     'Position',[pnlft,14.8*pspc,pnlwdth, 0.8*bhgt], ...
                     'Callback',@proj_menu_Callback);

 coastpopup=uicontrol('Style','popupmenu', 'String',{ ...
                      'GSHHS coarse', ...
                      'GSHHS low-resolution', ...
                      'GSHHS intermediate', ...
                      'GSHHS high-resolution', ...
                      'GSHHS full-resolution'}, ...
                      'Position',[pnlft,14.2*pspc,pnlwdth, 0.8*bhgt],...
                      'Callback',@popup_menu_Callback);

 fill_land_box=uicontrol('Style','checkbox', ...
                     'Position',[pnlft,          13.6*pspc, bhgt, bhgt],...
                     'Callback',@fill_land_Callback,'Value',0 );
 fill_land_txt=uicontrol('Style','text', ...
  'Position',[pnlft+0.125*pnlwdth, 13.6*pspc-0.25*bhgt, 0.75*pnlwdth, bhgt],...
                     'String','Fill in Land', 'HorizontalAlignment','left');

%% SECOND GROUP: Control parameters for the initial Mercator grid -- number of
%% points and sizes in [km] in both directions; initial latitude of the center,
%% and east-west tapering parameter:


 nx_txt=uicontrol('Style','text', ...
                  'Position',[pnlft,12.7*pspc+0.5*bhgt, 0.48*pnlwdth,bhgt],...
                  'String','nx');
 nx_box=uicontrol('Style','edit', ...
                  'Position',[pnlft, 12.7*pspc, 0.48*pnlwdth, bhgt],...
                  'Callback',@nxbox_Callback,'String',num2str(nx) );

 ny_txt=uicontrol('Style','text', ...
      'Position',[pnlft+0.52*pnlwdth,12.7*pspc+0.5*bhgt,0.48*pnlwdth,bhgt],...
                  'String','ny');
 ny_box=uicontrol('Style','edit', ...
               'Position',[pnlft+0.52*pnlwdth,12.7*pspc,0.48*pnlwdth,bhgt],...
                  'Callback',@nybox_Callback,'String',num2str(ny) );


 sizex_txt=uicontrol('Style','text', ...
                  'Position',[pnlft, 11.7*pspc+0.5*bhgt,0.7*pnlwdth, bhgt],...
                     'String','size_x');
 sizex_box=uicontrol('Style','edit', ...
                     'Position',[pnlft, 11.7*pspc, 0.7*pnlwdth, bhgt], ...
                  'Callback',@sizexbox_Callback,'String',num2str(size_x/1e3) );

 sizey_txt=uicontrol('Style','text', ...
        'Position',[pnlft+0.3*pnlwdth,10.7*pspc+0.5*bhgt,0.7*pnlwdth,bhgt],...
                     'String','size_y');
 sizey_box=uicontrol('Style','edit', ...
                 'Position',[pnlft+0.3*pnlwdth,10.7*pspc,0.7*pnlwdth,bhgt],...
                 'Callback',@sizeybox_Callback,'String',num2str(size_y/1e3) );

 clat_txt=uicontrol('Style','text',...
        'Position',[pnlft+0.2*pnlwdth,9.7*pspc+0.5*bhgt, 0.6*pnlwdth, bhgt],...
                    'String','Center Lat');
 clat_box=uicontrol('Style','edit', ...
                  'Position',[pnlft+0.2*pnlwdth,9.7*pspc, 0.6*pnlwdth,bhgt],...
	          'Callback',@clatbox_Callback, 'String',num2str(cent_lat) );

 taper_txt=uicontrol('Style','text',...
        'Position',[pnlft+0.2*pnlwdth,8.7*pspc+0.5*bhgt, 0.6*pnlwdth, bhgt],...
                    'String','E-W Tapering');
 taper_box=uicontrol('Style','edit', ...
                  'Position',[pnlft+0.2*pnlwdth,8.7*pspc, 0.6*pnlwdth,bhgt],...
                  'Callback',@taperbox_Callback,  'String',num2str(taper) );


%% THIRD GROUP: geographical coordinates of the center at the desired
%% location, azimuthal rotation angle, and flip_xy switch:


 lat_txt=uicontrol('Style','text', ...
                  'Position',[pnlft,7.7*pspc-0.35*bhgt, 0.4*pnlwdth, bhgt],...
                   'String','Latitude', 'HorizontalAlignment','left');
 lat_box=uicontrol('Style','edit', ...
               'Position',[pnlft+0.4*pnlwdth, 7.7*pspc, 0.6*pnlwdth, bhgt],...
                   'Callback',@latbox_Callback,'String',num2str(tra_lat) );

 lon_txt=uicontrol('Style','text', ...
                  'Position',[pnlft, 7.0*pspc-0.35*bhgt, 0.4*pnlwdth, bhgt],...
                   'String','Longitude', 'HorizontalAlignment','left');
 lon_box=uicontrol('Style','edit', ...
                'Position',[pnlft+0.4*pnlwdth, 7.0*pspc, 0.6*pnlwdth, bhgt],...
	           'Callback',@lonbox_Callback,'String',num2str(tra_lon) );

 rot_txt=uicontrol('Style','text', ...
                 'Position',[pnlft, 6.3*pspc-0.35*bhgt, 0.4*pnlwdth, bhgt],...
                   'String','Rotation','HorizontalAlignment','left');
 rot_box=uicontrol('Style','edit', ...
                'Position',[pnlft+0.4*pnlwdth,6.3*pspc, 0.6*pnlwdth, bhgt],...
                 'Callback',@rotbox_Callback, 'String',num2str(rot) );

 flipxy_box=uicontrol('Style','edit', ...
                      'Position',[pnlft,         5.4*pspc, bhgt, bhgt],...
                   'Callback',@flipxybox_Callback,'String',num2str(flip_xy) );
 flipxy_txt=uicontrol('Style','text', ...
       'Position',[pnlft+1.25*bhgt,5.4*pspc-0.25*bhgt, 0.75*pnlwdth, bhgt],...
              'String','flip_xy=0,1,or 2', 'HorizontalAlignment','left');



%% FOURTH GROUP: check box to plot parent grid; buttons to update; save
%% to file, exin, and status panel;

 etopo5_box=uicontrol('Style','checkbox', ...
                     'Position',[pnlft,  4.5*pspc, bhgt, bhgt],...
                     'Callback',@etopo5_box_Callback,'Value',0 );
 etopo5_txt=uicontrol('Style','text', ...
  'Position',[pnlft+0.125*pnlwdth, 4.5*pspc-0.35*bhgt, 0.75*pnlwdth, bhgt],...
                  'String','Put Topography', 'HorizontalAlignment','left');

 pgrid_box=uicontrol('Style','checkbox', ...
                     'Position',[pnlft,          4*pspc, bhgt, bhgt],...
                     'Callback',@pgridbox_Callback,'Value',0 );
 pgrid_txt=uicontrol('Style','text', ...
    'Position',[pnlft+0.125*pnlwdth, 4*pspc-0.35*bhgt, 0.75*pnlwdth, bhgt],...
                   'String','Plot Parent Grid', 'HorizontalAlignment','left');



 hupdate=uicontrol('Style','pushbutton', 'String','Update', ...
                   'Position',[pnlft, 3.25*pspc, pnlwdth,bhgt],...
                   'Callback',@updatebutton_Callback);

 hsave=uicontrol('Style','pushbutton', 'String','Save to File', ...
                 'Position',[pnlft,2.5*pspc, 0.6*pnlwdth,bhgt],...
                 'Callback',@savebutton_Callback);

 hexit=uicontrol('Style','pushbutton', 'String','Brexit', ...
               'Position',[pnlft+0.64*pnlwdth,2.5*pspc, 0.36*pnlwdth,bhgt],...
                 'Callback',@exitbutton_Callback);

 out_txt=uicontrol('Style','text', 'Position',[pnlft,pspc,pnlwdth,2*bhgt],...
                   'String','Output Messages','BackgroundColor',[.8 1 .4]);

%% define square region for map;

 ha = axes('Units','pixels','Position',[sl+60,sb+40, pnlft-bhgt-80, ...
                                                     pnlft-bhgt-80]);

 %========================== INITIALIZE UI ====================================
 % Change units to normalized so components resize automatically.

 f.Units='normalized'             ; ha.Units='normalized';
 projpopup.Units='normalized'     ; coastpopup.Units='normalized';
 fill_land_box.Units='normalized' ; fill_land_txt.Units='normalized';
 nx_box.Units='normalized'        ; nx_txt.Units='normalized';
 ny_box.Units='normalized'        ; ny_txt.Units='normalized';
 sizex_box.Units='normalized'     ; sizex_txt.Units='normalized';
 sizey_box.Units='normalized'     ; sizey_txt.Units='normalized';
 clat_box.Units='normalized'      ; clat_txt.Units='normalized';
 taper_box.Units='normalized'     ; taper_txt.Units='normalized';
 lat_box.Units='normalized'       ; lat_txt.Units='normalized';
 lon_box.Units='normalized'       ; lon_txt.Units='normalized';
 rot_box.Units='normalized'       ; rot_txt.Units='normalized';
 flipxy_box.Units='normalized'    ; flipxy_txt.Units='normalized';
 etopo5_box.Units='normalized'    ; etopo5_txt.Units='normalized';
 pgrid_box.Units='normalized'     ; pgrid_txt.Units='normalized';
 hinit.Units='normalized'         ; hupdate.Units='normalized';
 hsave.Units='normalized'         ; hexit.Units='normalized';
 out_txt.Units='normalized'       ;

 f.Name = 'GRID_GUI';    %% Assign name to appear in the window title.
 movegui(f,'center');    %% Move the window to the center of the screen.
 f.Visible = 'on';       %% Make the window visible.
 ha.Visible = 'off';

 %========================== FUNCTIONS ===================================
                                                           %% Function to
 function updatebutton_Callback(source,eventdata)          %% update grid and
                                                           %% redraw the figure
   projtype=proj_menu_Callback(projpopup,'String');        %% to make it
   cstdata = popup_menu_Callback(coastpopup,'String');     %% consistent with
   fill_land=fill_land_Callback(fill_land_box,'Value');    %% the entered
                                                           %% values
   nx = nxbox_Callback(nx_box,'Value');
   ny = nybox_Callback(ny_box,'Value');
   size_x = sizexbox_Callback(sizex_box,'Value');
   size_y = sizeybox_Callback(sizey_box,'Value');
   cent_lat = clatbox_Callback(clat_box,'Value');
   taper = taperbox_Callback(taper_box, 'Value');

   tra_lat = latbox_Callback(lat_box,'Value');
   tra_lon = lonbox_Callback(lon_box,'Value');
   rot = rotbox_Callback(rot_box,'Value');
   flip_xy = flipxybox_Callback(flipxy_box,'Value');

   fill_hraw = etopo5_box_Callback(etopo5_box,'Value');
   plot_parent = pgridbox_Callback(pgrid_box,'Value');

   tStart = tic;
   [nx, ny, size_x, size_y] = fill_in_blanc(nx, ny, size_x, size_y);
   [lone,late, lonr,latr, pm,pn, ang,orterr] = compute_grid(nx,ny, ...
                                     size_x,size_y, cent_lat,taper, ...
                                     tra_lon,tra_lat,rot, flip_xy, 0);
   tCompute = toc(tStart);
   disp(['Elapsed time to compute grid ', num2str(tCompute), ' sec'])
   tStart = tic;

%% Instead of drawing outline of grid passing through normal velocity points,
%% draw two outlines -- one going through the outermost RHO-points (these are
%% ghost points) and the other one through one row of RHO-points just inside,
%% so the two lines are only one grid spacing apart from each other.
%% This approach allows to get visual feeling of grid spacing relatively
%% to coastline and precise gauge the distances in terms of grid points --
%% ideally the coastline should fall between the two lines -- in this case
%% the case where only one row of outermost points needs to be masked.


%  out_lon = rad2deg*[ lone(2:end-2, 2)'        lone(end-1, 2:end-2) ...
%                      lone(end-1:-1:3, end-1)' lone(2,  end-1:-1:3) ];

%  out_lat = rad2deg*[ late(2:end-2, 2)'        late(end-1, 2:end-2) ...
%                      late(end-1:-1:3, end-1)' late(2,  end-1:-1:3) ];

   out_lon = rad2deg*[ lonr(1:end-1,1)'     lonr(end,1:end-1) ...
                       lonr(end:-1:2,end)'  lonr(1, end:-1:2) ];

   out_lat = rad2deg*[ latr(1:end-1,1)'     latr(end,1:end-1) ...
                       latr(end:-1:2,end)'  latr(1, end:-1:2) ];


   inn_lon = rad2deg*[ lonr(2:end-2, 2)'        lonr(end-1, 2:end-2) ...
                       lonr(end-1:-1:3, end-1)' lonr(2,  end-1:-1:3) ];

   inn_lat = rad2deg*[ latr(2:end-2, 2)'        latr(end-1, 2:end-2) ...
                       latr(end-1:-1:3, end-1)' latr(2,  end-1:-1:3) ];

%  disp(['size of inn_lon = ', num2str(size(inn_lon))])
%  disp(['size of inn_lat = ', num2str(size(inn_lat))])


   lo0 = min(min(out_lon)); lo1 = max(max(out_lon));  %% Compute extrema for
   la0 = min(min(out_lat)); la1 = max(max(out_lat));  %% the newly-built grid
                                                      %% even if parent is
   par0=0.85*la0+0.15*la1;                            %% present: these values
   par1=0.15*la0+0.85*la1;                            %% specify Lambert
   clo=0.5*(lo0+lo1);                                 %% projection.

   if plot_parent==1
     [filename, pathname] = uigetfile('*.nc', 'Select a parent grid file');
     if isequal(filename,0)
       disp('User selected Cancel')
       plot_parent==0;   %% if the user does not select any file,
                         %% uncheck the box
     else
       disp(['User selected ', fullfile(pathname, filename)])
     end

     pgrd = fullfile(pathname,filename);
     lonprnt = ncread(pgrd,'lon_rho');
     latprnt = ncread(pgrd,'lat_rho');

     out_lonp = [ lonprnt(1:end-1,1)' lonprnt(end, 1:end-1) ...
              lonprnt(end:-1:2, end)' lonprnt(1,  end:-1:2) ];

     out_latp = [ latprnt(1:end-1,1)' latprnt(end, 1:end-1) ...
              latprnt(end:-1:2, end)' latprnt(1,  end:-1:2) ];

     lo0 = min(min(out_lonp)); lo1 = max(max(out_lonp));
     la0 = min(min(out_latp)); la1 = max(max(out_latp));

     dx=0.01*(lo1-lo0); dy=0.01*(la1-la0);     %% smaller off-sets for parent

   else
     dx=0.05*(lo1-lo0); dy=0.05*(la1-la0);     %% larger for child
   end

   la0=la0-dy; la1=la1+dy;                      %% adjust to allow some space
   lo0=lo0-dx; lo1=lo1+dx;                      %% around the grid outline;

   cff=cos(0.5*(la0+la1)/rad2deg);              %% further adjust the ranges
   dy=la1-la0-cff*(lo1-lo0);                    %% to make the map fully occupy
   if (dy > 0.)                                 %% its designated square area
     dx=0.5*dy/cff; lo0=lo0-dx; lo1=lo1+dx;     %% on the figure
   else
     dy=-0.5*dy;    la0=la0-dy; la1=la1+dy;
   end

% Below "radius" is angular size of the grid expressed in degrees needed to
% control the size of the map produced by azimuthal projections (Stereographic,
% Gnomonic, etc..).  Because the projection pole is always aligned with grid
% center, radius is computed as the distance to the most remote corner of the
% grid.  Also note that if plotting parent grid is requested, the logic here
% is to compute the maximum radius between the parent and the child rather
% than just for the parent.  This is because accidentally child grid may not
% be fully enclosed by the parent, yet this plotting procedure is designed
% to produce sufficiently large map to be able to fully show both.


   if plot_parent==1
     radius=haversine(tra_lon*deg2rad, tra_lat*deg2rad, ...
                              deg2rad*lonprnt(1,1),deg2rad*latprnt(1,1));
     radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                         deg2rad*lonprnt(end,1),deg2rad*latprnt(end,1) ));
     radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                     deg2rad*lonprnt(end,end),deg2rad*latprnt(end,end) ));
     radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                        deg2rad*lonprnt(1,end),deg2rad*latprnt(1,end) ));
   else
     radius=0;
   end

   radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                                                  lone(1,1),late(1,1) ));
   radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                                               lone(end,1),late(end,1) ));
   radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                                           lone(end,end),late(end,end) ));
   radius=max( radius, haversine( tra_lon*deg2rad, tra_lat*deg2rad, ...
                                              lone(1,end),late(1,end) ));
   radius=radius*rad2deg;

%% Draw grid

   cla

   if strcmp(projtype,'Mercator')
     m_proj('Mercator','lon',[lo0 lo1],'lat',[la0 la1]);

   elseif strcmp(projtype,'Lambert')
     m_proj('Lambert','lon',[lo0 lo1], 'lat',[la0 la1], ...
                    'clo',clo, 'parallels',[par0,par1]);

   elseif strcmp(projtype,'Stereographic')
     m_proj('Stereographic', 'lon',tra_lon, 'lat',tra_lat, ...
                  'rad',1.5*radius, 'rot',0, 'rec','on');

   elseif strcmp(projtype,'Satellite')
     m_proj('Satellite', 'lon',tra_lon, 'lat',tra_lat, ...
                  'rad',radius, 'rot',0, 'rec','circle');

   elseif strcmp(projtype,'Gnomonic')
     m_proj('Gnomonic','lone',tra_lon, 'late',tra_lat, ...
                        'rad',1.5*radius, 'rec','on');
   end

   hold on

   ptch_color = [.8 .8 .7];

   if fill_land==1
     if strcmp(cstdata,'coarse')
       m_gshhs_c('patch',ptch_color, 'edgecolor','k')
     elseif strcmp(cstdata,'low')
       m_gshhs_l('patch',ptch_color, 'edgecolor','k')
     elseif strcmp(cstdata,'intermediate')
       m_gshhs_i('patch',ptch_color, 'edgecolor','k')
     elseif strcmp(cstdata,'high')
       m_gshhs_h('patch',ptch_color, 'edgecolor','k')
     elseif strcmp(cstdata,'full')
       m_gshhs_f('patch',ptch_color, 'edgecolor','k')
     else
       m_coast('patch',ptch_color)  %% coarse coast line
     end
   else
     if strcmp(cstdata,'coarse')
       m_gshhs_c('line')
     elseif strcmp(cstdata,'low')
       m_gshhs_l('line')
     elseif strcmp(cstdata,'intermediate')
       m_gshhs_i('line')
     elseif strcmp(cstdata,'high')
       m_gshhs_h('line')
     elseif strcmp(cstdata,'full')
       m_gshhs_f('line')
     else
       m_coast('line')  %% coarse coast line
     end
   end

   m_grid
   m_plot(out_lon, out_lat, 'r')
   m_plot(inn_lon, inn_lat, 'r')
   if plot_parent==1
     m_plot(out_lonp, out_latp, 'm')
   end
   refresh

   save('grid_settings.mat', 'nx','ny', 'size_x','size_y', ...
        'cent_lat', 'taper', 'tra_lat','tra_lon', 'rot', 'flip_xy', ...
        'plot_parent', 'projtype', 'cstdata');

   tDrawing = toc(tStart);
   disp(['Elapsed time to complete drawing ', num2str(tDrawing), ' sec'])
   icount=icount+1;
   out_txt.set('String',[num2str(icount),'> Update complete: computing ',...
          num2str(tCompute), ' sec, drawing ', num2str(tDrawing),' sec'])

 end %% <-- function updatebutton_Callback


 function dist = haversine(lon1,lat1,lon2,lat2)

% Angular distance between two points on a sphere measured along the
% great circle connecting them.  This is known as Haversine formula,
% https://en.wikipedia.org/wiki/Haversine_formula

   dist = 2*asin( sqrt( sin(0.5*(lat2-lat1))^2 ...
                       +cos(lat2)*cos(lat1)*sin(0.5*(lon2-lon1))^2 ...
                    ) );
 end


                                                         %% Function to create
 function savebutton_Callback(source,eventdata)          %% grid file and write
                                                         %% everything into it
   projtype=proj_menu_Callback(projpopup,'String');
   cstdata = popup_menu_Callback(coastpopup,'String');
   fill_land=fill_land_Callback(fill_land_box,'Value');

   nx = nxbox_Callback(nx_box,'Value');
   ny = nybox_Callback(ny_box,'Value');
   size_x = sizexbox_Callback(sizex_box,'Value');
   size_y = sizeybox_Callback(sizey_box,'Value');
   cent_lat = clatbox_Callback(clat_box,'Value');
   taper = taperbox_Callback(taper_box, 'Value');

   tra_lat = latbox_Callback(lat_box,'Value');
   tra_lon = lonbox_Callback(lon_box,'Value');
   rot = rotbox_Callback(rot_box,'Value');
   flip_xy = flipxybox_Callback(flipxy_box,'Value');

   fill_hraw = etopo5_box_Callback(etopo5_box,'Value');
   plot_parent = pgridbox_Callback(pgrid_box,'Value');

   tStart = tic;
   [nx, ny, size_x, size_y] = fill_in_blanc(nx, ny, size_x, size_y);
   [lone,late, lonr,latr, pm,pn, ang,orterr] = compute_grid(nx,ny, ...
                                     size_x,size_y, cent_lat,taper, ...
                                     tra_lon,tra_lat,rot, flip_xy, 1);
   tCompute = toc(tStart);
   disp(['Elapsed time to compute grid ', num2str(tCompute), ' sec'])
   tStart = tic;



% Reading topography:  Note that original code from Jeroen used a non-standard
%-------- -----------  (non-CF-compliant) version of etopo5.nc file with
% coordinate variable names as "lon_topo" and "lat_topo" rather than "lon" and
% "lat" (same as the corresponding dimensions in accordance to CF standard).
% This has been changed so this program can use a standard file downloaded from
% the web. While ETOPO5 is considered obsolete right now, it appears that that
% there are several versions of it available with slightly different variable
% names, lon,lat,topo vs. lon,lat,z, all of them adhere to CF standard.
% Overall this is not a big deal for our purposes here because topography
% generated here will be overwritten any way.

   if (fill_hraw==1)
     etopo = 'etopo5.nc';
     disp(['Reading ', etopo, ' ...'])
     x = ncread(etopo,'lon');
     y = ncread(etopo,'lat');
     topo = double(ncread(etopo,'topo'));
     x(find(x<0)) = x(find(x<0)) +360;
     xm = x-360;
     x = [xm' x']';
     topo = [topo' topo'];
     hraw = interp2(x,y, topo, lonr*rad2deg, latr*rad2deg);
   else
     disp('Not filling in topography')
     hraw=zeros(size(latr));
   end

%% The following two lines are merely for testing inverse transform and
%% should be kept commented out permanently.  [After application of these
%% two lines [lonr,latr] and [lone,late] should turn back into longitude-
%% latitude grid which can be verified by examining netCDF file.

%% [lonr,latr]=inverse_move_and_turn(tra_lon,tra_lat,rot,cent_lat, lonr,latr);
%% [lone,late]=inverse_move_and_turn(tra_lon,tra_lat,rot,cent_lat, lone,late);


   write_grid(lone,late, lonr,latr, pn,pm, hraw,ang, size_x,size_y, ...
                      cent_lat,taper, rot,tra_lon,tra_lat, flip_xy);

   icount=icount+1;
   out_txt.set('String',[num2str(icount),'> Saved to grid file'])
 end %% <-- function savebutton_Callback



 function [nx1, ny1, size_x1, size_y1] = fill_in_blanc(nx, ny, size_x, size_y)

% There is provision to leave one of the grid dimensions, nx,ny, or one
% of the physical sizes size_x,size_y, blank, so the missing parameter is
% automatically filled in by the program to make grid spacing be exactly
% the same in both directions. This translates into enforcing the
% relationship
%                      xi_max-xi_min     eta_max-eta_min
%                     --------------- = -----------------
%                           nx                 ny
%
% where  xi=xi(lon) = longitude expressed in radians; and
%
%         eta=eta(lat) = 0.5*ln[(1.+sin(lat))/(1.-sin(lat))]
%
% is Mercator latitude projection function; in their turn, xi_max and xi_min
% are functions of lon_min and lon_max which are, simply put,
%
%                 lon_max= 0.5*size_x/(Eradius*cos(cent_lat))
%                 lon_min=-0.5*size_x/(Eradius*cos(cent_lat))
%
% symmetrically around Greenwich Meridian, and
%
%                 lat_max=cent_lat+0.5*size_y/Eradius
%                 lat_min=cent_lat-0.5*size_y/Eradius
%
% symmetrically around cent_lat.
%
% Three out of four cases (the exception is when the unknown is "size_y") are
% straightforward as they only involve explicit forward lat --> eta transform.
% Finding size_y (if unknown) needs resolving
%
%   xi_max-xi_min     1      [  1+sin(cent_lat+dS)     1-sin(cent_lat-dS)  ]
%  -------------- = ------ ln[ -------------------- * -------------------- ]
%        nx          2*ny    [  1-sin(cent_lat+dS)     1+sin(cent_lat-dS)  ]
%
%                        size_y
% with respect to dS = -----------  which it its turn boils down to solving
%                       2*Eradius
%
% a quadratic equation
%
%                           1+p^2
%      cos^2(cent_lat) + 2*-------*cos(cent_lat)*sin(dS) + sin^2(dS) = 0
%                           1-p^2
%
% where, in its turn p=exp{ny*size_y/[nx*Eradius*cos(cent_lat)]}


   if (isempty(nx) || isnan(nx))
     deta=0.5*size_y/Eradius ;
     eta_max=latitude_to_eta( deg2rad*cent_lat +deta ) ;
     eta_min=latitude_to_eta( deg2rad*cent_lat -deta ) ;
     nx1=ceil( double(ny)*size_x/( (eta_max-eta_min) ...
                    *Eradius*cos(deg2rad*cent_lat) ) ) ;
     ny1=ny ; size_x1=size_x ; size_y1=size_y ;
     disp(['filled in empty entry nx=',num2str(nx1)])
   elseif (isempty(ny) || isnan(ny))
     deta=0.5*size_y/Eradius ;
     eta_max=latitude_to_eta( deg2rad*cent_lat +deta ) ;
     eta_min=latitude_to_eta( deg2rad*cent_lat -deta ) ;
     ny1=ceil( Eradius*cos(deg2rad*cent_lat) ...
                *double(nx)*(eta_max-eta_min)/size_x ) ;
     nx1=nx ; size_x1=size_x ; size_y1=size_y ;
     disp(['filled in empty entry ny=',num2str(ny1)])
   elseif (isempty(size_x) || isnan(size_x))
     deta=0.5*size_y/Eradius ;
     eta_max=latitude_to_eta( deg2rad*cent_lat +deta ) ;
     eta_min=latitude_to_eta( deg2rad*cent_lat -deta ) ;
     size_x1=Eradius*cos(deg2rad*cent_lat) ...
              *double(nx)*(eta_max-eta_min)/double(ny) ;
     nx1=nx ; ny1=ny ; size_y1=size_y ;
     disp(['filled in empty entry size_x=',num2str(size_x1)])
   elseif (isempty(size_y) || isnan(size_y))
     cosCent=cos(deg2rad*cent_lat) ;
     cff=exp(double(ny)*size_x/(double(nx)*Eradius*cosCent)) -1.0 ;
     size_y1=2.0*Eradius*asin( cosCent*cff/(cff+2.0) ) ;

     nx1=nx ; ny1=ny ; size_x1=size_x ;
     disp(['filled in empty entry size_y=',num2str(size_y1)])
   else
     nx1=nx; ny1=ny; size_x1=size_x; size_y1=size_y;
   end
 end

 function eta = latitude_to_eta(theta)                     %% Function to
   if (-0.5*pi < theta && theta < 0.5*pi)                  %% convert latitude
     cff=sin(theta);                                       %% into y-coordinate
     eta=0.5*log( (1.+cff)/(1.-cff) );                     %% of Mercator 
   else                                                    %% projection 
     disp(['lat_to_eta :: theta=', num2str(theta)])
     error('### ERROR: Latitude range exception.')
   end
 end

%----- The remaining functions are merely to read GUI input controls ---------

                                                           %% Function to
 function projtype=proj_menu_Callback(source,eventdata)    %% select type of
   str = get(source,'String'); val = get(source,'Value');  %% map projection
   switch str{val};                                        %% from popup up
     case 'Mercator'                                       %% menu
       projtype='Mercator'; icount = icount+1;
       out_txt.set('String',[num2str(icount), ...
                     '> Mercator projection selected'])
     case 'Lambert'
       projtype='Lambert';  icount = icount+1;
       out_txt.set('String',[num2str(icount), ...
            '> Lambert conformal projection selected'])
     case 'Stereographic'
       projtype='Stereographic'; icount = icount+1;
       out_txt.set('String',[num2str(icount), ...
                '> Stereographic projection selected'])
     case 'Satellite'
       projtype='Satellite'; icount = icount+1;
       out_txt.set('String',[num2str(icount), ...
                    '> Satellite projection selected'])
     case 'Gnomonic'
       projtype='Gnomonic'; icount = icount+1;
       out_txt.set('String',[num2str(icount), ...
                     '> Gnomonic projection selected'])
   end
 end
                                                           %% Function to
 function cstdata=popup_menu_Callback(source,eventdata)    %% select resolution
   str = get(source,'String'); val = get(source,'Value');  %% of coastline data
   switch str{val};                                        %% from popup menu
     case 'GSHHS coarse'
       cstdata='coarse';          icount = icount+1;
       out_txt.set( 'String', [ num2str(icount), ...
              '> Coarse resolution coastline selected' ])
     case 'GSHHS low-resolution'
       cstdata='low';            icount = icount+1;
       out_txt.set( 'String', [ num2str(icount), ...
                 '> Low-resolution coastline selected' ])
     case 'GSHHS intermediate'
       cstdata='intermediate';   icount = icount+1;
       out_txt.set( 'String', [ num2str(icount), ...
        '> Intermediate-resolution coastline selected' ])
     case 'GSHHS high-resolution'
       cstdata='high';          icount = icount+1;
       out_txt.set( 'String', [num2str(icount), ...
                '> High-resolution coastline selected' ])
     case 'GSHHS full-resolution'
       cstdata='full';          icount = icount+1;
       out_txt.set( 'String', [num2str(icount), ...
                '> Full-resolution coastline selected' ])
   end
 end
                                                           %% Function for
 function fill_land=fill_land_Callback(source,eventdata)   %% checkbox to fill
   fill_land=get(source, 'Value');                         %% land areas with
   icount = icount+1;                                      %% gray color
   out_txt.set( 'String', [num2str(icount), ...
                 '> check box Fill Land toggled' ])
 end

 function nx=nxbox_Callback(source,eventdata)              %% Function to
   nx=str2num(get(source, 'String'));                      %%  read nx
 end

 function ny=nybox_Callback(source,eventdata)              %% Function to
   ny=str2num(get(source, 'String'));                      %% read ny
 end

 function size_x=sizexbox_Callback(source,eventdata)       %% Function to
   size_x=str2double(get(source, 'String'))*1e3;           %% read size_x
 end

 function size_y=sizeybox_Callback(source,eventdata)       %% Function to
   size_y=str2double(get(source, 'String'))*1e3;           %% read size_y
 end

 function cent_lat=clatbox_Callback(source,eventdata)      %% Function to
   cent_lat=str2double(get(source, 'String'));             %% read cent_lat
 end

 function taper=taperbox_Callback(source,eventdata)        %% Function to
   taper=str2double(get(source, 'String'));                %% read tapering
 end

 function tra_lat=latbox_Callback(source,eventdata)        %% Function to
   tra_lat=str2double(get(source, 'String'));              %% read tra_lat
 end

 function tra_lon=lonbox_Callback(source,eventdata)        %% Function to
   tra_lon=str2double(get(source, 'String'));              %% read tra_lon
 end

 function rot=rotbox_Callback(source,eventdata)            %% Function to
   rot=str2double(get(source, 'String'));                  %% read azimuthal
 end                                                       %% rotation angle

 function flip_xy=flipxybox_Callback(source,eventdata)     %% Function to
   flip_xy=str2double(get(source, 'String'));              %% read flip_xy
 end

 function fill_hraw=etopo5_box_Callback(source,eventdata)  %% Function for
   fill_hraw=get(source, 'Value');                         %% checkbox to read
   icount = icount+1;                                      %% etopo5 dataset and
   out_txt.set( 'String', [num2str(icount), ...            %% compute hraw.
          '> check box Fill in Topography toggled'])
 end

 function plot_parent=pgridbox_Callback(source,eventdata)  %% Function for
   plot_parent=get(source, 'Value');                       %% checkbox to plot
   icount = icount+1;                                      %% parent grid
   out_txt.set( 'String', [num2str(icount), ...
          '> check box Plot Parent Grid toggled'])
 end

 function exitbutton_Callback(source,eventdata)            %% Function to exit
   clc ; clear all ; closereq                              %% the program
   disp('Exiting GRID_GUI')
 end
end %% <-- function grid_gui (the outermost function)
