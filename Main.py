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
        # Set initial piece positions
        self.piece_bitboards = {
            self.WHITE: {
                self.PAWN: self.squares['a2'] | self.squares['b2'] | self.squares['c2'] | self.squares['d2'] |
                          self.squares['e2'] | self.squares['f2'] | self.squares['g2'] | self.squares['h2'],
                self.KNIGHT: self.squares['b1'] | self.squares['g1'],
                self.BISHOP: self.squares['c1'] | self.squares['f1'],
                self.ROOK: self.squares['a1'] | self.squares['h1'],
                self.QUEEN: self.squares['d1'],
                self.KING: self.squares['e1']
            },
            self.BLACK: {
                self.PAWN: self.squares['a7'] | self.squares['b7'] | self.squares['c7'] | self.squares['d7'] |
                          self.squares['e7'] | self.squares['f7'] | self.squares['g7'] | self.squares['h7'],
                self.KNIGHT: self.squares['b8'] | self.squares['g8'],
                self.BISHOP: self.squares['c8'] | self.squares['f8'],
                self.ROOK: self.squares['a8'] | self.squares['h8'],
                self.QUEEN: self.squares['d8'],
                self.KING: self.squares['e8']
            }
        }

        self.current_player = self.WHITE

    def currentPlayer(self):
        return self.current_player
    def make_move(self, from_square, to_square):
        piece = self.get_piece_on_square(from_square)
        if piece is None:
            raise ValueError("No piece found on the source square.")

        if self.current_player == self.WHITE:
            opponent = self.BLACK
        else:
            opponent = self.WHITE

        # Check if the move is legal
        if not self.is_legal_move(piece, from_square, to_square):
            raise ValueError("Illegal move.")

        # Make the move
        self.move_piece(piece, from_square, to_square)

        # Check for capturing
        if self.is_piece_on_square(opponent, to_square):
            self.capture_piece(opponent, to_square)

        # Switch players
        self.current_player = opponent

    def move_piece(self, piece, from_square, to_square):
        from_bb = self.piece_bitboards[self.current_player][piece]
        to_bb = self.squares[to_square]
        self.piece_bitboards[self.current_player][piece] = from_bb & ~self.squares[from_square] | to_bb

    def capture_piece(self, opponent, square):
        for piece in self.piece_bitboards[opponent]:
            if self.is_piece_on_square(opponent, square):
                self.piece_bitboards[opponent][piece] &= ~self.squares[square]
                break

    def is_legal_move(self, piece, from_square, to_square):
        # Check if the piece is allowed to move from the source square
        if not self.is_piece_on_square(self.current_player, from_square):
            return False

        # Check if the destination square is occupied by the current player's piece
        if self.is_piece_on_square(self.current_player, to_square):
            return False

        # Check specific rules for each piece
        if piece == self.PAWN:
            return self.is_legal_pawn_move(from_square, to_square)
        elif piece == self.KNIGHT:
            return self.is_legal_knight_move(from_square, to_square)
        elif piece == self.BISHOP:
            return self.is_legal_bishop_move(from_square, to_square)
        elif piece == self.ROOK:
            return self.is_legal_rook_move(from_square, to_square)
        elif piece == self.QUEEN:
            return self.is_legal_queen_move(from_square, to_square)
        elif piece == self.KING:
            return self.is_legal_king_move(from_square, to_square)

    def is_legal_pawn_move(self, from_square, to_square):
        from_bb = self.squares[from_square]
        to_bb = self.squares[to_square]

        if self.current_player == self.WHITE:
            direction = 1
            starting_rank = 2
            en_passant_rank = 5
        else:
            direction = -1
            starting_rank = 7
            en_passant_rank = 4


        if to_bb & shift(from_bb , 8*direction):  # Single move forward
                return True


        elif from_square[1] == str(starting_rank) and to_bb & shift(from_bb , 16 * direction):  # Double move forward
            return True
        elif (to_bb & shift(from_bb , 7 * direction)) and (to_square[0] != 'h'):  # Capture to the left
            return True
        elif (to_bb & shift(from_bb , 9 * direction)) and (to_square[0] != 'a'):  # Capture to the right
            return True
        elif (to_bb & shift(from_bb , 7 * direction)) and (to_square[1] == str(en_passant_rank)):
            return True
        elif (to_bb & shift(from_bb , 9 * direction)) and (to_square[1] == str(en_passant_rank)):
            return True

        return False

    def is_legal_knight_move(self, from_square, to_square):
        from_bb = self.squares[from_square]
        to_bb = self.squares[to_square]
        valid_moves = (
                (from_bb << 6) | (from_bb >> 10) |
                (from_bb << 10) | (from_bb >> 6) |
                (from_bb << 15) | (from_bb >> 17) |
                (from_bb << 17) | (from_bb >> 15)
        )
        return bool(to_bb & valid_moves)

    def is_legal_bishop_move(self, from_square, to_square):
        from_bb = self.squares[from_square]
        to_bb = self.squares[to_square]
        valid_moves = (
                self.get_bishop_moves(from_bb, self.squares['a1'], self.squares['h8'], -9) |
                self.get_bishop_moves(from_bb, self.squares['h1'], self.squares['a8'], -7) |
                self.get_bishop_moves(from_bb, self.squares['a8'], self.squares['h1'], 7) |
                self.get_bishop_moves(from_bb, self.squares['h8'], self.squares['a1'], 9)
        )
        return bool(to_bb & valid_moves)

    def is_legal_rook_move(self, from_square, to_square):
        from_bb = self.squares[from_square]
        to_bb = self.squares[to_square]
        valid_moves = (
                self.get_rook_moves(from_bb, self.squares['a1'], self.squares['h1'], -1) |
                self.get_rook_moves(from_bb, self.squares['h1'], self.squares['a1'], 1) |
                self.get_rook_moves(from_bb, self.squares['a1'], self.squares['a8'], 8) |
                self.get_rook_moves(from_bb, self.squares['a8'], self.squares['a1'], -8)
        )
        return bool(to_bb & valid_moves)

    def is_legal_queen_move(self, from_square, to_square):
        return self.is_legal_bishop_move(from_square, to_square) or self.is_legal_rook_move(from_square, to_square)

    def is_legal_king_move(self, from_square, to_square):
        from_bb = self.squares[from_square]
        to_bb = self.squares[to_square]
        valid_moves = (
                from_bb << 1 | from_bb >> 1 |
                from_bb << 8 | from_bb >> 8 |
                from_bb << 9 | from_bb >> 9 |
                from_bb << 7 | from_bb >> 7
        )
        return bool(to_bb & valid_moves)

    def is_piece_on_square(self, player, square):
        square_bb = self.squares[square]
        for piece in self.piece_bitboards[player]:
            if self.piece_bitboards[player][piece] & square_bb:
                return True
        return False

    def get_piece_on_square(self, square):
        for player in self.piece_bitboards:
            for piece in self.piece_bitboards[player]:
                if self.piece_bitboards[player][piece] & self.squares[square]:
                    return piece
        return None

    @staticmethod
    def get_bishop_moves(from_bb, start_bb, end_bb, shift):
        moves = 0
        current_bb = start_bb
        while current_bb != end_bb:
            moves |= current_bb
            current_bb <<= shift
        moves |= current_bb  # Include the last square
        return moves

    @staticmethod
    def get_rook_moves(from_bb, start_bb, end_bb, shift):
        moves = 0
        current_bb = start_bb
        while current_bb != end_bb:
            moves |= current_bb
            current_bb = (current_bb << shift) & 0xFFFFFFFFFFFFFFFF
        moves |= current_bb  # Include the last square
        return moves

    def print_board(self):
        piece_symbols = {
            self.WHITE: {
                self.PAWN: 'P', self.KNIGHT: 'N', self.BISHOP: 'B',
                self.ROOK: 'R', self.QUEEN: 'Q', self.KING: 'K'
            },
            self.BLACK: {
                self.PAWN: 'p', self.KNIGHT: 'n', self.BISHOP: 'b',
                self.ROOK: 'r', self.QUEEN: 'q', self.KING: 'k'
            }
        }

        # Iterate over the board and print the pieces
        print("    a b c d e f g h")
        print("  -----------------")
        for row in range(8):
            print(f"{8 - row} |", end="")
            for col in range(8):
                square = chr(ord('a') + col) + str(8 - row)
                piece = self.get_piece_on_square(square)
                if piece is None:
                    print("  ", end="")
                else:
                    player = self.WHITE if self.is_piece_on_square(self.WHITE, square) else self.BLACK
                    print(f" {piece_symbols[player][piece]}", end="")
            print()
        print("  -----------------")

    def load_from_fen(self, fen):
        fen_to_piece = {
            'p': self.PAWN,
            'n': self.KNIGHT,
            'b': self.BISHOP,
            'r': self.ROOK,
            'q': self.QUEEN,
            'k': self.KING
        }

        # Clear the board
        for player in self.piece_bitboards:
            for piece in self.piece_bitboards[player]:
                self.piece_bitboards[player][piece] = self.EMPTY

        # Split the FEN string into sections
        sections = fen.split()

        # Parse the piece positions section
        rank_strings = sections[0].split('/')
        rank_index = 8 - 1
        for rank_string in rank_strings:
            file_index = 0
            for char in rank_string:
                if char.isdigit():
                    file_index += int(char)
                else:
                    player = self.WHITE if char.isupper() else self.BLACK
                    piece = fen_to_piece[char.lower()]
                    square = chr(ord('a') + file_index) + str(rank_index + 1)
                    self.place_piece(player, piece, square)
                    file_index += 1
            rank_index -= 1

        # Parse the active player section
        self.current_player = self.WHITE if sections[1] == 'w' else self.BLACK

        # ... (parse other FEN sections if needed)


    def place_piece(self, player, piece, square):
        player = player.lower()
        piece = piece.lower()
        if square in self.squares:
            self.piece_bitboards[player][piece] |= self.squares[square]


chess = BitboardChess()
fen = 'rnbqkbnr/pppppppp/8/p7/3K4/8/PPPPPPPP/RNBQKBNR w - - 0 1'
chess.load_from_fen(fen)
chess.print_board()
print(chess.get_piece_on_square('b2'))
print(chess.currentPlayer())
chess.make_move('b1','c3')
print(chess.currentPlayer())
chess.make_move('a7','a6')
chess.make_move('c3','d5')
chess.make_move('a5','a4')
chess.make_move('d5','c7')
chess.print_board()
