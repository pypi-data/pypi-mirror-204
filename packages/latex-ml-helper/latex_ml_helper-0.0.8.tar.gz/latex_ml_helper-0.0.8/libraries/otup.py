def Imports():
    text = """
!pip install control

import numpy as np
import scipy.linalg as spla
import scipy.sparse as sps
import matplotlib.pyplot as plt
import os
import math
import cmath
from sympy import *
import control as ct
from control.matlab import *
import scipy.integrate as integrate
from scipy.integrate import quad
from numpy.linalg import eig, svd, det
from scipy.integrate import solve_ivp
"""
    return text

def graphic_solution():
    text = """
sys = ss(A, B, C, D)
x0 = [0, 1, 0]
u0 = np.array([[1, 2] for i in range(2000)]).T
tt = np.arange(0, 200, 0.1)
T, yout = ct.forced_response(sys, tt, u0, x0)
plt.plot(T.T, yout.T)
"""
    return text

def graphic_solution2():
    text = """
x0 = [10,0]
u =0.5
tt = np.arange(0,140,0.1)

T, yout =ct.forced_response(sys_lin,tt,u,x0)

plt.plot(T.T,yout.T)
"""
    return text

def C_m():
    text = """
C_M = ct.ctrb(A, B)
C_M

U, sigma, VT = svd(C_M)
print(sigma)
plt.semilogy(sigma)
"""
    return text

def jordan_form_solution():
    text = """
P, J = A.jordan_form()
print(A.eigenvals())
J
"""
    return text

def tf():
    text = """
#sys = ss(A, B, C, D)
#G = ct.tf(sys)
"""
    return text

def tf2():
    text = """
s = symbols("s")
G = C * (s * eye(A.shape[0]) - A) ** (-1) * B
simplify(G)
"""
    return text

def e_At():
    text = """
t = symbols('t')
At = t * A
At.exp()  # e^tA
"""
    return text

def solution():
    text = """
x = symbols('x')
expr = (x + 2) * (x - 3)


sol = solve(expr)

sol[1], sol[0]
"""

    return text

def lyapunov():
    text = """
P = Matrix(lyap(Transpose(A),eye(4)))
# Postoji pozitivno definitna, simetrična P...
print(P.eigenvals())
P  
# -> Sustav je stabilan jer postoji takva P simetrična, pozitivno definitna.

# ... takva da je: A'*P+P*A=-I.  (Provjera)
Transpose(A)*P+P*A # <- mora bit jedinicna matrica
"""
    return text

def help_otup():
    text = """
Imports() <- import libraries
graphic_solution() <- graphic solution u = [1, 2]
graphic_solution2() <- graphic solution u = 0.5
C_m() <- controllability matrix
jordan_form_solution() <- jordan form
tf() <- transfer function
tf2() <- transfer function custom
e_At() <- e^At
solution() <- rjesavanje jednadzbi
lyapunov() <- lyapunov
"""

    return text
