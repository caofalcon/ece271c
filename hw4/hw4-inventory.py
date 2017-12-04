import numpy as np

#################################################################
#   Homework #4 2. Inventory Problem
#   Compute the optimal inventory thresholds.
#
#   S_k's are the unconstrained minimizers of the expressions
#   cz_k + H(z_k) + E[J_{k+1}(z_k-w_k)]
#
#   where z_k = x_k + u_k, H(z_k) = E[r(z_k - w_k)]
#
#################################################################

def inventory(Bmin,Bmax,wmax,q0,p,h,c,N):
    w = np.array([0, wmax])
    q = np.array([q0, 1-q0])
    
    costToGo = np.zeros((N, Bmax+Bmin-wmax+1)) 
    contPlan = np.zeros((N))
    
    for rnd in range(N-2, -1, -1):
        for state in range(-Bmin+wmax, Bmax+1):
            x = state*np.ones((2))-w
            H = np.dot(q, p*np.amax(np.array([-x, 
                np.zeros((2))]), axis=0) + h*np.amax(
                    np.array([x, np.zeros((2))]), axis=0)) 
            costToGo[rnd,state+Bmin-wmax] = c*state + H + \
                    np.dot( q, costToGo[rnd+1, (x+(Bmin-wmax)\
                    *np.ones((2))).astype(int)] )

    contPlan = np.argmin(costToGo, axis=1)-Bmin+wmax
    return contPlan

S = inventory(10,10,2,0.5,1,1,1,10)
print('S = ', S)

############################## EOF ##############################









