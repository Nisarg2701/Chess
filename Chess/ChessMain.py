# Driver File. It is responsible for user input and current GameState Object.
import time
import pygame as p
from Chess import ChessEngine, SmartMovesFinder
from multiprocessing import Process, Queue

WIDTH = HEIGHT = 512  # 400 IS ANOTHER OPTION
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT
DIMENSION = 8  # DIMENSION OF CHESS IS 8X8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # FOR ANIMATIONS
IMAGES = {}


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


# initialize a global dictionary of images. this will be called exactly once in the main

def loadImages():
    pieces = ['wP', 'wK', 'wN', 'wQ', 'wR', 'wB', 'bP', 'bK', 'bN', 'bQ', 'bR', 'bB']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQ_SIZE - 8, SQ_SIZE - 8))
    # we can access an image by the method shown above.


class DepthClass:
    def __init__(self, depth=0):
        self._depth = depth

    def get_depth(self):
        return self._depth

    def set_depth(self, d):
        self._depth = d


# THIS will be our main driver code. this will handle user input and updating the graphics.

# noinspection PyUnboundLocalVariable
def main():
    p.init()
    p.display.set_caption("Chess")
    icon = p.image.load("Images/wK.ico")
    p.display.set_icon(icon)
    screen = p.display.set_mode((WIDTH + 2 * MOVE_LOG_PANEL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("arial", 14, False, False)
    gs = ChessEngine.GameState()
    validmoves = gs.getValidMoves()
    once = 0
    movemade = False  # flag the variable when the move is made
    animate = False  # flag variable for when we should animate
    loadImages()  # only do this once before the while loop
    running = True
    sqselected = ()  # no squares selected initially, keep track of last click of the user (tuple: (row, col))
    playerclicks = []  # keeps track of player clicks (two tuples: [(6,4), (4,4)])
    gameOver = False
    print("if human is playing then h and if computer is playing then c")
    while True:
        try:
            player1 = input("player1 ")
        except player1 != 'h' or player1 != 'c':
            continue
        if player1 == 'h' or player1 == 'c':
            break
    while True:
        try:
            player2 = input("player2 ")
        except player2 != 'h' or player2 != 'c':
            continue
        if player2 == 'h' or player2 == 'c':
            break
    if player1 == 'c' or player2 == 'c':
        while True:
            try:
                Depth = input("Enter game level from 1 to 5: ")
            except Depth != '1' or Depth != '2' or Depth != '3' or Depth != '4' or Depth != '5' or Depth != '6':
                continue
            if Depth == '1' or Depth == '2' or Depth == '3' or Depth == '4' or Depth == '5' or Depth == '6':
                depth = DepthClass()
                depth.set_depth(int(Depth))
                break
    else:
        depth = DepthClass()
        depth.set_depth(0)
    if player1 == 'h':
        playerOne = True  # if human is playing then true and if AI is playing then false
    elif player1 == 'c':
        playerOne = False  # if human is playing then true and if AI is playing then false
    if player2 == 'c':
        playerTwo = False  # same as above
    elif player2 == 'h':
        playerTwo = True  # same as above
    print(playerOne, playerTwo)
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    start_time = time.time()
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # (x,y) location of the mouse
                    col = (location[0] - 256) // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqselected == (row, col) or col >= 8:  # the user clicked the same square twice
                        sqselected = ()  # deselect
                        playerclicks = []  # clear player clicks
                    else:
                        sqselected = (row, col)
                        playerclicks.append(sqselected)  # append for both first click and second click
                    if len(playerclicks) == 2 and humanTurn:  # after second click
                        move = ChessEngine.Move(playerclicks[0], playerclicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validmoves)):
                            if move == validmoves[i]:
                                gs.makeMove(move)
                                movemade = True
                                animate = True
                                sqselected = ()  # reset user clicks
                                playerclicks = []
                        if not movemade:
                            playerclicks = [sqselected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if p.key.get_pressed()[p.K_z]:  # Undo when 'z' is pressed
                    gs.undoMove()
                    movemade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if p.key.get_pressed()[p.K_r]:  # when r is pressed it will reset the board
                    gs = ChessEngine.GameState()
                    validmoves = gs.getValidMoves()
                    sqselected = ()
                    playerclicks = []
                    movemade = False
                    animate = False
                    gameOver = False
                    moveUndone = True

        # ai move finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("thinking...")
                returnQueue = Queue()  # used to pass data between threads
                moveFinderProcess = Process(target=SmartMovesFinder.findBestMove, args=(gs, validmoves, depth.get_depth(), returnQueue))
                moveFinderProcess.start()  # call findBestMove(gs, validmoves, returnQueue)

            if not moveFinderProcess.is_alive():
                print("Dumb Thinking...")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = SmartMovesFinder.findRandomMove(validmoves)
                gs.makeMove(AIMove)
                movemade = True
                animate = True
                AIThinking = False

        if movemade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validmoves = gs.getValidMoves()
            movemade = False
            animate = False
            moveUndone = False
        drawGameState(screen, gs, validmoves, sqselected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            drawEndGameText(screen,
                            'Stalemate' if gs.staleMate else 'White wins by Checkmate' if not gs.whiteToMove else 'Black wins by Checkmate')

        elif gs.inCheck:
            drawEndGameText(screen, 'White in Check' if gs.whiteToMove else 'Black in Check')

        clock.tick(MAX_FPS)
        p.display.flip()
    end_time = time.time()
    time_lapsed = end_time - start_time
    time_convert(time_lapsed)


# Responsible for graphics within current gameState

def drawGameState(screen, gs, validmoves, sqSelected, moveLogFont):
    drawBoard(screen)  # Draw squares on board
    highLightSquares(screen, gs, validmoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on the board
    drawMoveLog(screen, gs, moveLogFont)
    showPieceCapture(screen, gs, moveLogFont)


# highlight squares selected
def highLightSquares(screen, gs, validmoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # square selected is a piece that can't be moved
            # highlight the square selected
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # 0 transparent; 255 opaque
            s.fill(p.Color('orange'))
            screen.blit(s, (c * SQ_SIZE + 256, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('blue'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE + 256, move.endRow * SQ_SIZE))


# draw the squares on board. the top left square is always light

def drawBoard(screen):
    # noinspection PyGlobalUndefined
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + 256, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # draw pieces on board with current GameState.board


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + 258, r * SQ_SIZE + 4, SQ_SIZE, SQ_SIZE))


#  Animating the Move
def animateMove(move, screen, board, clock):
    # noinspection PyGlobalUndefined
    global colors
    # coords = []  # list of columns that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE + 256, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto the rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE + 256, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE + 256, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


'''
Draws Move Log 
'''


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(WIDTH + 256, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    preText = ["This screen shows Piece Moves. Every move", "is grouped in pair of first white and second",
               "black respectively"]
    linesPerRow = 1
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(preText), linesPerRow):
        textObject = font.render(preText[i], True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):  # make sure black made a move
            moveString += str(moveLog[i + 1])
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding + 55
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j] + " "
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


# noinspection PyTypeChecker
def drawEndGameText(screen, text):
    font = p.font.SysFont("arial", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(WIDTH / 2, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                            HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


# show piece capture
def showPieceCapture(screen, gs, font):
    pieceCaptureLogRect = p.Rect(0, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), pieceCaptureLogRect)
    textObject = font.render("This screen shows Piece Capture", True, p.Color('white'))
    textLocation = pieceCaptureLogRect.move(5, 5)
    screen.blit(textObject, textLocation)
    pieceCaptureLog = gs.pieceCapturedLog
    pieceCaptureTexts = []
    for i in range(0, len(pieceCaptureLog), 2):
        pieceCaptureString = str(pieceCaptureLog[i]) + " "
        if i + 1 < len(pieceCaptureLog):  # make sure black made a move
            pieceCaptureString += str(pieceCaptureLog[i + 1])
        pieceCaptureTexts.append(pieceCaptureString)
    piecePerRow = 1
    padding = 5
    lineSpacing = 6
    textY = padding + 20
    for i in range(0, len(pieceCaptureTexts), piecePerRow):
        text = ""
        for j in range(piecePerRow):
            if i + j < len(pieceCaptureTexts):
                text += pieceCaptureTexts[i + j] + ""
        textObject = font.render(text, True, p.Color('white'))
        textLocation = pieceCaptureLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


if __name__ == "__main__":
    main()
