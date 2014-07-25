"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_provided as provided



# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #print board
    empty_squares = board.get_empty_squares()
    all_moves = []        
    for square in empty_squares:
        tmp_board = board.clone()
        tmp_board.move(square[0], square[1], player)
        result =  tmp_board.check_win()
        if result != None:
            return (SCORES[result], square)
        next_player = provided.switch_player(player)
        move = mm_move(tmp_board, next_player)
        if move[0]*SCORES[player] == 1:
            return (move[0],square)
        all_moves.append((move[0],square))
    max_score = max(move[0]*SCORES[player] for move in all_moves)
    for move in all_moves:
        if move[0]*SCORES[player] == max_score:
            return move
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False) 
#print (SCORES[4])
#b = [[2,3,2],[3,2,1],[3,1,1]]
#board = provided.TTTBoard(3,board = b)
#print mm_move(board, 3)
