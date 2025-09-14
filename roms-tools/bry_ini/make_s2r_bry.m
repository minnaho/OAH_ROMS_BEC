clear all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Make a ROMS boundary forcing file.
%  Designed for MERCATOR-GLORYS products
%
%%%%%%%%%%%%%%%%%%%%% USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%%%
%
%  bry climatology file names:
bry_root = '/data/project7/pdamien/DATA/GLORYS12V1/';
bry_name = 'glorys12v1' ;  
%bry_root = '/data/project7/pdamien/DATA/GLORYS12V1_FORECAST/20*/';
%bry_name = 'mercatorglorys12v1_gl12_mean' ;

% Set a date range for the forcing file
start_date = datenum(2013,01,01);
end_date   = datenum(2021,01,31);

grdname  = '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed_grd.nc';
root_name= '/data/project7/pdamien/ROMS_outputs/ATLMED12KM/FORCINGS/atlmed';
rm_bryfile = 0 ; % remove and redo bry file

pars.theta_s = 6.0;
pars.theta_b = 6.0;
pars.hc     = 250.0;
pars.N      = 100;
pars.scoord = 'new2012';    % child 'new' or 'old' type scoord

obcflag        = [1 1 1 0];    % open boundaries flag (1=open , [S E N W])
time_ref = datenum(1995,1,1) ; % reference time for ROMS
coefs_dir = 'Coefs_atlmed' ; % to store precomputed coefs 
%
%%%%%%%%%%%%%%%%%%% END USER-DEFINED VARIABLES %%%%%%%%%%%%%%%%%%%%%%%

% make one bry file per year
  start_year = str2num(datestr(start_date,'YYYY')) ;   
  end_year = str2num(datestr(end_date,'YYYY')) ;

if ~exist(coefs_dir)
   mkdir(coefs_dir)
end

for yy=start_year:end_year

   disp(['Working on year ' num2str(yy)])

   frclist = dir([bry_root bry_name '*' num2str(yy) '*.nc']);
   nfiles = length(frclist);

   % time
   stime = zeros(nfiles,1);
   for i=1:nfiles
     datname = [frclist(i).folder '/' frclist(i).name];
     ncid = netcdf.open(datname,'nowrite');
     try
        ID = netcdf.inqVarID(ncid,'time');
     catch exception
        if strcmp(exception.identifier,'MATLAB:imagesci:netcdf:libraryFailure')
           index=strfind(datname,'Y') ;
           stime(i) = datenum(str2num(datname(index(end)+1:index(end)+4)), ...
                              str2num(datname(index(end)+6:index(end)+7)),...
                              str2num(datname(index(end)+9:index(end)+10))) + 0.5 ;
        end
      end
      netcdf.close(ncid)
      if stime(i)==0
         stime(i) = double(ncread(datname,'time',[1],[1]))/24 + datenum(1950,1,1);
      end
   end

   % Create bry file
   bry_file = [root_name '_bry_' num2str(yy) '.nc']
   if (exist(bry_file) && rm_bryfile==1)
      delete(bry_file)
   end
   if exist(bry_file)==0 
      disp('Creating boundary file: ');
      disp(bry_file)
      create_bry(bry_file,grdname,obcflag,pars);
      disp('Done')
   end

   time2wr = double(stime) - time_ref ;
   ncwrite(bry_file,'bry_time',time2wr);

   for irec =  1:nfiles

    disp(['%%%% ----> Working on days ' num2str(irec) '/' num2str(nfiles) ' <---- %%%%'])
    datname = [frclist(irec).folder '/' frclist(irec).name];
    s2r_hv_glorys(datname,grdname,bry_file,irec,pars,obcflag,coefs_dir);
 
   end

end
