import pygame as p
import ChessEngine

width = height = 512
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
    print(gs.board)
    loadImages()
    running = True
    while running :
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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