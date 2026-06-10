import time

# Os 8 movimentos em "L" possiveis do cavalo
KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]


def is_valid_move(board: list, row: int, col: int, n: int) -> bool:
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1 #Verifica se a posicao (row, col) e valida e ainda nao foi visitada.


def lookahead(board: list, row: int, col: int, n: int) -> int: #look-ahead
    count = 0
    for dx, dy in KNIGHT_MOVES:
        if is_valid_move(board, row + dx, col + dy, n):
            count += 1
    return count # retorna o grau da posicao atual, quantidade de movimentos possiveis


def warnsdorff(board: list, row: int, col: int, n: int) -> list:
    moves = []
    for dx, dy in KNIGHT_MOVES:
        x, y = row + dx, col + dy
        if is_valid_move(board, x, y, n):
            degree = lookahead(board, x, y, n)
            moves.append((degree, x, y))
    moves.sort()  # Ordena pelo grau ascendente (Warnsdorff)
    return [(r, c) for _, r, c in moves]


def knight_tour(n: int, start_row: int, start_col: int):
    start_time = time.perf_counter() #contador do tempo de execucao

    board = [[-1] * n for _ in range(n)] #definicao do tabuleiro (lista de listas)
    path = [(start_row, start_col)] #caminho percorrido pelo cavalo
    board[start_row][start_col] = 1 #posicao inicial do cavalo

    total_squares = n * n #quantidade total de casas a serem visitadas

    def backtrack(row, col, move_num): 
        if move_num > total_squares: #condicao de parada, todas as casas foram visitadas
            return True

        for x, y in warnsdorff(board, row, col, n): #chama o algoritmo de decisao do proximo movimento a executar
            board[x][y] = move_num #visita o tabuleiro
            path.append((x, y)) #incrementa o caminho

            if backtrack(x, y, move_num + 1): 
                return True

            # Backtrack: desfaz o movimento
            board[x][y] = -1
            path.pop()

        return False

    success = backtrack(start_row, start_col, 2)
    exec_time = (time.perf_counter() - start_time) * 1000

    return success, board, path, exec_time


def can_have_solution_size(n: int) -> bool: # Tabuleiros menores que 5x5 (exceto 1x1) nao possuem solucao.
    return n == 1 or n >= 5

def can_have_solution_pos(n,x,y: int) -> bool: # Tabuleiros de tamanho impar e posicao inicial (x+y)%2 == 1 nao possuem solucao
    return (n%2!=1 or (x+y)%2!=1)