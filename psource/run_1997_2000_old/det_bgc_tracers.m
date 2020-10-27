function [varnames_bgc,longnames_bgc,units_bgc,varnames_bgc_or] = det_bgc_tracers(par_file); 

par_file
% np = netcdf(par_file);

infovar = ncinfo(par_file) ;

disp('analyzing existing variables')
% var_in = var(np);
var_in = {infovar.Variables.Name} ;
%
count_bgc = 1;
for v = 1:length(var_in)
    thisVar = var_in{1,v};
    vname = thisVar ;
    if (count_bgc)
        % need to check if this is a 4D variable (no need to
        % set up boundary conditions for sediment etc.)
        % also exclude non-bgc variables (w and PAR at this
        % point)
%        itsDim = dim(thisVar);
        if (~strcmp(vname,'ocean_time') && ~strcmp(vname,'s_rho') && ...
            ~strcmp(vname,'eta_rho') && ~strcmp(vname,'xi_rho') && ...
            ~strcmp(vname, 'w') && ~strcmp(vname,'PAR') && ...
		~strcmp(vname, 'u') && ~strcmp(vname, 'v') && ~strcmp(vname, 'ubar') && ...
		~strcmp(vname, 'vbar') && ~strcmp(vname, 'zeta') && ~strcmp(vname, 'temp') && ~strcmp(vname, 'salt') )
            varnames_bgc{count_bgc} = vname;

%            longnames_bgc{count_bgc} = np{vname}.long_name(:);
		longnames_bgc{count_bgc} = infovar.Variables(v).Attributes(1).Value ; 
%            units_bgc{count_bgc} = np{vname}.units(:);
		units_bgc{count_bgc} = infovar.Variables(v).Attributes(2).Value ;

            count_bgc = count_bgc + 1;
        end
    elseif (strcmp(vname, 'salt'))
        % include all 4D variables after this one
        count_bgc = 1;
    end
end

count_bgc = count_bgc - 1; % subtract the last increase
varnames_bgc_or = varnames_bgc ;
% np = close(np);
return
