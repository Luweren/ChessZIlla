import evaluate
import Main as main
import pickle
import copy
#https://www.chessprogramming.org/Minimax
#https://www.chessprogramming.org/Alpha-Beta

tree_size = 0

#invocation of alphaBetaMax with initial values can be written in Main.py
def minmax_get_best_move(bitboard:main.BitboardChess, depthleft):

    score = alphaBetaMax((float('-inf'), ('a2','a3')), (float('inf'), ('a7','a6')), depthleft, bitboard)
    return score, tree_size

def alphaBetaMax(alpha, beta, depthleft, bitboard:main.BitboardChess):
    global tree_size

    if depthleft == 0:
        tree_size += 1
        return (evaluate.evaluate_board(bitboard,'white'),alpha[1])  #'white' should be changed to a player that will be defined and given to the alphaBetaMax in the playing game function
    boardcopy = pickle.dumps(bitboard)
    moves = bitboard.generate_all_player_moves()

    for move in moves:
        temp_bitboard = pickle.loads(boardcopy)    #hope it works without deepcopy

        if not temp_bitboard.make_move(move[0], move[1]):
            continue

        score = alphaBetaMin(alpha, beta, depthleft-1, temp_bitboard)
        #alpha := (alpha_eval, alpha_move)
        #beta := (beta_eval, beta_move)
        if score[0] >= beta[0]:
            return (beta[0], beta[1])   #previously just return beta
        if score[0] > alpha[0]:
            alpha = (score[0], (move[0],move[1]))

    return (alpha[0],alpha[1])

def alphaBetaMin(alpha, beta, depthleft, bitboard:main.BitboardChess):
    global tree_size

    if depthleft == 0:
        tree_size += 1
        return (evaluate.evaluate_board(bitboard,'white'), beta[1])
    
    boardcopy = pickle.dumps(bitboard)
    moves = bitboard.generate_all_player_moves()

    for move in moves:
        temp_bitboard = pickle.loads(boardcopy)       #hope it works without deepcopy

        if not temp_bitboard.make_move(move[0], move[1]):
            continue

        score = alphaBetaMax(alpha, beta, depthleft-1, temp_bitboard)
        #alpha := (alpha_eval, alpha_move)
        #beta := (beta_eval, beta_move)

        if score[0] <= alpha[0]:
            return (alpha[0],alpha[1])
        if score[0] < beta[0]:
            beta = (score[0], (move[0], move[1]))
    return (beta[0],beta[1])
