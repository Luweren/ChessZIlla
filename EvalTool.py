import Main
import evaluate
import alpha_beta
import monte_carlo

def main_loop(bitboard:Main.BitboardChess, board_fen,depth):
    bitboard.load_from_fen(board_fen)
    checkmate = False
    remi = False
    boards = []
    while not checkmate:
        best_move = alpha_beta.minmax_get_best_move(bitboard,depth)
        bitboard.make_move(best_move[1][0],best_move[1][1])
        bitboard.print_board()
        print("Eval für Spieler: " + bitboard.current_player)
        print(evaluate.evaluate_board(bitboard, bitboard.current_player))
        inp = input(" ")


chess = Main.BitboardChess()
print("TEST EVAL")
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1'
chess.load_from_fen(fen)
chess.print_board()
print(chess.generate_all_player_moves())
print(monte_carlo.mcts(chess,0,chess.current_player))

