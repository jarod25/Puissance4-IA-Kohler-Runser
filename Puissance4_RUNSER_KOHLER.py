import tkinter as tk
from queue import Queue
from threading import Thread
from tkinter import ttk

import numpy as np

from heuristiques import (
    heuristique_2_aligner,
    heuristique_3_aligner,
    heuristique_column_line_value,
    heuristique_defaite_victoire,
)

DISK_COLORS = ("white", "red", "orange")
PLAYER_TYPES = ["human", *[f"AI: alpha-beta level {level}" for level in range(1, 43)]]

WIDTH = 700
ROW_WIDTH = WIDTH // 7
ROW_HEIGHT = ROW_WIDTH
HEIGHT = ROW_WIDTH * 6
ROW_MARGIN = ROW_HEIGHT // 10

disks: list[list[int]] = []
window: tk.Tk | None = None
canvas: tk.Canvas | None = None
information: tk.Label | None = None
combobox_player1: ttk.Combobox | None = None
combobox_player2: ttk.Combobox | None = None


def alpha_beta_decision(board, turn, ai_level, queue, player):
    possible_moves = board.get_possible_moves()
    if not possible_moves:
        queue.put(0)
        return

    best_move = possible_moves[0]
    alpha = -float("inf")
    beta = float("inf")
    best_value = -float("inf")

    for move in possible_moves:
        updated_board = board.copy()
        row_to_play = updated_board.get_available_row(move)
        if row_to_play is None:
            continue

        updated_board.grid[move][row_to_play] = turn % 2 + 1

        value = min_value_ab(
            updated_board,
            turn + 1,
            ai_level,
            alpha,
            beta,
            player,
        )
        if ai_level % 2 == 0:
            value = -value

        if value > best_value:
            best_value = value
            best_move = move

        alpha = max(alpha, best_value)

    queue.put(best_move)


