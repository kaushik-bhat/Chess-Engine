import pygame as p
import ChessEngine

width = height = 704
dimension = 8
square_size = height // dimension
max_fps = 15 # for animation later on
images = {}

'''
initialise global dictionary of images in main function, so that it is called exactly once
Since it is an expensive operation
'''

def loadImages():
    pieces = ["wp" , "wR" , "wN" , "wB" , "wQ" , "wK" , "bp" , "bR" , "bN" , "bB" , "bQ" , "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/"+piece+".png") , (square_size,square_size))
    #Now we can access an image by images["wK"]
    
'''
The main driver of our code, this will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() #Game state from ChessEngine.py file
    valid_Moves = gs.getValidMoves()
    move_Made = False   #Flag variable for when a move is made
    loadImages()
    running = True
    square_Selected = ()    #initially nothing, stores user input selected square (row,col) tuple format
    player_Clicks = []  #keep track of player clicks [(r1,c1),(r2,c2),..] kind of a click log
    while running :
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #MOUSE HANDLERS
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()    #x and y coordinates
                col = location[0] // square_size  #x location is at 0 and y at 1
                row = location[1] // square_size
                if square_Selected == (row,col):
                    square_Selected = ()    #same square clicked twice case
                    player_Clicks = []
                else:    
                    square_Selected = (row,col)
                    player_Clicks.append(square_Selected)
                if len(player_Clicks) == 2: #basically after second click move should be registered, first click to select piece, second is where you want the piece to move 
                    move = ChessEngine.Move(player_Clicks[0],player_Clicks[1],gs.board)
                    print(move.getChessNotation())  #move_Notation
                    #print(move.move_Id) #move_ID
                    if move in valid_Moves:
                        gs.makeMove(move)
                        move_Made = True
                        square_Selected = ()
                        player_Clicks = []
                    else:
                        player_Clicks = [square_Selected]
            #KEYBOARD HANDLERS
            elif e.type == p.KEYDOWN:
                keys = p.key.get_pressed()
                if keys[p.K_LCTRL] or keys[p.K_RCTRL]:  #UNDO OPTION USING CTRL+Z
                    if e.key == p.K_z:
                        gs.undoMove()
                        move_Made = True
        if move_Made:
            valid_Moves = gs.getValidMoves()    #get new set of valid moves once a move is made
            move_Made = False                   #set the flag to false
        drawGameState(screen,gs)
        clock.tick(max_fps)
        p.display.flip()
    
def drawGameState(screen ,gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen , gs.board) #draw pieces on the squares

#Draw the squares on the board
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[(r+c)&1]
            p.draw.rect(screen,color,p.Rect(c*square_size,r*square_size,square_size,square_size))
            
#Draw the pieces on the board using the current GameState.board
def drawPieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece],p.Rect(c*square_size,r*square_size,square_size,square_size))

if __name__ == "__main__":    
    main()