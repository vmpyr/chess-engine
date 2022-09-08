from shutil import move
import numpy as np

class GameState():
    def __init__(self) -> None:
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])

        self.white_to_move = True
        self.move_log = []

    def makeMove(self, move):
        self.board[move.start_sq_row][move.start_sq_col] = "--"
        self.board[move.end_sq_row][move.end_sq_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undoMove(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_sq_row][move.start_sq_col] = move.piece_moved
            self.board[move.end_sq_row][move.end_sq_col] = move.piece_took
            self.white_to_move = not self.white_to_move

    # get all possible pawn moves
    def getPawnMoves(self, r, c, moves):
        pass

    # get all possible rook moves
    def getRookMoves(self, r, c, moves):
        pass

    # get all possible knight moves
    def getKnightMoves(self, r, c, moves):
        pass

    # get all possible bishop moves
    def getBishopMoves(self, r, c, moves):
        pass

    # get all possible queen moves
    def getQueenMoves(self, r, c, moves):
        pass

    # get all possible king moves
    def getKingMoves(self, r, c, moves):
        pass

    # get all possible moves not considering checks after that
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) and (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves
        

    # get all valid moves from all possible moves
    def getAllValidMoves(self):
        return self.getAllPossibleMoves();       

class Move():
    # mapping rows and cols
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {val: key for key, val in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7} 
    cols_to_files = {val: key for key, val in files_to_cols.items()}

    def __init__(self, board, start_sq, end_sq) -> None:
        self.start_sq_row = start_sq[0]
        self.start_sq_col = start_sq[1]
        self.end_sq_row = end_sq[0]
        self.end_sq_col = end_sq[1]
        self.piece_moved = board[self.start_sq_row][self.start_sq_col]
        self.piece_took = board[self.end_sq_row][self.end_sq_col]
        self.move_ID = self.start_sq_row*1000 + self.start_sq_col*100 + self.end_sq_row*10 + self.end_sq_col

    # overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def getNotation(self):
        return self.cols_to_files[self.start_sq_col] + self.rows_to_ranks[self.start_sq_row] + self.cols_to_files[self.end_sq_col] + self.rows_to_ranks[self.end_sq_row]