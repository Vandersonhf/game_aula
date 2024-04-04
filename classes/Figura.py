from config.Constantes import *

# definindo a função mover(), que registra a posição de uma figura
def mover(figura, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    if figura['objRect'].top < borda_superior or figura['objRect'].bottom > borda_inferior:
        # figura atingiu o topo ou a base da janela
        figura['vel'][1] = -figura['vel'][1]
    if figura['objRect'].left < borda_esquerda or figura['objRect'].right > borda_direita:
        # figura atingiu o lado esquerdo ou direito da janela
        figura['vel'][0] = -figura['vel'][0]
    figura['objRect'].x += figura['vel'][0]
    figura['objRect'].y += figura['vel'][1]