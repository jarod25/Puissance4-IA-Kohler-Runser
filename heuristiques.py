def heuristique_column_line_value(board, player, opponent):
    """Reward central and strategically useful board positions."""
    row_weights = [2, 5, 30, 30, 10, 2]
    column_weights = [2, 5, 10, 40, 10, 5, 2]
    score = 0

    for column in range(7):
        for row in range(6):
            if board.grid[column][row] == player:
                score += column_weights[column]
                score += row_weights[row]
            elif board.grid[column][row] == opponent:
                score -= column_weights[column]
                score -= row_weights[row]

    return score


def heuristique_3_aligner(board, player, opponent):
    """Score lines containing three pieces and one empty cell."""
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(0)

        if player_count == 3 and empty_count == 1:
            score += 200

        if opponent_count == 3 and empty_count == 1:
            score -= 300

    for row in range(6):
        for column in range(4):
            evaluate_line([board.grid[column + offset][row] for offset in range(4)])

    for column in range(7):
        for row in range(3):
            evaluate_line([board.grid[column][row + offset] for offset in range(4)])

    for column in range(4):
        for row in range(3):
            evaluate_line(
                [board.grid[column + offset][row + offset] for offset in range(4)]
            )

    for column in range(4):
        for row in range(3, 6):
            evaluate_line(
                [board.grid[column + offset][row - offset] for offset in range(4)]
            )

    return score


def heuristique_2_aligner(board, player, opponent):
    """Score lines containing two pieces and two empty cells."""
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(0)

        if player_count == 2 and empty_count == 2:
            score += 50

        if opponent_count == 2 and empty_count == 2:
            score -= 60

    for row in range(6):
        for column in range(4):
            evaluate_line([board.grid[column + offset][row] for offset in range(4)])

    for column in range(7):
        for row in range(3):
            evaluate_line([board.grid[column][row + offset] for offset in range(4)])

    for column in range(4):
        for row in range(3):
            evaluate_line(
                [board.grid[column + offset][row + offset] for offset in range(4)]
            )

    for column in range(4):
        for row in range(3, 6):
            evaluate_line(
                [board.grid[column + offset][row - offset] for offset in range(4)]
            )

    return score


def heuristique_defaite_victoire(board, player, opponent):
    """Return a high terminal score for winning or losing alignments."""
    score = 0

    def evaluate_line(line):
        nonlocal score

        player_count = line.count(player)
        opponent_count = line.count(opponent)

        if player_count == 4:
            score += 50000

        if opponent_count == 4:
            score -= 30000

    for row in range(6):
        for column in range(4):
            evaluate_line([board.grid[column + offset][row] for offset in range(4)])

    for column in range(7):
        for row in range(3):
            evaluate_line([board.grid[column][row + offset] for offset in range(4)])

    for column in range(4):
        for row in range(3):
            evaluate_line(
                [board.grid[column + offset][row + offset] for offset in range(4)]
            )

    for column in range(4):
        for row in range(3, 6):
            evaluate_line(
                [board.grid[column + offset][row - offset] for offset in range(4)]
            )

    return score
