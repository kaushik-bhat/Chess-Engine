class GameState():
    def __init__(self):
        #The board is a 8x8  , each element has 2 characters
        # First character represents the color of the piece and the second character represents the piece itself
        #"--" empty square on the chess board with no piece
        self.board = [
            ["bR" , "bN" , "bB" , "bQ" , "bK" , "bB" , "bN" , "bR"],
            ["bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp" , "bp"],
            ["--" , "--" , "--" , "wp" , "--" , "--" , "--" , "--"],
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
    '''
    Takes a move as a paramter and executes it(this doesnt take into account castling and en-passant)
    '''    
    def makeMove(self,move):
        self.board[move.start_Row][move.start_Col] = "--"   #starting square becomes empty
        self.board[move.end_Row][move.end_Col] = move.piece_Moved   #ending square is replaced by the piece moved
        self.moveLog.append(move)   #log the moves so that we can undo later   
        self.whiteToMove = not self.whiteToMove #change the players turn
    
    
    #to undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0 :  #making sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.start_Row][move.start_Col] = move.piece_Moved
            self.board[move.end_Row][move.end_Col] = move.piece_Captured
            self.whiteToMove = not self.whiteToMove
            
    #All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
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
    
    #Get all possible moves for the Rook at r,c and add to list moves
    def getRookMoves(self,r,c,moves):
        pass
    
    #Get all possible moves for the Knight at r,c and add to list moves
    def getKnightMoves(self,r,c,moves):
        pass
    
    #Get all possible moves for the Bishop at r,c and add to list moves
    def getBishopMoves(self,r,c,moves):
        pass
    
    #Get all possible moves for the Queen at r,c and add to list moves
    def getQueenMoves(self,r,c,moves):
        pass
    
    #Get all possible moves for the King at r,c and add to list moves
    def getKingMoves(self,r,c,moves):
        pass
                
            
        
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
        
        