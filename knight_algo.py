import time

KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]

def is_valid_move(board: list, row: int, col: int, n: int) -> bool:
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1

def lookahead(board: list, row: int, col: int, n: int) -> int:
    count = 0
    for dx, dy in KNIGHT_MOVES:
        if is_valid_move(board, row + dx, col + dy, n):
            count += 1
    return count

def warnsdorff(board: list, row: int, col: int, n: int) -> list:
    moves = []
    for dx, dy in KNIGHT_MOVES:
        x, y = row + dx, col + dy
        if is_valid_move(board, x, y, n):
            degree = lookahead(board, x, y, n)
            moves.append((degree, x, y))
    moves.sort() 
    return [(r, c) for _, r, c in moves]

def knight_tour(n: int, start_row: int, start_col: int):
    start_time = time.perf_counter()

    board = [[-1] * n for _ in range(n)]
    board[start_row][start_col] = 1
    total_squares = n * n

    # A pilha armazena: (linha_atual, coluna_atual, move_num, lista_de_proximos_movimentos)
    # Começamos com os movimentos possíveis a partir da casa inicial
    first_moves = warnsdorff(board, start_row, start_col, n)
    stack = [(start_row, start_col, 2, first_moves)]
    
    path = [(start_row, start_col)]
    success = False

    while stack:
        row, col, move_num, moves_to_try = stack[-1]

        if move_num > total_squares:
            success = True
            break

        if moves_to_try:
            # Pega o próximo movimento candidato (Warnsdorff já ordenou)
            next_x, next_y = moves_to_try.pop(0)
            
            # Executa o movimento
            board[next_x][next_y] = move_num
            path.append((next_x, next_y))
            
            # Gera os movimentos para a nova posição e empilha
            next_possible_moves = warnsdorff(board, next_x, next_y, n)
            stack.append((next_x, next_y, move_num + 1, next_possible_moves))
        else:
            # Backtrack manual: se não há mais movimentos para tentar nesta casa, desempilha
            curr_row, curr_col, m_num, _ = stack.pop()
            # Se não for a raiz, limpa o tabuleiro para permitir novas tentativas
            if stack:
                board[curr_row][curr_col] = -1
                path.pop()

    exec_time = (time.perf_counter() - start_time) * 1000
    return success, board, path, exec_time

def can_have_solution_size(n: int) -> bool: # Tabuleiros menores que 5x5 (exceto 1x1) nao possuem solucao.
    return n == 1 or n >= 5

def can_have_solution_pos(n,x,y: int) -> bool: # Tabuleiros de tamanho impar e posicao inicial (x+y)%2 == 1 nao possuem solucao
    return (n%2!=1 or (x+y)%2!=1)