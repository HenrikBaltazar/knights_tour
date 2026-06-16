# Passeio do Cavalo
O objetivo deste trabalho é implementar uma evolução à solução inicial para o
Problema do Passeio do Cavalo (Knight's Tour). 

O problema consiste em encontrar um caminho válido para que um cavalo de
xadrez visite todas as casas de um tabuleiro exatamente uma vez, seguindo as
regras tradicionais de movimentação da peça (em "L"). Trata-se de um problema
clássico com alta complexidade computacional, onde o espaço de busca cresce
exponencialmente conforme o tamanho do tabuleiro aumenta.
 
## Requisitos técnicos da implementação
- Linguagem de Programação: Livre escolha da equipe. **(Python)**
- Tamanho do Tabuleiro: A aplicação deve suportar tabuleiros de tamanhos
variáveis (N x N), definidos pelo usuário no início da execução.
- Posição Inicial: A coordenada de partida do cavalo (X, Y) também deve ser
parametrizável e escolhida pelo usuário antes da execução.
- Visualização: O programa deve ser capaz de exibir o caminho percorrido
pelo cavalo de forma compreensível (ex: matriz numerada com a ordem
dos saltos). **(TkinterBootstrap)**

## Autoria
- Curso: Ciencia da Computacao - UNIVALI
- Disciplina: Teoria da Computacao
- Professor: Ramices dos Santos Silva
- Alunos: Henrik Baltazar, Arthur de Oliveira Pereira e Gustavo Cezar

## Execução
1. `python -m venv venv`
2. `venv\Scripts\activate` (ou source `venv/bin/activate` em sistemas UNIX)
3. `pip install -r requirements.txt`
4. `python main.py` (ou `python main --cli` para vizualizar apenas o tempo de execução sem interface)

## Licença
MIT
