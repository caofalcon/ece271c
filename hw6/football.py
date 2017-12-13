import numpy as np
from scipy.special import factorial

def evalDistribution(l, k):
    return np.exp(-l)*np.power(l,k)/factorial(k)

def sumDistribution(l, bot, top):
    sumDistr = 0
    for k in range(bot, top+1):
        sumDistr = sumDistr + evalDistribution(l, k)
    return sumDistr

def genPhi1st(l):
    phi1st = np.zeros((10,5,5))
    phi1st[:,4,4] = 1
    phi1st[:,0,0] = sumDistribution(l, 10, 100)
    phi1st[:,0,1] = sumDistribution(l, 0, 9)
    
    for down in range(1,4):
        for yards2first in range(0,10):
            phi1st[yards2first,down,down+1] = sumDistribution(l, 0, yards2first)
            phi1st[yards2first,down,0] = sumDistribution(l, yards2first+1, 100)

    return phi1st

l_r = 3
l_p = 10
p = 0.4
q = 0.05

c2g = np.zeros((51,5,10,100))
cp = np.zeros((100))
c2g[:,4,:,:] = 100

phi1st_r = genPhi1st(l_r)
phi1st_p = genPhi1st(l_p)


'''
for k in range(1,100):
    for yards2td in range(0,51):
        for down in range(0,4):
            if down == 0:
                yards2first = 10
                c2g[yards2td,down,yards
            else:
                for yards2first in range(0,11):
                '''
