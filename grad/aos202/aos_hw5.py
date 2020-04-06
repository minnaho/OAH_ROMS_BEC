import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
#plt.ion()

Q0 = 50
t0 = 3.15E7
tQ = .5*t0
T_tQ = 5
p0 = 1E3
Cp = 4E3

# part a
h0_a = 75
t_var = np.linspace(0,t0,t0+1)
#T_t = ((Q0*t0)/(2*math.pi*p0*Cp))*(math.sin(2*math.pi*((t_var-tQ)/t0))/h0)

temp_a = np.empty((int(t0)))
temp_b = np.empty((int(t0)))
temp_c = np.empty((int(t0)))
h_b = np.empty((int(t0)))
h_c = np.empty((int(t0)))

h_q_b = 75 + (50*math.cos(2*math.pi*tQ/t0))
h_q_c = 75 + (50*math.cos((2*math.pi*(tQ-(.25*t0)))/t0))

for i_t in range(len(t_var)-1):
    # part a
    T_t_a = ((T_tQ*h0_a)/h0_a) + (((Q0*t0)/(2*math.pi*p0*Cp))*(math.sin(2*math.pi*((i_t-tQ)/t0))/h0_a))
    temp_a[int(i_t)] = T_t_a

    # part b
    h0_b = 75 + (50*math.cos(2*math.pi*i_t/t0))
    
    T_t_b = ((T_tQ*h_q_b)/h0_b) + (((Q0*t0)/(2*math.pi*p0*Cp*h0_b))*(math.sin(2*math.pi*((i_t-tQ)/t0))))
    h_b[i_t] = h0_b
    temp_b[int(i_t)] = T_t_b

    # part c
    h0_c = 75 + (50*math.cos((2*math.pi*(i_t-(.25*t0)))/t0))
    T_t_c = ((T_tQ*h_q_c)/h0_c) + (((Q0*t0)/(2*math.pi*p0*Cp*h0_c))*(math.sin(2*math.pi*((i_t-tQ)/t0))))
    h_c[i_t] = h0_c
    temp_c[int(i_t)] = T_t_c

plt.figure(figsize=[13,8])
plt.plot(temp_a,label='a. constant h(t) = 75 m')
plt.plot(temp_b,'--',label='b. variable h(t) peak depth at winter solstice')
plt.plot(temp_c,':',label='c. peak depth at spring equinox')

plt.ylabel('Temperature T(t)',fontsize=14)
plt.xlabel('Time (s)',fontsize=14)
plt.annotate('spring equinox',xy=(.25*t0-2.7E6,4.3),fontsize=14)
plt.annotate('fall equinox',xy=(.75*t0-2.1E6,5.25),fontsize=14)
plt.legend(loc='best',fontsize='large')
ax = plt.gca()
ax.grid(True)
plt.savefig('plot_aos_hw5_2pi.png',bbox_inches='tight')



