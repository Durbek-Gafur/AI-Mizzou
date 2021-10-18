# COde that makes computer play with itself
from game import *
from board import *
from heuristics import *
def playGame(p1,p2,board,playing):
  gameEnd = False
  
  nextMove = (len(board.matrix)//2-1,len(board.matrix[0])//2)
  # print(nextMove)
  while 'tie' not in nextMove and 'win' not in nextMove :
    board.matrix[nextMove[0]][nextMove[1]] = playing.symbol
    print(playing.symbol,"-s turn")
    print(board)
    if playing == p1: playing = p2
    else: playing = p1
    score,nextMove = board.minimax(playing.maximizing,playing.movesAhead)
    # print(score,nextMove)
    
class Player():
  def __init__(self,movesAhead,symbol,maximizing):
    self.movesAhead = movesAhead
    self.symbol = symbol
    self.maximizing = maximizing