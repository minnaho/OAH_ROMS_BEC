import numpy as np
from cvxopt import matrix,solvers

g1 = np.array([1.1,1.0,1.0,1.2,1.8,2.5,2.2,2.0,1.8,2.2,1.8,1.4])
g2 = np.array([1.4,1.1,1.0,1.0,1.2,1.8,2.5,2.2,2.0,1.8,2.2,1.8])
g3 = np.array([1.0,1.0,1.2,1.8,2.5,2.2,2.0,1.8,2.2,1.8,1.4,1.1])
g4 = np.array([1.0,1.2,1.8,2.5,2.2,2.0,1.8,2.2,1.8,1.4,1.1,1.0])
g5 = np.array([1.6,1.7,1.8,1.9,2.2,2.0,2.0,1.9,1.8,1.7,1.6,1.5])

g4_5 = np.array(g4,g5)

smin = np.zeros(12,4)
smax = np.zeros(12,4)
smax[:,:3] = 10
smax[:,3] = 15

r1 = np.empty(12,4)
r2 = np.empty(12,4)
r3 = np.empty(12,4)
r4 = np.empty(12,4)

c = matrix([r1,r2,r3,r4])

r1[1] = 4 - s[2,1] + 3
r2[1] = 4 - s[2,2] + 4
r3[1] = 4 - s[2,3] + r2[1]
r4[1] = 5 - s[2,4] + r1[1] + r3[1]

for t in range(2,12):
    for i range(5):
        if i == 1:
            r1[t] = s[t,i] - s[t+1,i] + 3
        elif i == 2:
            r2[t] = s[t,i] - s[t+1,i] + 4
        elif i == 3:
            r3[t] = s[t,i] - s[t+1,i] + r2[t]
        else:
            r4[t] = s[t,i] - s[t+1,i] + r1[t) + r3[t]
        A.append(r1[t],r2[t],r3[t],r4[t])
        b.append((g1[t]*r1[t])+(g2[t]*r2[t])+(g3[t]*r3[t])+(g4_5[t]*r4[t]))

r1[12] = s[12,1] - 4 + 3
r2[12] = s[12,2] - 4 + 4
r3[12] = s[12,3] - 4 + r2[12]
r4[12] = s[12,4] - 5 + r1[12] + r3[12]

sol = solvers.lp(c,A,b)
print(sol['x'])
