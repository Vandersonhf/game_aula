import pygame
from .Events import trata_eventos, aguardarEntrada
from .GameDisplay import draw_background, colocarTexto
from .Constantes import *
from classes.Inimigos import set_enemies, update_enemies
from classes.Jogador import update_player, get_player

def start(janela):
    # Tela de inicio.
    colocarTexto('Asteroides Troianos', fonte, janela,
                (LARGURAJANELA / 2), (ALTURAJANELA / 2)-font_size, 'center')
    colocarTexto('Pressione F1 para começar.', fonte, janela,
                (LARGURAJANELA / 2), (ALTURAJANELA / 2)+font_size, 'center')
    colocarTexto('Pressione ESC para sair.', fonte, janela,
                     (LARGURAJANELA / 2), (ALTURAJANELA / 2)+font_size*2, 'center')
    pygame.display.update()
    aguardarEntrada()
    
    recorde = 0
    while True:
        # Configurando o começo do jogo.
        asteroides = [] # lista com os asteroides
        raios = [] # lista com os raios
        pontuacao = 0 # pontuação
        deve_continuar = True # indica se o loop do jogo deve continuar
        
        # direções de movimentação
        teclas = {}
        teclas['esquerda'] = teclas['direita'] = teclas['cima'] = teclas['baixo'] = False
        contador = 0 # contador de iterações
        pygame.mixer.music.play(-1, 0.0) # colocando a música de fundo
        # criando um objeto pygame.time.Clock        
        relogio = pygame.time.Clock()
        
        # criar jogador
        jogador = get_player()
        
        #repetição principal
        recorde = main_loop(janela, jogador, asteroides, raios, relogio,
                  recorde, teclas, pontuacao, deve_continuar, contador)
        
        # Parando o jogo e mostrando a tela final.
        pygame.mixer.music.stop()
        somFinal.play()                
        colocarTexto('GAME OVER', fonte, janela,
                     (LARGURAJANELA / 2), (ALTURAJANELA / 2)-font_size, 'center')
        colocarTexto('Pressione F1 para jogar.', fonte, janela,
                     (LARGURAJANELA / 2), (ALTURAJANELA / 2)+font_size, 'center')
        colocarTexto('Pressione ESC para sair.', fonte, janela,
                     (LARGURAJANELA / 2), (ALTURAJANELA / 2)+font_size*2, 'center')
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        aguardarEntrada()
        somFinal.stop()
        

def main_loop(janela, jogador, asteroides, raios, relogio,
              recorde, teclas, pontuacao, deve_continuar, contador):
    while deve_continuar:
        pontuacao += 1        
            
        # preenchendo o fundo de janela com a sua imagem
        draw_background(janela, pontuacao, recorde)
        
        #verifica evetos e atualiza em memória       
        deve_continuar = trata_eventos(teclas,jogador,raios)
        
        #criar inimigos
        contador += 1;        
        contador = set_enemies(asteroides, contador) 
        #atualiza inimigos
        update_enemies(janela, asteroides, raios) 
        
        #atualiza jogador      
        deve_continuar = update_player(janela, jogador, teclas, asteroides,
                                       raios)
        if not deve_continuar and pontuacao > recorde:
            recorde = pontuacao        
            somRecorde.play()
        
        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()        
        # limitando a 60 quadros por segundo
        relogio.tick(60)
    return recorde
       
       
