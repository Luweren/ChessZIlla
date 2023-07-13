import Main as main
import numpy as np

#can we try to compare results while using this approach and another one where we will store
#more general bitboards: bitboard_white_knights = bitboard_white_pieces & bitboard_knights
#it might be faster

A1, B1, C1, D1, E1, F1, G1, H1 = range(8)
A2, B2, C2, D2, E2, F2, G2, H2 = range(8, 16)
A3, B3, C3, D3, E3, F3, G3, H3 = range(16, 24)
A4, B4, C4, D4, E4, F4, G4, H4 = range(24, 32)
A5, B5, C5, D5, E5, F5, G5, H5 = range(32, 40)
A6, B6, C6, D6, E6, F6, G6, H6 = range(40, 48)
A7, B7, C7, D7, E7, F7, G7, H7 = range(48, 56)
A8, B8, C8, D8, E8, F8, G8, H8 = range(56, 64)

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

#our indexing of the chess board is different in this run that is why piece square tables switched collors   so previous early_game_pawn_black is now early_game_pawn_white 
early_game_pawn_white = np.array([
    0,	0,	0,	0,	0,	 0,	0,	0,
    5,	10,	10,	-20,-20,10,	10,	5,
    5,	-5,	-10, 0,	0,  -10,-5,	5,
    0,	0,	0,	20,	20, 0,	0,	0,
    5,	5,	10,	25,	25,	10,	5,	5,
    10,	10,	20,	30,	30,	20,	10,	10,
    50,	50,	50,	50,	50,	50,	50,	50,
    0,	0,	0,	0,	0,	0,	0,	0 
])
early_game_night_white= np.array([
    -50, -40,-30, -30,-30,-30, -40, -50, 
    -40, -20,  0,   5,  5, 0, -20,  -40, 
    -30,   5, 10,  15, 15, 10,  5,  -30, 
    -30,   0, 15,  20, 20, 15,  0,  -30, 
    -30,   5, 15,  20, 20, 15,  5,  -30, 
    -30,   0, 10,  15, 15, 10,  0,  -30, 
    -40, -20,  0,   0,  0,  0, -20, -40, 
    -50, -40,-30, -30,-30,-30, -40, -50 

])

early_game_bishop_white = np.array([
      -20, -10, -10, -10, -10, -10, -10,-20, 
      -10,   5,   0,   0,   0,  0,   5, -10, 
      -10,  10,  10,  10,  10, 10,  10, -10, 
      -10,   0,  10,  10,  10, 10,   0, -10, 
      -10,   5,   5,  10,  10,  5,   5, -10, 
      -10,   0,   5,  10,  10,  5,   0, -10, 
      -10,   0,   0,   0,   0,  0,   0, -10, 
      -20, -10, -10, -10, -10, -10, -10,-20 
])

early_game_rook_white = np.array([
     0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0,-5,
    -5, 0, 0, 0, 0, 0, 0,-5,
    -5, 0, 0, 0, 0, 0, 0,-5,
    -5, 0, 0, 0, 0, 0, 0,-5,
    -5, 0, 0, 0, 0, 0, 0,-5,
    5, 10,10,10,10,10,10, 5,
    0,  0, 0, 0, 0, 0, 0, 0
])

early_game_queen_white = np.array([
-20,-10,-10,-5,-5,-10,-10,-20,  
-10, 0,  0,  0, 0, 5,  0, -10,  
-10, 0,  5,  5, 5, 5,  5, -10,  
-5,  0,  5,  5, 5, 5,  0,  -5,  
-5,  0,  5,  5, 5, 5,  0,  -5,  
-10, 0,  5,  5, 5, 5,  0, -10,  
-10, 0,  0,  0, 0, 0,  0, -10,  
-20,-10,-10,-5,-5,-10,-10,-20 
])

early_game_king_white = np.array([
     20,  30,  10,   0,   0,  10,  30,  20,
     20,  20,   0,   0,   0,   0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
])

mg_pawn_white = np.array([
    0,    0,    0,  0,  0,    0,     0, 0,       
    -22,   38, 24, -15, -23,  -20,  -1, -35,        
    -12,   33, 3,   3,  -10,  -4,   -4, -26,        
    -25,   10, 6,   17,  12,  -5,   -2, -27,        
    -23,   17, 12,  23,  21,   6,   13, -14,        
    -20,   25, 56,  65,  31,   26,  7, -6,       
    -11,   34, 126, 68,  95,   61,  134, 98,        
    0,    0,    0,  0,   0,     0,   0,  0             ])


