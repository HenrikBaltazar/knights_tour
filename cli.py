import sys
from knight_algo import knight_tour, can_have_solution_size, can_have_solution_pos

def main():
    print("=== PASSEIO DO CAVALO (M3: MODO CLI) ===")
    
    try:
        n = int(input("Digite o tamanho do tabuleiro (N x N): "))
        start_row = int(input(f"Digite a linha inicial (0 a {n-1}): "))
        start_col = int(input(f"Digite a coluna inicial (0 a {n-1}): "))
    except ValueError:
        print("\n[Erro] Por favor, digite apenas números inteiros válidos.")
        return

    # Validações lógicas pré-execução
    if not (0 <= start_row < n and 0 <= start_col < n):
        print("\n[Erro] Coordenadas iniciais fora dos limites do tabuleiro.")
        return
        
    if not can_have_solution_size(n):
        print(f"\n[Aviso] Tabuleiros de tamanho {n}x{n} matematicamente não possuem solução.")
        return
        
    if not can_have_solution_pos(n, start_row, start_col):
        print(f"\n[Aviso] A posição ({start_row}, {start_col}) em tabuleiros {n}x{n} viola restrições de paridade.")
        return

    print("\n[Processando] Construindo grafo e computando a DFS...")
    
    # Executa o motor algorítmico da M3
    success, board, path, exec_time, strategy = knight_tour(n, start_row, start_col)

    if success:
        print("\n=== SUCESSO! PASSEIO COMPLETO ENCONTRADO ===")
        print(f"Estratégia: {strategy}")
        print(f"Tempo de Execução: {exec_time:.2f} ms")
    else:
        print("\n[Falha] O algoritmo não conseguiu encontrar um caminho válido.")

if __name__ == "__main__":
    main()
