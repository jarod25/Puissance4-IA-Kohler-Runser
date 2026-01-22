def is_playable(board, x, y):
    return y == 0 or board.grid[x][y-1] != 0

def heuristique_column_line_value(board, player, opponent):
    """
    Favorise la colonne et lignes centrales
    """
    row_weights = [2, 5, 30, 30, 10, 2]
    column_weights = [2, 5, 10, 40, 10, 5, 2]

    score = 0

    for col in range(7):
        for row in range(6):
            if board.grid[col][row] == player:
                score += column_weights[col]
                score += row_weights[row]
            elif board.grid[col][row] == opponent:
                score -= column_weights[col]
                score -= row_weights[row]

    return score

def heuristique_open_threes(board, player, opponent):
    score = 0

    def evaluate_window(window):
        nonlocal score

        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(0)

        # Attaque
        if player_count == 3 and empty_count == 1:
            score += 300

        # Défense
        if opponent_count == 3 and empty_count == 1:
            score -= 200

    # Horizontal
    for row in range(6):
        for col in range(4):
            window = [board.grid[col + i][row] for i in range(4)]
            evaluate_window(window)

    # Vertical
    for col in range(7):
        for row in range(3):
            window = [board.grid[col][row + i] for i in range(4)]
            evaluate_window(window)

    # Diagonales
    for col in range(4):
        for row in range(3):
            window = [board.grid[col + i][row + i] for i in range(4)]
            evaluate_window(window)

    for col in range(4):
        for row in range(3, 6):
            window = [board.grid[col + i][row - i] for i in range(4)]
            evaluate_window(window)

    return score




def heuristique_defense(board, player, opponent):
    """
    Récompense fortement une victoire de l'IA
    """
    if board.check_victory():
        return 2000
    return 0
