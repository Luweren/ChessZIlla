import Main
import evaluate
import alpha_beta

chess = Main.BitboardChess()
print("TEST EVAL")
chess.print_board()
print(alpha_beta.minmax_get_best_move(chess,3))
print(evaluate.evaluate_board(chess, 'white'))