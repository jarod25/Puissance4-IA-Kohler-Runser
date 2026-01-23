import tkinter as tk
from tkinter import ttk
import numpy as np
import random as rnd
from threading import Thread
from queue import Queue
import os
import multiprocessing as mp

from heuristiques import heuristique_column_line_value, heuristique_3_aligner, heuristique_2_aligner, heuristique_defaite_victoire


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
        if ai_level % 2 == 0:
            value = -value # on inverse la valeur pour les niveaux pairs pour avoir le maximum pour l'IA
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

    if depth <= 0:
        current_player = turn % 2 + 1
        return board.eval(current_player)

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

class Board:
    grid = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])


    def eval(self, player):
        opponent = 3 - player
        score = 0
        filled = np.count_nonzero(self.grid)


        # gestion de victoire/defaite
        if self.check_victory():
            return heuristique_defaite_victoire(self, player, opponent)

        # early game
        if filled <= 10:
            score += heuristique_column_line_value(self, player, opponent) * 4
            score += heuristique_3_aligner(self, player, opponent) * 3
            score += heuristique_2_aligner(self, player, opponent)

        # mid game
        elif filled <= 30:
            score += heuristique_column_line_value(self, player, opponent)
            score += heuristique_3_aligner(self, player, opponent) * 3

        # late game
        else:
            score += heuristique_3_aligner(self, player, opponent)

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

# Ajout du multiprocessing pour l'alpha-beta
_ctx = None
_pool = None

_alpha_beta_decision_seq = alpha_beta_decision

def _ab_worker(grid_bytes, turn, ai_level, move, player, alpha):
    b = Board()
    b.grid = np.frombuffer(grid_bytes, dtype=np.int64).reshape(7, 6).copy()

    row_to_play = None
    for r in range(6):
        if b.grid[move][r] == 0:
            row_to_play = r
            break
    if row_to_play is None:
        return -1e18, move

    b.grid[move][row_to_play] = turn % 2 + 1

    v = min_value_ab(b, turn + 1, ai_level, alpha, 1e18, player)
    if ai_level % 2 == 0:
        v = -v
    return v, move

def alpha_beta_decision(board, turn, ai_level, queue, player):
    possible_moves = board.get_possible_moves()
    if not possible_moves:
        queue.put(0)
        return

    if mp.get_start_method(allow_none=True) != "fork":
        return _alpha_beta_decision_seq(board, turn, ai_level, queue, player)

    alpha = -1e18
    beta = 1e18

    best_move = possible_moves[0]
    best_value = -1e18

    b0 = board.copy()
    col = best_move
    row_to_play = None
    for r in range(6):
        if b0.grid[col][r] == 0:
            row_to_play = r
            break
    if row_to_play is not None:
        b0.grid[col][row_to_play] = turn % 2 + 1
        v0 = min_value_ab(b0, turn + 1, ai_level, alpha, beta, player)
        if ai_level % 2 == 0:
            v0 = -v0
        best_value = v0
        alpha = best_value

    rest = possible_moves[1:]
    if not rest:
        queue.put(best_move)
        return

    global _ctx, _pool
    if _ctx is None:
        _ctx = mp.get_context("fork")
    if _pool is None:
        n = os.cpu_count() or 1
        if n > len(rest):
            n = len(rest)
        if n < 1:
            n = 1
        _pool = _ctx.Pool(processes=n)

    grid_bytes = board.grid.astype(np.int64, copy=False).tobytes()
    tasks = [(grid_bytes, turn, ai_level, m, player, alpha) for m in rest]
    results = _pool.starmap(_ab_worker, tasks)

    for v, m in results:
        if v > best_value:
            best_value = v
            best_move = m

    queue.put(best_move)

window.mainloop()
