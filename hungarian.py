import numpy as np
import networkx as nx

def drawLines(matrix,assignedMatrix):
    rowsMarked = [1 if np.sum(row)==0 else 0 for row in assignedMatrix] #Tick an unassigned row
    colsMarked = [0]*len(rowsMarked) #Tick an unassigned column
    
    #print("rowsMarked")
    #print(rowsMarked)
    #print("colsMarked")
    #print(colsMarked)
    #print("\n\n\n")

    while True:
        ticks = 0
        for i in range(len(matrix)):
            if rowsMarked[i] <= 0:
                continue #If not a ticked row
            #print("Line "+str(i)+" marked")
            toTickCols = list(np.where(matrix[i,:] <= 0)[0]) #If a ticked row has a 0, then tick the corresponding column
            #print("toTickCols")
            #print(toTickCols)
            for j in toTickCols:
                if colsMarked[j] == 0:
                    ticks += 1
                    colsMarked[j] = 1
            rowsMarked[i] = -1


        for j in range(len(matrix)): 
            if colsMarked[j] <= 0:
                continue
            #print("Col "+str(j)+" marked")

            toTickRows = list(np.where(matrix[:,j] == 0)[0])
            #print("toTickRows")
            #print(toTickRows)

            for i in toTickRows:
                if rowsMarked[i] == 0:
                    ticks += 1
                    rowsMarked[i] = 1
            colsMarked[j] = -1

        if ticks == 0:
           break

    colsMarked = [0 if i == 0 else 1 for i in colsMarked]
    
    rowsUnmarked = [1 if i == 0 else 0 for i in rowsMarked]

    #print(rowsUnmarked)
    #print(colsMarked)

    return rowsUnmarked, colsMarked

#OK
def assignMatrix(matrix):
    assignedMatrix = np.zeros((len(matrix),len(matrix)), dtype=int)
    #print("PRE-MATRIX")
    #print(matrix)

    for i in range(len(matrix)):
        zeroesInRow = np.where(matrix[i,:] == 0)[0]
        if len(zeroesInRow) >= 1:
            assignedMatrix[i][zeroesInRow[0]] = True
            
            matrix[:,zeroesInRow[0]][matrix[:,zeroesInRow[0]] == 0] = -1
            matrix[i,:][matrix[i,:] == 0] = -1
            matrix[i,zeroesInRow[0]] = 0
    
    #print("assignedMatrix\n")
    #print(assignedMatrix)
    #print("matrix\n")
    #print(matrix)
    return assignedMatrix, matrix
    
        
#OK
def squarenizeMatrix(matrix):
    matrixShape = np.shape(matrix)
    if matrixShape[0] != matrixShape[1]:
        maxShape = max(matrixShape)
        squareMatrix = np.zeros((maxShape,maxShape))
        squareMatrix[:matrixShape[0],:matrixShape[1]] = matrix
        return squareMatrix
    else:
        return matrix


#OK
def matrixReduction(matrix):
    matrix -= np.min(matrix,axis=1)[:,None] #By each line
    matrix -= np.min(matrix,axis=0) #By each column
    return matrix



def getMinVal(crossedMatrix,rowsUnmarked,colsMarked):
    minVal = float("inf")
    for i in range(len(crossedMatrix)):
        if rowsUnmarked[i] == 1:
            continue
        for j in range(len(crossedMatrix)):
            if colsMarked[j] == 1:
                continue
            if crossedMatrix[i][j] < minVal:
                minVal = crossedMatrix[i][j]
    return minVal

def fixMatrix(matrix,rowsUnmarked,colsMarked,minVal):
    fixedMatrix = matrix
    lenM = len(matrix)
    rowsTuple = tuple([i for i in range(lenM) if rowsUnmarked[i] == 1])
    colsTuple = tuple([i for i in range(lenM) if colsMarked[i] == 1])
    fixedMatrix -= minVal
    fixedMatrix[rowsTuple,:] += minVal
    fixedMatrix[:,colsTuple] += minVal

    return fixedMatrix



