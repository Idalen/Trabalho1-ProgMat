import numpy as np
import networkx as nx

def drawLines(matrix,assignedMatrix):
    rowsMarked = [1 if np.sum(row)==0 else 0 for row in assignedMatrix] #Tick rows with unassigned zeroes
    colsMarked = [0]*len(rowsMarked) #Tick an unassigned column
    
    while True: #While ticking happens
        ticks = 0
        #Check for rows that are marked, find the zeroes and mark the columns
        for i in range(len(matrix)):
            if rowsMarked[i] <= 0:
                continue

            toTickCols = list(np.where(matrix[i,:] <= 0)[0]) #If a ticked row has a 0, then tick the corresponding column

            for j in toTickCols:
                if colsMarked[j] == 0:
                    ticks += 1
                    colsMarked[j] = 1
            rowsMarked[i] = -1

        #Check for cols that are marked, find the assigned values and mark the rows with assigned values
        for j in range(len(matrix)): 
            if colsMarked[j] <= 0:
                continue

            toTickRows = list(np.where(matrix[:,j] == 0)[0])

            for i in toTickRows:
                if rowsMarked[i] == 0:
                    ticks += 1
                    rowsMarked[i] = 1
            colsMarked[j] = -1

        if ticks == 0:
           break

    colsMarked = [0 if i == 0 else 1 for i in colsMarked]
    
    rowsUnmarked = [1 if i == 0 else 0 for i in rowsMarked]

    return rowsUnmarked, colsMarked

def assignMatrix(matrix):
    assignedMatrix = np.zeros((len(matrix),len(matrix)), dtype=int) #Create a matrix with zeroes

    for i in range(len(matrix)):
        zeroesInRow = np.where(matrix[i,:] == 0)[0] #Get the zeroes in the row
        if len(zeroesInRow) >= 1: #If there is at least one zero in the row
            #The first zero is set to 0 and assigned, the others in the same col and others in the same row are set to -1
            assignedMatrix[i][zeroesInRow[0]] = True
            
            matrix[:,zeroesInRow[0]][matrix[:,zeroesInRow[0]] == 0] = -1
            matrix[i,:][matrix[i,:] == 0] = -1
            matrix[i,zeroesInRow[0]] = 0
    
    return assignedMatrix, matrix
    
        
def squarenizeMatrix(matrix):
    matrixShape = np.shape(matrix)
    #If the matrix is not squared, then make it squared filling with zeroes
    if matrixShape[0] != matrixShape[1]:
        maxShape = max(matrixShape)
        squareMatrix = np.zeros((maxShape,maxShape))
        squareMatrix[:matrixShape[0],:matrixShape[1]] = matrix
        return squareMatrix
    else:
        return matrix


def matrixReduction(matrix):
    matrix -= np.min(matrix,axis=1)[:,None] #By each line
    matrix -= np.min(matrix,axis=0) #By each column
    return matrix



def getMinVal(crossedMatrix,rowsUnmarked,colsMarked):
    minVal = float("inf")
    #Get the min value of uncrossed nodes
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
    rowsTuple = tuple([i for i in range(lenM) if rowsUnmarked[i] == 1]) #Get the rows that are marked
    colsTuple = tuple([i for i in range(lenM) if colsMarked[i] == 1]) #Get the columns that are marked
    fixedMatrix -= minVal #Subtract the min value from the matrix
    fixedMatrix[rowsTuple,:] += minVal #Add the min value to the values in the rows marked
    fixedMatrix[:,colsTuple] += minVal #Add the min value to the values in the columns marked

    return fixedMatrix



def alterMatrixValues(crossedMatrix,rowsUnmarked,colsMarked):
    crossedMatrix[crossedMatrix == -1] = 0 #Set the -1s to 0s
    minVal = getMinVal(crossedMatrix,rowsUnmarked,colsMarked) #Get the minimum value
    return fixMatrix(crossedMatrix,rowsUnmarked,colsMarked,minVal) #Fix matrix

def getJobs(matrix):
    matrix[matrix == -1] = 0
    G = nx.Graph() #Create a graph
    for i in range(len(matrix)): #Add the nodes in biparted way
        G.add_node((i,"worker"),bipartite=0)
        G.add_node((i,"job"),bipartite=1)
    
    zeroes = np.where(matrix == 0) #Get the zeroes
    edges = [[(zeroes[0][i],"worker"),(zeroes[1][i],"job")] for i in range(len(zeroes[0]))] #Create the edges in biparted way from the zeroes
    G.add_edges_from(edges) #Add the edges to the graph
    matching = list(nx.max_weight_matching(G,maxcardinality=True)) #Get the matching
    jobs = np.array([[match[0][0],match[1][0]] if match[0][1] == "worker" else (match[1][0],match[0][0]) for match in matching]) #Get the jobs
    return [tuple(jobs[:,0]),tuple(jobs[:,1])]

def hungarianMethod(matrix):
    oldMatrix = np.copy(matrix) #Copy the matrix
    squareMatrix = squarenizeMatrix(matrix) #Squarenize the matrix
    squareMatrix = matrixReduction(squareMatrix) #Reduce the matrix

    linesQtty = 0
    iter = 1
    while True:
        assignedMatrix, crossedMatrix = assignMatrix(squareMatrix) #Assign the matrix
        rowsUnmarked, colsMarked = drawLines(crossedMatrix,assignedMatrix) #Draw lines
        if (np.sum(rowsUnmarked) + np.sum(colsMarked)) >= len(crossedMatrix): #If the matrix has lines passed through equal to the matrix size, break
            break
        squareMatrix = alterMatrixValues(crossedMatrix,rowsUnmarked,colsMarked) #Alter the matrix to continue loop
        iter += 1
    jobs = getJobs(crossedMatrix) #Get the jobs
    print("Jobs: "+str(jobs))   
    return np.sum(oldMatrix[tuple(jobs)]) #Return the cost of the jobs
        

# Toy problems
# n = 4
c1 = np.array([[20, 28, 19, 13],
               [15, 30, 31, 28],
               [40, 21, 20, 17],
               [21, 28, 26, 12]])

c2 = np.array([[35,  0,  0,  0],
               [ 0, 30,  0,  5],
               [55,  5,  0, 10],
               [ 0, 45, 30, 45]])

# n = 5
c3 = np.array([[0, 1, 0, 1, 1],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 0, 1],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 1, 0]])

c4 = np.array([[2, 9, 2, 7, 1],
               [6, 8, 7, 6, 1],
               [4, 6, 5, 3, 1],
               [4, 2, 7, 3, 1],
               [5, 3, 9, 5, 1]])

print(hungarianMethod(c4))
