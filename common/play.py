from math import inf as infinity

from nlp.app import COMPUTER, HUMAN, NOT_PLAYED


def get_weight(board):
    score = 0
    if wins(board, COMPUTER):
        score += COMPUTER
    elif wins(board, HUMAN):
        score += HUMAN
    return score


def wins(board, player):
    b = [b2 for b2 in board]
    board = [
        [b[0], b[1], b[2]],
        [b[3], b[4], b[5]],
        [b[6], b[7], b[8]]
    ]
    win_board = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [player, player, player] in win_board:
        return True
    else:
        return False


def game_over(board):
    return wins(board, HUMAN) or wins(board, COMPUTER)


def empty_cells(board):
    return [index for index, value in enumerate(board) if value == NOT_PLAYED]


def minimax(board, depth, player):
    best = [-1, -1 * player * infinity]
    if depth == 0 or game_over(board):
        score = get_weight(board)
        return [-1, score]

    for cell in empty_cells(board):
        board[cell] = player
        score = minimax(board, depth - 1, -player)
        board[cell] = 0
        score[0] = cell

        if player == COMPUTER:
            if score[1] > best[1]:
                best = score  # max value
        else:
            if score[1] < best[1]:
                best = score  # min value
    return best


def ai_turn(board):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    move = minimax(board, depth, COMPUTER)[0]
    if move in empty_cells(board):
        board[move] = COMPUTER
    return move
