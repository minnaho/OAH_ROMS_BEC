 create_psource('L2_psrc.nc',['temp' 'salt' 'NO3' 'NH4' 'PO4'],['psource tempeperature' 'psource salinity' 'input nitrate discharge' 'input ammonium discharge' 'input phosphate discharge'],...
['C' 'psu' 'mmmol m-2 s-1','mmmol m-2 s-1','mmmol m-2 s-1'],60,'POTW',2500,86400);

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
%	modified for new matlab version and add biogeochemical tracers
% 	Faycal Kessouri, SCCWRP/UCLA, Los Angeles, 04/24/2018
%
%===================================================================
% example:
frcname		=  'L2_psrc.nc';
 psvars          = 'temp' ; 'salt' ; 'NO3' ; 'NH4' ; 'PO4' ;
Nsrc		= 4 ;
N		= 60 ;
psrc_title	= 'POTW' ;
psrc_time	= 365 ;
psrc_cycle	= 1 ;
Npas=length(psvars);

ncid = netcdf.create('L2_psrc_POTW.nc','netcdf4');

  dimNsrc    = netcdf.defDim 	(	ncid,	'Nsrc',	Nsrc	);
  dimNpas    = netcdf.defDim	(	ncid,	'Npas',		Nsrc	  ) ;
  dims_rho    = netcdf.defDim	(	ncid,	's_rho',	N	  ) ;
  dimpsr_time = netcdf.defDim	(	ncid,	'psr_time',	psrc_time ) ;

%%%%%% Time
    psrc_time    =  netcdf.defVar(ncid,'psrc_time', 'double', [dimpsr_time]);
    netcdf.putAtt(ncid,psrc_time,'units','days');
    netcdf.putAtt(ncid,psrc_time,'long_name','point source time');
    if psrc_cycle>0;
        netcdf.putAtt(ncid,psrc_time,'cycle_length',psrc_cycle);
    end
%%%%%%% Characters


%%%%%%% Floats


nccreate(frcname,psrc_time,'Dimensions',{'psr_time',dimpsr_time},'Datatype','double') ;

nccreate(frcname,psvars(1),'Dimensions',{'Nsrc',dimNsrc,'eta_rho',size_eta_rho,dimname,dimlen},'Datatype','single','Format','64BIT') ;


    Lsrc    =  netcdf.defVar(ncid,'Nsrc', 'int32', [Nsrc]);
    netcdf.putAtt(ncid,psrc_time,'long_name','logical switch for any tracers at every point source locations');
    netcdf.putAtt(ncid,Lsrc,'option_1','true';
    netcdf.putAtt(ncid,Lsrc,'option_0','false';



netcdf.putAtt(ncid,iron,'long_name','iron deposition');
iron_units = 'nmol/cm2/s' ;
netcdf.putAtt(ncid,dust,'units',iron_units);
netcdf.putAtt(ncid,iron,'units',iron_units);

netcdf.putVar(ncid,dust,dust_roms);
netcdf.putVar(ncid,iron,iron_roms);

      disp('--- dust and iron')

              % define the dust-related variables (time and dust itself)
%     nc_frc('dust_time') = 12;
%     nc_frc{'dust_time'} = ncdouble('dust_time');
%     nc_frc{'dust_time'}.long_name = ncchar('');
%     nc_frc{'dust_time'}.units = ncchar('days');
%     nc_frc{'dust_time'}.cycle_length = woa_cycle; % 360.;
%     nc_frc{'dust_time'}(:) = woa_time; % [15:30:345];


dust_time_roms = 12 ;
woa_time = [15.21875 45.65625 76.09375 106.53125 136.96875 167.40625 ...
    197.84375 228.28125 258.71875 289.15625 319.59375 350.03125] ;

dust_time    =  netcdf.defVar(ncid,'dust_time', 'double', [dimidtdust]);
    netcdf.putAtt(ncid,dust_time,'units','days');
    netcdf.putAtt(ncid,dust_time,'long_name','');
    netcdf.putAtt(ncid,dust_time,'cycle_length',365.25);
netcdf.putVar(ncid,dust_time,woa_time);

iron_time    =  netcdf.defVar(ncid,'iron_time', 'double', [dimidtiron]);
    netcdf.putAtt(ncid,iron_time,'units','days');
    netcdf.putAtt(ncid,iron_time,'long_name','');
    netcdf.putAtt(ncid,iron_time,'cycle_length',365.25);
    netcdf.putVar(ncid,iron_time,woa_time);

  % insert global attribute
  NC_GLOBAL = netcdf.getConstant('NC_GLOBAL');
netcdf.putAtt(ncid,NC_GLOBAL,'title','iron and dust deposition in usw1')
netcdf.putAtt(ncid,NC_GLOBAL,'long_title','interpolation from Dust_1yr.nc')
netcdf.putAtt(ncid,NC_GLOBAL,'institution','UCLA/UW/SCCWRP')
netcdf.putAtt(ncid,NC_GLOBAL,'source','roms')
 %%%%%%%%%%%%%%
