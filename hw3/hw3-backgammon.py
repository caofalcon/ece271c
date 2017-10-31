import numpy as np

NUM_ROUNDS = 100

#################################################################
#
#   The cost-to-go should be the expected value for number of
#   turns it will take to reach the end. Thus,
#
#   g(x_k, u_k) = sum (1 + Pr[x_k+1] * J_k+1(x_k+1))
#
#   J_N(x_N) = { 0 if x_N == 0, 100 else }
#
#################################################################

#################################################################
#
#   combos.npy contains a pre-computed NumPy-array that hashes
#   each of i e [0, 3002] to a unique state x_i.
#
#   These states are all coded as 6-digit decimal integers.
#
#   i.e.    comboArr[0]     = 000000
#           comboArr[3002]  = 800000
#
#   TODO: Might need a hashing function for the opposite
#   direction - mapping states to their index. Use binary
#   search, as this is a sorted-list.
#
#################################################################

#################################################################
#
#   Function to generate all possible future states from
#   current state. Each future state has a certain probability
#   of coming to be, which will be multiplied by the cost of
#   advancing to that state.
#
#   The 6th bin is actually in the 0 index. So we will be adding
#   to 6.
#
#################################################################

def singleRollStates(state, roll):
    numAsNPArray = np.array(list(str(state))).astype(int)
    highestBin = np.argmax(numAsNPArray > 0)

    nextStates = []

    if roll >= 6 - highestBin:
        # take pieces home
        # print(6 - highestBin, '<=', roll)
        for binIdx in range(highestBin, 6):
            if numAsNPArray[binIdx] == 0:
                continue
            tempState = np.array(numAsNPArray, copy=True)
            tempState[binIdx] = tempState[binIdx] - 1
            # print('tempState: ', tempState)
            nextStates.append( int(
                ''.join(map(str,tempState))) )
    else:
        # shift pieces forward
        # print(6 - highestBin, '>',  roll)
        for binIdx in range(highestBin, 6 - roll):
            if numAsNPArray[binIdx] == 0:
                continue
            tempState = np.array(numAsNPArray, copy=True)
            tempState[binIdx] = tempState[binIdx] - 1
            tempState[binIdx + roll] = \
                    tempState[binIdx + roll] + 1
            # print('tempState: ', tempState)
            nextStates.append( int(
                ''.join(map(str,tempState))) )
    
    return nextStates

def possibleNextStates(state, roll):
    # every roll has probability 1/36, so just generate
    # what next states come out of specific roll
    if state == 0 or state == 1 or state == 2 or \
            state == 10:
        return [0]

    firstRollStates = singleRollStates(format(state, '06d')
            , max(roll) )
    # print('firstRollStates: ', firstRollStates)
    nextStates = []

    for rollState in firstRollStates:
        nextStates = nextStates + singleRollStates(
                format(rollState, '06d'), min(roll) )

    nextStates = nextStates + singleRollStates(
            format(state, '06d'), sum(roll) )
    
    nextStates = set(nextStates)
    return nextStates

def printState(state):
    print(format(state, '06d'))

def numPieces(state):
    numAsNPArray = np.array(list(str(state)))
    return np.sum(numAsNPArray.astype(int))

comboArr = np.load('combos.npy')
gameDims = np.shape(comboArr)

contPlan = np.zeros((NUM_ROUNDS, gameDims[0], 36))

costToGo = np.zeros((NUM_ROUNDS, gameDims[0]))
costToGo[NUM_ROUNDS-1,:] = 100*np.ones((gameDims[0]))
costToGo[NUM_ROUNDS-1,0] = 0

stateS = 230021
stateD = 000000

possibleRolls = []

for die1 in range(1,7):
    for die2 in range(1,7):
        possibleRolls.append( (die1, die2) )

probMtx = np.load('probMtx.npy')

# probMtx = np.zeros((3003, 3003), dtype=np.float)
# 
# for sIdx, state in enumerate(comboArr):
#     for roll in possibleRolls:
#         for nextState in possibleNextStates(state, roll):
#             nIdx = np.searchsorted(comboArr, nextState)
#             probMtx[sIdx][nIdx] += 1./36
# 
# np.save('probMtx.npy', probMtx)
# 
# print (possibleNextStates(stateS, (6,5)))

#################################################################
#   EOF










