import numpy as np

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
        zeroesInRow = list(np.where(matrix[i,:] == 0)[0])
        if len(zeroesInRow) >= 1:
            assignedMatrix[i][zeroesInRow[0]] = True
            zeroesInCol = list(np.where(matrix[:,zeroesInRow[0]] == 0)[0])
            for zeroes in zeroesInCol:
                matrix[zeroes,zeroesInRow[0]] = -1 
            matrix[i,zeroesInRow[0]] = 0
            for zeroes in zeroesInRow[1:]:
                matrix[i,zeroes] = -1
    
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
        for i in range(matrixShape[0]):
            for j in range(matrixShape[1]):
                squareMatrix[i][j] = matrix[i][j]
    else:
        squareMatrix = matrix

    return squareMatrix

#OK
def matrixReduction(matrix):
    for i in range(len(matrix)): 
        matrix[i, :]-=np.min(matrix[i, :])
    for i in range(len(matrix)): 
        matrix[:, i]-= np.min(matrix[:,i])        
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

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if rowsUnmarked[i] == 1 and colsMarked[j] == 1:
                #print("Line "+str(i)+"Col "+str(j)+" Intersection")
                fixedMatrix[i][j] += minVal
            elif not (rowsUnmarked[i] == 1 or colsMarked[j] == 1):
                #print("Line "+str(i)+"Col "+str(j)+" Free")
                fixedMatrix[i][j] -= minVal
                #print("Line "+str(i)+"Col "+str(j)+" Not important")
    #print("fixedMatrix\n")
    #print(fixedMatrix)
    #print("\n\n\n")
    return fixedMatrix



def alterMatrixValues(crossedMatrix,rowsUnmarked,colsMarked):
    crossedMatrix[crossedMatrix == -1] = 0
    minVal = getMinVal(crossedMatrix,rowsUnmarked,colsMarked)
    #print("minVal: "+str(minVal))
    return fixMatrix(crossedMatrix,rowsUnmarked,colsMarked,minVal)


def getJobs(matrix):
    matrix[matrix == -1] = 0
    worked = {}
    #print("matrix")
    #print(matrix)
    for workerId in range(len(matrix)):
        #print("matrix in worker"+str(workerId))
        #print(matrix)
        #print("Entering search for worker"+str(workerId))
        qtts = [[] if j in worked else list(np.where(matrix[j,:] == 0)[0]) for j in range(len(matrix))]
        #print("qtts")
        #print(qtts)
        #print("\n\n\n\n")
        zeros = [[j,qtts[j][0]] for j in range(len(qtts)) if len(qtts[j]) == 1]
        for zero in zeros:
            worked[zero[0]] = zero[1]
            matrix[:,zero[1]][matrix[:,zero[1]] == 0] = -1
            matrix[matrix[:,zero[1]] == 0] = -1
            #print("Job "+str(zero)+" done")
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
    return np.sum(oldMatrix[tuple(jobs)])
    
#assign a row if it has only one 0, else skip the row temporarily
#cross out the 0's in the assigned column
#assign a row if it has only one 0, else skip the row temporarily
#cross out the 0's in the assigned column
#lineNumber = drawLines(...)
#tornar a matriz quadrada
#reducao da matrix
#desenhar menor numero de linhas que cubram todos os zeros
    


c = np.array([[20, 28, 19, 13],
              [15, 30, 31, 28],
              [40, 21, 20, 17],
              [21, 28, 26, 12]])

so = np.array([
    [0,1,0,1,1],
    [1,1,0,1,1],
    [1,0,0,0,1],
    [1,1,0,1,1],
    [1,0,0,1,0]
])

ok = np.array([
    [35,0,0,0],
    [0,30,0,5],
    [55,5,0,10],
    [0,45,30,45]
])

ok2 = np.array([
    [2,9,2,7,1],
    [6,8,7,6,1],
    [4,6,5,3,1],
    [4,2,7,3,1],
    [5,3,9,5,1]
])

print(hungarianMethod(c))