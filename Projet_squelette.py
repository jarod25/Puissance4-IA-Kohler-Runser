import tkinter as tk
from tkinter import ttk
import numpy as np
import random as rnd
from threading import Thread
from queue import Queue

from heuristiques import heuristique_early_1, heuristique_early_2, heuristique_early_3
from heuristiques import heuristique_mid_1
from heuristiques import heuristique_late_1


disk_color = ['white', 'red', 'orange']
disks = list()

player_type = ['human']
for i in range(42):
    player_type.append('AI: alpha-beta level '+str(i+1))

def alpha_beta_decision(board, turn, ai_level, queue, player):
    possible_moves = board.get_possible_moves()
    best_move = possible_moves[0]
    alpha = -float("inf")
    beta  =  float("inf")
    best_value = -float("inf")
    print("tout :", turn)

    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break

        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = min_value_ab(updated_board, turn + 1, ai_level, alpha, beta, player)
        if value > best_value:
            best_value = value
            best_move = move
        print(f"col {move} → value {value}")
        alpha = max(alpha, best_value)
    
    queue.put(best_move)


def max_value_ab(board, turn, depth, alpha, beta, player):
    """
    if board.check_victory():
        last_player = 3 - (turn % 2 + 1)
        if last_player == player:
            return float("inf")
        else:
            return -float("inf")
    """
    if depth <= 0:
        return board.eval(player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    value = -float("inf")
    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break
        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = max(value, min_value_ab(updated_board, turn + 1, depth - 1, alpha, beta, player))
        if value >= beta:
            return value
        alpha = max(alpha, value)

    return value


def min_value_ab(board, turn, depth, alpha, beta, player):
    """
    if board.check_victory():
        last_player = 3 - (turn % 2 + 1)
        if last_player == player:
            return float("inf")
        else:
            return -float("inf")
    """
    if depth <= 0:
        return -board.eval(player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    value = float("inf")
    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break
        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = min(value, max_value_ab(updated_board, turn + 1, depth - 1, alpha, beta, player))
        if value <= alpha:
            return value
        beta = min(beta, value)

    return value


def minimax_decision(board, turn, ai_level, queue):
    possible_moves = board.get_possible_moves()
    best_move = possible_moves[0]
    best_value = -float("inf")

    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break
        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = min_value(updated_board, turn + 1, ai_level)
        if value > best_value:
            best_value = value
            best_move = move

    queue.put(best_move)


def max_value(board, turn, depth, player):
    if board.check_victory():
        return -1
    if depth <= 0:
        return board.eval(player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    best_value = -float("inf")
    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break
        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = min_value(updated_board, turn + 1, depth - 1)
        if value > best_value:
            best_value = value

    return best_value


def min_value(board, turn, depth, player):
    if board.check_victory():
        return 1
    if depth <= 0:
        return board.eval(player)

    possible_moves = board.get_possible_moves()
    if not possible_moves:
        return 0

    worst_value = float("inf")
    for move in possible_moves:
        updated_board = board.copy()

        col = move
        row_to_play = None
        for r in range(6):
            if updated_board.grid[col][r] == 0:
                row_to_play = r
                break
        if row_to_play is None:
            continue

        updated_board.grid[col][row_to_play] = turn % 2 + 1

        value = max_value(updated_board, turn + 1, depth - 1, player)
        if value < worst_value:
            worst_value = value

    return worst_value


class Board:
    grid = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])


    def eval(self, player):
        opponent = 3 - player
        score = 0

        def evaluate_window(window, positions):
            nonlocal score
            print(self.grid)
            filled_cells = np.count_nonzero(self.grid)
            fill_ratio = filled_cells / 42

            if fill_ratio <= 1:
                #score += heuristique_early_1(self, window, positions, player, opponent)
                score += heuristique_early_2(self, window, positions, player, opponent)
                score += heuristique_early_3(self, window, positions, player, opponent)

            elif fill_ratio <= 0.75:
                score += heuristique_mid_1(self, window, positions, player, opponent)

            else:
                score += heuristique_late_1(self, window, positions, player, opponent)


        # horizontal
        for y in range(6):
            for x in range(4):
                window = list(self.grid[x:x+4, y])
                positions = [(x+i, y) for i in range(4)]
                evaluate_window(window, positions)


        # Vertical
        for x in range(7):
            for y in range(3):
                window = [self.grid[x][y+i] for i in range(4)]
                positions = [(x, y+i) for i in range(4)]
                evaluate_window(window, positions)



        # Diagonal
        for x in range(4):
            for y in range(3):
                window = [self.grid[x+i][y+i] for i in range(4)]
                positions = [(x+i, y+i) for i in range(4)]
                evaluate_window(window, positions)

        for x in range(4):
            for y in range(3):
                window = [self.grid[x+i][y+3-i] for i in range(4)]
                positions = [(x+i, y+3-i) for i in range(4)]
                evaluate_window(window, positions)

        return score

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reinit(self):
        self.grid.fill(0)
        for i in range(7):
            for j in range(6):
                canvas1.itemconfig(disks[i][j], fill=disk_color[0])

    def get_possible_moves(self):
        possible_moves = list()
        if self.grid[3][5] == 0:
            possible_moves.append(3)
        for shift_from_center in range(1, 4):
            if self.grid[3 + shift_from_center][5] == 0:
                possible_moves.append(3 + shift_from_center)
            if self.grid[3 - shift_from_center][5] == 0:
                possible_moves.append(3 - shift_from_center)
        return possible_moves

    def add_disk(self, column, player, update_display=True):
        for j in range(6):
            if self.grid[column][j] == 0:
                break
        self.grid[column][j] = player
        if update_display:
            canvas1.itemconfig(disks[column][j], fill=disk_color[player])

    def column_filled(self, column):
        return self.grid[column][5] != 0

    def check_victory(self):
        # Horizontal alignment check
        for line in range(6):
            for horizontal_shift in range(4):
                if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] != 0:
                    return True
        # Vertical alignment check
        for column in range(7):
            for vertical_shift in range(3):
                if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
                        self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] != 0:
                    return True
        # Diagonal alignment check
        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] ==\
                        self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][vertical_shift + 3] != 0:
                    return True
                elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][4 - vertical_shift] ==\
                        self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][2 - vertical_shift] != 0:
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
        self.board.reinit()
        self.turn = 0
        information['fg'] = 'black'
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, column):
        if not self.board.column_filled(column):
            self.board.add_disk(column, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            column = event.x // row_width
            self.move(column)

    def ai_turn(self, ai_level):
        Thread(target=alpha_beta_decision, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),)).start()
        self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if not self.ai_move.empty():
            self.move(self.ai_move.get())
        else:
            window.after(100, self.ai_wait_for_move)

    def handle_turn(self):
        self.human_turn = False
        if self.board.check_victory():
            information['fg'] = 'red'
            information['text'] = "Player " + str(self.current_player()) + " wins !"
            return
        elif self.turn >= 42:
            information['fg'] = 'red'
            information['text'] = "This a draw !"
            return
        self.turn = self.turn + 1
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        if self.players[self.current_player() - 1] != 0:
            self.human_turn = False
            self.ai_turn(self.players[self.current_player() - 1])
        else:
            self.human_turn = True


