#from cvxpy import *
import cvxpy as cp
import numpy as np

x = cp.Variable(2)
c = np.array([1,-1])
A = np.array([[-1,1],[-1,-1],[1,0],[0,1]])
b = np.array([[-2],[-6],[0],[0]])

obj = cp.Minimize(np.transpose(c)*x)
constraints = [A*x>=b]
prob = Problem(obj,constraints)
result = prob.solve()
print(x.value)
print(result)
