import time
import sys

# Aumentar o limite de recursão para DFS profunda
sys.setrecursionlimit(20000)

KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]

def build_graph(n: int) -> dict:
    """
    Constrói a Lista de Adjacência do tabuleiro.
    Chave: Nodo (linha, coluna)
    Valor: Lista de Nodos vizinhos alcançáveis com 1 salto em 'L'.
    """
    graph = {}
    for r in range(n):
        for c in range(n):
            neighbors = []
            for dx, dy in KNIGHT_MOVES:
                nr, nc = r + dx, c + dy
                # Validação de fronteira feita apenas uma vez na criação
                if 0 <= nr < n and 0 <= nc < n:
                    neighbors.append((nr, nc))
            graph[(r, c)] = neighbors
    return graph


def knight_tour(n: int, start_row: int, start_col: int):
    start_time = time.perf_counter()
    
    # 1. Constrói o Grafo
    graph = build_graph(n)
    total_squares = n * n
    
    # Estruturas de controle para a Busca em Profundidade (DFS)
    path = []
    visited = set()

    def get_dynamic_degree(node):
        """Calcula conexões futuras baseadas nos nodos ainda não visitados."""
        return sum(1 for neighbor in graph[node] if neighbor not in visited)

    def dfs(current_node):
        path.append(current_node)
        visited.add(current_node)

        # Condição de parada: caminho hamiltoniano encontrado
        if len(path) == total_squares:
            return True

        # Obtém os vizinhos direto do grafo (sem precisar calcular deltas)
        valid_neighbors = [neighbor for neighbor in graph[current_node] if neighbor not in visited]
        
        # Ordena vizinhos pelo grau (Heurística de Warnsdorff aplicada a Grafos)
        valid_neighbors.sort(key=get_dynamic_degree)

        for neighbor in valid_neighbors:
            if dfs(neighbor):
                return True

        # Backtrack: desfaz a visita
        visited.remove(current_node)
        path.pop()
        return False

    # Executa a busca
    start_node = (start_row, start_col)
    success = dfs(start_node)
    
    # 3. Transforma o 'path' do Grafo em Matriz para o Front-end ler
    board = [[-1] * n for _ in range(n)]
    if success:
        for step, (r, c) in enumerate(path, 1):
            board[r][c] = step

    exec_time = (time.perf_counter() - start_time) * 1000
    strategy = "Grafo de Adjacência + DFS"
    
    return success, board, path, exec_time, strategy


def can_have_solution_size(n: int) -> bool:
    return n == 1 or n >= 5


def can_have_solution_pos(n, x, y: int) -> bool:
    return (n % 2 != 1 or (x + y) % 2 != 1)
