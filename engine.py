import numpy as np

class GameState():
    def __init__(self):
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
        self.move_funcs = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                           'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
    
    def makeMove(self, move):
        self.board[move.start_sq_row][move.start_sq_col] = "--"
        self.board[move.end_sq_row][move.end_sq_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved[1] == 'K':
            if move.piece_moved[0] == 'b':
                self.black_king_loc = (move.end_sq_row, move.end_sq_col)
            if move.piece_moved[0] == 'w':
                self.white_king_loc = (move.end_sq_row, move.end_sq_col)

    def undoMove(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_sq_row][move.start_sq_col] = move.piece_moved
            self.board[move.end_sq_row][move.end_sq_col] = move.piece_took
            self.white_to_move = not self.white_to_move

    # get all possible pawn moves
    def getPawnMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            if self.board[r-1][c] == "--":
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move(self.board, (r, c), (r-1, c)))
                    #checking for 2 square moves
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move(self.board, (r, c), (r-2, c)))
            if c-1 >= 0: #ensure we don't go out of the board to left
                if self.board[r-1][c-1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move(self.board, (r, c), (r-1, c-1)))
            if c+1 <= 7: #ensure we don't go out of the board to right
                if self.board[r-1][c+1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move(self.board, (r, c), (r-1, c+1)))
        else:
            if self.board[r+1][c] == "--":
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move(self.board, (r, c), (r+1, c)))
                    #checking for 2 square moves
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move(self.board, (r, c), (r+2, c)))
            if c-1 >= 0: #ensure we don't go out of the board to left
                if self.board[r-1][c-1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move(self.board, (r, c), (r+1, c-1)))
            if c+1 <= 7: #ensure we don't go out of the board to right
                if self.board[r-1][c+1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move(self.board, (r, c), (r+1, c+1)))        

    # get all possible rook moves
    def getRookMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # can't remove queen from pin with rook moves, only possible in bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        can_be_caputured = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]): # pinned in both directions
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move(self.board, (r, c), (end_row, end_col)))
                        elif end_piece[0] == can_be_caputured:
                            moves.append(Move(self.board, (r, c), (end_row, end_col)))
                            break
                        else: break
                else: break

    # get all possible knight moves
    def getKnightMoves(self, r, c, moves):
        # pin direction not required for a knight
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        possibilities = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        same_color = 'w' if self.white_to_move else 'b'
        for p in possibilities:
            end_row, end_col = r + p[0], c + p[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != same_color:
                        moves.append(Move(self.board, (r, c), (end_row, end_col)))

    # get all possible bishop moves
    def getBishopMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        can_be_caputured = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]): # pinned in both directions
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move(self.board, (r, c), (end_row, end_col)))
                        elif end_piece[0] == can_be_caputured:
                            moves.append(Move(self.board, (r, c), (end_row, end_col)))
                            break
                        else: break
                else: break

    # get all possible queen moves
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # get all possible king moves
    def getKingMoves(self, r, c, moves):
        possibilities = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        same_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row, end_col = r + possibilities[i][0], c + possibilities[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != same_color:
                    # placing king on goto square and checking for checks
                    if same_color == 'w':
                        self.white_king_loc = (end_row, end_col)
                    else:
                        self.black_king_loc = (end_row, end_col)

                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move(self.board, (r, c), (end_row, end_col)))
                    
                    # placing king back on original location
                    if same_color == 'w':
                        self.white_king_loc = (r, c)
                    else:
                        self.black_king_loc = (r, c)


    # get all possible moves not considering checks after that
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_funcs[piece](r, c, moves)
        return moves
    
    # check for all pins and checks
    def checkForPinsAndChecks(self):
        pins = [] # store pinned piece loc and directions of pin
        checks = [] # store squares where other color is applying check
        in_check = False
        
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_sq_row = self.white_king_loc[0]
            start_sq_col = self.white_king_loc[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_sq_row = self.black_king_loc[0]
            start_sq_col = self.black_king_loc[1]

        # checking outwards from king for all pins and checks
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for d_idx in range(len(directions)):
            d = directions[d_idx]
            possible_pin = ()
            for i in range(1, 8):
                end_row, end_col = start_sq_row + d[0] * i, start_sq_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K': # to avoid an imaginary 2nd king while calling this func in getKingMoves
                        if possible_pin == (): # first own piece could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else: break # 2nd own piece, so no pin or check possible in this direction
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        # 5 possibilities here
                        # 1) horizontally or vertically from king and piece is rook
                        # 2) diagonally from king and piece is bishop
                        # 3) any direction from king and piece is queen
                        # 4) one square diagonally from king and piece is pawn
                        # 5) one square any direction from king and piece is king (king cannot check king)
                        if (0 <= d_idx <= 3 and piece_type == 'R') or \
                                (4 <= d_idx <= 7 and piece_type == 'B') or \
                                (piece_type == 'Q') or \
                                (i == 1 and piece_type == 'P' and ((enemy_color == 'w' and 6 <= d_idx <= 7) or (enemy_color == 'b' and 4 <= d_idx <= 5))) or \
                                (i == 1 and piece_type == 'K'):
                            if possible_pin == (): # no blocking piece so directly check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else: # there is a blocking piece which will lead to a pin
                                pins.append(possible_pin)
                                break
                        else: break

        # checking for knight checks
        possibilities = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for p in possibilities:
            end_row, end_col = start_sq_row + p[0], start_sq_col + p[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, p[0], p[1]))
        return in_check, pins, checks


        
    # get all valid moves from all possible moves
    def getAllValidMoves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.white_to_move:
            king_row = self.white_king_loc[0]
            king_col = self.white_king_loc[1]
        else:
            king_row = self.black_king_loc[0]
            king_col = self.black_king_loc[1]

        if self.in_check:
            # just one check, not compulsory to move king
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                check_row, check_col = check[0], check[1]
                piece_checking = self.board[check_row][check_col] #piece causing check
                valid_squares = [] # squares where to pieces can move

                # for knight, either capture it or move king
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                # for the rest, blocking can also be done
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i) # using check directions
                        valid_squares.append(valid_square)
                        # end checks when reach check square
                        if valid_square[0] == check_row and valid_square[1] == check_col: break
                
                # removing all moves that don't block check or move king
                for i in range(len(moves)-1, -1, -1):
                    # if not moving king then block or capture
                    if moves[i].piece_moved[1] != 'K':
                        # remove move if it is not blocking or capturing
                        if not (moves[i].end_sq_row, moves[i].end_sq_col) in valid_squares:
                            moves.remove(moves[i])
            # double check, king has to move
            else:
                moves = self.getKingMoves(king_row, king_col, moves)
        # no checks then all moves are fine
        else:
            moves = self.getAllPossibleMoves()
        return moves


class Move():
    # mapping rows and cols
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {val: key for key, val in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7} 
    cols_to_files = {val: key for key, val in files_to_cols.items()}

    def __init__(self, board, start_sq, end_sq):
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