

def trata_eventos(pygame):
    #print("Tratando...")
    for event in pygame.event.get():
        # Se for um evento QUIT
        if event.type == pygame.QUIT:
            print("Saindo...")            
            return False
    return True

