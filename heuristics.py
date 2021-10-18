from game import *
from board import *
from heuristics import *
# heuristic
def heuristicBig(matrix,player):
  player = player if player == 'x' else 'o'
  opponent = 'o' if player == 'x' else 'x'
  sc = {'x':1,'o':-1}
  threeSidePlayer = heuristicNinArow(matrix,3,player) 
  threeSideOpponent = heuristicNinArow(matrix,3,opponent)
  h1side3inRowPlayer = threeSidePlayer[0]
  h2side3inRowPlayer = threeSidePlayer[1]
  h1side3inRowOpponent = threeSideOpponent[0]
  h2side3inRowOpponent = threeSideOpponent[1]


  twoSidePlayer = heuristicNinArow(matrix,2,player)
  twoSideOpponent = heuristicNinArow(matrix,2,opponent)
  h1side2inRowPlayer = twoSidePlayer[0]
  h2side2inRowPlayer = twoSidePlayer[1]
  h1side2inRowOpponent = twoSideOpponent[0]
  h2side2inRowOpponent = twoSideOpponent[1]
  ans = 100*h2side3inRowPlayer - 10*h2side3inRowOpponent +100*h1side3inRowPlayer - 5*h1side3inRowOpponent +2*h2side2inRowPlayer-2*h2side2inRowOpponent+ h1side2inRowPlayer- h1side2inRowOpponent
  return ans*sc[player]

def heuristicNinArow(matrix,n,player): # (oneSidesCount, twoSidesCount)
  # we get all possible N-rows array   |||  
  dioganals = checkDioganalsForNonly(n,matrix,player)
  rows = checkRowsForNonly(n,matrix,player) # returns array  DONE DONE 
  columns = checkColsForNonly(n,matrix,player)


  oneTwoSideDioganals  = checkSideDioganals(n,dioganals,matrix) # => [NumberOfOneSide, NumberOfTwoSide]
  oneTwoSideRows  = checkSideRows(n,rows,matrix) # returns tuple  check if start-1 == -  or 
  oneTwoSideColumns  = checkSideColumns(n,columns,matrix)

  return (oneTwoSideDioganals[0]+oneTwoSideRows[0]+oneTwoSideColumns[0],oneTwoSideDioganals[1]+oneTwoSideRows[1]+oneTwoSideColumns[1])


def checkSideRows(n,rows,matrix):
  oneTwoSide = [0,0]
  for unit in rows:
    s = unit
    e = (unit[0],unit[1]+n-1)
    sideCount = 0
    # check for left side
    if s[1]-1>=0 and matrix[s[0]][s[1]-1]=='-':
      sideCount+=1
    # check for right side
    if e[1]+1<len(matrix[0]) and matrix[e[0]][e[1]+1]=='-':
      sideCount+=1

    if sideCount>0: oneTwoSide[sideCount-1]+=1

  return oneTwoSide
def checkLeft(row,col):
  if col-1<0:
    return True
  if row[col-1]!=row[col]:
    return True
  return False
def checkRight(row,col):
  if col>=len(row) :
    return True
  if row[col-1]!=row[col]:
    return True
  return False
def checkRowsForNonly(n,matrix,player):
    ans = []
    nrows = [player]*n
    for row in range(len(matrix)):
      for col in range(len(matrix[0])-n+1): 
        if nrows == matrix[row][col:col+n] and checkLeft(matrix[row],col) and checkRight(matrix[row],col+n):
          # print(row,col,matrix[row][col:col+n])
          ans.append((row,col))

    return ans

