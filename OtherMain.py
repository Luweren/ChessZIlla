class ChessBoard:
    def __init__(self):
        self.white_pieces = 0
        self.black_pieces = 0
        self.white_king = 0
        self.black_king = 0

    def set_piece(self, piece, position):
        if piece.color == 'white':
            self.white_pieces |= (1 << position)
            if isinstance(piece, King):
                self.white_king |= (1 << position)
        else:
            self.black_pieces |= (1 << position)
            if isinstance(piece, King):
                self.black_king |= (1 << position)

    def get_piece(self, position):
        if self.white_pieces & (1 << position):
            return 'white'
        elif self.black_pieces & (1 << position):
            return 'black'
        else:
            return None

    def is_legal_move(self, piece, start, end):
        if not (0 <= start <= 63) or not (0 <= end <= 63):
            return False

        if piece.color == 'white':
            own_pieces = self.white_pieces
            opponent_pieces = self.black_pieces
            king = self.white_king
        else:
            own_pieces = self.black_pieces
            opponent_pieces = self.white_pieces
            king = self.black_king

        if piece.get_legal_moves(start, own_pieces, opponent_pieces, king) & (1 << end):
            return True

        return False

    def is_in_check(self, color):
        if color == 'white':
            own_king = self.white_king
            opponent_pieces = self.black_pieces
        else:
            own_king = self.black_king
            opponent_pieces = self.white_pieces

        for piece in self.get_all_pieces(color):
            if self.is_legal_move(piece, piece.position, own_king):
                return True

        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for piece in self.get_all_pieces(color):
            for move in piece.get_legal_moves(piece.position, self.white_pieces, self.black_pieces, self.white_king):
                if not self.is_in_check_after_move(piece, move):
                    return False

        return True

    def is_in_check_after_move(self, piece, move):
        start = piece.position
        piece.color = None
        piece.position = move
        self.set_piece(piece, move)
        result = self.is_in_check('white' if piece.color == 'black' else 'black')
        self.clear_piece(move)
        piece.color = 'white' if piece.color == 'black' else 'black'
        piece.position = start
        self.set_piece(piece, start)
        return result

    def clear_piece(self, position):
        self.white_pieces &= ~(1 << position)
        self.black_pieces &= ~(1 << position)
        self.white_king &= ~(1 << position)
        self.black_king &= ~(1 << position)

    def get_all_pieces(self, color):
        if color == 'white':
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces

        all_pieces = []
        for i in range(64):
            if pieces & (1 << i):
                all_pieces.append(self.get_piece_object(i, color))

        return all_pieces


class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        pass


class King(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        for move in [-9, -8, -7, -1, 1, 7, 8, 9]:
            target = position + move
            if 0 <= target <= 63 and not (move == -1 and target % 8 == 7) and not (move == 1 and target % 8 == 0):
                if not own_pieces & (1 << target):
                    legal_moves |= (1 << target)

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves


class Queen(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        for move in [-9, -8, -7, -1, 1, 7, 8, 9]:
            target = position + move
            while 0 <= target <= 63 and not (move == -1 and target % 8 == 7) and not (move == 1 and target % 8 == 0):
                legal_moves |= (1 << target)
                if opponent_pieces & (1 << target):
                    break
                elif own_pieces & (1 << target):
                    legal_moves &= ~((1 << target) - 1)
                    break
                target += move

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves


class Rook(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        for move in [-8, -1, 1, 8]:
            target = position + move
            while 0 <= target <= 63 and not (move == -1 and target % 8 == 7) and not (move == 1 and target % 8 == 0):
                legal_moves |= (1 << target)
                if opponent_pieces & (1 << target):
                    break
                elif own_pieces & (1 << target):
                    legal_moves &= ~((1 << target) - 1)
                    break
                target += move

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves


class Bishop(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        for move in [-9, -7, 7, 9]:
            target = position + move
            while 0 <= target <= 63 and not (move == -1 and target % 8 == 7) and not (move == 1 and target % 8 == 0):
                legal_moves |= (1 << target)
                if opponent_pieces & (1 << target):
                    break
                elif own_pieces & (1 << target):
                    legal_moves &= ~((1 << target) - 1)
                    break
                target += move

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves


class Knight(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        for move in [-17, -15, -10, -6, 6, 10, 15, 17]:
            target = position + move
            if 0 <= target <= 63 and not (move == -6 and target % 8 in [0, 1]) and not (move == 10 and target % 8 in [6, 7]):
                legal_moves |= (1 << target)

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves


class Pawn(Piece):
    def get_legal_moves(self, position, own_pieces, opponent_pieces, king):
        legal_moves = 0
        if self.color == 'white':
            if position % 8 != 0 and opponent_pieces & (1 << (position - 9)):
                legal_moves |= (1 << (position - 9))
            if position % 8 != 7 and opponent_pieces & (1 << (position - 7)):
                legal_moves |= (1 << (position - 7))
            if position % 8 != 7 and not (opponent_pieces | own_pieces) & (1 << (position - 7)) and not (opponent_pieces | own_pieces) & (1 << (position - 8)):
                legal_moves |= (1 << (position - 7))
            if position % 8 != 0 and not (opponent_pieces | own_pieces) & (1 << (position - 9)) and not (opponent_pieces | own_pieces) & (1 << (position - 8)):
                legal_moves |= (1 << (position - 9))
            if position // 8 == 6 and not (opponent_pieces | own_pieces) & (1 << (position - 16)) and not (opponent_pieces | own_pieces) & (1 << (position - 8)):
                legal_moves |= (1 << (position - 16))
        else:
            if position % 8 != 0 and opponent_pieces & (1 << (position + 7)):
                legal_moves |= (1 << (position + 7))
            if position % 8 != 7 and opponent_pieces & (1 << (position + 9)):
                legal_moves |= (1 << (position + 9))
            if position % 8 != 7 and not (opponent_pieces | own_pieces) & (1 << (position + 9)) and not (opponent_pieces | own_pieces) & (1 << (position + 8)):
                legal_moves |= (1 << (position + 9))
            if position % 8 != 0 and not (opponent_pieces | own_pieces) & (1 << (position + 7)) and not (opponent_pieces | own_pieces) & (1 << (position + 8)):
                legal_moves |= (1 << (position + 7))
            if position // 8 == 1 and not (opponent_pieces | own_pieces) & (1 << (position + 16)) and not (opponent_pieces | own_pieces) & (1 << (position + 8)):
                legal_moves |= (1 << (position + 16))

        legal_moves &= ~own_pieces  # Remove own pieces from legal moves
        return legal_moves