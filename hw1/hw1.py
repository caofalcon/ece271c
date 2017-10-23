'''

hw1.py

Implements a dynamic programming algorithm in function
'pathplan' that takes in a 3-dimensional numpy array 
defining a path-finding problem, and outputs the 
optimal route.

'''


import numpy as np

def pathplan ( L ):
    '''
    num_nodes - number of nodes per stage
    num_stages - total number of stages
    '''
    num_nodes = np.size(L[:,0,0])
    num_stages = np.size(L[0,0,:])

    '''
    contingency_plan - np array with ik indexing
    i.e. first index is node number, second index is stage
    number
    '''
    cont_plan = np.array(np.zeros((num_nodes,num_stages)))
    route = np.array(np.zeros((num_stages,)))
    
    for stage in range(num_stages-1, 0, -1):
        a = np.tile(cont_plan[:,stage], (num_nodes, 1))
        cont_plan[:,stage-1] = np.amin(L[:,:,stage-1] + a, 
                axis=1)
        route[stage-1] = np.argmin(cont_plan[:,stage-1])

    # print("route1: ", route1)
    # route = np.argmin(cont_plan, axis=0)
    return route

'''
L is the 3-dimensional array containing the  posed path-
finding problem.

The first index corresponds to the current node number 'i'
The second index corresponds to the next node number 'j'
The third index corresponds to the stage number 'k'

L[i,j,k] is the penalty for travelling from node 'i' in
stage 'k' to node 'j' in stage 'k+1'

'''

L = np.array([[[1,2,3,4,0],[9,1,4,5,0],[5,6,7,8,0]],
              [[2,2,3,6,0],[2,3,4,9,0],[5,6,1,6,0]],
              [[3,2,3,5,0],[3,3,4,3,0],[5,6,7,1,0]]])

route = pathplan(L)
print("The optimal path is: ", route)
