"""
Plota duas series de medidas (M1 e M3) em milissegundos, usando o tamanho
do tabuleiro (ex: "8x8") como referencia no eixo X.

Uso:
    python plot_m1_m3.py

Ou importando a funcao em outro script:
    from plot_m1_m3 import plot_m1_m3
    plot_m1_m3(M1, M3)
"""

import matplotlib.pyplot as plt


def _board_size_to_int(label: str) -> int:
    """Converte um rotulo tipo '8x8' no inteiro 8, usado para ordenar/posicionar no eixo X."""
    return int(label.split("x")[0])


def plot_m1_m3(M1: dict[str, float], M3: dict[str, float], save_path: str | None = None):
    """
    Plota M1 e M3 no mesmo grafico, usando o tamanho do tabuleiro como eixo X.

    Parametros
    ----------
    M1, M3 : dict[str, float]
        Mapeamento {"NxN": tempo_em_ms}. Os dois dicionarios nao precisam
        ter as mesmas chaves (ex: M3 pode nao ter "65x65").
    save_path : str, opcional
        Se informado, salva a figura nesse caminho (ex: "grafico.png")
        em vez de exibi-la.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Ordena cada serie pelo tamanho do tabuleiro
    m1_items = sorted(M1.items(), key=lambda kv: _board_size_to_int(kv[0]))
    m3_items = sorted(M3.items(), key=lambda kv: _board_size_to_int(kv[0]))

    x1 = [_board_size_to_int(k) for k, _ in m1_items]
    y1 = [v for _, v in m1_items]

    x3 = [_board_size_to_int(k) for k, _ in m3_items]
    y3 = [v for _, v in m3_items]

    ax.plot(x1, y1, label="M1", color="tab:blue", marker="o", markersize=5)
    ax.plot(x3, y3, label="M3", color="tab:orange", marker="o", markersize=5)

    # Eixo X mostra o rotulo original ("8x8", "12x12", ...), nao so o numero
    todos_labels = {k: k for k, _ in m1_items}
    todos_labels.update({k: k for k, _ in m3_items})
    xticks_ordenados = sorted(todos_labels.keys(), key=_board_size_to_int)
    ax.set_xticks([_board_size_to_int(k) for k in xticks_ordenados])
    ax.set_xticklabels(xticks_ordenados)

    ax.set_xlabel("Tamanho do tabuleiro")
    ax.set_ylabel("Tempo (ms)")
    ax.set_title("M1 vs M3")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
        print(f"Grafico salvo em: {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    M3 = {
        "8x8": 0.25,
        "12x12": 0.63,
        "16x16": 1.08,
        "24x24": 3.30,
        "31x31": 4.39,
        "65x65": 20.46,
    }

    M1 = {
        "8x8": 0.36,
        "12x12": 0.88,
        "16x16": 1.68,
        "24x24": 4.69,
        "31x31": 6.77,
    }

    plot_m1_m3(M1, M3)
