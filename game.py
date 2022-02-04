from board import Board
import random
import math
import copy
numEvals = 0

class Game:
    
    def __init__(self, board, player, minmax, depth, prevMove):
        self.board = board
        self.player = player
        self.minmax = minmax
        self.depth = depth
        self.prevMove = prevMove
        self.legal_moves = Game.generateMoves(self)

    def copyState(self):
        state = Game(self)

    def setPlayer(self, player):
        self.player = player
    
    def setMinmax(self, minmax):
        self.minmax = minmax
    
    def setPrevMove(self, prevMove):
        self.prevMove = prevMove

    def generateMoves(self):
        legal_moves = []
        for i in range(0,8):
            for j in range(0,8):
                board = self.board.game_board
                if (board[i][j]==self.player):
                    #check surroundings for open spots
                    legal_moves = self.generateDirection(legal_moves, "north", i, j)
                    legal_moves = self.generateDirection(legal_moves, "south", i, j)
                    legal_moves = self.generateDirection(legal_moves, "east", i, j)
                    legal_moves = self.generateDirection(legal_moves, "west", i, j)

        self.legal_moves = legal_moves   
        return legal_moves

    def generateDirection(self,legal_moves, dir, i, j):
        board = self.board.game_board
        x = 0; y = 0; coord = 0; midx = 0; midy = 0
        ii = i+1
        jj = j+1
        
        if (dir=="south" or dir=="west"):
            if (dir=="south"):
                y = -2
                coord = j
            if (dir=="west"):
                x = -2
                coord = i
            midx = int(x/2); midy = int(y/2)
            #check negative jumps in either direction and check if there is food in the middle
            if (coord>=2) and (board[i+x][j+y]==".") and (board[i+midx][j+midy]!="."):
                legal_moves.append([(ii,jj),(ii+x,jj+y)])
                #check for double jump
                if (coord>=4) and (board[i+2*x][j+2*y]==".") and (board[i+3*midx][j+3*midy]!="."):
                    legal_moves.append([(ii,jj),(ii+x,jj+y), (ii+2*x,jj+2*y)])
                    #triple jump
                    if (coord>=6) and (board[i+3*x][j+3*y]==".") and (board[i+5*midx][j+5*midy]!="."):
                        legal_moves.append([(ii,jj),(ii+x,jj+y), (ii+2*x,jj+2*y), (ii+3*x,jj+3*y)])

        if (dir=="north" or dir=="east"):
            if (dir=="north"):
                y = 2
                coord = j
            if (dir=="east"):
                x = 2
                coord = i
            midx = int(x/2); midy = int(y/2)
            #check positive jumps in either direction and check if there is food in the middle
            if (coord<=5) and (board[i+x][j+y]==".") and (board[i+midx][j+midy]!="."):
                legal_moves.append([(ii,jj),(ii+x,jj+y)])
                #check for double jump
                if (coord<=3) and (board[i+2*x][j+2*y]==".") and (board[i+3*midx][j+3*midy]!="."):
                    legal_moves.append([(ii,jj),(ii+x,jj+y), (ii+2*x,jj+2*y)])
                    #triple jump
                    if (coord<=1) and (board[i+3*x][j+3*y]==".") and (board[i+5*midx][j+5*midy]!="."):
                        legal_moves.append([(ii,jj),(ii+x,jj+y), (ii+2*x,jj+2*y), (ii+3*x,jj+3*y)])
            
        return legal_moves

    def isLegal(self,move_list,legal_moves):
        if move_list in legal_moves:
            return True
        return False
    
    def isLoss(self,legal_moves):
        if len(legal_moves)<1:
           return True
        return False

    def getSuccessors(self):
        #get next player and minmax values
        opp = "X"; currMinmax = "MIN"
        if (self.player == "X"):
            opp = "O"
        if (self.minmax == "MIN"):
            currMinmax = "MAX"
        successors = []
        moves = self.legal_moves
        for m in moves:
            #for each move, copy board and create game object to add to successor list
            currBoard = copy.copy(self.board)
            currState = Game(currBoard,opp,currMinmax,self.depth+1, m)
            successors.append(currState)
        return successors

    def minimax(self):
        if (self.depth == 6 or len(self.legal_moves)<1):
            return Game.staticFunction(self), None
        successors = Game.getSuccessors(self)
        move = 0; cbv = math.inf; bestMove = 0; bv = 0
        #if layer is max
        if self.minmax=="MAX":
            cbv = -math.inf; bestMove=0
            for s in successors:
                #go through successors and get best moves
                bv, move = Game.minimax(s)
                if bv > cbv:
                    cbv = bv
                    bestMove = s.prevMove
            return cbv, bestMove
        #if layer is min
        elif self.minmax=="MIN":
            cbv = math.inf; bestMove=0
            for s in successors:
                #go through successors and get best moves
                bv, move = Game.minimax(s)
                if bv < cbv:
                    cbv = bv
                    bestMove = s.prevMove
            return cbv, bestMove
    
    def minimaxAB(self, A, B):
        if (self.depth == 6 or len(self.legal_moves)<1):
            return Game.staticFunction(self), None
        successors = Game.getSuccessors(self)
        #if layer is max
        if self.minmax=="MAX":
            bestMove=0
            for s in successors:
                bv, move = Game.minimaxAB(s, A, B)
                if bv > A:
                    #replace alpha and best move
                    A = bv
                    bestMove = s.prevMove
                if A >= B:
                    return B, bestMove
            return A, bestMove
        #if layer is min
        elif self.minmax=="MIN":
            bestMove=0
            for s in successors:
                bv, move = Game.minimaxAB(s, A, B)
                if bv < B:
                    #replace beta and best move
                    B = bv
                    bestMove = s.prevMove
                if B <= A:
                    return A, bestMove
            return B, bestMove

    def staticFunction(self):
        #move where there are not as many moves as there
        global numEvals
        numEvals += 1
        
        score = len(self.legal_moves)*3
        #set score as length of legal moves

        move = self.prevMove
        countx = 0; county = 0;
        for (x,y) in move:
            countx = countx + x
            county = county + y
        avgpos = (countx / len(move), county / len(move))
        #calculate average positions for the move

        if len(self.legal_moves) > 6:
            #if many moves (near start of game), do less double jumps
            score = score-len(move)
        else:
            score = score+len(move)
        
        #check surrounding spots if they are empty
        x = int(avgpos[0])
        y = int(avgpos[1])
        lowerx = x-3 if x-2>=0 else 0
        higherx = x+3 if x+3<8 else 7
        lowery = y-3 if y-3>=0 else 0
        highery = y+3 if y+3<8 else 7
        for i in range (lowerx, higherx):
            for j in range (lowery, highery):
                if self.board.game_board[i][j]==".":
                    score = score + 1
                    # higher score if more empty area
        return score