def alterMatrixValues(crossedMatrix,rowsUnmarked,colsMarked):
    crossedMatrix[crossedMatrix == -1] = 0
    minVal = getMinVal(crossedMatrix,rowsUnmarked,colsMarked)
    #print("minVal: "+str(minVal))
    return fixMatrix(crossedMatrix,rowsUnmarked,colsMarked,minVal)

def getJobs(matrix):
    matrix[matrix == -1] = 0
    #print("matrix")
    #print(matrix)
    #Create graph
    G = nx.Graph()
    for i in range(len(matrix)):
        G.add_node((i,"worker"),bipartite=0)
        G.add_node((i,"job"),bipartite=1)
    
    zeroes = np.where(matrix == 0)
    edges = [[(zeroes[0][i],"worker"),(zeroes[1][i],"job")] for i in range(len(zeroes[0]))]
    #print("edges")
    #print(edges)
    G.add_edges_from(edges)
    #get maximal cardinality matching from biparted graph G
    matching = list(nx.max_weight_matching(G,maxcardinality=True))
    #plot matching pairs
    #nx.draw_networkx_nodes(G,pos=nx.spring_layout(G),nodelist=matching,node_color='r')
    #print("\n\nmatching")
    #print(matching)
    jobs = np.array([[match[0][0],match[1][0]] if match[0][1] == "worker" else (match[1][0],match[0][0]) for match in matching])
    return [tuple(jobs[:,0]),tuple(jobs[:,1])]

def oldGetJobs(matrix):
    matrix[matrix == -1] = 0
    worked = {}
    #print("matrix")
    #print(matrix)
    for workerId in range(len(matrix)):
        #print("matrix in worker"+str(workerId))
        #print(matrix)
        #print("Entering search for worker"+str(workerId))
        qtts = [[len(list(np.where(matrix[j,:] == 0)[0])),j] for j in range(len(matrix)) if not j in worked]
        minZeroesLine = min(qtts)[1]
        cols = list(np.where(matrix[minZeroesLine,:] == 0)[0])
        worked[minZeroesLine] = cols[0]
        matrix[:,cols[0]][matrix[:,cols[0]] == 0] = -1
        #print("qtts")
        #print(qtts)
        #print("\n\n\n\n")
    listOfKeyVal = np.array([[k, v] for k, v in worked.items()])
    likv2 = [tuple(listOfKeyVal[:,0]),tuple(listOfKeyVal[:,1])]
    return likv2

def hungarianMethod(matrix):
    oldMatrix = np.copy(matrix)
    squareMatrix = squarenizeMatrix(matrix)
    squareMatrix = matrixReduction(squareMatrix)    
    #print("squareMatrix\n")
    #print(squareMatrix)
    ##print(crossedMatrix)
    linesQtty = 0
    iter = 1
    while True:
        #print("Part "+str(iter))
        assignedMatrix, crossedMatrix = assignMatrix(squareMatrix)
        rowsUnmarked, colsMarked = drawLines(crossedMatrix,assignedMatrix)
        if (np.sum(rowsUnmarked) + np.sum(colsMarked)) >= len(crossedMatrix):
            break
        squareMatrix = alterMatrixValues(crossedMatrix,rowsUnmarked,colsMarked)
        iter += 1
    jobs = getJobs(crossedMatrix)
    print("Jobs: "+str(jobs))   
    return np.sum(oldMatrix[tuple(jobs)])
    
#assign a row if it has only one 0, else skip the row temporarily
#cross out the 0's in the assigned column
#assign a row if it has only one 0, else skip the row temporarily
#cross out the 0's in the assigned column
#lineNumber = drawLines(...)
#tornar a matriz quadrada
#reducao da matrix
#desenhar menor numero de linhas que cubram todos os zeros
    

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

print(hungarianMethod(c4))
