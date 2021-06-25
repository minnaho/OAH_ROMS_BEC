function [var_KBDD] = Fx_var_KBDD_v02(var, DepthWeight_KBDD)

% Matlab function to obtain use the 3-dimensional depth-weighting factors (layers, y, x) or (layers, x, y) 
% that were calculated with Fx_DepthWeight_KBDD 
% This function multiplies those depth weigting factors "DepthWeight_KBDD" by the
% 3-dimensional concentration "var" (layers, y, x)  or (layers, x, y)
% and then sums that product across all depths to obtain a 2-dimensional array (y,x) or (x,y)
% of the depth-weighted avg concentrations var_KBDD (y,x) or (x,y) from the bottom to height DD above the bottom
% (for example, to obtain 2-D bottom 5m depth-weighted average temp, o2, dic, alk, etc)
%
% Written by:
%
% Greg Pelletier 
% gregp@sccwrp.org
%

% INPUT
% - var = 3-dimensional array (layers, y, x)  or (layers, x, y) of variable concentrations
% - DepthWeight_KBDD = 3-dimensional array  (layers, y, x)  or (layers, x, y)
%   of proportional depth-weighting factors (unitless)
%   that sum to 1 across all depths. These factors are used in this function
%   to multiply by the 3-dimensional concentrations of any variable (e.g. temp, o2, etc)
%   and then sum that product across all depths to obtain a 2-dimensional array (y,x) or (x,y)
%   of depth-weighted average concentrations between the bottom and height DD above the bottom
%
% OUTPUT
% - var_KBDD = 2-dimensional array (y,x) or (x,y)
%   of the depth-weighted avg concentrations var_KTDD (y,x) or (x,y) from the surface to depth DD
%   (for example, 2-D bottom 5m depth-weighted average temp, o2, dic, alk, etc)
 
var_KBDD = squeeze(nansum(var.*DepthWeight_KBDD,1));   % thickness-weighted average from bottom to DD above bottom

end    % function