mg_night_white = np.array([
    -23,     -19,-28, -17, -33,   -58, -21, -105,                 
    -19,    -14, 18,  -1,   -3,   -12, -53, -29,                 
    -16,     25, 17,  19,   10,   12, -9,   -23,                 
    -8,     21,  19,  28,   13,   16, 4,    -13,                 
    22,     18,  69,  37,   53,   19, 17,   -9,                  
    44,     73,  129, 84,   65,   37, 60,   -47,                 
    -17,    7,  62,   23,   36,   72, -41,  -73,                 
    -107, -15,  -97,  61,   -49, -34, -89,  -167                 ])


mg_bishop_white = np.array([
    -21, -39, -12, -13, -21, -14, -3, -33,              
    1, 33, 21, 7, 0, 16, 15, 4,                 
    10, 18, 27, 14, 15, 15, 15, 0,              
    4, 10, 12, 34, 26, 13, 13, -6,              
    -2, 7, 37, 37, 50, 19, 5, -4,               
    -2, 37, 50, 35, 40, 43, 37, -16,                
    -47, 18, 59, 30, -13, -18, 16, -26,                 
    -8, 7, -42, -25, -37, -82, 4, -29              
])



mg_rook_white = np.array([
-26, -37, 7, 16, 17, 1, -13, -19,      
-71, -6, 11, -1, -9, -20, -16, -44,        
-33, -5, 0, 3, -17, -16, -25, -45,     
-23, 6, -7, 9, -1, -12, -26, -36,      
-20, -8, 35, 24, 26, 7, -11, -24,      
16, 61, 45, 17, 36, 26, 19, -5,        
44, 26, 67, 80, 62, 58, 32, 27,        
43, 31, 9, 63, 51, 32, 42, 32   
])


mg_queen_white = np.array([
    -50, -31, -25, -15, 10, -9, -18, -1,                              
    1, -3, 15, 8, 2, 11, -8, -35,                             
    5, 14, 2, -5, -2, -11, 2, -14,                            
    -3, 3, -4, -2, -10, -9, -26, -9,                              
    1, -2, 17, -1, -16, -16, -27, -27,                            
    57, 47, 56, 29, 8, 7, -17, -13,                               
    54, 28, 57, -16, 1, -5, -39, -24,                             
    45, 43, 44, 59, 12, 29, 0, -28                         
])

mg_king_white = np.array([
    14, 24, -28, 8, -54, 12, 36, -15,                           
    8, 9, -16, -43, -64, -8, 7, 1,                          
    -27, -15, -30, -44, -46, -22, -14, -14,                             
    -51, -33, -44, 1000, 1000, -27, -1, -49,                            
    -36, -14, -25, 1000, 1000, -12, -20, -17,                           
    -22, 22, 6, -20, -16, 2, 24, -9,                            
    -29, -38, -4, -8, -7, -20, -1, 29,                          
    13, 2, -34, -56, -15, 16, 23, -65                          
])

early_game_pawn_black = np.array([
    0,  0,  0,  0,  0,  0,  0,  0, 
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
])

early_game_night_black = np.array([
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
])

early_game_bishop_black = np.array([
    -20,-10,-10,-10,-10,-10,-10,-20, 
    -10,  0,  0,  0,  0,  0,  0,-10, 
    -10,  0,  5, 10, 10,  5,  0,-10, 
    -10,  5,  5, 10, 10,  5,  5,-10, 
    -10,  0, 10, 10, 10, 10,  0,-10, 
    -10, 10, 10, 10, 10, 10, 10,-10, 
    -10,  5,  0,  0,  0,  0,  5,-10, 
    -20,-10,-10,-10,-10,-10,-10,-20 
])

early_game_rook_black = np.array([
    0,  0,  0,  0,  0,  0,  0,  0,  
     5, 10, 10, 10, 10, 10, 10,  5, 
    -5,  0,  0,  0,  0,  0,  0, -5, 
    -5,  0,  0,  0,  0,  0,  0, -5, 
    -5,  0,  0,  0,  0,  0,  0, -5, 
    -5,  0,  0,  0,  0,  0,  0, -5, 
    -5,  0,  0,  0,  0,  0,  0, -5, 
     0,  0,  0,  5,  5,  0,  0,  0
])

early_game_queen_black = np.array([
    -20,-10,-10, -5, -5,-10,-10,-20, 
    -10,  0,  0,  0,  0,  0,  0,-10, 
    -10,  0,  5,  5,  5,  5,  0,-10, 
     -5,  0,  5,  5,  5,  5,  0, -5, 
      0,  0,  5,  5,  5,  5,  0, -5, 
    -10,  5,  5,  5,  5,  5,  0,-10, 
    -10,  0,  5,  0,  0,  0,  0,-10, 
    -20,-10,-10, -5, -5,-10,-10,-20
])

