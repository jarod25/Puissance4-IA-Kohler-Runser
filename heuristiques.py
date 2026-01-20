def is_playable(board, x, y):
    return y == 0 or board.grid[x][y-1] != 0


def heuristique_early_1(board, window, positions, player, opponent):
    score = 0
    for (x, y), cell in zip(positions, window):
        if cell == player and x == 3:
            score += 10
    return score


def heuristique_early_2(board, window, positions, player, opponent):
    score = 0
    
    if window.count(opponent) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 10000

    elif window.count(opponent) == 2 and window.count(0) == 2:
        for i, (x, y) in enumerate(positions):
            if window[i] == 0 and is_playable(board, x, y):
                score += 2

    return score


def heuristique_early_3(board, window, positions, player, opponent):
    score = 0

    if window.count(player) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 10000

    return score



def heuristique_mid_1(board, window, positions, player, opponent):
    score = 0

    if window.count(player) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 10000
    
    if window.count(opponent) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 1000

    elif window.count(opponent) == 2 and window.count(0) == 2:
        for i, (x, y) in enumerate(positions):
            if window[i] == 0 and is_playable(board, x, y):
                score += 10

    return score


def heuristique_late_1(board, window, positions, player, opponent):
    score = 0

    if window.count(player) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 10000
    
    if window.count(opponent) == 3 and window.count(0) == 1:
        idx = window.index(0)
        x, y = positions[idx]

        if is_playable(board, x, y):
            score += 1000

    elif window.count(opponent) == 2 and window.count(0) == 2:
        for i, (x, y) in enumerate(positions):
            if window[i] == 0 and is_playable(board, x, y):
                score += 10

    return score
