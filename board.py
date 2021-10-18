# PART 1 ONE MINIMAX
# Board and Minimax
from game import *
from board import *
from heuristics import *
# import time
class Board:

  def __str__(self):
    ans = ""
    for i in self.matrix: ans+=str(i)+"\n"
    return ans
  
  def __init__(self,row=6,col=5,winSize=4,matrix=[]):
    self.winSize = winSize
    self.row = row
    self.col = col
    self.matrix = [ [ '-' for i in range(col) ] for j in range(row) ] if matrix==[] else matrix# col*j+i
    # for i in self.matrix: print(i)
  
  def makeMove(self,i,j,xOrO):
    self.matrix[i][j] = xOrO
  
  def removMove(self,i,j):
    self.matrix[i][j] = '-'

    
# Checks if there are moves remaining on the board. 
  def anyMovesLeft(self) :
    for rows in self.matrix :
      for cell in rows :
        if (cell == '-') :
          return True
    return False

# Checks if the someone won
  def terminalFunction(self,verbose=False):

    dioganals = self.checkDioganals()
    if dioganals!=0: return dioganals

    rows = self.checkRows()
    if rows!=0: return rows
    
    columns = self.checkCols()
    if columns!=0: return columns


  
  def checkDioganalsSubfunctionAllSame(self,rowStart,colStart): # pass function as an argument to unite checkDioganalsSubfunctionAllSame and right to left
    current = self.matrix[rowStart][colStart]
    allSame = True
    # checks if all values in diagonals are the same
    for i in range(1,self.winSize):
      if current != self.matrix[rowStart+i][colStart+i]:
        allSame = False
        break
      current = self.matrix[rowStart+i][colStart+i]
    return allSame

  def checkDioganalsSubfunctionAllSameRightToLeft(self,rowStart,colEnd):
    current = self.matrix[rowStart][colEnd]
    allSame = True
    # checks if all values in diagonals are the same
    for i in range(1,self.winSize):
      if current != self.matrix[rowStart+i][colEnd-i]:
        allSame = False
        break
      current = self.matrix[rowStart+i][colEnd-i]

    
    return allSame

  def checkDioganals(self):
    
    
    for rowStart in range(len(self.matrix)-self.winSize+1):
      # print(rowStart)
      for colStart in range(len(self.matrix[0])-self.winSize+1):
        # \\\
        if self.matrix[rowStart][colStart] != '-': 
          if self.checkDioganalsSubfunctionAllSame(rowStart,colStart): return 1 if self.matrix[rowStart][colStart] == 'x' else -1
        # ///
        colEnd = len(self.matrix[0])-colStart-1
        if self.matrix[rowStart][colEnd] != '-': 
          if self.checkDioganalsSubfunctionAllSameRightToLeft(rowStart,colEnd): return 1 if self.matrix[rowStart][colEnd] == 'x' else -1      
    return 0

  def checkRows(self):
      col_elements = []
      for row in range(len(self.matrix)):
          for col in range(len(self.matrix[0]) - self.winSize + 1):
              col_elements.extend(self.matrix[row][col:col+self.winSize])
              if col_elements[0] == 'x' and col_elements.count(col_elements[0]) == self.winSize: return 1
              if col_elements[0] == 'o' and col_elements.count(col_elements[0]) == self.winSize: return -1
              col_elements = []
      return 0

  def checkCols(self):
      
      row_elements = []
      for col in range(len(self.matrix[0])):
          for row in range(len(self.matrix) - self.winSize + 1):
              for num in range(self.winSize):
                  row_elements.append(self.matrix[row + num][col])
              if row_elements[0] == 'x' and row_elements.count(row_elements[0]) == self.winSize: return 1
              if row_elements[0] == 'o' and row_elements.count(row_elements[0]) == self.winSize: return -1
              row_elements = []
      return 0
  def utilityFunction(val):
    if val==0: return 0
    return 1 if val>0 else -1
  
  def minimax(self, maximizing,depth,verbose=False) :
    terminalScore = self.terminalFunction(verbose)

    # If someone has won print their score
    if (terminalScore ==1 or terminalScore==-1) :
      winner = 'x' if terminalScore==1 else 'o'
      terminalScore = float("inf") if terminalScore>0 else -float("inf")
      return (terminalScore,str(winner)+" wins")  #float('inf')

    # Check if there are moves left
    if (self.anyMovesLeft() == False) :
      return (0,"tie")

    best = -float("inf") if maximizing else float("inf")
    bestMove = (-1,-1)
    bestMoveSum = 0

    if depth !=0:
      # Create all children nodes
      # tmpChildNode =  Board(6,5,4,self.matrix)
      tmpChildNode =  [[cell for cell in row] for row in self.matrix]
      # print("aa",tmpChildNode )
      for i in range(self.row) :		
        for j in range(self.col) :
          # Check if cell is empty
          if (self.matrix[i][j]=='-') :
            # Make the move
            if maximizing:
              self.matrix[i][j] = 'x'  
            else:
              self.matrix[i][j] = 'o'

            # actually creating children
            if maximizing: 
              currentScore,currentBestReturned = self.minimax(not maximizing,depth-1) #max(self.minimax(not maximizing,depth-1)[0],best) #
              # print("current move for maximizer: ", currentScore,best,currentScore>best)
              if currentScore>best:
                best = currentScore
                bestMove = (i,j) #if 'heur' in currentBestReturned else currentBestReturned
                bestMoveSum+=currentScore
            else: 
              currentScore,currentBestReturned = self.minimax(not maximizing,depth-1) #min(self.minimax(not maximizing,depth-1)[0],best) #
              
              if currentScore<best:
                best = currentScore
                bestMoveSum+=currentScore
                bestMove = (i,j) #if 'heur' in currentBestReturned or 'win' in currentBestReturned or 'tie' in currentBestReturned else currentBestReturned
                      
            tmpChildNode[i][j] = currentScore
            self.matrix[i][j] = '-'
      tmpChildNodeTmpSum = 0
      ans = "\nFor : "+('x' if maximizing else 'o')
      for i in tmpChildNode: 
        ans+="\t\t"
        for j in i: 
          if type(j) == int:
            tmpChildNodeTmpSum+=j
          ans+=str(j)+"\t"
        ans+="\n"

      tmpChildNodeTmpSum = tmpChildNodeTmpSum if tmpChildNodeTmpSum!=0 else float("inf")
      return (tmpChildNodeTmpSum,bestMove)
    else:
      #call heuristic
      players = ['o','x']
      return (heuristicBig(self.matrix, players[maximizing]),"heur")      
  