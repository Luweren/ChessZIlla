import Main
import evaluate
import alpha_beta
import time

chess = Main.BitboardChess()

import monte_carlo


def main_loop(bitboard:Main.BitboardChess, board_fen,depth):
    bitboard.load_from_fen(board_fen)

    remi = False
    boards = []
    while not bitboard.game_over():
        #

        best_move = monte_carlo.mcts(bitboard,bitboard.game_over(),bitboard.current_player,15)
        if best_move is None:
            best_move = alpha_beta.minmax_get_best_move(bitboard, depth)
            best_move = best_move[0][1]
        print(best_move)
        bitboard.make_move(best_move[0],best_move[1])
        bitboard.print_board()
        print("Eval für Spieler: " + bitboard.current_player)
        print(evaluate.evaluate_board(bitboard, bitboard.current_player))
        #inp = input(" ")


fen = '8/8/8/8/8/8/8/K2b4 w - - 0 1'
fen2 = '8/8/8/8/8/8/b7/Kb6 w - - 0 1'
start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
chess.load_from_fen(start)

chess.print_board()

shannon = [20, 400, 8902, 197281, 4865609]\

#chess.make_move('a1', 'a2')
#print(monte_carlo.mcts(chess,0,chess.current_player,10))
main_loop(chess,start,3)
"""
for i in range(5):
    inp = input("")
    timer = time.time()

    score, tree_size = alpha_beta.minmax_get_best_move(chess, 2)
    chess.make_move(score[1][0], score[1][1])

    print("Best move:", score[1])
    print("Time:" + str(time.time() - timer))

    chess.print_board()
"""
