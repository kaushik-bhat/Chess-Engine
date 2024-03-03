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