early_game_king_black = np.array([
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -20,-30,-30,-40,-40,-30,-30,-20, 
    -10,-20,-20,-20,-20,-20,-20,-10, 
     20, 20,  0,  0,  0,  0, 20, 20, 
     20, 30, 10,  0,  0, 10, 30, 20
])


mg_pawn_black = np.array([ 
    0,   0,   0,   0,   0,   0,  0,   0,        
     98, 134,  61,  95,  68, 126, 34, -11,      
     -6,   7,  26,  31,  65,  56, 25, -20,      
    -14,  13,   6,  21,  23,  12, 17, -23,      
    -27,  -2,  -5,  12,  17,   6, 10, -25,      
    -26,  -4,  -4, -10,   3,   3, 33, -12,      
    -35,  -1, -20, -23, -15,  24, 38, -22,      
      0,   0,   0,   0,   0,   0,  0,   0          ])


mg_night_black = np.array([
    -167, -89, -34, -49,  61, -97, -15, -107,               
     -73, -41,  72,  36,  23,  62,   7,  -17,               
     -47,  60,  37,  65,  84, 129,  73,   44,               
      -9,  17,  19,  53,  37,  69,  18,   22,               
     -13,   4,  16,  13,  28,  19,  21,   -8,               
     -23,  -9,  12,  10,  19,  17,  25,  -16,               
     -29, -53, -12,  -3,  -1,  18, -14,  -19,               
    -105, -21, -58, -33, -17, -28, -19,  -23               ])

mg_bishop_black = np.array([
    -29,   4, -82, -37, -25, -42,   7,  -8, 
    -26,  16, -18, -13,  30,  59,  18, -47, 
    -16,  37,  43,  40,  35,  50,  37,  -2, 
     -4,   5,  19,  50,  37,  37,   7,  -2, 
     -6,  13,  13,  26,  34,  12,  10,   4, 
      0,  15,  15,  15,  14,  27,  18,  10, 
      4,  15,  16,   0,   7,  21,  33,   1, 
    -33,  -3, -14, -21, -13, -12, -39, -21
])

mg_rook_black = np.array([
     32,  42,  32,  51, 63,  9,  31,  43,       
     27,  32,  58,  62, 80, 67,  26,  44,       
     -5,  19,  26,  36, 17, 45,  61,  16,       
    -24, -11,   7,  26, 24, 35,  -8, -20,       
    -36, -26, -12,  -1,  9, -7,   6, -23,       
    -45, -25, -16, -17,  3,  0,  -5, -33,       
    -44, -16, -20,  -9, -1, 11,  -6, -71,       
    -19, -13,   1,  17, 16,  7, -37, -26     
])

mg_queen_black = np.array([
    -28,   0,  29,  12,  59,  44,  43,  45,              
    -24, -39,  -5,   1, -16,  57,  28,  54,              
    -13, -17,   7,   8,  29,  56,  47,  57,              
    -27, -27, -16, -16,  -1,  17,  -2,   1,              
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,              
    -14,   2, -11,  -2,  -5,   2,  14,   5,              
    -35,  -8,  11,   2,   8,  15,  -3,   1,              
     -1, -18,  -9,  10, -15, -25, -31, -50              
])    


mg_king_black = np.array([
    -65,  23,  16, -15, -56, -34,   2,    13, 
     29,  -1, -20,  -7,  -8,  -4, -38,   -29, 
     -9,  24,   2, -16, -20,   6,  22,   -22, 
    -17, -20, -12, 1000,  1000, -25, -14,-36, 
    -49,  -1, -27, 1000, 1000, -44, -33, -51, 
    -14, -14, -22, -46, -44, -30, -15,   -27, 
      1,   7,  -8, -64, -43, -16,   9,    8,  
    -15,  36,  12, -54,   8, -28,  24,    14
])

eg_tables_white = {
    'pawn'  : early_game_pawn_white,
    'knight': early_game_night_white,
    'bishop': early_game_bishop_white,
    'rook'  : early_game_rook_white,
    'queen' : early_game_queen_white,
    'king'  : early_game_king_white}

eg_tables_black = {
    'pawn'   : early_game_pawn_black,
    'knight' : early_game_night_black,
    'bishop' : early_game_bishop_black,
    'rook'   : early_game_rook_black,
    'queen'  : early_game_queen_black,
    'king'   : early_game_king_black}

