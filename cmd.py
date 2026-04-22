import time
import sys
from knight_algo import knight_tour, can_have_solution_size, can_have_solution_pos

def run_cli_benchmark():
    print("-" * 40)
    print("KNIGHT'S TOUR - BENCHMARK MODE (CLI)")
    print("-" * 40)

    try:
        n = int(input("Tamanho do tabuleiro (N x N): "))
        x = int(input(f"Posição inicial X (0 a {n-1}): "))
        y = int(input(f"Posição inicial Y (0 a {n-1}): "))
    except ValueError:
        print("\n[Erro] Entrada inválida. Use apenas números inteiros.")
        return

    # Validações rápidas usando suas funções existentes
    if not can_have_solution_size(n):
        print(f"[Aviso] Tabuleiros {n}x{n} geralmente não possuem solução.")
    if not can_have_solution_pos(n, x, y):
        print(f"[Aviso] Posição ({x},{y}) pode ser matematicamente impossível neste tabuleiro.")

    print(f"\nIniciando busca em tabuleiro {n}x{n} a partir de ({x}, {y})...")
    print("Pressione Ctrl+C para abortar se demorar demais.\n")

    # Início do processamento
    start_time = time.perf_counter()
    
    # Nota: Como o knight_tour original é síncrono, para exibir um contador em tempo real 
    # precisaríamos de threads ou alterar o knight_algo. 
    # Para manter o seu knight_algo intocado (como solicitado antes), 
    # o tempo será medido após o retorno.
    
    try:
        success, board, path, exec_time = knight_tour(n, x, y)

        if success:
            print(f"\n[SUCESSO] Solução encontrada!")
            print(f"Caminho completo: {len(path)} casas visitadas.")
        else:
            print(f"\n[FALHA] Não foi possível completar o passeio.")

        print("-" * 40)
        print(f"Tempo total: {exec_time:.2f} ms")
        print("-" * 40)

    except KeyboardInterrupt:
        print("\n\n[Abortado] Execução interrompida pelo usuário.")

if __name__ == "__main__":
    run_cli_benchmark()