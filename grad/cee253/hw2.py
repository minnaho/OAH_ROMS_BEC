############################
# forward difference method
###########################
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# parameters
C_i0 = 0
C_inlet = 1
D_f = 2.
V_f = 0
K_f = 0

grid_points_f = 20
dx_f = 1./grid_points_f
t_steps_f = 20
dt_f = .0001

# calculate if it's stable; stability <= .5 for stable
stability = (D_f*dt_f)/(dx_f**2)

stability_half = .5
dt_f_half = (stability_half*(dx_f**2))/D_f
dt_f = dt_f_half


# create output array to fill
output_f = np.empty((t_steps_f,grid_points_f))
output_f.fill(np.nan)

# fill boundary conditions
output_f[:,0] = C_inlet
output_f[0,:] = C_i0

# make foward difference function
def forward_diff(D,V,K,dx,dt,t,t_steps,x,grid_points,output):
    # account for exit boundary
    if x==grid_points-1:
        output[t,x] = output[t-1,x] + (D*(dt/(dx)**2))*(2*output[t-1,x-1]-2*output[t-1,x]) - (dt*K*output[t-1,x])
    else:
        output[t,x] = output[t-1,x] + (D*(dt/(dx)**2))*(output[t-1,x+1]-2*output[t-1,x]+output[t-1,x-1]) - (V*(dt/(2*dx))*(output[t-1,x+1]-output[t-1,x-1])) - (dt*K*output[t-1,x])
    return 

# run function looping over t and x
for t_i in range(1,t_steps_f):
    for x_i in range(1,grid_points_f):
        forward_diff(D_f,V_f,K_f,dx_f,dt_f,t_i,t_steps_f,x_i,grid_points_f,output_f)

print(output_f)

# plot
plt.figure(figsize=[16,7])
for p_i in range(t_steps_f):
    plt.plot(range(grid_points_f),output_f[p_i])
        
