import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# gradient search algorithm

x1 = 12 
x2 = .5

x = np.array([x1,x2])

p_steps = []
f_x_pd = []
for i in range(10):

    df_x1 = 36-(10*x[0])-(8*x[1])
    df_x2 = 36-(10*x[1])-(8*x[0])
    d = np.array([df_x1,df_x2])

    no_p = (36*x[0])+(36*x[1])-(5*x[0]**2)-(8*x[0]*x[1])-(5*x[1]**2)
    # terms with p
    p = (36*d[0])+(36*d[1])-(5*2*x[0]*d[0])-(8*((x[0]*d[1])+(x[1]*d[0])))-(5*2*x[1]*d[1])
    # terms with p**2, multiplied by 2 for derivative value
    p2 = ((-5*d[0]**2)-(8*d[0]*d[1])-(5*d[1]**2))
    p2_derivative = 2*p2

    p_star = -p/p2_derivative
    f_x_pd.append(no_p + (p*p_star) + (p2*p_star*p_star))
    p_steps.append(p_star)

    p_d = p_star*d
    x = x+p_d


print('d: ',d)
print('p_star: ',p_star)
print('new x: ',x)

title_font = 18
axis_font = 14
plt.figure(figsize=[13,7])
plt.plot(p_steps,f_x_pd)
plt.title('Gradient Search Algorithm: Rate of convergence',fontsize=title_font)
plt.ylabel('f(x0 +pd)',fontsize=axis_font)
plt.xlabel('p',fontsize=axis_font)

# Newton's algorithm
x1 = 12 
x2 = .5

x = np.array([x1,x2])

p_steps = []
f_x_pd = []

# Hessian matrix inverse
H_inverse = np.array([[-10,8],[8,-10]])

df_x1 = 36-(10*x[0])-(8*x[1])
df_x2 = 36-(10*x[1])-(8*x[0])
del_f_T = np.array([df_x1,df_x2])

d = np.dot(H_inverse,del_f_T)/-36

no_p = (36*x[0])+(36*x[1])-(5*x[0]**2)-(8*x[0]*x[1])-(5*x[1]**2)
# terms with p
p = (36*d[0])+(36*d[1])-(5*2*x[0]*d[0])-(8*((x[0]*d[1])+(x[1]*d[0])))-(5*2*x[1]*d[1])
# terms with p**2, multiplied by 2 for derivative value
p2 = ((-5*d[0]**2)-(8*d[0]*d[1])-(5*d[1]**2))
p2_derivative = 2*p2

p_star = -p/p2_derivative
f_x_pd.append(no_p + (p*p_star) + (p2*p_star*p_star))
p_steps.append(p_star)

p_d = p_star*d
# no iterations because converges immediately
new_x = x+p_d


print('d: ',d)
print('p_star: ',p_star)
print('new x: ',x)

