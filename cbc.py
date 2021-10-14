import numpy as np
# from cylp.py import CyCbcModel, CyClpSimplex

from mip import *

def cbc2(cost_mat):
    numT,numC = np.shape(cost_mat)
    m = Model(sense=MINIMIZE, solver_name=CBC)

    x = []
    for t in range(numT):
	    x.append([])
	    for c in range(numC):
		    x[t].append(m.add_var(var_type=BINARY,name="x_%d_%d"% (t, c)))

    
    for t in range(numT):
        m+=xsum(x[t][c] for c in range(numC)) == 1
        
    for c in range(numC):
        m+=xsum(x[t][c] for t in range(numT)) == 1

    m.objective = xsum(xsum([x[t][c]*cost_mat[t][c] for c in range(numC)]) for t in range(numT))

    m.write('model.lp')

    m.max_gap = 0.05
    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(m.objective_value))
    elif status == OptimizationStatus.FEASIBLE:
        print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print('solution:')
        for v in m.vars:
            if abs(v.x) > 1e-6: # only printing non-zeros
                print('{} : {}'.format(v.name, v.x))


# def cbc(cost_mat):

#     model = CyLPModel()
#     numT,numC = np.MMshape(cost_mat)
    
#     x = []
#     for t in range(numT):
#         x.append([])
#         for c in range(numC):
#             x[t].append(model.addVariable(f'x_{t}-{c}'M))
    
#     for t in range(numT):
#            model+=np.sum(x[t][c] for c in range(numC)) == 1
        
#     for c in range(numC):
#            model+=np.sum(x[t][c] for t in range(numT)) == 1

#     model.objective = np.sum(np.sum([x[t][c]*cost_mat[t][c] for c in range(numC)]) for t in range(numT))

#     s = CyClpSimplex(model)
    
#     cbcModel = s.getCbcModel()
#     cbcModel.solve()


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

cbc2(c1)
