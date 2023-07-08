import Main as main
import random


#https://www.chessprogramming.org/Minimax
#https://www.chessprogramming.org/Alpha-Beta

#invocation of alphaBetaMax with initial values can be written in Main.py
def minmax_get_best_move(bitboard:main.BitboardChess, depthleft):

    score = alphaBetaMax((float('-inf'), ('a2','a3')), (float('inf'), ('a7','a6')), depthleft, bitboard)
    return score[1]

def alphaBetaMax(alpha, beta, depthleft, bitboard:main.BitboardChess):
    if depthleft == 0:
        return random.randint(1,10)   #evaluate(bitboard)
    
    moves = bitboard.generate_all_player_moves()
    for move in moves:
        temp_bitboard = bitboard    #hope it works without deepcopy
        bitboard.make_move(move)
        score = alphaBetaMin(alpha, beta, depthleft-1, temp_bitboard)
        #alpha := (alpha_val, alpha_move)
        #beta := (beta_val, beta_move)
        if score[0] >= beta[0]:
            return beta
        if score[0] > alpha[0]:
            alpha = (score[0], move)

    return alpha

def alphaBetaMin(alpha, beta, depthleft, bitboard:main.BitboardChess):
    if depthleft == 0:
        return random.randint(-10,-1)
    
    moves = bitboard.generate_all_player_moves()
    for move in moves:
        temp_bitboard = bitboard       #hope it works without deepcopy
        bitboard.make_move(move)
        score = alphaBetaMax(alpha, beta, depthleft-1, temp_bitboard)
        #alpha := (alpha_val, alpha_move)
        #beta := (beta_val, beta_move)
        if score[0] <= alpha[0]:
            return alpha
        if score[0] < beta[0]:
            beta = (score[0], move)
    return beta
