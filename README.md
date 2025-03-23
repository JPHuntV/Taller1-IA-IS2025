# TicTacToe VS IA

En este juego de tictactoe contra la maquina se utiliza el algoritmo minimax con Alpha Beta Prunning.
El algoritmo asume lo siguiente:
- La IA (O) siempre va a jugar de manera optima para optimizar su puntaje
- El jugador (X) juega de manera optima para minimizar el puntaje de la IA

El juego tiene 3 dificultades:
-Principiante: La IA jugará de manera aleatoria
-Intermedio: La IA aplicará el algoritmo con una profundidad de 3
-Avanzado: La IA aplicará el algoritmo con una profundidad

## Implementación
Luego de que el jugador X hace una jugada la IA buscará hacer su mejor movimiento 
```python
def best_move(self):
        if self.depth == 1: #si la profundidad es 1, se elige un movimiento aleatorio
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None] #una lista con las celdas vacias
            return random.choice(empty_cells) if empty_cells else None
        
        best_score = float('-inf') #Peor valor posible
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
```
Para ello se comparan los arboles de cada una de las posibles posiciones que puede jugar y se escoge la que da un mejor puntaje.

La función minimax va a buscar minimizar el puntaje obtenido por (X) y maximizar el puntaje obtenido por (O).
```python
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
```
Al maximizar, se recorre recursivamente el arbol de jugadas posibles despues de la jugada actual, se compara el valor "puntaje" actual y con el retorno de llamada recursiva 
para obtener el valor maximo. Caso contrario, si estamos minizando se debera buscar el valor minimo luego de las llamadas recursivas sobre el arbol.

Esta selección de puntajes se puede visualzar de la siguiente manera
![image](https://github.com/user-attachments/assets/2bb9f3e7-a52a-4169-84f6-e00d8df7a2b0)

Podemos ver como la IA siempre va a escoger el mayor puntaje, es decir, el que maximiza sus oportunidades de ganar.