mg_tables_white = {
    'pawn'  : mg_pawn_white,
    'knight': mg_night_white,
    'bishop': mg_bishop_white,
    'rook'  : mg_rook_white,
    'queen' : mg_queen_white,
    'king'  : mg_king_white}

mg_tables_black = {
    'pawn'   : mg_pawn_black,
    'knight' : mg_night_black,
    'bishop' : mg_bishop_black,
    'rook'   : mg_rook_black,
    'queen'  : mg_queen_black,
    'king'   : mg_king_black}


def evaluate_board(bitboard: main.BitboardChess,player):
    return evaluate_position(bitboard,player) + evaluate_material(bitboard,player)



def get_square_table(player):   #needs to be extended with mg_tables
    if player == 'white':
        return eg_tables_white
    elif player == 'black':
        return eg_tables_black

def evaluate_position(bb_for_position:main.BitboardChess, player):
    pos_value = 0
    side = 0
    if player == 'white':
        side = 1
    if player == 'black':
        side =-1 

    bitboards_of_current_pieces =bb_for_position.piece_bitboards["white"]
    for piece in bitboards_of_current_pieces:
        piece_squares = bb_for_position.get_piece_squares_according_to_player(piece,'white')
        added_pos_value = evaluate_position_of_a_piece_art(piece_squares, get_square_table('white')[piece])  
        pos_value += added_pos_value
    
    bitboards_of_oponent_pieces  = bb_for_position.piece_bitboards["black"] 
    for piece in bitboards_of_oponent_pieces:
        piece_squares_black = bb_for_position.get_piece_squares_according_to_player(piece,"black")
        added_black_pos_value = evaluate_position_of_a_piece_art(piece_squares_black, get_square_table('black')[piece])  
        pos_value -= added_black_pos_value

    return pos_value*side

def evaluate_position_of_a_piece_art(pieces, piece_square_table):
    evaluation = 0
    #example of pieces: ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
    if not pieces:
        return 0
    
    for piece in pieces:
        index = int(np.log2(squares[piece]))
        evaluation += piece_square_table[index]

    return evaluation


def evaluate_position1(bb_for_position:main.BitboardChess, player):     #old version
    pos_value = 0
    side = 0
    if player == 'white':
        side = 1
    if player == 'black':
        side =-1 

    bitboards_of_current_pieces =bb_for_position.piece_bitboards["white"]
    for piece in bitboards_of_current_pieces:
        pos_value += evaluate_position_of_a_piece_art(bitboards_of_current_pieces[piece], get_square_table('white')[piece])  
    
    bitboards_of_oponent_pieces  = bb_for_position.piece_bitboards["black"] 
    for piece in bitboards_of_oponent_pieces:
        pos_value -= evaluate_position_of_a_piece_art(bitboards_of_oponent_pieces[piece], get_square_table('black')[piece])  

    return pos_value*side





def evaluate_position_of_a_piece_art1(pieces, piece_square_table):
    evaluation = 0
    while pieces != 0:
        square = pieces & -pieces  # Get the least significant set bit         #having pieces = 0b1010 and applying & -pieces => we will get square = 0b10  => the next stored piece in the bitboard
        #index = bin(square).count('0') - 1          #another way to calculate index. I do not think that it is faster
        index = 0
        while square & 1 == 0:
            square >>= 1
            index += 1
        evaluation += piece_square_table[index]
        pieces &= pieces - 1  # Clear the least significant set bit      #pieces = 0b1010;   pieces -1 == 0b1001;    pieces & pieces -1 == 0b1000

    return evaluation

#material_value of starting position equals to 14000 = 8*100 + 2*320 + 2*330 + 2*500 + 900 +10 000
piece_values = {'pawn':100, 'knight':320, 'bishop':330, 'rook':500, 'queen':900, 'king':10000}

def evaluate_material(bb_material:main.BitboardChess, player):
    material_value = 0
    side = 0
    if player == 'white':
        side = 1
    if player == 'black':
        side =-1 
    for piece in bb_material.piece_bitboards[bb_material.current_player]:
        times = bb_material.piece_bitboards[bb_material.current_player][piece].bit_count()
        material_value += piece_values[piece]*times

    oponent = bb_material.get_opponent(bb_material.current_player)
    for piece in bb_material.piece_bitboards[oponent]:
        times = bb_material.piece_bitboards[oponent][piece].bit_count()
        material_value -= piece_values[piece]*times
    return material_value * side