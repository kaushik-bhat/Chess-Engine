class GameState():
    def __init__(self):
        #The board is a 8x8  , each element has 2 characters
        # First character represents the color of the piece and the second character represents the piece itself
        #"--" empty square on the chess board with no piece
        self.board = [
            ["bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR"],
            ["bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["--" , "--" , "--" , "--" , "--" , "--" , "--" , "--"],
            ["wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp" , "wp"],
            ["wR" , "wN" , "wB" , "wQ" , "wK" , "wB" , "wN" , "wR"]
        ]
        
        self.validMoveFunction = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                                  'B':self.getBishopMoves,'K':self.getKingMoves,'Q':self.getQueenMoves}
        
        self.whiteToMove = True
        self.moveLog = []
        self.white_King_Location = (7,4)
        self.black_King_Location = (0,4)
        self.checkmate = False
        self.stalemate = False
        
    '''
    Takes a move as a paramter and executes it(this doesnt take into account castling and en-passant)
    '''    
    def makeMove(self,move):
        self.board[move.start_Row][move.start_Col] = "--"   #starting square becomes empty
        self.board[move.end_Row][move.end_Col] = move.piece_Moved   #ending square is replaced by the piece moved
        self.moveLog.append(move)   #log the moves so that we can undo later   
        self.whiteToMove = not self.whiteToMove #change the players turn
        #updating the kings location if moved
        if move.piece_Moved == "wK":
            self.white_King_Location = (move.end_Row,move.end_Col)
        if move.piece_Moved == "bK":
            self.black_King_Location= (move.end_Row,move.end_Col)
    
    
    
    #to undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0 :  #making sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.whiteToMove = not self.whiteToMove
            #incase king move undo, then location must be updated
            if move.piece_Moved == "wK":
                self.white_King_Location = (move.start_Row,move.start_Col)
            if move.piece_Moved == "bK":
                self.black_King_Location= (move.start_Row,move.start_Col)
            
    #All moves considering checks
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1 , -1 , -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            #switch turn because, say its white's turn to move
            #you generated all possible black moves and called makeMove function which switched the turn
            #you ll be checking for opponent's king check condition and not the required players
            if self.inCheck():
                moves.remove(moves[i])  #if it attacks your king it is not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()   
        
        if len(moves) == 0: #means checkamte or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False  #handling cases of undo
            self.stalemate = False 
                
        return moves
    
    #Determine if current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.white_King_Location[0],self.white_King_Location[1])
        else:
            return self.squareUnderAttack(self.black_King_Location[0],self.black_King_Location[1])
    
    #Determine if the enemy can attack the square r,c
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        opponent_Moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch the turn back to original player
        for move in opponent_Moves:
            if move.end_Row == r and move.end_Col == c: #square is under attack
                return True
        return False
        
        
    
    #All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):    #number of rows is no of lists in 2D list
            for c in range(len(self.board[r])): #number of columns is no of items in each list
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.validMoveFunction[piece](r,c,moves)    #INSTEAD OF MULTIPLE IF ELSE FOR EACH PIECE
        
        return moves
    
    #Get all possible moves for the pawn at r,c and add to list moves
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:    #WHITE pawn moves
            if self.board[r-1][c] == "--":  #1 square pawn move
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c] == "--": #2 square pawn move
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0: #capturing pieces to left
                if self.board[r-1][c-1][0] == 'b':  #black enenmy piece to capture cause no point in white takes white
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7: #capturing pieces to right
                if self.board[r-1][c+1][0] == 'b': 
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                    
        else:   #BLACK pawn moves
            if self.board[r+1][c] == "--":  #1 square pawn move
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c] == "--": #2 square pawn move
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0: #capturing pieces to right
                if self.board[r+1][c-1][0] == 'w':  #white enemy piece to capture cause no point in black takes black
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7: #capturing pieces to left
                if self.board[r+1][c+1][0] == 'w': 
                    moves.append(Move((r,c),(r+1,c+1),self.board))
    #Pawn promotions need to be added and taken care later                
    
    
    #Get all possible moves for the Rook at r,c and add to list moves
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))    # up , left, down , right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i
                if 0<=final_row<8 and 0<=final_col<8:   #checking for valid square on board
                    end_Piece = self.board[final_row][final_col]
                    if end_Piece == "--":   #empty square is valid
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                    elif end_Piece[0] == enemyColor: #capture this piece valid and break to not go any further from there
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                        break
                    else:   #friendly piece encountered so break
                        break
                else:   #final row and column are illegal then break
                    break
    
    #Get all possible moves for the Knight at r,c and add to list moves
    def getKnightMoves(self,r,c,moves):
        directions = ((-2,-1),(-2,1),(2,-1),(2,1),(1,2),(1,-2),(-1,2),(-1,-2))
        ally_Color = "w" if self.whiteToMove else "b"
        for d in directions:
            final_row = r + d[0]
            final_col = c + d[1]
            if 0<=final_row<8 and 0<=final_col<8:
                end_Piece = self.board[final_row][final_col]
                if end_Piece[0] != ally_Color:  #basically if opponent piece or empty square
                    moves.append(Move((r,c),(final_row,final_col),self.board))
    
    #Get all possible moves for the Bishop at r,c and add to list moves
    #Same logic like te rook moves but the moves are diagonal
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(1,1),(1,-1),(-1,1))    # topleft , topright , bottomleft, bottomright
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i
                if 0<=final_row<8 and 0<=final_col<8:   #checking for valid square on board
                    end_Piece = self.board[final_row][final_col]
                    if end_Piece == "--":   #empty square is valid
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                    elif end_Piece[0] == enemyColor: #capture this piece valid and break to not go any further from there
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                        break
                    else:   #friendly piece encountered so break
                        break
                else:   #final row and column are illegal then break
                    break
    
    #Get all possible moves for the Queen at r,c and add to list moves
    #Queen moves is nothing but a combination of both rook moves and bishop moves:)
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    
    #Get all possible moves for the King at r,c and add to list moves
    def getKingMoves(self,r,c,moves):
        directions = ((1,-1),(1,1),(1,0),(0,-1),(0,1),(-1,1),(-1,-1),(-1,0))
        ally_Color = "w" if self.whiteToMove else "b"
        for i in range(8):
            final_row = r + directions[i][0]
            final_col = c + directions[i][1]
            if 0<=final_row<8 and 0<=final_col<8:
                end_Piece = self.board[final_row][final_col]
                if end_Piece[0] != ally_Color:
                    moves.append(Move((r,c),(final_row,final_col),self.board))
                 
        
