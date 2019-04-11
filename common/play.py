import random

from nlp.app import PLAYER, COMPUTER, NOT_PLAYED


def get_free_cells(board):
    """Get the cells that are playable
    
    Arguments:
        board {list} -- Representation of the board
    
    Returns:
        list -- integers representing the free cells
    """

    return [index for index, value in enumerate(board) if value == NOT_PLAYED]


def get_random_move(board, player_number):
    """Get a random move from the list of free cells
    
    Arguments:
        board {list} -- Representation of the board
        player_number {int} -- Player
    
    Returns:
        int -- A free cell
    """

    return random.choice(get_free_cells(board))


def get_weight(winner):
    if winner == COMPUTER:
        return 1000
    elif winner == PLAYER:
        return -1000
    else:
        return 0


def compute_weight(board, deepness):
    value = 1001
    winner = find_winner(board)
    if deepness == 0 or winner is not None:
        # if deepness != 0 : print("########################path found before full########################")
        weight = get_weight(winner)
        # print("weight:"+ str(weight))
        return weight
    for i in range(0, 8):
        if board[i] == NOT_PLAYED:
            if deepness % 2 != 0:  # min
                board[i] = PLAYER
                tmp = compute_weight(board, deepness - 1)
                if tmp < value:
                    value = tmp
            else:  # max
                board[i] = COMPUTER
                tmp = compute_weight(board, deepness - 1)
                if tmp > value:
                    value = tmp
            board[i] = NOT_PLAYED
    return value


def get_smart_move(board, player_number):
    """Apply the min-max algorithm or another smart one to find next move
    
    Arguments:
        board {list} -- Reprensetation of the board
        player_number {int} -- Player
    """
    max_value = 0
    index_to_play = -1
    for i in range(0, 8):
        maxV = compute_weight(board, 8)
        print("Max value for index" + str(i) + " is " + str(maxV))
        if maxV > max_value:
            max_value = maxV
            index_to_play = index_to_play

    print("index to play:" + str(index_to_play) + " associated max value" + str(max_value))
    return index_to_play


def find_winner(game_board):
    """Taken on https://pastebin.com/FKrbiuCc and adapted for our data format
    
    Arguments:
        b1 {list} -- Reprensetation of the board
    
    Returns:
        int -- None if there's no winner, else the player who won
    """

    b = [b2 + 1 for b2 in game_board]
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


def display(board):
    for index, value in enumerate(board):
        if index % 3 == 0:
            print("")
        print(value, end="|")
    print()
