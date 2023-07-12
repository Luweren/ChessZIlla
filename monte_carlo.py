import Main as main
import random
import time
from math import log,sqrt,e,inf
import pickle

class node():
    def __init__(self):
        self.state = main.BitboardChess()
        self.action = ''                        #????????????
        self.children = set()
        self.parent = None
        self.N = 0
        self.n = 0
        self.v = 0

def ucb1(curr_node):
    value = curr_node.v + 2*(sqrt(log(curr_node.N +e+(10**-6))/(curr_node.n+(10**-10))))   #compare it to the original formula
    return value

def rollout(curr_node):
    #if(curr_node.state)     ## check the original code
    if(curr_node.state.is_game_over()):
        return(1,curr_node)    # instead of 1 evaluate.evaluate_board(curr_node.state)
    all_moves = curr_node.state.generate_all_player_moves()
    copy_state = pickle.dumps(curr_node.state)
    for move in all_moves:
        tmp_state = pickle.loads(copy_state)
        tmp_state.make_move(move[0],move[1])
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    rnd_state = random.choice(list(curr_node.children))
    return rollout(rnd_state)  # does not work, because we do not play till the end

def expand(curr_node:node, color):
    if(len(curr_node.children)==0):
        return curr_node
    max_ucb = -inf
    if(color == 'white'):     
        idx = -1
        max_ucb = -inf
        sel_child = None
        for child in curr_node.children:
            tmp = ucb1(child)
            if tmp>max_ucb:
                idx = child
                max_ucb = tmp
                sel_child = child    #why do we need idx and sel_child? aren't they redundant?

        return expand(sel_child,"black")

    else:
        idx = -1
        min_ucb = inf
        sel_child = None
        for child in curr_node.children:
            tmp = ucb1(child)
            if tmp < min_ucb:
                idx = child
                min_ucb =tmp
                sel_child = child
        
        return expand(sel_child, "white")
    
def rollback(curr_node, reward):
    curr_node.n += 1
    curr_node.v += reward
    while curr_node.parent != None:
        curr_node.N += 1
        curr_node = curr_node.parent
    return curr_node


def mcts(curr_node:node, over, color, iterations=10):

    if over:
        return -1
    all_moves = curr_node.state.generate_all_player_moves
    map_state_move = dict()

    copy_state = pickle.dumps(curr_node.state)
    for move in all_moves:
        tmp_state = pickle.loads(copy_state)
        tmp_state.make_move(move[0], move[1])   #why does it not autocomplete while i am writing make_move() does it not recognize tmp_state as BitboardChess?
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = move

    while iterations > 0:
        if color == "white":
            idx = -1
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if tmp > max_ucb:
                    idx = i
                    max_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child,"black")
            reward, state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations -=1
        else:
            idx = -1
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if tmp < min_ucb:
                    idx = i
                    min_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child,"white")
            reward, state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations -= 1
    if(color == "white"):
        mx = -inf
        idx = -1
        selcted_move = ''
        for k in curr_node.children:
            tmp = ucb1(k)
            if tmp > mx:
                mx = tmp
                selcted_move = map_state_move[i]
        return selcted_move
    
    #continue from 160th line of the original code in github
            


            