def checkSideDioganals(n,dioganals,matrix):
  # \\
  oneTwoSide = [0,0]
  for unit in dioganals:
    s = unit["start"]
    e = unit["end"]
    sideCount = 0
    # \\
    if s[1]<e[1]:
      # if not out of matrix
      if s[0]-1>=0 and s[1]-1>=0 and matrix[s[0]-1][s[1]-1]=='-':
        sideCount+=1
      # check for end side
      if e[0]+1<len(matrix) and e[1]+1<len(matrix[0]) and matrix[e[0]+1][e[1]+1]=='-':
        sideCount+=1
    # //
    else:
      # if not out of matrix
      if s[0]-1>=0 and s[1]+1<len(matrix[0]) and matrix[s[0]-1][s[1]+1]=='-':
        sideCount+=1
      # check for end side
      if e[0]+1<len(matrix) and e[1]-1>=0 and matrix[e[0]+1][e[1]-1]=='-':
        sideCount+=1
    if sideCount>0: oneTwoSide[sideCount-1]+=1
  return oneTwoSide
def topLeft(matrix, i, j):
  # if 0 <= index < len(list)
  if 0 > i or 0 > j or matrix[i][j]!=matrix[i+1][j+1]:
    return True
  return False
def topRight(matrix, i, j):
  # extreme i , j passed they are corners
  # if 0 <= index < len(list)
  if 0 > i or len(matrix[0]) <= j or matrix[i][j]!=matrix[i+1][j-1]:
    return True
  return False
def bottomRight(matrix, i, j):
  # extreme i , j passed they are corners
  if i >= len(matrix) or j >= len(matrix[i-1]) or matrix[i][j]!=matrix[i-1][j-1]:
    return True
  return False
def bottomLeft(matrix, i, j):
  # extreme i , j passed they are corners
  if i >= len(matrix) or 0 > j or matrix[i][j]!=matrix[i-1][j+1]:
    return True
  return False
def checkDioganalsForNonly(n,matrix,player):
  nrow = [player]*n
  ans = []
  
  for rowStart in range(len(matrix)-n+1):
    for colStart in range(len(matrix[0])-n+1):
      # \\\
      if matrix[rowStart][colStart] == player: 
        tmpArray = []
        for i in range(n):
          tmpArray.append(matrix[rowStart+i][colStart+i])
        if tmpArray==nrow and topLeft(matrix,rowStart-1,colStart-1) and bottomRight(matrix,rowStart+n,colStart+n):
          ans.append({"start":(rowStart,colStart),"end":(rowStart+n-1,colStart+n-1)})
      # ///
      if matrix[rowStart][len(matrix[0])-1-colStart] == player:      
        tmpArray = []
        for i in range(n):
          tmpArray.append(matrix[rowStart+i][len(matrix[0])-1-(colStart+i)])
        if tmpArray==nrow and topRight(matrix,rowStart-1,len(matrix[0])-1-colStart+1) and bottomLeft(matrix,rowStart+n,len(matrix[0])-1-colStart-n): #
          ans.append({"start":(rowStart,len(matrix[0])-1-(colStart)),"end":(rowStart+n-1,len(matrix[0])-1-colStart-n+1)})
  return ans

def checkSideColumns(n,cols,matrix):
  oneTwoSide = [0,0]
  for unit in cols:
    s = unit
    e = (unit[0]+n-1,unit[1])
    sideCount = 0
    # if not out of matrix
    if s[0]-1>=0 and matrix[s[0]-1][s[1]]=='-':
      sideCount+=1
    # check for end side
    if e[0]+1<len(matrix) and matrix[e[0]+1][e[1]]=='-':
      sideCount+=1

    if sideCount>0: oneTwoSide[sideCount-1]+=1
  return oneTwoSide
def checkUp(col,row):
  if row-1<0:
    return True
  if col[row-1]!=col[row]:
    return True
  return False
def checkDown(col,row):
  if row>=len(col) :
    return True
  if col[row-1]!=col[row]:
    return True
  return False
def checkColsForNonly(n,matrix,player):
    ans = []
    ncols = [player]*n
    for col in range(len(matrix[0])):
      col_arr = []
      for row in range(len(matrix)):
        col_arr.append(matrix[row][col])
      for rows2 in range(len(col_arr)):
        if ncols == col_arr[rows2:rows2+n] and checkUp(col_arr, rows2) and checkDown(col_arr, rows2+n):
          ans.append((rows2,col))

    return ans
