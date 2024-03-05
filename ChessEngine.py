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
    
    def getChessNotation(self):
        return self.getRankFile(self.start_Row,self.start_Col)+"-"+self.getRankFile(self.end_Row,self.end_Col)
    
    def getRankFile(self,r,c):
        return self.cols_To_Files[c] + self.rows_To_Ranks[r]
        
        