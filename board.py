

class Board:
    game_board = []
    def __init__(self, prev_board = None):
        #initalize the board
        if (prev_board == None):
            self.game_board = []
            a = []
            b = []
            for i in range (0,8):
                if i%2==0:
                    #even index
                    a.append("X")
                    b.append("O")
                else:
                    a.append("O")
                    b.append("X")
            #have alternating rows, a and b
            for i in range(0,8):
                if i%2==0:
                    self.game_board.append(a.copy())
                else:
                    self.game_board.append(b.copy())
        else:
            self.game_board = prev_board.getBoard()
            
    def getBoard(self):
        boardCopy = []
        for i in range(len(self.game_board)):
            rowCopy=[]
            for j in range(len(self.game_board)):
                rowCopy.append(self.game_board[i][j])
            boardCopy.append(rowCopy)
        return boardCopy
    
    def getValue(self, pos):
        return self.game_board[pos]

    #take in a list of moves and carry it out
    def makeMove(self, move_list,legal_moves,player):
        curr_movex = move_list[0][0]
        curr_movey = move_list[0][1]
        #set current x and y values
        printstr="\n"+player+" moves <"+str(curr_movex)+", "+str(curr_movey)+"> "
        #loop to carry out each move
        for i in range(1,len(move_list)):
            curr_movex = move_list[i][0]
            curr_movey = move_list[i][1]
            self.removePiece(move_list[i-1])
            #remove pieces in between, replace last empty spot w piece
            if (move_list[i-1][0]<curr_movex):
                #prev pos and next pos have diff x coordinates
                self.removePiece((curr_movex-1, curr_movey))
            elif (move_list[i-1][0]>curr_movex):
                self.removePiece((curr_movex+1, curr_movey))
            elif(move_list[i-1][1]<curr_movey):
                #diff y coordinates
                self.removePiece((curr_movex, curr_movey-1))
            elif(move_list[i-1][1]>curr_movey):
                self.removePiece((curr_movex, curr_movey+1))
            printstr=printstr+"to <"+str(curr_movex)+", "+str(curr_movey)+"> "
        self.replacePiece(move_list[len(move_list)-1],player)

        print(printstr)

    def removePiece(self, pos):
        row = pos[0]
        col = pos[1]
        #substring to get coordinates
        self.game_board[row-1][col-1] = "."

    def replacePiece(self,pos,player):
        #replace a piece when it jumps
        row = pos[0]
        col = pos[1]
        self.game_board[row-1][col-1] = player

    def printBoard(self):
        index_list = [x for x in range(1,9)]
        print("\n   ", *index_list, "\n")
        for i in range(0,8):
            print(index_list[i], " ", " ".join(self.game_board[i]))
        print("")
