
#http://www.codeskulptor.org/#user35_ftDXElTttQ_5.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 200    # Number of trials to run
MCMATCH = 2.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Play the game (board) with random moves started from "player"
    return None
    """
    
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        next_move = empty_squares[random.randrange(len(empty_squares))]
        board.move(next_move[0],next_move[1], player)
        player = provided.switch_player(player)      


def mc_update_scores(scores, board, player):
    """
    Update the scores according to scores grid based on the result board
    """
    winner = board.check_win()
    if winner == provided.DRAW:
        return None
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if winner == player:
                if board.square(row, col) == player:
                    scores[row][col] += MCMATCH
                elif board.square(row, col) != provided.EMPTY:
                    scores[row][col] -= MCOTHER
            else:
                if board.square(row, col) == player:
                    scores[row][col] -= MCMATCH
                elif board.square(row, col) != provided.EMPTY:
                    scores[row][col] += MCOTHER
                    
def get_best_move(board, scores):
    """
    return one of the highest score as (row,col), while board[row][col] is empty
    """
    empty_squares = board.get_empty_squares()
    best_move = []
    max_score = float("-inf")
    for (row, col) in empty_squares:
        score = scores[row][col]
        if score > max_score:
            max_score = score
    for (row, col) in empty_squares:
        if scores[row][col] == max_score:
            best_move.append((row,col))
    return best_move[random.randrange(len(best_move))]


def mc_move(board, player, trials):
    """
    return the best move as (row,col) computed by MC method
    """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]
    for dummy_count in range(trials):
        initial_board = board.clone()
        mc_trial(initial_board, player)
        mc_update_scores(scores, initial_board, player)    
    return get_best_move(board, scores)    

    

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
#mc_update_scores([[0, 0, 0], [0, 0, 0], [0, 0, 0]], provided.TTTBoard(3, False, [[PLAYERX, PLAYERX, PLAYERO], [PLAYERO, PLAYERX, EMPTY], [EMPTY, PLAYERX, PLAYERO]]), 2)
