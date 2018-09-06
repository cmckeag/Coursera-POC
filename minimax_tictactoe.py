"""
Mini-max Tic-Tac-Toe Player

Uses recursive depth first search logic to evaluate every possible
tic tac toe board from the current position, and pick one that is most likely
to lead to a win/not a lose.
Modules are not present so can't actually run but the recursive mm_move() function works.
"""
import random
#import poc_ttt_gui
#import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
#import codeskulptor
#codeskulptor.set_timeout(60)

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
    winner = board.check_win()
    if winner is not None:
        return SCORES[winner], (-1,-1)
    moves_and_scores = {}
    for move in board.get_empty_squares():
        new_board = board.clone()
        new_board.move(move[0],move[1], player)
        next_board = mm_move(new_board, provided.switch_player(player))
        moves_and_scores[move] = next_board[0] * SCORES[player]
    max_score = max(moves_and_scores.values())
    potential_moves = [key for key in moves_and_scores.keys() if moves_and_scores[key] == max_score]
    return max_score * SCORES[player], potential_moves[random.randint(0, len(potential_moves)-1)]
        

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

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
