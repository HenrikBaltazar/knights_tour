import time

# Os 8 movimentos em "L" possiveis do cavalo
KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]


def is_valid_move(board: list, row: int, col: int, n: int) -> bool:
    """Verifica se a posicao (row, col) e valida e ainda nao foi visitada."""
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1


def count_onward_moves(board: list, row: int, col: int, n: int) -> int:
    """
    Conta o numero de movimentos futuros validos a partir de (row, col).
    Esta e a essencia da Regra de Warnsdorff: escolhemos o proximo
    movimento que leva a casa com MENOS opcoes futuras, reduzindo
    drasticamente o espaco de busca.
    """
    count = 0
    for dr, dc in KNIGHT_MOVES:
        if is_valid_move(board, row + dr, col + dc, n):
            count += 1
    return count


def get_next_moves_sorted(board: list, row: int, col: int, n: int) -> list:
    """
    Retorna os proximos movimentos ordenados pela Regra de Warnsdorff
    (grau ascendente). Movimentos com menor numero de saidas futuras
    sao priorizados, o que evita becos sem saida.
    """
    moves = []
    for dr, dc in KNIGHT_MOVES:
        nr, nc = row + dr, col + dc
        if is_valid_move(board, nr, nc, n):
            degree = count_onward_moves(board, nr, nc, n)
            moves.append((degree, nr, nc))
    moves.sort()  # Ordena pelo grau (Warnsdorff)
    return [(r, c) for _, r, c in moves]


def solve_knight_tour(n: int, start_row: int, start_col: int):
    """
    Resolve o Passeio do Cavalo usando Backtracking + Warnsdorff.

    Complexidade teorica: O(N^2) com a heuristica de Warnsdorff,
    comparado a O(8^(N^2)) do backtracking puro (forca bruta).

    Retorna: (success, board, path, exec_time_ms)
    """
    start_time = time.perf_counter()

    board = [[-1] * n for _ in range(n)]
    path = [(start_row, start_col)]
    board[start_row][start_col] = 1
    total_squares = n * n

    def backtrack(row, col, move_num):
        if move_num > total_squares:
            return True

        for nr, nc in get_next_moves_sorted(board, row, col, n):
            board[nr][nc] = move_num
            path.append((nr, nc))

            if backtrack(nr, nc, move_num + 1):
                return True

            # Backtrack: desfaz o movimento
            board[nr][nc] = -1
            path.pop()

        return False

    success = backtrack(start_row, start_col, 2)
    exec_time = (time.perf_counter() - start_time) * 1000

    return success, board, path, exec_time


def can_have_solution(n: int) -> bool:
    """Tabuleiros menores que 5x5 (exceto 1x1) nao possuem solucao."""
    return n == 1 or n >= 5
