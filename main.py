from board import Board
from game import Game
import random
import math
import game as g

class Main:
    currPlayer = "user"
    ai="O"
    isLoss = False

    totalLegalMoves = 0
    totalMoves = 0


    if __name__=='__main__':    
        
        user = input("Pick X or O to determine player: ")
        
        print("You have chosen to play",user)
        board = Board()
        if user=="O":
            currPlayer= "ai"
            ai = "X"
            game = Game(board,ai,"MAX", 0,[])
        else:
            ai = "O"
            currPlayer = "user"
            game = Game(board,user,"MIN", 0,[])

        game.board.removePiece((4,4))
        game.board.removePiece((4,5))
        print("\nX removes <4, 4>")
        print("O removes <4, 5>")

        while isLoss==False:
            board.printBoard()
            #check if next move has no legal moves
            if game.player == user:
                playerMoves = game.generateMoves()
                successors = game.getSuccessors()
                loss = 0

                totalLegalMoves = totalLegalMoves + len(playerMoves)
                totalMoves = totalMoves + 1

                print("playermoves",playerMoves)
                for s in successors:
                    if len(s.legal_moves)==0:
                        loss = loss + 1
                if loss == len(successors):
                    print("User has won the game, AI has lost. ")
                    isLoss = True

                
                elif len(playerMoves)<1:
                    #player loss
                    print("User has lost the game, AI has won. ")
                    isLoss=True

                else:
                    # move = input("Type in a move, including every space to land on, formatted <4, 2>, <4, 4>: ")
                    # #format and create move list with tuples for each jump
                    # moveList = move.split(">, ")
                    # if(len(moveList)<0):
                    #     move = input("Incorrect format, try again: ")
                    # tList = []
                    # for m in moveList:
                    #     try:
                    #         t = (int(m[1:2]),int(m[4:5]))
                    #         tList.append(t)
                    #     except:
                    #         print("Please enter integers correctly formated: ")
                    # if not game.isLegal(tList, playerMoves):
                    #     print("Move selected is not legal. ")
                    # else:

                        #make move if legal move, set values
                        # game.board.makeMove(tList,playerMoves,user)
                        # game.setPrevMove(tList)
                        rand_index = random.randint(0,len(playerMoves)-1)
                        playerMove = playerMoves[rand_index]
                        game.board.makeMove(playerMove,playerMoves,user)
                        game.setPlayer(ai)
            else:
                aiMoves = game.generateMoves()
                #check if next move has no moves
                successors = game.getSuccessors()
                totalLegalMoves = totalLegalMoves + len(aiMoves)
                totalMoves = totalMoves + 1
                loss = 0
                for s in successors:
                    if len(s.legal_moves)==0:
                        loss = loss + 1
                if loss == len(successors):
                    print("User has lost the game, AI has won. ")
                    isLoss = True
                    
                #print("aimoves",aiMoves)
                elif len(aiMoves)<1:
                    #ai loss, player win
                    print("User has won the game, AI has lost. ")
                    isLoss=True
                else:
                    #random
                    # rand_index = random.randint(0,len(aiMoves)-1)
                    # aiMove = aiMoves[rand_index]
                    # game.board.makeMove(aiMove,aiMoves,ai)
                    
                    # minimax
                    cbv, aiMove = game.minimax()
                    
                    # #print(cbv, aiMove)
                    game.board.makeMove(aiMove,aiMoves,ai)

                    # #alpha-beta pruning
                    # AB, aiMove = game.minimaxAB(-math.inf,math.inf)
                    # game.board.makeMove(aiMove,aiMoves,ai)

                    game.setPrevMove(aiMove)
                    game.setPlayer(user)
        print("Average branching factor: ", totalLegalMoves/totalMoves)
        print("Total Static Evaluations: ", g.numEvals)

    