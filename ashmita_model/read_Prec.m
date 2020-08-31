
for i=1990:2013
	M{i-1989} = csvread(['/data/project3/kesf/ashmita_model/Precip/AllPrecip_',num2str(i),'.csv']);
end



MM = nan(24,366,366);
for i=1990:2013
	toto = csvread(['/data/project3/kesf/ashmita_model/Precip/AllPrecip_',num2str(i),'.csv']);
[X Y] = size(toto);
       MM(i-1989,1:X-1,1:Y-1) = squeeze(toto(2:end,2:end));
end







