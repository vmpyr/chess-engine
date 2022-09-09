import pygame as pg
import engine

WIDTH = HEIGHT = 960
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
FPS = 15
IMAGES = {}


# initialize global dict of images
def loadImages():
    pieces = ['wP', 'wB', 'wR', 'wN', 'wQ',
              'wK', 'bP', 'bB', 'bR', 'bN', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("./graphics/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# for drawing the game state at a particular time
def drawBoard(gameBoard):
    boardColors = [pg.Color(238, 238, 213, 255), pg.Color(125, 148, 93, 255)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            boardColor = boardColors[(r+c) % 2]
            pg.draw.rect(gameBoard, boardColor, rect=pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(gameBoard, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                gameBoard.blit(IMAGES[piece], dest=pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(gameBoard, gs):
    # for drawing the board
    drawBoard(gameBoard)

    # for placing the pieces
    drawPieces(gameBoard, gs.board)


# main driver code for inputs and updating graphics
def main():
    pg.init()
    gameBoard = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    pg.display.set_caption('Chess')
    gameBoard.fill(pg.Color("white"))
    gs = engine.GameState()
    valid_moves = gs.getAllValidMoves()
    move_made = False

    loadImages()
    running = True
    sq_selected = () # tuple for selected square
    selection_hist = [] # list of 2 tuples for last 2 selections
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            
            # for mouse stuff
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col, row = location[0] // SQ_SIZE, location[1] // SQ_SIZE 
                if sq_selected == (row, col): # same square selected again
                    sq_selected = () # deselect square
                    selection_hist = [] # clear history
                else:
                    sq_selected = (row, col)
                    selection_hist.append(sq_selected)
                
                if len(selection_hist) == 2:
                    move = engine.Move(gs.board, selection_hist[0], selection_hist[1])
                    if move in valid_moves:
                        print(move.getNotation())
                        gs.makeMove(move)
                        move_made = True
                        sq_selected = ()
                        selection_hist = []
                    else:
                        selection_hist = [sq_selected]

            # for keyboard stuff
            elif e.type == pg.KEYDOWN:
                #undo when z is pressed
                if e.key == pg.K_z:
                    gs.undoMove()
                    move_made = True

        if move_made:
            valid_moves = gs.getAllValidMoves()
            move_made = False

        drawGameState(gameBoard, gs)
        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
