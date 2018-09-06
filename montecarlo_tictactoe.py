"""
Monte Carlo Tic-Tac-Toe Player

Note: requires external modules that are not present, so this code won't work,
but the logic is sound and functional.
"""

import random
#import poc_ttt_gui
#import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Plays out the rest of the board with random moves
    """
    while board.check_win() is None:
        rand_row, rand_col = board.get_empty_squares()[random.randint(0, len(board.get_empty_squares()) - 1)]
        board.move(rand_row, rand_col, player)
        provided.switch_player(player)
    return

def mc_update_scores(scores, board, player):
    """
    Takes in a scores matrix, a completed board that
    we want to update the scores matrix with,
    and which player the machine is.
    Updates the scores matrix based on who won and
    the constants defined above.
    """
    values = {provided.EMPTY: 0, player:SCORE_CURRENT, provided.switch_player(player):SCORE_OTHER}
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            square = board.square(row, col)
            if square == winner:
                scores[row][col] += values[square]
            else:
                scores[row][col] -= values[square]
                
def get_best_move(board, scores):
    """
    Uses the scores matrix (which would have been built
    using the above method) to decide which of the empty spaces
    is the best move.
    """
    if board.check_win() is not None:
        return
    spaces = board.get_empty_squares()
    scores_of_empty_spaces = [scores[row][col] for (row,col) in spaces]
    max_score = max(scores_of_empty_spaces)
    best_spaces = [spaces[ind] for ind in range(len(spaces)) if scores_of_empty_spaces[ind] == max_score]
    return best_spaces[random.randint(0, len(best_spaces)-1)]

def mc_move(board, player, trials = NTRIALS):
    """
    Given a board, does _trials_ number of mc_trial's, scores each
    one, and picks the next move based on which empty square
    has the highest overall score.
    """
    row_of_scores = [0] * board.get_dim()
    scores = [row_of_scores[:] for dummy in range(board.get_dim())]
    for dummy in range(trials):
        test_board = board.clone()
        mc_trial(test_board, player)
        mc_update_scores(scores, test_board, player)
    return get_best_move(board, scores)
        