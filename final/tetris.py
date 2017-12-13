import numpy as np

def isBoxEnclosed(maze, x, y):
    if maze[x,y] == 2:
        return True
    elif maze[x,y] == 1:
        return False
    elif maze[x,y] == 3:
        return False

    maze[x,y] = 3

    # Can't move down a row because pieces can't rise
    if ((x < 13 and isBoxEnclosed(maze, x+1,y))
        or (y > 0 and isBoxEnclosed(maze, x,y-1))
        or (y < 7 and isBoxEnclosed(maze, x,y+1))):      
        return True

    return False



def controlSpace(board, piece, orient):
    ctrl = []
    landingHeightList = []
    p = np.copy(piece)
    tmp = np.zeros((14,8), dtype=int)
    for idx in range(0,orient):
        for row in range(0,14):
            for col in range(0,8):
                if row + np.shape(p)[0] > 14:
                    continue
                if col + np.shape(p)[1] > 8:
                    continue

                if row != 0:
                    if np.sum(board[row-1,:]) == 0: 
                        continue

                if row != 0:
                    if np.sum(np.multiply(board[row-1:row-1+np.shape(p)[0],col:col+np.shape(p)[1]], p)) == 0: 
                        continue

                if np.sum(board[row+np.shape(p)[0]:row+np.shape(p)[0]+1, col:col+np.shape(p)[1]]) == np.shape(p)[1]:
                    maze = np.copy(board)
                    maze[13,:] = maze[13,:] + 2*(maze[13,:] == 0)
                    if not isBoxEnclosed(maze, row, col):
                        continue
                    
                tmp = np.copy(board)
                tmp[row:row+np.shape(p)[0],col:col+np.shape(p)[1]] = board[row:row+np.shape(p)[0],col:col+np.shape(p)[1]] | p

                if np.sum(tmp-board) < 4:
                    continue


                ctrl.append(np.copy(tmp))
                landingHeightList.append(row)

    
        p = np.rot90(p)

    options = []
    # Statistics
    for idx, tmp in enumerate(ctrl):
        board = np.copy(tmp)
        removedLines = 0
        for row in range(13,-1,-1):
            if np.sum(board[row]) == 8:
                removedLines = removedLines + 1
                board[row:13,:] = board[row+1:14,:]
                board[13,:] = 0
            
        ctrl[idx] = board
        
        pileHeight = 0
        lowestOccupied = 14
        holes = 0
        connectedHoles = 0
        maxWellDepth = 0
        sumOfAllWells = 0
        columnTransitions = 0
        rowTransitions = 0
        weightedBlocks = 0

        columnPeaks = np.zeros(8,dtype=int)

        brd = np.insert(board,0,1,axis=0)
        brd = np.insert(brd,0,1,axis=1)
        brd = np.append(brd,np.ones((15, 1)),axis=1)
        

        for col in range(0,10):
            if col > 0 and col < 9:
                listOfOnes = np.argwhere(brd[:,col] == np.amax(brd[:,col])).flatten()
                holes = holes + np.sum(np.diff(listOfOnes)-1)
                connectedHoles = connectedHoles + np.sum((np.diff(listOfOnes)-1) > 0)
                if np.max(listOfOnes) > pileHeight:
                    pileHeight = np.max(listOfOnes)
                if np.max(listOfOnes) < lowestOccupied:
                    lowestOccupied = np.max(listOfOnes)
                columnPeaks[col-1] = np.max(listOfOnes)

            convCol = np.convolve([-1,1], brd[:,col] - (brd[:,col] == 0), 'same')[1:]
            columnTransitions = columnTransitions + np.sum(np.abs(convCol)) / 2

        for row in range(0,15):
            convRow = np.convolve([-1,1], brd[row,:] - (brd[row,:] == 0), 'same')[1:]
            rowTransitions = rowTransitions + np.sum(np.abs(convRow)) / 2
            weightedBlocks = weightedBlocks + np.sum(brd[row,1:9]) * row

        columnPeakDiff = np.diff(columnPeaks)
        for col in range(0,7):
            if col == 0:
                if columnPeakDiff[col] < 0:
                    continue
                wellDepth = columnPeakDiff[col]
            elif col == 6:
                if columnPeakDiff[col] > 0:
                    continue
                wellDepth = np.abs(columnPeakDiff[col])
            else:
                if columnPeakDiff[col] > 0:
                    continue
                wellDepth = min([np.abs(columnPeakDiff[col]), np.abs(columnPeakDiff[col+1])])
            sumOfAllWells = sumOfAllWells + wellDepth
            if maxWellDepth < wellDepth:
                maxWellDepth = wellDepth


        options.append(
                {
                    'board': board,
                    'pileHeight': pileHeight,
                    'holes': holes,
                    'connectedHoles': connectedHoles,
                    'removedLines': removedLines,
                    'altitudeDifference': pileHeight - lowestOccupied,
                    'maxWellDepth': maxWellDepth,
                    'sumOfAllWells': sumOfAllWells,
                    'landingHeight': landingHeightList[idx],
                    'blocks': np.sum(board),
                    'weightedBlocks': int(weightedBlocks),
                    'columnTransitions': int(columnTransitions),
                    'rowTransitions': int(rowTransitions)
                    }
                )

    return options

piece = []

piece.append(np.ones((4,1), dtype=int))
piece.append(np.ones((2,2), dtype=int))
piece.append(np.ones((2,3), dtype=int))
piece[2][0,0:2] = 0
piece.append(np.ones((2,3), dtype=int))
piece[3][0,1:3] = 0
piece.append(np.ones((2,3), dtype=int))
piece[4][0,0] = 0
piece[4][0,2] = 0
piece.append(np.ones((2,3), dtype=int))
piece[5][1,0] = 0
piece[5][0,2] = 0
piece.append(np.ones((2,3), dtype=int))
piece[6][0,0] = 0
piece[6][1,2] = 0

orient = {}

orient[0] = 2
orient[1] = 1
orient[2] = 4
orient[3] = 4
orient[4] = 4
orient[5] = 2
orient[6] = 2

board = np.zeros((14,8), dtype=int)

'''
maze = np.copy(board)
maze[0:4,7] = 1
maze[4,0:8] = 1
maze[13,:] = maze[13,:] + 2*(maze[13,:] == 0)
print(maze)
print(isBoxEnclosed(maze, 0,6))


'''

pileHeight = 0
while(1):
    ctrl = controlSpace(board, piece[0], orient[0])
    for idx, option in enumerate(ctrl):
        print('\nOption:', idx)
        for val in option:
            if val == 'board':
                print(np.flip(option[val],axis=0))
            else:
                print(val, ': ', option[val])
    idx = input()
    board = ctrl[int(idx)]['board']

