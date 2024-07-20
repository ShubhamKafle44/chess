import pygame as p

from Chess import ChessEngine

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8  #this is the dimension of the chess board 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images
'''


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

    #WE CAN ACCESS AN IMAGE USING IMAGES[wp]


'''
THis will be the main driver 
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag varriable
    loadImages()  #loading the images only once
    running = True
    sqSelected = ()
    playerClicks = []  #keep track of player clicks(two tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #these are mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #get the (x,y) position of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()  #unselect the square
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            #This are key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
This is responsible for current state of the game
'''


def drawGameState(screen, gs):
    drawBoard(screen)  #this is going to draw squares on the board

    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color('white'), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
