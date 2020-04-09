addpath(genpath('/data/project3/kesf/tools_matlab/psource'))

frcname         =  'L2_psrc.nc';
psvars          = 'temp' ; 'salt' ; 'NO3' ; 'NH4' ; 'PO4' ;
Nsrc            = 4 ;
N               = 60 ;
psrc_title      = 'POTW' ;
psrc_time       = 365 ;
psrc_cycle      = 1 ;
Npas=length(psvars);


ncid = netcdf.create('L2_psrc_POTW.nc','netcdf4');
  dimNsrc    = netcdf.defDim    (       ncid,   'Nsrc', Nsrc    );
  dimNpas    = netcdf.defDim    (       ncid,   'Npas',         Nsrc      ) ;
  dims_rho    = netcdf.defDim   (       ncid,   's_rho',        N         ) ;
  dimpsr_time = netcdf.defDim   (       ncid,   'psr_time',     psrc_time ) ;

%% Time
    psrc_time    =  netcdf.defVar(ncid,'psrc_time', 'double', [dimpsr_time]);
    netcdf.putAtt(ncid,psrc_time,'units','days');
    netcdf.putAtt(ncid,psrc_time,'long_name','point source time');
    if psrc_cycle>0;
        netcdf.putAtt(ncid,psrc_time,'cycle_length',psrc_cycle);
    end

%% Characters
%  dimLsrc    = netcdf.defDim    (       ncid,   'Lsrc',  Nsrc   );
  Lsrc    =  netcdf.defVar(ncid,'Lsrc', 'int', [dimNsrc dimNpas]);
      netcdf.putAtt(ncid,Lsrc,'long_name','logical switch for any tracers at every point source locations');
%      netcdf.putAtt(ncid,Nsrc,'option_1','true');
%      netcdf.putAtt(ncid,Nsrc,'option_0','false');

%  dimIsrc    = netcdf.defDim    (       ncid,   'Isrc',  Nsrc   );
  Isrc    =  netcdf.defVar(ncid,'Isrc', 'int', [dimNsrc]);
      netcdf.putAtt(ncid,Isrc,'long_name','global xi-directional grid number of the point sources');

%  dimJsrc    = netcdf.defDim    (       ncid,   'Jsrc',  Nsrc   );
  Jsrc    =  netcdf.defVar(ncid,'Jsrc', 'int', [dimNsrc]);
      netcdf.putAtt(ncid,Jsrc,'long_name','global eta-directional grid number of the point sources');

%  dimJsrc    = netcdf.defDim    (       ncid,   'Dsrc',  Nsrc   );
  Jsrc    =  netcdf.defVar(ncid,'Dsrc', 'int', [dimNsrc]);
      netcdf.putAtt(ncid,Dsrc,'long_name','flag to determine direction of the mass point source');
%nw{'Dsrc'}.option_0 = 'xi-direction';
%nw{'Dsrc'}.option_1 = 'eta-direction';
%nw{'Dsrc'}.option_2 = 's-direction';

%  dimQshape    = netcdf.defDim    (       ncid,   'Qshape',  Nsrc  );
  Qshape    =  netcdf.defVar(ncid,'Qshape', 'float', [dims_rho dimNsrc]);
      netcdf.putAtt(ncid,Qshape,'long_name','non-dimensional vertical spahe function for Qbar');
      netcdf.putAtt(ncid,Qshape,'units','no unit');

%  dimQbar    = netcdf.defDim    (       ncid,   'Qbar',  Nsrc  );
  Qbar    =  netcdf.defVar(ncid,'Qbar', 'float', [dimpsrc_time dimNsrc]);
      netcdf.putAtt(ncid,Qshape,'long_name','vertically integrated mass transport of point');
      netcdf.putAtt(ncid,Qshape,'units','meter3 second-1');

for ii=1:Npas;
	char(psvars(ii))    =  netcdf.defVar(ncid,char(psvars(ii)), 'float', [dimpsrc_time dimNsrc]);
	netcdf.putAtt(ncid,psvars,'long_name',char(psname(ii)));
        netcdf.putAtt(ncid,psvars,'units',char(psunit(ii)));
end

%for ii=1:Npas;
%  nw{char(psvars(ii))} = ncfloat('psrc_time', 'Nsrc');
%  nw{char(psvars(ii))}.long_name = char(psname(ii));
%  nw{char(psvars(ii))}.units = char(psunit(ii));
%end;


result = endef(nw);

% Create global attributes
%nw.title = ncchar(psrc_title);
%nw.title = psrc_title;
%nw.date = ncchar(date);
%nw.date = date;
%nw.type = ncchar('ROMS point fource file');
%nw.type = 'ROMS point source file';

