function  create_psource(frcname,psvars,psname,psunit,Nsrc,N,psrc_title,psrc_time,psrc_cycle);
%===================================================================
%
% Create an empty netcdf point source file
%
%    Inputs
%     frcname:    name of the psource file
%     psvars:     variable names of passive tracers (include T and S)
%     psname:     netcdf longnames of passive tracers
%     psunit:     unit of passive tracers
%     Nsrc:       number of point source locations
%     N:          number of vertical s-layers
%     psrc_title: title in the netcdf file  
%     psrc_time:  1D time array
%     psrc_cycle: cycle length
%
% Built on the Pierrick Penven's ROMS tools
%                         Yusuke Uchiyama, Kobe Univ., 6-17-2011
%                      modified to include sediments, 10-15-2013
%
%===================================================================

warning('off','MATLAB:dispatcher:InexactCaseMatch'); % for R2011a and later
Npas=length(psvars);
if Npas<2; disp('ERROR in create_psource.m: number of tracer < 2'); return; end;

nw = netcdf(frcname, 'clobber');
result = redef(nw);

% dimensions
nw('Nsrc') = Nsrc;
nw('Npas') = Npas;
nw('s_rho') = N;
nw('psrc_time') = length(psrc_time);

% create variables and attributes
nw{'psrc_time'} = ncdouble('psrc_time');
nw{'psrc_time'}.long_name = 'point source time';
nw{'psrc_time'}.units = 'days';
if psrc_cycle>0;
  nw{'psrc_time'}.cycle_length = psrc_cycle;
end;

nw{'Lsrc'} = ncint('Npas', 'Nsrc');
nw{'Lsrc'}.long_name = 'logical switch for any tracers at every point source locations';
nw{'Lsrc'}.option_1 = 'true';
nw{'Lsrc'}.option_0 = 'false';

nw{'Isrc'} = ncint('Nsrc');
nw{'Isrc'}.long_name = 'global xi-directional grid number of the point sources';

nw{'Jsrc'} = ncint('Nsrc');
nw{'Jsrc'}.long_name = 'global eta-directional grid number of the point sources';

nw{'Dsrc'} = ncint('Nsrc');
nw{'Dsrc'}.long_name = 'flag to determine direction of the mass point source';
nw{'Dsrc'}.option_0 = 'xi-direction';
nw{'Dsrc'}.option_1 = 'eta-direction';
nw{'Dsrc'}.option_2 = 's-direction';

nw{'Qshape'} = ncfloat('s_rho', 'Nsrc');
nw{'Qshape'}.long_name = 'non-dimensional vertical spahe function for Qbar';
nw{'Qshape'}.units = 'no unit';

nw{'Qbar'} = ncfloat('psrc_time', 'Nsrc');
nw{'Qbar'}.long_name = 'vertically integrated mass transport of point';
nw{'Qbar'}.units = 'meter3 second-1';

for ii=1:Npas;
  nw{char(psvars(ii))} = ncfloat('psrc_time', 'Nsrc');
  nw{char(psvars(ii))}.long_name = char(psname(ii));
  nw{char(psvars(ii))}.units = char(psunit(ii));
end;

result = endef(nw);

% Create global attributes
nw.title = ncchar(psrc_title);
nw.title = psrc_title;
nw.date = ncchar(date);
nw.date = date;
nw.type = ncchar('ROMS point fource file');
nw.type = 'ROMS point source file';

% Write time variables
nw{'psrc_time'}(:) = psrc_time;

close(nw);
