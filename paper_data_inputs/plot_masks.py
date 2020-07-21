import h5py
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
plt.ion()
region_mask = h5py.File('/data/project1/minnaho/mask.mat','r')['mask']

colors = ['spring','viridis_r','gray','rainbow','gnuplot_r','seismic','Greens_r']

plt.imshow(np.transpose(region_mask['maskla']),origin='lower',cmap=colors[0])
plt.imshow(np.transpose(region_mask['masksdn']),origin='lower',cmap=colors[1])
plt.imshow(np.transpose(region_mask['masksds']),origin='lower',cmap=colors[2])
plt.imshow(np.transpose(region_mask['maskocn']),origin='lower',cmap=colors[1])
plt.imshow(np.transpose(region_mask['maskocs']),origin='lower',cmap=colors[2])
plt.imshow(np.transpose(region_mask['masksp']),origin='lower',cmap=colors[3])
plt.imshow(np.transpose(region_mask['masksm']),origin='lower',cmap=colors[4])
plt.imshow(np.transpose(region_mask['maskv']),origin='lower',cmap=colors[5])
plt.imshow(np.transpose(region_mask['masksb']),origin='lower',cmap=colors[6])

# south sd, north sd, oc, sp, sm, v, sb
j_locs = np.array((164,264,500,610,740,948))
