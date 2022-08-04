# It stores all the information about the current state of the game. It will also be responsible for current moves.
# It will also keep move log.

# from typing import Set, Tuple

class GameState:
    # initialize the timer

    def __init__(self):
        # board is 8x8 2d list, each element of the list has 2 characters.
        # the first character repsents color and the second character represents the type of the piece.
        # "--" represents the empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.pieceCapturedLog = []
        self.captureOn = False
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = ()  # Co-ordinates for the square where en passant capture is possible
        self.enpassantPossibleLogs = [self.enpassantPossible]
        self.pieceCaptured = '--'
        self.currentCastlingRights = CastlingRights(True, True, True, True)
        self.castleRightsLog = [CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                               self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]

    # Take moves parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            # promotedPiece = input("Promote to Q, R, B, or N:")  # we can promote the piece selected
            # promotedPiece = promotedPiece.upper()
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        if move.pieceCaptured != "--":
            if move.pieceCaptured[0] == "w":
                if move.pieceCaptured[1] == "P":
                    capture = "White Pawn   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "N":
                    capture = "White Knight   "
                    self.captureOn = True
                    self.pieceCapturedLog.append(capture)
                elif move.pieceCaptured[1] == "B":
                    capture = "White Bishop   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "R":
                    capture = "White Rook   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "Q":
                    capture = "White Queen   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
            elif move.pieceCaptured[0] == "b":
                if move.pieceCaptured[1] == "P":
                    capture = "Black Pawn   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "N":
                    capture = "Black Knight   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "B":
                    capture = "Black Bishop   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "R":
                    capture = "Black Rook   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
                elif move.pieceCaptured[1] == "Q":
                    capture = "Black Queen   "
                    self.pieceCapturedLog.append(capture)
                    self.captureOn = True
            else:
                self.captureOn = False
        # # en Passant
        # for i in range(0, 8):
        #     if self.enpassantPossible == (2, i) and self.board[2][i] == 'wP':
        #         self.board[3][i] = '--'
        #         self.pieceCaptured = 'bP'
        #     elif self.enpassantPossible == (5, i) and self.board[5][i] == 'bP':
        #         self.board[4][i] = '--'
        #         self.pieceCaptured = 'wP'
        # #
        # # update en passant possible variable
        # if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # only on 2 square pawn advances
        #     self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        # else:
        #     self.enpassantPossible = ()
        # # if en passant move then must update the board to capture
        # if move.isEnpassantMove:
        #     self.board[move.startRow][move.startCol] = '--'
        #
        # castle move
        # if self.castle:
        #     if move.endCol - move.startCol == 2:  # kingside castle move
        #         self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # moves the rook
        #         self.board[move.endRow][move.endCol + 1] = '--'  # erase old rook
        #     else:  # queenside castle moves
        #         self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # moves the rook
        #         self.board[move.endRow][move.endCol - 2] = '--'  # erase old rook
        #     self.castle = False
        # #
        # # self.enpassantPossibleLogs.append(self.enpassantPossible)
        # # # update castling rights - whenever it is a rook or a king move
        # self.updateCastlingRights(move)
        # self.castleRightsLog.append(CastlingRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
        #                                            self.currentCastlingRights.bks, self.currentCastlingRights.bqs))

    # undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0:  # makes sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update king's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo en passant

            # for i in range(0, 8):
            #     if self.enpassantPossible == () and self.board[3][i] == 'wP' and move.endRow == 2 and self.pieceCaptured == 'bP' and move.pieceMoved == 'wP':
            #         self.board[move.endRow+1][move.endCol] = self.pieceCaptured
            #         self.enpassantPossible = (move.endRow, move.endCol)
            #     elif self.enpassantPossible == () and self.board[4][i] == 'bP' and move.endRow == 5 and self.pieceCaptured == 'wP' and move.pieceMoved == 'bP':
            #         self.board[move.endRow-1][move.endCol] = self.pieceCaptured
            #         self.enpassantPossible = (move.endRow, move.endCol)
            # if move.isEnpassantMove:
            #     self.board[move.endRow][move.endCol] = '--'  # landing square blank
            #     self.board[move.startRow][move.startCol] = move.pieceCaptured  # put the piece to the
            #     # correct place for where it was
            # self.enpassantPossibleLogs.pop()
            # self.enpassantPossible = self.enpassantPossibleLogs[-1]

            # in the list
            # undo castle moves
            # if self.castleRightsLog:
            #     if move.endCol - move.startCol == 2:  # kingside
            #         self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
            #         self.board[move.endRow][move.endCol - 1] = '--'
            #     else:
            #         self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
            #         self.board[move.endRow][move.endCol + 1] = '--'
            #
            # # undo castling rights
            # self.castleRightsLog.pop()  # get rid of the new castle rights from the move we are undoing
            # self.currentCastlingRights = self.castleRightsLog[-1]  # set the current castling rights to the last one
            # self.checkMate = False
            # self.staleMate = False
            if move.pieceCaptured != "--" and self.captureOn is True and self.pieceCapturedLog != []:
                self.pieceCapturedLog.pop()

    # # update the castle rights given the move
    # def updateCastlingRights(self, move):
    #     if move.pieceMoved == 'wK':
    #         self.currentCastlingRights.wks = False
    #         self.currentCastlingRights.wqs = False
    #     elif move.pieceMoved == 'bK':
    #         self.currentCastlingRights.bqs = False
    #         self.currentCastlingRights.bks = False
    #     elif move.pieceMoved == 'wR':
    #         if move.startRow == 7:
    #             if move.startCol == 0:  # left Rook
    #                 self.currentCastlingRights.wqs = False
    #             elif move.startCol == 7:  # right Rook
    #                 self.currentCastlingRights.wks = False
    #     elif move.pieceMoved == 'bR':
    #         if move.startRow == 0:
    #             if move.startCol == 0:  # left Rook
    #                 self.currentCastlingRights.bqs = False
    #             elif move.startCol == 7:  # right Rook
    #                 self.currentCastlingRights.bks = False

    # all moves considering checks
    def getValidMoves(self):
        # # 1) generate all the possible moves = self.getAllPossibleMoves()
        # # 2) for each move, make the move
        # for i in range(len(moves)-1, -1, -1):  # when removing from the list go backwards through that list
        #     self.makeMove(moves[i])
        #     # 3) generate all opponent's move
        #     # 4) for each of your opponent's moves, see if they attack the king
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         moves.remove(moves[i])  # 5) if they do attack the king it's not the valid move
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        # if len(moves) == 0: # either checkmate or stalemate
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False
        #
        # return moves
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only one check, block check or move king
                moves = self.getAllPossibleMoves
                if self.whiteToMove:
                    self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, 'w')
                else:
                    self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, 'b')
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # squares that piece can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)  # check[2] and check[3] are
                        # the check directions
                        validSquares.append(validSquare)
                        if validSquares[0] == checkRow and validSquares[1] == checkCol:  # once we get to piece and
                            # check
                            break
                # get rid of any moves that don't block or move king
                for i in range(len(moves) - 1, -1, -1):  # go through backwards when you are removing from the list
                    # using iteration
                    if moves[i].pieceMoved[1] != "K":  # Move doesn't move king, so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:  # move doesn't block, check or
                            # capture piece
                            moves.remove(moves[i])
            else:  # double check king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    # determines if the current player is in the check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1], 'w')
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1], 'b')

    # determine if the enemy can attack the square r, c
    # noinspection PyShadowingBuiltins
    def squareUnderAttack(self, r, c, allycolor):
        # check outward from square
        enemycolor = 'w' if allycolor == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allycolor:  # no attack from that direction
                        break
                    elif endPiece[0] == enemycolor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and (
                                        (enemycolor == 'w' and 6 <= j <= 7) or (enemycolor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            return True
                        else:
                            break
                else:
                    break
        # check for knight's check
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemycolor and endPiece[1] == 'N':  # enemy knight attacking king
                    return True

        return False
        # self.whiteToMove = not self.whiteToMove  # switch to opponent's point of view
        # oopMoves = self.getAllPossibleMoves
        # self.whiteToMove = not self.whiteToMove  # switch turns back
        # for move in oopMoves:
        #     if move.endRow == r and move.endCol == c:  # square is under attack
        #         return True
        # return False

    @property
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # piece function based on piece types
        return moves

    # get all the pawn moves
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'

        if self.board[r + moveAmount][c] == "--":  # first square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r, c), (r + moveAmount, c), self.board))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c - 1 >= 0:  # capture to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board))
                if (r + moveAmount, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board))
        if c + 1 <= 7:  # capture to right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board))
                if (r + moveAmount, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board))

        # if self.whiteToMove:  # white pawn move
        #     if self.board[r - 1][c] == "--":  # 1 square pawn advance
        #         if not piecePinned or pinDirection == (-1, 0):
        #             moves.append(Move((r, c), (r - 1, c), self.board))
        #             if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
        #                 moves.append(Move((r, c), (r - 2, c), self.board))
        #     if c - 1 >= 0:  # captures to the left
        #         if self.board[r - 1][c - 1][0] == 'b':  # Enemy piece to capture
        #             if not piecePinned or pinDirection == (-1, -1):
        #                 moves.append(Move((r, c), (r - 1, c - 1), self.board))
        #             elif (r-1, c-1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
        #     if c + 1 <= 7:  # captures to the right
        #         if self.board[r - 1][c + 1][0] == 'b':  # Enemy piece to capture
        #             if not piecePinned or pinDirection == (-1, 1):
        #                 moves.append(Move((r, c), (r - 1, c + 1), self.board))
        #             elif (r-1, c+1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        # else:  # black pawn move
        #     if self.board[r + 1][c] == "--":  # 1 square pawn advance
        #         if not piecePinned or pinDirection == (1, 0):
        #             moves.append(Move((r, c), (r + 1, c), self.board))
        #             if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
        #                 moves.append(Move((r, c), (r + 2, c), self.board))
        #     if c - 1 >= 0:  # captures to the left
        #         if self.board[r + 1][c - 1][0] == 'w':  # Enemy piece to capture
        #             if not piecePinned or pinDirection == (1, -1):
        #                 moves.append(Move((r, c), (r + 1, c - 1), self.board))
        #             elif (r+1, c-1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
        #     if c + 1 <= 7:  # captures to the right
        #         if self.board[r + 1][c + 1][0] == 'w':  # Enemy piece to capture
        #             if not piecePinned or pinDirection == (1, 1):
        #                 moves.append(Move((r, c), (r + 1, c + 1), self.board))
        #             elif (r+1, c+1) == self.enpassantPossible:
        #                 moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    # get all the rook moves
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':  # can't remove queen from pin on rook moves, only remove it on bishop
                    # moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemycolor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endpiece = self.board[endRow][endCol]
                        if endpiece == "--":  # empty space  valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endpiece[0] == enemycolor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    # get all the knight moves
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((-2, +1), (-2, -1), (+2, +1), (+2, -1), (-1, -2), (+1, -2), (-1, +2), (+1, +2))
        allycolor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allycolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    # get all the Bishop moves
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemycolor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece invalid
                            break
                else:  # off board
                    break

    # get all the Queen moves
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # get all the King moves
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allycolor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:  # not an ally piece (empty or enemy piece)
                    # place king on end squares and check for checks
                    if allycolor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back on original location
                    if allycolor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        # self.getCastleMoves(r, c, moves, allycolor)

    # generate all valid castle moves for the king at (r, c) and add them to the list of moves
    def getCastleMoves(self, r, c, moves, allycolor):
        if self.inCheck:
            return  # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (
                not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves, allycolor)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (
                not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves, allycolor)

    def getKingsideCastleMoves(self, r, c, moves, allycolor):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and \
                not self.squareUnderAttack(r, c + 1, allycolor) and not self.squareUnderAttack(r, c + 2, allycolor):
            moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves, allycolor):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                not self.squareUnderAttack(r, c - 1, allycolor) and not self.squareUnderAttack(r, c - 2, allycolor):
            moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    # Returns if the player is in check, a list of pins, and a list of checks
    def checkForPinAndChecks(self):
        pins = []  # square where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying to check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outwards from the king for the pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():  # list allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        Type = endPiece[1]
                        # 5 possibilities here in this complex condition
                        # 1) orthogonally away from the king and the piece is a rook
                        # 2) diagonally away from the king and the piece is a bishop
                        # 3) 1 square away diagonally from the king and piece is the pawn
                        # 4) any direction and piece is queen
                        # 5) any direction 1 square away and the piece is a king(this is
                        #    necessary to prevent a king move to a square controlled by another king)
                        if (0 <= j <= 3 and Type == 'R') or \
                                (4 <= j <= 7 and Type == 'B') or \
                                (i == 1 and Type == 'P' and (
                                        (enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (Type == "Q") or (i == 1 and Type == 'K'):
                            if possiblePin == ():  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


class CastlingRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7, }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.inti = 0
        # Pawn Promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (
                self.pieceMoved == 'bP' and self.endRow == 7)
        # en Passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'  # enpassant capture
        # castle moves
        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this look like real chess notation
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow, self.endCol)

    def getRankFiles(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # overriding the equals method
    def __str__(self):
        # castle move
        if self.isCastleMove:
            return "o_o" if self.endCol == 6 else "o_o_o"

        endSquare = self.getRankFiles(self.endRow, self.endCol)
        # pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
