from config.Constantes import *

def trata_eventos(pygame,teclas,blocos):
    #print("Tratando...")
    for evento in pygame.event.get():
        # Se for um evento QUIT
        if evento.type == pygame.QUIT:
            print("Saindo...")            
            return False
        
        # quando uma tecla é pressionada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas['esquerda'] = True
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas['direita'] = True
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas['cima'] = True
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas['baixo'] = True
        
        # quando uma tecla é solta
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas['esquerda'] = False
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas['direita'] = False
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas['cima'] = False
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas['baixo'] = False
        
        # quando um botao do mouse é pressionado
        if evento.type == pygame.MOUSEBUTTONDOWN:
            blocos.append({'objRect': pygame.Rect(evento.pos[0], evento.pos[1],
                        TAMANHOBLOCO, TAMANHOBLOCO), 'cor': BRANCO, 'vel': 1})
        
    return True

