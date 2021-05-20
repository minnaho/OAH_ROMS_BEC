##############################
# generalized Crank-Nicolson
##############################
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# f_v is parameter for generalized Crank-Nicolson
# .5 = Crank-Nicolson
# 1.0 = backwards diff
# 0 = forward diff
f_v = 0.5
f_prime_v = 1-f_v

# parameters
C_i0 = 0
C_inlet = 1
D_v = 2.
V_v = 0
K_v = 0

grid_points_v = 40
dx_v = 1./grid_points_v
t_steps_v = 1000

# calculate if it's stable; stability <= .5 for forward diff stable
#stability = (D_v*dt_v)/(dx_v**2)
# Crank-Nicolson
stability = 3
# forward diff
#stability = .5
# backward diff

dt_v = (stability*(dx_v**2))/D_v
#dt_v = 2E-6

# create output array to fill
output_v = np.empty((t_steps_v,grid_points_v))
output_v.fill(np.nan)

# boundary conditions
output_v[:,0] = C_inlet
output_v[0,:] = C_i0

#####################
# Thomas Algorithm
#####################
beta = np.empty((t_steps_v,grid_points_v))
beta.fill(np.nan)
gamma = np.empty((t_steps_v,grid_points_v))
gamma.fill(np.nan)
d_i = np.empty((t_steps_v,grid_points_v))
d_i.fill(np.nan)

# a, b, c terms
a_1 = ((-f_v*D_v)/(dx_v**2)) - ((f_v*V_v)/(2*dx_v))
b_1 = (1/dt_v)+((2*f_v*D_v)/(dx_v**2))+(f_v*K_v)
c_1 = ((-f_v*D_v)/(dx_v**2)) + ((f_v*V_v)/(2*dx_v))

# first d_1 has inlet boundary so add a_1 term
d_1 = ((((f_prime_v*D_v)/(dx_v**2)) + ((f_prime_v*V_v)/(2*dx_v)))*output_v[0,0]) + (((1/dt_v)-((2*f_prime_v*D_v)/(dx_v**2))-(f_prime_v*K_v))*output_v[0,1]) + ((((f_prime_v*D_v)/(dx_v**2)) - ((f_prime_v*V_v)/(2*dx_v)))*output_v[0,2]) + (((f_v*D_v)/(dx_v**2)) + ((f_v*V_v)/(2*dx_v)))*output_v[1,0]


beta[:,0] = b_1
gamma[:,0] = d_1/b_1
d_i[:,0] = d_1

for t_i in range(1,t_steps_v):
    # forward substitution
    for x_i_f in range(1,(grid_points_v)):
        if x_i_f == grid_points_v-1:
            c_1 = (-f_v*D_v)/(dx_v**2)
            a_1 = (-f_v*D_v)/(dx_v**2)
            beta[t_i,x_i_f] = b_1 - (a_1*c_1)/beta[t_i,x_i_f-1]
            d_i[t_i,x_i_f] = ((((f_prime_v*D_v)/(dx_v**2)) + ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f-1]) + (((1/dt_v)-((2*f_prime_v*D_v)/(dx_v**2))-(f_prime_v*K_v))*output_v[t_i-1,x_i_f]) + ((((f_prime_v*D_v)/(dx_v**2)) - ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f-1])
            gamma[t_i,x_i_f] = (d_i[t_i,x_i_f] - (a_1*gamma[t_i,x_i_f-1]))/beta[t_i,x_i_f] 
        #if x_i_f > 1 and x_i_f < grid_points_v-1: 
        if x_i_f >= 1 and x_i_f < grid_points_v-1: 
            beta[t_i,x_i_f] = b_1 - (a_1*c_1)/beta[t_i,x_i_f-1]        
            d_i[t_i,x_i_f] = ((((f_prime_v*D_v)/(dx_v**2)) + ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f-1]) + (((1/dt_v)-((2*f_prime_v*D_v)/(dx_v**2))-(f_prime_v*K_v))*output_v[t_i-1,x_i_f]) + ((((f_prime_v*D_v)/(dx_v**2)) - ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f+1])
            gamma[t_i,x_i_f] = (d_i[t_i,x_i_f] - (a_1*gamma[t_i,x_i_f-1]))/beta[t_i,x_i_f]
        if x_i_f == 1: 
            beta[t_i,x_i_f] = b_1        
            d_i[t_i,x_i_f] = ((((f_prime_v*D_v)/(dx_v**2)) + ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f-1]) + (((1/dt_v)-((2*f_prime_v*D_v)/(dx_v**2))-(f_prime_v*K_v))*output_v[t_i-1,x_i_f]) + ((((f_prime_v*D_v)/(dx_v**2)) - ((f_prime_v*V_v)/(2*dx_v)))*output_v[t_i-1,x_i_f+1]) + (((f_v*D_v)/(dx_v**2)) + ((f_v*V_v)/(2*dx_v)))*output_v[t_i,0]
            gamma[t_i,x_i_f] = d_i[t_i,x_i_f]/beta[t_i,x_i_f]
    # solve for u using backwards looping
    for x_i_b in range((grid_points_v-1),0,-1): 
        if x_i_b >= 1 and x_i_b < grid_points_v-1: 
            output_v[t_i,x_i_b] = gamma[t_i,x_i_b] - ((c_1*output_v[t_i,x_i_b+1])/beta[t_i,x_i_b])
        if x_i_b == grid_points_v-1:
            output_v[t_i,x_i_b] = gamma[t_i,x_i_b]

# plot
fig = plt.figure(figsize=[13,9])
for t_p in range((t_steps_v)):
    plt.plot(range(grid_points_v),output_v[t_p,:])

