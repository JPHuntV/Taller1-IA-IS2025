import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class TicTacToe:
    def __init__(self, depth=3):
        self.depth = depth #profundidad del arbol de busqueda
        self.board = np.full((3, 3), None) #un tablero de 3x3 con valores nulos
        self.current_player = 'X' 
    
    def minimax(self, board, depth, alpha, beta, maximizing):
        winner = self.check_winner(board) 
        if winner == 'X':
            return -1 
        if winner =='O':
            return 1
        if self.is_draw(board) or depth == 0:
            return 0

        
        if maximizing: #se maximiza si es el turno de la IA
            max_eval = float('-inf') #este valor es el peor valor posible
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'O'
                        eval = self.minimax(board, depth-1, alpha, beta, False) #se llama recursivamente minimax con el nuevo tablero
                        board[i][j] = None
                        max_eval = max(max_eval, eval) #se obtiene el maximo entre el valor actual y el valor de la llamada recursiva
                        alpha = max(alpha, eval)
                        if beta <= alpha: #alpha beta pruning 
                            break
            return max_eval
        else: #se minimiza si es el turno del jugador
            min_eval = float('inf') #este valor es el mejor valor posible
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'X'
                        eval = self.minimax(board, depth - 1, alpha, beta, True) #se llama recursivamente minimax con el nuevo tablero
                        board[i][j] = None
                        min_eval = min(min_eval, eval) #se obtiene el minimo entre el valor actual y el valor de la llamada recursiva
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval
    
    def best_move(self):
        if self.depth == 1: #si la profundidad es 1, se elige un movimiento aleatorio
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None] #una lista con las celdas vacias
            return random.choice(empty_cells) if empty_cells else None
        
        best_score = float('-inf') 
        move = None
        for i in range(3):
            for j in range(3):
                #para cada celda vacia se llama minimax
                if self.board[i][j] is None: 
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, self.depth, float('-inf'), float('inf'), False) #se llama minimax con el nuevo tablero
                    self.board[i][j] = None
                    if score > best_score: #se encontró un mejor movimiento
                        best_score = score
                        move = (i, j) 
        return move 
    
    def check_winner(self, board):
        for row in board:
            if all(cell == 'X' for cell in row): return 'X'
            if all(cell == 'O' for cell in row): return 'O'
        for col in range(3):
            if all(board[row][col] == 'X' for row in range(3)): return 'X'
            if all(board[row][col] == 'O' for row in range(3)): return 'O'
        if all(board[i][i] == 'X' for i in range(3)) or all(board[i][2 - i] == 'X' for i in range(3)): return 'X'
        if all(board[i][i] == 'O' for i in range(3)) or all(board[i][2 - i] == 'O' for i in range(3)): return 'O'
        return None
    
    def is_draw(self, board): #tablero lleno
        return all(cell is not None for row in board for cell in row) 
    
    def make_move(self, row, col):
        if self.board[row][col] is None: #si la celda que se hizo click está vacía
            self.board[row][col] = 'X'
            if not self.check_winner(self.board) and not self.is_draw(self.board): #si el juego no ha terminado le toca a la IA
                ai_move = self.best_move()
                if ai_move:
                    self.board[ai_move[0]][ai_move[1]] = 'O'
    
    def reset_game(self):
        self.board = np.full((3, 3), None)

####IA####
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI")
        self.difficulty = tk.IntVar(value=3)
        self.game = TicTacToe(depth=self.difficulty.get())
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.create_difficulty_options()
    
    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(frame, text='', font=('Arial', 20), width=12, height=6
                                                , background="black", foreground="white", border=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)
        
    def create_difficulty_options(self):
        frame = tk.Frame(self.root)
        frame.pack()
        #3 opciones de dificultad que abarquen toda la pantalla
        tk.Radiobutton(frame, text="Principiante", variable=self.difficulty, value=1, command=self.update_difficulty).pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Intermedio", variable=self.difficulty, value=3, command=self.update_difficulty).pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Experto", variable=self.difficulty, value=5, command=self.update_difficulty).pack(side=tk.LEFT)
    
    def update_difficulty(self):
        self.game.depth = self.difficulty.get()
    
    def on_click(self, row, col):
        if self.game.board[row][col] is None:
            self.game.make_move(row, col)
            self.update_board()
            winner = self.game.check_winner(self.game.board)
            if winner:
                messagebox.showinfo("Fin del juego", f"Ganó {winner}!")
                self.game.reset_game()
                self.update_board()
            elif self.game.is_draw(self.game.board):
                messagebox.showinfo("Fin del juego", "Empate!")
                self.game.reset_game()
                self.update_board()
    
    def update_board(self):
        for i in range(3):
            for j in range(3):
                text = self.game.board[i][j] if self.game.board[i][j] is not None else ''
                self.buttons[i][j].config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
##############################################################################################################