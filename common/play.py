import random


def get_free_cells(board):
    """Get the cells that are playable
    
    Arguments:
        board {list} -- Representation of the board
    
    Returns:
        list -- integers representing the free cells
    """

    return [index for index, value in enumerate(board) if value == -1]


def get_random_move(board, player_number):
    """Get a random move from the list of free cells
    
    Arguments:
        board {list} -- Representation of the board
        player_number {int} -- Player
    
    Returns:
        int -- A free cell
    """

    return random.choice(get_free_cells(board))


def get_smart_move(board, player_number):
    """Apply the min-max algorithm or another smart one to find next move
    
    Arguments:
        board {list} -- Reprensetation of the board
        player_number {int} -- Player
    """

    ## ----- TODO : Use the minmax algorithm or another smart one to find the best move ----- ## 
    pass
    ##------------------------------------------------------------------------------------##


def find_winner(b1):
    """Taken on https://pastebin.com/FKrbiuCc and adapted for our data format
    
    Arguments:
        b1 {list} -- Reprensetation of the board
    
    Returns:
        int -- None if there's no winner, else the player who won
    """

    b = [b2 + 1 for b2 in b1]
    board = [
        [b[0], b[1], b[2]],
        [b[3], b[4], b[5]],
        [b[6], b[7], b[8]]
    ]
    winners = {0: None, 1: 0, 2: 1}

    for i in range(1, 3):

        if board[0] == [i, i, i] or board[1] == [i, i, i] or board[2] == [i, i, i]:  # horizontal wins
            return winners[i]
        elif board[0][0] == i and board[1][0] == i and board[2][0] == i:  # vertical first column
            return winners[i]
        elif board[0][1] == i and board[1][1] == i and board[2][1] == i:  # vertical second column
            return winners[i]
        elif board[0][2] == i and board[1][2] == i and board[2][2] == i:  # vertical third column
            return winners[i]
        elif board[0][0] == i and board[1][1] == i and board[2][2] == i:  # diagonal top-bottom
            return winners[i]
        elif board[0][2] == i and board[1][1] == i and board[2][0] == i:  # diagonal bottom-top
            return winners[i]
    else:
        return winners[0]
