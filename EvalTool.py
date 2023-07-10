import Main
import evaluate
import alpha_beta

def main_loop(bitboard:Main.BitboardChess, board_fen,depth):
    bitboard.load_from_fen(board_fen)
    checkmate = False
    remi = False
    boards = []
    while not checkmate:
        best_move = alpha_beta.minmax_get_best_move(bitboard,depth)
        bitboard.make_move(best_move[1][0],best_move[1][1])
        bitboard.print_board()
        print("Eval für Spieler: " + chess.current_player)
        print(evaluate.evaluate_board(chess, chess.current_player))
        inp = input(" ")


chess = Main.BitboardChess()
print("TEST EVAL")
fen = 'rnbqkbnr/pppppppp/8/8/8/3p4/PPP1PPPP/RNBQKBNR w - - 0 1'
chess.load_from_fen(fen)
chess.print_board()
print(chess.generate_all_player_moves())
print(alpha_beta.minmax_get_best_move(chess,5))
print(evaluate.evaluate_board(chess,chess.current_player))