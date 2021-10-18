# COMP - COMP 2PLY - 2PLY
from game import *
from board import *
from heuristics import *


p1 = Player(2,"x",True)
p2 = Player(4,"o",False)

b1 = Board(6,5,4)
playGame(p1,p2,b1,p1)
