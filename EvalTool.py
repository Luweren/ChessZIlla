import Main
import evaluate
import alpha_beta

chess = Main.BitboardChess()
print("TEST EVAL")
chess.print_board()

shannon = [20, 400, 8902, 197281, 4865609]

for i in range(5):
    score, tree_size = alpha_beta.minmax_get_best_move(chess, i + 1)

    print("Depth: " + str(i + 1))
    print("Real number: " + str(shannon[i]))
    print("Our number: " + str(tree_size))
    print("Diff: " + str(shannon[i] - tree_size) + "\n\n")