def max_value_ab(board, turn, depth, alpha, beta, player):
    if depth <= 0:
        current_player = turn % 2 + 1
        return board.eval(current_player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    value = -float("inf")
    for move in possible_moves:
        updated_board = board.copy()
        row_to_play = updated_board.get_available_row(move)
        if row_to_play is None:
            continue

        updated_board.grid[move][row_to_play] = turn % 2 + 1

        value = max(
            value,
            min_value_ab(
                updated_board,
                turn + 1,
                depth - 1,
                alpha,
                beta,
                player,
            ),
        )
        if value >= beta:
            return value

        alpha = max(alpha, value)

    return value


def min_value_ab(board, turn, depth, alpha, beta, player):
    if depth <= 0:
        current_player = turn % 2 + 1
        return board.eval(current_player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    value = float("inf")
    for move in possible_moves:
        updated_board = board.copy()
        row_to_play = updated_board.get_available_row(move)
        if row_to_play is None:
            continue

        updated_board.grid[move][row_to_play] = turn % 2 + 1

        value = min(
            value,
            max_value_ab(
                updated_board,
                turn + 1,
                depth - 1,
                alpha,
                beta,
                player,
            ),
        )
        if value <= alpha:
            return value

        beta = min(beta, value)

    return value


class Board:
    def __init__(self):
        self.grid = np.zeros((7, 6), dtype=np.int64)

    def eval(self, player):
        opponent = 3 - player
        score = 0
        filled = np.count_nonzero(self.grid)

        if self.check_victory():
            return heuristique_defaite_victoire(self, player, opponent)

        if filled <= 10:
            score += heuristique_column_line_value(self, player, opponent) * 4
            score += heuristique_3_aligner(self, player, opponent) * 3
            score += heuristique_2_aligner(self, player, opponent)
        elif filled <= 30:
            score += heuristique_column_line_value(self, player, opponent)
            score += heuristique_3_aligner(self, player, opponent) * 3
        else:
            score += heuristique_3_aligner(self, player, opponent)

        return score

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reset(self):
        self.grid.fill(0)

    def reinit(self):
        self.reset()

        if canvas is None:
            return

        for column in range(7):
            for row in range(6):
                canvas.itemconfig(disks[column][row], fill=DISK_COLORS[0])

    def get_available_row(self, column):
        for row in range(6):
            if self.grid[column][row] == 0:
                return row

        return None

    def get_possible_moves(self):
        possible_moves = []

        if self.grid[3][5] == 0:
            possible_moves.append(3)

        for shift_from_center in range(1, 4):
            if self.grid[3 + shift_from_center][5] == 0:
                possible_moves.append(3 + shift_from_center)
            if self.grid[3 - shift_from_center][5] == 0:
                possible_moves.append(3 - shift_from_center)

        return possible_moves

    def add_disk(self, column, player, update_display=True):
        row = self.get_available_row(column)
        if row is None:
            return False

        self.grid[column][row] = player

        if update_display and canvas is not None:
            canvas.itemconfig(disks[column][row], fill=DISK_COLORS[player])

        return True

    def column_filled(self, column):
        return self.grid[column][5] != 0

    def check_victory(self):
        for row in range(6):
            for horizontal_shift in range(4):
                if (
                    self.grid[horizontal_shift][row]
                    == self.grid[horizontal_shift + 1][row]
                    == self.grid[horizontal_shift + 2][row]
                    == self.grid[horizontal_shift + 3][row]
                    != 0
                ):
                    return True

        for column in range(7):
            for vertical_shift in range(3):
                if (
                    self.grid[column][vertical_shift]
                    == self.grid[column][vertical_shift + 1]
                    == self.grid[column][vertical_shift + 2]
                    == self.grid[column][vertical_shift + 3]
                    != 0
                ):
                    return True

        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if (
                    self.grid[horizontal_shift][vertical_shift]
                    == self.grid[horizontal_shift + 1][vertical_shift + 1]
                    == self.grid[horizontal_shift + 2][vertical_shift + 2]
                    == self.grid[horizontal_shift + 3][vertical_shift + 3]
                    != 0
                ):
                    return True

                if (
                    self.grid[horizontal_shift][5 - vertical_shift]
                    == self.grid[horizontal_shift + 1][4 - vertical_shift]
                    == self.grid[horizontal_shift + 2][3 - vertical_shift]
                    == self.grid[horizontal_shift + 3][2 - vertical_shift]
                    != 0
                ):
                    return True

        return False


class Connect4:
    def __init__(self):
        self.board = Board()
        self.human_turn = False
        self.turn = 1
        self.players = (0, 0)
        self.ai_move = Queue()

    def current_player(self):
        return 2 - (self.turn % 2)

    def launch(self):
        if information is None or combobox_player1 is None or combobox_player2 is None:
            return

        self.board.reinit()
        self.turn = 0
        information["fg"] = "black"
        information["text"] = (
            f"Turn {self.turn} - Player {self.current_player()} is playing"
        )
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, column):
        if not self.board.column_filled(column):
            self.board.add_disk(column, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            column = event.x // ROW_WIDTH
            self.move(column)

    def ai_turn(self, ai_level):
        Thread(
            target=alpha_beta_decision,
            args=(
                self.board,
                self.turn,
                ai_level,
                self.ai_move,
                self.current_player(),
            ),
            daemon=True,
        ).start()
        self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if window is None:
            return

        if not self.ai_move.empty():
            self.move(self.ai_move.get())
        else:
            window.after(100, self.ai_wait_for_move)

    def handle_turn(self):
        if information is None:
            return

        self.human_turn = False

        if self.board.check_victory():
            information["fg"] = "red"
            information["text"] = f"Player {self.current_player()} wins!"
            return

        if self.turn >= 42:
            information["fg"] = "red"
            information["text"] = "This is a draw!"
            return

        self.turn += 1
        information["text"] = (
            f"Turn {self.turn} - Player {self.current_player()} is playing"
        )

        if self.players[self.current_player() - 1] != 0:
            self.ai_turn(self.players[self.current_player() - 1])
        else:
            self.human_turn = True


def main():
    global window
    global canvas
    global information
    global combobox_player1
    global combobox_player2

    window = tk.Tk()
    window.title("Connect Four")

    canvas = tk.Canvas(window, bg="blue", width=WIDTH, height=HEIGHT)

    for column in range(7):
        disks.append([])
        for row in range(5, -1, -1):
            disks[column].append(
                canvas.create_oval(
                    ROW_MARGIN + column * ROW_WIDTH,
                    ROW_MARGIN + row * ROW_HEIGHT,
                    (column + 1) * ROW_WIDTH - ROW_MARGIN,
                    (row + 1) * ROW_HEIGHT - ROW_MARGIN,
                    fill=DISK_COLORS[0],
                )
            )

    canvas.grid(row=0, column=0, columnspan=2)

    information = tk.Label(window, text="")
    information.grid(row=1, column=0, columnspan=2)

    label_player1 = tk.Label(window, text="Player 1:")
    label_player1.grid(row=2, column=0)

    combobox_player1 = ttk.Combobox(window, state="readonly", values=PLAYER_TYPES)
    combobox_player1.grid(row=2, column=1)
    combobox_player1.current(0)

    label_player2 = tk.Label(window, text="Player 2:")
    label_player2.grid(row=3, column=0)

    combobox_player2 = ttk.Combobox(window, state="readonly", values=PLAYER_TYPES)
    combobox_player2.grid(row=3, column=1)
    combobox_player2.current(6)

    game = Connect4()

    new_game_button = tk.Button(window, text="New game", command=game.launch)
    new_game_button.grid(row=4, column=0)

    quit_button = tk.Button(window, text="Quit", command=window.destroy)
    quit_button.grid(row=4, column=1)

    canvas.bind("<Button-1>", game.click)
    window.mainloop()


if __name__ == "__main__":
    main()
