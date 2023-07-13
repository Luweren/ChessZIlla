import pickle


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
        self.king_check = False

    def get_king_check(self):
        self.king_check = True
        
        moves = self.generate_all_opponent_moves()

        #print(moves)

        for move in moves:
            if self.get_square_name(self.piece_bitboards[self.current_player][self.KING]) == move[1]:
                print(self.get_square_name(self.piece_bitboards[self.current_player][self.KING]), move[1])
                return 1
        return 0

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

        # Make the move
        self.move_piece(piece, from_square, to_square)

        # Check for capturing
        if self.is_piece_on_square(opponent, to_square):
            self.capture_piece(opponent, to_square)

        #self.print_board()

        #check for check after move
        if self.get_king_check():
            print("CHECK")
            return 0

        # Switch players
        self.current_player = opponent

        return 1

    def move_piece(self, piece, from_square, to_square):
        from_bb = self.piece_bitboards[self.current_player][piece]
        to_bb = self.squares[to_square]
        self.piece_bitboards[self.current_player][piece] = from_bb & ~self.squares[from_square] | to_bb

    def capture_piece(self, opponent, square):
        for piece in self.piece_bitboards[opponent]:
            if self.is_piece_on_square(opponent, square):
                self.piece_bitboards[opponent][piece] &= ~self.squares[square]
                break

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
        print("    a b c d e f g h")


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

    def attacked_square(self, move):
        return move[1]

    def generate_king_moves(self, square, player):
        if isinstance(square, str):
            square = self.squares[square]
        
        moves = []
        # Define the king's possible move directions (right, left, up, down, up-left, down-right, up-right, down-left)
        directions = [(1), (-1), (8), (-8), (7), (-7), (9), (-9)]

        for direction in directions:
            from_square = square

            #dest_square = shift(dest_square, direction)
            from_square_char = self.get_square_name(from_square)

            if from_square_char[0] == 'a' and ((direction == -1) or (direction ==+7) or (direction == -9)):
                continue

            if from_square_char[0] == 'h' and ((direction == 1) or (direction ==-7) or (direction == 9)):
                continue

            if from_square_char[1] == '1' and ((direction == -9 ) or (direction == -8) or (direction==-7)):
                continue

            if from_square_char[1] == '8' and ((direction == 7 ) or (direction == 8) or (direction==9)):
                continue
            
            dest_square = shift(from_square, direction)
            dest_square_char = self.get_square_name(dest_square)
            if dest_square_char is None:
                continue
            if self.is_piece_on_square(self.current_player, dest_square_char):
                continue


            moves.append((self.get_square_name(square), dest_square_char))

            # Check for castling moves
        if player:
            if self.can_castle_kingside(self.current_player):
                kingside_dest = self.squares['g1'] if self.current_player == self.WHITE else self.squares['g8']


                moves.append((self.get_square_name(square), self.get_square_name(kingside_dest)))

            if self.can_castle_queenside(self.current_player):
                queenside_dest = self.squares['c1'] if self.current_player == self.WHITE else self.squares['c8']


                moves.append((self.get_square_name(square), self.get_square_name(queenside_dest)))

        return moves

    def can_castle_kingside(self, player):
        # Check if the king and the kingside rook are in their initial positions
        king_start_square = 'e1' if player == self.WHITE else 'e8'
        rook_start_square = 'h1' if player == self.WHITE else 'h8'
        if self.get_piece_on_square(king_start_square) != self.KING or self.get_piece_on_square(
                rook_start_square) != self.ROOK:
            return False

        # Check if there are no pieces between the king and the rook
        squares_between = ['f1', 'g1'] if player == self.WHITE else ['f8', 'g8']
        if any(self.get_piece_on_square(square) is not None for square in squares_between):
            return False

        # Check if the king is not in check and does not pass through attacked squares
        squares_attacked = ['f1', 'g1'] if player == self.WHITE else ['f8','g8']

        for move in self.generate_all_opponent_moves():
            if self.attacked_square(move) in squares_attacked:
                return False

        # All conditions are satisfied, castling is allowed
        return True

    def can_castle_queenside(self, player):
        # Check if the king and the queenside rook are in their initial positions
        king_start_square = 'e1' if player == self.WHITE else 'e8'
        rook_start_square = 'a1' if player == self.WHITE else 'a8'
        if self.get_piece_on_square(king_start_square) != self.KING or self.get_piece_on_square(
                rook_start_square) != self.ROOK:
            return False

        # Check if there are no pieces between the king and the rook
        squares_between = ['b1', 'c1', 'd1'] if player == self.WHITE else [
           'b8','c8','d8']
        if any(self.get_piece_on_square(square) is not None for square in squares_between):
            return False

        # Check if the king is not in check and does not pass through attacked squares
        squares_attacked = ['c1','d1'] if player == self.WHITE else [
           'c8', 'd8']

        for move in self.generate_all_opponent_moves():
            if self.attacked_square(move) in squares_attacked:
                return False


        # All conditions are satisfied, castling is allowed
        return True

    def generate_knight_moves(self, square):
        if isinstance(square, str):
            square = self.squares[square]
        
        moves = []

        directions = [(6), (10), (-10), (-6), (15), (17), (-17), (-15)]

        for direction in directions:
            from_square = square
            from_square_char = self.get_square_name(from_square)

            if from_square_char[0] == 'a' and ((direction == -17) or (direction == -10) or (direction == 6) or (direction == 15)):
                continue
            
            if from_square_char[0] == 'b' and ((direction ==-10) or (direction == 6)):
                continue

            if from_square_char[0] == 'h' and ((direction ==-15) or (direction == -6) or (direction == 10) or (direction == 17)):
                continue
            
            if from_square_char[0] == 'g' and ((direction == -6) or (direction == 10)):
                continue

            if from_square_char[1] == '1' and ((direction == -10) or (direction == -17) or (direction == -15) or (direction ==-6)):
                continue

            if from_square_char[1] == '2' and ((direction == -17) or (direction == -15)):
                continue

            if from_square_char[1] == '8' and ((direction == 6) or (direction == 15) or (direction ==17) or (direction == 10)):
                continue

            if from_square_char[1] == '7' and ((direction == 15) or (direction == 17)):
                continue

            dest_square = shift(from_square, direction)
            dest_square_char = self.get_square_name(dest_square)
            if dest_square_char is None:
                continue
            if self.is_piece_on_square(self.current_player, dest_square_char):
                continue


            moves.append((self.get_square_name(square), dest_square_char))

        return moves

    def generate_pawn_moves(self, square):
        if isinstance(square, str):
            # Convert the square from string to integer representation
            square = self.squares[square]

        moves = []

        if self.current_player == self.WHITE:
            directions = [(8), (16), (7), (9)]
        else:
            directions = [(-8), (-16), (-7), (-9)]
        
        for direction in directions:
            from_square = square
            from_square_char = self.get_square_name(from_square)


            #checking edges of the board
            if from_square_char[0] == 'a' and ((direction == 7) or (direction == -9)):
                continue

            if from_square_char[0] == 'h' and ((direction == 9) or (direction == -7)):
                continue

            dest_square = shift(from_square, direction)
            dest_square_char = self.get_square_name(dest_square)
            if dest_square_char is None:
                continue
            #vertical movement
            #while we go vertical on the board we always check the square in front of us
            if direction == 8 or direction == 16 or direction == -8 or direction == -16:  # if direction % 8 == 0: 
                if direction < 0:
                    help_dest_square = shift(from_square, -8)
                else: 
                    help_dest_square = shift(from_square, 8)
                
                help_dest_square_char = self.get_square_name(help_dest_square)
    
                if self.is_piece_on_square(self.current_player, help_dest_square_char):
                    continue
                if self.is_piece_on_square(self.get_opponent(self.current_player), help_dest_square_char):
                    continue

            if not (from_square_char[1] == '2' or from_square_char[1] == '7') and (direction == 16 or direction == -16):
                continue

            if (from_square_char[1] == '2' and direction == 16)  or (from_square_char[1] == '7' and direction == -16):
                #the piece can go up two squares only if there is no pieces
                if self.is_piece_on_square(self.current_player, dest_square_char):
                    continue
                if self.is_piece_on_square(self.get_opponent(self.current_player), dest_square_char):
                    continue
            #diagonal movement
            #if direction is diagonal and there is no enemie piece on the dest_square then skip
            if not self.is_piece_on_square(self.get_opponent(self.current_player), dest_square_char) and (direction == 7 or direction == 9 or direction == -7 or direction == -9):
                continue

            moves.append((self.get_square_name(square), dest_square_char))


        return moves
    
    def generate_rook_moves(self, square):
        if isinstance(square, str):
            # Convert the square from string to integer representation
            square = self.squares[square]

        from_square_char = self.get_square_name(square)
        moves = []

        # Define the rook's possible move directions (up, down, left, right)
        directions = [(1), (-1), (8), (-8)]

        for direction in directions:
            dest_square = square
            
            if from_square_char[0] == 'a' and direction == -1:
                continue  # Reached the left edge of the board, cannot move further
            if from_square_char[0] == 'h' and direction == 1:
                continue  # Reached the right edge of the board
            if from_square_char[1] == '1' and direction == -8:
                continue  # Reached the bottom edge of the board
            if from_square_char[1] == '8' and direction == 8:
                continue  # Reached the top edge of the board
                
            while True:
                dest_square = shift(dest_square, direction)
                dest_square_char = self.get_square_name(dest_square)
                if dest_square_char is None:
                    break

                if self.is_piece_on_square(self.current_player, dest_square_char):
                    break  # Reached own piece, cannot move further

                moves.append((self.get_square_name(square), dest_square_char))

                if dest_square_char[0] == 'a' and direction == -1:
                    break  # Reached the left edge of the board, cannot move further

                if dest_square_char[0] == 'h' and direction == 1:
                    break  # Reached the right edge of the board

                if dest_square_char[1] == '1' and direction == -8:
                    break  # Reached the bottom edge of the board

                if dest_square_char[1] == '8' and direction == 8:
                    break  # Reached the top edge of the board

                if self.is_piece_on_square(self.get_opponent(self.current_player), dest_square_char):
                    break  # Reached opponent's piece, can capture and stop moving

        return moves


    def generate_bishop_moves(self, square):   # generate only legal moves from this square
        if isinstance(square, str):
            # Convert the square from string to integer representation
            square = self.squares[square]

        from_square_char = self.get_square_name(square)
        moves = []

        # Define the bishop's possible move directions (up, down, left, right)
        directions = [(7), (-7), (9), (-9)]

        for direction in directions:
            dest_square = square
            if from_square_char[0] == 'a' and (direction == 7 or direction == -9):
                continue  # Reached the left edge of the board

            if from_square_char[0] == 'h' and (direction == -7 or direction == 9):
                continue  # Reached the right edge of the board

            if from_square_char[1] == '1' and (direction == -7 or direction == -9):
                continue  # Reached the bottom edge of the board

            if from_square_char[1] == '8' and (direction == 7 or direction == 9):
                continue  # Reached the top edge of the board   

            while True:
                dest_square = shift(dest_square, direction)
                dest_square_char = self.get_square_name(dest_square)
                if dest_square_char is None:
                    break

                if self.is_piece_on_square(self.current_player, dest_square_char):
                    break  # Reached own piece, cannot move further
                moves.append((self.get_square_name(square), dest_square_char))
                if dest_square_char[0] == 'a' and (direction == 7 or direction == -9):
                    break  # Reached the left edge of the board

                if dest_square_char[0] == 'h' and (direction == -7 or direction == 9):
                    break  # Reached the right edge of the board

                if dest_square_char[1] == '1' and (direction == -7 or direction == -9):
                    break  # Reached the bottom edge of the board

                if dest_square_char[1] == '8' and (direction == 7 or direction == 9):
                    break  # Reached the top edge of the board                
                if self.is_piece_on_square(self.get_opponent(self.current_player), dest_square_char):
                    break  # Reached opponent's piece, can capture and stop moving

        return moves

    def generate_queen_moves(self, square):
        moves = []
        moves += self.generate_bishop_moves(square)
        moves += self.generate_rook_moves(square)
        return moves

    def get_square_name(self, square):
        for name, value in self.squares.items():
            if square & value:
                return name

        return None  # Square not found

    def get_opponent(self, color):
        if color == self.WHITE:
            return self.BLACK
        elif color == self.BLACK:
            return self.WHITE
        else:
            raise ValueError("Invalid color value.")

    def generate_all_player_moves(self):
        moves = []
        for piece in self.piece_bitboards[self.current_player]:
            if piece == self.EMPTY:
                continue
            piece_moves = self.generate_piece_moves(piece, True)
            moves += piece_moves
        return moves
    def generate_all_opponent_moves(self):
        self.current_player = self.get_opponent(self.current_player )
        moves = []
        for piece in self.piece_bitboards[self.current_player]:
            if piece == self.EMPTY:
                continue
            piece_moves = self.generate_piece_moves(piece, False)
            moves += piece_moves
        self.current_player = self.get_opponent(self.current_player )
        return moves

    def generate_piece_moves(self, piece, player):
        squares = self.get_piece_squares(piece)
        moves = []
        if piece == self.PAWN:
            for square in squares:
                moves += self.generate_pawn_moves(square)
            return moves
        elif piece == self.KNIGHT:
            for square in squares:
                moves += self.generate_knight_moves(square)
            return moves
        elif piece == self.BISHOP:
            for square in squares:
                moves += self.generate_bishop_moves(square)
            return moves
        elif piece == self.ROOK:
            for square in squares:
                moves += self.generate_rook_moves(square)
            return moves
        elif piece == self.QUEEN:
            for square in squares:
                moves += self.generate_queen_moves(square)
            return moves
        elif piece == self.KING:
            for square in squares:
                moves += self.generate_king_moves(square, player)
            return moves

    def get_piece_squares(self, piece):
        squares = []
        bitboard = self.piece_bitboards[self.current_player][piece]
        for square in self.squares:
            if bitboard & self.squares[square] != 0:
                squares.append(square)
        return squares

    def get_piece_squares_according_to_player(self, piece, player):
        squares = []
        bitboard = self.piece_bitboards[player][piece]
        for square in self.squares:
            if bitboard & self.squares[square] != 0:
                squares.append(square)
        return squares

chess = BitboardChess()
fen = '8/8/8/8/8/8/8/K2b4 w - - 0 1'
fen2 = '8/8/8/8/8/8/b7/Kb6 w - - 0 1'
start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
chess.load_from_fen(start)
#chess.print_board()