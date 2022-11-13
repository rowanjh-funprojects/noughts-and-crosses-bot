"""
Tic Tac Toe Player
"""

from cmath import inf
import math
import copy

X = "X"
O = "O"
EMPTY = None

def count_board(board):
    x = 0
    o = 0
    for row in board:
        for element in row:
            if element == "X":
                x += 1
            elif element == "O":
                o += 1
    return x, o


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count number of X's and O's on the board
    x, o = count_board(board)
    if x > o:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_available = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == None:
                actions_available.append((row,col))
    return actions_available


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception()
    resultingboard = copy.deepcopy(board)
    resultingboard[action[0]][action[1]] = player(board)
    return resultingboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if utility(board) != 0:
        x, o = count_board(board)
        if x > o:
            return "X"
        elif o == x:
            return "O"
        else:
            return None
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if utility(board) != 0:
        return True
    if None in [j for i in board for j in i]:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (board[0][0] == board[1][1] == board[2][2] != None) or \
        (board[0][1] == board[1][1] == board[2][1]!= None) or \
        (board[1][0] == board[1][1] == board[1][2]!= None) or \
        (board[0][2] == board[1][1] == board[2][0]!= None) or \
        (board[0][0] == board[0][1] == board[0][2]!= None) or \
        (board[2][0] == board[2][1] == board[2][2]!= None) or \
        (board[0][0] == board[1][0] == board[2][0]!= None) or \
        (board[0][2] == board[1][2] == board[2][2]!= None):
        # I there is a winner, decide who won
        # If X just played a winning move, player(board) will switch to O,
        # and then the victory condition is checked
        if player(board) == "X":
            return -1 # O just played the winning move
        elif player(board) == "O":
            return 1 # X just played the winning move
    else:
        # if no winner
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """ 
    # If player is X, maximise, if player is O, minimise
    # Start with actions available and choose the best
    if terminal(board):
        return None
    values = []
    actions_available = actions(board)
    if player(board) == "X":
        for action in actions_available:
            this_action_value = MINVALUE(result(board, action), -math.inf, math.inf)
            values.append(this_action_value)
        return choose_action(actions_available, values, max(values))
    else:
        for action in actions_available:
            this_action_value = MAXVALUE(result(board, action), -math.inf, math.inf)
            values.append(this_action_value)
        return choose_action(actions_available, values, min(values))


def MAXVALUE(state, alpha, beta):
    # Return the highest possible value of a given board state,
    # assuming that the opponent will play optimally
    # Alpha keeps track of the max player's current best move. Beta tracks the min player's current best move.
    # Alpha: The max player uses alpha. If the max player encounters a branch where the 
    #       min player's optimal moves result in max getting a low score 
    if terminal(state):
        return utility(state)
    else:
        maxV = -math.inf
        for action in actions(state):
            thisv = MINVALUE(result(state, action), alpha, beta)
            maxV = max(maxV, thisv)
            alpha = max(alpha, maxV)
            if beta <= alpha:  
                break
        return maxV


def MINVALUE(state, alpha, beta):
    # Return the lowest possible value of a given board state,
    # assuming that the opponent will play optimally
    # Beta keeps track of the current best minimum
    if terminal(state):
        return utility(state)
    else:
        minV = math.inf
        for action in actions(state):
            thisv = MAXVALUE(result(state, action), alpha, beta)
            minV = min(minV, thisv)
            beta = min(beta, minV)
            if beta <= alpha:
                break
        return minV


def choose_action(list, vals, target):
    ## Go over a list, and return the index of the first value that matches
    for i in range(len(vals)):
        if vals[i] == target:
            return list[i]
