import numpy as np


############################################################
#
#   Nested for-loops {100-1}-{0-511}
#   Each of {0-511} represents a possible configuration
#   of the board, many of these states are invalid or
#   cannot be reached by a prior state. These invalid
#   states are assigned an arbitrarily high value. Other
#   states can be assigned a cost the DP way (i.e. with our 
#   cost function and the future cost of going to the 
#   state. 
#
#   Cost = a*BLOCKS_OCCUPIED_IN_STATE - b*ROWS_ERASED
#   where a, b > 0, b >> a
#
#   Storing the costs at each stage will require a game
#   board that is of dimensions 512*100. 
#
############################################################

############################################################
#
#   The easiest invalid states to identify have rows that 
#   are occupied above rows that are empty. As well as
#   states with full rows.
#
#   In binary, these would be for example: 0b000111000, 
#   0b111000000, 0b111111000, 0b110010000.
#
#   A state admits a piece if AND-ing the state with the
#   piece gives the state. i.e. state & 0b000100100 = state
#   If a state does not admit a given piece it is also
#   considered invalid. 
#
############################################################

fullRows = [7, 56, 448]

def fullRowTest(state, removeRows):
    rowsToRemove = []
    if removeRows:
        for idx, row in enumerate(fullRows):
            if (row & state) == row:
                state = state & ~row
                rowsToRemove.append(idx)
        if (1 in rowsToRemove):
            state = state | ((state & fullRows[2]) >> 3)
            state = state & ~fullRows[2]
        if (0 in rowsToRemove):
            state = (state & (fullRows[1] | fullRows[2])) \
                    >> 3
        return [state, len(rowsToRemove)]
    else:
        for row in fullRows:
            if (row & state) == row:
                return True
        return False

def isStateValid (state):
    if state < 7:
        # only the bottom row is occupied or empty state
        return True
    elif (not state & 7):
        # catches 101010000, 110011000, etc.
        return False
    elif (state > 63) and (not state & 56):
        # cathes 111000111, 101000010, etc.
        return False
    elif (fullRowTest(state, False)):
        # catches full rows
        return False
    else:
        return True

def costOfState(state, numRowsRemoved):
    return format(state, '09b').count('1') - \
            10 * numRowsRemoved

def possibleNextStates(state, piece):
    nextStates = []
    for config in pieces[piece]:
        mask = pieces[piece][config]
        if (config & state == 0):
            if (mask & state) or (mask == 0):
                nextStates.append(state|config)
    return nextStates


############################################################
#
#   For placing pieces, have another mask to check if there
#   is enough support to place it there. i.e. AND together
#   0b000000100 AND 0b000000110 to make sure you can place
#   0b000110100. Should return the mask (0b000000100). A
#   given piece can have more than one mask, so OR them 
#   together and make sure when ANDing with state it gives
#   a result greater than 0.
#
#   Piece 0:
#
#   000         000         000         000
#   100         110         110         010
#   110         100         010         110
#
#   000100110   000110100   000110010   000010110
#   000010011   000011010   000011001   000001011
#   100110000   110100000   110010000   010110000   
#   010011000   011010000   011001000   001011000
#
#   38          52          50          22
#   19          26          25          11
#   304         416         400         176
#   152         208         200         88
#
############################################################

pieces = {}
pieces[0] = {
        38:0, 19:0, 304:(4 | 2 ),  152:(2 | 1 ),
        52:0, 26:0, 416:(4 | 16),  208:(2 | 8 ),
        50:0, 25:0, 400:(2 | 32),  200:(1 | 16),
        22:0, 11:0, 176:(2 | 4 ),   88:(2 | 1 )
        }

############################################################
#
#   Piece 1:
#   
#   000         010
#   110         110
#   011         100
#
#   000110011   010110100
#   110011000   001011010
#
#   51          180
#   408         90
#
############################################################

pieces[1] = {
        51:0, 408:(1 | 2 | 32), 180:0, 90:0
        }

############################################################
#
#   Piece 2:
#
#   000         000
#   100         000
#   100         110
#
#   000100100   000000110
#   000010010   000000011
#   000001001   000110000
#   100100000   000011000
#   010010000   110000000
#   001001000   011000000
#
#   36          6
#   18          3
#   9           48
#   288         24
#   144         384
#   72          192
#
############################################################

pieces[2] = {
        36:0, 18:0, 9:0, 288:4, 144:2, 72:1, 
        6:0, 3:0, 48:(4 | 2), 24:(2 | 1), 
        384:(32 | 16), 192:(16 | 8)
        }

############################################################
#
#   Functions:
#   + fullRowTest(state, removeRows)
#   + isStateValid(state)
#   + possibleNextStates(state, piece)
#   + costOfState(state, rowsRemoved)
#
###########################################################

# Creating a precomputed list of valid states, no matter 
# whether it is comprehensive of all invalid states or
# not, will improve computation time dramatically.

validStates = []
for state in range(0, 512):
    if isStateValid(state):
        validStates.append(state)

'''
for state in possibleNextStates(6, 3):
    print('main:possibleNextStates(192,1): ', 
            format(state, '09b'))
'''

numRounds = 100
sequencePattern = np.array([2, 0, 1])
pieceSequence = np.tile(sequencePattern, 100)

contPlan  = 100*np.ones((numRounds, 512), dtype=int)
costToGo = 100*np.ones((numRounds, 512), dtype=int)

validStatesList = validStates

for rnd in range(numRounds-2, -1, -1):
    piece = pieceSequence[rnd]
    if rnd == 0:
        validStatesList = [0]
    for state in validStatesList:
        minVal = costToGo[rnd, state]
        for nextState in possibleNextStates(state, piece):
            cleanNext, numRows = fullRowTest(
                    nextState, True)
            costOfNext = costOfState(cleanNext, numRows) +\
                    costToGo[rnd+1, cleanNext]
            if costOfNext < minVal:
                contPlan[rnd, state] = cleanNext
                minVal = costOfNext
        costToGo[rnd, state] = minVal

print("The pattern is ", sequencePattern)

nextState = np.argmin(costToGo[0,:])
for rnd in range(0, numRounds):
    state = nextState
    nextState = contPlan[rnd, state]
    print(format(state, '09b'), '-->', 
            format(nextState, '09b'), '\tPiece: ',
            pieceSequence[rnd], '\tCost: ',
            costToGo[rnd, state])

    
