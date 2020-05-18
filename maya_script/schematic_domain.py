# make vertical velocity (w) comparisons
# along pipe
# mean and RMS (root mean square)
import numpy as np
#import seawater as sw
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import glob

#####################
# 1m 30x500 vs 60x500
#####################

res = 3

pipe1_cw0 = 256
pipe1_cw1 = 265
pipe1_cw = np.arange(pipe1_cw0,pipe1_cw1)

pipe0_cw0 = 508
pipe0_cw1 = 517
pipe0_cw = np.arange(pipe0_cw0,pipe0_cw1)

pipe_l0 = 106
pipe_l1 = 405
pipe_l = np.arange(pipe_l0,pipe_l1)

# pick file (0024)
#output0 = list(sorted(glob.glob(output_path0+'*')))[0]

# get mask
#mask_nc = Dataset(output0,'r').variables['mask_rho'][:,:]
mask_nc = np.zeros([514,1026])

f0_mask = np.copy(mask_nc)
for e_i in range(len(pipe_l)):
    f0_mask[pipe_l[e_i],pipe0_cw] = 1

f1_mask = np.copy(mask_nc)
for e_i in range(len(pipe_l)):
    f1_mask[pipe_l[e_i],pipe1_cw] = 1


######################
# plotting
#################

#cma = 'bwr'
cma = 'gray_r'
plt.ion()
axisfont = 16
axistick = 14

savename = 'schematic.pdf'
xtext0 = 50
ytext = 450

# plot
fig,(ax0,ax1) = plt.subplots(2,1,figsize=[12,8])
im0 = ax0.imshow(f0_mask,cmap=cma,aspect='auto')
im1 = ax1.imshow(f1_mask,cmap=cma,aspect='auto')
ax0.invert_yaxis()
ax1.invert_yaxis()
ax0.text(xtext0,ytext,'a) F = 0',fontsize=axisfont)
ax1.text(xtext0,ytext,'b) 0.1 $\leq$ F $\leq$ 100',fontsize=axisfont)
ax1.annotate('',xy=(365+100,344),xytext=(365,344),arrowprops=dict(arrowstyle="->"))
ax1.annotate('',xy=(365+100,200),xytext=(365,200),arrowprops=dict(arrowstyle="->"))
ax1.annotate('',xy=(65+100,344),xytext=(65,344),arrowprops=dict(arrowstyle="->"))
ax1.annotate('',xy=(65+100,200),xytext=(65,200),arrowprops=dict(arrowstyle="->"))
ax0.set_ylabel('y',fontsize=axisfont)
ax1.set_ylabel('y',fontsize=axisfont)
ax1.set_xlabel('x',fontsize=axisfont)
ax0.tick_params(axis='both',which='major',labelsize=axistick)
ax1.tick_params(axis='both',which='major',labelsize=axistick)
plt.savefig(savename,bbox_inches='tight')
