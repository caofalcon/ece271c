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

def optimal_coin_dispersion(change, coin_denominations):
    number_coins = np.zeros(np.shape(coin_denominations), dtype=np.int)
    NUM_ROUNDS = np.int(np.ceil(float(change) / np.min(coin_denominations))) + 1

    cost2go = NUM_ROUNDS*np.ones((NUM_ROUNDS, change+1))
    cost2go[NUM_ROUNDS-1, change] = 0

    contplan = -1*np.ones((NUM_ROUNDS,change+1), dtype=int)
    roundStart = 0
    for rnd in range(NUM_ROUNDS-2,-1,-1):
        for idx, coin in enumerate(coin_denominations):
            for nVal in range(0,change+1):
                if nVal < coin:
                    continue
                nextCost = cost2go[rnd+1, nVal]
                if nextCost == NUM_ROUNDS:
                    continue
                currCost = cost2go[rnd, nVal-coin]
                if currCost > nextCost+1:
                    cost2go[rnd, nVal-coin] = nextCost + 1
                    currCost = nextCost + 1
                    contplan[rnd, nVal-coin] = idx
        if cost2go[rnd,0] != NUM_ROUNDS:
            roundStart = rnd
            break

    val = 0
    for rnd in range(roundStart, NUM_ROUNDS-1):
        idx = contplan[rnd,val]
        number_coins[idx] = number_coins[idx] + 1
        val = val + coin_denominations[idx]
    return number_coins

change = 121
coin_denominations = np.array([1,5,8,33], dtype=np.int)
number_coins = optimal_coin_dispersion(change, coin_denominations)
print(number_coins)

change = 135
coin_denominations = np.array([1,7,11,32,63], dtype=np.int)
number_coins = optimal_coin_dispersion(change, coin_denominations)
print(number_coins)

change = 47
coin_denominations = np.array([1,5,10,25], dtype=np.int)
number_coins = optimal_coin_dispersion(change, coin_denominations)
print(number_coins)

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
        number_coins = optimal_coin_dispersion(change, coin_denominations)
        if maxCoins < np.sum(number_coins):
            maxCoins = np.sum(number_coins)
            maxAlloc = number_coins
    return maxCoins

minCoins = 100
maxCoins = 0
bestAlloc = np.zeros((4))
for x2 in range(2, 8):
    print('x2:', x2)
    for x3 in range(x2+1, 25):
        for x4 in range(x3+1, 50):
            if x3 == x4 or x2 == x4:
                continue
            maxCoins = maximum_coins_for_denominations(np.array([1,x2,x3,x4]))
            if minCoins >= maxCoins:
                minCoins = maxCoins
                bestAlloc = np.array([1,x2,x3,x4])
                print(minCoins, bestAlloc)

####################################################################################################
#
#   Minimum is 6 coins
#   [1 4 13 29]
#   [1 4 15 24]
#   [1 4 15 39]
#   [1 4 16 27]
#   [1 4 16 29]
#   [1 4 17 29]
#   [1 4 18 30]
#   [1 4 18 31]
#   [1 4 19 24]
#   [1 4 19 29]
#   [1 4 19 32]
#   [1 4 19 33]
#   [1 5 12 28]
#   [1 5 12 39]
#   [1 5 13 28]
#   [1 5 16 28]
#   [1 5 16 40]
#   [1 5 17 20]
#   [1 5 17 24]
#   [1 5 18 25]
#   [1 5 18 29]
#   [1 5 19 30]
#   [1 6 13 28]
#   [1 6 15 26]
#   [1 6 15 32]
#   [1 6 15 40]
#   [1 6 15 41]
#   [1 6 16 25]
#   [1 6 17 21]
#   [1 6 17 24]
#   [1 7 11 38]
####################################################################################################





