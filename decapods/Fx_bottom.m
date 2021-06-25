function [dz, zKB, DepthWeight_KBDD, idxKBDD, TotalDepth] = Fx_bottom( ...
    DDkb, h, zeta, theta_s, theta_b, hc, NZ, wstr, sc_type)
% function [DepthWeight_KBDD, NumLayersTo_KBDD, CumHeight, TotalDepth] = Fx_DepthWeightGivenDZ_KBDD_v01( ...
    % DD, dz)
	
% Matlab function to obtain the 3-dimensional depth-weighting factors (layers, y, x) 
% that will be used in another function to multiply by the
% 3-dimensional concentration (layers, y, x) or (layers, x, y)
% from the bottom to any height DDkb above the bottom
% (for example, to obtain 2-D near-bottom depth-weighted average temp, o2, dic, alk, etc)
%
% This script includes zlevs4
%
% Written by:
%
% Greg Pelletier 
% gregp@sccwrp.org
% 
% INPUTS
%
% - DDkb = height above the bottom to which the depth-weighting will be done 
%   (for example, use DD=5 to obtain the DepthWeight_KBDD factors 
%   that will be used in another function 
%   to obtain the average from 5m above the bottom to the bottom, etc.) 
%
% - zlevs4 inputs: h, zeta, theta_s, theta_b, hc, NZ, 'w', sc_type
%
% OUTPUTS 
%
% - dz = 3-dimensional array (layer, y, x) or (layer, x, y) of the thickness (m) of each layer
%
% - z = 3-dimensional array (layer, y, x) (layer, x, y) of the midpoint depth (m) of each layer
%
% - DepthWeight_KBDD = 3-dimensional array  (layers, y, x) or (layers, x, y) 
%   of proportional depth-weighting factors (unitless)
%   that sum to 1 across all depths. These factors will be used in another function
%   to multiply by the 3-dimensional concentrations of any variable (e.g. temp, o2, etc)
%   and then sum that product across all depths to obtain a 2-dimensional array (y,x)
%   of depth-weighted average concentrations between the bottom and height DD above the bottom
%
% - idxKBDD = 2-dimensional array (y,x) or (x,y) 
%   of the layer index (unitless) that corresponds to the layer that contains height DD from the bottom
%
% - CumDepth = 3-dimensional array (layer, y, x)  or (layers, x, y) of the cumulative depth (m) to the bottom of each layer
%
% - CumHeight = 3-dimensional array (layer, y, x)  or (layers, x, y) of the cumulative height (m) above the bottom of each layer
%
% - TotalDepth = 2-dimensional array (y,x) or (x,y) of the total depth (m) of each grid cell

% Faycal's code from extract_2D_omega_ara.m, except:
% changed NY to numel(z_w(1,:,1))
% changed NX to numel(z_w(1,1,:))
[z_w,Cw1] = zlevs4(h, zeta, theta_s, theta_b, hc, NZ, wstr, sc_type);
dz = diff(z_w);

        % zbot = flipdim(cumsum(flipdim(dz,1)),1);
        % ztop = [zbot(2:end,:,:);zeros(1,numel(z_w(1,:,1)),numel(z_w(1,1,:)))];
	% z = (zbot+ztop)./2 ;
	
% find zKB = midpoint heights from bottom
    zbotKB = cumsum(dz,1);
    ztopKB=zeros(size(zbotKB));
    endKB=numel(zbotKB(:,1,1))-1;
    ztopKB(2:end,:,:)=zbotKB(1:endKB,:,:);
	zKB = (zbotKB+ztopKB)./2 ;
	CumHeight=zbotKB;	% cumulative height from bottom to top of each layer

% new efficient code by gp
%
% vars for KB
ztop2KB=ztopKB;
dz2KB=dz;
ztop2KB(ztopKB>DDkb)=0;  % set all layers below DD to 0
dz2KB(ztopKB>DDkb)=0;   % set all layers below DD to 0
idxKBDD=zeros(size(dz,2),size(dz,3));
DepthWeight_KBDD=zeros(size(dz,1),size(dz,2),size(dz,3));
%
for j = 1:size(dz,2)
	for k = 1:size(dz,3)
		% for KB
		if zbotKB(1,j,k)>DDkb
			idxKBDD(j,k)= 1;
		else
			idxKBDD(j,k)=find(ztop2KB(:,j,k)==max(ztop2KB(:,j,k)));   % layer index for the deepest layer that contains DD
		end
		if ztopKB(idxKBDD(j,k),j,k)<=DDkb && zbotKB(idxKBDD(j,k),j,k)>=DDkb
			dz2KB(idxKBDD(j,k),j,k)=DDkb-ztop2KB(idxKBDD(j,k),j,k);   % adjusted dz in the deepest layer that contains DD
		end
		DepthWeight_KBDD(:,j,k)=dz2KB(:,j,k)./nansum(dz2KB(:,j,k),1);   % depth weighting factors
	end
end
TotalDepth = h + zeta; 
	
end  %function
