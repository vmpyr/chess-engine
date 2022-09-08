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

    def getNotation(self):
        return self.cols_to_files[self.start_sq_col] + self.rows_to_ranks[self.start_sq_row] + self.cols_to_files[self.end_sq_col] + self.rows_to_ranks[self.end_sq_row]