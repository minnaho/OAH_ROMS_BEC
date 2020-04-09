create_psource(frcname,psvars,psname,psunit,Nsrc,N,psrc_title,psrc_time,psrc_cycle);

 create_psource('L2_psrc.nc',['temp' 'salt' 'NO3' 'NH4' 'PO4'],['psource tempeperature' 'psource salinity' 'input nitrate discharge' 'input ammonium discharge' 'input phosphate discharge'],...
['C' 'psu' 'mmmol m-2 s-1','mmmol m-2 s-1','mmmol m-2 s-1'],60,'POTW',2500,86400);



