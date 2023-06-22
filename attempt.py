def shift(bitboard, value):
    if value < 0:
        # Convert negative left value to positive right value
        value = -value
        return bitboard >> value
    else:
        return bitboard << value


class BitboardChess:
    NUM_SQUARES = 64

    # Define constants for each square on the board
    A1, B1, C1, D1, E1, F1, G1, H1 = range(8)
    A2, B2, C2, D2, E2, F2, G2, H2 = range(8, 16)
    A3, B3, C3, D3, E3, F3, G3, H3 = range(16, 24)
    A4, B4, C4, D4, E4, F4, G4, H4 = range(24, 32)
    A5, B5, C5, D5, E5, F5, G5, H5 = range(32, 40)
    A6, B6, C6, D6, E6, F6, G6, H6 = range(40, 48)
    A7, B7, C7, D7, E7, F7, G7, H7 = range(48, 56)
    A8, B8, C8, D8, E8, F8, G8, H8 = range(56, 64)

    # Define bitboard representations for each square
    squares = {
        'a1': 1 << A1, 'b1': 1 << B1, 'c1': 1 << C1, 'd1': 1 << D1,
        'e1': 1 << E1, 'f1': 1 << F1, 'g1': 1 << G1, 'h1': 1 << H1,
        'a2': 1 << A2, 'b2': 1 << B2, 'c2': 1 << C2, 'd2': 1 << D2,
        'e2': 1 << E2, 'f2': 1 << F2, 'g2': 1 << G2, 'h2': 1 << H2,
        'a3': 1 << A3, 'b3': 1 << B3, 'c3': 1 << C3, 'd3': 1 << D3,
        'e3': 1 << E3, 'f3': 1 << F3, 'g3': 1 << G3, 'h3': 1 << H3,
        'a4': 1 << A4, 'b4': 1 << B4, 'c4': 1 << C4, 'd4': 1 << D4,
        'e4': 1 << E4, 'f4': 1 << F4, 'g4': 1 << G4, 'h4': 1 << H4,
        'a5': 1 << A5, 'b5': 1 << B5, 'c5': 1 << C5, 'd5': 1 << D5,
        'e5': 1 << E5, 'f5': 1 << F5, 'g5': 1 << G5, 'h5': 1 << H5,
        'a6': 1 << A6, 'b6': 1 << B6, 'c6': 1 << C6, 'd6': 1 << D6,
        'e6': 1 << E6, 'f6': 1 << F6, 'g6': 1 << G6, 'h6': 1 << H6,
        'a7': 1 << A7, 'b7': 1 << B7, 'c7': 1 << C7, 'd7': 1 << D7,
        'e7': 1 << E7, 'f7': 1 << F7, 'g7': 1 << G7, 'h7': 1 << H7,
        'a8': 1 << A8, 'b8': 1 << B8, 'c8': 1 << C8, 'd8': 1 << D8,
        'e8': 1 << E8, 'f8': 1 << F8, 'g8': 1 << G8, 'h8': 1 << H8
    }

    # Define piece bitboards
    EMPTY = 0
    PAWN = 'pawn'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'

    WHITE = 'white'
    BLACK = 'black'

    def __init__(self):
        # ...

        self.piece_bitboards = {
            self.WHITE: {
                self.PAWN: int(self.squares['a2'] | self.squares['b2'] | self.squares['c2'] | self.squares['d2'] |
                               self.squares['e2'] | self.squares['f2'] | self.squares['g2'] | self.squares['h2']),
                self.KNIGHT: int(self.squares['b1'] | self.squares['g1']),
                self.BISHOP: int(self.squares['c1'] | self.squares['f1']),
                self.ROOK: int(self.squares['a1'] | self.squares['h1']),
                self.QUEEN: int(self.squares['d1']),
                self.KING: int(self.squares['e1'])
            },
            self.BLACK: {
                self.PAWN: int(self.squares['a7'] | self.squares['b7'] | self.squares['c7'] | self.squares['d7'] |
                               self.squares['e7'] | self.squares['f7'] | self.squares['g7'] | self.squares['h7']),
                self.KNIGHT: int(self.squares['b8'] | self.squares['g8']),
                self.BISHOP: int(self.squares['c8'] | self.squares['f8']),
                self.ROOK: int(self.squares['a8'] | self.squares['h8']),
                self.QUEEN: int(self.squares['d8']),
                self.KING: int(self.squares['e8'])
            }
        }



        self.current_player = self.WHITE

    def generate_pawn_moves(self, square, color):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Get the pawn bitboard for the given color
        pawn_bb = self.piece_bitboards[color][self.PAWN]

        # Generate possible pawn moves
        moves = []

        # Check if the pawn can move one square forward
        forward_one = shift(square_bb, 8 if color == self.WHITE else -8)
        if forward_one & self.EMPTY:
            moves.append(forward_one)

        # Check if the pawn can move two squares forward from the starting position
        start_rank = 1 if color == self.WHITE else 6
        if square_bb & pawn_bb and forward_one & self.EMPTY:
            double_forward = shift(forward_one, 8 if color == self.WHITE else -8)
            if double_forward & self.EMPTY and (square_bb & self.squares[f'{chr(ord(square[0]))}{start_rank}']):
                moves.append(double_forward)

        # Check if the pawn can capture diagonally
        left_capture = shift(forward_one, -1 if color == self.WHITE else 1)
        right_capture = shift(forward_one, 1 if color == self.WHITE else -1)
        enemy_pieces = self.piece_bitboards[self.opposite_color(color)]
        if left_capture & enemy_pieces:
            moves.append(left_capture)
        if right_capture & enemy_pieces:
            moves.append(right_capture)

        return moves

    def generate_knight_moves(self, square):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Generate possible knight moves
        moves = []

        # Possible knight move offsets
        offsets = [-17, -15, -10, -6, 6, 10, 15, 17]

        for offset in offsets:
            move = shift(square_bb, offset)
            if move & self.EMPTY:
                moves.append(move)

        return moves

    def generate_bishop_moves(self, square):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Generate possible bishop moves
        moves = []

        # Generate diagonal moves in four directions
        directions = [7, 9, -7, -9]

        for direction in directions:
            move = square_bb
            while True:
                move = shift(move, direction)
                if move & self.EMPTY:
                    moves.append(move)
                else:
                    break

        return moves

    def generate_rook_moves(self, square):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Generate possible rook moves
        moves = []

        # Generate horizontal and vertical moves in four directions
        directions = [1, -1, 8, -8]

        for direction in directions:
            move = square_bb
            while True:
                move = shift(move, direction)
                if move & self.EMPTY:
                    moves.append(move)
                else:
                    break

        return moves

    def generate_queen_moves(self, square):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Generate possible queen moves
        moves = []

        # Generate diagonal and horizontal/vertical moves in eight directions
        directions = [7, 9, -7, -9, 1, -1, 8, -8]

        for direction in directions:
            move = square_bb
            while True:
                move = shift(move, direction)
                if move & self.EMPTY:
                    moves.append(move)
                else:
                    break

        return moves

    def generate_king_moves(self, square):
        # Get the bitboard for the given square
        square_bb = self.squares[square]

        # Generate possible king moves
        moves = []

        # Possible king move offsets
        offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

        for offset in offsets:
            move = shift(square_bb, offset)
            if move & self.EMPTY:
                moves.append(move)

        return moves

    def generate_moves(self):
        moves = []

        # Generate moves for pawns
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.PAWN:
                color = self.get_piece_color(square)
                moves.extend(self.generate_pawn_moves(square, color))

        # Generate moves for knights
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.KNIGHT:
                moves.extend(self.generate_knight_moves(square))

        # Generate moves for bishops
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.BISHOP:
                moves.extend(self.generate_bishop_moves(square))

        # Generate moves for rooks
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.ROOK:
                moves.extend(self.generate_rook_moves(square))

        # Generate moves for queens
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.QUEEN:
                moves.extend(self.generate_queen_moves(square))

        # Generate moves for kings
        for square in self.squares:
            piece = self.get_piece_on_square(square)
            if piece == self.KING:
                moves.extend(self.generate_king_moves(square))

        return moves
    def get_piece_on_square(self, square):
        for player in self.piece_bitboards:
            for piece in self.piece_bitboards[player]:
                if self.piece_bitboards[player][piece] & self.squares[square]:
                    return piece
        return None

    def get_piece_color(self, bitboard):
        if bitboard & self.piece_bitboards[self.WHITE][self.PAWN]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.WHITE][self.KNIGHT]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.WHITE][self.BISHOP]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.WHITE][self.ROOK]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.WHITE][self.QUEEN]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.WHITE][self.KING]:
            return self.WHITE
        elif bitboard & self.piece_bitboards[self.BLACK][self.PAWN]:
            return self.BLACK
        elif bitboard & self.piece_bitboards[self.BLACK][self.KNIGHT]:
            return self.BLACK
        elif bitboard & self.piece_bitboards[self.BLACK][self.BISHOP]:
            return self.BLACK
        elif bitboard & self.piece_bitboards[self.BLACK][self.ROOK]:
            return self.BLACK
        elif bitboard & self.piece_bitboards[self.BLACK][self.QUEEN]:
            return self.BLACK
        elif bitboard & self.piece_bitboards[self.BLACK][self.KING]:
            return self.BLACK
        else:
            return None


chess = BitboardChess()
chess.generate_moves()