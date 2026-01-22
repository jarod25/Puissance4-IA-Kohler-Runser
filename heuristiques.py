
# heuristique qui favorise les cases du centre
def heuristique_column_line_value(board, player, opponent):
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

# heuristique permettant de défendre si l'adversaire peut aligner 3 pions en bloquant avant que cela n'arrive.
def heuristique_3_aligner(board, player, opponent):
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(0)

        # Attaque
        if player_count == 3 and empty_count == 1:
            score += 200

        # Défense
        if opponent_count == 3 and empty_count == 1:
            score -= 300

    # Horizontal
    for row in range(6):
        for col in range(4):
            line = [board.grid[col + i][row] for i in range(4)]
            evaluate_line(line)

    # Vertical
    for col in range(7):
        for row in range(3):
            line = [board.grid[col][row + i] for i in range(4)]
            evaluate_line(line)

    # Diagonales
    for col in range(4):
        for row in range(3):
            line = [board.grid[col + i][row + i] for i in range(4)]
            evaluate_line(line)

    for col in range(4):
        for row in range(3, 6):
            line = [board.grid[col + i][row - i] for i in range(4)]
            evaluate_line(line)

    return score

# heuristique permettant de défendre si l'adversaire peut aligner 2 pions en bloquant avant que cela n'arrive.
def heuristique_2_aligner(board, player, opponent):
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(0)

        # Attaque
        if player_count == 2 and empty_count == 2:
            score += 50

        # Défense
        if opponent_count == 2 and empty_count == 2:
            score -= 60

    # Horizontal
    for row in range(6):
        for col in range(4):
            line = [board.grid[col + i][row] for i in range(4)]
            evaluate_line(line)

    # Vertical
    for col in range(7):
        for row in range(3):
            line = [board.grid[col][row + i] for i in range(4)]
            evaluate_line(line)

    # Diagonales
    for col in range(4):
        for row in range(3):
            line = [board.grid[col + i][row + i] for i in range(4)]
            evaluate_line(line)

    for col in range(4):
        for row in range(3, 6):
            line = [board.grid[col + i][row - i] for i in range(4)]
            evaluate_line(line)

    return score

# heuristique permettant de défendre une défaite ou assurer une victoire
def heuristique_defaite_victoire(board, player, opponent):
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)

        # Attaque
        if player_count == 4 :
            score += 5000

        # Défense
        if opponent_count == 4 :
            score -= 3000

    # Horizontal
    for row in range(6):
        for col in range(4):
            line = [board.grid[col + i][row] for i in range(4)]
            evaluate_line(line)

    # Vertical
    for col in range(7):
        for row in range(3):
            line = [board.grid[col][row + i] for i in range(4)]
            evaluate_line(line)

    # Diagonales
    for col in range(4):
        for row in range(3):
            line = [board.grid[col + i][row + i] for i in range(4)]
            evaluate_line(line)

    for col in range(4):
        for row in range(3, 6):
            line = [board.grid[col + i][row - i] for i in range(4)]
            evaluate_line(line)

    return score

