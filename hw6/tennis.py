import numpy as np
import matplotlib.pyplot as plt

########################################################################################################################
#   Homework 6.3 (7.1) - Tennis Problem
#   (F)ast and (S)low serves with probability of landing inbounds of p_F and p_S, and winning the point of
#   q_F and q_S, respectively. Solving for optimal contingency plan using value iteration.
#
#   Players start at 30-30 score. Thus, if either player goes ahead by 2 points, that player wins.
#   
#   8 states - {L, -1F, -1, 0F, 0, 1F, 1, W}
#               0   1    2  3   4   5   6  7
#
########################################################################################################################

def genPhi(p, q):
    phi = np.zeros((8,8), dtype=np.float)
    
    phi[0,0] = 1
    
    phi[1,0] = p * (1 - q) + (1 - p)
    phi[1,2] = p * q
    
    phi[2,0] = p * (1 - q)
    phi[2,1] = 1 - p
    phi[2,4] = p * q
    
    phi[3,2] = p * (1 - q) + (1 - p)
    phi[3,4] = p * q
    
    phi[4,2] = p * (1 - q)
    phi[4,3] = 1 - p
    phi[4,6] = p * q
    
    phi[5,4] = p * (1 - q) + (1 - p)
    phi[5,6] = p * q
    
    phi[6,4] = p * (1 - q)
    phi[6,5] = 1 - p
    phi[6,7] = p * q
    
    phi[7,7] = 1

    return phi

c2g = np.zeros((8, 100), dtype=np.float)
cp = np.zeros((8, 100), dtype=np.float)
c2g[0, :] = 100 # Penalty for losing

p_S = 0.95

q_F = 0.6
q_S = 0.4

prob = np.zeros(19)

phi_S = genPhi(p_S, q_S)

for p_F20 in range(0, 19):
    p_F = 1.0 * p_F20 / 20
    phi_F = genPhi(p_F, q_F)
    for k in range(1, 100):
        cp[:,k] = np.argmin(np.array([np.dot(phi_S, c2g[:,k-1]), np.dot(phi_F, c2g[:,k-1])]), axis=0)
        c2g[:,k] = 1 + np.amin(np.array([np.dot(phi_S, c2g[:,k-1]), np.dot(phi_F, c2g[:,k-1])]), axis=0)

    phi = (np.multiply(cp[:,99] == 1, phi_F.transpose()) + np.multiply(cp[:,99] == 0, phi_S.transpose())).transpose()
    phi_N = np.linalg.matrix_power(phi, 20)
    prob[p_F20] = phi_N[4, 7]

print(prob)

plt.plot(np.arange(9.5, step=0.5), prob)
plt.ylabel('Probability of winning')
plt.xlabel('p_F')
plt.show()

