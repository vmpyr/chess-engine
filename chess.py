import pygame as pg
import engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
print(SQ_SIZE)
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

    loadImages()
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        drawGameState(gameBoard, gs)
        clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