class Move():
    
    ranks_To_Rows = {"1" : 7 , "2" : 6 , "3" : 5 , "4" : 4 , "5" : 3 , "6" : 2 , "7" : 1 , "8" : 0}
    rows_To_Ranks = {v : k for k,v in ranks_To_Rows.items()} #reverse of above dictionary basically
    files_To_Cols = {"a" : 0 , "b" : 1 , "c" : 2 , "d" : 3 , "e" : 4 , "f" : 5 , "g" : 6 , "h" : 7}
    cols_To_Files = {v : k for k,v in files_To_Cols.items()} #reverse of above dictionary basically
    
    def __init__(self,start_square,end_square,board):
        self.start_Row = start_square[0]
        self.start_Col = start_square[1]
        self.end_Row = end_square[0]
        self.end_Col = end_square[1]
        self.piece_Moved = board[self.start_Row][self.start_Col]
        self.piece_Captured = board[self.end_Row][self.end_Col]
        self.move_Id = self.start_Row*1000 + self.start_Col*100 + self.end_Row*10 + self.end_Col #a unique move id  
        
    #Overriding the equals method, cause we are using a class
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.move_Id == other.move_Id
        return False
            
    
    def getChessNotation(self):
        return self.getRankFile(self.start_Row,self.start_Col)+"-"+self.getRankFile(self.end_Row,self.end_Col)
    
    def getRankFile(self,r,c):
        return self.cols_To_Files[c] + self.rows_To_Ranks[r]
        
        