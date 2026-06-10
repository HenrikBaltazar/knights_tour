import time
import sys

# Aumentar o limite de recursão para tabuleiros maiores (ex: 24x24)
sys.setrecursionlimit(20000)

# Os 8 movimentos em "L" possiveis do cavalo
KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]


def is_valid_move(board: list, row: int, col: int, n: int) -> bool:
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1


def knight_tour_m1(n: int, start_row: int, start_col: int, target_end=None):
    """
    Abordagem do M1 modificada para suportar um ponto de término obrigatório (M3 Constrained).
    """
    board = [[-1] * n for _ in range(n)]
    path = [(start_row, start_col)]
    board[start_row][start_col] = 1
    total_squares = n * n

    def is_valid_constrained(r, c, move_num):
        if 0 <= r < n and 0 <= c < n and board[r][c] == -1:
            # Oculta a célula final para a heurística até o último movimento exato
            if target_end and (r, c) == target_end and move_num < total_squares:
                return False
            return True
        return False

    def get_degree(r, c, move_num):
        count = 0
        for dx, dy in KNIGHT_MOVES:
            if is_valid_constrained(r + dx, c + dy, move_num):
                count += 1
        return count

    def warnsdorff(r, c, move_num):
        moves = []
        for dx, dy in KNIGHT_MOVES:
            nr, nc = r + dx, c + dy
            if is_valid_constrained(nr, nc, move_num):
                moves.append((get_degree(nr, nc, move_num), nr, nc))
        moves.sort()  # Grau ascendente
        return [(nr, nc) for _, nr, nc in moves]

    def backtrack(row, col, move_num):
        if move_num > total_squares:
            return True

        for x, y in warnsdorff(row, col, move_num):
            board[x][y] = move_num
            path.append((x, y))

            if backtrack(x, y, move_num + 1):
                return True

            board[x][y] = -1
            path.pop()

        return False

    success = backtrack(start_row, start_col, 2)
    return success, board, path


def get_quadrant_sequence(start_row: int, start_col: int, half: int):
    """
    Ordena a sequência de visitação dos 4 quadrantes garantindo que inicie no quadrante clicado.
    """
    # Mapeamento dos offsets: 0: Top-Left, 1: Top-Right, 2: Bottom-Right, 3: Bottom-Left
    quadrants = [(0, 0), (0, half), (half, half), (half, 0)]
    
    start_idx = 0
    if start_row < half and start_col >= half: start_idx = 1
    elif start_row >= half and start_col >= half: start_idx = 2
    elif start_row >= half and start_col < half: start_idx = 3

    # Rotaciona para iniciar pelo quadrante onde o cavalo foi posicionado
    return quadrants[start_idx:] + quadrants[:start_idx]


def find_bridge(qa_off, qb_off, half, avoid_cells):
    """
    Busca nas células de borda um par (saída, entrada) separados por 1 movimento válido.
    """
    for r1 in range(qa_off[0], qa_off[0] + half):
        for c1 in range(qa_off[1], qa_off[1] + half):
            if (r1, c1) in avoid_cells: continue
            
            for dx, dy in KNIGHT_MOVES:
                r2, c2 = r1 + dx, c1 + dy
                # Verifica se o salto pousa no quadrante vizinho
                if qb_off[0] <= r2 < qb_off[0] + half and qb_off[1] <= c2 < qb_off[1] + half:
                    if (r2, c2) not in avoid_cells:
                        return (r1, c1), (r2, c2)
    return None, None


def run_dc(n: int, start_row: int, start_col: int):
    """
    Implementação da abordagem Divisão e Conquista.
    """
    half = n // 2
    seq = get_quadrant_sequence(start_row, start_col, half)
    
    used_cells = {(start_row, start_col)}
    bridges = []
    
    # 1. Pré-processar as pontes entre os quadrantes
    for i in range(3):
        ex, en = find_bridge(seq[i], seq[i+1], half, used_cells)
        if not ex: return False, [], []
        bridges.append((ex, en))
        used_cells.add(ex)
        used_cells.add(en)

    full_path = []
    board = [[-1] * n for _ in range(n)]

    # 2. Conquistar cada quadrante independentemente
    for i in range(4):
        q_off = seq[i]
        
        # Ponto de entrada global
        if i == 0:
            g_start = (start_row, start_col)
        else:
            g_start = bridges[i-1][1]
            
        # Converter para local
        l_start = (g_start[0] - q_off[0], g_start[1] - q_off[1])
        
        # Ponto de saída global (o último quadrante é livre e não precisa convergir pra borda)
        if i < 3:
            g_end = bridges[i][0]
            l_end = (g_end[0] - q_off[0], g_end[1] - q_off[1])
        else:
            l_end = None
            
        success, _, q_path = knight_tour_m1(half, l_start[0], l_start[1], l_end)
        
        if not success:
            return False, [], []
            
        # 3. Combinar: Converter caminho local para matriz global
        for lr, lc in q_path:
            gr, gc = lr + q_off[0], lc + q_off[1]
            full_path.append((gr, gc))
            
    # Reconstruir o mapa numérico
    for move_num, (r, c) in enumerate(full_path, 1):
        board[r][c] = move_num
        
    return True, board, full_path


def knight_tour(n: int, start_row: int, start_col: int):
    start_time = time.perf_counter()
    strategy = "M1 Direto"

    # Critério de Divisão (N par e tamanho de quadrante >= 6)
    if n % 2 == 0 and (n // 2) >= 6:
        success, board, path = run_dc(n, start_row, start_col)
        if success:
            strategy = "D&C Híbrido"
        else:
            # Fallback seguro: Em raras configurações onde o target_end causa estrangulamento.
            success, board, path = knight_tour_m1(n, start_row, start_col)
    else:
        success, board, path = knight_tour_m1(n, start_row, start_col)

    exec_time = (time.perf_counter() - start_time) * 1000
    return success, board, path, exec_time, strategy


def can_have_solution_size(n: int) -> bool:
    return n == 1 or n >= 5


def can_have_solution_pos(n, x, y: int) -> bool:
    # A restrição de paridade aplica-se apenas aos tabuleiros ímpares
    return (n % 2 != 1 or (x + y) % 2 != 1)
