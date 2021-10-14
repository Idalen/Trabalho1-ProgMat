from gurobipy import *
import numpy as np

def guropi(cost_mat):

    m = Model("Assigment")
    numT,numC = np.shape(cost_mat)
     
    # cria variaveis
    #x = m.addMVar(shape=(numT,numC), name="x", vtype=GRB.BINARY)    

    x = []
    for t in range(numT):
	    x.append([])
	    for c in range(numC):
		    x[t].append(m.addVar(vtype=GRB.BINARY,name="x %d %d"% (t, c)))

    m.update()

    constraintT = []
    constraintC = []

    for t in range(numT):
	    constraintT.append(
            m.addConstr(quicksum(x[t][c] for c in range(numC)) == 1 ,'constraintT%d' % c)
        )
	
    for c in range(numC):
	    constraintT.append(
            m.addConstr(quicksum(x[t][c] for t in range(numT)) == 1 ,'constraintC%d' % t)
        )



    m.setObjective(quicksum(quicksum([x[t][c]*cost_mat[t][c] for c in range(numC)]) for t in range(numT)))
    #m.setObjective()
    
    m.optimize()

    print(f"Optimal objective value: {m.objVal}")


# Toy problems
# n = 4
c1 = np.array([[20, 28, 19, 13],
               [15, 30, 31, 28],
               [40, 21, 20, 17],
               [21, 28, 26, 12]])
# Solução otimizada: (0, 2) + (1, 0) + (2, 1) + (3, 3) = 19 + 15 + 21 + 12 = 67

c2 = np.array([[35,  0,  0,  0],
               [ 0, 30,  0,  5],
               [55,  5,  0, 10],
               [ 0, 45, 30, 45]])
# Solução otimizada: (0, 3) + (1, 2) + (2, 1) + (3, 0) = 0 + 0 + 5 + 0 = 5

# n = 5
c3 = np.array([[0, 1, 0, 1, 1],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 0, 1],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 1, 0]])
# Solução otimizada: (0, 0) + (1, 4) + (2, 3) + (3, 2) + (4, 1) = 0 + 1 + 0 + 0 + 0 = 1

c4 = np.array([[2, 9, 2, 7, 1],
               [6, 8, 7, 6, 1],
               [4, 6, 5, 3, 1],
               [4, 2, 7, 3, 1],
               [5, 3, 9, 5, 1]])
# Solução otimizada: (0, 2) + (1, 4) + (2, 3) + (3, 0) + (4, 1) = 2 + 1 + 3 + 4 + 3 = 13

guropi(c1)
