import numpy as np
import matplotlib.pyplot as plt
plt.ion()
################
# one bloom
################

# parameters
i_m = 1
mu_p = .4
mu_z = .01
S0 = .15
s_m = 1
gamma = 0.35
eps = .028
k = 5

t0 = 365*2

N_plt = np.empty(int(t0))
P_plt = np.empty(int(t0))
Z_plt = np.empty(int(t0))

# initial conditions
N_plt[0] = 10
P_plt[0] = 2
Z_plt[0] = .1

dN_dt = np.empty(int(t0))
dP_dt = np.empty(int(t0))
dZ_dt = np.empty(int(t0))

I_t = np.empty(int(t0))
S_t = np.empty(int(t0))

# solve equations
for t in range(int(t0)):

    I_t[t] = 1-(i_m*np.cos((2*np.pi*t)/t0))
    S_t[t] = S0*(1+(s_m*np.cos((2*np.pi*t)/t0)))

    dN_dt[t] = ((-((mu_p)*I_t[t]*N_plt[t]*P_plt[t])/(k+N_plt[t]))+((1-gamma)*mu_z*P_plt[t]*Z_plt[t])+S_t[t])
    dP_dt[t] = (((mu_p*I_t[t]*N_plt[t]*P_plt[t])/(k+N_plt[t]))-(mu_z*P_plt[t]*Z_plt[t]))
    dZ_dt[t] = ((gamma*mu_z*P_plt[t]*Z_plt[t])-(eps*Z_plt[t]))
    
    if t == int(t0-1):
        break
    else:
        N_plt[t+1] = N_plt[t] + dN_dt[t]    
        P_plt[t+1] = P_plt[t] + dP_dt[t]    
        Z_plt[t+1] = Z_plt[t] + dZ_dt[t]    
    
# plot
axis_font = 14
title_font = 18
lw = 3
plt.figure(figsize=[13,7])
plt.plot(list(range(365)),N_plt[:365],'--',label='N',linewidth=lw)
plt.plot(list(range(365)),P_plt[:365],label='P',linewidth=lw)
plt.plot(list(range(365)),Z_plt[:365],'-.',label='Z',linewidth=lw)
plt.legend(loc='best',fontsize=16)
plt.gca().grid(True)
plt.xlabel('Time (days)',fontsize=axis_font)
plt.ylabel(r'$\mu$M/kg',fontsize=axis_font)
plt.title('NPZ model one bloom',fontsize=title_font)
plt.savefig('NPZ_plt_1peak.png',bbox_inches='tight')

############
# two blooms
############

# parameters
i_m = 1
mu_p = .4
mu_z = .01
S0 = .15
s_m = 1
gamma = 0.35
eps = .028
k = 5

t0 = 365*3

N_plt = np.empty(int(t0))
P_plt = np.empty(int(t0))
Z_plt = np.empty(int(t0))

# initial conditions
N_plt[0] = 20
P_plt[0] = 2
Z_plt[0] = .1

dN_dt = np.empty(int(t0))
dP_dt = np.empty(int(t0))
dZ_dt = np.empty(int(t0))

I_t = np.empty(int(t0))
S_t = np.empty(int(t0))

# solve equations
for t in range(int(t0)):

    I_t[t] = 1-(i_m*np.cos((2*np.pi*t)/t0))
    S_t[t] = S0*(1+(s_m*np.cos((2*np.pi*t)/t0)))

    dN_dt[t] = ((-((mu_p)*I_t[t]*N_plt[t]*P_plt[t])/(k+N_plt[t]))+((1-gamma)*mu_z*P_plt[t]*Z_plt[t])+S_t[t])
    dP_dt[t] = (((mu_p*I_t[t]*N_plt[t]*P_plt[t])/(k+N_plt[t]))-(mu_z*P_plt[t]*Z_plt[t]))
    dZ_dt[t] = ((gamma*mu_z*P_plt[t]*Z_plt[t])-(eps*Z_plt[t]))
    
    if t == int(t0-1):
        break
    else:
        N_plt[t+1] = N_plt[t] + dN_dt[t]    
        P_plt[t+1] = P_plt[t] + dP_dt[t]    
        Z_plt[t+1] = Z_plt[t] + dZ_dt[t]    
    
# plot
axis_font = 14
title_font = 18
lw = 3
plt.figure(figsize=[13,7])
plt.plot(list(range(365)),N_plt[:365],'--',label='N',linewidth=lw)
plt.plot(list(range(365)),P_plt[:365],label='P',linewidth=lw)
plt.plot(list(range(365)),Z_plt[:365],'-.',label='Z',linewidth=lw)
plt.legend(loc='best',fontsize=16)
plt.gca().grid(True)
plt.xlabel('Time (days)',fontsize=axis_font)
plt.ylabel(r'$\mu$M/kg',fontsize=axis_font)
plt.title('NPZ model two blooms',fontsize=title_font)
plt.savefig('NPZ_plt_2peaks.png',bbox_inches='tight')
