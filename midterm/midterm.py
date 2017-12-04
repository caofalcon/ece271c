####################################################################################################
#
#   ECE 271C: Dynamic Programming MIDTERM 2017 
#
#   Given a set of coin denominations and a desired change amount, find the most efficient
#   allocation of coins according to different measures of efficiency.
#
#   1. Number of coins
#   2. 
#
####################################################################################################


import numpy as np

####################################################################################################
#   
#   1. Number of coins is the measure of efficiency. Assuming we add maximum one coin per round,
#   this means we would like to minimize the number of rounds it takes to achieve the desired
#   change amount.
#
#   i.e. J_k(x_k) = min u_k {   1 + J_{k+1}(x_k + v_i) to add a coin i
#
#   where x_k is the value achieved.
#
#   J_N(x_N) = 0
#
####################################################################################################

def optimal_coin_dispersion(change, coin_denominations, p1, p2):
    number_coins = np.zeros(np.shape(coin_denominations), dtype=np.int)
    NUM_ROUNDS = np.int(np.ceil(float(change) / np.min(coin_denominations))) + 1

    cost2go = NUM_ROUNDS*np.ones((NUM_ROUNDS, change+3))
    cost2go[NUM_ROUNDS-1, 0] = 0

    contplan = -1*np.ones((NUM_ROUNDS,change+1), dtype=int)
    roundStart = 0
    minVal = NUM_ROUNDS
    for rnd in range(NUM_ROUNDS-2,-1,-1):
        for idx, coin in enumerate(coin_denominations):
            for val in range(0,change+1):
                if val < coin:
                    continue

                nextCost0 = cost2go[rnd+1, val-coin] + 1
                nextCost1 = cost2go[rnd+1, val-coin+1] + 1
                nextCost2 = cost2go[rnd+1, val-coin+2] + 1

                nextCost = (1-p1-p2)*nextCost0 + p1*nextCost1 + p2*nextCost2

                currCost = cost2go[rnd, val]

                if currCost > nextCost:
                    cost2go[rnd, val] = nextCost
                    currCost = nextCost
                    contplan[rnd, val] = idx
    
        if cost2go[rnd,change] < minVal:
            minVal = cost2go[rnd,change]
            roundStart = rnd

    val = change
    for rnd in range(roundStart, NUM_ROUNDS-1):
        idx = contplan[rnd, val]
        number_coins[idx] = number_coins[idx] + 1
        val = val - coin_denominations[idx]
        if val < 0:
            break

    return number_coins

# change = 135
# coin_denominations = np.array([1,7,11,32,63], dtype=np.int)
# number_coins = optimal_coin_dispersion(change, coin_denominations, 0, 0)
# print(number_coins)
# 
# change = 135
# coin_denominations = np.array([1,7,11,32,63], dtype=np.int)
# number_coins = optimal_coin_dispersion(change, coin_denominations, 0.1, 0.05)
# print(number_coins)
# 
# 
# change = 135
# coin_denominations = np.array([1,7,11,32,63, 100], dtype=np.int)
# number_coins = optimal_coin_dispersion(change, coin_denominations, 0.08, 0.05)
# print(number_coins)
# 
# change = 47
# coin_denominations = np.array([1,5,10,25], dtype=np.int)
# number_coins = optimal_coin_dispersion(change, coin_denominations, 0, 0)
# print(number_coins)

####################################################################################################
#
#   2. Minimize the maximum number of coins used for any change amount y in {1,2,...,99}
#
#
####################################################################################################

def maximum_coins_for_denominations(coin_denominations):
    maxCoins = 0
    maxAlloc = np.zeros(np.shape(coin_denominations))
    for change in range(1,100):
        number_coins = optimal_coin_dispersion(change, coin_denominations, 0.1, 0.05)
        if maxCoins < np.sum(number_coins):
            maxCoins = np.sum(number_coins)
            maxAlloc = number_coins
    return maxCoins

minCoins = 100
maxCoins = 0
bestAlloc = np.zeros((4))
for x2 in range(99, 1, -1):
    print('x2:', x2)
    for x3 in range(10, 25):
        for x4 in range(5, 15):
            if x3 == x4 or x2 == x4:
                continue
            maxCoins = maximum_coins_for_denominations(np.array([1,x2,x3,x4]))
            if minCoins >= maxCoins:
                minCoins = maxCoins
                bestAlloc = np.array([1,x2,x3,x4])
                print(minCoins, bestAlloc)