game = Connect4()

# Graphical settings
width = 700
row_width = width // 7
row_height = row_width
height = row_width * 6
row_margin = row_height // 10

window = tk.Tk()
window.title("Connect 4")
canvas1 = tk.Canvas(window, bg="blue", width=width, height=height)

# Drawing the grid
for i in range(7):
    disks.append(list())
    for j in range(5, -1, -1):
        disks[i].append(canvas1.create_oval(row_margin + i * row_width, row_margin + j * row_height, (i + 1) * row_width - row_margin,
                            (j + 1) * row_height - row_margin, fill='white'))


canvas1.grid(row=0, column=0, columnspan=2)

information = tk.Label(window, text="")
information.grid(row=1, column=0, columnspan=2)

label_player1 = tk.Label(window, text="Player 1: ")
label_player1.grid(row=2, column=0)
combobox_player1 = ttk.Combobox(window, state='readonly')
combobox_player1.grid(row=2, column=1)

label_player2 = tk.Label(window, text="Player 2: ")
label_player2.grid(row=3, column=0)
combobox_player2 = ttk.Combobox(window, state='readonly')
combobox_player2.grid(row=3, column=1)

combobox_player1['values'] = player_type
combobox_player1.current(0)
combobox_player2['values'] = player_type
combobox_player2.current(6)

button2 = tk.Button(window, text='New game', command=game.launch)
button2.grid(row=4, column=0)

button = tk.Button(window, text='Quit', command=window.destroy)
button.grid(row=4, column=1)

# Mouse handling
canvas1.bind('<Button-1>', game.click)

window.mainloop()
